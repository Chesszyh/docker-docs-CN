---
title: 构建垃圾回收 (Garbage collection)
description: 了解 BuildKit 守护进程中的垃圾回收机制
keywords: build, buildx, buildkit, garbage collection, prune, gc, 垃圾回收, 清理
aliases:
  - /build/building/cache/garbage-collection/
---

虽然 [`docker builder prune`](/reference/cli/docker/builder/prune.md) 或 [`docker buildx prune`](/reference/cli/docker/buildx/prune.md) 命令可以立即运行清理，但垃圾回收 (Garbage Collection, GC) 是定期运行的，并遵循一组有序的清理策略。当构建缓存的大小超过限制或缓存已过期时，BuildKit 守护进程会自动清除这些缓存。

对于大多数用户，默认的 GC 行为已经足够，无需任何干预。高级用户，特别是那些处理大规模构建、管理私有构建器或处于存储受限环境中的用户，可能会受益于自定义这些设置，以更好地适应其工作流需求。以下章节将解释 GC 的工作原理，并提供通过自定义配置调整其行为的指导。

## 垃圾回收策略 (Garbage collection policies)

GC 策略定义了一组规则，用于确定如何管理和清理构建缓存。这些策略包含了移除缓存条目的标准，如缓存时长、已占用的空间大小以及要清理的缓存记录类型。

每个 GC 策略都会按顺序进行评估，从最具体的标准开始，如果之前的策略未能释放足够的空间，则继续执行更宽泛的规则。这使得 BuildKit 能够优先处理缓存条目，在保留最有价值的缓存的同时，确保系统的性能和可用性。

例如，假设您有以下 GC 策略：

1. 寻找过去 48 小时内未使用的“过时”缓存记录，并删除记录，直到最多剩下 5GB 的“过时”缓存。
2. 如果构建缓存总大小超过 10GB，则删除记录，直到总缓存大小不超过 10GB。

第一条规则更具体，它优先处理过时的缓存记录，并为这类价值较低的缓存设置了一个较低的限制。第二条规则设置了一个适用于任何类型缓存记录的更高的硬性限制。根据这些策略，如果您有 11GB 的构建缓存，其中：

- 7GB 是“过时”缓存
- 4GB 是其他更有价值的缓存

一次 GC 扫描将作为第一条策略的一部分删除 5GB 的过时缓存，剩下 6GB，这意味着第二条策略无需再清除任何缓存。

默认的 GC 策略（近似值）如下：

1. 移除容易重新生成的缓存，如来自本地目录或远程 Git 仓库的构建上下文，以及过去 48 小时内未使用的缓存挂载。
2. 移除在构建中超过 60 天未使用的缓存。
3. 移除超过构建缓存大小限制的未共享缓存。未共享缓存记录是指未被其他资源（通常作为镜像层）使用的层 blob。
4. 移除超过构建缓存大小限制的任何构建缓存。

具体的算法和配置策略的方式因您使用的构建器类型而略有不同。详情请参阅 [配置](#配置) 部分。

## 配置

> [!NOTE]
> 如果您对默认的垃圾回收行为感到满意，且不需要微调其设置，可以跳过本节。默认配置适用于大多数用例，无需额外设置。

取决于您使用的 [构建驱动](../builders/drivers/_index.md) 类型，您将使用不同的配置文件来更改构建器的 GC 设置：

- 如果您使用的是 Docker Engine 的默认构建器（`docker` 驱动），请使用 [Docker 守护进程配置文件](#docker-守护进程配置文件)。
- 如果您使用的是自定义构建器，请使用 [BuildKit 配置文件](#buildkit-配置文件)。

### Docker 守护进程配置文件

如果您使用的是默认的 [`docker` 驱动](../builders/drivers/docker.md)，GC 可以在 [`daemon.json` 配置文件](/reference/cli/dockerd.md#daemon-configuration-file) 中进行配置；如果您使用的是 Docker Desktop，则在 [**Settings > Docker Engine**](/manuals/desktop/settings-and-maintenance/settings.md) 中配置。

以下代码片段展示了 Docker Desktop 用户使用 `docker` 驱动时的默认构建器配置：

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

`defaultKeepStorage` 选项配置了构建缓存的大小限制，这会影响 GC 策略。`docker` 驱动的默认策略如下：

1. 如果临时、未使用的构建缓存超过 48 小时且超过 `defaultKeepStorage` 的 13.8%（或至少 512MB），则将其移除。
2. 移除超过 60 天未使用的构建缓存。
3. 移除超过 `defaultKeepStorage` 限制的未共享构建缓存。
4. 移除超过 `defaultKeepStorage` 限制的任何构建缓存。

假设 Docker Desktop 的 `defaultKeepStorage` 默认值为 20GB，那么默认 GC 策略解析为：

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

调整 `docker` 驱动构建缓存配置最简单的方法是修改 `defaultKeepStorage` 选项：

- 如果您觉得 GC 过于频繁或严格，请调高限制。
- 如果您需要节省空间，请调低限制。

如果您需要更精细的控制，可以直接定义自己的 GC 策略。以下示例定义了一个更保守的 GC 配置，包含以下策略：

1. 如果构建缓存超过 50GB，移除超过 1440 小时（即 60 天）未使用的缓存条目。
2. 如果构建缓存超过 50GB，移除未共享的缓存条目。
3. 如果构建缓存超过 100GB，移除任何缓存条目。

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

这里的策略 1 和 2 将 `keepStorage` 设置为 `0`，意味着它们将回退到由 `defaultKeepStorage` 定义的 50GB 默认限制。

### BuildKit 配置文件

对于 `docker` 以外的构建驱动，GC 使用 [`buildkitd.toml`](../buildkit/toml-configuration.md) 配置文件进行配置。该文件使用以下高级配置选项，您可以利用它们来调整 BuildKit 使用缓存磁盘空间的阈值：

| 选项 | 说明 | 默认值 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `reservedSpace` | 允许 BuildKit 为缓存分配的最小磁盘空间。低于此阈值的使用量不会在垃圾回收期间被收回。 | 总磁盘空间的 10% 或 10GB（以较低者为准） |
| `maxUsedSpace` | 允许 BuildKit 使用的最大磁盘空间。超过此阈值的使用量将在垃圾回收期间被收回。 | 总磁盘空间的 60% 或 100GB（以较低者为准） |
| `minFreeSpace` | 必须保持空闲的磁盘空间量。 | 20GB |

您可以将这些选项设置为字节数、单位字符串（例如 `512MB`）或总磁盘大小的百分比。更改这些选项会影响 BuildKit 工作线程使用的默认 GC 策略。在默认阈值下，GC 策略解析如下：

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

从实际意义上讲，这意味着：

- **策略 1**：如果构建缓存超过 512MB，BuildKit 会移除过去 48 小时内未使用的本地构建上下文、远程 Git 上下文和缓存挂载的记录。
- **策略 2**：如果磁盘使用超过 100GB，则移除超过 60 天未使用的未共享构建缓存，同时确保至少预留 10GB 磁盘空间用于缓存。
- **策略 3**：如果磁盘使用超过 100GB，则移除任何未共享的缓存，同时确保至少预留 10GB 磁盘空间用于缓存。
- **策略 4**：如果磁盘使用超过 100GB，则移除所有缓存（包括共享和内部记录），同时确保至少预留 10GB 磁盘空间用于缓存。

在定义构建缓存大小的下限时，`reservedSpace` 具有最高优先级。即便 `maxUsedSpace` 或 `minFreeSpace` 定义了一个更低的值，最小缓存大小也绝不会被降至 `reservedSpace` 以下。

如果同时设置了 `reservedSpace` 和 `maxUsedSpace`，一次 GC 扫描的结果将使缓存大小处于这两个阈值之间。例如，如果 `reservedSpace` 设置为 10GB，`maxUsedSpace` 设置为 20GB，那么 GC 运行后的缓存量将小于 20GB，但至少为 10GB。

您还可以定义完全自定义的 GC 策略。自定义策略还允许您定义过滤器 (filters)，使您可以精确指定某项策略允许清理的缓存条目类型。

#### BuildKit 中的自定义 GC 策略

自定义 GC 策略允许您微调 BuildKit 管理其缓存的方式，并让您根据缓存类型、时长或磁盘空间阈值等标准完全控制缓存保留。如果您需要完全控制缓存阈值以及缓存记录的优先级，定义自定义 GC 策略是最佳选择。

要定义自定义 GC 策略，请使用 `buildkitd.toml` 中的 `[[worker.oci.gcpolicy]]` 配置块。每个策略定义了该策略将使用的阈值。如果您使用了自定义策略，全局的 `reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 值将不再适用。

以下是一个配置示例：

```toml
# 自定义 GC 策略 1：移除 24 小时内未使用的本地上下文
[[worker.oci.gcpolicy]]
  filters = ["type==source.local"]
  keepDuration = "24h"
  reservedSpace = "5GB"
  maxUsedSpace = "50GB"

# 自定义 GC 策略 2：移除超过 30 天的远程 Git 上下文
[[worker.oci.gcpolicy]]
  filters = ["type==source.git.checkout"]
  keepDuration = "720h"
  reservedSpace = "5GB"
  maxUsedSpace = "30GB"

# 自定义 GC 策略 3：如果磁盘使用超过 90GB，则激进地清理所有缓存
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "5GB"
  maxUsedSpace = "90GB"
```

除了 `reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 阈值外，在定义 GC 策略时，您还有两个额外的配置选项：

- `all`：默认情况下，BuildKit 在 GC 期间会排除某些缓存记录。将此选项设置为 `true` 将允许清理任何缓存记录。
- `filters`：过滤器允许您指定 GC 策略允许清理的特定类型的缓存记录。