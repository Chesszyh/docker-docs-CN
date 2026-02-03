---
title: 构建发布说明
weight: 120
description: 了解最新 Buildx 版本的特性、错误修复和重大变更
keywords: build, buildx, buildkit, release notes, 发布说明
tags: [Release notes]
toc_max: 2
---

本页包含关于 [Docker Buildx](https://github.com/docker/buildx) 的新特性、改进和错误修复的信息。

## 0.24.0

{{< release-date date="2025-05-21" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.24.0) 查看。

### 增强功能

- 在 Bake 的 `variable` 块中增加了新的 `type` 属性，允许对变量进行显式类型定义。[docker/buildx#3167](https://github.com/docker/buildx/pull/3167), [docker/buildx#3189](https://github.com/docker/buildx/pull/3189), [docker/buildx#3198](https://github.com/docker/buildx/pull/3198)
- 在 `history export` 命令中增加了新的 `--finalize` 标志，以便在导出前完成构建追踪。[docker/buildx#3152](https://github.com/docker/buildx/pull/3152)
- Compose 兼容性已更新至 v2.6.3。[docker/buildx#3191](https://github.com/docker/buildx/pull/3191), [docker/buildx#3171](https://github.com/docker/buildx/pull/3171)

### 错误修复

- 修复了某些构建在完成后可能留下临时文件的问题。[docker/buildx#3133](https://github.com/docker/buildx/pull/3133)
- 修复了开启 containerd-snapshotter 后，使用 Docker 构建时返回的镜像 ID 错误的问题。[docker/buildx#3136](https://github.com/docker/buildx/pull/3136)
- 修复了在 Bake 中使用空的 `call` 定义时可能发生的 panic。[docker/buildx#3168](https://github.com/docker/buildx/pull/3168)
- 修复了 Windows 上使用 Bake 时可能出现的 Dockerfile 路径格式错误。[docker/buildx#3141](https://github.com/docker/buildx/pull/3141)
- 修复了 `ls` 命令的 JSON 输出中当前构建器不可用的问题。[docker/buildx#3179](https://github.com/docker/buildx/pull/3179)
- 修复了 OTEL 上下文未传播到 Docker 守护进程的问题。[docker/buildx#3146](https://github.com/docker/buildx/pull/3146)

## 0.23.0

{{< release-date date="2025-04-15" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.23.0) 查看。

### 新特性

- 新增 `buildx history export` 命令，允许将构建记录导出为可导入 [Docker Desktop](/desktop/) 的包。[docker/buildx#3073](https://github.com/docker/buildx/pull/3073)

### 增强功能

- 新增 `--local` 和 `--filter` 标志，允许在 `buildx history ls` 中过滤历史记录。[docker/buildx#3091](https://github.com/docker/buildx/pull/3091)
- Compose 兼容性已更新至 v2.6.0。[docker/buildx#3080](https://github.com/docker/buildx/pull/3080), [docker/buildx#3105](https://github.com/docker/buildx/pull/3105)
- 在独立（standalone）模式下支持 CLI 环境变量。[docker/buildx#3087](https://github.com/docker/buildx/pull/3087)

### 错误修复

- 修复了 Bake 的 `--print` 输出会产生带有未转义变量的输出，可能导致后续构建错误的问题。[docker/buildx#3097](https://github.com/docker/buildx/pull/3097)
- 修复了 `additional_contexts` 字段在指向另一个服务时无法正常工作的问题。[docker/buildx#3090](https://github.com/docker/buildx/pull/3090)
- 修复了空的 validation 块导致 Bake HCL 解析器崩溃的问题。[docker/buildx#3101](https://github.com/docker/buildx/pull/3101)

## 0.22.0

{{< release-date date="2025-03-18" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.22.0) 查看。

### 新特性

- 新增 `buildx history import` 命令，允许您将构建记录导入 Docker Desktop，以便在 [Build UI](/desktop/use-desktop/builds/) 中进行进一步调试。此命令要求已安装 [Docker Desktop](/desktop/)。[docker/buildx#3039](https://github.com/docker/buildx/pull/3039)

### 增强功能

- 历史记录现在可以在 `history inspect`、`history logs` 和 `history open` 命令中通过相对于最新记录的偏移量打开（例如 `^1`）。[docker/buildx#3049](https://github.com/docker/buildx/pull/3049), [docker/buildx#3055](https://github.com/docker/buildx/pull/3055)
- Bake 现在在覆盖设置中使用 `--set` 时支持 `+=` 运算符进行追加。[docker/buildx#3031](https://github.com/docker/buildx/pull/3031)
- Docker 容器驱动程序在可用时会将 GPU 设备添加到容器中。[docker/buildx#3063](https://github.com/docker/buildx/pull/3063)
- 在 Bake 中使用覆盖设置时现在支持设置注解 (Annotations)。[docker/buildx#2997](https://github.com/docker/buildx/pull/2997)
- 发布版本中现在包含 NetBSD 二进制文件。[docker/buildx#2901](https://github.com/docker/buildx/pull/2901)
- 如果节点启动失败，`inspect` 和 `create` 命令现在会返回错误。[docker/buildx#3062](https://github.com/docker/buildx/pull/3062)

### 错误修复

- 修复了开启 containerd 镜像存储后，使用 Docker 驱动程序时的重复推送问题。[docker/buildx#3023](https://github.com/docker/buildx/pull/3023)
- 修复了 `imagetools create` 命令会推送多个标签的问题。现在只有最终清单会通过标签推送。[docker/buildx#3024](https://github.com/docker/buildx/pull/3024)

## 0.21.0

{{< release-date date="2025-02-19" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.21.0) 查看。

### 新特性

- 新增 `buildx history trace` 命令，允许您在基于 Jaeger UI 的查看器中检查构建的追踪数据，并对比不同的追踪记录。[docker/buildx#2904](https://github.com/docker/buildx/pull/2904)

### 增强功能

- 历史检查命令 `buildx history inspect` 现在支持使用 `--format` 标志进行自定义格式化，并支持 JSON 格式以实现机器可读的输出。[docker/buildx#2964](https://github.com/docker/buildx/pull/2964) 
- 在构建 (build) 和 Bake 中支持 CDI 设备授权。[docker/buildx#2994](https://github.com/docker/buildx/pull/2994)
- 支持的 CDI 设备现在会显示在构建器检查信息中。[docker/buildx#2983](https://github.com/docker/buildx/pull/2983)
- 使用 [GitHub Cache 后端 `type=gha`](cache/backends/gha.md) 时，现在会从环境中读取第 2 版或 API 的 URL 并发送给 BuildKit。第 2 版后端要求使用 BuildKit v0.20.0 或更高版本。[docker/buildx#2983](https://github.com/docker/buildx/pull/2983), [docker/buildx#3001](https://github.com/docker/buildx/pull/3001)

### 错误修复

- 避免在使用 `--progress=rawjson` 时出现不必要的警告和提示。[docker/buildx#2957](https://github.com/docker/buildx/pull/2957)
- 修复了调试 shell 在使用 `--on=error` 时有时无法正常工作的回归问题。[docker/buildx#2958](https://github.com/docker/buildx/pull/2958)
- 修复了在 Bake 定义中使用未知变量时可能发生的 panic 错误。[docker/buildx#2960](https://github.com/docker/buildx/pull/2960)
- 修复了 `buildx ls` 命令在 JSON 格式化时的无效重复输出。[docker/buildx#2970](https://github.com/docker/buildx/pull/2970)
- 修复了 Bake 处理包含多个注册表引用的 CSV 字符串缓存导入的问题。[docker/buildx#2944](https://github.com/docker/buildx/pull/2944)
- 修复了拉取 BuildKit 镜像时的错误可能被忽略的问题。[docker/buildx#2988](https://github.com/docker/buildx/pull/2988)
- 修复了在调试 shell 上暂停进度时的竞态条件。[docker/buildx#3003](https://github.com/docker/buildx/pull/3003)

## 0.20.1

{{< release-date date="2025-01-23" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.20.1) 查看。

### 错误修复

- 修复了因缺少某些证明 (attestations) 属性导致的 `bake --print` 输出问题。[docker/buildx#2937](https://github.com/docker/buildx/pull/2937)
- 修复了允许在缓存导入和导出值中使用逗号分隔的镜像引用字符串的问题。[docker/buildx#2944](https://github.com/docker/buildx/pull/2944)

## 0.20.0

{{< release-date date="2025-01-20" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.20.0) 查看。

> [!NOTE]
>
> 此版本的 buildx 默认开启了针对 `buildx bake` 命令的文件系统授权检查。如果您的 Bake 定义需要读取或写入当前工作目录以外的文件，您需要使用 `--allow fs=<路径|*>` 来授权访问这些路径。在终端中，您也可以通过弹出的提示交互式地批准这些路径。此外，您可以通过设置 `BUILDX_BAKE_ENTITLEMENTS_FS=0` 来禁用这些检查。此验证在 Buildx v0.19.0+ 版本中曾以警告形式出现，但从当前版本开始将产生错误。更多信息请参阅 [参考文档](/reference/cli/docker/buildx/bake.md#allow)。

### 新特性

- 增加了新的 `buildx history` 命令，允许对已完成和运行中的构建记录进行操作。您可以使用这些命令列出、检查、移除您的构建，回放已完成构建的日志，并在 Docker Desktop 构建 UI 中快速打开构建进行进一步调试。这是该命令的早期版本，我们预计在未来的版本中增加更多特性。[#2891](https://github.com/docker/buildx/pull/2891), [#2925](https://github.com/docker/buildx/pull/2925)

### 增强功能

- Bake：定义现在支持对以前需要 CSV 字符串作为输入的字段使用新的对象记法（`attest`、`output`、`cache-from`、`cache-to`、`secret`、`ssh`）。[docker/buildx#2758](https://github.com/docker/buildx/pull/2758), [docker/buildx#2848](https://github.com/docker/buildx/pull/2848), [docker/buildx#2871](https://github.com/docker/buildx/pull/2871), [docker/buildx#2814](https://github.com/docker/buildx/pull/2814)
- Bake：文件系统授权现在默认报错。要禁用此行为，可以设置 `BUILDX_BAKE_ENTITLEMENTS_FS=0`。[docker/buildx#2875](https://github.com/docker/buildx/pull/2875)
- Bake：从远程文件推断 Git 身份验证令牌到构建请求。[docker/buildx#2905](https://github.com/docker/buildx/pull/2905)
- Bake：增加了对使用 `--list` 标志列出目标和变量的支持。[docker/buildx#2900](https://github.com/docker/buildx/pull/2900), [docker/buildx#2907](https://github.com/docker/buildx/pull/2907)
- Bake：更新了默认定义文件的查找顺序，以便更晚地加载带有 "override" 后缀的文件。[docker/buildx#2886](https://github.com/docker/buildx/pull/2886)

### 错误修复

- Bake：修复了默认 SSH 套接字的文件系统授权检查。[docker/buildx#2898](https://github.com/docker/buildx/pull/2898)
- Bake：修复了组默认目标中缺失的默认目标问题。[docker/buildx#2863](https://github.com/docker/buildx/pull/2863)
- Bake：修复了与目标平台匹配的命名上下文问题。[docker/buildx#2877](https://github.com/docker/buildx/pull/2877)
- 修复了 quiet 进度模式缺失文档的问题。[docker/buildx#2899](https://github.com/docker/buildx/pull/2899)
- 修复了加载层时丢失最后进度的问题。[docker/buildx#2876](https://github.com/docker/buildx/pull/2876)
- 创建构建器前验证 BuildKit 配置。[docker/buildx#2864](https://github.com/docker/buildx/pull/2864)

### 封装

- Compose 兼容性已更新至 v2.4.7。[docker/buildx#2893](https://github.com/docker/buildx/pull/2893), [docker/buildx#2857](https://github.com/docker/buildx/pull/2857), [docker/buildx#2829](https://github.com/docker/buildx/pull/2829)

## 0.19.1

{{< release-date date="2024-11-27" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.19.1) 查看。

### 错误修复

- 撤销了 v0.19.0 中为 Bake 定义中以前需要 CSV 字符串的字段添加新对象记法的更改。撤销此项增强是因为在某些边界情况下发现了向后不兼容的问题。此特性已推迟到 v0.20.0 版本。[docker/buildx#2824](https://github.com/docker/buildx/pull/2824)

## 0.19.0

{{< release-date date="2024-11-27" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.19.0) 查看。

### 新特性

- 现在，当您的构建需要读取或写入当前工作目录以外的文件时，Bake 会要求您开启文件系统授权。[docker/buildx#2796](https://github.com/docker/buildx/pull/2796), [docker/buildx#2812](https://github.com/docker/buildx/pull/2812)。

  要开启文件系统授权，请为 `docker buildx bake` 命令使用 `--allow fs.read=<路径>` 标志。

  目前在使用本地 Bake 定义时此特性仅报告警告，但将从 v0.20 版本开始产生错误。要在当前版本中启用报错，您可以设置 `BUILDX_BAKE_ENTITLEMENTS_FS=1`。

### 增强功能

- Bake 定义现在支持对以前需要 CSV 字符串作为输入的字段使用新的对象记法。[docker/buildx#2758](https://github.com/docker/buildx/pull/2758)

  > [!NOTE]
  > 此项增强已在 [v0.19.1](#0191) 中因 Bug 被撤销。

- Bake 定义现在允许为变量定义验证条件。[docker/buildx#2794](https://github.com/docker/buildx/pull/2794)
- 元数据文件中的值现在可以包含 JSON 数组值。[docker/buildx#2777](https://github.com/docker/buildx/pull/2777)
- 优化了使用错误的标签格式时的错误消息。[docker/buildx#2778](https://github.com/docker/buildx/pull/2778)
- 发布版本中现在包含 FreeBSD 和 OpenBSD 产物。[docker/buildx#2774](https://github.com/docker/buildx/pull/2774), [docker/buildx#2775](https://github.com/docker/buildx/pull/2775), [docker/buildx#2781](https://github.com/docker/buildx/pull/2781)

### 错误修复

- 修复了打印包含空 Compose 网络的 Bake 定义时的问题。[docker/buildx#2790](https://github.com/docker/buildx/pull/2790)。

### 封装

- Compose 支持已更新至 v2.4.4。[docker/buildx#2806](https://github.com/docker/buildx/pull/2806) [docker/buildx#2780](https://github.com/docker/buildx/pull/2780)。

## 0.18.0

{{< release-date date="2024-10-31" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.18.0) 查看。

### 新特性

- `docker buildx inspect` 命令现在显示使用 TOML 文件设置的 BuildKit 守护进程配置选项。[docker/buildx#2684](https://github.com/docker/buildx/pull/2684)
- 通过压缩平台列表，`docker buildx ls` 命令的输出现在默认更加紧凑。可以使用新的 `--no-trunc` 选项查看完整列表。[docker/buildx#2138](https://github.com/docker/buildx/pull/2138), [docker/buildx#2717](https://github.com/docker/buildx/pull/2717)
- 对于 BuildKit v0.17.0+ 的构建器，`docker buildx prune` 命令现在支持新的 `--max-used-space` 和 `--min-free-space` 过滤器。[docker/buildx#2766](https://github.com/docker/buildx/pull/2766)

### 增强功能

- 支持使用 [`BUILDX_CPU_PROFILE`](/manuals/build/building/variables.md#buildx_cpu_profile) 和 [`BUILDX_MEM_PROFILE`](/manuals/build/building/variables.md#buildx_mem_profile) 环境变量通过 `pprof` 捕获 CPU 和内存分析数据。[docker/buildx#2746](https://github.com/docker/buildx/pull/2746)
- 增加了从标准输入接收的 Dockerfile 的最大尺寸限制。[docker/buildx#2716](https://github.com/docker/buildx/pull/2716), [docker/buildx#2719](https://github.com/docker/buildx/pull/2719)
- 减少了内存分配。[docker/buildx#2724](https://github.com/docker/buildx/pull/2724), [docker/buildx#2713](https://github.com/docker/buildx/pull/2713)
- `docker buildx bake` 的 `--list-targets` 和 `--list-variables` 标志现在不再要求初始化构建器。[docker/buildx#2763](https://github.com/docker/buildx/pull/2763)

### 错误修复

- 检查警告现在打印相对于当前工作目录的违规 Dockerfile 的完整文件路径。[docker/buildx#2672](https://github.com/docker/buildx/pull/2672)
- 更新了 `--check` 和 `--call` 选项的备用镜像到正确的引用。[docker/buildx#2705](https://github.com/docker/buildx/pull/2705)
- 修复了在实验性模式下不显示构建详情链接的问题。[docker/buildx#2722](https://github.com/docker/buildx/pull/2722)
- 修复了 Bake 的无效目标链接验证问题。[docker/buildx#2700](https://github.com/docker/buildx/pull/2700)
- 修复了运行无效命令时缺少错误消息的问题。[docker/buildx#2741](https://github.com/docker/buildx/pull/2741)
- 修复了 `--call` 请求中本地状态可能出现的虚假警告。[docker/buildx#2754](https://github.com/docker/buildx/pull/2754)
- 修复了在 Bake 中使用链接目标时潜在的授权问题。[docker/buildx#2701](https://github.com/docker/buildx/pull/2701)
- 修复了使用 `sudo` 运行 Buildx 后访问本地状态时可能出现的权限问题。[docker/buildx#2745](https://github.com/docker/buildx/pull/2745)

### 封装

- Compose 兼容性已更新至 v2.4.1。[docker/buildx#2760](https://github.com/docker/buildx/pull/2760)

## 0.17.1

{{< release-date date="2024-09-13" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.17.1) 查看。

### 错误修复

- 针对 `docker-container` 和 `kubernetes` 驱动程序，如果在 [BuildKit 配置文件](/manuals/build/buildkit/toml-configuration.md) 中设置了 `network.host` 授权标志，则在创建构建器时不再自动设置该标志。[docker/buildx#2685]
- 当 `network` 字段为空时，执行 `docker buildx bake --print` 不再打印该字段。[docker/buildx#2689]
- 修复了 WSL2 下的遥测套接字路径。[docker/buildx#2698]

## 0.17.0

{{< release-date date="2024-09-10" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.17.0) 查看。

### 新特性

- 为 Bake 增加了 `basename`、`dirname` 和 `sanitize` 函数。[docker/buildx#2649]
- 增加了对 Bake 授权的支持，以允许在构建期间执行特权操作。[docker/buildx#2666]

### 增强功能

- 为 Bake 命令引入了 CLI 指标追踪。[docker/buildx#2610]
- 为所有构建命令增加了 `--debug` 选项。此前，该选项仅在顶层的 `docker` 和 `docker buildx` 命令中可用。[docker/buildx#2660]
- 允许从标准输入为多节点构建器进行构建。[docker/buildx#2656]
- 优化了 `kubernetes` 驱动程序的初始化过程。[docker/buildx#2606]
- 在使用 Bake 构建多个目标时，错误消息中现在包含了目标名称。[docker/buildx#2651]
- 优化了指标处理，以减少进度追踪期间的性能开销。[docker/buildx#2641]
- 完成规则检查后显示警告数量。[docker/buildx#2647]
- 跳过针对前端方法的构建引用和来源元数据。[docker/buildx#2650]
- 增加了在 Bake 文件（HCL 和 JSON）中设置网络模式的支持。[docker/buildx#2671]
- 当 `--metadata-file` 标志与 `--call` 标志一同设置时提供支持。[docker/buildx#2640]
- 为多个 Bake 目标使用的本地上下文使用共享会话。[docker/buildx#2615], [docker/buildx#2607], [docker/buildx#2663]

### 错误修复

- 优化了内存管理，以避免不必要的分配。[docker/buildx#2601]

### 封装更新

- Compose 支持已更新至 v2.1.6。[docker/buildx#2547]

## 0.16.2

{{< release-date date="2024-07-25" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.16.2) 查看。

### 错误修复

- 修复了将本地缓存导出到 NFS 卷时可能出现的 "bad file descriptor" 错误 [docker/buildx#2629](https://github.com/docker/buildx/pull/2629/)。

## 0.16.1

{{< release-date date="2024-07-18" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.16.1) 查看。

### 错误修复

- 修复了 `buildx bake --print` 命令中由于数据竞争可能导致的 panic [docker/buildx#2603](https://github.com/docker/buildx/pull/2603/)。
- 优化了关于使用 `--debug` 标志检查构建警告的提示信息 [docker/buildx#2612](https://github.com/docker/buildx/pull/2612/)。

## 0.16.0

{{< release-date date="2024-07-11" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.16.0) 查看。

### 新特性

- Bake 命令现在支持 `--call` 和 `--check` 标志，目标定义中支持 `call` 属性，用于选择自定义前端方法。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/), [docker/buildx#2576](https://github.com/docker/buildx/pull/2576/)
- {{< badge color=violet text=实验性 >}} Bake 现在支持 `--list-targets` 和 `--list-variables` 标志，用于检查项目的定义和可能的配置选项。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/)
- Bake 定义中的变量和目标现在支持新的 `description` 属性，用于定义可通过 `--list-targets` 和 `--list-variables` 检查的文本描述。[docker/buildx#2556](https://github.com/docker/buildx/pull/2556/)
- Bake 现在支持打印构建检查违规警告。[docker/buildx#2501](https://github.com/docker/buildx/pull/2501/)

### 增强功能

- 构建命令现在确保多节点构建为每个节点使用相同的构建引用。[docker/buildx#2572](https://github.com/docker/buildx/pull/2572/)
- 避免了重复请求并提升了远程驱动程序的性能。[docker/buildx#2501](https://github.com/docker/buildx/pull/2501/)
- 构建警告现在可以通过设置 `BUILDX_METADATA_WARNINGS=1` 环境变量保存到元数据文件中。[docker/buildx#2551](https://github.com/docker/buildx/pull/2551/), [docker/buildx#2521](https://github.com/docker/buildx/pull/2521/), [docker/buildx#2550](https://github.com/docker/buildx/pull/2550/)
- 优化了未检测到警告时 `--check` 标志的消息显示。[docker/buildx#2549](https://github.com/docker/buildx/pull/2549/)

### 错误修复

- 修复了构建期间对多类型注解的支持。[docker/buildx#2522](https://github.com/docker/buildx/pull/2522/)
- 修复了一个回归问题：由于增量传输复用，切换项目时可能发生低效的文件传输。[docker/buildx#2558](https://github.com/docker/buildx/pull/2558/)
- 修复了链式 Bake 目标的错误默认加载行为。[docker/buildx#2583](https://github.com/docker/buildx/pull/2583/)
- 修复了 Bake 中错误的 `COMPOSE_PROJECT_NAME` 处理。[docker/buildx#2579](https://github.com/docker/buildx/pull/2579/)
- 修复了多节点构建对索引注解 (index annotations) 的支持。[docker/buildx#2546](https://github.com/docker/buildx/pull/2546/)
- 修复了从远程上下文捕获构建的来源元数据的问题。[docker/buildx#2560](https://github.com/docker/buildx/pull/2560/)

### 封装更新

- Compose 支持已更新至 v2.1.3。[docker/buildx#2547](https://github.com/docker/buildx/pull/2547/)

## 0.15.1

{{< release-date date="2024-06-18" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.15.1) 查看。

### 错误修复

- 修复了某些使用 `--check` 的验证请求中缺失构建错误和退出码的问题。[docker/buildx#2518](https://github.com/docker/buildx/pull/2518/)
- 将 `--check` 的备用镜像更新至 Dockerfile v1.8.1。[docker/buildx#2538](https://github.com/docker/buildx/pull/2538/)

## 0.15.0

{{< release-date date="2024-06-11" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.15.0) 查看。

### 新特性

- 新的 `--call` 选项允许设置构建的评估方法，取代了之前的实验性 `--print` 标志。[docker/buildx#2498](https://github.com/docker/buildx/pull/2498/), [docker/buildx#2487](https://github.com/docker/buildx/pull/2487/), [docker/buildx#2513](https://github.com/docker/buildx/pull/2513/)

  除了默认的 `build` 方法外，Dockerfile 前端还实现了以下方法：

  - [`--call=check`](/reference/cli/docker/buildx/build.md#check)：运行构建配置的验证程序。有关构建检查的更多信息，请参见 [构建检查](/manuals/build/checks.md)。
  - [`--call=outline`](/reference/cli/docker/buildx/build.md#call-outline)：显示当前构建将使用的配置，包括所有构建参数、机密、SSH 挂载等。
  - [`--call=targets`](/reference/cli/docker/buildx/build.md#call-targets)：显示所有可用的目标及其描述。

- 为 `docker buildx imagetools create` 命令增加了新的 `--prefer-index` 标志，用于控制从单个平台镜像清单创建镜像时的行为。[docker/buildx#2482](https://github.com/docker/buildx/pull/2482/)
- [`kubernetes` 驱动程序](/manuals/build/builders/drivers/kubernetes.md) 现在支持配置部署超时的 `timeout` 选项。[docker/buildx#2492](https://github.com/docker/buildx/pull/2492/)
- 增加了针对构建警告类型的全新指标定义。[docker/buildx#2482](https://github.com/docker/buildx/pull/2482/), [docker/buildx#2507](https://github.com/docker/buildx/pull/2507/)
- [`buildx prune`](/reference/cli/docker/buildx/prune.md) 和 [`buildx du`](/reference/cli/docker/buildx/du.md) 命令现在支持反向过滤和前缀过滤器。[docker/buildx#2473](https://github.com/docker/buildx/pull/2473/)
- 使用 Bake 构建 Compose 文件现在支持传递 SSH 转发配置。[docker/buildx#2445](https://github.com/docker/buildx/pull/2445/)
- 修复了为 `kubernetes` 驱动程序配置自定义 TLS 证书的问题。[docker/buildx#2454](https://github.com/docker/buildx/pull/2454/)
- 修复了加载节点时并发访问 kubeconfig 的问题。[docker/buildx#2497](https://github.com/docker/buildx/pull/2497/)

### 封装更新

- Compose 支持已更新至 v2.1.2。[docker/buildx#2502](https://github.com/docker/buildx/pull/2502/), [docker/buildx#2425](https://github.com/docker/buildx/pull/2425/)

## 0.14.0

{{< release-date date="2024-04-18" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.14.0) 查看。

### 增强功能

- 增加了对 `--print=lint` 的支持（实验性）。[docker/buildx#2404](https://github.com/docker/buildx/pull/2404), [docker/buildx#2406](https://github.com/docker/buildx/pull/2406)
- 修复了前端自定义实现打印子请求时的 JSON 格式化问题。[docker/buildx#2374](https://github.com/docker/buildx/pull/2374)
- 带有 `--metadata-file` 进行构建时现在会设置来源记录。[docker/buildx#2280](https://github.com/docker/buildx/pull/2280)
- 为远程定义增加了 [Git 身份验证支持](./bake/remote-definition.md#远程定义在私有仓库中)。[docker/buildx#2363](https://github.com/docker/buildx/pull/2363)
- 为 `docker-container`、`remote` 和 `kubernetes` 驱动程序增加了新的 `default-load` 驱动选项，用于默认将构建结果加载到 Docker 引擎的镜像库中。[docker/buildx#2259](https://github.com/docker/buildx/pull/2259)
- 为 [`kubernetes` 驱动程序](/manuals/build/builders/drivers/kubernetes.md) 增加了 `requests.ephemeral-storage`、`limits.ephemeral-storage` 和 `schedulername` 选项。[docker/buildx#2370](https://github.com/docker/buildx/pull/2370), [docker/buildx#2415](https://github.com/docker/buildx/pull/2415)
- 为 `docker-bake.hcl` 文件增加了 `indexof` 函数。[docker/buildx#2384](https://github.com/docker/buildx/pull/2384)
- Buildx 的 OpenTelemetry 指标现在可以测量构建期间空闲时间、镜像导出、运行操作以及镜像源操作的镜像传输时长。[docker/buildx#2316](https://github.com/docker/buildx/pull/2316), [docker/buildx#2317](https://github.com/docker/buildx/pull/2317), [docker/buildx#2323](https://github.com/docker/buildx/pull/2323), [docker/buildx#2271](https://github.com/docker/buildx/pull/2271)
- 向与 `desktop-linux` 上下文关联的 OpenTelemetry 端点发送构建进度指标不再要求开启 Buildx 的实验性模式 (`BUILDX_EXPERIMENTAL=1`)。[docker/buildx#2344](https://github.com/docker/buildx/pull/2344)

### 错误修复

- 修复了在使用多个 Bake 文件定义时，`--load` 和 `--push` 错误覆盖输出的问题。[docker/buildx#2336](https://github.com/docker/buildx/pull/2336)
- 修复了开启实验性模式时从标准输入构建的问题。[docker/buildx#2394](https://github.com/docker/buildx/pull/2394)
- 修复了委托追踪数据可能重复的问题。[docker/buildx#2362](https://github.com/docker/buildx/pull/2362)

### 封装更新

- Compose 支持已更新至 [v2.26.1](https://github.com/docker/compose/releases/tag/v2.26.1)（通过 [`compose-go` v2.0.2](https://github.com/compose-spec/compose-go/releases/tag/v2.0.2)）。[docker/buildx#2391](https://github.com/docker/buildx/pull/2391)

## 0.13.1

{{< release-date date="2024-03-13" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.13.1) 查看。

### 错误修复

- 修复了使用远程驱动程序连接到 `docker-container://` 和 `kube-pod://` 风格 URL 的问题。[docker/buildx#2327](https://github.com/docker/buildx/pull/2327)
- 修复了当 Bake 目标已经定义了非镜像输出时，对 `--push` 的处理。[docker/buildx#2330](https://github.com/docker/buildx/pull/2330)

## 0.13.0

{{< release-date date="2024-03-06" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.13.0) 查看。

### 新特性

- 增加了新的 `docker buildx dial-stdio` 命令，用于直接联系配置的构建器实例的 BuildKit 守护进程。[docker/buildx#2112](https://github.com/docker/buildx/pull/2112)
- 现在可以使用 `remote` 驱动程序和 npipe 连接创建 Windows 容器构建器。[docker/buildx#2287](https://github.com/docker/buildx/pull/2287)
- Npipe URL 方案现已在 Windows 上得到支持。[docker/buildx#2250](https://github.com/docker/buildx/pull/2250)
- {{< badge color=violet text=实验性 >}} Buildx 现在可以导出关于构建时长和传输大小的 OpenTelemetry 指标。[docker/buildx#2235](https://github.com/docker/buildx/pull/2235), [docker/buildx#2258](https://github.com/docker/buildx/pull/2258) [docker/buildx#2225](https://github.com/docker/buildx/pull/2225) [docker/buildx#2224](https://github.com/docker/buildx/pull/2224) [docker/buildx#2155](https://github.com/docker/buildx/pull/2155)

### 增强功能

- Bake 命令现在支持定义 `shm-size` 和 `ulimit` 值。[docker/buildx#2279](https://github.com/docker/buildx/pull/2279), [docker/buildx#2242](https://github.com/docker/buildx/pull/2242)
- 优化了使用远程驱动程序连接到不健康节点时的处理。[docker/buildx#2130](https://github.com/docker/buildx/pull/2130)
- 使用 `docker-container` 和 `kubernetes` 驱动程序的构建器现在默认允许 `network.host` 授权（允许访问容器的网络）。[docker/buildx#2266](https://github.com/docker/buildx/pull/2266)
- 构建任务现在可以使用单个命令使用多个输出（需要 BuildKit v0.13+）。[docker/buildx#2290](https://github.com/docker/buildx/pull/2290), [docker/buildx#2302](https://github.com/docker/buildx/pull/2302)
- 默认的 Git 存储库路径现在通过配置的追踪分支（tracking branch）查找。[docker/buildx#2146](https://github.com/docker/buildx/pull/2146)
- 修复了在 Bake 中使用链接目标时可能导致的缓存失效问题。[docker/buildx#2265](https://github.com/docker/buildx/pull/2265)
- 修复了 WSL 下 Git 存储库路径脱敏的问题。[docker/buildx#2167](https://github.com/docker/buildx/pull/2167)
- 现在可以使用单个命令移除多个构建器。[docker/buildx#2140](https://github.com/docker/buildx/pull/2140)
- 通过 Unix 套接字实现了新的取消信号处理。[docker/buildx#2184](https://github.com/docker/buildx/pull/2184) [docker/buildx#2289](https://github.com/docker/buildx/pull/2289)
- Compose 规范支持已更新至 v2.0.0-rc.8。[docker/buildx#2205](https://github.com/docker/buildx/pull/2205)
- `docker buildx create` 的 `--config` 标志重命名为 `--buildkitd-config`。[docker/buildx#2268](https://github.com/docker/buildx/pull/2268)
- `docker buildx build` 的 `--metadata-file` 标志现在还可以返回构建引用，可用于进一步的构建调试，例如在 Docker Desktop 中。[docker/buildx#2263](https://github.com/docker/buildx/pull/2263)
- `docker buildx bake` 命令现在为所有目标共享同一个身份验证提供者，以提高性能。[docker/buildx#2147](https://github.com/docker/buildx/pull/2147)
- `docker buildx imagetools inspect` 命令现在显示经 DSSE 签名的 SBOM 和来源 (Provenance) 证明。[docker/buildx#2194](https://github.com/docker/buildx/pull/2194)
- `docker buildx ls` 命令现在支持通过 `--format` 选项控制输出。[docker/buildx#1787](https://github.com/docker/buildx/pull/1787)
- `docker-container` 驱动程序现在支持定义 BuildKit 容器重启策略的驱动选项。[docker/buildx#1271](https://github.com/docker/buildx/pull/1271)
- 从 Buildx 导出的 VCS 属性现在包含了相对于当前 Git 存储库的本地目录子路径。[docker/buildx#2156](https://github.com/docker/buildx/pull/2156)
- `--add-host` 标志现在允许针对 IPv6 地址使用 `=` 分隔符。[docker/buildx#2121](https://github.com/docker/buildx/pull/2121)

### 错误修复

- 修复了使用 `--progress=rawjson` 导出进度时的额外输出问题 [docker/buildx#2252](https://github.com/docker/buildx/pull/2252)
- 修复了 Windows 上可能出现的控制台警告。[docker/buildx#2238](https://github.com/docker/buildx/pull/2238)
- 修复了在使用多个 Bake 配置时可能出现的不一致合并顺序问题。[docker/buildx#2237](https://github.com/docker/buildx/pull/2237)
- 修复了 `docker buildx imagetools create` 命令中可能发生的 panic。[docker/buildx#2230](https://github.com/docker/buildx/pull/2230)

## 0.12.1

{{< release-date date="2024-01-12" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.12.1) 查看。

### 错误修复与增强

- 修复了一些 `--driver-opt` 值的错误验证，这些值可能导致 panic 并导致存储的状态损坏。
  [docker/buildx#2176](https://github.com/docker/buildx/pull/2176)

## 0.12.0

{{< release-date date="2023-11-16" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.12.0) 查看。

### 新特性

- 为 `buildx build` 增加了新的 `--annotation` 标志，并在 Bake 文件中增加了 `annotations` 键，允许为构建结果添加 OCI 注解。
  [#2020](https://github.com/docker/buildx/pull/2020),
  [#2098](https://github.com/docker/buildx/pull/2098)
- 增加了新的实验性调试特性，包括一个新的 `debug` 命令和交互式调试控制台。
  此特性目前需要设置 `BUILDX_EXPERIMENTAL=1`。
  [#2006](https://github.com/docker/buildx/pull/2006),
  [#1896](https://github.com/docker/buildx/pull/1896),
  [#1970](https://github.com/docker/buildx/pull/1970),
  [#1914](https://github.com/docker/buildx/pull/1914),
  [#2026](https://github.com/docker/buildx/pull/2026),
  [#2086](https://github.com/docker/buildx/pull/2086)

### 错误修复与增强

- 构建期间，`--add-host` 标志现在可以使用特殊的 `host-gateway` IP 映射。
  [#1894](https://github.com/docker/buildx/pull/1894),
  [#2083](https://github.com/docker/buildx/pull/2083)
- Bake 现在允许在从远程定义构建时添加本地源文件。
  [#1838](https://github.com/docker/buildx/pull/1838)
- 构建结果上传到 Docker 的状态现在可以在进度条上交互式显示。
  [#1994](https://github.com/docker/buildx/pull/1994)
- 优化了引导多节点构建集群时的错误处理。
  [#1869](https://github.com/docker/buildx/pull/1869)
- `buildx imagetools create` 命令现在允许在注册表中创建新镜像时添加注解。
  [#1965](https://github.com/docker/buildx/pull/1965)
- 现在可以使用 Docker 和远程驱动程序从 buildx 进行 OpenTelemetry 构建追踪委托。
  [#2034](https://github.com/docker/buildx/pull/2034)
- Bake 命令现在会在进度条上显示加载构建定义的所有文件。
  [#2076](https://github.com/docker/buildx/pull/2076)
- Bake 文件现在允许在多个定义文件中定义相同的属性。
  [#1062](https://github.com/docker/buildx/pull/1062)
- 将 Bake 命令与远程定义配合使用时，现在允许该定义使用本地 Dockerfile。
  [#2015](https://github.com/docker/buildx/pull/2015)
- Docker 容器驱动程序现在显式设置 BuildKit 配置路径，以确保主流镜像和无 root 镜像从相同位置加载配置。
  [#2093](https://github.com/docker/buildx/pull/2093)
- 提升了检测 BuildKit 实例完成引导的性能。
  [#1934](https://github.com/docker/buildx/pull/1934)
- 容器驱动程序现在接受许多新的驱动选项，用于定义 BuildKit 容器的资源限制。
  [#2048](https://github.com/docker/buildx/pull/2048)
- 优化了检查命令的格式化显示。
  [#2068](https://github.com/docker/buildx/pull/2068)
- 优化了关于驱动程序能力的错误消息。
  [#1998](https://github.com/docker/buildx/pull/1998)
- 优化了在没有目标的情况下调用 Bake 命令时的错误。
  [#2100](https://github.com/docker/buildx/pull/2100)
- 允许在以独立模式运行时通过环境变量启用调试日志。
  [#1821](https://github.com/docker/buildx/pull/1821)
- 使用 Docker 驱动程序时，默认镜像解析模式已更新为首选本地 Docker 镜像，以保持向后兼容性。
  [#1886](https://github.com/docker/buildx/pull/1886)
- Kubernetes 驱动程序现在允许为 BuildKit 部署和 pod 设置自定义注解和标签。
  [#1938](https://github.com/docker/buildx/pull/1938)
- Kubernetes 驱动程序现在允许通过端点配置设置身份验证令牌。
  [#1891](https://github.com/docker/buildx/pull/1891)
- 修复了 Bake 中链式目标的潜在问题，该问题可能导致构建失败或某个目标的本地源被多次上传。
  [#2113](https://github.com/docker/buildx/pull/2113)
- 修复了使用 Bake 命令的矩阵 (matrix) 特性时访问全局目标属性的问题。
  [#2106](https://github.com/docker/buildx/pull/2106)
- 修复了某些构建标志的格式验证。
  [#2040](https://github.com/docker/buildx/pull/2040)
- 修复了在引导构建器节点时由于不必要的锁定导致某些命令受阻的问题。
  [#2066](https://github.com/docker/buildx/pull/2066)
- 修复了多个构建任务尝试并行引导同一个构建器实例的情况。
  [#2000](https://github.com/docker/buildx/pull/2000)
- 修复了在某些情况下上传构建结果到 Docker 时的错误被丢弃的问题。
  [#1927](https://github.com/docker/buildx/pull/1927)
- 修复了根据构建输出检测缺失证明 (attestation) 支持能力的问题。
  [#1988](https://github.com/docker/buildx/pull/1988)
- 修复了用于在 Bake 远程定义中加载的构建任务，使其不显示在构建历史记录中。
  [#1961](https://github.com/docker/buildx/pull/1961),
  [#1954](https://github.com/docker/buildx/pull/1954)
- 修复了使用 Bake 构建定义了配置文件的 Compose 文件时的错误。
  [#1903](https://github.com/docker/buildx/pull/1903)
- 修复了进度条上可能出现的时间修正错误。
  [#1968](https://github.com/docker/buildx/pull/1968)
- 修复了在使用新控制器接口的构建中传递自定义 cgroup parent 的问题。
  [#1913](https://github.com/docker/buildx/pull/1913)

### 封装

- Compose 支持已更新至 1.20，允许在使用 Bake 命令时使用 "include" 功能。
  [#1971](https://github.com/docker/buildx/pull/1971),
  [#2065](https://github.com/docker/buildx/pull/2065),
  [#2094](https://github.com/docker/buildx/pull/2094)

## 0.11.2

{{< release-date date="2023-07-18" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.11.2) 查看。

### 错误修复与增强

- 修复了一个回归问题：导致 buildx 未能从实例存储中读取 `KUBECONFIG` 路径。
  [docker/buildx#1941](https://github.com/docker/buildx/pull/1941)
- 修复了一个回归问题：结果句柄构建任务会错误地显示在构建历史记录中。
  [docker/buildx#1954](https://github.com/docker/buildx/pull/1954)

## 0.11.1

{{< release-date date="2023-07-05" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.11.1) 查看。

### 错误修复与增强

- 修复了 Bake 的一个回归问题：配置文件的服务无法加载。
  [docker/buildx#1903](https://github.com/docker/buildx/pull/1903)
- 修复了一个回归问题：`--cgroup-parent` 选项在构建期间无效。
  [docker/buildx#1913](https://github.com/docker/buildx/pull/1913)
- 修复了一个回归问题：有效的 Docker 上下文可能导致 buildx 构建器名称验证失败。
  [docker/buildx#1879](https://github.com/docker/buildx/pull/1879)
- 修复了构建期间调整终端大小时可能发生的 panic。
  [docker/buildx#1929](https://github.com/docker/buildx/pull/1929)

## 0.11.0

{{< release-date date="2023-06-13" >}}

此版本的完整发行说明可在 [GitHub 上](https://github.com/docker/buildx/releases/tag/v0.11.0) 查看。

### 新特性

- Bake 现在支持 [矩阵构建 (matrix builds)](/manuals/build/bake/reference.md#targetmatrix)。
  `target` 上新增的矩阵字段允许您创建多个相似的目标，从而消除 Bake 文件中的重复代码。[docker/buildx#1690](https://github.com/docker/buildx/pull/1690)
- 增加了新的实验性 `--detach` 标志，用于以分离模式运行构建任务。
  [docker/buildx#1296](https://github.com/docker/buildx/pull/1296),
  [docker/buildx#1620](https://github.com/docker/buildx/pull/1620),
  [docker/buildx#1614](https://github.com/docker/buildx/pull/1614),
  [docker/buildx#1737](https://github.com/docker/buildx/pull/1737),
  [docker/buildx#1755](https://github.com/docker/buildx/pull/1755)
- 增加了新的实验性 [调试监控模式 (debug monitor mode)](https://github.com/docker/buildx/blob/v0.11.0-rc1/docs/guides/debugging.md)，允许您在构建中开启调试会话。
  [docker/buildx#1626](https://github.com/docker/buildx/pull/1626),
  [docker/buildx#1640](https://github.com/docker/buildx/pull/1640)
- 增加了新的 [`EXPERIMENTAL_BUILDKIT_SOURCE_POLICY` 环境变量](./building/variables.md#experimental_buildkit_source_policy)，用于应用 BuildKit 源码策略文件。
  [docker/buildx#1628](https://github.com/docker/buildx/pull/1628)

### 错误修复与增强

- 当开启 containerd 镜像存储后，`--load` 现在支持加载多平台镜像。
  [docker/buildx#1813](https://github.com/docker/buildx/pull/1813)
- 构建进度输出现在会显示正在使用的构建器名称。
  [docker/buildx#1177](https://github.com/docker/buildx/pull/1177)
- Bake 现在支持检测 `compose.{yml,yaml}` 文件。
  [docker/buildx#1752](https://github.com/docker/buildx/pull/1752)
- Bake 现在支持新的 Compose 构建键 `dockerfile_inline` 和 `additional_contexts`。
  [docker/buildx#1784](https://github.com/docker/buildx/pull/1784)
- Bake 现在支持 replace HCL 函数。
  [docker/buildx#1720](https://github.com/docker/buildx/pull/1720)
- Bake 现在允许将多个相似的证明参数合并为一个参数，从而支持使用单个全局值进行覆盖。
  [docker/buildx#1699](https://github.com/docker/buildx/pull/1699)
- 对 shell 补全提供了初步支持。
  [docker/buildx#1727](https://github.com/docker/buildx/pull/1727)
- 对于使用 `docker` 驱动程序的构建器，其 BuildKit 版本现在能正确显示在 `buildx ls` 和 `buildx inspect` 中。
  [docker/buildx#1552](https://github.com/docker/buildx/pull/1552)
- 在 buildx 检查视图中显示额外的构建器节点详情。
  [docker/buildx#1440](https://github.com/docker/buildx/pull/1440),
  [docker/buildx#1854](https://github.com/docker/buildx/pull/1874)
- 使用 `remote` 驱动程序的构建器允许在不提供自身密钥/证书的情况下使用 TLS（如果 BuildKit 远程配置支持的话）。
  [docker/buildx#1693](https://github.com/docker/buildx/pull/1693)
- 使用 `kubernetes` 驱动程序的构建器支持新的 `serviceaccount` 选项，用于设置 Kubernetes pod 的 `serviceAccountName`。
  [docker/buildx#1597](https://github.com/docker/buildx/pull/1597)
- 使用 `kubernetes` 驱动程序的构建器支持 kubeconfig 文件中的 `proxy-url` 选项。
  [docker/buildx#1780](https://github.com/docker/buildx/pull/1780)
- 使用 `kubernetes` 驱动程序的构建器，如果未显式提供节点名称，现在会自动分配。
  [docker/buildx#1673](https://github.com/docker/buildx/pull/1673)
- 修复了 Windows 上为 `docker-container` 驱动程序写入证书时的无效路径问题。
  [docker/buildx#1831](https://github.com/docker/buildx/pull/1831)
- 修复了通过 SSH 访问远程 Bake 文件时发生的 Bake 失败问题。
  [docker/buildx#1711](https://github.com/docker/buildx/pull/1711),
  [docker/buildx#1734](https://github.com/docker/buildx/pull/1734)
- 修复了远程 Bake 上下文解析错误导致的问题。
  [docker/buildx#1783](https://github.com/docker/buildx/pull/1783)
- 修复了 Bake 上下文中 `BAKE_CMD_CONTEXT` 和 `cwd://` 路径的路径解析。
  [docker/buildx#1840](https://github.com/docker/buildx/pull/1840)
- 修复了使用 `buildx imagetools create` 创建镜像时混合使用 OCI 和 Docker 媒体类型的问题。
  [docker/buildx#1797](https://github.com/docker/buildx/pull/1797)
- 修复了 `--iidfile` 和 `-q` 之间镜像 ID 不匹配的问题。
  [docker/buildx#1844](https://github.com/docker/buildx/pull/1844)
- 修复了混合静态凭据和 IAM 配置文件时的 AWS 身份验证问题。
  [docker/buildx#1816](https://github.com/docker/buildx/pull/1816)

## 0.10.4

{{< release-date date="2023-03-06" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复与增强

- 增加了 `BUILDX_NO_DEFAULT_ATTESTATIONS` 作为 `--provenance false` 的替代方案。[docker/buildx#1645](https://github.com/docker/buildx/issues/1645)
- 为了性能，默认禁用了脏（dirty）Git 检出检测。可以通过设置 `BUILDX_GIT_CHECK_DIRTY` 手动开启。[docker/buildx#1650](https://github.com/docker/buildx/issues/1650)
- 在发送给 BuildKit 之前，从 VCS 提示 URL 中剥离凭据信息。[docker/buildx#1664](https://github.com/docker/buildx/issues/1664)

## 0.10.3

{{< release-date date="2023-02-16" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复与增强

- 修复了收集 Git 来源信息时的可达提交和警告问题。[docker/buildx#1592](https://github.com/docker/buildx/issues/1592), [docker/buildx#1634](https://github.com/docker/buildx/issues/1634)
- 修复了一个回归问题：未验证 Docker 上下文。[docker/buildx#1596](https://github.com/docker/buildx/issues/1596)
- 修复了 JSON Bake 定义中的函数解析问题。[docker/buildx#1605](https://github.com/docker/buildx/issues/1605)
- 修复了原始 HCL Bake 诊断信息被丢弃的情况。[docker/buildx#1607](https://github.com/docker/buildx/issues/1607)
- 修复了使用 Bake 和 Compose 文件时标签未能正确设置的问题。[docker/buildx#1631](https://github.com/docker/buildx/issues/1631)

## 0.10.2

{{< release-date date="2023-01-30" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复与增强

- 修复了多节点构建中未考虑首选平台顺序的问题。[docker/buildx#1561](https://github.com/docker/buildx/issues/1561)
- 修复了处理 `SOURCE_DATE_EPOCH` 环境变量时可能发生的 panic。[docker/buildx#1564](https://github.com/docker/buildx/issues/1564)
- 修复了自 BuildKit v0.11 起，在某些注册表上进行多节点清单合并时可能出现的推送错误。[docker/buildx#1566](https://github.com/docker/buildx/issues/1566)
- 优化了收集 Git 来源信息时的警告显示。[docker/buildx#1568](https://github.com/docker/buildx/issues/1568)

## 0.10.1

{{< release-date date="2023-01-27" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 错误修复与增强

- 修复了将正确的原始 URL 作为 `vsc:source` 元数据发送的问题。[docker/buildx#1548](https://github.com/docker/buildx/issues/1548)
- 修复了由于数据竞争可能导致的 panic。[docker/buildx#1504](https://github.com/docker/buildx/issues/1504)
- 修复了 `rm --all-inactive` 的回归问题。[docker/buildx#1547](https://github.com/docker/buildx/issues/1547)
- 通过延迟加载数据，优化了 `imagetools inspect` 中的证明访问。[docker/buildx#1546](https://github.com/docker/buildx/issues/1546)
- 正确地将能力请求标记为内部请求。[docker/buildx#1538](https://github.com/docker/buildx/issues/1538)
- 检测无效的证明配置。[docker/buildx#1545](https://github.com/docker/buildx/issues/1545)
- 更新了 containerd 补丁，修复了影响 `imagetools` 命令的潜在推送回归问题。[docker/buildx#1559](https://github.com/docker/buildx/issues/1559)

## 0.10.0

{{< release-date date="2023-01-10" >}}

{{% include "buildx-v0.10-disclaimer.md" %}}

### 新特性

- `buildx build` 命令现在支持新的 `--attest` 标志，以及简写 `--sbom` 和 `--provenance`，用于为您当前的构建添加证明。[docker/buildx#1412](https://github.com/docker/buildx/issues/1412) [docker/buildx#1475](https://github.com/docker/buildx/issues/1475)
  - `--attest type=sbom` 或 `--sbom=true` 增加 [SBOM 证明](/manuals/build/metadata/attestations/sbom.md)。
  - `--attest type=provenance` 或 `--provenance=true` 增加 [SLSA 来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。
  - 创建 OCI 镜像时，默认会包含一个最小化的来源证明。
- 当配合支持来源证明的 BuildKit 进行构建时，Buildx 会自动分享构建上下文的版本控制信息，以便在来源信息中显示以供后续调试。此前，这仅在直接从 Git URL 构建时发生。要选择退出此行为，可以设置 `BUILDX_GIT_INFO=0`。此外，还可以通过设置 `BUILDX_GIT_LABELS=1` 自动定义带有 VCS 信息的标签。[docker/buildx#1462](https://github.com/docker/buildx/issues/1462), [docker/buildx#1297](https://github.com/docker/buildx), [docker/buildx#1341](https://github.com/docker/buildx/issues/1341), [docker/buildx#1468](https://github.com/docker/buildx), [docker/buildx#1477](https://github.com/docker/buildx/issues/1477)
- 带 `--build-context` 的命名上下文现在支持 `oci-layout://` 协议，用于使用本地 OCI 布局目录的值初始化上下文。例如 `--build-context stagename=oci-layout://path/to/dir`。此特性要求使用 BuildKit v0.11.0+ 和 Dockerfile 1.5.0+。[docker/buildx#1456](https://github.com/docker/buildx/issues/1456)
- Bake 现在支持 [资源插值 (resource interpolation)](bake/inheritance.md#reusing-single-attribute-from-targets)，您可以在其中复用其他目标定义中的值。[docker/buildx#1434](https://github.com/docker/buildx/issues/1434)
- 如果您的环境中定义了 `SOURCE_DATE_EPOCH` 环境变量，Buildx 现在会自动转发它。此特性旨在配合 BuildKit v0.11.0+ 中更新的 [可重现构建 (reproducible builds)](https://github.com/moby/buildkit/blob/master/docs/build-repro.md) 支持使用。[docker/buildx#1482](https://github.com/docker/buildx/issues/1482)
- Buildx 现在会记录构建器的最后一次活动，以便更好地组织构建器实例。[docker/buildx#1439](https://github.com/docker/buildx/issues/1439)
- Bake 定义现在支持为 [变量](bake/reference.md#variable) 和 [标签](bake/reference.md#targetlabels) 使用 null 值，以便针对构建参数和标签使用 Dockerfile 中设置的默认值。[docker/buildx#1449](https://github.com/docker/buildx/issues/1449)
- [`buildx imagetools inspect` 命令](/reference/cli/docker/buildx/imagetools/inspect.md) 现在支持显示 SBOM 和来源数据。[docker/buildx#1444](https://github.com/docker/buildx/issues/1444), [docker/buildx#1498](https://github.com/docker/buildx/issues/1498)
- 提升了 `ls` 命令和 inspect 流程的性能。[docker/buildx#1430](https://github.com/docker/buildx/issues/1430), [docker/buildx#1454](https://github.com/docker/buildx/issues/1454), [docker/buildx#1455](https://github.com/docker/buildx/issues/1455), [docker/buildx#1345](https://github.com/docker/buildx/issues/1345)
- 使用 [Docker 驱动程序](/manuals/build/builders/drivers/docker.md) 增加额外 hosts 时，现在支持 Docker 特有的 `host-gateway` 特殊值。[docker/buildx#1446](https://github.com/docker/buildx/issues/1446)
- [OCI 导出器](exporters/oci-docker.md) 现在支持 `tar=false` 选项，以便直接在目录中导出 OCI 格式。[docker/buildx#1420](https://github.com/docker/buildx/issues/1420)

### 升级

- 将 Compose 规范更新至 1.6.0。[docker/buildx#1387](https://github.com/docker/buildx/issues/1387)

### 错误修复与增强

- `--invoke` 现在可以从镜像元数据加载默认启动环境。[docker/buildx#1324](https://github.com/docker/buildx/issues/1324)
- 修复了容器驱动程序在 UserNS 方面的行为。[docker/buildx#1368](https://github.com/docker/buildx/issues/1368)
- 修复了 Bake 在使用错误变量值类型时可能发生的 panic。[docker/buildx#1442](https://github.com/docker/buildx/issues/1442)
- 修复了 `imagetools inspect` 中可能发生的 panic。[docker/buildx#1441](https://github.com/docker/buildx/issues/1441) [docker/buildx#1406](https://github.com/docker/buildx/issues/1406)
- 修复了默认情况下向 BuildKit 发送空 `--add-host` 值的问题。[docker/buildx#1457](https://github.com/docker/buildx/issues/1457)
- 修复了带进度组的进度前缀处理。[docker/buildx#1305](https://github.com/docker/buildx/issues/1305)
- 修复了 Bake 中递归解析组的问题。[docker/buildx#1313](https://github.com/docker/buildx/issues/1313)
- 修复了多节点构建器清单上可能出现的缩进错误。[docker/buildx#1396](https://github.com/docker/buildx/issues/1396)
- 修复了由于缺失 OpenTelemetry 配置导致的 panic。[docker/buildx#1383](https://github.com/docker/buildx/issues/1383)
- 修复了 TTY 不可用时 `--progress=tty` 的行为。[docker/buildx#1371](https://github.com/docker/buildx/issues/1371)
- 修复了 `prune` 和 `du` 命令中的连接错误条件。[docker/buildx#1307](https://github.com/docker/buildx/issues/1307)

## 0.9.1

{{< release-date date="2022-08-18" >}}

### 错误修复与增强

- `inspect` 命令现在会显示正在使用的 BuildKit 版本。[docker/buildx#1279](https://github.com/docker/buildx/issues/1279)
- 修复了构建包含不带 build 块的服务的 Compose 文件时的回归问题。[docker/buildx#1277](https://github.com/docker/buildx/issues/1277)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.9.1) 中的完整发行说明。

## 0.9.0

{{< release-date date="2022-08-17" >}}

### 新特性

- 支持新的 [`remote` 驱动程序](/manuals/build/builders/drivers/remote.md)，您可以将其用于连接任何已在运行的 BuildKit 实例。
  [docker/buildx#1078](https://github.com/docker/buildx/issues/1078),
  [docker/buildx#1093](https://github.com/docker/buildx/issues/1093),
  [docker/buildx#1094](https://github.com/docker/buildx/issues/1094),
  [docker/buildx#1103](https://github.com/docker/buildx/issues/1103),
  [docker/buildx#1134](https://github.com/docker/buildx/issues/1134),
  [docker/buildx#1204](https://github.com/docker/buildx/issues/1204)
- 即便构建上下文来自外部 Git 或 HTTP URL，您现在也可以从标准输入加载 Dockerfile。[docker/buildx#994](https://github.com/docker/buildx/issues/994)
- 构建命令现在支持新的构建上下文类型 `oci-layout://`，用于 [从本地 OCI 布局目录加载构建上下文](/reference/cli/docker/buildx/build.md#source-oci-layout)。请注意，此特性依赖于尚未发布的 BuildKit 功能，需要使用来自 `moby/buildkit:master` 的构建器实例，直到 BuildKit v0.11 发布。[docker/buildx#1173](https://github.com/docker/buildx/issues/1173)
- 您现在可以使用新的 `--print` 标志来运行由执行构建的 BuildKit 前端支持的辅助函数并打印其结果。您可以在 Dockerfile 中使用此特性，通过 `--print=outline` 显示当前构建支持的构建参数和机密，并通过 `--print=targets` 列出所有可用的 Dockerfile 阶段。此特性为实验性，旨在收集早期反馈，需要启用 `BUILDX_EXPERIMENTAL=1` 环境变量。我们计划在未来更新/扩展此特性而不保持向后兼容性。[docker/buildx#1100](https://github.com/docker/buildx/issues/1100), [docker/buildx#1272](https://github.com/docker/buildx/issues/1272)
- 您现在可以使用新的 `--invoke` 标志从构建结果启动交互式容器，以进行交互式调试循环。您可以使用代码更改重新加载这些容器，或从特殊的监控模式将它们恢复到初始状态。此特性为实验性，旨在收集早期反馈，需要启用 `BUILDX_EXPERIMENTAL=1` 环境变量。我们计划在未来更新/扩展此特性而不开启向后兼容性。
  [docker/buildx#1168](https://github.com/docker/buildx/issues/1168),
  [docker/buildx#1257](https://github.com/docker/buildx),
  [docker/buildx#1259](https://github.com/docker/buildx/issues/1259)
- Buildx 现在能识别环境变量 `BUILDKIT_COLORS` 和 `NO_COLOR`，用以自定义/禁用交互式构建进度条的颜色。[docker/buildx#1230](https://github.com/docker/buildx/issues/1230), [docker/buildx#1226](https://github.com/docker/buildx/issues/1226)
- `buildx ls` 命令现在会显示每个构建器实例当前的 BuildKit 版本。[docker/buildx#998](https://github.com/docker/buildx/issues/998)
- 为了兼容性，`bake` 命令现在在构建 Compose 文件时会自动加载 `.env` 文件。[docker/buildx#1261](https://github.com/docker/buildx/issues/1261)
- Bake 现在支持带有 `cache_to` 定义的 Compose 文件。[docker/buildx#1155](https://github.com/docker/buildx/issues/1155)
- Bake 现在支持新的内置函数 `timestamp()` 用以获取当前时间。[docker/buildx#1214](https://github.com/docker/buildx/issues/1214)
- Bake 现在支持 Compose 构建机密 (build secrets) 定义。[docker/buildx#1069](https://github.com/docker/buildx/issues/1069)
- 现在的 Compose 文件支持通过 `x-bake` 配置额外的构建上下文。[docker/buildx#1256](https://github.com/docker/buildx/issues/1256)
- 检查构建器现在会显示当前的驱动选项配置。[docker/buildx#1003](https://github.com/docker/buildx/issues/1003), [docker/buildx#1066](https://github.com/docker/buildx/issues/1066)

### 更新

- 将 Compose 规范更新至 1.4.0。[docker/buildx#1246](https://github.com/docker/buildx/issues/1246), [docker/buildx#1251](https://github.com/docker/buildx/issues/1251)

### 错误修复与增强

- 更新了 `buildx ls` 命令的输出，以便更好地查看来自不同构建器的错误。[docker/buildx#1109](https://github.com/docker/buildx/issues/1109)
- `buildx create` 命令现在会对构建器参数执行额外验证，以避免创建带有无效配置的构建器实例。[docker/buildx#1206](https://github.com/docker/buildx/issues/1206)
- `buildx imagetools create` 命令现在即便源子镜像位于不同的存储库或注册表中，也能创建新的多平台镜像。[docker/buildx#1137](https://github.com/docker/buildx/issues/1137)
- 您现在可以设置默认的构建器配置，在创建构建器实例且未传递自定义 `--config` 值时使用。[docker/buildx#1111](https://github.com/docker/buildx/issues/1111)
- Docker 驱动程序现在可以检测 `dockerd` 实例是否支持最初被禁用的 BuildKit 特性（如多平台镜像）。[docker/buildx#1260](https://github.com/docker/buildx/issues/1260), [docker/buildx#1262](https://github.com/docker/buildx/issues/1262)
- 在名称中使用 `.` 的 Compose 文件目标现在会被转换为使用 `_`，以便选择器键仍能用于此类目标。[docker/buildx#1011](https://github.com/docker/buildx/issues/1011)
- 增加了对检查有效驱动配置的额外验证。[docker/buildx#1188](https://github.com/docker/buildx/issues/1188), [docker/buildx#1273](https://github.com/docker/buildx/issues/1273)
- `remove` 命令现在会显示被移除的构建器，并禁止移除上下文构建器。[docker/buildx#1128](https://github.com/docker/buildx/issues/1128)
- 使用 Kubernetes 驱动程序时启用 Azure 身份验证。[docker/buildx#974](https://github.com/docker/buildx/issues/974)
- 为 kubernetes 驱动程序增加了 tolerations 处理。[docker/buildx#1045](https://github.com/docker/buildx/issues/1045) [docker/buildx#1053](https://github.com/docker/buildx/issues/1053)
- 在 `kubernetes` 驱动程序中用 `securityContext` 替换了已弃用的 seccomp 注解。[docker/buildx#1052](https://github.com/docker/buildx/issues/1052)
- 修复了处理带 nil 平台的清单时的 panic 问题。[docker/buildx#1144](https://github.com/docker/buildx/issues/1144)
- 修复了 `prune` 命令使用时长过滤器时的问题。[docker/buildx#1252](https://github.com/docker/buildx/issues/1252)
- 修复了 Bake 定义中合并多个 JSON 文件的问题。[docker/buildx#1025](https://github.com/docker/buildx/issues/1025)
- 修复了从 Docker 上下文创建的隐式构建器配置无效或连接断开的问题。[docker/buildx#1129](https://github.com/docker/buildx/issues/1129)
- 修复了使用命名上下文时显示“无输出”警告的条件。[docker/buildx#968](https://github.com/docker/buildx/issues/968)
- 修复了构建器实例与 Docker 上下文同名时重复创建构建器的问题。[docker/buildx#1131](https://github.com/docker/buildx/issues/1131)
- 修复了打印不必要的 SSH 警告日志的问题。[docker/buildx#1085](https://github.com/docker/buildx/issues/1085)
- 修复了在 Bake JSON 定义中使用空变量块时可能发生的 panic。[docker/buildx#1080](https://github.com/docker/buildx/issues/1080)
- 修复了镜像工具命令未能正确处理 `--builder` 标志的问题。[docker/buildx#1067](https://github.com/docker/buildx/issues/1067)
- 修复了自定义镜像与 rootless 选项配合使用时的问题。[docker/buildx#1063](https://github.com/docker/buildx/issues/1063)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.9.0) 中的完整发行说明。

## 0.8.2

{{< release-date date="2022-04-04" >}}

### 更新

- 将 `buildx bake` 使用的 Compose 规范更新至 v1.2.1，以修复解析端口定义的问题。[docker/buildx#1033](https://github.com/docker/buildx/issues/1033)

### 错误修复与增强

- 修复了处理来自 BuildKit v0.10 进度流时可能发生的崩溃。[docker/buildx#1042](https://github.com/docker/buildx/issues/1042)
- 修复了在 `buildx bake` 中，当某组已被父组加载时解析该组的问题。[docker/buildx#1021](https://github.com/docker/buildx/issues/1021)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.8.2) 中的完整发行说明。

## 0.8.1

{{< release-date date="2022-03-21" >}}

### 错误修复与增强

- 修复了处理构建上下文扫描错误时可能发生的 panic。[docker/buildx#1005](https://github.com/docker/buildx/issues/1005)
- 为了向后兼容，允许在 `buildx bake` 的 Compose 目标名称中使用 `.`。[docker/buildx#1018](https://github.com/docker/buildx/issues/1018)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.8.1) 中的完整发行说明。

## 0.8.0

{{< release-date date="2022-03-09" >}}

### 新特性

- 构建命令现在接受 `--build-context` 标志，用以 [为您的构建定义额外的命名构建上下文](/reference/cli/docker/buildx/build/#build-context)。[docker/buildx#904](https://github.com/docker/buildx/issues/904)
- Bake 定义现在支持 [定义目标间的依赖关系](bake/contexts.md)，并支持在另一个构建中使用某个构建目标的结果。
  [docker/buildx#928](https://github.com/docker/buildx/issues/928),
  [docker/buildx#965](https://github.com/docker/buildx/issues/965),
  [docker/buildx#963](https://github.com/docker/buildx/issues/963),
  [docker/buildx#962](https://github.com/docker/buildx/issues/962),
  [docker/buildx#981](https://github.com/docker/buildx/issues/981)
- `imagetools inspect` 现在接受 `--format` 标志，允许访问特定镜像的配置和构建信息 (buildinfo)。[docker/buildx#854](https://github.com/docker/buildx/issues/854), [docker/buildx#972](https://github.com/docker/buildx/issues/972)
- 增加了新的标志 `--no-cache-filter`，允许配置构建任务，使其仅忽略指定 Dockerfile 阶段的缓存。[docker/buildx#860](https://github.com/docker/buildx/issues/860)
- 构建任务现在可以显示由构建前端设置的警告摘要。[docker/buildx#892](https://github.com/docker/buildx/issues/892)
- 新的构建参数 `BUILDKIT_INLINE_BUILDINFO_ATTRS` 允许选择将构建属性嵌入到生成的镜像中。[docker/buildx#908](https://github.com/docker/buildx/issues/908)
- 新标志 `--keep-buildkitd` 允许在移除构建器时保持 BuildKit 守护进程运行。
  - [docker/buildx#852](https://github.com/docker/buildx/issues/852)

### 错误修复与增强

- `--metadata-file` 的输出现在支持嵌入式结构类型。[docker/buildx#946](https://github.com/docker/buildx/issues/946)
- `buildx rm` 现在接受新标志 `--all-inactive`，用以移除所有当前未运行的构建器。[docker/buildx#885](https://github.com/docker/buildx/issues/885)
- 为了向后兼容，现在会从 Docker 配置文件中读取代理配置并随构建请求一同发送。[docker/buildx#959](https://github.com/docker/buildx/issues/959)
- 支持 Compose 中的宿主机网络。[docker/buildx#905](https://github.com/docker/buildx/issues/905), [docker/buildx#880](https://github.com/docker/buildx/issues/880)
- Bake 文件现在支持通过 `-f -` 从标准输入读取。[docker/buildx#864](https://github.com/docker/buildx/issues/864)
- `--iidfile` 现在总是写入镜像配置的 digest，这与所使用的驱动程序无关（使用 `--metadata-file` 获取 digest）。[docker/buildx#980](https://github.com/docker/buildx/issues/980)
- 限制了 Bake 中的目标名称，禁止使用特殊字符。[docker/buildx#929](https://github.com/docker/buildx/issues/929)
- 使用 `docker` 驱动程序推送时，可以从元数据中读取镜像清单的 digest。[docker/buildx#989](https://github.com/docker/buildx/issues/989)
- 修复了 Compose 文件中环境文件的处理问题。[docker/buildx#905](https://github.com/docker/buildx/issues/905)
- 在 `du` 命令中显示最后访问时间。[docker/buildx#867](https://github.com/docker/buildx/issues/867)
- 修复了多个 Bake 目标运行相同构建步骤时可能出现的重复输出日志问题。[docker/buildx#977](https://github.com/docker/buildx/issues/977)
- 修复了多节点构建器在构建混合平台的多个目标时可能出现的错误。[docker/buildx#985](https://github.com/docker/buildx/issues/985)
- 修复了 Bake 中某些嵌套继承的情况。[docker/buildx#914](https://github.com/docker/buildx/issues/914)
- 修复了打印 Bake 文件中默认组的问题。[docker/buildx#884](https://github.com/docker/buildx/issues/884)
- 修复了使用 rootless 容器时的 `UsernsMode` 问题。[docker/buildx#887](https://github.com/docker/buildx/issues/887)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.8.0) 中的完整发行说明。

## 0.7.1

{{< release-date date="2021-08-25" >}}

### 修复

- 修复了匹配 `.dockerignore` 中排除规则的问题。[docker/buildx#858](https://github.com/docker/buildx/issues/858)
- 修复了当前组的 `bake --print` JSON 输出。[docker/buildx#857](https://github.com/docker/buildx/issues/857)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.7.1) 中的完整发行说明。

## 0.7.0

{{< release-date date="2021-11-10" >}}

### 新特性

- 对于 `docker-container` 和 `kubernetes` 驱动程序，BuildKit 配置中的 TLS 证书现在会被传输到构建容器中。[docker/buildx#787](https://github.com/docker/buildx/issues/787)
- 构建命令支持 `--ulimit` 标志，以实现功能对等。[docker/buildx#800](https://github.com/docker/buildx/issues/800)
- 构建命令支持 `--shm-size` 标志，以实现功能对等。[docker/buildx#790](https://github.com/docker/buildx/issues/790)
- 构建命令支持 `--quiet`，以实现功能对等。[docker/buildx#740](https://github.com/docker/buildx/issues/740)
- 构建命令支持 `--cgroup-parent` 标志，以实现功能对等。[docker/buildx#814](https://github.com/docker/buildx/issues/814)
- Bake 支持内置变量 `BAKE_LOCAL_PLATFORM`。[docker/buildx#748](https://github.com/docker/buildx/issues/748)
- Bake 支持 Compose 文件中的 `x-bake` 扩展字段。[docker/buildx#721](https://github.com/docker/buildx/issues/721)
- `kubernetes` 驱动程序现在支持以冒号分隔的 `KUBECONFIG`。[docker/buildx#761](https://github.com/docker/buildx/issues/761)
- `kubernetes` 驱动程序现在支持通过 `--config` 设置 Buildkit 配置文件。[docker/buildx#682](https://github.com/docker/buildx/issues/682)
- `kubernetes` 驱动程序现在支持通过 driver-opt 安装 QEMU 模拟器。[docker/buildx#682](https://github.com/docker/buildx/issues/682)

### 增强功能

- 允许从客户端为多节点推送使用自定义注册表配置。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- 允许为 `buildx imagetools` 命令使用自定义注册表配置。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- 允许在通过 `buildx create --bootstrap` 创建后引导构建器。[docker/buildx#692](https://github.com/docker/buildx/issues/692)
- 为多节点推送允许 `registry:insecure` 输出选项。[docker/buildx#825](https://github.com/docker/buildx/issues/825)
- BuildKit 配置和 TLS 文件现在保留在 Buildx 状态目录中，并在 BuildKit 实例需要重新创建时复用。[docker/buildx#824](https://github.com/docker/buildx/issues/824)
- 确保不同项目为增量上下文传输使用独立的目录，以获得更好的性能。[docker/buildx#817](https://github.com/docker/buildx/issues/817)
- 构建容器现在默认放置在独立的 cgroup 中。[docker/buildx#782](https://github.com/docker/buildx/issues/782)
- Bake 现在使用 `--print` 打印默认组。[docker/buildx#720](https://github.com/docker/buildx/issues/720)
- `docker` 驱动程序现在通过 HTTP 拨号构建会话，以获得更好的性能。[docker/buildx#804](https://github.com/docker/buildx/issues/804)

### 修复

- 修复了 `--iidfile` 与多节点推送一同使用的问题。[docker/buildx#826](https://github.com/docker/buildx/issues/826)
- 在 Bake 中使用 `--push` 不会清除文件中的其他镜像导出选项。[docker/buildx#773](https://github.com/docker/buildx/issues/773)
- 修复了使用 `https` 协议时 `buildx bake` 的 Git URL 检测问题。[docker/buildx#822](https://github.com/docker/buildx/issues/822)
- 修复了多节点构建中推送具有多个名称的镜像的问题。[docker/buildx#815](https://github.com/docker/buildx/issues/815)
- 避免为不使用 `--builder` 标志的命令显示该标志。[docker/buildx#818](https://github.com/docker/buildx/issues/818)
- 不受支持的构建标志现在会显示警告。[docker/buildx#810](https://github.com/docker/buildx/issues/810)
- 修复了某些 OpenTelemetry 追踪中报告的错误详情。[docker/buildx#812](https://github.com/docker/buildx/issues/812)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.7.0) 中的完整发行说明。

## 0.6.3

{{< release-date date="2021-08-30" >}}

### 修复

- 修复了 Windows 客户端上 BuildKit 状态卷的位置。[docker/buildx#751](https://github.com/docker/buildx/issues/751)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.3) 中的完整发行说明。

## 0.6.2

{{< release-date date="2021-08-21" >}}

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.2) 中的完整发行说明。

### 修复

- 修复了某些 SSH 配置中显示的连接错误。[docker/buildx#741](https://github.com/docker/buildx/issues/741)

## 0.6.1

{{< release-date date="2021-07-30" >}}

### 增强功能

- 设置 `ConfigFile` 以便使用 Bake 解析 Compose 文件。[docker/buildx#704](https://github.com/docker/buildx/issues/704)

### 修复

- 重复的进度环境变量。[docker/buildx#693](https://github.com/docker/buildx/issues/693)
- 应忽略 nil 客户端。[docker/buildx#686](https://github.com/docker/buildx/issues/686)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.1) 中的完整发行说明。

## 0.6.0

{{< release-date date="2021-07-16" >}}

### 新特性

- 支持 OpenTelemetry 追踪，并支持将 Buildx 客户端追踪转发至 BuildKit。[docker/buildx#635](https://github.com/docker/buildx/issues/635)
- 增加了实验性的 GitHub Actions 远程缓存后端，使用 `--cache-to type=gha` 和 `--cache-from type=gha`。[docker/buildx#535](https://github.com/docker/buildx/issues/535)
- 为构建 (build) 和 Bake 命令增加了新的 `--metadata-file` 标志，允许以 JSON 格式保存构建结果元数据。[docker/buildx#605](https://github.com/docker/buildx/issues/605)
- 这是首个支持 Windows ARM64 的版本。[docker/buildx#654](https://github.com/docker/buildx/issues/654)
- 这是首个支持 Linux RISC-V 的版本。[docker/buildx#652](https://github.com/docker/buildx/issues/652)
- Bake 现在支持以本地文件或其他远程源作为上下文从远程定义进行构建。[docker/buildx#671](https://github.com/docker/buildx/issues/671)
- Bake 现在允许变量相互引用，并在变量中使用用户函数，反之亦然。
  [docker/buildx#575](https://github.com/docker/buildx/issues/575),
  [docker/buildx#539](https://github.com/docker/buildx/issues/539),
  [docker/buildx#532](https://github.com/docker/buildx/issues/532)
- Bake 允许在全局作用域定义属性。[docker/buildx#541](https://github.com/docker/buildx/issues/541)
- Bake 允许跨多个文件使用变量。[docker/buildx#538](https://github.com/docker/buildx/issues/538)
- 进度打印器增加了新的 quiet 模式。[docker/buildx#558](https://github.com/docker/buildx/issues/558)
- `kubernetes` 驱动程序现在支持定义资源/限制。[docker/buildx#618](https://github.com/docker/buildx/issues/618)
- Buildx 二进制文件现在可以通过 [buildx-bin](https://hub.docker.com/r/docker/buildx-bin) Docker 镜像访问。[docker/buildx#656](https://github.com/docker/buildx/issues/656)

### 增强功能

- `docker-container` 驱动程序现在将 BuildKit 状态保留在卷中。支持在保留状态的情况下进行更新。[docker/buildx#672](https://github.com/docker/buildx/issues/672)
- Compose 解析器现在基于全新的 [compose-go 解析器](https://github.com/compose-spec/compose-go)，修复了对某些新语法的支持。[docker/buildx#669](https://github.com/docker/buildx/issues/669)
- 当构建基于 SSH 的 Git URL 时，现在会自动转发 SSH 套接字。[docker/buildx#581](https://github.com/docker/buildx/issues/581)
- 重写了 Bake HCL 解析器。[docker/buildx#645](https://github.com/docker/buildx/issues/645)
- 扩展了 HCL 支持，增加了更多函数。[docker/buildx#491](https://github.com/docker/buildx/issues/491) [docker/buildx#503](https://github.com/docker/buildx/issues/503)
- 允许从环境变量中获取机密 (Secrets)。[docker/buildx#488](https://github.com/docker/buildx/issues/488)
- 对于不支持的多平台和加载 (load) 配置构建，现在会快速失败。[docker/buildx#582](https://github.com/docker/buildx/issues/582)
- 存储 Kubernetes 配置文件，使 buildx 构建器可切换。[docker/buildx#497](https://github.com/docker/buildx/issues/497)
- Kubernetes 现在在检查时将所有 pod 列为节点。[docker/buildx#477](https://github.com/docker/buildx/issues/477)
- 默认 Rootless 镜像已设置为 `moby/buildkit:buildx-stable-1-rootless`。[docker/buildx#480](https://github.com/docker/buildx/issues/480)

### 修复

- `imagetools create` 命令现在能正确将 JSON 描述符与旧的合并。[docker/buildx#592](https://github.com/docker/buildx/issues/592)
- 修复了使用 `--network=none` 构建时不需要额外安全授权的问题。[docker/buildx#531](https://github.com/docker/buildx/issues/531)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.6.0) 中的完整发行说明。

## 0.5.1

{{< release-date date="2020-12-15" >}}

### 修复

- 修复了在 `kubernetes` 驱动程序之外对 `buildx create` 设置 `--platform` 的回归问题。[docker/buildx#475](https://github.com/docker/buildx/issues/475)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.5.1) 中的完整发行说明。

## 0.5.0

{{< release-date date="2020-12-15" >}}

### 新特性

- `docker` 驱动程序现在支持 `--push` 标志。[docker/buildx#442](https://github.com/docker/buildx/issues/442)
- Bake 支持内联 Dockerfile。[docker/buildx#398](https://github.com/docker/buildx/issues/398)
- Bake 支持从远程 URL 和 Git 存储库构建。[docker/buildx#398](https://github.com/docker/buildx/issues/398)
- `BUILDX_CONFIG` 环境变量允许用户将 Buildx 状态与 Docker 配置分离。[docker/buildx#385](https://github.com/docker/buildx/issues/385)
- `BUILDKIT_MULTI_PLATFORM` 构建参数允许即便只指定了一个 `--platform`，也强制构建多平台返回对象。[docker/buildx#467](https://github.com/docker/buildx/issues/467)

### 增强功能

- 允许为 `kubernetes` 驱动程序使用 `--append` 参数。[docker/buildx#370](https://github.com/docker/buildx/issues/370)
- 构建错误会显示源码中的错误位置，使用 `--debug` 时会显示系统堆栈追踪。[docker/buildx#389](https://github.com/docker/buildx/issues/389)
- Bake 会根据源码定义格式化 HCL 错误信息。[docker/buildx#391](https://github.com/docker/buildx/issues/391)
- Bake 允许在数组中使用空字符串值（这些值将被丢弃）。[docker/buildx#428](https://github.com/docker/buildx/issues/428)
- 您现在可以为 `kubernetes` 驱动程序使用 Kubernetes 集群配置。[docker/buildx#368](https://github.com/docker/buildx/issues/368) [docker/buildx#460](https://github.com/docker/buildx/issues/460)
- 在可能的情况下，为拉取镜像创建临时令牌而不是共享凭据。[docker/buildx#469](https://github.com/docker/buildx/issues/469)
- 确保在拉取 BuildKit 容器镜像时传递凭据。[docker/buildx#441](https://github.com/docker/buildx/issues/441) [docker/buildx#433](https://github.com/docker/buildx/issues/433)
- 在 `docker-container` 驱动程序中禁用用户命名空间重映射。[docker/buildx#462](https://github.com/docker/buildx/issues/462)
- 允许使用 `--builder` 标志切换到默认实例。[docker/buildx#425](https://github.com/docker/buildx/issues/425)
- 避免对空的 `BUILDX_NO_DEFAULT_LOAD` 配置值发出警告。[docker/buildx#390](https://github.com/docker/buildx/issues/390)
- 将 `quiet` 选项产生的错误替换为警告。[docker/buildx#403](https://github.com/docker/buildx/issues/403)
- CI 已切换至 GitHub Actions。
  [docker/buildx#451](https://github.com/docker/buildx/issues/451),
  [docker/buildx#463](https://github.com/docker/buildx/issues/463),
  [docker/buildx#466](https://github.com/docker/buildx/issues/466),
  [docker/buildx#468](https://github.com/docker/buildx/issues/468),
  [docker/buildx#471](https://github.com/docker/buildx/issues/471)

### 修复

- 为了向后兼容，在找不到 Dockerfile 时尝试使用全小写的文件名作为回退。[docker/buildx#444](https://github.com/docker/buildx/issues/444)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.5.0) 中的完整发行说明。

## 0.4.2

{{< release-date date="2020-08-22" >}}

### 新特性

- 支持 `cacheonly` 导出器。[docker/buildx#337](https://github.com/docker/buildx/issues/337)

### 增强功能

- 更新了 `go-cty` 以引入更多 `stdlib` 函数。[docker/buildx#277](https://github.com/docker/buildx/issues/277)
- 优化了加载时的错误检查。[docker/buildx#281](https://github.com/docker/buildx/issues/281)

### 修复

- 修复了使用 HCL 解析 JSON 配置的问题。[docker/buildx#280](https://github.com/docker/buildx/issues/280)
- 确保从根选项接入 `--builder` 标志。[docker/buildx#321](https://github.com/docker/buildx/issues/321)
- 移除了针对多平台 iidfile 的警告。[docker/buildx#351](https://github.com/docker/buildx/issues/351)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.4.2) 中的完整发行说明。

## 0.4.1

{{< release-date date="2020-05-01" >}}

### 修复

- 修复了标志解析的回归问题。[docker/buildx#268](https://github.com/docker/buildx/issues/268)
- 修复了在 HCL 目标中使用 pull 和 no-cache 键的问题。[docker/buildx#268](https://github.com/docker/buildx/issues/268)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.4.1) 中的完整发行说明。

## 0.4.0

{{< release-date date="2020-04-30" >}}

### 新特性

- 增加了 `kubernetes` 驱动程序。[docker/buildx#167](https://github.com/docker/buildx/issues/167)
- 增加了全局 `--builder` 标志，可为单个命令覆盖构建器实例。[docker/buildx#246](https://github.com/docker/buildx/issues/246)
- 增加了用于管理本地构建器缓存的新命令 `prune` 和 `du`。[docker/buildx#249](https://github.com/docker/buildx/issues/249)
- 您现在可以为 HCL 目标设置新的 `pull` 和 `no-cache` 选项。[docker/buildx#165](https://github.com/docker/buildx/issues/165)

### 增强功能

- 将 Bake 升级至 HCL2，支持变量和函数。[docker/buildx#192](https://github.com/docker/buildx/issues/192)
- Bake 现在支持 `--load` 和 `--push`。[docker/buildx#164](https://github.com/docker/buildx/issues/164)
- Bake 现在支持多个目标的通配符覆盖。[docker/buildx#164](https://github.com/docker/buildx/issues/164)
- 容器驱动程序允许通过 `driver-opt` 设置环境变量。[docker/buildx#170](https://github.com/docker/buildx/issues/170)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.4.0) 中的完整发行说明。

## 0.3.1

{{< release-date date="2019-09-27" >}}

### 增强功能

- 实现了对 Unix 套接字拷贝的处理而非报错。[docker/buildx#155](https://github.com/docker/buildx/issues/155) [moby/buildkit#1144](https://github.com/moby/buildkit/issues/1144)

### 修复

- 修复了运行带多个 Compose 文件的 Bake 时未能正确合并目标的问题。[docker/buildx#134](https://github.com/docker/buildx/issues/134)
- 修复了从标准输入构建 Dockerfile (`build -f -`) 时的 Bug。[docker/buildx#153](https://github.com/docker/buildx/issues/153)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.3.1) 中的完整发行说明。

## 0.3.0

{{< release-date date="2019-08-02" >}}

### 新特性

- 支持自定义 `buildkitd` 守护进程标志。[docker/buildx#102](https://github.com/docker/buildx/issues/102)
- 为 `create` 命令增加了驱动特定的选项。[docker/buildx#122](https://github.com/docker/buildx/issues/122)

### 增强功能

- Compose 文件支持使用环境变量。[docker/buildx#117](https://github.com/docker/buildx/issues/117)
- Bake 现在遵循 `--no-cache` 和 `--pull` 标志。[docker/buildx#118](https://github.com/docker/buildx/issues/118)
- 支持自定义 BuildKit 配置文件。[docker/buildx#121](https://github.com/docker/buildx/issues/121)
- 支持带 `build --allow` 的权限授权功能。[docker/buildx#104](https://github.com/docker/buildx/issues/104)

### 修复

- 修复了 `--build-arg foo` 未能从环境中读取 `foo` 变量的 Bug。[docker/buildx#116](https://github.com/docker/buildx/issues/116)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.3.0) 中的完整发行说明。

## 0.2.2

{{< release-date date="2019-05-30" >}}

### 增强功能

- 更改了 Compose 文件处理逻辑，现在要求提供有效的服务规范。[docker/buildx#87](https://github.com/docker/buildx/issues/87)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.2.2) 中的完整发行说明。

## 0.2.1

{{< release-date date="2019-05-25" >}}

### 新特性

- 增加了 `BUILDKIT_PROGRESS` 环境变量。[docker/buildx#69](https://github.com/docker/buildx/issues/69)
- 增加了 `local` 平台支持。[docker/buildx#70](https://github.com/docker/buildx/issues/70)

### 增强功能

- 如果配置中定义了 ARM 变体，则予以保留。[docker/buildx#68](https://github.com/docker/buildx/issues/68)
- 使 Dockerfile 路径相对于上下文。[docker/buildx#83](https://github.com/docker/buildx/issues/83)

### 修复

- 修复了从 Compose 文件解析目标的问题。[docker/buildx#53](https://github.com/docker/buildx/issues/53)

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.2.1) 中的完整发行说明。

## 0.2.0

{{< release-date date="2019-04-25" >}}

### 新特性

- 首个发布版本。

更多详情请参阅 [Buildx GitHub 仓库](https://github.com/docker/buildx/releases/tag/v0.2.0) 中的完整发行说明。