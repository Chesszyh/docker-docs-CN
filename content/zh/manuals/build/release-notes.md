---
title: 构建发行说明
weight: 120
description: 了解最新 Buildx 版本的特性、Bug 修复和重大变更
keywords: build, buildx, buildkit, 发行说明
tags: [发行说明]
toc_max: 2
---

本页面包含 [Docker Buildx](https://github.com/docker/buildx) 中的新特性、改进和 Bug 修复信息。

## 0.24.0

{{< release-date date="2025-05-21" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.24.0) 上获取。

### 增强功能

- 在 Bake 的 `variable` 块中添加了新的 `type` 属性，允许显式指定变量类型。[docker/buildx#3167](https://github.com/docker/buildx/pull/3167), [docker/buildx#3189](https://github.com/docker/buildx/pull/3189), [docker/buildx#3198](https://github.com/docker/buildx/pull/3198)
- 在 `history export` 命令中添加了新的 `--finalize` 标志，以便在导出前完成构建追踪。[docker/buildx#3152](https://github.com/docker/buildx/pull/3152)
- Compose 兼容性已更新至 v2.6.3。[docker/buildx#3191](https://github.com/docker/buildx/pull/3191), [docker/buildx#3171](https://github.com/docker/buildx/pull/3171)

### Bug 修复

- 修复了某些构建在完成后可能留下临时文件的问题。[docker/buildx#3133](https://github.com/docker/buildx/pull/3133)
- 修复了启用 containerd-snapshotter 时，使用 Docker 构建返回错误镜像 ID 的问题。[docker/buildx#3136](https://github.com/docker/buildx/pull/3136)
- 修复了在 Bake 中使用空的 `call` 定义时可能发生的 panic。[docker/buildx#3168](https://github.com/docker/buildx/pull/3168)
- 修复了在 Windows 上使用 Bake 时可能出现的 Dockerfile 路径格式错误。[docker/buildx#3141](https://github.com/docker/buildx/pull/3141)
- 修复了 `ls` 命令的 JSON 输出中无法获取当前构建器的问题。[docker/buildx#3179](https://github.com/docker/buildx/pull/3179)
- 修复了 OTEL 上下文未传播到 Docker 守护进程的问题。[docker/buildx#3146](https://github.com/docker/buildx/pull/3146)

## 0.23.0

{{< release-date date="2025-04-15" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.23.0) 上获取。

### 新增

- 新增 `buildx history export` 命令，允许将构建记录导出为可以导入到 [Docker Desktop](/desktop/) 的包。[docker/buildx#3073](https://github.com/docker/buildx/pull/3073)

### 增强功能

- 新增 `--local` 和 `--filter` 标志，允许在 `buildx history ls` 中过滤历史记录。[docker/buildx#3091](https://github.com/docker/buildx/pull/3091)
- Compose 兼容性已更新至 v2.6.0。[docker/buildx#3080](https://github.com/docker/buildx/pull/3080), [docker/buildx#3105](https://github.com/docker/buildx/pull/3105)
- 支持独立模式下的 CLI 环境变量。[docker/buildx#3087](https://github.com/docker/buildx/pull/3087)

### Bug 修复

- 修复了 Bake 的 `--print` 输出产生包含未转义变量的输出，这可能会导致后续构建错误的问题。[docker/buildx#3097](https://github.com/docker/buildx/pull/3097)
- 修复了 `additional_contexts` 字段在指向另一个服务时无法正确工作的问题。[docker/buildx#3090](https://github.com/docker/buildx/pull/3090)
- 修复了空的验证块导致 Bake HCL 解析器崩溃的问题。[docker/buildx#3101](https://github.com/docker/buildx/pull/3101)

## 0.22.0

{{< release-date date="2025-03-18" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.22.0) 上获取。

### 新增

- 新增 `buildx history import` 命令，允许您将构建记录导入到 Docker Desktop 中，以便在 [构建 UI](/desktop/use-desktop/builds/) 中进一步调试。此命令需要安装 [Docker Desktop](/desktop/)。[docker/buildx#3039](https://github.com/docker/buildx/pull/3039)

### 增强功能

- 历史记录现在可以通过 `history inspect`、`history logs` 和 `history open` 命令中的最新偏移量打开（例如 `^1`）。[docker/buildx#3049](https://github.com/docker/buildx/pull/3049), [docker/buildx#3055](https://github.com/docker/buildx/pull/3055)
- Bake 现在支持使用 `--set` 进行覆盖时的 `+=` 追加运算符。[docker/buildx#3031](https://github.com/docker/buildx/pull/3031)
- 如果可用，Docker 容器驱动程序会将 GPU 设备添加到容器中。[docker/buildx#3063](https://github.com/docker/buildx/pull/3063)
- 在 Bake 中使用覆盖时，现在可以设置注解（Annotations）。[docker/buildx#2997](https://github.com/docker/buildx/pull/2997)
- 此版本现在包含 NetBSD 二进制文件。[docker/buildx#2901](https://github.com/docker/buildx/pull/2901)
- 如果节点启动失败，`inspect` 和 `create` 命令现在会返回错误。[docker/buildx#3062](https://github.com/docker/buildx/pull/3062)

### Bug 修复

- 修复了启用 containerd 镜像存储时，使用 Docker 驱动程序重复推送的问题。[docker/buildx#3023](https://github.com/docker/buildx/pull/3023)
- 修复了 `imagetools create` 命令推送多个标签的问题。现在只有最终清单按标签推送。[docker/buildx#3024](https://github.com/docker/buildx/pull/3024)

## 0.21.0

{{< release-date date="2025-02-19" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.21.0) 上获取。

### 新增

- 新增 `buildx history trace` 命令，允许您在基于 Jaeger UI 的查看器中检查构建追踪，并比较不同的追踪。[docker/buildx#2904](https://github.com/docker/buildx/pull/2904)

### 增强功能

- 历史检查命令 `buildx history inspect` 现在支持使用 `--format` 标志进行自定义格式化，并支持 JSON 格式以实现机器可读输出。[docker/buildx#2964](https://github.com/docker/buildx/pull/2964) 
- 在构建和 Bake 中支持 CDI 设备授权（CDI device entitlement）。[docker/buildx#2994](https://github.com/docker/buildx/pull/2994)
- 支持的 CDI 设备现在会显示在构建器检查中。[docker/buildx#2983](https://github.com/docker/buildx/pull/2983)
- 使用 [GitHub 缓存后端 `type=gha`](cache/backends/gha.md) 时，Version 2 或 API 的 URL 现在从环境中读取并发送到 BuildKit。Version 2 后端需要 BuildKit v0.20.0 或更高版本。[docker/buildx#2983](https://github.com/docker/buildx/pull/2983), [docker/buildx#3001](https://github.com/docker/buildx/pull/3001)

### Bug 修复

- 避免在使用 `--progress=rawjson` 时产生不必要的警告和提示。[docker/buildx#2957](https://github.com/docker/buildx/pull/2957)
- 修复了调试 shell 在 `--on=error` 时有时无法正确工作的回归问题。[docker/buildx#2958](https://github.com/docker/buildx/pull/2958)
- 修复了在 Bake 定义中使用未知变量时可能发生的 panic 错误。[docker/buildx#2960](https://github.com/docker/buildx/pull/2960)
- 修复了 `buildx ls` 命令在 JSON 格式化时产生的无效重复输出。[docker/buildx#2970](https://github.com/docker/buildx/pull/2970)
- 修复了 Bake 处理包含多个镜像库引用的 CSV 字符串缓存导入的问题。[docker/buildx#2944](https://github.com/docker/buildx/pull/2944)
- 修复了拉取 BuildKit 镜像时的错误可能被忽略的问题。[docker/buildx#2988](https://github.com/docker/buildx/pull/2988)
- 修复了调试 shell 暂停进度时的竞态问题。[docker/buildx#3003](https://github.com/docker/buildx/pull/3003)

## 0.20.1

{{< release-date date="2025-01-23" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.20.1) 上获取。

### Bug 修复

- 修复了证明（Attestations）缺失某些属性后的 `bake --print` 输出。[docker/buildx#2937](https://github.com/docker/buildx/pull/2937)
- 修复了允许在缓存导入和导出值中使用逗号分隔的镜像引用字符串的问题。[docker/buildx#2944](https://github.com/docker/buildx/pull/2944)

## 0.20.0

{{< release-date date="2025-01-20" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.20.0) 上获取。

> [!NOTE]
>
> 此版本的 buildx 默认对 `buildx bake` 命令启用文件系统授权检查。如果您的 Bake 定义需要读取或写入当前工作目录之外的文件，您需要使用 `--allow fs=<path|*>` 允许访问这些路径。在终端上，您还可以通过提供的提示交互式地批准这些路径。或者，您可以通过设置 `BUILDX_BAKE_ENTITLEMENTS_FS=0` 来禁用这些检查。此验证在 Buildx v0.19.0+ 中会产生警告，但从当前版本开始会产生错误。有关更多信息，请参阅 [参考文档](/reference/cli/docker/buildx/bake.md#allow)。

### 新增

- 添加了新的 `buildx history` 命令，允许处理已完成和正在运行的构建记录。您可以使用这些命令列出、检查、删除您的构建，回放已完成构建的日志，并在 Docker Desktop 构建 UI 中快速打开您的构建以进行进一步调试。这是该命令的早期版本，我们预计在未来的版本中添加更多功能。[#2891](https://github.com/docker/buildx/pull/2891), [#2925](https://github.com/docker/buildx/pull/2925)

### 增强功能

- Bake：定义现在支持以前需要 CSV 字符串作为输入的字段的新对象表示法（`attest`、`output`、`cache-from`、`cache-to`、`secret`、`ssh`）。[docker/buildx#2758](https://github.com/docker/buildx/pull/2758), [docker/buildx#2848](https://github.com/docker/buildx/pull/2848), [docker/buildx#2871](https://github.com/docker/buildx/pull/2871), [docker/buildx#2814](https://github.com/docker/buildx/pull/2814)
- Bake：文件系统授权现在默认报错。要禁用此行为，您可以设置 `BUILDX_BAKE_ENTITLEMENTS_FS=0`。[docker/buildx#2875](https://github.com/docker/buildx/pull/2875)
- Bake：从远程文件推断 Git 身份验证令牌到构建请求。[docker/buildx#2905](https://github.com/docker/buildx/pull/2905)
- Bake：支持使用 `--list` 标志列出目标和变量。[docker/buildx#2900](https://github.com/docker/buildx/pull/2900), [docker/buildx#2907](https://github.com/docker/buildx/pull/2907)
- Bake：更新了默认定义文件的查找顺序，以便稍后加载带有 "override" 后缀的文件。[docker/buildx#2886](https://github.com/docker/buildx/pull/2886)

### Bug 修复

- Bake：修复了默认 SSH 套接字的授权检查。[docker/buildx#2898](https://github.com/docker/buildx/pull/2898)
- Bake：修复了组默认目标中缺失的默认目标。[docker/buildx#2863](https://github.com/docker/buildx/pull/2863)
- Bake：修复了目标平台匹配的命名上下文。[docker/buildx#2877](https://github.com/docker/buildx/pull/2877)
- 修复了静默进度模式缺失的文档。[docker/buildx#2899](https://github.com/docker/buildx/pull/2899)
- 修复了加载层时缺失的最后进度。[docker/buildx#2876](https://github.com/docker/buildx/pull/2876)
- 在创建构建器之前验证 BuildKit 配置。[docker/buildx#2864](https://github.com/docker/buildx/pull/2864)

### 打包

- Compose 兼容性已更新至 v2.4.7。[docker/buildx#2893](https://github.com/docker/buildx/pull/2893), [docker/buildx#2857](https://github.com/docker/buildx/pull/2857), [docker/buildx#2829](https://github.com/docker/buildx/pull/2829)

## 0.19.1

{{< release-date date="2024-11-27" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.19.1) 上获取。

### Bug 修复

- 还原了 v0.19.0 中为 Bake 定义中以前需要 CSV 字符串的字段添加新对象表示法的更改。由于在某些边缘情况下发现了向后不兼容的问题，此项增强已被还原。此功能现已推迟到 v0.20.0 版本。[docker/buildx#2824](https://github.com/docker/buildx/pull/2824)

## 0.19.0

{{< release-date date="2024-11-27" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.19.0) 上获取。

### 新增

- 当您的构建需要读取或写入当前工作目录之外的文件时，Bake 现在要求您允许文件系统授权。[docker/buildx#2796](https://github.com/docker/buildx/pull/2796), [docker/buildx#2812](https://github.com/docker/buildx/pull/2812)。

  要允许文件系统授权，请在 `docker buildx bake` 命令中使用 `--allow fs.read=<path>` 标志。

  此功能目前在使用本地 Bake 定义时仅报告警告，但将从 v0.20 版本开始产生错误。要在当前版本中启用该错误，您可以设置 `BUILDX_BAKE_ENTITLEMENTS_FS=1`。

### 增强功能

- Bake 定义现在支持以前需要 CSV 字符串作为输入的字段的新对象表示法。[docker/buildx#2758](https://github.com/docker/buildx/pull/2758)

  > [!NOTE]
  > 此项增强在 [v0.19.1](#0191) 中因一个 Bug 而被还原。

- Bake 定义现在允许为变量定义验证条件。[docker/buildx#2794](https://github.com/docker/buildx/pull/2794)
- 元数据文件值现在可以包含 JSON 数组值。[docker/buildx#2777](https://github.com/docker/buildx/pull/2777)
- 改进了使用不正确标签格式时的错误消息。[docker/buildx#2778](https://github.com/docker/buildx/pull/2778)
- FreeBSD 和 OpenBSD 构件现在包含在此版本中。[docker/buildx#2774](https://github.com/docker/buildx/pull/2774), [docker/buildx#2775](https://github.com/docker/buildx/pull/2775), [docker/buildx#2781](https://github.com/docker/buildx/pull/2781)

### Bug 修复

- 修复了打印包含空 Compose 网络的目标 Bake 定义时的一个问题。[docker/buildx#2790](https://github.com/docker/buildx/pull/2790)。

### 打包

- Compose 支持已更新至 v2.4.4。[docker/buildx#2806](https://github.com/docker/buildx/pull/2806) [docker/buildx#2780](https://github.com/docker/buildx/pull/2780)。

## 0.18.0

{{< release-date date="2024-10-31" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.18.0) 上获取。

### 新增

- `docker buildx inspect` 命令现在会显示使用 TOML 文件设置的 BuildKit 守护进程配置选项。[docker/buildx#2684](https://github.com/docker/buildx/pull/2684)
- `docker buildx ls` 命令的输出现在默认更加紧凑（通过压缩平台列表）。新的 `--no-trunc` 选项可用于显示完整列表。[docker/buildx#2138](https://github.com/docker/buildx/pull/2138), [docker/buildx#2717](https://github.com/docker/buildx/pull/2717)
- `docker buildx prune` 命令现在支持与 BuildKit v0.17.0+ 构建器配合使用的新的 `--max-used-space` 和 `--min-free-space` 过滤器。[docker/buildx#2766](https://github.com/docker/buildx/pull/2766)

### 增强功能

- 允许使用 [`BUILDX_CPU_PROFILE`](/manuals/build/building/variables.md#buildx_cpu_profile) 和 [`BUILDX_MEM_PROFILE`](/manuals/build/building/variables.md#buildx_mem_profile) 环境变量通过 `pprof` 捕获 CPU 和内存分析数据。[docker/buildx#2746](https://github.com/docker/buildx/pull/2746)
- 增加了来自标准输入的 Dockerfile 最大限制。[docker/buildx#2716](https://github.com/docker/buildx/pull/2716), [docker/buildx#2719](https://github.com/docker/buildx/pull/2719)
- 减少了内存分配。[docker/buildx#2724](https://github.com/docker/buildx/pull/2724), [docker/buildx#2713](https://github.com/docker/buildx/pull/2713)
- `docker buildx bake` 的 `--list-targets` 和 `--list-variables` 标志不再需要初始化构建器。[docker/buildx#2763](https://github.com/docker/buildx/pull/2763)

### Bug 修复

- 检查警告现在会打印违规 Dockerfile 的完整文件路径（相对于当前工作目录）。[docker/buildx#2672](https://github.com/docker/buildx/pull/2672)
- `--check` 和 `--call` 选项的回退镜像（Fallback images）已更新为正确的引用。[docker/buildx#2705](https://github.com/docker/buildx/pull/2705)
- 修复了构建详情链接在实验模式下不显示的问题。[docker/buildx#2722](https://github.com/docker/buildx/pull/2722)
- 修复了 Bake 无效目标链接的验证问题。[docker/buildx#2700](https://github.com/docker/buildx/pull/2700)
- 修复了运行无效命令时缺失错误消息的问题。[docker/buildx#2741](https://github.com/docker/buildx/pull/2741)
- 修复了 `--call` 请求中可能出现的本地状态错误警告。[docker/buildx#2754](https://github.com/docker/buildx/pull/2754)
- 修复了在 Bake 中使用链接目标时可能出现的授权问题。[docker/buildx#2701](https://github.com/docker/buildx/pull/2701)
- 修复了在使用 `sudo` 运行 Buildx 后访问本地状态时可能出现的权限问题。[docker/buildx#2745](https://github.com/docker/buildx/pull/2745)

### 打包

- Compose 兼容性已更新至 v2.4.1。[docker/buildx#2760](https://github.com/docker/buildx/pull/2760)

## 0.17.1

{{< release-date date="2024-09-13" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.17.1) 上获取。

### Bug 修复

- 如果在 [BuildKit 配置文件](/manuals/build/buildkit/toml-configuration.md) 中设置了授权，则在为 `docker-container` 和 `kubernetes` 驱动程序创建构建器时，不自动设置 `network.host` 授权标志。[docker/buildx#2685]
- 使用 `docker buildx bake --print` 时，如果 `network` 字段为空，则不打印该字段。[docker/buildx#2689]
- 修复了 WSL2 下的遥测套接字路径。[docker/buildx#2698]

[docker/buildx#2685]: https://github.com/docker/buildx/pull/2685
[docker/buildx#2689]: https://github.com/docker/buildx/pull/2689
[docker/buildx#2698]: https://github.com/docker/buildx/pull/2698

## 0.17.0

{{< release-date date="2024-09-10" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.17.0) 上获取。

### 新增

- 为 Bake 添加了 `basename`、`dirname` 和 `sanitize` 函数。[docker/buildx#2649]
- 启用了对 Bake 授权的支持，以允许构建期间的特权操作。[docker/buildx#2666]

### 增强功能

- 为 Bake 命令引入了 CLI 指标跟踪。[docker/buildx#2610]
- 为所有构建命令添加了 `--debug`。以前，它仅在顶级 `docker` 和 `docker buildx` 命令中可用。[docker/buildx#2660]
- 允许从标准输入为多节点构建器进行构建。[docker/buildx#2656]
- 改进了 `kubernetes` 驱动程序的初始化。[docker/buildx#2606]
- 在使用 Bake 构建多个目标时，在错误消息中包含目标名称。[docker/buildx#2651]
- 优化了指标处理，以减少进度跟踪期间的性能开销。[docker/buildx#2641]
- 完成规则检查后显示警告数量。[docker/buildx#2647]
- 跳过前端方法的构建引用和来源元数据。[docker/buildx#2650]
- 增加了对在 Bake 文件（HCL 和 JSON）中设置网络模式的支持。[docker/buildx#2671]
- 当与 `--call` 标志一起设置时，支持 `--metadata-file` 标志。[docker/buildx#2640]
- 为多个 Bake 目标使用的本地上下文使用共享会话。[docker/buildx#2615], [docker/buildx#2607], [docker/buildx#2663]

### Bug 修复

- 改进了内存管理以避免不必要的分配。[docker/buildx#2601]

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

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.16.2) 上获取。

### Bug 修复

- 修复了将本地缓存导出到 NFS 卷时可能出现的 "bad file descriptor" 错误。[docker/buildx#2629](https://github.com/docker/buildx/pull/2629/)

## 0.16.1

{{< release-date date="2024-07-18" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.16.1) 上获取。

### Bug 修复

- 修复了 `buildx bake --print` 命令中由于数据竞态可能导致的 panic。[docker/buildx#2603](https://github.com/docker/buildx/pull/2603/)
- 改进了关于使用 `--debug` 标志检查构建警告的消息。[docker/buildx#2612](https://github.com/docker/buildx/pull/2612/)

## 0.16.0

{{< release-date date="2024-07-11" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.16.0) 上获取。

### 新增

- Bake 命令现在支持 `--call` 和 `--check` 标志以及目标定义中的 `call` 属性，用于选择自定义前端方法。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/), [docker/buildx#2576](https://github.com/docker/buildx/pull/2576/)
- {{< badge color=violet text=实验性 >}} Bake 现在支持 `--list-targets` 和 `--list-variables` 标志，用于检查项目的定义和可能的配置选项。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/)
- Bake 定义变量和目标支持新的 `description` 属性，用于定义可以使用例如 `--list-targets` 和 `--list-variables` 检查的基于文本的描述。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/)
- Bake 现在支持打印构建检查违规的警告。[docker/buildx#2501](https://github.com/docker/buildx/pull/2501/)

### 增强功能

- 构建命令现在确保多节点构建为每个节点使用相同的构建引用。[docker/buildx#2572](https://github.com/docker/buildx/pull/2572/)
- 避免重复请求并提高远程驱动程序的性能。[docker/buildx#2501](https://github.com/docker/buildx/pull/2501/)
- 现在可以通过设置 `BUILDX_METADATA_WARNINGS=1` 环境变量将构建警告保存到元数据文件中。[docker/buildx#2551](https://github.com/docker/buildx/pull/2551/), [docker/buildx#2521](https://github.com/docker/buildx/pull/2521/), [docker/buildx#2550](https://github.com/docker/buildx/pull/2550/)
- 改进了未检测到警告时 `--check` 标志的消息。[docker/buildx#2549](https://github.com/docker/buildx/pull/2549/)

### Bug 修复

- 修复了构建期间多类型注解的支持。[docker/buildx#2522](https://github.com/docker/buildx/pull/2522/)
- 修复了一个回归问题，即由于增量传输重用，在切换项目时可能会发生效率低下的文件传输。[docker/buildx#2558](https://github.com/docker/buildx/pull/2558/)
- 修复了链式 Bake 目标的不正确默认加载。[docker/buildx#2583](https://github.com/docker/buildx/pull/2583/)
- 修复了 Bake 中不正确的 `COMPOSE_PROJECT_NAME` 处理。[docker/buildx#2579](https://github.com/docker/buildx/pull/2579/)
- 修复了多节点构建的索引注解（index annotations）支持。[docker/buildx#2546](https://github.com/docker/buildx/pull/2546/)
- 修复了从远程上下文捕获构建的来源元数据。[docker/buildx#2560](https://github.com/docker/buildx/pull/2560/)

### 打包更新

- Compose 支持已更新至 v2.1.3。[docker/buildx#2547](https://github.com/docker/buildx/pull/2547/)

## 0.15.1

{{< release-date date="2024-06-18" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.15.1) 上获取。

### Bug 修复

- 修复了某些带 `--check` 的验证请求缺失构建错误和退出代码的问题。[docker/buildx#2518](https://github.com/docker/buildx/pull/2518/)
- 将 `--check` 的回退镜像更新至 Dockerfile v1.8.1。[docker/buildx#2538](https://github.com/docker/buildx/pull/2538/)

## 0.15.0

{{< release-date date="2024-06-11" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.15.0) 上获取。

### 新增

- 新的 `--call` 选项允许为构建设置评估方法，取代了以前实验性的 `--print` 标志。[docker/buildx#2498](https://github.com/docker/buildx/pull/2498/), [docker/buildx#2487](https://github.com/docker/buildx/pull/2487/), [docker/buildx#2513](https://github.com/docker/buildx/pull/2513/)

  除了默认的 `build` 方法外，Dockerfile 前端还实现了以下方法：

  - [`--call=check`](/reference/cli/docker/buildx/build.md#check)：运行构建配置的验证程序。有关构建检查的更多信息，请参阅 [构建检查](/manuals/build/checks.md)
  - [`--call=outline`](/reference/cli/docker/buildx/build.md#call-outline)：显示当前构建将使用的配置，包括构建将使用的所有构建参数、密钥（Secrets）、SSH 挂载等。
  - [`--call=targets`](/reference/cli/docker/buildx/build.md#call-targets)：显示所有可用的目标及其描述。

- `docker buildx imagetools create` 命令中添加了新的 `--prefer-index` 标志，用于控制从单个平台镜像清单创建镜像的行为。[docker/buildx#2482](https://github.com/docker/buildx/pull/2482/)
- [`kubernetes` 驱动程序](/manuals/build/builders/drivers/kubernetes.md) 现在支持 `timeout` 选项用于配置部署超时。[docker/buildx#2492](https://github.com/docker/buildx/pull/2492/)
- 为构建警告类型添加了新的指标定义。[docker/buildx#2482](https://github.com/docker/buildx/pull/2482/), [docker/buildx#2507](https://github.com/docker/buildx/pull/2507/)
- [`buildx prune`](/reference/cli/docker/buildx/prune.md) 和 [`buildx du`](/reference/cli/docker/buildx/du.md) 命令现在支持负向和前缀过滤器。[docker/buildx#2473](https://github.com/docker/buildx/pull/2473/)
- 使用 Bake 构建 Compose 文件现在支持传递 SSH 转发配置。[docker/buildx#2445](https://github.com/docker/buildx/pull/2445/)
- 修复了使用自定义 TLS 证书配置 `kubernetes` 驱动程序的问题。[docker/buildx#2454](https://github.com/docker/buildx/pull/2454/)
- 修复了加载节点时并发访问 kubeconfig 的问题。[docker/buildx#2497](https://github.com/docker/buildx/pull/2497/)

### 打包更新

- Compose 支持已更新至 v2.1.2。[docker/buildx#2502](https://github.com/docker/buildx/pull/2502/), [docker/buildx#2425](https://github.com/docker/buildx/pull/2425/)

## 0.14.0

{{< release-date date="2024-04-18" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.14.0) 上获取。

### 增强功能

- 增加了对 `--print=lint` 的支持（实验性）。[docker/buildx#2404](https://github.com/docker/buildx/pull/2404), [docker/buildx#2406](https://github.com/docker/buildx/pull/2406)
- 修复了前端打印子请求自定义实现的 JSON 格式化问题。[docker/buildx#2374](https://github.com/docker/buildx/pull/2374)
- 使用 `--metadata-file` 构建时，现在会设置来源记录（Provenance records）。[docker/buildx#2280](https://github.com/docker/buildx/pull/2280)
- 为远程定义添加了 [Git 身份验证支持](./bake/remote-definition.md#remote-definition-in-a-private-repository)。[docker/buildx#2363](https://github.com/docker/buildx/pull/2363)
- 为 `docker-container`、`remote` 和 `kubernetes` 驱动程序新增了 `default-load` 选项，用于默认将构建结果加载到 Docker Engine 镜像存储中。[docker/buildx#2259](https://github.com/docker/buildx/pull/2259)
- 为 [`kubernetes` 驱动程序](/manuals/build/builders/drivers/kubernetes.md) 添加了 `requests.ephemeral-storage`、`limits.ephemeral-storage` 和 `schedulername` 选项。[docker/buildx#2370](https://github.com/docker/buildx/pull/2370), [docker/buildx#2415](https://github.com/docker/buildx/pull/2415)
- 为 `docker-bake.hcl` 文件添加了 `indexof` 函数。[docker/buildx#2384](https://github.com/docker/buildx/pull/2384)
- Buildx 的 OpenTelemetry 指标现在可以测量空闲时间、镜像导出、运行操作以及构建期间镜像源操作的镜像传输时长。[docker/buildx#2316](https://github.com/docker/buildx/pull/2316), [docker/buildx#2317](https://github.com/docker/buildx/pull/2317), [docker/buildx#2323](https://github.com/docker/buildx/pull/2323), [docker/buildx#2271](https://github.com/docker/buildx/pull/2271)
- 发送到与 `desktop-linux` 上下文关联的 OpenTelemetry 端点的构建进度指标不再需要 Buildx 处于实验模式 (`BUILDX_EXPERIMENTAL=1`)。[docker/buildx#2344](https://github.com/docker/buildx/pull/2344)

### Bug 修复

- 修复了 `--load` 和 `--push` 在与多个 Bake 文件定义一起使用时，错误地覆盖输出的问题。[docker/buildx#2336](https://github.com/docker/buildx/pull/2336)
- 修复了启用实验模式时从标准输入构建的问题。[docker/buildx#2394](https://github.com/docker/buildx/pull/2394)
- 修复了委托追踪（Delegated traces）可能重复的问题。[docker/buildx#2362](https://github.com/docker/buildx/pull/2362)

### 打包更新

- Compose 支持已更新至 [v2.26.1](https://github.com/docker/compose/releases/tag/v2.26.1)（通过 [`compose-go` v2.0.2](https://github.com/compose-spec/compose-go/releases/tag/v2.0.2)）。[docker/buildx#2391](https://github.com/docker/buildx/pull/2391)

## 0.13.1

{{< release-date date="2024-03-13" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.13.1) 上获取。

### Bug 修复

- 修复了使用远程驱动程序连接到 `docker-container://` 和 `kube-pod://` 样式 URL 的问题。[docker/buildx#2327](https://github.com/docker/buildx/pull/2327)
- 修复了当目标已定义非镜像输出时，Bake 处理 `--push` 的问题。[docker/buildx#2330](https://github.com/docker/buildx/pull/2330)

## 0.13.0

{{< release-date date="2024-03-06" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.13.0) 上获取。

### 新增

- 新增 `docker buildx dial-stdio` 命令，用于直接联系配置的构建器实例的 BuildKit 守护进程。[docker/buildx#2112](https://github.com/docker/buildx/pull/2112)
- 现在可以使用 `remote` 驱动程序和 npipe 连接创建 Windows 容器构建器。[docker/buildx#2287](https://github.com/docker/buildx/pull/2287)
- Windows 上现在支持 Npipe URL 方案。[docker/buildx#2250](https://github.com/docker/buildx/pull/2250)
- {{< badge color=violet text=实验性 >}} Buildx 现在可以导出用于构建时长和传输大小的 OpenTelemetry 指标。[docker/buildx#2235](https://github.com/docker/buildx/pull/2235), [docker/buildx#2258](https://github.com/docker/buildx/pull/2258) [docker/buildx#2225](https://github.com/docker/buildx/pull/2225) [docker/buildx#2224](https://github.com/docker/buildx/pull/2224) [docker/buildx#2155](https://github.com/docker/buildx/pull/2155)

### 增强功能

- Bake 命令现在支持定义 `shm-size` 和 `ulimit` 值。[docker/buildx#2279](https://github.com/docker/buildx/pull/2279), [docker/buildx#2242](https://github.com/docker/buildx/pull/2242)
- 更好地处理使用远程驱动程序连接到不健康节点的情况。[docker/buildx#2130](https://github.com/docker/buildx/pull/2130)
- 使用 `docker-container` 和 `kubernetes` 驱动程序的构建器现在默认允许 `network.host` 授权（允许访问容器的网络）。[docker/buildx#2266](https://github.com/docker/buildx/pull/2266)
- 构建现在可以使用单个命令使用多个输出（需要 BuildKit v0.13+）。[docker/buildx#2290](https://github.com/docker/buildx/pull/2290), [docker/buildx#2302](https://github.com/docker/buildx/pull/2302)
- 现在可以通过配置的跟踪分支找到默认 Git 仓库路径。[docker/buildx#2146](https://github.com/docker/buildx/pull/2146)
- 修复了在 Bake 中使用链接目标时可能出现的缓存失效问题。[docker/buildx#2265](https://github.com/docker/buildx/pull/2265)
- 修复了 WSL 中 Git 仓库路径清理的问题。[docker/buildx#2167](https://github.com/docker/buildx/pull/2167)
- 现在可以使用单个命令移除多个构建器。[docker/buildx#2140](https://github.com/docker/buildx/pull/2140)
- 通过 Unix 套接字新增了取消信号处理。[docker/buildx#2184](https://github.com/docker/buildx/pull/2184) [docker/buildx#2289](https://github.com/docker/buildx/pull/2289)
- Compose 规范支持已更新至 v2.0.0-rc.8。[docker/buildx#2205](https://github.com/docker/buildx/pull/2205)
- `docker buildx create` 的 `--config` 标志已重命名为 `--buildkitd-config`。[docker/buildx#2268](https://github.com/docker/buildx/pull/2268)
- `docker buildx build` 的 `--metadata-file` 标志现在还可以返回构建引用，可用于进一步的构建调试，例如在 Docker Desktop 中。[docker/buildx#2263](https://github.com/docker/buildx/pull/2263)
- `docker buildx bake` 命令现在为所有目标共享相同的身份验证提供程序，以提高性能。[docker/buildx#2147](https://github.com/docker/buildx/pull/2147)
- `docker buildx imagetools inspect` 命令现在会显示 DSSE 签名的 SBOM 和来源证明。[docker/buildx#2194](https://github.com/docker/buildx/pull/2194)
- `docker buildx ls` 命令现在支持用于控制输出的 `--format` 选项。[docker/buildx#1787](https://github.com/docker/buildx/pull/1787)
- `docker-container` 驱动程序现在支持用于定义 BuildKit 容器重启策略的驱动程序选项。[docker/buildx#1271](https://github.com/docker/buildx/pull/1271)
- 从 Buildx 导出的 VCS 属性现在包含本地目录子路径（如果它们相对于当前 Git 仓库）。[docker/buildx#2156](https://github.com/docker/buildx/pull/2156)
- `--add-host` 标志现在允许 IPv6 地址使用 `=` 分隔符。[docker/buildx#2121](https://github.com/docker/buildx/pull/2121)

### Bug 修复

- 修复了使用 `--progress=rawjson` 导出进度时的额外输出。[docker/buildx#2252](https://github.com/docker/buildx/pull/2252)
- 修复了 Windows 上可能出现的控制台警告。[docker/buildx#2238](https://github.com/docker/buildx/pull/2238)
- 修复了在使用许多配置进行 Bake 时可能出现的不一致配置合并顺序。[docker/buildx#2237](https://github.com/docker/buildx/pull/2237)
- 修复了 `docker buildx imagetools create` 命令中可能出现的 panic。[docker/buildx#2230](https://github.com/docker/buildx/pull/2230)

## 0.12.1

{{< release-date date="2024-01-12" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.12.1) 上获取。

### Bug 修复和增强功能

- 修复了一些 `--driver-opt` 值验证不正确的问题，这可能会导致 panic 并存储损坏的状态。[docker/buildx#2176](https://github.com/docker/buildx/pull/2176)

## 0.12.0

{{< release-date date="2023-11-16" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.12.0) 上获取。

### 新增

- `buildx build` 新增 `--annotation` 标志，Bake 文件中新增 `annotations` 键，允许您为构建结果添加 OCI 注解。[#2020](https://github.com/docker/buildx/pull/2020), [#2098](https://github.com/docker/buildx/pull/2098)
- 新的实验性调试功能，包括新的 `debug` 命令和交互式调试控制台。此功能目前需要设置 `BUILDX_EXPERIMENTAL=1`。[#2006](https://github.com/docker/buildx/pull/2006), [#1896](https://github.com/docker/buildx/pull/1896), [#1970](https://github.com/docker/buildx/pull/1970), [#1914](https://github.com/docker/buildx/pull/1914), [#2026](https://github.com/docker/buildx/pull/2026), [#2086](https://github.com/docker/buildx/pull/2086)

### Bug 修复和增强功能

- 特殊的 `host-gateway` IP 映射现在可以在构建期间与 `--add-host` 标志配合使用。[#1894](https://github.com/docker/buildx/pull/1894), [#2083](https://github.com/docker/buildx/pull/2083)
- Bake 现在允许在从远程定义构建时添加本地源文件。[#1838](https://github.com/docker/buildx/pull/1838)
- 构建结果上传到 Docker 的状态现在会交互式地显示在进度条上。[#1994](https://github.com/docker/buildx/pull/1994)
- 改进了引导多节点构建集群时的错误处理。[#1869](https://github.com/docker/buildx/pull/1869)
- `buildx imagetools create` 命令现在允许在镜像库中创建新镜像时添加注解。[#1965](https://github.com/docker/buildx/pull/1965)
- 现在可以使用 Docker 和远程驱动程序实现来自 buildx 的 OpenTelemetry 构建追踪委托。[#2034](https://github.com/docker/buildx/pull/2034)
- Bake 命令现在会在进度条上显示加载构建定义的所有文件。[#2076](https://github.com/docker/buildx/pull/2076)
- Bake 文件现在允许在多个定义文件中定义相同的属性。[#1062](https://github.com/docker/buildx/pull/1062)
- 将 Bake 命令与远程定义配合使用时，现在允许该定义使用本地 Dockerfile。[#2015](https://github.com/docker/buildx/pull/2015)
- Docker 容器驱动程序现在显式设置 BuildKit 配置路径，以确保从主流镜像和 rootless 镜像的相同位置加载配置。[#2093](https://github.com/docker/buildx/pull/2093)
- 提高了检测 BuildKit 实例何时完成启动的性能。[#1934](https://github.com/docker/buildx/pull/1934)
- 容器驱动程序现在接受许多新的驱动程序选项，用于定义 BuildKit 容器的资源限制。[#2048](https://github.com/docker/buildx/pull/2048)
- 改进了检查命令的格式化。[#2068](https://github.com/docker/buildx/pull/2068)
- 改进了关于驱动程序能力的错误消息。[#1998](https://github.com/docker/buildx/pull/1998)
- 改进了在不带目标的情况下调用 Bake 命令时的错误消息。[#2100](https://github.com/docker/buildx/pull/2100)
- 允许在独立模式运行时使用环境变量启用调试日志。[#1821](https://github.com/docker/buildx/pull/1821)
- 使用 Docker 驱动程序时，默认的镜像解析模式已更新为首选本地 Docker 镜像，以保持向后兼容性。[#1886](https://github.com/docker/buildx/pull/1886)
- Kubernetes 驱动程序现在允许为 BuildKit 部署和 Pod 设置自定义注解和标签。[#1938](https://github.com/docker/buildx/pull/1938)
- Kubernetes 驱动程序现在允许通过端点配置设置身份验证令牌。[#1891](https://github.com/docker/buildx/pull/1891)
- 修复了 Bake 中链式目标的可能问题，该问题可能导致构建失败或某个目标的本地源被多次上传。[#2113](https://github.com/docker/buildx/pull/2113)
- 修复了在使用 Bake 命令的矩阵（matrix）功能时访问全局目标属性的问题。[#2106](https://github.com/docker/buildx/pull/2106)
- 修复了某些构建标志的格式验证。[#2040](https://github.com/docker/buildx/pull/2040)
- 修复了避免在启动构建器节点时由于不必要的原因锁定某些命令的问题。[#2066](https://github.com/docker/buildx/pull/2066)
- 修复了多个构建尝试并行引导同一个构建器实例的情况。[#2000](https://github.com/docker/buildx/pull/2000)
- 修复了在某些情况下上传构建结果到 Docker 的错误可能被丢弃的情况。[#1927](https://github.com/docker/buildx/pull/1927)
- 修复了根据构建输出检测缺失证明支持的能力。[#1988](https://github.com/docker/buildx/pull/1988)
- 修复了加载 Bake 远程定义的构建，使其不显示在构建历史记录中。[#1961](https://github.com/docker/buildx/pull/1961), [#1954](https://github.com/docker/buildx/pull/1954)
- 修复了使用 Bake 构建定义了配置（Profiles）的 Compose 文件时的错误。[#1903](https://github.com/docker/buildx/pull/1903)
- 修复了进度条上可能出现的时间校正错误。[#1968](https://github.com/docker/buildx/pull/1968)
- 修复了向使用新控制器界面的构建传递自定义 cgroup 父级的问题。[#1913](https://github.com/docker/buildx/pull/1913)

### 打包

- Compose 支持已更新至 1.20，在使用 Bake 命令时启用了 "include" 功能。[#1971](https://github.com/docker/buildx/pull/1971), [#2065](https://github.com/docker/buildx/pull/2065), [#2094](https://github.com/docker/buildx/pull/2094)

## 0.11.2

{{< release-date date="2023-07-18" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.11.2) 上获取。

### Bug 修复和增强功能

- 修复了一个导致 buildx 不从实例存储中读取 `KUBECONFIG` 路径的回归问题。[docker/buildx#1941](https://github.com/docker/buildx/pull/1941)
- 修复了一个导致结果处理构建错误地出现在构建历史记录中的回归问题。[docker/buildx#1954](https://github.com/docker/buildx/pull/1954)

## 0.11.1

{{< release-date date="2023-07-05" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.11.1) 上获取。

### Bug 修复和增强功能

- 修复了 Bake 中配置中的服务无法加载的回归问题。[docker/buildx#1903](https://github.com/docker/buildx/pull/1903)
- 修复了 `--cgroup-parent` 选项在构建期间无效的回归问题。[docker/buildx#1913](https://github.com/docker/buildx/pull/1913)
- 修复了有效的 Docker 上下文可能导致 buildx 构建器名称验证失败的回归问题。[docker/buildx#1879](https://github.com/docker/buildx/pull/1879)
- 修复了构建期间调整终端大小时可能发生的 panic。[docker/buildx#1929](https://github.com/docker/buildx/pull/1929)

## 0.11.0

{{< release-date date="2023-06-13" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/docker/buildx/releases/tag/v0.11.0) 上获取。

### 新增

- Bake 现在支持 [矩阵构建](/manuals/build/bake/reference.md#targetmatrix)。`target` 上的新矩阵字段允许您创建多个类似的目标，以减少 Bake 文件中的重复。[docker/buildx#1690](https://github.com/docker/buildx/pull/1690)
- 新的实验性 `--detach` 标志，用于在分离模式下运行构建。[docker/buildx#1296](https://github.com/docker/buildx/pull/1296), [docker/buildx#1620](https://github.com/docker/buildx/pull/1620), [docker/buildx#1614](https://github.com/docker/buildx/pull/1614), [docker/buildx#1737](https://github.com/docker/buildx/pull/1737), [docker/buildx#1755](https://github.com/docker/buildx/pull/1755)
- 新的实验性 [调试监控模式](https://github.com/docker/buildx/blob/v0.11.0-rc1/docs/guides/debugging.md)，允许您在构建中启动调试会话。[docker/buildx#1626](https://github.com/docker/buildx/pull/1626), [docker/buildx#1640](https://github.com/docker/buildx/pull/1640)
- 新的 [`EXPERIMENTAL_BUILDKIT_SOURCE_POLICY` 环境变量](./building/variables.md#experimental_buildkit_source_policy)，用于应用 BuildKit 源策略文件。[docker/buildx#1628](https://github.com/docker/buildx/pull/1628)

### Bug 修复和增强功能

- 启用 containerd 镜像存储后，`--load` 现在支持加载多平台镜像。[docker/buildx#1813](https://github.com/docker/buildx/pull/1813)
- 构建进度输出现在会显示正在使用的构建器名称。[docker/buildx#1177](https://github.com/docker/buildx/pull/1177)
- Bake 现在支持检测 `compose.{yml,yaml}` 文件。[docker/buildx#1752](https://github.com/docker/buildx/pull/1752)
- Bake 现在支持新的 Compose 构建键 `dockerfile_inline` 和 `additional_contexts`。[docker/buildx#1784](https://github.com/docker/buildx/pull/1784)
- Bake 现在支持 replace HCL 函数。[docker/buildx#1720](https://github.com/docker/buildx/pull/1720)
- Bake 现在允许将多个类似的证明参数合并为单个参数，以便使用单个全局值进行覆盖。[docker/buildx#1699](https://github.com/docker/buildx/pull/1699)
- 对 shell 补全的初步支持。[docker/buildx#1727](https://github.com/docker/buildx/pull/1727)
- 使用 `docker` 驱动程序的构建器在 `buildx ls` 和 `buildx inspect` 中现在可以正确显示 BuildKit 版本。[docker/buildx#1552](https://github.com/docker/buildx/pull/1552)
- 在 buildx 检查视图中显示额外的构建器节点详情。[docker/buildx#1440](https://github.com/docker/buildx/pull/1440), [docker/buildx#1854](https://github.com/docker/buildx/pull/1874)
- 使用 `remote` 驱动程序的构建器允许在不证明其自身密钥/证书的情况下使用 TLS（如果远程 BuildKit 配置为支持它）。[docker/buildx#1693](https://github.com/docker/buildx/pull/1693)
- 使用 `kubernetes` 驱动程序的构建器支持新的 `serviceaccount` 选项，用于设置 Kubernetes Pod 的 `serviceAccountName`。[docker/buildx#1597](https://github.com/docker/buildx/pull/1597)
- 使用 `kubernetes` 驱动程序的构建器支持 kubeconfig 文件中的 `proxy-url` 选项。[docker/buildx#1780](https://github.com/docker/buildx/pull/1780)
- 如果没有显式提供名称，使用 `kubernetes` 的构建器现在会自动分配节点名称。[docker/buildx#1673](https://github.com/docker/buildx/pull/1673)
- 修复了在 Windows 上为 `docker-container` 驱动程序写入证书时路径无效的问题。[docker/buildx#1831](https://github.com/docker/buildx/pull/1831)
- 修复了使用 SSH 访问远程 Bake 文件时的 Bake 失败问题。[docker/buildx#1711](https://github.com/docker/buildx/pull/1711), [docker/buildx#1734](https://github.com/docker/buildx/pull/1734)
- 修复了远程 Bake 上下文解析错误导致的 Bake 失败问题。[docker/buildx#1783](https://github.com/docker/buildx/pull/1783)
- 修复了 Bake 上下文中 `BAKE_CMD_CONTEXT` 和 `cwd://` 路径的路径解析。[docker/buildx#1840](https://github.com/docker/buildx/pull/1840)
- 修复了使用 `buildx imagetools create` 创建镜像时混合使用 OCI 和 Docker 媒体类型的问题。[docker/buildx#1797](https://github.com/docker/buildx/pull/1797)
- 修复了 `--iidfile` 和 `-q` 之间不匹配的镜像 ID。[docker/buildx#1844](https://github.com/docker/buildx/pull/1844)
- 修复了混合静态凭据和 IAM 配置文件时的 AWS 身份验证问题。[docker/buildx#1816](https://github.com/docker/buildx/pull/1816)

## 0.10.4

{{< release-date date="2023-03-06" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### Bug 修复和增强功能

- 添加了 `BUILDX_NO_DEFAULT_ATTESTATIONS` 作为 `--provenance false` 的替代方案。[docker/buildx#1645](https://github.com/docker/buildx/issues/1645)
- 为了性能，默认禁用脏 Git 检出检测。可以使用 `BUILDX_GIT_CHECK_DIRTY` 显式启用。[docker/buildx#1650](https://github.com/docker/buildx/issues/1650)
- 在发送到 BuildKit 之前，从 VCS 提示 URL 中剥离凭据。[docker/buildx#1664](https://github.com/docker/buildx/issues/1664)

## 0.10.3

{{< release-date date="2023-02-16" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### Bug 修复和增强功能

- 修复了收集 Git 来源信息时的可达提交和警告。[docker/buildx#1592](https://github.com/docker/buildx/issues/1592), [docker/buildx#1634](https://github.com/docker/buildx/issues/1634)
- 修复了一个导致 Docker 上下文未被验证的回归问题。[docker/buildx#1596](https://github.com/docker/buildx/issues/1596)
- 修复了 JSON Bake 定义中的函数解析问题。[docker/buildx#1605](https://github.com/docker/buildx/issues/1605)
- 修复了原始 HCL Bake 诊断信息被丢弃的情况。[docker/buildx#1607](https://github.com/docker/buildx/issues/1607)
- 修复了 Bake 和 Compose 文件无法正确设置标签的问题。[docker/buildx#1631](https://github.com/docker/buildx/issues/1631)

## 0.10.2

{{< release-date date="2023-01-30" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### Bug 修复和增强功能

- 修复了多节点构建中未考虑首选平台顺序的问题。[docker/buildx#1561](https://github.com/docker/buildx/issues/1561)
- 修复了处理 `SOURCE_DATE_EPOCH` 环境变量时可能出现的 panic。[docker/buildx#1564](https://github.com/docker/buildx/issues/1564)
- 修复了自 BuildKit v0.11 以来在某些镜像库上进行多节点清单合并时可能出现的推送错误。[docker/buildx#1566](https://github.com/docker/buildx/issues/1566)
- 改进了收集 Git 来源信息时的警告。[docker/buildx#1568](https://github.com/docker/buildx/issues/1568)

## 0.10.1

{{< release-date date="2023-01-27" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### Bug 修复和增强功能

- 修复了发送正确的原始 URL 作为 `vsc:source` 元数据的问题。[docker/buildx#1548](https://github.com/docker/buildx/issues/1548)
- 修复了数据竞态导致的可能 panic。[docker/buildx#1504](https://github.com/docker/buildx/issues/1504)
- 修复了 `rm --all-inactive` 的回归问题。[docker/buildx#1547](https://github.com/docker/buildx/issues/1547)
- 通过延迟加载数据，改进了 `imagetools inspect` 中的证明访问。[docker/buildx#1546](https://github.com/docker/buildx/issues/1546)
- 将能力请求正确标记为内部请求。[docker/buildx#1538](https://github.com/docker/buildx/issues/1538)
- 检测无效的证明配置。[docker/buildx#1545](https://github.com/docker/buildx/issues/1545)
- 更新了 containerd 补丁以修复可能影响 `imagetools` 命令的推送回归问题。[docker/buildx#1559](https://github.com/docker/buildx/issues/1559)

## 0.10.0

{{< release-date date="2023-01-10" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 新增

- `buildx build` 命令支持新的 `--attest` 标志，以及简写 `--sbom` 和 `--provenance`，用于为当前构建添加证明（Attestations）。[docker/buildx#1412](https://github.com/docker/buildx/issues/1412) [docker/buildx#1475](https://github.com/docker/buildx/issues/1475)
  - `--attest type=sbom` 或 `--sbom=true` 添加 [SBOM 证明](/manuals/build/metadata/attestations/sbom.md)。
  - `--attest type=provenance` 或 `--provenance=true` 添加 [SLSA 来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。
  - 创建 OCI 镜像时，镜像默认会包含一个最小的来源证明。
- 当使用支持来源证明的 BuildKit 进行构建时，Buildx 会自动共享构建上下文的版本控制信息，以便稍后在来源中显示以供调试。以前这仅在直接从 Git URL 构建时发生。要选择退出此行为，您可以设置 `BUILDX_GIT_INFO=0`。或者，您还可以通过设置 `BUILDX_GIT_LABELS=1` 自动定义带有 VCS 信息的标签。[docker/buildx#1462](https://github.com/docker/buildx/issues/1462), [docker/buildx#1297](https://github.com/docker/buildx), [docker/buildx#1341](https://github.com/docker/buildx/issues/1341), [docker/buildx#1468](https://github.com/docker/buildx), [docker/buildx#1477](https://github.com/docker/buildx/issues/1477)
- 带有 `--build-context` 的命名上下文现在支持 `oci-layout://` 协议，用于使用本地 OCI 布局目录的值初始化上下文。例如 `--build-context stagename=oci-layout://path/to/dir`。此功能需要 BuildKit v0.11.0+ 和 Dockerfile 1.5.0+。[docker/buildx#1456](https://github.com/docker/buildx/issues/1456)
- Bake 现在支持 [资源插值](bake/inheritance.md#reusing-single-attribute-from-targets)，您可以重用其他目标定义中的值。[docker/buildx#1434](https://github.com/docker/buildx/issues/1434)
- 如果在您的环境中定义了 `SOURCE_DATE_EPOCH` 环境变量，Buildx 现在将自动转发该变量。此功能旨在与 BuildKit v0.11.0+ 中更新的 [可复现构建](https://github.com/moby/buildkit/blob/master/docs/build-repro.md) 支持配合使用。[docker/buildx#1482](https://github.com/docker/buildx/issues/1482)
- Buildx 现在会记住构建器的最后一次活动，以便更好地组织构建器实例。[docker/buildx#1439](https://github.com/docker/buildx/issues/1439)
- Bake 定义现在支持对构建参数和标签的 [变量](bake/reference.md#variable) 和 [标签](bake/reference.md#targetlabels) 使用 null 值，以便使用 Dockerfile 中设置的默认值。[docker/buildx#1449](https://github.com/docker/buildx/issues/1449)
- [`buildx imagetools inspect` 命令](/reference/cli/docker/buildx/imagetools/inspect.md) 现在支持显示 SBOM 和来源数据。[docker/buildx#1444](https://github.com/docker/buildx/issues/1444), [docker/buildx#1498](https://github.com/docker/buildx/issues/1498)
- 提高了 `ls` 命令和检查流的性能。[docker/buildx#1430](https://github.com/docker/buildx/issues/1430), [docker/buildx#1454](https://github.com/docker/buildx/issues/1454), [docker/buildx#1455](https://github.com/docker/buildx/issues/1455), [docker/buildx#1345](https://github.com/docker/buildx/issues/1345)
- 使用 [Docker 驱动程序](/manuals/build/builders/drivers/docker.md) 添加额外主机现在支持 Docker 特有的 `host-gateway` 特殊值。[docker/buildx#1446](https://github.com/docker/buildx/issues/1446)
- [OCI 导出器](exporters/oci-docker.md) 现在支持 `tar=false` 选项，用于直接将 OCI 格式导出到目录中。[docker/buildx#1420](https://github.com/docker/buildx/issues/1420)

### 升级

- 将 Compose 规范更新至 1.6.0。[docker/buildx#1387](https://github.com/docker/buildx/issues/1387)

### Bug 修复和增强功能

- `--invoke` 现在可以从镜像元数据加载默认启动环境。[docker/buildx#1324](https://github.com/docker/buildx/issues/1324)
- 修复了容器驱动程序关于 UserNS 的行为。[docker/buildx#1368](https://github.com/docker/buildx/issues/1368)
- 修复了 Bake 中使用错误变量值类型时可能发生的 panic。[docker/buildx#1442](https://github.com/docker/buildx/issues/1442)
- 修复了 `imagetools inspect` 中可能发生的 panic。[docker/buildx#1441](https://github.com/docker/buildx/issues/1441) [docker/buildx#1406](https://github.com/docker/buildx/issues/1406)
- 修复了默认向 BuildKit 发送空 `--add-host` 值的问题。[docker/buildx#1457](https://github.com/docker/buildx/issues/1457)
- 修复了进度组处理进度前缀的问题。[docker/buildx#1305](https://github.com/docker/buildx/issues/1305)
- 修复了 Bake 中递归解析组的问题。[docker/buildx#1313](https://github.com/docker/buildx/issues/1313)
- 修复了多节点构建器清单上可能出现的缩进错误。[docker/buildx#1396](https://github.com/docker/buildx/issues/1396)
- 修复了由于缺失 OpenTelemetry 配置可能导致的 panic。[docker/buildx#1383](https://github.com/docker/buildx/issues/1383)
- 修复了 TTY 不可用时 `--progress=tty` 的行为。[docker/buildx#1371](https://github.com/docker/buildx/issues/1371)
- 修复了 `prune` 和 `du` 命令中的连接错误条件。[docker/buildx#1307](https://github.com/docker/buildx/issues/1307)

## 0.9.1

{{< release-date date="2022-08-18" >}}

### Bug 修复和增强功能

- `inspect` 命令现在会显示正在使用的 BuildKit 版本。[docker/buildx#1279](https://github.com/docker/buildx/issues/1279)
- 修复了构建包含不带 build 块的服务的 Compose 文件时的回归问题。[docker/buildx#1277](https://github.com/docker/buildx/issues/1277)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.9.1) 中的完整发行说明。

## 0.9.0

{{< release-date date="2022-08-17" >}}

### 新增

- 支持新的 [`remote` 驱动程序](/manuals/build/builders/drivers/remote.md)，您可以将其用于连接到任何已经在运行的 BuildKit 实例。[docker/buildx#1078](https://github.com/docker/buildx/issues/1078), [docker/buildx#1093](https://github.com/docker/buildx/issues/1093), [docker/buildx#1094](https://github.com/docker/buildx/issues/1094), [docker/buildx#1103](https://github.com/docker/buildx/issues/1103), [docker/buildx#1134](https://github.com/docker/buildx/issues/1134), [docker/buildx#1204](https://github.com/docker/buildx/issues/1204)
- 现在即使构建上下文来自外部 Git 或 HTTP URL，也可以从标准输入加载 Dockerfile。[docker/buildx#994](https://github.com/docker/buildx/issues/994)
- 构建命令现在支持新的构建上下文类型 `oci-layout://`，用于 [从本地 OCI 布局目录加载构建上下文](/reference/cli/docker/buildx/build.md#source-oci-layout)。请注意，此功能依赖于尚未发布的 BuildKit 功能，在 BuildKit v0.11 发布之前需要使用 `moby/buildkit:master` 的构建器实例。[docker/buildx#1173](https://github.com/docker/buildx/issues/1173)
- 您现在可以使用新的 `--print` 标志来运行执行构建的 BuildKit 前端所支持的助手函数，并打印其结果。您可以在 Dockerfile 中使用此功能，通过 `--print=outline` 显示当前构建支持的构建参数和密钥，并通过 `--print=targets` 列出所有可用的 Dockerfile 阶段。此功能是实验性的，旨在收集早期反馈，需要启用 `BUILDX_EXPERIMENTAL=1` 环境变量。我们计划在未来更新/扩展此功能，而不保持向后兼容性。[docker/buildx#1100](https://github.com/docker/buildx/issues/1100), [docker/buildx#1272](https://github.com/docker/buildx/issues/1272)
- 您现在可以使用新的 `--invoke` 标志从构建结果启动交互式容器，以进行交互式调试循环。您可以使用代码更改重新加载这些容器，或从特殊监控模式将其恢复到初始状态。此功能是实验性的，旨在收集早期反馈，需要启用 `BUILDX_EXPERIMENTAL=1` 环境变量。我们计划在未来更新/扩展此功能，而不启用向后兼容性。[docker/buildx#1168](https://github.com/docker/buildx/issues/1168), [docker/buildx#1257](https://github.com/docker/buildx), [docker/buildx#1259](https://github.com/docker/buildx/issues/1259)
- Buildx 现在能够识别环境变量 `BUILDKIT_COLORS` 和 `NO_COLOR`，以自定义/禁用交互式构建进度条的颜色。[docker/buildx#1230](https://github.com/docker/buildx/issues/1230), [docker/buildx#1226](https://github.com/docker/buildx/issues/1226)
- `buildx ls` 命令现在会显示每个构建器实例的当前 BuildKit 版本。[docker/buildx#998](https://github.com/docker/buildx/issues/998)
- 为了兼容性，`bake` 命令现在在构建 Compose 文件时会自动加载 `.env` 文件。[docker/buildx#1261](https://github.com/docker/buildx/issues/1261)
- Bake 现在支持带有 `cache_to` 定义的 Compose 文件。[docker/buildx#1155](https://github.com/docker/buildx/issues/1155)
- Bake 现在支持新的内置函数 `timestamp()` 以访问当前时间。[docker/buildx#1214](https://github.com/docker/buildx/issues/1214)
- Bake 现在支持 Compose 构建密钥（Secrets）定义。[docker/buildx#1069](https://github.com/docker/buildx/issues/1069)
- 现在通过 `x-bake` 在 Compose 文件中支持额外的构建上下文配置。[docker/buildx#1256](https://github.com/docker/buildx/issues/1256)
- 检查构建器现在会显示当前的驱动程序选项配置。[docker/buildx#1003](https://github.com/docker/buildx/issues/1003), [docker/buildx#1066](https://github.com/docker/buildx/issues/1066)

### 更新

- 将 Compose 规范更新至 1.4.0。[docker/buildx#1246](https://github.com/docker/buildx/issues/1246), [docker/buildx#1251](https://github.com/docker/buildx/issues/1251)

### Bug 修复和增强功能

- `buildx ls` 命令输出已更新，可以更好地访问来自不同构建器的错误。[docker/buildx#1109](https://github.com/docker/buildx/issues/1109)
- `buildx create` 命令现在会对构建器参数进行额外验证，以避免创建配置无效的构建器实例。[docker/buildx#1206](https://github.com/docker/buildx/issues/1206)
- `buildx imagetools create` 命令现在可以创建新的多平台镜像，即使源子镜像位于不同的仓库或镜像库中。[docker/buildx#1137](https://github.com/docker/buildx/issues/1137)
- 您现在可以设置默认的构建器配置，该配置在创建构建器实例时使用，而无需传递自定义的 `--config` 值。[docker/buildx#1111](https://github.com/docker/buildx/issues/1111)
- Docker 驱动程序现在可以检测 `dockerd` 实例是否支持最初禁用的 Buildkit 功能，如多平台镜像。[docker/buildx#1260](https://github.com/docker/buildx/issues/1260), [docker/buildx#1262](https://github.com/docker/buildx/issues/1262)
- 使用名称中带有 `.` 的目标的 Compose 文件现在被转换为使用 `_`，因此选择器键仍然可以在此类目标中使用。[docker/buildx#1011](https://github.com/docker/buildx/issues/1011)
- 包含了一个额外的验证，用于检查有效的驱动程序配置。[docker/buildx#1188](https://github.com/docker/buildx/issues/1188), [docker/buildx#1273](https://github.com/docker/buildx/issues/1273)
- `remove` 命令现在会显示已移除的构建器，并禁止移除上下文构建器。[docker/buildx#1128](https://github.com/docker/buildx/issues/1128)
- 允许在使用 Kubernetes 驱动程序时进行 Azure 身份验证。[docker/buildx#974](https://github.com/docker/buildx/issues/974)
- 为 kubernetes 驱动程序添加了容忍度（Tolerations）处理。[docker/buildx#1045](https://github.com/docker/buildx/issues/1045) [docker/buildx#1053](https://github.com/docker/buildx/issues/1053)
- 在 `kubernetes` 驱动程序中用 `securityContext` 替换了弃用的 seccomp 注解。[docker/buildx#1052](https://github.com/docker/buildx/issues/1052)
- 修复了处理平台为 nil 的清单时的 panic。[docker/buildx#1144](https://github.com/docker/buildx/issues/1144)
- 修复了在 `prune` 命令中使用时长过滤器的问题。[docker/buildx#1252](https://github.com/docker/buildx/issues/1252)
- 修复了在 Bake 定义中合并多个 JSON 文件的问题。[docker/buildx#1025](https://github.com/docker/buildx/issues/1025)
- 修复了从 Docker 上下文创建的隐式构建器配置无效或连接断开的问题。[docker/buildx#1129](https://github.com/docker/buildx/issues/1129)
- 修复了使用命名上下文时显示无输出警告的条件。[docker/buildx#968](https://github.com/docker/buildx/issues/968)
- 修复了构建器实例和 Docker 上下文同名时重复构建器的问题。[docker/buildx#1131](https://github.com/docker/buildx/issues/1131)
- 修复了打印不必要的 SSH 警告日志的问题。[docker/buildx#1085](https://github.com/docker/buildx/issues/1085)
- 修复了在 Bake JSON 定义中使用空变量块时可能出现的 panic。[docker/buildx#1080](https://github.com/docker/buildx/issues/1080)
- 修复了镜像工具命令无法正确处理 `--builder` 标志的问题。[docker/buildx#1067](https://github.com/docker/buildx/issues/1067)
- 修复了将自定义镜像与 rootless 选项结合使用的问题。[docker/buildx#1063](https://github.com/docker/buildx/issues/1063)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.9.0) 中的完整发行说明。

## 0.8.2

{{< release-date date="2022-04-04" >}}

### 更新

- 将 `buildx bake` 使用的 Compose 规范更新至 v1.2.1，以修复解析端口定义的问题。[docker/buildx#1033](https://github.com/docker/buildx/issues/1033)

### Bug 修复和增强功能

- 修复了处理来自 BuildKit v0.10 的进度流时可能发生的崩溃。[docker/buildx#1042](https://github.com/docker/buildx/issues/1042)
- 修复了在 `buildx bake` 中解析已被父组加载的组时的问题。[docker/buildx#1021](https://github.com/docker/buildx/issues/1021)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.8.2) 中的完整发行说明。

## 0.8.1

{{< release-date date="2022-03-21" >}}

### Bug 修复和增强功能

- 修复了处理构建上下文扫描错误时可能出现的 panic。[docker/buildx#1005](https://github.com/docker/buildx/issues/1005)
- 为了向后兼容，允许在 `buildx bake` 的 Compose 目标名称中使用 `.`。[docker/buildx#1018](https://github.com/docker/buildx/issues/1018)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.8.1) 中的完整发行说明。

## 0.8.0

{{< release-date date="2022-03-09" >}}

### 新增

- 构建命令现在接受 `--build-context` 标志，用于为您的构建 [定义额外的命名构建上下文](/reference/cli/docker/buildx/build/#build-context)。[docker/buildx#904](https://github.com/docker/buildx/issues/904)
- Bake 定义现在支持 [在目标之间定义依赖关系](bake/contexts.md)，并可以在另一个构建中使用一个目标的结果。[docker/buildx#928](https://github.com/docker/buildx/issues/928), [docker/buildx#965](https://github.com/docker/buildx/issues/965), [docker/buildx#963](https://github.com/docker/buildx/issues/963), [docker/buildx#962](https://github.com/docker/buildx/issues/962), [docker/buildx#981](https://github.com/docker/buildx/issues/981)
- `imagetools inspect` 现在接受 `--format` 标志，允许访问特定镜像的配置和构建信息。[docker/buildx#854](https://github.com/docker/buildx/issues/854), [docker/buildx#972](https://github.com/docker/buildx/issues/972)
- 新标志 `--no-cache-filter` 允许配置构建，使其仅对指定的 Dockerfile 阶段忽略缓存。[docker/buildx#860](https://github.com/docker/buildx/issues/860)
- 构建现在可以显示由构建前端设置的警告摘要。[docker/buildx#892](https://github.com/docker/buildx/issues/892)
- 新的构建参数 `BUILDKIT_INLINE_BUILDINFO_ATTRS` 允许选择将构建属性嵌入到生成的镜像中。[docker/buildx#908](https://github.com/docker/buildx/issues/908)
- 新标志 `--keep-buildkitd` 允许在移除构建器时保持 BuildKit 守护进程运行
  - [docker/buildx#852](https://github.com/docker/buildx/issues/852)

### Bug 修复和增强功能

- `--metadata-file` 输出现在支持嵌入式结构类型。[docker/buildx#946](https://github.com/docker/buildx/issues/946)
- `buildx rm` 现在接受新标志 `--all-inactive`，用于移除所有当前未运行的构建器。[docker/buildx#885](https://github.com/docker/buildx/issues/885)
- 为了向后兼容，现在从 Docker 配置文件中读取代理配置并随构建请求一起发送。[docker/buildx#959](https://github.com/docker/buildx/issues/959)
- 在 Compose 中支持主机网络。[docker/buildx#905](https://github.com/docker/buildx/issues/905), [docker/buildx#880](https://github.com/docker/buildx/issues/880)
- 现在可以使用 `-f -` 从标准输入读取 Bake 文件。[docker/buildx#864](https://github.com/docker/buildx/issues/864)
- `--iidfile` 现在总是写入镜像配置摘要，而与所使用的驱动程序无关（使用 `--metadata-file` 获取摘要）。[docker/buildx#980](https://github.com/docker/buildx/issues/980)
- Bake 中的目标名称现在限制为不能使用特殊字符。[docker/buildx#929](https://github.com/docker/buildx/issues/929)
- 使用 `docker` 驱动程序推送时，可以从元数据中读取镜像清单摘要。[docker/buildx#989](https://github.com/docker/buildx/issues/989)
- 修复了 Compose 文件中的环境文件处理问题。[docker/buildx#905](https://github.com/docker/buildx/issues/905)
- 在 `du` 命令中显示最后访问时间。[docker/buildx#867](https://github.com/docker/buildx/issues/867)
- 修复了当多个 Bake 目标运行相同的构建步骤时可能出现的双重输出日志。[docker/buildx#977](https://github.com/docker/buildx/issues/977)
- 修复了多节点构建器构建具有混合平台的多个目标时可能出现的错误。[docker/buildx#985](https://github.com/docker/buildx/issues/985)
- 修复了 Bake 中的一些嵌套继承情况。[docker/buildx#914](https://github.com/docker/buildx/issues/914)
- 修复了打印 Bake 文件默认组的问题。[docker/buildx#884](https://github.com/docker/buildx/issues/884)
- 修复了使用 rootless 容器时的 `UsernsMode`。[docker/buildx#887](https://github.com/docker/buildx/issues/887)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.8.0) 中的完整发行说明。

## 0.7.1

{{< release-date date="2021-08-25" >}}

### 修复

- 修复了 `.dockerignore` 中排除规则匹配的问题。[docker/buildx#858](https://github.com/docker/buildx/issues/858)
- 修复了当前组的 `bake --print` JSON 输出。[docker/buildx#857](https://github.com/docker/buildx/issues/857)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.7.1) 中的完整发行说明。

## 0.7.0

{{< release-date date="2021-11-10" >}}

### 新功能

- 来自 BuildKit 配置的 TLS 证书现在会通过 `docker-container` 和 `kubernetes` 驱动程序传输到构建容器。[docker/buildx#787](https://github.com/docker/buildx/issues/787)
- 构建支持 `--ulimit` 标志以实现功能对等。[docker/buildx#800](https://github.com/docker/buildx/issues/800)
- 构建支持 `--shm-size` 标志以实现功能对等。[docker/buildx#790](https://github.com/docker/buildx/issues/790)
- 构建支持 `--quiet` 以实现功能对等。[docker/buildx#740](https://github.com/docker/buildx/issues/740)
- 构建支持 `--cgroup-parent` 标志以实现功能对等。[docker/buildx#814](https://github.com/docker/buildx/issues/814)
- Bake 支持内置变量 `BAKE_LOCAL_PLATFORM`。[docker/buildx#748](https://github.com/docker/buildx/issues/748)
- Bake 支持 Compose 文件中的 `x-bake` 扩展字段。[docker/buildx#721](https://github.com/docker/buildx/issues/721)
- `kubernetes` 驱动程序现在支持冒号分隔的 `KUBECONFIG`。[docker/buildx#761](https://github.com/docker/buildx/issues/761)
- `kubernetes` 驱动程序现在支持使用 `--config` 设置 Buildkit 配置文件。[docker/buildx#682](https://github.com/docker/buildx/issues/682)
- `kubernetes` 驱动程序现在支持通过 driver-opt 安装 QEMU 模拟器。[docker/buildx#682](https://github.com/docker/buildx/issues/682)

### 增强功能

- 允许从客户端为多节点推送使用自定义镜像库配置。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- 允许为 `buildx imagetools` 命令使用自定义镜像库配置。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- 允许在通过 `buildx create --bootstrap` 创建后启动构建器。[docker/buildx#692](https://github.com/docker/buildx/issues/692)
- 允许为多节点推送使用 `registry:insecure` 输出选项。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- BuildKit 配置和 TLS 文件现在保存在 Buildx 状态目录中，如果需要重新创建 BuildKit 实例则可以重复使用。[docker/buildx#824](https://github.com/docker/buildx/issues/824)
- 确保不同的项目为增量上下文传输使用单独的目标目录，以获得更好的性能。[docker/buildx#817](https://github.com/docker/buildx/issues/817)
- 构建容器现在默认放置在单独的 cgroup 上。[docker/buildx#782](https://github.com/docker/buildx/issues/782)
- Bake 现在使用 `--print` 打印默认组。[docker/buildx#720](https://github.com/docker/buildx/issues/720)
- `docker` 驱动程序现在通过 HTTP 拨号构建会话，以获得更好的性能。[docker/buildx#804](https://github.com/docker/buildx/issues/804)

### 修复

- 修复了 `--iidfile` 与多节点推送配合使用的问题。[docker/buildx#826](https://github.com/docker/buildx/issues/826)
- 在 Bake 中使用 `--push` 不会清除文件中的其他镜像导出选项。[docker/buildx#773](https://github.com/docker/buildx/issues/773)
- 修复了使用 `https` 协议时 `buildx bake` 的 Git URL 检测问题。[docker/buildx#822](https://github.com/docker/buildx/issues/822)
- 修复了在多节点构建中推送带有多个名称的镜像的问题。[docker/buildx#815](https://github.com/docker/buildx/issues/815)
- 避免对不使用 `--builder` 标志的命令显示该标志。[docker/buildx#818](https://github.com/docker/buildx/issues/818)
- 不支持的构建标志现在会显示警告。[docker/buildx#810](https://github.com/docker/buildx/issues/810)
- 修复了在某些 OpenTelemetry 追踪中报告错误详情的问题。[docker/buildx#812](https://github.com/docker/buildx/issues/812)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.7.0) 中的完整发行说明。

## 0.6.3

{{< release-date date="2021-08-30" >}}

### 修复

- 修复了 Windows 客户端的 BuildKit 状态卷位置。[docker/buildx#751](https://github.com/docker/buildx/issues/751)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.3) 中的完整发行说明。

## 0.6.2

{{< release-date date="2021-08-21" >}}

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.2) 中的完整发行说明。

### 修复

- 修复了在某些 SSH 配置中显示的连接错误。[docker/buildx#741](https://github.com/docker/buildx/issues/741)

## 0.6.1

{{< release-date date="2021-07-30" >}}

### 增强功能

- 设置 `ConfigFile` 以使用 Bake 解析 Compose 文件。[docker/buildx#704](https://github.com/docker/buildx/issues/704)

### 修复

- 重复的进度环境变量。[docker/buildx#693](https://github.com/docker/buildx/issues/693)
- 应忽略 nil 客户端。[docker/buildx#686](https://github.com/docker/buildx/issues/686)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.1) 中的完整发行说明。

## 0.6.0

{{< release-date date="2021-07-16" >}}

### 新功能

- 支持 OpenTelemetry 追踪，并将 Buildx 客户端追踪转发至 BuildKit。[docker/buildx#635](https://github.com/docker/buildx/issues/635)
- 带有 `--cache-to type=gha` 和 `--cache-from type=gha` 的实验性 GitHub Actions 远程缓存后端。[docker/buildx#535](https://github.com/docker/buildx/issues/535)
- 为构建和 Bake 命令添加了新的 `--metadata-file` 标志，允许以 JSON 格式保存构建结果元数据。[docker/buildx#605](https://github.com/docker/buildx/issues/605)
- 这是第一个支持 Windows ARM64 的版本。[docker/buildx#654](https://github.com/docker/buildx/issues/654)
- 这是第一个支持 Linux Risc-V 的版本。[docker/buildx#652](https://github.com/docker/buildx/issues/652)
- Bake 现在支持使用本地文件或其他远程源作为上下文从远程定义进行构建。[docker/buildx#671](https://github.com/docker/buildx/issues/671)
- Bake 现在允许变量相互引用，并在变量中使用用户函数，反之亦然。
  [docker/buildx#575](https://github.com/docker/buildx/issues/575),
  [docker/buildx#539](https://github.com/docker/buildx/issues/539),
  [docker/buildx#532](https://github.com/docker/buildx/issues/532)
- Bake 允许在全局范围内定义属性。[docker/buildx#541](https://github.com/docker/buildx/issues/541)
- Bake 允许跨多个文件使用变量。[docker/buildx#538](https://github.com/docker/buildx/issues/538)
- 进度打印器新增了静默（Quiet）模式。[docker/buildx#558](https://github.com/docker/buildx/issues/558)
- `kubernetes` 驱动程序现在支持定义资源/限制。[docker/buildx#618](https://github.com/docker/buildx/issues/618)
- 现在可以通过 [buildx-bin](https://hub.docker.com/r/docker/buildx-bin) Docker 镜像访问 Buildx 二进制文件。[docker/buildx#656](https://github.com/docker/buildx/issues/656)

### 增强功能

- `docker-container` 驱动程序现在将 BuildKit 状态保存在卷中。支持在保持状态的情况下进行更新。[docker/buildx#672](https://github.com/docker/buildx/issues/672)
- Compose 解析器现在基于新的 [compose-go 解析器](https://github.com/compose-spec/compose-go)，修复了对一些较新语法的支持。[docker/buildx#669](https://github.com/docker/buildx/issues/669)
- 构建基于 ssh 的 git URL 时，现在会自动转发 SSH 套接字。[docker/buildx#581](https://github.com/docker/buildx/issues/581)
- 重写了 Bake HCL 解析器。[docker/buildx#645](https://github.com/docker/buildx/issues/645)
- 使用更多函数扩展了 HCL 支持。[docker/buildx#491](https://github.com/docker/buildx/issues/491) [docker/buildx#503](https://github.com/docker/buildx/issues/503)
- 允许从环境变量中使用密钥。[docker/buildx#488](https://github.com/docker/buildx/issues/488)
- 多平台构建且带 load 配置（不受支持）现在会快速失败。[docker/buildx#582](https://github.com/docker/buildx/issues/582)
- 存储 Kubernetes 配置文件以使 buildx 构建器可切换。[docker/buildx#497](https://github.com/docker/buildx/issues/497)
- Kubernetes 现在在检查时将所有 Pod 列为节点。[docker/buildx#477](https://github.com/docker/buildx/issues/477)
- 默认 Rootless 镜像已设置为 `moby/buildkit:buildx-stable-1-rootless`。[docker/buildx#480](https://github.com/docker/buildx/issues/480)

### 修复

- `imagetools create` 命令现在可以正确地将 JSON 描述符与旧描述符合并。[docker/buildx#592](https://github.com/docker/buildx/issues/592)
- 修复了使用 `--network=none` 构建时不需要额外安全授权的问题。[docker/buildx#531](https://github.com/docker/buildx/issues/531)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.0) 中的完整发行说明。

## 0.5.1

{{< release-date date="2020-12-15" >}}

### 修复

- 修复了在 `kubernetes` 驱动程序之外对 `buildx create` 设置 `--platform` 的回归问题。[docker/buildx#475](https://github.com/docker/buildx/issues/475)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.5.1) 中的完整发行说明。

## 0.5.0

{{< release-date date="2020-12-15" >}}

### 新功能

- `docker` 驱动程序现在支持 `--push` 标志。[docker/buildx#442](https://github.com/docker/buildx/issues/442)
- Bake 支持内联 Dockerfile。[docker/buildx#398](https://github.com/docker/buildx/issues/398)
- Bake 支持从远程 URL 和 Git 仓库构建。[docker/buildx#398](https://github.com/docker/buildx/issues/398)
- `BUILDX_CONFIG` 环境变量允许用户使 buildx 状态与 Docker 配置分离。[docker/buildx#385](https://github.com/docker/buildx/issues/385)
- `BUILDKIT_MULTI_PLATFORM` 构建参数允许强制构建多平台返回对象，即使仅指定了一个 `--platform`。[docker/buildx#467](https://github.com/docker/buildx/issues/467)

### 增强功能

- 允许 `--append` 与 `kubernetes` 驱动程序配合使用。[docker/buildx#370](https://github.com/docker/buildx/issues/370)
- 使用 `--debug` 时，构建错误会显示源文件中的错误位置和系统堆栈跟踪。[docker/buildx#389](https://github.com/docker/buildx/issues/389)
- Bake 使用源定义格式化 HCL 错误。[docker/buildx#391](https://github.com/docker/buildx/issues/391)
- Bake 允许数组中出现将被丢弃的空字符串值。[docker/buildx#428](https://github.com/docker/buildx/issues/428)
- 您现在可以将 Kubernetes 集群配置与 `kubernetes` 驱动程序配合使用。[docker/buildx#368](https://github.com/docker/buildx/issues/368) [docker/buildx#460](https://github.com/docker/buildx/issues/460)
- 尽可能创建临时令牌用于拉取镜像，而不是共享凭据。[docker/buildx#469](https://github.com/docker/buildx/issues/469)
- 确保拉取 BuildKit 容器镜像时传递了凭据。[docker/buildx#441](https://github.com/docker/buildx/issues/441) [docker/buildx#433](https://github.com/docker/buildx/issues/433)
- 在 `docker-container` 驱动程序中禁用了用户命名空间重映射。[docker/buildx#462](https://github.com/docker/buildx/issues/462)
- 允许使用 `--builder` 标志切换到默认实例。[docker/buildx#425](https://github.com/docker/buildx/issues/425)
- 避免对空的 `BUILDX_NO_DEFAULT_LOAD` 配置值发出警告。[docker/buildx#390](https://github.com/docker/buildx/issues/390)
- 用警告替换由 `quiet` 选项生成的错误。[docker/buildx#403](https://github.com/docker/buildx/issues/403)
- CI 已切换到 GitHub Actions。
  [docker/buildx#451](https://github.com/docker/buildx/issues/451),
  [docker/buildx#463](https://github.com/docker/buildx/issues/463),
  [docker/buildx#466](https://github.com/docker/buildx/issues/466),
  [docker/buildx#468](https://github.com/docker/buildx/issues/468),
  [docker/buildx#471](https://github.com/docker/buildx/issues/471)

### 修复

- 为了向后兼容，处理小写 Dockerfile 名称作为回退。[docker/buildx#444](https://github.com/docker/buildx/issues/444)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.5.0) 中的完整发行说明。

## 0.4.2

{{< release-date date="2020-08-22" >}}

### 新功能

- 支持 `cacheonly` 导出器。[docker/buildx#337](https://github.com/docker/buildx/issues/337)

### 增强功能

- 更新了 `go-cty` 以引入更多 `stdlib` 函数。[docker/buildx#277](https://github.com/docker/buildx/issues/277)
- 改进了加载时的错误检查。[docker/buildx#281](https://github.com/docker/buildx/issues/281)

### 修复

- 修复了使用 HCL 解析 JSON 配置的问题。[docker/buildx#280](https://github.com/docker/buildx/issues/280)
- 确保从根选项接入 `--builder`。[docker/buildx#321](https://github.com/docker/buildx/issues/321)
- 移除了多平台 iidfile 的警告。[docker/buildx#351](https://github.com/docker/buildx/issues/351)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.4.2) 中的完整发行说明。

## 0.4.1

{{< release-date date="2020-05-01" >}}

### 修复

- 修复了标志解析的回归问题。[docker/buildx#268](https://github.com/docker/buildx/issues/268)
- 修复了在 HCL 目标中使用 pull 和 no-cache 键的问题。[docker/buildx#268](https://github.com/docker/buildx/issues/268)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.4.1) 中的完整发行说明。

## 0.4.0

{{< release-date date="2020-04-30" >}}

### 新功能

- 添加了 `kubernetes` 驱动程序。[docker/buildx#167](https://github.com/docker/buildx/issues/167)
- 新增全局 `--builder` 标志，用于在单个命令中覆盖构建器实例。[docker/buildx#246](https://github.com/docker/buildx/issues/246)
- 新增 `prune` 和 `du` 命令用于管理本地构建器缓存。[docker/buildx#249](https://github.com/docker/buildx/issues/249)
- 您现在可以为 HCL 目标设置新的 `pull` 和 `no-cache` 选项。[docker/buildx#165](https://github.com/docker/buildx/issues/165)

### 增强功能

- 将 Bake 升级到 HCL2，支持变量和函数。[docker/buildx#192](https://github.com/docker/buildx/issues/192)
- Bake 现在支持 `--load` 和 `--push`。[docker/buildx#164](https://github.com/docker/buildx/issues/164)
- Bake 现在支持多个目标的通配符覆盖。[docker/buildx#164](https://github.com/docker/buildx/issues/164)
- 容器驱动程序允许通过 `driver-opt` 设置环境变量。[docker/buildx#170](https://github.com/docker/buildx/issues/170)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.4.0) 中的完整发行说明。

## 0.3.1

{{< release-date date="2019-09-27" >}}

### 增强功能

- 处理复制 unix 套接字而不是报错。[docker/buildx#155](https://github.com/docker/buildx/issues/155) [moby/buildkit#1144](https://github.com/moby/buildkit/issues/1144)

### 修复

- 运行带有多个 Compose 文件的 Bake 现在可以正确合并目标。[docker/buildx#134](https://github.com/docker/buildx/issues/134)
- 修复了从标准输入构建 Dockerfile (`build -f -`) 时的 Bug。[docker/buildx#153](https://github.com/docker/buildx/issues/153)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.3.1) 中的完整发行说明。

## 0.3.0

{{< release-date date="2019-08-02" >}}

### 新功能

- 自定义 `buildkitd` 守护进程标志。[docker/buildx#102](https://github.com/docker/buildx/issues/102)
- `create` 上的驱动程序特定选项。[docker/buildx#122](https://github.com/docker/buildx/issues/122)

### 增强功能

- 在 Compose 文件中使用环境变量。[docker/buildx#117](https://github.com/docker/buildx/issues/117)
- Bake 现在遵循 `--no-cache` 和 `--pull`。[docker/buildx#118](https://github.com/docker/buildx/issues/118)
- 自定义 BuildKit 配置文件。[docker/buildx#121](https://github.com/docker/buildx/issues/121)
- 通过 `build --allow` 支持授权。[docker/buildx#104](https://github.com/docker/buildx/issues/104)

### 修复

- 修复了 `--build-arg foo` 无法从环境中读取 `foo` 的 Bug。[docker/buildx#116](https://github.com/docker/buildx/issues/116)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.3.0) 中的完整发行说明。

## 0.2.2

{{< release-date date="2019-05-30" >}}

### 增强功能

- 更改了 Compose 文件处理，要求有效的服务规范。[docker/buildx#87](https://github.com/docker/buildx/issues/87)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.2.2) 中的完整发行说明。

## 0.2.1

{{< release-date date="2019-05-25" >}}

### 新功能

- 添加了 `BUILDKIT_PROGRESS` 环境变量。[docker/buildx#69](https://github.com/docker/buildx/issues/69)
- 添加了 `local` 平台。[docker/buildx#70](https://github.com/docker/buildx/issues/70)

### 增强功能

- 如果配置中定义了 arm 变体，则予以保留。[docker/buildx#68](https://github.com/docker/buildx/issues/68)
- 使 dockerfile 相对于上下文。[docker/buildx#83](https://github.com/docker/buildx/issues/83)

### 修复

- 修复了从 compose 文件解析目标的问题。[docker/buildx#53](https://github.com/docker/buildx/issues/53)

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.2.1) 中的完整发行说明。

## 0.2.0

{{< release-date date="2019-04-25" >}}

### 新功能

- 首次发布

有关更多详情，请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.2.0) 中的完整发行说明。
