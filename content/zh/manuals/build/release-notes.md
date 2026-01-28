---
title: Build 发布说明
weight: 120
description: 了解最新的 Buildx 版本的发布说明，包括新特性、错误修复和重大变更
keywords: build, buildx, buildkit, release notes
tags: [Release notes]
toc_max: 2
---

本页面包含有关 [Docker Buildx](https://github.com/docker/buildx) 中的新功能、改进和错误修复的信息。

## 0.24.0

{{< release-date date="2025-05-21" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.24.0)获得。

### 增强功能

- 在 Bake 的 `variable` 块中添加了新的 `type` 属性，以允许对变量进行显式类型定义。[docker/buildx#3167](https://github.com/docker/buildx/pull/3167), [docker/buildx#3189](https://github.com/docker/buildx/pull/3189), [docker/buildx#3198](https://github.com/docker/buildx/pull/3198)
- 在 `history export` 命令中添加了新的 `--finalize` 标志，以便在导出之前完成构建跟踪。[docker/buildx#3152](https://github.com/docker/buildx/pull/3152)
- Compose 兼容性已更新至 v2.6.3。[docker/buildx#3191](https://github.com/docker/buildx/pull/3191), [docker/buildx#3171](https://github.com/docker/buildx/pull/3171)

### 错误修复

- 修复了某些构建在完成后可能会留下临时文件的问题。[docker/buildx#3133](https://github.com/docker/buildx/pull/3133)
- 修复了在启用 containerd-snapshotter 时使用 Docker 构建返回错误镜像 ID 的问题。[docker/buildx#3136](https://github.com/docker/buildx/pull/3136)
- 修复了在使用 Bake 的空 `call` 定义时可能发生的 panic。[docker/buildx#3168](https://github.com/docker/buildx/pull/3168)
- 修复了在 Windows 上使用 Bake 时可能出现的格式错误的 Dockerfile 路径。[docker/buildx#3141](https://github.com/docker/buildx/pull/3141)
- 修复了 `ls` 命令的 JSON 输出中当前构建器不可用的问题。[docker/buildx#3179](https://github.com/docker/buildx/pull/3179)
- 修复了 OTEL 上下文未传播到 Docker 守护进程的问题。[docker/buildx#3146](https://github.com/docker/buildx/pull/3146)

## 0.23.0

{{< release-date date="2025-04-15" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.23.0)获得。

### 新功能

- 新的 `buildx history export` 命令允许将构建记录导出为可以导入到 [Docker Desktop](/desktop/) 的捆绑包。[docker/buildx#3073](https://github.com/docker/buildx/pull/3073)

### 增强功能

- 新的 `--local` 和 `--filter` 标志允许在 `buildx history ls` 中过滤历史记录。[docker/buildx#3091](https://github.com/docker/buildx/pull/3091)
- Compose 兼容性已更新至 v2.6.0。[docker/buildx#3080](https://github.com/docker/buildx/pull/3080), [docker/buildx#3105](https://github.com/docker/buildx/pull/3105)
- 在独立模式下支持 CLI 环境变量。[docker/buildx#3087](https://github.com/docker/buildx/pull/3087)

### 错误修复

- 修复了 Bake 的 `--print` 输出产生带有未转义变量的输出，从而可能导致后续构建错误的问题。[docker/buildx#3097](https://github.com/docker/buildx/pull/3097)
- 修复了 `additional_contexts` 字段在指向另一个服务时无法正常工作的问题。[docker/buildx#3090](https://github.com/docker/buildx/pull/3090)
- 修复了空验证块导致 Bake HCL 解析器崩溃的问题。[docker/buildx#3101](https://github.com/docker/buildx/pull/3101)

## 0.22.0

{{< release-date date="2025-03-18" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.22.0)获得。

### 新功能

- 新的命令 `buildx history import` 允许您将构建记录导入到 Docker Desktop，以便在 [Build UI](/desktop/use-desktop/builds/) 中进行进一步调试。此命令需要安装 [Docker Desktop](/desktop/)。[docker/buildx#3039](https://github.com/docker/buildx/pull/3039)

### 增强功能

- 历史记录现在可以通过 `history inspect`、`history logs` 和 `history open` 命令中与最新记录的偏移量来打开（例如 `^1`）。[docker/buildx#3049](https://github.com/docker/buildx/pull/3049), [docker/buildx#3055](https://github.com/docker/buildx/pull/3055)
- Bake 现在支持在使用 `--set` 进行覆盖时使用 `+=` 运算符进行追加。[docker/buildx#3031](https://github.com/docker/buildx/pull/3031)
- 如果可用，Docker 容器驱动程序会将 GPU 设备添加到容器中。[docker/buildx#3063](https://github.com/docker/buildx/pull/3063)
- 现在可以在使用 Bake 进行覆盖时设置注释。[docker/buildx#2997](https://github.com/docker/buildx/pull/2997)
- NetBSD 二进制文件现在已包含在发行版中。[docker/buildx#2901](https://github.com/docker/buildx/pull/2901)
- 如果节点启动失败，`inspect` 和 `create` 命令现在会返回错误。[docker/buildx#3062](https://github.com/docker/buildx/pull/3062)

### 错误修复

- 修复了在启用 containerd 镜像存储时使用 Docker 驱动程序重复推送的问题。[docker/buildx#3023](https://github.com/docker/buildx/pull/3023)
- 修复了 `imagetools create` 命令推送多个标签的问题。现在只有最终清单按标签推送。[docker/buildx#3024](https://github.com/docker/buildx/pull/3024)

## 0.21.0

{{< release-date date="2025-02-19" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.21.0)获得。

### 新功能

- 新的命令 `buildx history trace` 允许您在基于 Jaeger UI 的查看器中检查构建的跟踪，并将一个跟踪与另一个进行比较。[docker/buildx#2904](https://github.com/docker/buildx/pull/2904)

### 增强功能

- 历史检查命令 `buildx history inspect` 现在支持使用 `--format` 标志进行自定义格式化，以及用于机器可读输出的 JSON 格式。[docker/buildx#2964](https://github.com/docker/buildx/pull/2964)
- 在 build 和 bake 中支持 CDI 设备授权。[docker/buildx#2994](https://github.com/docker/buildx/pull/2994)
- 支持的 CDI 设备现在显示在构建器检查中。[docker/buildx#2983](https://github.com/docker/buildx/pull/2983)
- 当使用 [GitHub Cache 后端 `type=gha`](cache/backends/gha.md) 时，版本 2 或 API 的 URL 现在从环境中读取并发送到 BuildKit。版本 2 后端需要 BuildKit v0.20.0 或更高版本。[docker/buildx#2983](https://github.com/docker/buildx/pull/2983), [docker/buildx#3001](https://github.com/docker/buildx/pull/3001)

### 错误修复

- 避免了在使用 `--progress=rawjson` 时出现不必要的警告和提示。[docker/buildx#2957](https://github.com/docker/buildx/pull/2957)
- 修复了调试 shell 有时在 `--on=error` 上无法正常工作的问题。[docker/buildx#2958](https://github.com/docker/buildx/pull/2958)
- 修复了在 Bake 定义中使用未知变量时可能出现的 panic 错误。[docker/buildx#2960](https://github.com/docker/buildx/pull/2960)
- 修复了 `buildx ls` 命令的 JSON 格式输出中无效的重复输出。[docker/buildx#2970](https://github.com/docker/buildx/pull/2970)
- 修复了 bake 处理包含多个注册表引用的 CSV 字符串的缓存导入问题。[docker/buildx#2944](https://github.com/docker/buildx/pull/2944)
- 修复了拉取 BuildKit 镜像时的错误可能被忽略的问题。[docker/buildx#2988](https://github.com/docker/buildx/pull/2988)
- 修复了调试 shell 上暂停进度的竞争问题。[docker/buildx#3003](https://github.com/docker/buildx/pull/3003)

## 0.20.1

{{< release-date date="2025-01-23" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.20.1)获得。

### 错误修复

- 修复了 `bake --print` 输出在遗漏证明的某些属性后的问题。[docker/buildx#2937](https://github.com/docker/buildx/pull/2937)
- 修复了允许缓存导入和导出值使用逗号分隔的镜像引用字符串。[docker/buildx#2944](https://github.com/docker/buildx/pull/2944)

## 0.20.0

{{< release-date date="2025-01-20" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.20.0)获得。

> [!NOTE]
>
> 此版本的 buildx 默认启用 `buildx bake` 命令的文件系统授权检查。如果您的 Bake 定义需要读取或写入当前工作目录之外的文件，您需要使用 `--allow fs=<path|*>` 允许访问这些路径。在终端上，您也可以通过提供的提示交互式地批准这些路径。或者，您可以通过设置 `BUILDX_BAKE_ENTITLEMENTS_FS=0` 来禁用这些检查。此验证在 Buildx v0.19.0+ 中会产生警告，但从当前版本开始会产生错误。有关更多信息，请参阅 [参考文档](/reference/cli/docker/buildx/bake.md#allow)。

### 新功能

- 添加了新的 `buildx history` 命令，允许处理已完成和正在运行的构建的构建记录。您可以使用这些命令列出、检查、删除您的构建，重播已完成构建的日志，并在 Docker Desktop Build UI 中快速打开您的构建以进行进一步调试。这是此命令的早期版本，我们期望在未来的版本中添加更多功能。[#2891](https://github.com/docker/buildx/pull/2891), [#2925](https://github.com/docker/buildx/pull/2925)

### 增强功能

- Bake：定义现在支持新对象表示法，用于以前需要 CSV 字符串作为输入的字段（`attest`, `output`, `cache-from`, `cache-to`, `secret`, `ssh`）。[docker/buildx#2758](https://github.com/docker/buildx/pull/2758), [docker/buildx#2848](https://github.com/docker/buildx/pull/2848), [docker/buildx#2871](https://github.com/docker/buildx/pull/2871), [docker/buildx#2814](https://github.com/docker/buildx/pull/2814)
- Bake：文件系统授权现在默认为错误。要禁用此行为，您可以设置 `BUILDX_BAKE_ENTITLEMENTS_FS=0`。[docker/buildx#2875](https://github.com/docker/buildx/pull/2875)
- Bake：从远程文件推断 Git 身份验证令牌到构建请求。[docker/buildx#2905](https://github.com/docker/buildx/pull/2905)
- Bake：添加对 `--list` 标志的支持以列出目标和变量。[docker/buildx#2900](https://github.com/docker/buildx/pull/2900), [docker/buildx#2907](https://github.com/docker/buildx/pull/2907)
- Bake：更新默认定义文件的查找顺序，以便稍后加载带有 "override" 后缀的文件。[docker/buildx#2886](https://github.com/docker/buildx/pull/2886)

### 错误修复

- Bake：修复默认 SSH 套接字的授权检查。[docker/buildx#2898](https://github.com/docker/buildx/pull/2898)
- Bake：修复组的默认目标中缺少默认目标的问题。[docker/buildx#2863](https://github.com/docker/buildx/pull/2863)
- Bake：修复来自目标平台的命名上下文匹配。[docker/buildx#2877](https://github.com/docker/buildx/pull/2877)
- 修复安静进度模式缺少文档的问题。[docker/buildx#2899](https://github.com/docker/buildx/pull/2899)
- 修复加载层时缺少最后进度的问题。[docker/buildx#2876](https://github.com/docker/buildx/pull/2876)
- 在创建构建器之前验证 BuildKit 配置。[docker/buildx#2864](https://github.com/docker/buildx/pull/2864)

### 打包

- Compose 兼容性已更新至 v2.4.7。[docker/buildx#2893](https://github.com/docker/buildx/pull/2893), [docker/buildx#2857](https://github.com/docker/buildx/pull/2857), [docker/buildx#2829](https://github.com/docker/buildx/pull/2829)

## 0.19.1

{{< release-date date="2024-11-27" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.19.1)获得。

### 错误修复

- 撤销了 v0.19.0 中的更改，该更改为 Bake 定义中以前需要 CSV 字符串的字段添加了新的对象表示法。此增强功能被撤销是因为在某些边缘情况下发现了向后不兼容的问题。此功能现已推迟到 v0.20.0 版本。[docker/buildx#2824](https://github.com/docker/buildx/pull/2824)

## 0.19.0

{{< release-date date="2024-11-27" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.19.0)获得。

### 新功能

- Bake 现在要求您在构建需要读取或写入当前工作目录之外的文件时允许文件系统授权。
  [docker/buildx#2796](https://github.com/docker/buildx/pull/2796),
  [docker/buildx#2812](https://github.com/docker/buildx/pull/2812).

  要允许文件系统授权，请使用 `docker buildx bake` 命令的 `--allow fs.read=<path>` 标志。

  此功能目前仅在使用本地 Bake 定义时报告警告，但从 v0.20 版本开始将产生错误。要在当前版本中启用错误，您可以设置 `BUILDX_BAKE_ENTITLEMENTS_FS=1`。

### 增强功能

- Bake 定义现在支持新对象表示法，用于以前需要 CSV 字符串作为输入的字段。[docker/buildx#2758](https://github.com/docker/buildx/pull/2758)

  > [!NOTE]
  > 此增强功能因错误在 [v0.19.1](#0191) 中被撤销。

- Bake 定义现在允许对变量定义验证条件。[docker/buildx#2794](https://github.com/docker/buildx/pull/2794)
- 元数据文件值现在可以包含 JSON 数组值。[docker/buildx#2777](https://github.com/docker/buildx/pull/2777)
- 改进了使用不正确格式的标签时的错误消息。[docker/buildx#2778](https://github.com/docker/buildx/pull/2778)
- FreeBSD 和 OpenBSD 工件现在已包含在发行版中。[docker/buildx#2774](https://github.com/docker/buildx/pull/2774), [docker/buildx#2775](https://github.com/docker/buildx/pull/2775), [docker/buildx#2781](https://github.com/docker/buildx/pull/2781)

### 错误修复

- 修复了打印包含空 Compose 网络的 Bake 定义的问题。[docker/buildx#2790](https://github.com/docker/buildx/pull/2790)。

### 打包

- Compose 支持已更新至 v2.4.4。[docker/buildx#2806](https://github.com/docker/buildx/pull/2806) [docker/buildx#2780](https://github.com/docker/buildx/pull/2780)。

## 0.18.0

{{< release-date date="2024-10-31" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.18.0)获得。

### 新功能

- `docker buildx inspect` 命令现在显示使用 TOML 文件设置的 BuildKit 守护进程配置选项。[docker/buildx#2684](https://github.com/docker/buildx/pull/2684)
- `docker buildx ls` 命令输出现在默认更紧凑，通过压缩平台列表实现。可以使用新的 `--no-trunc` 选项获取完整列表。[docker/buildx#2138](https://github.com/docker/buildx/pull/2138), [docker/buildx#2717](https://github.com/docker/buildx/pull/2717)
- `docker buildx prune` 命令现在支持新的 `--max-used-space` 和 `--min-free-space` 过滤器，适用于 BuildKit v0.17.0+ 构建器。[docker/buildx#2766](https://github.com/docker/buildx/pull/2766)

### 增强功能

- 允许使用 [`BUILDX_CPU_PROFILE`](/manuals/build/building/variables.md#buildx_cpu_profile) 和 [`BUILDX_MEM_PROFILE`](/manuals/build/building/variables.md#buildx_mem_profile) 环境变量使用 `pprof` 捕获 CPU 和内存分析。[docker/buildx#2746](https://github.com/docker/buildx/pull/2746)
- 增加了标准输入的最大 Dockerfile 大小。[docker/buildx#2716](https://github.com/docker/buildx/pull/2716), [docker/buildx#2719](https://github.com/docker/buildx/pull/2719)
- 减少了内存分配。[docker/buildx#2724](https://github.com/docker/buildx/pull/2724), [docker/buildx#2713](https://github.com/docker/buildx/pull/2713)
- `docker buildx bake` 的 `--list-targets` 和 `--list-variables` 标志不再需要初始化构建器。[docker/buildx#2763](https://github.com/docker/buildx/pull/2763)

### 错误修复

- 检查警告现在打印有问题的 Dockerfile 的完整文件路径（相对于当前工作目录）。[docker/buildx#2672](https://github.com/docker/buildx/pull/2672)
- `--check` 和 `--call` 选项的后备镜像已更新为正确的引用。[docker/buildx#2705](https://github.com/docker/buildx/pull/2705)
- 修复了构建详细信息链接在实验模式下未显示的问题。[docker/buildx#2722](https://github.com/docker/buildx/pull/2722)
- 修复了 Bake 的无效目标链接验证问题。[docker/buildx#2700](https://github.com/docker/buildx/pull/2700)
- 修复了运行无效命令时缺少错误消息的问题。[docker/buildx#2741](https://github.com/docker/buildx/pull/2741)
- 修复了 `--call` 请求中本地状态可能出现的错误警告。[docker/buildx#2754](https://github.com/docker/buildx/pull/2754)
- 修复了在 Bake 中使用链接目标时可能出现的授权问题。[docker/buildx#2701](https://github.com/docker/buildx/pull/2701)
- 修复了使用 `sudo` 运行 Buildx 后访问本地状态时可能出现的权限问题。[docker/buildx#2745](https://github.com/docker/buildx/pull/2745)

### 打包

- Compose 兼容性已更新至 v2.4.1。[docker/buildx#2760](https://github.com/docker/buildx/pull/2760)

## 0.17.1

{{< release-date date="2024-09-13" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.17.1)获得。

### 错误修复

- 如果在 [BuildKit 配置文件](/manuals/build/buildkit/toml-configuration.md)中设置了授权，则不再在为 `docker-container` 和 `kubernetes` 驱动程序创建构建器时自动设置 `network.host` 授权标志。[docker/buildx#2685]
- 当 `docker buildx bake --print` 为空时，不再打印 `network` 字段。[docker/buildx#2689]
- 修复 WSL2 下的遥测套接字路径。[docker/buildx#2698]

[docker/buildx#2685]: https://github.com/docker/buildx/pull/2685
[docker/buildx#2689]: https://github.com/docker/buildx/pull/2689
[docker/buildx#2698]: https://github.com/docker/buildx/pull/2698

## 0.17.0

{{< release-date date="2024-09-10" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.17.0)获得。

### 新功能

- 向 Bake 添加了 `basename`、`dirname` 和 `sanitize` 函数。[docker/buildx#2649]
- 启用对 Bake 授权的支持，以允许在构建期间进行特权操作。[docker/buildx#2666]

### 增强功能

- 引入 Bake 命令的 CLI 指标跟踪。[docker/buildx#2610]
- 向所有构建命令添加 `--debug`。以前，它仅在顶级 `docker` 和 `docker buildx` 命令中可用。[docker/buildx#2660]
- 允许从 stdin 进行多节点构建器的构建。[docker/buildx#2656]
- 改进 `kubernetes` 驱动程序初始化。[docker/buildx#2606]
- 在使用 Bake 构建多个目标时，在错误消息中包含目标名称。[docker/buildx#2651]
- 优化指标处理，以减少进度跟踪期间的性能开销。[docker/buildx#2641]
- 完成规则检查后显示警告数量。[docker/buildx#2647]
- 跳过前端方法的构建引用和来源元数据。[docker/buildx#2650]
- 添加对在 Bake 文件（HCL 和 JSON）中设置网络模式的支持。[docker/buildx#2671]
- 当与 `--call` 标志一起设置时，支持 `--metadata-file` 标志。[docker/buildx#2640]
- 对多个 Bake 目标使用的本地上下文使用共享会话。[docker/buildx#2615], [docker/buildx#2607], [docker/buildx#2663]

### 错误修复

- 改进内存管理以避免不必要的分配。[docker/buildx#2601]

### 打包更新

- Compose 支持已更新至 v2.1.6。[docker/buildx#2547]

[docker/buildx#2547]: https://github.com/docker/buildx/pull/2547/
[docker/buildx#2601]: https://github.com/docker/buildx/pull/2601/
[docker/buildx#2606]: https://github.com/docker/buildx/pull/2606/
[docker/buildx#2607]: https://github.com/docker/buildx/pull/2607/
[docker/buildx#2610]: https://github.com/docker/buildx/pull/2610/
[docker/buildx#2615]: https://github.com/docker/buildx/pull/2615/
[docker/buildx#2640]: https://github.com/docker/buildx/pull/2640/
[docker/buildx#2641]: https://github.com/docker/buildx/pull/2641/
[docker/buildx#2647]: https://github.com/docker/buildx/pull/2647/
[docker/buildx#2649]: https://github.com/docker/buildx/pull/2649/
[docker/buildx#2650]: https://github.com/docker/buildx/pull/2650/
[docker/buildx#2651]: https://github.com/docker/buildx/pull/2651/
[docker/buildx#2656]: https://github.com/docker/buildx/pull/2656/
[docker/buildx#2660]: https://github.com/docker/buildx/pull/2660/
[docker/buildx#2663]: https://github.com/docker/buildx/pull/2663/
[docker/buildx#2666]: https://github.com/docker/buildx/pull/2666/
[docker/buildx#2671]: https://github.com/docker/buildx/pull/2671/

## 0.16.2

{{< release-date date="2024-07-25" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.16.2)获得。

### 错误修复

- 修复了将本地缓存导出到 NFS 卷时可能出现的“错误的文件描述符”错误 [docker/buildx#2629](https://github.com/docker/buildx/pull/2629/)

## 0.16.1

{{< release-date date="2024-07-18" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.16.1)获得。

### 错误修复

- 修复了 `buildx bake --print` 命令中由于数据竞争可能导致的 panic [docker/buildx#2603](https://github.com/docker/buildx/pull/2603/)
- 改进关于使用 `--debug` 标志检查构建警告的消息 [docker/buildx#2612](https://github.com/docker/buildx/pull/2612/)

## 0.16.0

{{< release-date date="2024-07-11" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.16.0)获得。

### 新功能

- Bake 命令现在支持 `--call` 和 `--check` 标志以及目标定义中的 `call` 属性，用于选择自定义前端方法。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/), [docker/buildx#2576](https://github.com/docker/buildx/pull/2576/)
- {{< badge color=violet text=Experimental >}} Bake 现在支持 `--list-targets` 和 `--list-variables` 标志，用于检查项目的定义和可能的配置选项。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/)
- Bake 定义变量和目标支持新的 `description` 属性，用于定义基于文本的描述，可以使用例如 `--list-targets` 和 `--list-variables` 进行检查。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/)
- Bake 现在支持打印构建检查违规的警告。[docker/buildx#2501](https://github.com/docker/buildx/pull/2501/)

### 增强功能

- 构建命令现在确保多节点构建对每个节点使用相同的构建引用。[docker/buildx#2572](https://github.com/docker/buildx/pull/2572/)
- 避免重复请求并提高远程驱动程序的性能。[docker/buildx#2501](https://github.com/docker/buildx/pull/2501/)
- 现在可以通过设置 `BUILDX_METADATA_WARNINGS=1` 环境变量将构建警告保存到元数据文件。[docker/buildx#2551](https://github.com/docker/buildx/pull/2551/), [docker/buildx#2521](https://github.com/docker/buildx/pull/2521/), [docker/buildx#2550](https://github.com/docker/buildx/pull/2550/)
- 改进未检测到警告时 `--check` 标志的消息。[docker/buildx#2549](https://github.com/docker/buildx/pull/2549/)

### 错误修复

- 修复了构建期间对多类型注释的支持。[docker/buildx#2522](https://github.com/docker/buildx/pull/2522/)
- 修复了一个回归，即由于增量传输重用，切换项目时可能会发生效率低下的文件传输。[docker/buildx#2558](https://github.com/docker/buildx/pull/2558/)
- 修复了链式 Bake 目标的错误默认加载。[docker/buildx#2583](https://github.com/docker/buildx/pull/2583/)
- 修复了 Bake 中不正确的 `COMPOSE_PROJECT_NAME` 处理。[docker/buildx#2579](https://github.com/docker/buildx/pull/2579/)
- 修复了对多节点构建的索引注释支持。[docker/buildx#2546](https://github.com/docker/buildx/pull/2546/)
- 修复了从远程上下文捕获构建的来源元数据。[docker/buildx#2560](https://github.com/docker/buildx/pull/2560/)

### 打包更新

- Compose 支持已更新至 v2.1.3。[docker/buildx#2547](https://github.com/docker/buildx/pull/2547/)

## 0.15.1

{{< release-date date="2024-06-18" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.15.1)获得。

### 错误修复

- 修复了使用 `--check` 时某些验证请求缺少构建错误和退出代码的问题。[docker/buildx#2518](https://github.com/docker/buildx/pull/2518/)
- 更新 `--check` 的后备镜像至 Dockerfile v1.8.1。[docker/buildx#2538](https://github.com/docker/buildx/pull/2538/)

## 0.15.0

{{< release-date date="2024-06-11" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.15.0)获得。

### 新功能

- 新的 `--call` 选项允许设置构建的评估方法，取代了以前的实验性 `--print` 标志。[docker/buildx#2498](https://github.com/docker/buildx/pull/2498/), [docker/buildx#2487](https://github.com/docker/buildx/pull/2487/), [docker/buildx#2513](https://github.com/docker/buildx/pull/2513/)

  除了默认的 `build` 方法外，Dockerfile 前端还实现了以下方法：

  - [`--call=check`](/reference/cli/docker/buildx/build.md#check): 运行构建配置的验证例程。有关构建检查的更多信息，请参阅 [构建检查](/manuals/build/checks.md)
  - [`--call=outline`](/reference/cli/docker/buildx/build.md#call-outline): 显示当前构建将使用的配置，包括您的构建将使用的所有构建参数、密钥、SSH 挂载等。
  - [`--call=targets`](/reference/cli/docker/buildx/build.md#call-targets): 显示所有可用目标及其描述。

- `docker buildx imagetools create` 命令添加了新的 `--prefer-index` 标志，用于控制从单个单平台镜像清单创建镜像的行为。[docker/buildx#2482](https://github.com/docker/buildx/pull/2482/)
- [`kubernetes` 驱动程序](/manuals/build/builders/drivers/kubernetes.md) 现在支持 `timeout` 选项用于配置部署超时。[docker/buildx#2492](https://github.com/docker/buildx/pull/2492/)
- 为构建警告类型添加了新的指标定义。[docker/buildx#2482](https://github.com/docker/buildx/pull/2482/), [docker/buildx#2507](https://github.com/docker/buildx/pull/2507/)
- [`buildx prune`](/reference/cli/docker/buildx/prune.md) 和 [`buildx du`](/reference/cli/docker/buildx/du.md) 命令现在支持否定和前缀过滤器。[docker/buildx#2473](https://github.com/docker/buildx/pull/2473/)
- 使用 Bake 构建 Compose 文件现在支持传递 SSH 转发配置。[docker/buildx#2445](https://github.com/docker/buildx/pull/2445/)
- 修复了使用自定义 TLS 证书配置 `kubernetes` 驱动程序的问题。[docker/buildx#2454](https://github.com/docker/buildx/pull/2454/)
- 修复了加载节点时并发访问 kubeconfig 的问题。[docker/buildx#2497](https://github.com/docker/buildx/pull/2497/)

### 打包更新

- Compose 支持已更新至 v2.1.2。[docker/buildx#2502](https://github.com/docker/buildx/pull/2502/), [docker/buildx#2425](https://github.com/docker/buildx/pull/2425/)

## 0.14.0

{{< release-date date="2024-04-18" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.14.0)获得。

### 增强功能

- 添加对 `--print=lint`（实验性）的支持。
  [docker/buildx#2404](https://github.com/docker/buildx/pull/2404),
  [docker/buildx#2406](https://github.com/docker/buildx/pull/2406)
- 修复了前端中自定义实现打印子请求的 JSON 格式化。
  [docker/buildx#2374](https://github.com/docker/buildx/pull/2374)
- 使用 `--metadata-file` 构建时现在会设置来源记录。
  [docker/buildx#2280](https://github.com/docker/buildx/pull/2280)
- 为远程定义添加 [Git 身份验证支持](./bake/remote-definition.md#remote-definition-in-a-private-repository)。
  [docker/buildx#2363](https://github.com/docker/buildx/pull/2363)
- 为 `docker-container`、`remote` 和 `kubernetes` 驱动程序添加了新的 `default-load` 驱动程序选项，以默认将构建结果加载到 Docker 引擎镜像存储。
  [docker/buildx#2259](https://github.com/docker/buildx/pull/2259)
- 向 [`kubernetes` 驱动程序](/manuals/build/builders/drivers/kubernetes.md)添加 `requests.ephemeral-storage`、`limits.ephemeral-storage` 和 `schedulername` 选项。
  [docker/buildx#2370](https://github.com/docker/buildx/pull/2370),
  [docker/buildx#2415](https://github.com/docker/buildx/pull/2415)
- 为 `docker-bake.hcl` 文件添加 `indexof` 函数。
  [docker/buildx#2384](https://github.com/docker/buildx/pull/2384)
- Buildx 的 OpenTelemetry 指标现在测量构建期间图像源操作的空闲时间、图像导出、运行操作和图像传输的持续时间。
  [docker/buildx#2316](https://github.com/docker/buildx/pull/2316),
  [docker/buildx#2317](https://github.com/docker/buildx/pull/2317),
  [docker/buildx#2323](https://github.com/docker/buildx/pull/2323),
  [docker/buildx#2271](https://github.com/docker/buildx/pull/2271)
- 关联到 `desktop-linux` 上下文的 OpenTelemetry 端点的构建进度指标不再需要 Buildx 处于实验模式 (`BUILDX_EXPERIMENTAL=1`)。
  [docker/buildx#2344](https://github.com/docker/buildx/pull/2344)

### 错误修复

- 修复了与多个 Bake 文件定义一起使用时，`--load` 和 `--push` 错误地覆盖输出的问题。
  [docker/buildx#2336](https://github.com/docker/buildx/pull/2336)
- 修复了启用实验模式时从 stdin 构建的问题。
  [docker/buildx#2394](https://github.com/docker/buildx/pull/2394)
- 修复了委托跟踪可能重复的问题。
  [docker/buildx#2362](https://github.com/docker/buildx/pull/2362)

### 打包更新

- Compose 支持已更新至 [v2.26.1](https://github.com/docker/compose/releases/tag/v2.26.1)
  (通过 [`compose-go` v2.0.2](https://github.com/compose-spec/compose-go/releases/tag/v2.0.2))。
  [docker/buildx#2391](https://github.com/docker/buildx/pull/2391)

## 0.13.1

{{< release-date date="2024-03-13" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.13.1)获得。

### 错误修复

- 修复了使用远程驱动程序连接到 `docker-container://` 和 `kube-pod://` 样式 URL 的问题。[docker/buildx#2327](https://github.com/docker/buildx/pull/2327)
- 修复了当目标已定义非镜像输出时使用 `--push` 与 Bake 的处理问题。[docker/buildx#2330](https://github.com/docker/buildx/pull/2330)

## 0.13.0

{{< release-date date="2024-03-06" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.13.0)获得。

### 新功能

- 新的 `docker buildx dial-stdio` 命令用于直接联系配置的构建器实例的 BuildKit 守护进程。[docker/buildx#2112](https://github.com/docker/buildx/pull/2112)
- 现在可以使用 `remote` 驱动程序和 npipe 连接创建 Windows 容器构建器。[docker/buildx#2287](https://github.com/docker/buildx/pull/2287)
- Windows 上现在支持 Npipe URL 方案。[docker/buildx#2250](https://github.com/docker/buildx/pull/2250)
- {{< badge color=violet text=Experimental >}} Buildx 现在可以导出构建持续时间和传输大小的 OpenTelemetry 指标。[docker/buildx#2235](https://github.com/docker/buildx/pull/2235), [docker/buildx#2258](https://github.com/docker/buildx/pull/2258) [docker/buildx#2225](https://github.com/docker/buildx/pull/2225) [docker/buildx#2224](https://github.com/docker/buildx/pull/2224) [docker/buildx#2155](https://github.com/docker/buildx/pull/2155)

### 增强功能

- Bake 命令现在支持定义 `shm-size` 和 `ulimit` 值。[docker/buildx#2279](https://github.com/docker/buildx/pull/2279), [docker/buildx#2242](https://github.com/docker/buildx/pull/2242)
- 更好地处理使用远程驱动程序连接到不健康节点的情况。[docker/buildx#2130](https://github.com/docker/buildx/pull/2130)
- 使用 `docker-container` 和 `kubernetes` 驱动程序的构建器现在默认允许 `network.host` 授权（允许访问容器网络）。[docker/buildx#2266](https://github.com/docker/buildx/pull/2266)
- 构建现在可以使用单个命令使用多个输出（需要 BuildKit v0.13+）。[docker/buildx#2290](https://github.com/docker/buildx/pull/2290), [docker/buildx#2302](https://github.com/docker/buildx/pull/2302)
- 默认 Git 存储库路径现在通过配置的跟踪分支查找。[docker/buildx#2146](https://github.com/docker/buildx/pull/2146)
- 修复了在 Bake 中使用链接目标时可能出现的缓存失效问题。[docker/buildx#2265](https://github.com/docker/buildx/pull/2265)
- 修复了 WSL 中 Git 存储库路径清理的问题。[docker/buildx#2167](https://github.com/docker/buildx/pull/2167)
- 现在可以使用单个命令删除多个构建器。[docker/buildx#2140](https://github.com/docker/buildx/pull/2140)
- 通过 Unix 套接字进行新的取消信号处理。[docker/buildx#2184](https://github.com/docker/buildx/pull/2184) [docker/buildx#2289](https://github.com/docker/buildx/pull/2289)
- Compose 规范支持已更新至 v2.0.0-rc.8。[docker/buildx#2205](https://github.com/docker/buildx/pull/2205)
- `docker buildx create` 的 `--config` 标志已重命名为 `--buildkitd-config`。[docker/buildx#2268](https://github.com/docker/buildx/pull/2268)
- `docker buildx build` 的 `--metadata-file` 标志现在也可以返回构建引用，可用于进一步的构建调试，例如在 Docker Desktop 中。[docker/buildx#2263](https://github.com/docker/buildx/pull/2263)
- `docker buildx bake` 命令现在为所有目标共享相同的身份验证提供程序，以提高性能。[docker/buildx#2147](https://github.com/docker/buildx/pull/2147)
- `docker buildx imagetools inspect` 命令现在显示 DSSE 签名的 SBOM 和来源证明。[docker/buildx#2194](https://github.com/docker/buildx/pull/2194)
- `docker buildx ls` 命令现在支持 `--format` 选项以控制输出。[docker/buildx#1787](https://github.com/docker/buildx/pull/1787)
- `docker-container` 驱动程序现在支持用于定义 BuildKit 容器重启策略的驱动程序选项。[docker/buildx#1271](https://github.com/docker/buildx/pull/1271)
- 如果它们相对于当前的 Git 存储库，从 Buildx 导出的 VCS 属性现在包括本地目录子路径。[docker/buildx#2156](https://github.com/docker/buildx/pull/2156)
- `--add-host` 标志现在允许 IPv6 地址使用 `=` 分隔符。[docker/buildx#2121](https://github.com/docker/buildx/pull/2121)

### 错误修复

- 修复了使用 `--progress=rawjson` 导出进度时的额外输出 [docker/buildx#2252](https://github.com/docker/buildx/pull/2252)
- 修复了 Windows 上可能出现的控制台警告。[docker/buildx#2238](https://github.com/docker/buildx/pull/2238)
- 修复了使用包含许多配置的 Bake 时可能出现的配置合并顺序不一致问题。[docker/buildx#2237](https://github.com/docker/buildx/pull/2237)
- 修复了 `docker buildx imagetools create` 命令中可能出现的 panic。[docker/buildx#2230](https://github.com/docker/buildx/pull/2230)

## 0.12.1

{{< release-date date="2024-01-12" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.12.1)获得。

### 错误修复和增强功能

- 修复了某些 `--driver-opt` 值的不正确验证，这可能导致 panic 并存储损坏的状态。
  [docker/buildx#2176](https://github.com/docker/buildx/pull/2176)

## 0.12.0

{{< release-date date="2023-11-16" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.12.0)获得。

### 新功能

- `buildx build` 的新 `--annotation` 标志，以及 Bake 文件中的 `annotations` 键，允许您向构建结果添加 OCI 注释。
  [#2020](https://github.com/docker/buildx/pull/2020),
  [#2098](https://github.com/docker/buildx/pull/2098)
- 新的实验性调试功能，包括新的 `debug` 命令和交互式调试控制台。
  此功能目前需要设置 `BUILDX_EXPERIMENTAL=1`。
  [#2006](https://github.com/docker/buildx/pull/2006),
  [#1896](https://github.com/docker/buildx/pull/1896),
  [#1970](https://github.com/docker/buildx/pull/1970),
  [#1914](https://github.com/docker/buildx/pull/1914),
  [#2026](https://github.com/docker/buildx/pull/2026),
  [#2086](https://github.com/docker/buildx/pull/2086)

### 错误修复和增强功能

- 特殊的 `host-gateway` IP 映射现在可以在构建期间与 `--add-host` 标志一起使用。
  [#1894](https://github.com/docker/buildx/pull/1894),
  [#2083](https://github.com/docker/buildx/pull/2083)
- Bake 现在允许在从远程定义构建时添加本地源文件。
  [#1838](https://github.com/docker/buildx/pull/1838)
- 将构建结果上传到 Docker 的状态现在交互式地显示在进度条上。
  [#1994](https://github.com/docker/buildx/pull/1994)
- 改进了引导多节点构建集群时的错误处理。
  [#1869](https://github.com/docker/buildx/pull/1869)
- `buildx imagetools create` 命令现在允许在注册表中创建新镜像时添加注释。
  [#1965](https://github.com/docker/buildx/pull/1965)
- 现在可以使用 Docker 和远程驱动程序从 buildx 进行 OpenTelemetry 构建跟踪委托。
  [#2034](https://github.com/docker/buildx/pull/2034)
- Bake 命令现在在进度条上显示加载构建定义的所有文件。
  [#2076](https://github.com/docker/buildx/pull/2076)
- Bake 文件现在允许在多个定义文件中定义相同的属性。
  [#1062](https://github.com/docker/buildx/pull/1062)
- 使用带有远程定义的 Bake 命令现在允许此定义使用本地 Dockerfile。
  [#2015](https://github.com/docker/buildx/pull/2015)
- Docker 容器驱动程序现在显式设置 BuildKit 配置路径，以确保为主线和无根镜像从同一位置加载配置。
  [#2093](https://github.com/docker/buildx/pull/2093)
- 提高检测 BuildKit 实例何时完成启动的性能。
  [#1934](https://github.com/docker/buildx/pull/1934)
- 容器驱动程序现在接受许多新的驱动程序选项，用于定义 BuildKit 容器的资源限制。
  [#2048](https://github.com/docker/buildx/pull/2048)
- 检查命令格式已改进。
  [#2068](https://github.com/docker/buildx/pull/2068)
- 改进了有关驱动程序功能的错误消息。
  [#1998](https://github.com/docker/buildx/pull/1998)
- 改进了在没有目标的情况下调用 Bake 命令时的错误。
  [#2100](https://github.com/docker/buildx/pull/2100)
- 允许在独立模式下运行时使用环境变量启用调试日志。
  [#1821](https://github.com/docker/buildx/pull/1821)
- 当使用 Docker 驱动程序时，默认镜像解析模式已更新为首选本地 Docker 镜像以实现向后兼容性。
  [#1886](https://github.com/docker/buildx/pull/1886)
- Kubernetes 驱动程序现在允许为 BuildKit 部署和 Pod 设置自定义注释和标签。
  [#1938](https://github.com/docker/buildx/pull/1938)
- Kubernetes 驱动程序现在允许通过端点配置设置身份验证令牌。
  [#1891](https://github.com/docker/buildx/pull/1891)
- 修复了 Bake 中链接目标可能导致构建失败或目标本地源多次上传的可能问题。
  [#2113](https://github.com/docker/buildx/pull/2113)
- 修复了使用 Bake 命令的矩阵功能时访问全局目标属性的问题。
  [#2106](https://github.com/docker/buildx/pull/2106)
- 修复了某些构建标志的格式验证
  [#2040](https://github.com/docker/buildx/pull/2040)
- 修复了在启动构建器节点时不必要地锁定某些命令的问题。
  [#2066](https://github.com/docker/buildx/pull/2066)
- 修复了多个构建尝试并行引导同一构建器实例的情况。
  [#2000](https://github.com/docker/buildx/pull/2000)
- 修复了在某些情况下上传构建结果到 Docker 时错误可能被丢弃的情况。
  [#1927](https://github.com/docker/buildx/pull/1927)
- 修复了基于构建输出检测缺少证明支持的功能。
  [#1988](https://github.com/docker/buildx/pull/1988)
- 修复了 Bake 远程定义中用于加载的构建不显示在构建历史记录中的问题。
  [#1961](https://github.com/docker/buildx/pull/1961),
  [#1954](https://github.com/docker/buildx/pull/1954)
- 修复了使用 Bake 定义配置文件的 Compose 文件进行构建时的错误。
  [#1903](https://github.com/docker/buildx/pull/1903)
- 修复了进度条上可能的时间校正错误。
  [#1968](https://github.com/docker/buildx/pull/1968)
- 修复了将自定义 cgroup parent 传递给使用新控制器接口的构建的问题。
  [#1913](https://github.com/docker/buildx/pull/1913)

### 打包

- Compose 支持已更新至 1.20，在使用 Bake 命令时启用“包含”功能。
  [#1971](https://github.com/docker/buildx/pull/1971),
  [#2065](https://github.com/docker/buildx/pull/2065),
  [#2094](https://github.com/docker/buildx/pull/2094)

## 0.11.2

{{< release-date date="2023-07-18" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.11.2)获得。

### 错误修复和增强功能

- 修复了导致 buildx 无法从实例存储读取 `KUBECONFIG` 路径的回归。
  [docker/buildx#1941](https://github.com/docker/buildx/pull/1941)
- 修复了结果处理构建错误地显示在构建历史记录中的回归。
  [docker/buildx#1954](https://github.com/docker/buildx/pull/1954)

## 0.11.1

{{< release-date date="2023-07-05" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.11.1)获得。

### 错误修复和增强功能

- 修复了 bake 中配置文件中的服务无法加载的回归。
  [docker/buildx#1903](https://github.com/docker/buildx/pull/1903)
- 修复了 `--cgroup-parent` 选项在构建期间无效的回归。
  [docker/buildx#1913](https://github.com/docker/buildx/pull/1913)
- 修复了有效 docker 上下文可能导致 buildx 构建器名称验证失败的回归。[docker/buildx#1879](https://github.com/docker/buildx/pull/1879)
- 修复了构建期间调整终端大小时可能发生的 panic。
  [docker/buildx#1929](https://github.com/docker/buildx/pull/1929)

## 0.11.0

{{< release-date date="2023-06-13" >}}

此版本的完整发布说明可[在 GitHub 上](https://github.com/docker/buildx/releases/tag/v0.11.0)获得。

### 新功能

- Bake 现在支持 [矩阵构建](/manuals/build/bake/reference.md#targetmatrix)。
  `target` 上的新矩阵字段允许您创建多个相似的目标，以消除 bake 文件中的重复。[docker/buildx#1690](https://github.com/docker/buildx/pull/1690)
- 新的实验性 `--detach` 标志用于在分离模式下运行构建。
  [docker/buildx#1296](https://github.com/docker/buildx/pull/1296),
  [docker/buildx#1620](https://github.com/docker/buildx/pull/1620),
  [docker/buildx#1614](https://github.com/docker/buildx/pull/1614),
  [docker/buildx#1737](https://github.com/docker/buildx/pull/1737),
  [docker/buildx#1755](https://github.com/docker/buildx/pull/1755)
- 新的实验性 [调试监控模式](https://github.com/docker/buildx/blob/v0.11.0-rc1/docs/guides/debugging.md)
  允许您在构建中启动调试会话。
  [docker/buildx#1626](https://github.com/docker/buildx/pull/1626),
  [docker/buildx#1640](https://github.com/docker/buildx/pull/1640)
- 新的 [`EXPERIMENTAL_BUILDKIT_SOURCE_POLICY` 环境变量](./building/variables.md#experimental_buildkit_source_policy)
  用于应用 BuildKit 源策略文件。
  [docker/buildx#1628](https://github.com/docker/buildx/pull/1628)

### 错误修复和增强功能

- `--load` 现在支持在启用 containerd 镜像存储时加载多平台镜像。
  [docker/buildx#1813](https://github.com/docker/buildx/pull/1813)
- 构建进度输出现在显示正在使用的构建器的名称。
  [docker/buildx#1177](https://github.com/docker/buildx/pull/1177)
- Bake 现在支持检测 `compose.{yml,yaml}` 文件。
  [docker/buildx#1752](https://github.com/docker/buildx/pull/1752)
- Bake 现在支持新的 compose 构建键 `dockerfile_inline` 和 `additional_contexts`。
  [docker/buildx#1784](https://github.com/docker/buildx/pull/1784)
- Bake 现在支持 replace HCL 函数。
  [docker/buildx#1720](https://github.com/docker/buildx/pull/1720)
- Bake 现在允许将多个相似的证明参数合并为一个参数，以允许使用单个全局值进行覆盖。
  [docker/buildx#1699](https://github.com/docker/buildx/pull/1699)
- 初步支持 shell 补全。
  [docker/buildx#1727](https://github.com/docker/buildx/pull/1727)
- 对于使用 `docker` 驱动程序的构建器，BuildKit 版本现在可以在 `buildx ls` 和 `buildx inspect` 中正确显示。
  [docker/buildx#1552](https://github.com/docker/buildx/pull/1552)
- 在 buildx 检查视图中显示其他构建器节点详细信息。
  [docker/buildx#1440](https://github.com/docker/buildx/pull/1440),
  [docker/buildx#1854](https://github.com/docker/buildx/pull/1874)
- 使用 `remote` 驱动程序的构建器允许使用 TLS 而无需提供自己的密钥/证书（如果 BuildKit 远程配置为支持它）
  [docker/buildx#1693](https://github.com/docker/buildx/pull/1693)
- 使用 `kubernetes` 驱动程序的构建器支持新的 `serviceaccount` 选项，该选项设置 Kubernetes Pod 的 `serviceAccountName`。
  [docker/buildx#1597](https://github.com/docker/buildx/pull/1597)
- 使用 `kubernetes` 驱动程序的构建器支持 kubeconfig 文件中的 `proxy-url` 选项。
  [docker/buildx#1780](https://github.com/docker/buildx/pull/1780)
- 如果未显式提供名称，使用 `kubernetes` 的构建器现在会自动分配节点名称。
  [docker/buildx#1673](https://github.com/docker/buildx/pull/1673)
- 修复了在 Windows 上为 `docker-container` 驱动程序写入证书时的无效路径。
  [docker/buildx#1831](https://github.com/docker/buildx/pull/1831)
- 修复了使用 SSH 访问远程 bake 文件时的 bake 失败。
  [docker/buildx#1711](https://github.com/docker/buildx/pull/1711),
  [docker/buildx#1734](https://github.com/docker/buildx/pull/1734)
- 修复了远程 bake 上下文被错误解析时的 bake 失败。
  [docker/buildx#1783](https://github.com/docker/buildx/pull/1783)
- 修复了 bake 上下文中 `BAKE_CMD_CONTEXT` 和 `cwd://` 路径的路径解析。
  [docker/buildx#1840](https://github.com/docker/buildx/pull/1840)
- 修复了使用 `buildx imagetools create` 创建镜像时混合 OCI 和 Docker 媒体类型的问题。
  [docker/buildx#1797](https://github.com/docker/buildx/pull/1797)
- 修复了 `--iidfile` 和 `-q` 之间不匹配的镜像 ID。
  [docker/buildx#1844](https://github.com/docker/buildx/pull/1844)
- 修复了混合静态凭据和 IAM 配置文件时的 AWS 身份验证。
  [docker/buildx#1816](https://github.com/docker/buildx/pull/1816)

## 0.10.4

{{< release-date date="2023-03-06" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复和增强功能

- 添加 `BUILDX_NO_DEFAULT_ATTESTATIONS` 作为 `--provenance false` 的替代方案。[docker/buildx#1645](https://github.com/docker/buildx/issues/1645)
- 默认情况下禁用脏 Git 检出检测以提高性能。可以使用 `BUILDX_GIT_CHECK_DIRTY` 选择加入。[docker/buildx#1650](https://github.com/docker/buildx/issues/1650)
- 在发送到 BuildKit 之前从 VCS 提示 URL 中剥离凭据。[docker/buildx#1664](https://github.com/docker/buildx/issues/1664)

## 0.10.3

{{< release-date date="2023-02-16" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复和增强功能

- 修复了收集 Git 来源信息时的可达提交和警告。[docker/buildx#1592](https://github.com/docker/buildx/issues/1592), [docker/buildx#1634](https://github.com/docker/buildx/issues/1634)
- 修复了 docker 上下文未被验证的回归。[docker/buildx#1596](https://github.com/docker/buildx/issues/1596)
- 修复了 JSON bake 定义的函数解析。[docker/buildx#1605](https://github.com/docker/buildx/issues/1605)
- 修复了原始 HCL bake 诊断被丢弃的情况。[docker/buildx#1607](https://github.com/docker/buildx/issues/1607)
- 修复了使用 bake 和 compose 文件时未正确设置的标签。[docker/buildx#1631](https://github.com/docker/buildx/issues/1631)

## 0.10.2

{{< release-date date="2023-01-30" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复和增强功能

- 修复了在多节点构建中未考虑首选平台顺序的问题。[docker/buildx#1561](https://github.com/docker/buildx/issues/1561)
- 修复了处理 `SOURCE_DATE_EPOCH` 环境变量时可能发生的 panic。[docker/buildx#1564](https://github.com/docker/buildx/issues/1564)
- 修复了自 BuildKit v0.11 以来在某些注册表上进行多节点清单合并时可能出现的推送错误。[docker/buildx#1566](https://github.com/docker/buildx/issues/1566)
- 改进了收集 Git 来源信息时的警告。[docker/buildx#1568](https://github.com/docker/buildx/issues/1568)

## 0.10.1

{{< release-date date="2023-01-27" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复和增强功能

- 修复了发送正确的来源 URL 作为 `vsc:source` 元数据。[docker/buildx#1548](https://github.com/docker/buildx/issues/1548)
- 修复了数据竞争导致的可能 panic。[docker/buildx#1504](https://github.com/docker/buildx/issues/1504)
- 修复了 `rm --all-inactive` 的回归。[docker/buildx#1547](https://github.com/docker/buildx/issues/1547)
- 通过延迟加载数据改进 `imagetools inspect` 中的证明访问。[docker/buildx#1546](https://github.com/docker/buildx/issues/1546)
- 正确将功能请求标记为内部。[docker/buildx#1538](https://github.com/docker/buildx/issues/1538)
- 检测无效的证明配置。[docker/buildx#1545](https://github.com/docker/buildx/issues/1545)
- 更新 containerd 补丁以修复影响 `imagetools` 命令的可能推送回归。[docker/buildx#1559](https://github.com/docker/buildx/issues/1559)

## 0.10.0

{{< release-date date="2023-01-10" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 新功能

- `buildx build` 命令支持新的 `--attest` 标志，以及简写 `--sbom` 和 `--provenance`，用于为当前构建添加证明。[docker/buildx#1412](https://github.com/docker/buildx/issues/1412)
  [docker/buildx#1475](https://github.com/docker/buildx/issues/1475)
  - `--attest type=sbom` 或 `--sbom=true` 添加 [SBOM 证明](/manuals/build/metadata/attestations/sbom.md)。
  - `--attest type=provenance` 或 `--provenance=true` 添加 [SLSA 来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。
  - 创建 OCI 镜像时，默认情况下镜像包含最小来源证明。
- 当使用支持来源证明的 BuildKit 构建时，Buildx 将自动共享构建上下文的版本控制信息，以便可以在来源中显示以供后续调试。以前这仅在直接从 Git URL 构建时发生。要退出此行为，您可以设置 `BUILDX_GIT_INFO=0`。可选地，您还可以通过设置 `BUILDX_GIT_LABELS=1` 自动定义带有 VCS 信息的标签。
  [docker/buildx#1462](https://github.com/docker/buildx/issues/1462),
  [docker/buildx#1297](https://github.com/docker/buildx),
  [docker/buildx#1341](https://github.com/docker/buildx/issues/1341),
  [docker/buildx#1468](https://github.com/docker/buildx),
  [docker/buildx#1477](https://github.com/docker/buildx/issues/1477)
- 带有 `--build-context` 的命名上下文现在支持 `oci-layout://` 协议，用于使用本地 OCI 布局目录的值初始化上下文。
  例如 `--build-context stagename=oci-layout://path/to/dir`。此功能需要 BuildKit v0.11.0+ 和 Dockerfile 1.5.0+。[docker/buildx#1456](https://github.com/docker/buildx/issues/1456)
- Bake 现在支持 [资源插值](bake/inheritance.md#reusing-single-attribute-from-targets)，您可以在其中重用其他目标定义中的值。[docker/buildx#1434](https://github.com/docker/buildx/issues/1434)
- 如果您的环境中定义了 `SOURCE_DATE_EPOCH` 环境变量，Buildx 现在将自动转发它。此功能旨在与 BuildKit v0.11.0+ 中更新的 [可重复构建](https://github.com/moby/buildkit/blob/master/docs/build-repro.md) 支持一起使用。[docker/buildx#1482](https://github.com/docker/buildx/issues/1482)
- Buildx 现在会记住构建器的最后活动，以便更好地组织构建器实例。[docker/buildx#1439](https://github.com/docker/buildx/issues/1439)
- Bake 定义现在支持 [变量](bake/reference.md#variable) 和 [标签](bake/reference.md#targetlabels) 的空值，以便构建参数和标签使用 Dockerfile 中设置的默认值。
  [docker/buildx#1449](https://github.com/docker/buildx/issues/1449)
- [`buildx imagetools inspect` 命令](/reference/cli/docker/buildx/imagetools/inspect.md)
  现在支持显示 SBOM 和来源数据。
  [docker/buildx#1444](https://github.com/docker/buildx/issues/1444),
  [docker/buildx#1498](https://github.com/docker/buildx/issues/1498)
- 提高 `ls` 命令和检查流程的性能。
  [docker/buildx#1430](https://github.com/docker/buildx/issues/1430),
  [docker/buildx#1454](https://github.com/docker/buildx/issues/1454),
  [docker/buildx#1455](https://github.com/docker/buildx/issues/1455),
  [docker/buildx#1345](https://github.com/docker/buildx/issues/1345)
- 使用 [Docker 驱动程序](/manuals/build/builders/drivers/docker.md) 添加额外主机现在支持 Docker 特定的 `host-gateway` 特殊值。[docker/buildx#1446](https://github.com/docker/buildx/issues/1446)
- [OCI 导出器](exporters/oci-docker.md) 现在支持 `tar=false` 选项，用于直接在目录中导出 OCI 格式。[docker/buildx#1420](https://github.com/docker/buildx/issues/1420)

### 升级

- 将 Compose 规范更新为 1.6.0。[docker/buildx#1387](https://github.com/docker/buildx/issues/1387)

### 错误修复和增强功能

- `--invoke` 现在可以从镜像元数据加载默认启动环境。[docker/buildx#1324](https://github.com/docker/buildx/issues/1324)
- 修复关于 UserNS 的容器驱动程序行为。[docker/buildx#1368](https://github.com/docker/buildx/issues/1368)
- 修复了在 Bake 中使用错误变量值类型时可能发生的 panic。[docker/buildx#1442](https://github.com/docker/buildx/issues/1442)
- 修复了 `imagetools inspect` 中可能发生的 panic。[docker/buildx#1441](https://github.com/docker/buildx/issues/1441)
  [docker/buildx#1406](https://github.com/docker/buildx/issues/1406)
- 修复了默认向 BuildKit 发送空 `--add-host` 值的问题。[docker/buildx#1457](https://github.com/docker/buildx/issues/1457)
- 修复了处理带有进度组的进度前缀。[docker/buildx#1305](https://github.com/docker/buildx/issues/1305)
- 修复了在 Bake 中递归解析组。[docker/buildx#1313](https://github.com/docker/buildx/issues/1313)
- 修复了多节点构建器清单上可能出现的错误缩进。[docker/buildx#1396](https://github.com/docker/buildx/issues/1396)
- 修复了缺少 OpenTelemetry 配置可能导致的 panic。[docker/buildx#1383](https://github.com/docker/buildx/issues/1383)
- 修复了当 TTY 不可用时 `--progress=tty` 的行为。[docker/buildx#1371](https://github.com/docker/buildx/issues/1371)
- 修复了 `prune` 和 `du` 命令中的连接错误条件。[docker/buildx#1307](https://github.com/docker/buildx/issues/1307)

## 0.9.1

{{< release-date date="2022-08-18" >}}

### 错误修复和增强功能

- `inspect` 命令现在显示正在使用的 BuildKit 版本。[docker/buildx#1279](https://github.com/docker/buildx/issues/1279)
- 修复了构建包含没有构建块的服务的 Compose 文件时的回归。[docker/buildx#1277](https://github.com/docker/buildx/issues/1277)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.9.1)中的完整发布说明。

## 0.9.0

{{< release-date date="2022-08-17" >}}

### 新功能

- 支持新的 [`remote` 驱动程序](/manuals/build/builders/drivers/remote.md)，您可以使用它连接到任何已运行的 BuildKit 实例。
  [docker/buildx#1078](https://github.com/docker/buildx/issues/1078),
  [docker/buildx#1093](https://github.com/docker/buildx/issues/1093),
  [docker/buildx#1094](https://github.com/docker/buildx/issues/1094),
  [docker/buildx#1103](https://github.com/docker/buildx/issues/1103),
  [docker/buildx#1134](https://github.com/docker/buildx/issues/1134),
  [docker/buildx#1204](https://github.com/docker/buildx/issues/1204)
- 即使构建上下文来自外部 Git 或 HTTP URL，您现在也可以从标准输入加载 Dockerfile。[docker/buildx#994](https://github.com/docker/buildx/issues/994)
- 构建命令现在支持新的构建上下文类型 `oci-layout://`，用于 [从本地 OCI 布局目录加载构建上下文](/reference/cli/docker/buildx/build.md#source-oci-layout)。
  请注意，此功能取决于未发布的 BuildKit 功能，在 BuildKit v0.11 发布之前需要使用来自 `moby/buildkit:master` 的构建器实例。[docker/buildx#1173](https://github.com/docker/buildx/issues/1173)
- 您现在可以使用新的 `--print` 标志运行执行构建的 BuildKit 前端支持的辅助函数并打印其结果。您可以在 Dockerfile 中使用此功能来显示当前构建支持的构建参数和密钥（使用 `--print=outline`），并使用 `--print=targets` 列出所有可用的 Dockerfile 阶段。这是一项实验性功能，用于收集早期反馈，需要启用 `BUILDX_EXPERIMENTAL=1` 环境变量。我们计划在未来更新/扩展此功能，而不保留向后兼容性。[docker/buildx#1100](https://github.com/docker/buildx/issues/1100),
  [docker/buildx#1272](https://github.com/docker/buildx/issues/1272)
- 您现在可以使用新的 `--invoke` 标志从构建结果启动交互式容器，以进行交互式调试循环。您可以使用代码更改重新加载这些容器，或从特殊的监视器模式将它们恢复到初始状态。这是一项实验性功能，用于收集早期反馈，需要启用 `BUILDX_EXPERIMENTAL=1` 环境变量。我们计划在未来更新/扩展此功能，而不启用向后兼容性。
  [docker/buildx#1168](https://github.com/docker/buildx/issues/1168),
  [docker/buildx#1257](https://github.com/docker/buildx),
  [docker/buildx#1259](https://github.com/docker/buildx/issues/1259)
- Buildx 现在理解 `BUILDKIT_COLORS` 和 `NO_COLOR` 环境变量，以自定义/禁用交互式构建进度条的颜色。[docker/buildx#1230](https://github.com/docker/buildx/issues/1230),
  [docker/buildx#1226](https://github.com/docker/buildx/issues/1226)
- `buildx ls` 命令现在显示每个构建器实例的当前 BuildKit 版本。[docker/buildx#998](https://github.com/docker/buildx/issues/998)
- `bake` 命令现在在构建 Compose 文件时会自动加载 `.env` 文件以实现兼容性。[docker/buildx#1261](https://github.com/docker/buildx/issues/1261)
- Bake 现在支持带有 `cache_to` 定义的 Compose 文件。[docker/buildx#1155](https://github.com/docker/buildx/issues/1155)
- Bake 现在支持新的内置函数 `timestamp()` 以访问当前时间。[docker/buildx#1214](https://github.com/docker/buildx/issues/1214)
- Bake 现在支持 Compose 构建密钥定义。[docker/buildx#1069](https://github.com/docker/buildx/issues/1069)
- 现在通过 `x-bake` 在 Compose 文件中支持其他构建上下文配置。[docker/buildx#1256](https://github.com/docker/buildx/issues/1256)
- 检查构建器现在显示当前驱动程序选项配置。[docker/buildx#1003](https://github.com/docker/buildx/issues/1003),
  [docker/buildx#1066](https://github.com/docker/buildx/issues/1066)

### 更新

- 将 Compose 规范更新为 1.4.0。[docker/buildx#1246](https://github.com/docker/buildx/issues/1246),
  [docker/buildx#1251](https://github.com/docker/buildx/issues/1251)

### 错误修复和增强功能

- `buildx ls` 命令输出已更新，可以更好地访问来自不同构建器的错误。[docker/buildx#1109](https://github.com/docker/buildx/issues/1109)
- `buildx create` 命令现在执行构建器参数的额外验证，以避免创建配置无效的构建器实例。[docker/buildx#1206](https://github.com/docker/buildx/issues/1206)
- `buildx imagetools create` 命令现在可以创建新的多平台镜像，即使源子镜像位于不同的存储库或注册表中。[docker/buildx#1137](https://github.com/docker/buildx/issues/1137)
- 您现在可以设置默认构建器配置，该配置在创建构建器实例且未传递自定义 `--config` 值时使用。[docker/buildx#1111](https://github.com/docker/buildx/issues/1111)
- Docker 驱动程序现在可以检测 `dockerd` 实例是否支持最初禁用的 Buildkit 功能，如多平台镜像。[docker/buildx#1260](https://github.com/docker/buildx/issues/1260),
  [docker/buildx#1262](https://github.com/docker/buildx/issues/1262)
- 使用名称中带有 `.` 的目标的 Compose 文件现在转换为使用 `_`，以便选择器键仍可在此类目标中使用。[docker/buildx#1011](https://github.com/docker/buildx/issues/1011)
- 包含了检查有效驱动程序配置的额外验证。[docker/buildx#1188](https://github.com/docker/buildx/issues/1188),
  [docker/buildx#1273](https://github.com/docker/buildx/issues/1273)
- `remove` 命令现在显示已删除的构建器，并禁止删除上下文构建器。[docker/buildx#1128](https://github.com/docker/buildx/issues/1128)
- 在使用 Kubernetes 驱动程序时启用 Azure 身份验证。[docker/buildx#974](https://github.com/docker/buildx/issues/974)
- 添加 kubernetes 驱动程序的容忍度处理。[docker/buildx#1045](https://github.com/docker/buildx/issues/1045)
  [docker/buildx#1053](https://github.com/docker/buildx/issues/1053)
- 在 `kubernetes` 驱动程序中用 `securityContext` 替换已弃用的 seccomp 注释。
  [docker/buildx#1052](https://github.com/docker/buildx/issues/1052)
- 修复了处理带有 nil 平台的清单时的 panic。[docker/buildx#1144](https://github.com/docker/buildx/issues/1144)
- 修复了将持续时间过滤器与 `prune` 命令一起使用的问题。[docker/buildx#1252](https://github.com/docker/buildx/issues/1252)
- 修复了在 Bake 定义上合并多个 JSON 文件的问题。[docker/buildx#1025](https://github.com/docker/buildx/issues/1025)
- 修复了从 Docker 上下文创建的隐式构建器具有无效配置或连接中断的问题。[docker/buildx#1129](https://github.com/docker/buildx/issues/1129)
- 修复了使用命名上下文时显示无输出警告的条件。[docker/buildx#968](https://github.com/docker/buildx/issues/968)
- 修复了构建器实例和 docker 上下文具有相同名称时重复构建器的问题。[docker/buildx#1131](https://github.com/docker/buildx/issues/1131)
- 修复了打印不必要的 SSH 警告日志的问题。[docker/buildx#1085](https://github.com/docker/buildx/issues/1085)
- 修复了在使用带有 Bake JSON 定义的空变量块时可能发生的 panic。[docker/buildx#1080](https://github.com/docker/buildx/issues/1080)
- 修复了镜像工具命令未正确处理 `--builder` 标志的问题。[docker/buildx#1067](https://github.com/docker/buildx/issues/1067)
- 修复了将自定义镜像与 rootless 选项一起使用的问题。[docker/buildx#1063](https://github.com/docker/buildx/issues/1063)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.9.0)中的完整发布说明。

## 0.8.2

{{< release-date date="2022-04-04" >}}

### 更新

- 将 `buildx bake` 使用的 Compose 规范更新为 v1.2.1，以修复解析端口定义的问题。[docker/buildx#1033](https://github.com/docker/buildx/issues/1033)

### 错误修复和增强功能

- 修复了处理 BuildKit v0.10 的进度流时可能发生的崩溃。[docker/buildx#1042](https://github.com/docker/buildx/issues/1042)
- 修复了在 `buildx bake` 中解析已被父组加载的组的问题。[docker/buildx#1021](https://github.com/docker/buildx/issues/1021)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.8.2)中的完整发布说明。

## 0.8.1

{{< release-date date="2022-03-21" >}}

### 错误修复和增强功能

- 修复了处理构建上下文扫描错误时可能发生的 panic。[docker/buildx#1005](https://github.com/docker/buildx/issues/1005)
- 允许在 `buildx bake` 中的 Compose 目标名称上使用 `.` 以实现向后兼容性。[docker/buildx#1018](https://github.com/docker/buildx/issues/1018)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.8.1)中的完整发布说明。

## 0.8.0

{{< release-date date="2022-03-09" >}}

### 新功能

- 构建命令现在接受 `--build-context` 标志来 [定义其他命名构建上下文](/reference/cli/docker/buildx/build/#build-context)
  用于您的构建。[docker/buildx#904](https://github.com/docker/buildx/issues/904)
- Bake 定义现在支持 [定义目标之间的依赖关系](bake/contexts.md)
  并在另一个构建中使用一个目标的结果。
  [docker/buildx#928](https://github.com/docker/buildx/issues/928),
  [docker/buildx#965](https://github.com/docker/buildx/issues/965),
  [docker/buildx#963](https://github.com/docker/buildx/issues/963),
  [docker/buildx#962](https://github.com/docker/buildx/issues/962),
  [docker/buildx#981](https://github.com/docker/buildx/issues/981)
- `imagetools inspect` 现在接受 `--format` 标志，允许访问特定镜像的配置和构建信息。[docker/buildx#854](https://github.com/docker/buildx/issues/854),
  [docker/buildx#972](https://github.com/docker/buildx/issues/972)
- 新标志 `--no-cache-filter` 允许配置构建，以便它仅针对指定的 Dockerfile 阶段忽略缓存。[docker/buildx#860](https://github.com/docker/buildx/issues/860)
- 构建现在可以显示构建前端设置的警告摘要。[docker/buildx#892](https://github.com/docker/buildx/issues/892)
- 新的构建参数 `BUILDKIT_INLINE_BUILDINFO_ATTRS` 允许选择加入以将构建属性嵌入到结果镜像中。[docker/buildx#908](https://github.com/docker/buildx/issues/908)
- 新标志 `--keep-buildkitd` 允许在删除构建器时保持 BuildKit 守护进程运行
  - [docker/buildx#852](https://github.com/docker/buildx/issues/852)

### 错误修复和增强功能

- `--metadata-file` 输出现在支持嵌入式结构类型。[docker/buildx#946](https://github.com/docker/buildx/issues/946)
- `buildx rm` 现在接受新标志 `--all-inactive`，用于删除所有当前未运行的构建器。[docker/buildx#885](https://github.com/docker/buildx/issues/885)
- 代理配置现在从 Docker 配置文件读取并随构建请求一起发送以实现向后兼容性。[docker/buildx#959](https://github.com/docker/buildx/issues/959)
- 支持 Compose 中的主机网络。[docker/buildx#905](https://github.com/docker/buildx/issues/905),
  [docker/buildx#880](https://github.com/docker/buildx/issues/880)
- Bake 文件现在可以使用 `-f -` 从 stdin 读取。[docker/buildx#864](https://github.com/docker/buildx/issues/864)
- 无论使用何种驱动程序，`--iidfile` 现在总是写入镜像配置摘要（使用 `--metadata-file` 获取摘要）。[docker/buildx#980](https://github.com/docker/buildx/issues/980)
- Bake 中的目标名称现在被限制为不使用特殊字符。[docker/buildx#929](https://github.com/docker/buildx/issues/929)
- 当使用 `docker` 驱动程序推送时，可以从元数据中读取镜像清单摘要。[docker/buildx#989](https://github.com/docker/buildx/issues/989)
- 修复 Compose 文件中的环境文件处理。[docker/buildx#905](https://github.com/docker/buildx/issues/905)
- 在 `du` 命令中显示上次访问时间。[docker/buildx#867](https://github.com/docker/buildx/issues/867)
- 修复了当多个 Bake 目标运行相同的构建步骤时可能出现的双重输出日志。[docker/buildx#977](https://github.com/docker/buildx/issues/977)
- 修复了多节点构建器构建具有混合平台的多个目标时可能出现的错误。[docker/buildx#985](https://github.com/docker/buildx/issues/985)
- 修复了 Bake 中的一些嵌套继承情况。[docker/buildx#914](https://github.com/docker/buildx/issues/914)
- 修复了 Bake 文件上的默认组打印。[docker/buildx#884](https://github.com/docker/buildx/issues/884)
- 修复了使用 rootless 容器时的 `UsernsMode`。[docker/buildx#887](https://github.com/docker/buildx/issues/887)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.8.0)中的完整发布说明。

## 0.7.1

{{< release-date date="2021-08-25" >}}

### 修复

- 修复了 `.dockerignore` 中排除规则匹配的问题。[docker/buildx#858](https://github.com/docker/buildx/issues/858)
- 修复了当前组的 `bake --print` JSON 输出。[docker/buildx#857](https://github.com/docker/buildx/issues/857)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.7.1)中的完整发布说明。

## 0.7.0

{{< release-date date="2021-11-10" >}}

### 新功能

- 来自 BuildKit 配置的 TLS 证书现在通过 `docker-container` 和 `kubernetes` 驱动程序传输到构建容器。[docker/buildx#787](https://github.com/docker/buildx/issues/787)
- 构建支持 `--ulimit` 标志以实现功能对等。[docker/buildx#800](https://github.com/docker/buildx/issues/800)
- 构建支持 `--shm-size` 标志以实现功能对等。[docker/buildx#790](https://github.com/docker/buildx/issues/790)
- 构建支持 `--quiet` 以实现功能对等。[docker/buildx#740](https://github.com/docker/buildx/issues/740)
- 构建支持 `--cgroup-parent` 标志以实现功能对等。[docker/buildx#814](https://github.com/docker/buildx/issues/814)
- Bake 支持内置变量 `BAKE_LOCAL_PLATFORM`。[docker/buildx#748](https://github.com/docker/buildx/issues/748)
- Bake 支持 Compose 文件中的 `x-bake` 扩展字段。[docker/buildx#721](https://github.com/docker/buildx/issues/721)
- `kubernetes` 驱动程序现在支持冒号分隔的 `KUBECONFIG`。[docker/buildx#761](https://github.com/docker/buildx/issues/761)
- `kubernetes` 驱动程序现在支持使用 `--config` 设置 Buildkit 配置文件。[docker/buildx#682](https://github.com/docker/buildx/issues/682)
- `kubernetes` 驱动程序现在支持使用 driver-opt 安装 QEMU 模拟器。[docker/buildx#682](https://github.com/docker/buildx/issues/682)

### 增强功能

- 允许从客户端使用自定义注册表配置进行多节点推送。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- 允许为 `buildx imagetools` 命令使用自定义注册表配置。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- 允许在使用 `buildx create --bootstrap` 创建后启动构建器。[docker/buildx#692](https://github.com/docker/buildx/issues/692)
- 允许多节点推送使用 `registry:insecure` 输出选项。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- BuildKit 配置和 TLS 文件现在保存在 Buildx 状态目录中，并在需要重新创建 BuildKit 实例时重用。[docker/buildx#824](https://github.com/docker/buildx/issues/824)
- 确保不同项目使用单独的目标目录进行增量上下文传输以获得更好的性能。[docker/buildx#817](https://github.com/docker/buildx/issues/817)
- 构建容器现在默认放置在单独的 cgroup 上。[docker/buildx#782](https://github.com/docker/buildx/issues/782)
- Bake 现在使用 `--print` 打印默认组。[docker/buildx#720](https://github.com/docker/buildx/issues/720)
- `docker` 驱动程序现在通过 HTTP 拨号构建会话以获得更好的性能。[docker/buildx#804](https://github.com/docker/buildx/issues/804)

### 修复

- 修复了将 `--iidfile` 与多节点推送一起使用的问题。[docker/buildx#826](https://github.com/docker/buildx/issues/826)
- 在 Bake 中使用 `--push` 不会清除文件中的其他镜像导出选项。[docker/buildx#773](https://github.com/docker/buildx/issues/773)
- 修复了在使用 `https` 协议时 `buildx bake` 的 Git URL 检测。[docker/buildx#822](https://github.com/docker/buildx/issues/822)
- 修复了在多节点构建上推送具有多个名称的镜像。[docker/buildx#815](https://github.com/docker/buildx/issues/815)
- 避免为不使用它的命令显示 `--builder` 标志。[docker/buildx#818](https://github.com/docker/buildx/issues/818)
- 不受支持的构建标志现在显示警告。[docker/buildx#810](https://github.com/docker/buildx/issues/810)
- 修复了在某些 OpenTelemetry 跟踪中报告错误详细信息的问题。[docker/buildx#812](https://github.com/docker/buildx/issues/812)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.7.0)中的完整发布说明。

## 0.6.3

{{< release-date date="2021-08-30" >}}

### 修复

- 修复 Windows 客户端的 BuildKit 状态卷位置。[docker/buildx#751](https://github.com/docker/buildx/issues/751)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.6.3)中的完整发布说明。

## 0.6.2

{{< release-date date="2021-08-21" >}}

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.6.2)中的完整发布说明。

### 修复

- 修复了某些 SSH 配置中出现的连接错误。[docker/buildx#741](https://github.com/docker/buildx/issues/741)

## 0.6.1

{{< release-date date="2021-07-30" >}}

### 增强功能

- 设置 `ConfigFile` 以使用 Bake 解析 compose 文件。[docker/buildx#704](https://github.com/docker/buildx/issues/704)

### 修复

- 重复的进度环境变量。[docker/buildx#693](https://github.com/docker/buildx/issues/693)
- 应忽略 nil 客户端。[docker/buildx#686](https://github.com/docker/buildx/issues/686)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.6.1)中的完整发布说明。

## 0.6.0

{{< release-date date="2021-07-16" >}}

### 新功能

- 支持 OpenTelemetry 跟踪并将 Buildx 客户端跟踪转发到 BuildKit。[docker/buildx#635](https://github.com/docker/buildx/issues/635)
- 实验性的 GitHub Actions 远程缓存后端，使用 `--cache-to type=gha` 和 `--cache-from type=gha`。[docker/buildx#535](https://github.com/docker/buildx/issues/535)
- 向 build 和 Bake 命令添加了新的 `--metadata-file` 标志，允许以 JSON 格式保存构建结果元数据。[docker/buildx#605](https://github.com/docker/buildx/issues/605)
- 这是第一个支持 Windows ARM64 的版本。[docker/buildx#654](https://github.com/docker/buildx/issues/654)
- 这是第一个支持 Linux Risc-V 的版本。[docker/buildx#652](https://github.com/docker/buildx/issues/652)
- Bake 现在支持使用本地文件或另一个远程源作为上下文从远程定义构建。[docker/buildx#671](https://github.com/docker/buildx/issues/671)
- Bake 现在允许变量相互引用，并在变量中使用用户函数，反之亦然。
  [docker/buildx#575](https://github.com/docker/buildx/issues/575),
  [docker/buildx#539](https://github.com/docker/buildx/issues/539),
  [docker/buildx#532](https://github.com/docker/buildx/issues/532)
- Bake 允许在全局范围内定义属性。[docker/buildx#541](https://github.com/docker/buildx/issues/541)
- Bake 允许跨多个文件的变量。[docker/buildx#538](https://github.com/docker/buildx/issues/538)
- 向进度打印机添加了新的安静模式。[docker/buildx#558](https://github.com/docker/buildx/issues/558)
- `kubernetes` 驱动程序现在支持定义资源/限制。[docker/buildx#618](https://github.com/docker/buildx/issues/618)
- Buildx 二进制文件现在可以通过 [buildx-bin](https://hub.docker.com/r/docker/buildx-bin) Docker 镜像访问。[docker/buildx#656](https://github.com/docker/buildx/issues/656)

### 增强功能

- `docker-container` 驱动程序现在将 BuildKit 状态保存在卷中。启用保留状态的更新。[docker/buildx#672](https://github.com/docker/buildx/issues/672)
- Compose 解析器现在基于新的 [compose-go parser](https://github.com/compose-spec/compose-go)，修复了对某些较新语法的支持。[docker/buildx#669](https://github.com/docker/buildx/issues/669)
- 构建基于 ssh 的 git URL 时，现在会自动转发 SSH 套接字。[docker/buildx#581](https://github.com/docker/buildx/issues/581)
- Bake HCL 解析器已重写。[docker/buildx#645](https://github.com/docker/buildx/issues/645)
- 扩展 HCL 支持更多功能。[docker/buildx#491](https://github.com/docker/buildx/issues/491)
  [docker/buildx#503](https://github.com/docker/buildx/issues/503)
- 允许来自环境变量的密钥。[docker/buildx#488](https://github.com/docker/buildx/issues/488)
- 使用不支持的多平台和加载配置的构建现在会快速失败。[docker/buildx#582](https://github.com/docker/buildx/issues/582)
- 存储 Kubernetes 配置文件以使 buildx 构建器可切换。[docker/buildx#497](https://github.com/docker/buildx/issues/497)
- Kubernetes 现在在检查时将所有 pod 列为节点。[docker/buildx#477](https://github.com/docker/buildx/issues/477)
- 默认 Rootless 镜像已设置为 `moby/buildkit:buildx-stable-1-rootless`。[docker/buildx#480](https://github.com/docker/buildx/issues/480)

### 修复

- `imagetools create` 命令现在正确地将 JSON 描述符与旧描述符混合。[docker/buildx#592](https://github.com/docker/buildx/issues/592)
- 修复了使用 `--network=none` 构建时不需要额外安全授权的问题。[docker/buildx#531](https://github.com/docker/buildx/issues/531)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.6.0)中的完整发布说明。

## 0.5.1

{{< release-date date="2020-12-15" >}}

### 修复

- 修复了在 `kubernetes` 驱动程序之外设置 `buildx create` 上的 `--platform` 时的回归。[docker/buildx#475](https://github.com/docker/buildx/issues/475)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.5.1)中的完整发布说明。

## 0.5.0

{{< release-date date="2020-12-15" >}}

### 新功能

- `docker` 驱动程序现在支持 `--push` 标志。[docker/buildx#442](https://github.com/docker/buildx/issues/442)
- Bake 支持内联 Dockerfile。[docker/buildx#398](https://github.com/docker/buildx/issues/398)
- Bake 支持从远程 URL 和 Git 存储库构建。[docker/buildx#398](https://github.com/docker/buildx/issues/398)
- `BUILDX_CONFIG` 环境变量允许用户拥有与 Docker 配置分开的 buildx 状态。[docker/buildx#385](https://github.com/docker/buildx/issues/385)
- `BUILDKIT_MULTI_PLATFORM` 构建参数允许强制构建多平台返回对象，即使仅指定了一个 `--platform`。[docker/buildx#467](https://github.com/docker/buildx/issues/467)

### 增强功能

- 允许 `--append` 与 `kubernetes` 驱动程序一起使用。[docker/buildx#370](https://github.com/docker/buildx/issues/370)
- 使用 `--debug` 时，构建错误会显示源文件中的错误位置和系统堆栈跟踪。[docker/buildx#389](https://github.com/docker/buildx/issues/389)
- Bake 使用源定义格式化 HCL 错误。[docker/buildx#391](https://github.com/docker/buildx/issues/391)
- Bake 允许数组中的空字符串值，这些值将被丢弃。[docker/buildx#428](https://github.com/docker/buildx/issues/428)
- 您现在可以将 Kubernetes 集群配置与 `kubernetes` 驱动程序一起使用。[docker/buildx#368](https://github.com/docker/buildx/issues/368)
  [docker/buildx#460](https://github.com/docker/buildx/issues/460)
- 创建临时令牌以拉取镜像，而不是在可能的情况下共享凭据。[docker/buildx#469](https://github.com/docker/buildx/issues/469)
- 确保在拉取 BuildKit 容器镜像时传递凭据。[docker/buildx#441](https://github.com/docker/buildx/issues/441)
  [docker/buildx#433](https://github.com/docker/buildx/issues/433)
- 在 `docker-container` 驱动程序中禁用用户命名空间重新映射。[docker/buildx#462](https://github.com/docker/buildx/issues/462)
- 允许 `--builder` 标志切换到默认实例。[docker/buildx#425](https://github.com/docker/buildx/issues/425)
- 避免对空 `BUILDX_NO_DEFAULT_LOAD` 配置值发出警告。[docker/buildx#390](https://github.com/docker/buildx/issues/390)
- 将 `quiet` 选项生成的错误替换为警告。[docker/buildx#403](https://github.com/docker/buildx/issues/403)
- CI 已切换到 GitHub Actions。
  [docker/buildx#451](https://github.com/docker/buildx/issues/451),
  [docker/buildx#463](https://github.com/docker/buildx/issues/463),
  [docker/buildx#466](https://github.com/docker/buildx/issues/466),
  [docker/buildx#468](https://github.com/docker/buildx/issues/468),
  [docker/buildx#471](https://github.com/docker/buildx/issues/471)

### 修复

- 处理小写 Dockerfile 名称作为后备以实现向后兼容性。[docker/buildx#444](https://github.com/docker/buildx/issues/444)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.5.0)中的完整发布说明。

## 0.4.2

{{< release-date date="2020-08-22" >}}

### 新功能

- 支持 `cacheonly` 导出器。[docker/buildx#337](https://github.com/docker/buildx/issues/337)

### 增强功能

- 更新 `go-cty` 以引入更多 `stdlib` 函数。[docker/buildx#277](https://github.com/docker/buildx/issues/277)
- 改进加载时的错误检查。[docker/buildx#281](https://github.com/docker/buildx/issues/281)

### 修复

- 修复了解析带有 HCL 的 json 配置。[docker/buildx#280](https://github.com/docker/buildx/issues/280)
- 确保 `--builder` 从根选项连接。[docker/buildx#321](https://github.com/docker/buildx/issues/321)
- 移除多平台 iidfile 的警告。[docker/buildx#351](https://github.com/docker/buildx/issues/351)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.4.2)中的完整发布说明。

## 0.4.1

{{< release-date date="2020-05-01" >}}

### 修复

- 修复了标志解析的回归。[docker/buildx#268](https://github.com/docker/buildx/issues/268)
- 修复了在 HCL 目标中使用 pull 和 no-cache 键的问题。[docker/buildx#268](https://github.com/docker/buildx/issues/268)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.4.1)中的完整发布说明。

## 0.4.0

{{< release-date date="2020-04-30" >}}

### 新功能

- 添加 `kubernetes` 驱动程序。[docker/buildx#167](https://github.com/docker/buildx/issues/167)
- 新的全局 `--builder` 标志，用于覆盖单个命令的构建器实例。[docker/buildx#246](https://github.com/docker/buildx/issues/246)
- 新的 `prune` 和 `du` 命令，用于管理本地构建器缓存。[docker/buildx#249](https://github.com/docker/buildx/issues/249)
- 您现在可以为 HCL 目标设置新的 `pull` 和 `no-cache` 选项。[docker/buildx#165](https://github.com/docker/buildx/issues/165)

### 增强功能

- 升级 Bake 到 HCL2，支持变量和函数。[docker/buildx#192](https://github.com/docker/buildx/issues/192)
- Bake 现在支持 `--load` 和 `--push`。[docker/buildx#164](https://github.com/docker/buildx/issues/164)
- Bake 现在支持多个目标的通配符覆盖。[docker/buildx#164](https://github.com/docker/buildx/issues/164)
- 容器驱动程序允许通过 `driver-opt` 设置环境变量。[docker/buildx#170](https://github.com/docker/buildx/issues/170)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.4.0)中的完整发布说明。

## 0.3.1

{{< release-date date="2019-09-27" >}}

### 增强功能

- 处理复制 unix 套接字而不是报错。[docker/buildx#155](https://github.com/docker/buildx/issues/155)
  [moby/buildkit#1144](https://github.com/moby/buildkit/issues/1144)

### 修复

- 运行带有多个 Compose 文件的 Bake 现在可以正确合并目标。[docker/buildx#134](https://github.com/docker/buildx/issues/134)
- 修复了从 stdin (`build -f -`) 构建 Dockerfile 时的错误。
  [docker/buildx#153](https://github.com/docker/buildx/issues/153)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.3.1)中的完整发布说明。

## 0.3.0

{{< release-date date="2019-08-02" >}}

### 新功能

- 自定义 `buildkitd` 守护进程标志。[docker/buildx#102](https://github.com/docker/buildx/issues/102)
- `create` 上的驱动程序特定选项。[docker/buildx#122](https://github.com/docker/buildx/issues/122)

### 增强功能

- 环境变量用于 Compose 文件中。[docker/buildx#117](https://github.com/docker/buildx/issues/117)
- Bake 现在遵守 `--no-cache` 和 `--pull`。[docker/buildx#118](https://github.com/docker/buildx/issues/118)
- 自定义 BuildKit 配置文件。[docker/buildx#121](https://github.com/docker/buildx/issues/121)
- 使用 `build --allow` 支持授权。[docker/buildx#104](https://github.com/docker/buildx/issues/104)

### 修复

- 修复了 `--build-arg foo` 不会从环境中读取 `foo` 的错误。[docker/buildx#116](https://github.com/docker/buildx/issues/116)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.3.0)中的完整发布说明。

## 0.2.2

{{< release-date date="2019-05-30" >}}

### 增强功能

- 更改 Compose 文件处理以要求有效的服务规范。[docker/buildx#87](https://github.com/docker/buildx/issues/87)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.2.2)中的完整发布说明。

## 0.2.1

{{< release-date date="2019-05-25" >}}

### 新功能

- 添加 `BUILDKIT_PROGRESS` 环境变量。[docker/buildx#69](https://github.com/docker/buildx/issues/69)
- 添加 `local` 平台。[docker/buildx#70](https://github.com/docker/buildx/issues/70)

### 增强功能

- 如果配置中定义了 arm 变体，则保留它。[docker/buildx#68](https://github.com/docker/buildx/issues/68)
- 使 dockerfile 相对于上下文。[docker/buildx#83](https://github.com/docker/buildx/issues/83)

### 修复

- 修复了从 compose 文件解析目标的问题。[docker/buildx#53](https://github.com/docker/buildx/issues/53)

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.2.1)中的完整发布说明。

## 0.2.0

{{< release-date date="2019-04-25" >}}

### 新功能

- 首次发布

有关更多详细信息，请参阅 [Buildx GitHub 存储库](https://github.com/docker/buildx/releases/tag/v0.2.0)中的完整发布说明。
