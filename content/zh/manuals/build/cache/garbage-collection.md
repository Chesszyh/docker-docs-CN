---
title: 构建垃圾回收
description: 了解 BuildKit 守护进程中的垃圾回收
keywords: build, buildx, buildkit, garbage collection, prune, gc
aliases:
  - /build/building/cache/garbage-collection/
---

虽然 [`docker builder prune`](/reference/cli/docker/builder/prune.md)
或 [`docker buildx prune`](/reference/cli/docker/buildx/prune.md)
命令是一次性运行的，但垃圾回收（GC）是定期运行的，并遵循一个有序的清理策略列表。当缓存大小变得过大或缓存过期时，BuildKit 守护进程会清理构建缓存。

对于大多数用户来说，默认的 GC 行为已经足够，不需要任何干预。高级用户，特别是那些处理大规模构建、自管理构建器或受限存储环境的用户，可能会受益于自定义这些设置以更好地适应他们的工作流程需求。以下章节解释了 GC 的工作原理，并提供了通过自定义配置调整其行为的指南。

## 垃圾回收策略

GC 策略定义了一组规则，用于确定如何管理和清理构建缓存。这些策略包括何时删除缓存条目的标准，例如缓存的使用时间、使用的空间量以及要清理的缓存记录类型。

每个 GC 策略按顺序评估，从最具体的标准开始，如果之前的策略没有释放足够的缓存，则继续执行更广泛的规则。这使得 BuildKit 能够对缓存条目进行优先级排序，在确保系统保持性能和可用性的同时，保留最有价值的缓存。

例如，假设你有以下 GC 策略：

1. 查找过去 48 小时内未使用的"过期"缓存记录，并删除记录，直到剩余最多 5GB 的"过期"缓存。
2. 如果构建缓存大小超过 10GB，则删除记录，直到总缓存大小不超过 10GB。

第一条规则更具体，优先处理过期缓存记录，并为价值较低的缓存类型设置较低的限制。第二条规则对任何类型的缓存记录施加较高的硬限制。使用这些策略，如果你有 11GB 的构建缓存，其中：

- 7GB 是"过期"缓存
- 4GB 是其他更有价值的缓存

GC 清理将删除 5GB 的过期缓存作为第一条策略的一部分，剩余 6GB，这意味着第二条策略不需要清理更多缓存。

默认的 GC 策略（大致）如下：

1. 如果超过 48 小时未使用，则删除可以轻松重新生成的缓存，例如来自本地目录或远程 Git 仓库的构建上下文，以及缓存挂载。
2. 删除超过 60 天未在构建中使用的缓存。
3. 删除超过构建缓存大小限制的非共享缓存。非共享缓存记录是指其他资源（通常作为镜像层）未使用的层 blob。
4. 删除任何超过构建缓存大小限制的构建缓存。

具体的算法和配置策略的方式因你使用的构建器类型而略有不同。有关更多详细信息，请参阅[配置](#configuration)。

## 配置

> [!NOTE]
> 如果你对默认的垃圾回收行为感到满意，不需要微调其设置，可以跳过本节。默认配置适用于大多数用例，不需要额外设置。

根据你使用的[构建驱动程序](../builders/drivers/_index.md)类型，你将使用不同的配置文件来更改构建器的 GC 设置：

- 如果你使用 Docker Engine 的默认构建器（`docker` 驱动程序），请使用 [Docker 守护进程配置文件](#docker-daemon-configuration-file)。
- 如果你使用自定义构建器，请使用 [BuildKit 配置文件](#buildkit-configuration-file)。

### Docker 守护进程配置文件

如果你使用默认的 [`docker` 驱动程序](../builders/drivers/docker.md)，GC 在 [`daemon.json` 配置文件](/reference/cli/dockerd.md#daemon-configuration-file)中配置，或者如果你使用 Docker Desktop，则在[**设置 > Docker Engine**](/manuals/desktop/settings-and-maintenance/settings.md)中配置。

以下代码片段显示了 Docker Desktop 用户的 `docker` 驱动程序的默认构建器配置：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  }
}
```

`defaultKeepStorage` 选项配置构建缓存的大小限制，这会影响 GC 策略。`docker` 驱动程序的默认策略工作方式如下：

1. 如果超过 `defaultKeepStorage` 的 13.8%（或最小 512MB），则删除超过 48 小时未使用的临时构建缓存。
2. 删除超过 60 天未使用的构建缓存。
3. 删除超过 `defaultKeepStorage` 限制的非共享构建缓存。
4. 删除任何超过 `defaultKeepStorage` 限制的构建缓存。

鉴于 Docker Desktop 的 `defaultKeepStorage` 默认值为 20GB，默认 GC 策略解析为：

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "policy": [
        {
          "keepStorage": "2.764GB",
          "filter": [
            "unused-for=48h",
            "type==source.local,type==exec.cachemount,type==source.git.checkout"
          ]
        },
        { "keepStorage": "20GB", "filter": ["unused-for=1440h"] },
        { "keepStorage": "20GB" },
        { "keepStorage": "20GB", "all": true }
      ]
    }
  }
}
```

调整 `docker` 驱动程序构建缓存配置的最简单方法是调整 `defaultKeepStorage` 选项：

- 如果你觉得 GC 过于激进，请增加限制。
- 如果你需要保留空间，请减少限制。

如果你需要更多控制，可以直接定义自己的 GC 策略。以下示例定义了一个更保守的 GC 配置，具有以下策略：

1. 如果构建缓存超过 50GB，则删除超过 1440 小时（即 60 天）未使用的缓存条目。
2. 如果构建缓存超过 50GB，则删除非共享缓存条目。
3. 如果构建缓存超过 100GB，则删除任何缓存条目。

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "50GB",
      "policy": [
        { "keepStorage": "0", "filter": ["unused-for=1440h"] },
        { "keepStorage": "0" },
        { "keepStorage": "100GB", "all": true }
      ]
    }
  }
}
```

这里的策略 1 和 2 将 `keepStorage` 设置为 `0`，这意味着它们将回退到由 `defaultKeepStorage` 定义的 50GB 的默认限制。

### BuildKit 配置文件

对于 `docker` 以外的构建驱动程序，GC 使用 [`buildkitd.toml`](../buildkit/toml-configuration.md) 配置文件进行配置。此文件使用以下高级配置选项，你可以使用这些选项来调整 BuildKit 应该用于缓存的磁盘空间阈值：

| 选项            | 描述                                                                                                         | 默认值                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------- |
| `reservedSpace` | BuildKit 允许为缓存分配的最小磁盘空间量。低于此阈值的使用量在垃圾回收期间不会被回收。                                   | 总磁盘空间的 10% 或 10GB（取较小者）              |
| `maxUsedSpace`  | BuildKit 允许使用的最大磁盘空间量。超过此阈值的使用量将在垃圾回收期间被回收。                                          | 总磁盘空间的 60% 或 100GB（取较小者）             |
| `minFreeSpace`  | 必须保持空闲的磁盘空间量。                                                                                      | 20GB                                          |

你可以将这些选项设置为字节数、单位字符串（例如，`512MB`）或总磁盘大小的百分比。更改这些选项会影响 BuildKit worker 使用的默认 GC 策略。使用默认阈值，GC 策略解析如下：

```toml
# 全局默认值
[worker.oci]
  gc = true
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"
  minFreeSpace = "20%"

# 策略 1
[[worker.oci.gcpolicy]]
  filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout" ]
  keepDuration = "48h"
  maxUsedSpace = "512MB"

# 策略 2
[[worker.oci.gcpolicy]]
  keepDuration = "1440h" # 60 天
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"

# 策略 3
[[worker.oci.gcpolicy]]
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"

# 策略 4
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"
```

实际上，这意味着：

- 策略 1：如果构建缓存超过 512MB，BuildKit 会删除过去 48 小时内未使用的本地构建上下文、远程 Git 上下文和缓存挂载的缓存记录。
- 策略 2：如果磁盘使用量超过 100GB，则删除超过 60 天的非共享构建缓存，确保至少保留 10GB 的磁盘空间用于缓存。
- 策略 3：如果磁盘使用量超过 100GB，则删除任何非共享缓存，确保至少保留 10GB 的磁盘空间用于缓存。
- 策略 4：如果磁盘使用量超过 100GB，则删除所有缓存——包括共享和内部记录，确保至少保留 10GB 的磁盘空间用于缓存。

`reservedSpace` 在定义构建缓存大小的下限时具有最高优先级。如果 `maxUsedSpace` 或 `minFreeSpace` 定义了较低的值，最小缓存大小永远不会低于 `reservedSpace`。

如果同时设置了 `reservedSpace` 和 `maxUsedSpace`，GC 清理的结果缓存大小将在这些阈值之间。例如，如果 `reservedSpace` 设置为 10GB，`maxUsedSpace` 设置为 20GB，则 GC 运行后的缓存量将小于 20GB，但至少为 10GB。

你还可以定义完全自定义的 GC 策略。自定义策略还允许你定义过滤器，让你可以精确指定给定策略允许清理的缓存条目类型。

#### BuildKit 中的自定义 GC 策略

自定义 GC 策略让你可以微调 BuildKit 管理其缓存的方式，并让你可以根据缓存类型、持续时间或磁盘空间阈值等标准完全控制缓存保留。如果你需要完全控制缓存阈值以及缓存记录应如何优先处理，定义自定义 GC 策略是最佳选择。

要定义自定义 GC 策略，请在 `buildkitd.toml` 中使用 `[[worker.oci.gcpolicy]]` 配置块。每个策略定义将用于该策略的阈值。如果你使用自定义策略，`reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 的全局值不适用。

以下是一个示例配置：

```toml
# 自定义 GC 策略 1：删除超过 24 小时未使用的本地上下文
[[worker.oci.gcpolicy]]
  filters = ["type==source.local"]
  keepDuration = "24h"
  reservedSpace = "5GB"
  maxUsedSpace = "50GB"

# 自定义 GC 策略 2：删除超过 30 天的远程 Git 上下文
[[worker.oci.gcpolicy]]
  filters = ["type==source.git.checkout"]
  keepDuration = "720h"
  reservedSpace = "5GB"
  maxUsedSpace = "30GB"

# 自定义 GC 策略 3：如果磁盘使用量超过 90GB，则积极清理所有缓存
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "5GB"
  maxUsedSpace = "90GB"
```

除了 `reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 阈值外，在定义 GC 策略时，你还有两个额外的配置选项：

- `all`：默认情况下，BuildKit 会排除某些缓存记录在 GC 期间被清理。将此选项设置为 `true` 将允许清理任何缓存记录。
- `filters`：过滤器让你可以指定 GC 策略允许清理的特定类型的缓存记录。
