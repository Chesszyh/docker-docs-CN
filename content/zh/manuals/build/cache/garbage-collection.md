---
title: 构建垃圾回收
description: 了解 BuildKit 守护进程中的垃圾回收。
keywords: build, buildx, buildkit, 垃圾回收, prune, gc
---

虽然 [`docker builder prune`](/reference/cli/docker/builder/prune.md) 或 [`docker buildx prune`](/reference/cli/docker/buildx/prune.md) 命令是一次性运行的，但垃圾回收 (GC) 会定期运行并遵循有序的清理策略列表。当缓存大小变得过大或缓存时间过期时，BuildKit 守护进程会清除构建缓存。

对于大多数用户来说，默认的 GC 行为已经足够，不需要任何干预。高级用户，特别是那些处理大规模构建、使用自管构建器或受限存储环境的用户，可能会从自定义这些设置中受益，以便更好地与其工作流需求保持一致。以下章节解释了 GC 的工作原理，并提供了关于通过自定义配置调整其行为的指导。

## 垃圾回收策略

GC 策略定义了一组规则，决定了构建缓存的管理和清理方式。这些策略包括删除缓存条目的标准，例如缓存的时间、正在使用的空间量以及要清理的缓存记录类型。

每条 GC 策略按顺序评估，从最具体的标准开始，如果之前的策略没有释放足够的缓存，则继续执行更广泛的规则。这让 BuildKit 能够优先处理缓存条目，在确保系统维持性能和可用性的同时，保留最有价值的缓存。

例如，假设您有以下 GC 策略：

1. 查找在过去 48 小时内未使用的“陈旧”缓存记录，并删除记录，直到剩下最多 5GB 的“陈旧”缓存。
2. 如果构建缓存大小超过 10GB，则删除记录，直到总缓存大小不超过 10GB。

第一条规则更具体，优先处理陈旧的缓存记录，并为价值较低的缓存类型设置较低的限制。第二条规则施加了一个更高的硬限制，适用于任何类型的缓存记录。有了这些策略，如果您有 11GB 的构建缓存，其中：

- 其中 7GB 是“陈旧”缓存
- 4GB 是其他更有价值的缓存

GC 扫描将根据第一条策略删除 5GB 的陈旧缓存，剩余 6GB，这意味着第二条策略不需要再清除任何缓存。

默认的 GC 策略（大约）如下：

1. 如果超过 48 小时未使用，则删除可以轻松重新生成的缓存，例如来自本地目录或远程 Git 仓库的构建上下文，以及缓存挂载。
2. 删除在构建中超过 60 天未使用的缓存。
3. 删除超过构建缓存大小限制的非共享缓存。非共享缓存记录是指不被其他资源（通常是作为镜像层）使用的层 blob。
4. 删除任何超过构建缓存大小限制的构建缓存。

精确的算法和配置策略的方式略有不同，具体取决于您使用的构建器类型。有关更多详细信息，请参阅 [配置](#配置)。

## 配置

> [!NOTE]
> 如果您对默认的垃圾回收行为感到满意，并且不需要微调其设置，可以跳过本节。默认配置适用于大多数用例，不需要额外设置。

根据您使用的 [构建驱动程序](../builders/drivers/_index.md) 类型，您将使用不同的配置文件来更改构建器的 GC 设置：

- 如果您使用 Docker Engine 的默认构建器（`docker` 驱动程序），请使用 [Docker 守护进程配置文件](#docker-守护进程配置文件)。
- 如果您使用自定义构建器，请使用 [BuildKit 配置文件](#buildkit-配置文件)。

### Docker 守护进程配置文件

如果您使用的是默认的 [`docker` 驱动程序](../builders/drivers/docker.md)，GC 将在 [`daemon.json` 配置文件](/reference/cli/dockerd.md#daemon-configuration-file) 中进行配置，或者如果您使用 Docker Desktop，则在 [**Settings > Docker Engine**](/manuals/desktop/settings-and-maintenance/settings.md) 中进行配置。

以下代码片段显示了 Docker Desktop 用户使用 `docker` 驱动程序的默认构建器配置：

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

`defaultKeepStorage` 选项配置了构建缓存的大小限制，这会影响 GC 策略。`docker` 驱动程序的默认策略工作方式如下：

1. 如果超过 `defaultKeepStorage` 的 13.8%，或至少 512MB，则删除超过 48 小时的临时的、未使用的构建缓存。
2. 删除超过 60 天未使用的构建缓存。
3. 删除超过 `defaultKeepStorage` 限制的非共享构建缓存。
4. 删除任何超过 `defaultKeepStorage` 限制的构建缓存。

鉴于 Docker Desktop 的 `defaultKeepStorage` 默认值为 20GB，默认的 GC 策略解析为：

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

调整 `docker` 驱动程序的构建缓存配置最简单的方法是调整 `defaultKeepStorage` 选项：

- 如果您觉得 GC 太过激进，请调高限制。
- 如果您需要节省空间，请调低限制。

如果您需要更多控制，可以直接定义自己的 GC 策略。以下示例定义了一个更保守的 GC 配置，包含以下策略：

1. 如果构建缓存超过 50GB，删除超过 1440 小时（或 60 天）未使用的缓存条目。
2. 如果构建缓存超过 50GB，删除非共享缓存条目。
3. 如果构建缓存超过 100GB，删除任何缓存条目。

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

此处的策略 1 和 2 将 `keepStorage` 设置为 `0`，这意味着它们将回退到 `defaultKeepStorage` 定义的 50GB 默认限制。

### BuildKit 配置文件

对于除 `docker` 之外的构建驱动程序，GC 使用 [`buildkitd.toml`](../buildkit/toml-configuration.md) 配置文件进行配置。此文件包含以下高级配置选项，您可以用来调整 BuildKit 应为缓存使用多少磁盘空间的阈值：

| 选项          | 描述                                                                                                                                             | 默认值                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `reservedSpace` | 允许 BuildKit 为缓存分配的最小磁盘空间量。低于此阈值的使用量在垃圾回收期间不会被回收。 | 磁盘总空间的 10% 或 10GB（以较低者为准）  |
| `maxUsedSpace`  | 允许 BuildKit 使用的最大磁盘空间量。超过此阈值的使用量将在垃圾回收期间被回收。               | 磁盘总空间的 60% 或 100GB（以较低者为准） |
| `minFreeSpace`  | 必须保持空闲的磁盘空间量。                                                                                                        | 20GB                                                  |

您可以将这些选项设置为字节数、单位字符串（例如 `512MB`）或磁盘总容量的百分比。更改这些选项会影响 BuildKit worker 使用的默认 GC 策略。在默认阈值下，GC 策略解析如下：

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

- 策略 1：如果构建缓存超过 512MB，BuildKit 将删除过去 48 小时内未使用的本地构建上下文、远程 Git 上下文和缓存挂载的缓存记录。
- 策略 2：如果磁盘使用量超过 100GB，将删除超过 60 天的非共享构建缓存，确保至少保留 10GB 的磁盘空间用于缓存。
- 策略 3：如果磁盘使用量超过 100GB，将删除任何非共享缓存，确保至少保留 10GB 的磁盘空间用于缓存。
- 策略 4：如果磁盘使用量超过 100GB，将删除所有缓存（包括共享和内部记录），确保至少保留 10GB 的磁盘空间用于缓存。

`reservedSpace` 在定义构建缓存大小下限方面具有最高优先级。即使 `maxUsedSpace` 或 `minFreeSpace` 定义了更低的值，最小缓存大小也绝不会低于 `reservedSpace`。

如果同时设置了 `reservedSpace` 和 `maxUsedSpace`，则 GC 扫描后的缓存大小将处于这些阈值之间。例如，如果 `reservedSpace` 设置为 10GB，`maxUsedSpace` 设置为 20GB，那么 GC 运行后生成的缓存量将小于 20GB，但至少为 10GB。

您还可以定义完全自定义的 GC 策略。自定义策略还允许您定义过滤器（filters），这让您可以精准地确定给定策略允许清理的缓存条目类型。

#### BuildKit 中的自定义 GC 策略

自定义 GC 策略允许您微调 BuildKit 管理其缓存的方式，并根据缓存类型、持续时间或磁盘空间阈值等标准让您完全控制缓存保留。如果您需要完全控制缓存阈值以及如何对缓存记录进行优先级排序，那么定义自定义 GC 策略是最佳选择。

要定义自定义 GC 策略，请在 `buildkitd.toml` 中使用 `[[worker.oci.gcpolicy]]` 配置块。每条策略定义了该策略将使用的阈值。如果您使用自定义策略，全局的 `reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 值将不适用。

示例如下：

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

# 自定义 GC 策略 3：如果磁盘使用量超过 90GB，则激进地清理所有缓存
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "5GB"
  maxUsedSpace = "90GB"
```

除了 `reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 阈值外，在定义 GC 策略时，您还有两个额外的配置选项：

- `all`：默认情况下，BuildKit 会排除某些缓存记录，使其在 GC 期间不被清理。将此选项设置为 `true` 将允许清理任何缓存记录。
- `filters`：过滤器允许您指定 GC 策略允许清理的特定类型的缓存记录。
