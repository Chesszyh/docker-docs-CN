---
title: Dockerfile 发行说明
description: Dockerfile 前端的发行说明
keywords: build, dockerfile, frontend, release notes
tags: [Release notes]
toc_max: 2
aliases:
  - /build/dockerfile/release-notes/
---

本页包含有关 [Dockerfile 参考](/reference/dockerfile.md)中新功能、改进、
已知问题和错误修复的信息。

有关用法，请参阅 [Dockerfile 前端语法](frontend.md)页面。

## 1.16.0

{{< release-date date="2025-05-22" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.16.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.16.0
```

* `ADD --checksum` 支持 Git URL。[moby/buildkit#5975](https://github.com/moby/buildkit/pull/5975)
* 允许在 heredocs 中使用空白字符。[moby/buildkit#5817](https://github.com/moby/buildkit/pull/5817)
* `WORKDIR` 现在支持 `SOURCE_DATE_EPOCH`。[moby/buildkit#5960](https://github.com/moby/buildkit/pull/5960)
* 对于 WCOW，保留基础镜像设置的默认 PATH 环境变量。[moby/buildkit#5895](https://github.com/moby/buildkit/pull/5895)

## 1.15.1

{{< release-date date="2025-03-30" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.15.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.15.1
```

* 修复使用 `--attest type=sbom` 时出现的 `no scan targets for linux/arm64/v8` 问题。[moby/buildkit#5941](https://github.com/moby/buildkit/pull/5941)

## 1.15.0

{{< release-date date="2025-04-15" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.15.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.15.0
```

- 无效目标的构建错误现在会显示正确可能名称的建议。[moby/buildkit#5851](https://github.com/moby/buildkit/pull/5851)
- 修复 Windows 目标的 SBOM 证明产生错误的问题。[moby/buildkit#5837](https://github.com/moby/buildkit/pull/5837)
- 修复递归 `ARG` 在处理 outline 请求时产生无限循环的问题。[moby/buildkit#5823](https://github.com/moby/buildkit/pull/5823)
- 修复从 JSON 解析语法指令时，如果 JSON 包含字符串以外的其他数据类型会失败的问题。[moby/buildkit#5815](https://github.com/moby/buildkit/pull/5815)
- 修复镜像配置中的平台格式未规范化的问题（1.12 版本的回归）。[moby/buildkit#5776](https://github.com/moby/buildkit/pull/5776)
- 修复在 WCOW 中当目录不存在时复制到目标目录的问题。[moby/buildkit#5249](https://github.com/moby/buildkit/pull/5249)

## 1.14.1

{{< release-date date="2025-03-05" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.14.1
```

- 规范化镜像配置中的平台格式。[moby/buildkit#5776](https://github.com/moby/buildkit/pull/5776)

## 1.14.0

{{< release-date date="2025-02-19" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.14.0
```

- `COPY --chmod` 现在允许非八进制值。此功能之前在 labs 通道中，现在在主发布版本中可用。[moby/buildkit#5734](https://github.com/moby/buildkit/pull/5734)
- 修复当基础镜像设置了 OSVersion 平台属性时的处理问题 [moby/buildkit#5714](https://github.com/moby/buildkit/pull/5714)
- 修复命名上下文元数据即使当前构建配置无法访问也可能被解析的错误，导致构建错误 [moby/buildkit#5688](https://github.com/moby/buildkit/pull/5688)

## 1.14.0 (labs)

{{< release-date date="2025-02-19" >}}

{{% include "dockerfile-labs-channel.md" %}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.0-labs) 上获取。

```dockerfile
# syntax=docker.io/docker/dockerfile-upstream:1.14.0-labs
```

- 新的 `RUN --device=name,[required]` 标志允许构建请求 CDI 设备在构建步骤中可用。需要 BuildKit v0.20.0+ [moby/buildkit#4056](https://github.com/moby/buildkit/pull/4056)、[moby/buildkit#5738](https://github.com/moby/buildkit/pull/5738)

## 1.13.0

{{< release-date date="2025-01-20" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.13.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.13.0
```

- 新的 `TARGETOSVERSION`、`BUILDOSVERSION` 内置构建参数可用于 Windows 构建，`TARGETPLATFORM` 值现在也包含 `OSVersion` 值。[moby/buildkit#5614](https://github.com/moby/buildkit/pull/5614)
- 允许对以字节顺序标记（BOM）开头的文件进行外部前端的语法转发。[moby/buildkit#5645](https://github.com/moby/buildkit/pull/5645)
- Windows 容器中的默认 `PATH` 已更新，添加了 `powershell.exe` 目录。[moby/buildkit#5446](https://github.com/moby/buildkit/pull/5446)
- 修复 Dockerfile 指令解析以不允许无效语法。[moby/buildkit#5646](https://github.com/moby/buildkit/pull/5646)
- 修复 `ONBUILD` 命令可能在继承的阶段上运行两次的情况。[moby/buildkit#5593](https://github.com/moby/buildkit/pull/5593)
- 修复 Dockerfile 中子阶段可能缺少命名上下文替换的问题。[moby/buildkit#5596](https://github.com/moby/buildkit/pull/5596)

## 1.13.0 (labs)

{{< release-date date="2025-01-20" >}}

{{% include "dockerfile-labs-channel.md" %}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.13.0-labs) 上获取。

```dockerfile
# syntax=docker.io/docker/dockerfile-upstream:1.13.0-labs
```

- 修复对 `COPY --chmod` 非八进制值的支持。[moby/buildkit#5626](https://github.com/moby/buildkit/pull/5626)

## 1.12.0

{{< release-date date="2024-11-27" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.12.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.12.0
```

- 修复多个 `ARG` 指令的镜像配置 History 行中描述不正确的问题。[moby/buildkit#5508]

[moby/buildkit#5508]: https://github.com/moby/buildkit/pull/5508

## 1.11.1

{{< release-date date="2024-11-08" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.11.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.11.1
```

- 修复在同一 Dockerfile 中继承的阶段使用 `ONBUILD` 指令时的回归问题。[moby/buildkit#5490]

[moby/buildkit#5490]: https://github.com/moby/buildkit/pull/5490

## 1.11.0

{{< release-date date="2024-10-30" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.11.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.11.0
```

- [`ONBUILD` 指令](/reference/dockerfile.md#onbuild)现在支持使用 `from` 引用其他阶段或镜像的命令，例如 `COPY --from` 或 `RUN mount=from=...`。[moby/buildkit#5357]
- [`SecretsUsedInArgOrEnv`](/reference/build-checks/secrets-used-in-arg-or-env.md) 构建检查已改进以减少误报。[moby/buildkit#5208]
- 新的 [`InvalidDefinitionDescription`](/reference/build-checks/invalid-definition-description.md) 构建检查建议格式化构建参数和阶段描述的注释。这是一个[实验性检查](/manuals/build/checks.md#experimental-checks)。[moby/buildkit#5208]、[moby/buildkit#5414]
- 多个 `ONBUILD` 指令的进度和错误处理修复。[moby/buildkit#5397]
- 改进了缺少标志错误的错误报告。[moby/buildkit#5369]
- 增强了作为环境变量挂载的密钥值的进度输出。[moby/buildkit#5336]
- 添加了内置构建参数 `TARGETSTAGE` 以公开当前构建的（最终）目标阶段的名称。[moby/buildkit#5431]

## 1.11.0 (labs)

{{% include "dockerfile-labs-channel.md" %}}

- `COPY --chmod` 现在支持非八进制值。[moby/buildkit#5380]

[moby/buildkit#5357]: https://github.com/moby/buildkit/pull/5357
[moby/buildkit#5208]: https://github.com/moby/buildkit/pull/5208
[moby/buildkit#5414]: https://github.com/moby/buildkit/pull/5414
[moby/buildkit#5397]: https://github.com/moby/buildkit/pull/5397
[moby/buildkit#5369]: https://github.com/moby/buildkit/pull/5369
[moby/buildkit#5336]: https://github.com/moby/buildkit/pull/5336
[moby/buildkit#5431]: https://github.com/moby/buildkit/pull/5431
[moby/buildkit#5380]: https://github.com/moby/buildkit/pull/5380

## 1.10.0

{{< release-date date="2024-09-10" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.10.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.10.0
```

- [构建密钥](/manuals/build/building/secrets.md#target)现在可以使用 `env=VARIABLE` 选项作为环境变量挂载。[moby/buildkit#5215]
- [`# check` 指令](/reference/dockerfile.md#check)现在允许新的 experimental 属性以启用实验性验证规则，如 `CopyIgnoredFile`。[moby/buildkit#5213]
- 改进了变量替换不支持的修饰符的验证。[moby/buildkit#5146]
- `ADD` 和 `COPY` 指令现在支持 `--chmod` 选项值的构建参数变量插值。[moby/buildkit#5151]
- 改进了 `COPY` 和 `ADD` 指令的 `--chmod` 选项的验证。[moby/buildkit#5148]
- 修复了挂载的 size 和 destination 属性缺少补全的问题。[moby/buildkit#5245]
- OCI 注解现在已设置到 Dockerfile 前端发布镜像。[moby/buildkit#5197]

[moby/buildkit#5215]: https://github.com/moby/buildkit/pull/5215
[moby/buildkit#5213]: https://github.com/moby/buildkit/pull/5213
[moby/buildkit#5146]: https://github.com/moby/buildkit/pull/5146
[moby/buildkit#5151]: https://github.com/moby/buildkit/pull/5151
[moby/buildkit#5148]: https://github.com/moby/buildkit/pull/5148
[moby/buildkit#5245]: https://github.com/moby/buildkit/pull/5245
[moby/buildkit#5197]: https://github.com/moby/buildkit/pull/5197

## 1.9.0

{{< release-date date="2024-07-11" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.9.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.9.0
```

- 添加新的验证规则：
  - `SecretsUsedInArgOrEnv`
  - `InvalidDefaultArgInFrom`
  - `RedundantTargetPlatform`
  - `CopyIgnoredFile`（实验性）
  - `FromPlatformFlagConstDisallowed`
- 处理大型 Dockerfile 的多项性能改进。[moby/buildkit#5067](https://github.com/moby/buildkit/pull/5067/)、[moby/buildkit#5029](https://github.com/moby/buildkit/pull/5029/)
- 修复构建没有定义阶段的 Dockerfile 时可能出现的 panic。[moby/buildkit#5150](https://github.com/moby/buildkit/pull/5150/)
- 修复不正确的 JSON 解析，该问题可能导致某些不正确的 JSON 值通过而不产生错误。[moby/buildkit#5107](https://github.com/moby/buildkit/pull/5107/)
- 修复 `COPY --link` 目标路径为 `.` 时可能失败的回归问题。[moby/buildkit#5080](https://github.com/moby/buildkit/pull/5080/)
- 修复与 Git URL 一起使用 `ADD --checksum` 时的验证问题。[moby/buildkit#5085](https://github.com/moby/buildkit/pull/5085/)

## 1.8.1

{{< release-date date="2024-06-18" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.8.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.8.1
```

### 错误修复和增强

- 修复变量展开时空字符串的处理。[moby/buildkit#5052](https://github.com/moby/buildkit/pull/5052/)
- 改进构建警告的格式化。[moby/buildkit#5037](https://github.com/moby/buildkit/pull/5037/)、[moby/buildkit#5045](https://github.com/moby/buildkit/pull/5045/)、[moby/buildkit#5046](https://github.com/moby/buildkit/pull/5046/)
- 修复多阶段构建中 `UndeclaredVariable` 警告可能产生无效输出的问题。[moby/buildkit#5048](https://github.com/moby/buildkit/pull/5048/)

## 1.8.0

{{< release-date date="2024-06-11" >}}

此版本的完整发行说明可在
[GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.8.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.8.0
```

- 添加了许多新的验证规则来验证您的 Dockerfile 是否使用最佳实践。这些规则在构建期间进行验证，新的 `check` 前端方法可用于仅触发验证而不完成整个构建。
- 新的 `#check` 指令和构建参数 `BUILDKIT_DOCKERFILE_CHECK` 允许您控制构建检查的行为。[moby/buildkit#4962](https://github.com/moby/buildkit/pull/4962/)
- 现在会验证使用与预期平台不匹配的单平台基础镜像。[moby/buildkit#4924](https://github.com/moby/buildkit/pull/4924/)
- 现在正确处理全局范围内 `ARG` 定义展开的错误。[moby/buildkit#4856](https://github.com/moby/buildkit/pull/4856/)
- `ARG` 默认值的展开现在只在用户未覆盖时发生。之前，展开会完成但值随后被忽略，这可能导致意外的展开错误。[moby/buildkit#4856](https://github.com/moby/buildkit/pull/4856/)
- 改进了解析具有多个阶段的大型 Dockerfile 的性能。[moby/buildkit#4970](https://github.com/moby/buildkit/pull/4970/)
- 修复了一些 Windows 路径处理一致性错误。[moby/buildkit#4825](https://github.com/moby/buildkit/pull/4825/)

## 1.7.0

{{< release-date date="2024-03-06" >}}

### Stable

```dockerfile
# syntax=docker/dockerfile:1.7
```

- 变量展开现在支持字符串替换和修剪。
  [moby/buildkit#4427](https://github.com/moby/buildkit/pull/4427)、
  [moby/buildkit#4287](https://github.com/moby/buildkit/pull/4287)
- 具有本地源的命名上下文现在正确地只传输 Dockerfile 中使用的文件，而不是完整的源目录。
  [moby/buildkit#4161](https://github.com/moby/buildkit/pull/4161)
- Dockerfile 现在更好地验证阶段的顺序，如果阶段顺序不正确，会返回带有堆栈跟踪的友好错误。
  [moby/buildkit#4568](https://github.com/moby/buildkit/pull/4568)、
  [moby/buildkit#4567](https://github.com/moby/buildkit/pull/4567)
- History 提交消息现在包含与 `COPY` 和 `ADD` 一起使用的标志。
  [moby/buildkit#4597](https://github.com/moby/buildkit/pull/4597)
- 改进了来自 Git 和 HTTP 源的 `ADD` 命令的进度消息。
  [moby/buildkit#4408](https://github.com/moby/buildkit/pull/4408)

### Labs

```dockerfile
# syntax=docker/dockerfile:1.7-labs
```

- 为 `COPY` 添加了新的 `--parents` 标志，用于在保持父目录结构的同时复制文件。
  [moby/buildkit#4598](https://github.com/moby/buildkit/pull/4598)、
  [moby/buildkit#3001](https://github.com/moby/buildkit/pull/3001)、
  [moby/buildkit#4720](https://github.com/moby/buildkit/pull/4720)、
  [moby/buildkit#4728](https://github.com/moby/buildkit/pull/4728)、
  [docs](/reference/dockerfile.md#copy---parents)
- 新的 `--exclude` 标志可在 `COPY` 和 `ADD` 命令中用于对复制的文件应用过滤器。
  [moby/buildkit#4561](https://github.com/moby/buildkit/pull/4561)、
  [docs](/reference/dockerfile.md#copy---exclude)

## 1.6.0

{{< release-date date="2023-06-13" >}}

### 新功能

- 为 [`HEALTHCHECK` 指令](/reference/dockerfile.md#healthcheck)添加 `--start-interval` 标志。

以下功能已从 labs 通道毕业到 stable：

- `ADD` 指令现在可以[直接从 Git URL 导入文件](/reference/dockerfile.md#adding-a-git-repository-add-git-ref-dir)
- `ADD` 指令现在支持 [`--checksum` 标志](/reference/dockerfile.md#verifying-a-remote-file-checksum-add---checksumchecksum-http-src-dest)
  来验证远程 URL 内容

### 错误修复和增强

- 变量替换现在支持不带 `:` 的其他 POSIX 兼容变体。
  [moby/buildkit#3611](https://github.com/moby/buildkit/pull/3611)
- 导出的 Windows 镜像现在包含来自基础镜像的 OSVersion 和 OSFeatures 值。
  [moby/buildkit#3619](https://github.com/moby/buildkit/pull/3619)
- 将 Heredocs 的权限更改为 0644。
  [moby/buildkit#3992](https://github.com/moby/buildkit/pull/3992)

## 1.5.2

{{< release-date date="2023-02-14" >}}

### 错误修复和增强

- 修复从缺少分支名称但包含子目录的 Git 引用构建的问题
- 发布中现在包含 386 平台镜像

## 1.5.1

{{< release-date date="2023-01-18" >}}

### 错误修复和增强

- 修复多平台构建中出现警告条件时可能出现的 panic

## 1.5.0 (labs)

{{< release-date date="2023-01-10" >}}

{{% include "dockerfile-labs-channel.md" %}}

### 新功能

- `ADD` 命令现在支持 [`--checksum` 标志](/reference/dockerfile.md#verifying-a-remote-file-checksum-add---checksumchecksum-http-src-dest)
  来验证远程 URL 内容

## 1.5.0

{{< release-date date="2023-01-10" >}}

### 新功能

- `ADD` 命令现在可以[直接从 Git URL 导入文件](/reference/dockerfile.md#adding-a-git-repository-add-git-ref-dir)

### 错误修复和增强

- 命名上下文现在支持 `oci-layout://` 协议，用于从
  本地 OCI 布局结构包含镜像
- Dockerfile 现在支持辅助请求，用于列出所有构建目标或
  打印特定构建目标接受的参数概要
- 重定向到外部前端镜像的 Dockerfile `#syntax` 指令
  现在允许该指令也通过 `//` 注释或 JSON 设置。文件
  也可以包含 shebang 头
- 命名上下文现在可以用空的 scratch 镜像初始化
- 命名上下文现在可以用 SSH Git URL 初始化
- 修复导入 Schema1 镜像时 `ONBUILD` 的处理

## 1.4.3

{{< release-date date="2022-08-23" >}}

### 错误修复和增强

- 修复从 `docker-image://` 命名上下文构建镜像时创建时间戳未被重置的问题
- 修复加载 `docker-image://` 命名上下文时传递 `FROM` 命令的 `--platform` 标志

## 1.4.2

{{< release-date date="2022-05-06" >}}

### 错误修复和增强

- 修复从通过构建上下文传递的镜像加载某些环境变量的问题

## 1.4.1

{{< release-date date="2022-04-08" >}}

### 错误修复和增强

- 修复当输入为不同平台构建时，从输入进行交叉编译情况下的命名上下文解析

## 1.4.0

{{< release-date date="2022-03-09" >}}

### 新功能

- [`COPY --link` 和 `ADD --link`](/reference/dockerfile.md#copy---link)
  允许以更高的缓存效率复制文件并重新构建基础镜像而无需重建它们。`--link` 将文件复制到单独的层，然后使用新的 LLB MergeOp 实现将独立层链接在一起
- [Heredocs](/reference/dockerfile.md#here-documents) 支持已从 labs 通道
  升级到 stable。此功能允许编写
  多行内联脚本和文件
- 额外的[命名构建上下文](/reference/cli/docker/buildx/build.md#build-context)
  可以传递给构建以添加或覆盖构建中的阶段或镜像。上下文的源可以是本地源、镜像、Git 或 HTTP URL
- [`BUILDKIT_SANDBOX_HOSTNAME` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args)
  可用于设置 `RUN` 步骤的默认主机名

### 错误修复和增强

- 使用交叉编译阶段时，步骤的目标平台现在
  显示在进度输出中
- 修复了 Heredocs 错误删除内容中引号的某些情况

## 1.3.1

{{< release-date date="2021-10-04" >}}

### 错误修复和增强

- 修复解析没有值的 "required" 挂载键

## 1.3.0 (labs)

{{< release-date date="2021-07-16" >}}

{{% include "dockerfile-labs-channel.md" %}}

### 新功能

- `RUN` 和 `COPY` 命令现在支持 [Here-document 语法](/reference/dockerfile.md#here-documents)
  允许编写多行内联脚本和文件

## 1.3.0

{{< release-date date="2021-07-16" >}}

### 新功能

- `RUN` 命令允许 [`--network` 标志](/reference/dockerfile.md#run---network)
  用于请求特定类型的网络条件。`--network=host`
  需要允许 `network.host` 权限。此功能之前
  仅在 labs 通道中可用

### 错误修复和增强

- 带有远程 URL 输入的 `ADD` 命令现在正确处理 `--chmod` 标志
- [`RUN --mount` 标志](/reference/dockerfile.md#run---mount)
  的值现在支持变量展开，`from` 字段除外
- 允许 [`BUILDKIT_MULTI_PLATFORM` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args)
  强制始终创建多平台镜像，即使只包含单个
  平台

## 1.2.1 (labs)

{{< release-date date="2020-12-12" >}}

{{% include "dockerfile-labs-channel.md" %}}

### 错误修复和增强

- `RUN` 命令允许 [`--network` 标志](/reference/dockerfile.md#run---network)
  用于请求特定类型的网络条件。`--network=host`
  需要允许 `network.host` 权限

## 1.2.1

{{< release-date date="2020-12-12" >}}

### 错误修复和增强

- 撤销 "Ensure ENTRYPOINT command has at least one argument"
- 优化多平台交叉编译构建中 `COPY` 调用的处理

## 1.2.0 (labs)

{{< release-date date="2020-12-03" >}}

{{% include "dockerfile-labs-channel.md" %}}

### 错误修复和增强

- 实验性通道已重命名为 _labs_

## 1.2.0

{{< release-date date="2020-12-03" >}}

### 新功能

- 用于创建 secret、ssh、bind 和 cache 挂载的 [`RUN --mount` 语法](/reference/dockerfile.md#run---mount)已移至主线
  通道
- [`ARG` 命令](/reference/dockerfile.md#arg)现在支持在同一行上定义
  多个构建参数，类似于 `ENV`

### 错误修复和增强

- 元数据加载错误现在被视为致命错误，以避免不正确的构建结果
- 允许小写的 Dockerfile 名称
- `ADD` 中的 `--chown` 标志现在允许参数展开
- `ENTRYPOINT` 至少需要一个参数以避免创建损坏的镜像

## 1.1.7

{{< release-date date="2020-04-18" >}}

### 错误修复和增强

- 将 `FrontendInputs` 转发到网关

## 1.1.2 (labs)

{{< release-date date="2019-07-31" >}}

{{% include "dockerfile-labs-channel.md" %}}

### 错误修复和增强

- 允许使用 `RUN --security=sandbox|insecure` 为进程设置安全模式
- 允许为[缓存挂载](/reference/dockerfile.md#run---mounttypecache)设置 uid/gid
- 避免请求内部链接的路径被拉取到构建上下文
- 确保缺少的缓存 ID 默认为目标路径
- 允许使用 [`BUILDKIT_CACHE_MOUNT_NS` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args)为缓存挂载设置命名空间

## 1.1.2

{{< release-date date="2019-07-31" >}}

### 错误修复和增强

- 修复使用正确用户创建 workdir 且不重置自定义所有权
- 修复处理也用作 `ENV` 的空构建参数
- 检测循环依赖

## 1.1.0

{{< release-date date="2019-04-27" >}}

### 新功能

- `ADD/COPY` 命令现在支持基于 `llb.FileOp` 的实现，如果内置文件操作支持可用则不需要辅助镜像
- `COPY` 命令的 `--chown` 标志现在支持变量展开

### 错误修复和增强

- 为了查找从构建上下文中忽略的文件，Dockerfile 前端将
  首先查找文件 `<path/to/Dockerfile>.dockerignore`，如果未找到，
  则从构建上下文的根目录查找 `.dockerignore` 文件。这允许具有多个 Dockerfile 的项目使用不同的
  `.dockerignore` 定义
