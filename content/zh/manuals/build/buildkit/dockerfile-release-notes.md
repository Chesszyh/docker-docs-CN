---
title: Dockerfile 发行说明
description: Dockerfile 前端的发行说明
keywords: build, dockerfile, 前端, 发行说明
tags: [发行说明]
toc_max: 2
---

本页面包含 [Dockerfile 参考](/reference/dockerfile.md) 中的新特性、改进、已知问题和 Bug 修复信息。

有关用法，请参阅 [Dockerfile 前端语法](frontend.md) 页面。

## 1.16.0

{{< release-date date="2025-05-22" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.16.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.16.0
```

* `ADD --checksum` 支持 Git URL。[moby/buildkit#5975](https://github.com/moby/buildkit/pull/5975)
* 允许在 heredoc 中使用空白字符。[moby/buildkit#5817](https://github.com/moby/buildkit/pull/5817)
* `WORKDIR` 现在支持 `SOURCE_DATE_EPOCH`。[moby/buildkit#5960](https://github.com/moby/buildkit/pull/5960)
* 为 WCOW（Windows 容器）保留由基础镜像设置的默认 PATH 环境变量。[moby/buildkit#5895](https://github.com/moby/buildkit/pull/5895)

## 1.15.1

{{< release-date date="2025-03-30" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.15.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.15.1
```

* 修复了使用 `--attest type=sbom` 时出现的 `no scan targets for linux/arm64/v8` 错误。[moby/buildkit#5941](https://github.com/moby/buildkit/pull/5941)

## 1.15.0

{{< release-date date="2025-04-15" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.15.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.15.0
```

- 针对无效目标的构建错误现在会显示正确可能名称的建议。[moby/buildkit#5851](https://github.com/moby/buildkit/pull/5851)
- 修复了 Windows 目标产生 SBOM 证明错误的问题。[moby/buildkit#5837](https://github.com/moby/buildkit/pull/5837)
- 修复了在处理大纲（outline）请求时，递归 `ARG` 产生无限循环的问题。[moby/buildkit#5823](https://github.com/moby/buildkit/pull/5823)
- 修复了从 JSON 解析语法指令时，如果 JSON 包含字符串以外的其他数据类型会失败的问题。[moby/buildkit#5815](https://github.com/moby/buildkit/pull/5815)
- 修复了镜像配置中的平台处于非规范化形式的问题（1.12 的回归问题）。[moby/buildkit#5776](https://github.com/moby/buildkit/pull/5776)
- 修复了 WCOW 在目标目录不存在时进行复制的问题。[moby/buildkit#5249](https://github.com/moby/buildkit/pull/5249)

## 1.14.1

{{< release-date date="2025-03-05" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.14.1
```

- 规范化镜像配置中的平台。[moby/buildkit#5776](https://github.com/moby/buildkit/pull/5776)

## 1.14.0

{{< release-date date="2025-02-19" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.14.0
```

- `COPY --chmod` 现在允许非八进制值。此功能之前在 labs 频道中，现在已在主版本中提供。[moby/buildkit#5734](https://github.com/moby/buildkit/pull/5734)
- 修复了对基础镜像设置的 OSVersion 平台属性的处理。[moby/buildkit#5714](https://github.com/moby/buildkit/pull/5714)
- 修复了具名上下文元数据即使在当前构建配置无法访问时也能被解析，从而导致构建错误的问题。[moby/buildkit#5688](https://github.com/moby/buildkit/pull/5688)

## 1.14.0 (labs)

{{< release-date date="2025-02-19" >}}

{{% include "dockerfile-labs-channel.md" %}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.0-labs) 上获取。

```dockerfile
# syntax=docker.io/docker/dockerfile-upstream:1.14.0-labs
```

- 新的 `RUN --device=name,[required]` 标志允许构建请求在构建步骤中使用 CDI 设备。需要 BuildKit v0.20.0+ [moby/buildkit#4056](https://github.com/moby/buildkit/pull/4056), [moby/buildkit#5738](https://github.com/moby/buildkit/pull/5738)

## 1.13.0

{{< release-date date="2025-01-20" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.13.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.13.0
```

- 新的 `TARGETOSVERSION`、`BUILDOSVERSION` 内置构建参数可用于 Windows 构建，且 `TARGETPLATFORM` 的值现在也包含 `OSVersion` 值。[moby/buildkit#5614](https://github.com/moby/buildkit/pull/5614)
- 允许为以字节顺序标记 (BOM) 开头的文件转发外部前端语法。[moby/buildkit#5645](https://github.com/moby/buildkit/pull/5645)
- Windows 容器中的默认 `PATH` 已更新，加入了 `powershell.exe` 目录。[moby/buildkit#5446](https://github.com/moby/buildkit/pull/5446)
- 修复了 Dockerfile 指令解析，不允许无效语法。[moby/buildkit#5646](https://github.com/moby/buildkit/pull/5646)
- 修复了 `ONBUILD` 命令可能在继承阶段运行两次的问题。[moby/buildkit#5593](https://github.com/moby/buildkit/pull/5593)
- 修复了 Dockerfile 中子阶段可能缺失具名上下文替换的问题。[moby/buildkit#5596](https://github.com/moby/buildkit/pull/5596)

## 1.13.0 (labs)

{{< release-date date="2025-01-20" >}}

{{% include "dockerfile-labs-channel.md" %}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.13.0-labs) 上获取。

```dockerfile
# syntax=docker.io/docker/dockerfile-upstream:1.13.0-labs
```

- 修复了 `COPY --chmod` 对非八进制值的支持。[moby/buildkit#5626](https://github.com/moby/buildkit/pull/5626)

## 1.12.0

{{< release-date date="2024-11-27" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.12.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.12.0
```

- 修复了带有多个 `ARG` 指令的镜像配置的历史行中描述不正确的问题。[moby/buildkit#5508]

[moby/buildkit#5508]: https://github.com/moby/buildkit/pull/5508

## 1.11.1

{{< release-date date="2024-11-08" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.11.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.11.1
```

- 修复了在同一个 Dockerfile 内继承的阶段中使用 `ONBUILD` 指令时的回归问题。[moby/buildkit#5490]

[moby/buildkit#5490]: https://github.com/moby/buildkit/pull/5490

## 1.11.0

{{< release-date date="2024-10-30" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.11.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.11.0
```

- [`ONBUILD` 指令](/reference/dockerfile.md#onbuild) 现在支持使用 `from` 引用其他阶段或镜像的命令，例如 `COPY --from` 或 `RUN mount=from=...`。[moby/buildkit#5357]
- 改进了 [`SecretsUsedInArgOrEnv`](/reference/build-checks/secrets-used-in-arg-or-env.md) 构建检查，以减少误报。[moby/buildkit#5208]
- 新增的 [`InvalidDefinitionDescription`](/reference/build-checks/invalid-definition-description.md) 构建检查建议对构建参数和阶段描述的注释进行格式化。这是一项 [实验性检查](/manuals/build/checks.md#实验性检查)。[moby/buildkit#5208], [moby/buildkit#5414]
- 修复了多处 `ONBUILD` 指令的进度和错误处理问题。[moby/buildkit#5397]
- 改进了缺失标志错误时的错误报告。[moby/buildkit#5369]
- 增强了挂载为环境变量的密钥值的进度输出。[moby/buildkit#5336]
- 添加了内置构建参数 `TARGETSTAGE`，以暴露当前构建的（最终）目标阶段名称。[moby/buildkit#5431]

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

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.10.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.10.0
```

- [构建密钥](/manuals/build/building/secrets.md#目标) 现在可以使用 `env=VARIABLE` 选项挂载为环境变量。[moby/buildkit#5215]
- [`# check` 指令](/reference/dockerfile.md#check) 现在允许新的实验性属性，用于启用实验性验证规则，如 `CopyIgnoredFile`。[moby/buildkit#5213]
- 改进了变量替换中不支持的修饰符的验证。[moby/buildkit#5146]
- `ADD` 和 `COPY` 指令现在支持对 `--chmod` 选项值的构建参数进行变量插值。[moby/buildkit#5151]
- 改进了 `COPY` 和 `ADD` 指令中 `--chmod` 选项的验证。[moby/buildkit#5148]
- 修复了挂载上 size 和 destination 属性缺失补全的问题。[moby/buildkit#5245]
- 现在为 Dockerfile 前端发行镜像设置了 OCI 注解。[moby/buildkit#5197]

[moby/buildkit#5215]: https://github.com/moby/buildkit/pull/5215
[moby/buildkit#5213]: https://github.com/moby/buildkit/pull/5213
[moby/buildkit#5146]: https://github.com/moby/buildkit/pull/5146
[moby/buildkit#5151]: https://github.com/moby/buildkit/pull/5151
[moby/buildkit#5148]: https://github.com/moby/buildkit/pull/5148
[moby/buildkit#5245]: https://github.com/moby/buildkit/pull/5245
[moby/buildkit#5197]: https://github.com/moby/buildkit/pull/5197

## 1.9.0

{{< release-date date="2024-07-11" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.9.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.9.0
```

- 添加了新的验证规则：
  - `SecretsUsedInArgOrEnv`
  - `InvalidDefaultArgInFrom`
  - `RedundantTargetPlatform`
  - `CopyIgnoredFile`（实验性）
  - `FromPlatformFlagConstDisallowed`
- 针对大型 Dockerfile 的许多性能改进。[moby/buildkit#5067](https://github.com/moby/buildkit/pull/5067/), [moby/buildkit#5029](https://github.com/moby/buildkit/pull/5029/)
- 修复了构建没有定义阶段的 Dockerfile 时可能发生的 panic。[moby/buildkit#5150](https://github.com/moby/buildkit/pull/5150/)
- 修复了错误的 JSON 解析，该错误可能导致一些错误的 JSON 值在不报错的情况下通过验证。[moby/buildkit#5107](https://github.com/moby/buildkit/pull/5107/)
- 修复了一个回归问题，即目标路径为 `.` 的 `COPY --link` 可能会失败。[moby/buildkit#5080](https://github.com/moby/buildkit/pull/5080/)
- 修复了 `ADD --checksum` 与 Git URL 配合使用时的验证问题。[moby/buildkit#5085](https://github.com/moby/buildkit/pull/5085/)

## 1.8.1

{{< release-date date="2024-06-18" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.8.1) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.8.1
```

### Bug 修复和增强功能

- 修复了变量展开中空字符串的处理问题。[moby/buildkit#5052](https://github.com/moby/buildkit/pull/5052/)
- 改进了构建警告的格式化。[moby/buildkit#5037](https://github.com/moby/buildkit/pull/5037/), [moby/buildkit#5045](https://github.com/moby/buildkit/pull/5045/), [moby/buildkit#5046](https://github.com/moby/buildkit/pull/5046/)
- 修复了多阶段构建中 `UndeclaredVariable` 警告可能出现的无效输出。[moby/buildkit#5048](https://github.com/moby/buildkit/pull/5048/)

## 1.8.0

{{< release-date date="2024-06-11" >}}

此版本的完整发行说明可在 [GitHub](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.8.0) 上获取。

```dockerfile
# syntax=docker/dockerfile:1.8.0
```

- 添加了许多新的验证规则，以验证您的 Dockerfile 是否使用了最佳实践。这些规则在构建期间进行验证，新的 `check` 前端方法可用于仅触发验证而不完成整个构建。
- 新指令 `#check` 和构建参数 `BUILDKIT_DOCKERFILE_CHECK` 允许您控制构建检查的行为。[moby/buildkit#4962](https://github.com/moby/buildkit/pull/4962/)
- 现在会对使用与预期平台不匹配的单平台基础镜像进行验证。[moby/buildkit#4924](https://github.com/moby/buildkit/pull/4924/)
- 现在可以正确处理全局作用域中 `ARG` 定义展开时的错误。[moby/buildkit#4856](https://github.com/moby/buildkit/pull/4856/)
- 只有在用户没有覆盖时，才会对 `ARG` 的默认值进行展开。以前，展开是完成的，但随后该值被忽略，这可能会导致意外的展开错误。[moby/buildkit#4856](https://github.com/moby/buildkit/pull/4856/)
- 提高了解析具有许多阶段的大型 Dockerfile 的性能。[moby/buildkit#4970](https://github.com/moby/buildkit/pull/4970/)
- 修复了一些 Windows 路径处理一致性错误。[moby/buildkit#4825](https://github.com/moby/buildkit/pull/4825/)

## 1.7.0

{{< release-date date="2024-03-06" >}}

### 稳定版

```dockerfile
# syntax=docker/dockerfile:1.7
```

- 变量展开现在允许字符串替换和修剪。[moby/buildkit#4427](https://github.com/moby/buildkit/pull/4427), [moby/buildkit#4287](https://github.com/moby/buildkit/pull/4287)
- 带有本地源的具名上下文现在可以正确地仅传输 Dockerfile 中使用的文件，而不是完整的源目录。[moby/buildkit#4161](https://github.com/moby/buildkit/pull/4161)
- Dockerfile 现在可以更好地验证阶段顺序，如果阶段顺序不正确，则会返回带有堆栈跟踪的出色错误。[moby/buildkit#4568](https://github.com/moby/buildkit/pull/4568), [moby/buildkit#4567](https://github.com/moby/buildkit/pull/4567)
- 历史提交消息现在包含与 `COPY` 和 `ADD` 一起使用的标志。[moby/buildkit#4597](https://github.com/moby/buildkit/pull/4597)
- 改进了来自 Git 和 HTTP 源的 `ADD` 命令的进度消息。[moby/buildkit#4408](https://github.com/moby/buildkit/pull/4408)

### Labs 版

```dockerfile
# syntax=docker/dockerfile:1.7-labs
```

- 为 `COPY` 添加了新的 `--parents` 标志，用于在复制文件时保留父目录结构。[moby/buildkit#4598](https://github.com/moby/buildkit/pull/4598), [moby/buildkit#3001](https://github.com/moby/buildkit/pull/3001), [moby/buildkit#4720](https://github.com/moby/buildkit/pull/4720), [moby/buildkit#4728](https://github.com/moby/buildkit/pull/4728), [文档](/reference/dockerfile.md#copy---parents)
- `COPY` 和 `ADD` 命令中可以使用新的 `--exclude` 标志，对复制的文件应用过滤器。[moby/buildkit#4561](https://github.com/moby/buildkit/pull/4561), [文档](/reference/dockerfile.md#copy---exclude)

## 1.6.0

{{< release-date date="2023-06-13" >}}

### 新增

- 为 [`HEALTHCHECK` 指令](/reference/dockerfile.md#healthcheck) 添加了 `--start-interval` 标志。

以下功能已从 labs 频道毕业到稳定版：

- `ADD` 指令现在可以 [直接从 Git URL 导入文件](/reference/dockerfile.md#adding-a-git-repository-add-git-ref-dir)
- `ADD` 指令现在支持 [`--checksum` 标志](/reference/dockerfile.md#verifying-a-remote-file-checksum-add---checksumchecksum-http-src-dest)，用于验证远程 URL 内容的准确性

### Bug 修复和增强功能

- 变量替换现在支持不带 `:` 的额外 POSIX 兼容变体。[moby/buildkit#3611](https://github.com/moby/buildkit/pull/3611)
- 导出的 Windows 镜像现在包含来自基础镜像的 OSVersion 和 OSFeatures 值。[moby/buildkit#3619](https://github.com/moby/buildkit/pull/3619)
- 将 Heredoc 的权限更改为 0644。[moby/buildkit#3992](https://github.com/moby/buildkit/pull/3992)

## 1.5.2

{{< release-date date="2023-02-14" >}}

### Bug 修复和增强功能

- 修复了从缺少分支名称但包含子目录的 Git 引用进行构建的问题
- 此版本现在包含 386 平台镜像

## 1.5.1

{{< release-date date="2023-01-18" >}}

### Bug 修复和增强功能

- 修复了多平台构建中出现警告条件时可能发生的 panic

## 1.5.0 (labs)

{{< release-date date="2023-01-10" >}}

{{% include "dockerfile-labs-channel.md" %}}

### 新增

- `ADD` 命令现在支持 [`--checksum` 标志](/reference/dockerfile.md#verifying-a-remote-file-checksum-add---checksumchecksum-http-src-dest)，用于验证远程 URL 内容的准确性

## 1.5.0

{{< release-date date="2023-01-10" >}}

### 新增

- `ADD` 命令现在可以 [直接从 Git URL 导入文件](/reference/dockerfile.md#adding-a-git-repository-add-git-ref-dir)

### Bug 修复和增强功能

- 具名上下文现在支持 `oci-layout://` 协议，用于包含来自本地 OCI 布局结构的镜像
- Dockerfile 现在支持次要请求，用于列出所有构建目标或打印特定构建目标接受的参数大纲
- 重定向到外部前端镜像的 Dockerfile `#syntax` 指令现在也允许使用 `//` 注释或 JSON 设置。该文件还可能包含 shebang 标头
- 具名上下文现在可以使用空的 scratch 镜像初始化
- 具名上下文现在可以使用 SSH Git URL 初始化
- 修复了导入 Schema1 镜像时对 `ONBUILD` 的处理

## 1.4.3

{{< release-date date="2022-08-23" >}}

### Bug 修复和增强功能

- 修复了从 `docker-image://` 具名上下文构建镜像时创建时间戳未重置的问题
- 修复了加载 `docker-image://` 具名上下文时传递 `FROM` 命令的 `--platform` 标志的问题

## 1.4.2

{{< release-date date="2022-05-06" >}}

### Bug 修复和增强功能

- 修复了从通过构建上下文传递的镜像加载某些环境变量的问题

## 1.4.1

{{< release-date date="2022-04-08" >}}

### Bug 修复和增强功能

- 修复了当输入是针对不同平台构建时，输入中的交叉编译情况下的具名上下文解析问题

## 1.4.0

{{< release-date date="2022-03-09" >}}

### 新增

- [`COPY --link` 和 `ADD --link`](/reference/dockerfile.md#copy---link) 允许以更高的缓存效率复制文件，并在无需重新构建镜像的情况下重新设置镜像基准。`--link` 将文件复制到单独的层，然后使用新的 LLB MergeOp 实现将独立的层链接在一起
- [Heredocs](/reference/dockerfile.md#here-documents) 支持已从 labs 频道晋升到稳定版。此功能允许编写多行内联脚本和文件
- 额外的 [具名构建上下文](/reference/cli/docker/buildx/build.md#build-context) 可以传递给构建，以添加或覆盖构建内部的阶段或镜像。上下文的源可以是本地源、镜像、Git 或 HTTP URL
- [`BUILDKIT_SANDBOX_HOSTNAME` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args) 可用于为 `RUN` 步骤设置默认主机名

### Bug 修复和增强功能

- 使用交叉编译阶段时，一个步骤的目标平台现在显示在进度输出中
- 修复了 Heredoc 错误移除内容中引号的一些情况

## 1.3.1

{{< release-date date="2021-10-04" >}}

### Bug 修复和增强功能

- 修复了解析没有值的 "required" 挂载键的问题

## 1.3.0 (labs)

{{< release-date date="2021-07-16" >}}

{{% include "dockerfile-labs-channel.md" %}}

### 新增

- `RUN` 和 `COPY` 命令现在支持 [Here-document 语法](/reference/dockerfile.md#here-documents)，允许编写多行内联脚本和文件

## 1.3.0

{{< release-date date="2021-07-16" >}}

### 新增

- `RUN` 命令允许使用 [`--network` 标志](/reference/dockerfile.md#run---network) 请求特定类型的网络条件。`--network=host` 需要允许 `network.host` 授权。此功能之前仅在 labs 频道可用

### Bug 修复和增强功能

- 带有远程 URL 输入的 `ADD` 命令现在可以正确处理 `--chmod` 标志
- [`RUN --mount` 标志](/reference/dockerfile.md#run---mount) 的值现在支持变量展开，但 `from` 字段除外
- 允许 [`BUILDKIT_MULTI_PLATFORM` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args) 强制始终创建多平台镜像，即使仅包含单个平台

## 1.2.1 (labs)

{{< release-date date="2020-12-12" >}}

{{% include "dockerfile-labs-channel.md" %}}

### Bug 修复和增强功能

- `RUN` 命令允许使用 [`--network` 标志](/reference/dockerfile.md#run---network) 请求特定类型的网络条件。`--network=host` 需要允许 `network.host` 授权

## 1.2.1

{{< release-date date="2020-12-12" >}}

### Bug 修复和增强功能

- 还原了 "确保 ENTRYPOINT 命令至少有一个参数" 的更改
- 优化了多平台交叉编译构建中对 `COPY` 调用的处理

## 1.2.0 (labs)

{{< release-date date="2020-12-03" >}}

{{% include "dockerfile-labs-channel.md" %}}

### Bug 修复和增强功能

- 实验性频道已重命名为 _labs_

## 1.2.0

{{< release-date date="2020-12-03" >}}

### 新增

- 用于创建 secret、ssh、bind 和 cache 挂载的 [`RUN --mount` 语法](/reference/dockerfile.md#run---mount) 已移至主线频道
- [`ARG` 命令](/reference/dockerfile.md#arg) 现在支持在同一行定义多个构建参数，类似于 `ENV`

### Bug 修复和增强功能

- 元数据加载错误现在被处理为致命错误，以避免错误的构建结果
- 允许使用小写的 Dockerfile 名称
- `ADD` 中的 `--chown` 标志现在允许参数展开
- `ENTRYPOINT` 要求至少有一个参数，以避免创建损坏的镜像

## 1.1.7

{{< release-date date="2020-04-18" >}}

### Bug 修复和增强功能

- 将 `FrontendInputs` 转发到网关

## 1.1.2 (labs)

{{< release-date date="2019-07-31" >}}

{{% include "dockerfile-labs-channel.md" %}}

### Bug 修复和增强功能

- 允许通过 `RUN --security=sandbox|insecure` 为进程设置安全模式
- 允许为 [缓存挂载](/reference/dockerfile.md#run---mounttypecache) 设置 uid/gid
- 避免请求将内部链接路径拉取到构建上下文
- 确保缺失的缓存 ID 默认为目标路径
- 允许通过 [`BUILDKIT_CACHE_MOUNT_NS` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args) 为缓存挂载设置命名空间

## 1.1.2

{{< release-date date="2019-07-31" >}}

### Bug 修复和增强功能

- 修复了使用正确用户创建工作目录的问题，且不重置自定义所有权
- 修复了处理同时用作 `ENV` 的空构建参数的问题
- 检测循环依赖

## 1.1.0

{{< release-date date="2019-04-27" >}}

### 新增

- `ADD/COPY` 命令现在支持基于 `llb.FileOp` 的实现，且如果提供了内置文件操作支持，则不需要助手镜像
- `COPY` 命令的 `--chown` 标志现在支持变量展开

### Bug 修复和增强功能

- 为了寻找从构建上下文中忽略的文件，Dockerfile 前端将首先寻找 `<path/to/Dockerfile>.dockerignore` 文件，如果没有找到，将从构建上下文的根目录寻找 `.dockerignore` 文件。这允许具有多个 Dockerfile 的项目使用不同的 `.dockerignore` 定义
