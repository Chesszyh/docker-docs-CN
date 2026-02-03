---
title: 缓存存储后端 (Cache storage backends)
description: |
  缓存后端允许您在外部管理构建缓存。
  外部缓存对于创建共享缓存非常有用，可以帮助加速内部循环和 CI 构建。
keywords: build, buildx, cache, backend, gha, azblob, s3, registry, local, 缓存, 后端, 存储
alias:
  - /build/building/cache/backends/
---

为了确保快速构建，BuildKit 会自动在自身的内部缓存中缓存构建结果。此外，BuildKit 还支持将构建缓存导出到外部位置，从而可以在未来的构建任务中进行导入。

在 CI/CD 构建环境中，外部缓存几乎成了必选项。此类环境在不同运行之间通常很少或完全没有持久化能力，但尽可能缩短镜像构建的运行时间依然非常重要。

默认的 `docker` 驱动支持 `inline`、`local`、`registry` 和 `gha` 缓存后端，但前提是您已启用了 [containerd 镜像存储](/manuals/desktop/features/containerd.md)。其他缓存后端则要求您选择不同的 [驱动](/manuals/build/builders/drivers/_index.md)。

> [!WARNING]
>
> 如果您在构建过程中使用了机密或凭据，请确保使用专用的 [`--secret` 选项](/reference/cli/docker/buildx/build.md#secret) 来操作它们。通过 `COPY` 或 `ARG` 手动管理机密可能会导致凭据泄露。

## 后端类型

Buildx 支持以下缓存存储后端：

- `inline`：将构建缓存嵌入到镜像中。

  内联缓存会被推送到与主输出结果相同的位置。这仅在使用 [`image` 导出器](../../exporters/image-registry.md) 时有效。

- `registry`：将构建缓存嵌入到一个单独的镜像中，并推送到与主输出分开的专用位置。

- `local`：将构建缓存写入文件系统的本地目录。

- `gha`：将构建缓存上传到 [GitHub Actions 缓存](https://docs.github.com/en/rest/actions/cache)（测试版）。

- `s3`：将构建缓存上传到 [AWS S3 桶](https://aws.amazon.com/s3/)（尚未发布）。

- `azblob`：将构建缓存上传到 [Azure Blob 存储](https://azure.microsoft.com/en-us/services/storage/blobs/)（尚未发布）。

## 命令语法

要使用任何缓存后端，首先需要在构建时通过 [`--cache-to` 选项](/reference/cli/docker/buildx/build.md#cache-to) 指定，以便将缓存导出到您选择的存储后端。然后，使用 [`--cache-from` 选项](/reference/cli/docker/buildx/build.md#cache-from) 将缓存从该存储后端导入到当前构建任务中。与始终启用的本地 BuildKit 缓存不同，所有这些缓存存储后端都必须显式地进行导出和导入操作。

使用 `registry` 后端进行缓存导入和导出的 `buildx` 命令示例：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=registry,ref=<注册表>/<缓存镜像名>[,参数...] \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名>[,参数...] .
```

> [!WARNING]
>
> 作为通用规则，每项缓存都会写入某个位置。在不覆盖之前缓存数据的情况下，同一个位置不能写入两次。如果您想维护多个作用域不同的缓存（例如，每个 Git 分支一个缓存），请确保为导出的缓存使用不同的位置。

## 多个缓存

BuildKit 支持多个缓存导出器，允许您将缓存推送到多个目的地。您也可以从任意多个远程缓存中进行导入。例如，一个常见的模式是同时使用当前分支和主分支（main）的缓存。以下示例展示了使用注册表缓存后端从多个位置导入缓存：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=registry,ref=<注册表>/<缓存镜像名>:<分支名> \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名>:<分支名> \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名>:main .
```

## 配置选项

本节描述了生成缓存导出时可用的一些配置选项。此处描述的选项至少适用于两种或更多后端类型。此外，不同的后端类型还支持特定的参数。请参阅关于每种后端类型的详细页面，了解适用的配置参数。

此处描述的通用参数包括：

- [缓存模式](#缓存模式)
- [缓存压缩](#缓存压缩)
- [OCI 媒体类型](#oci-媒体类型)

### 缓存模式

在生成缓存输出时，`--cache-to` 参数接受一个 `mode` 选项，用于定义要在导出的缓存中包含哪些层。除 `inline` 缓存外，所有缓存后端都支持此选项。

模式可以设置为以下两个选项之一：`mode=min` 或 `mode=max`。例如，使用注册表后端并以 `mode=max` 构建缓存：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=registry,ref=<注册表>/<缓存镜像名>,mode=max \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名> .
```

此选项仅在导出缓存（使用 `--cache-to`）时设置。导入缓存 (`--cache-from`) 时，相关参数会自动检测。

在 `min` 缓存模式（默认值）下，仅缓存导出到结果镜像中的层；而在 `max` 缓存模式下，所有层都会被缓存，包括中间步骤的层。

虽然 `min` 缓存通常更小（这加快了导入/导出时间并降低了存储成本），但 `max` 缓存更有可能获得更多的缓存命中。根据您构建的复杂性和位置，您应该尝试这两个参数以找到最适合您的结果。

### 缓存压缩

缓存压缩选项与 [导出器压缩选项](../../exporters/_index.md#压缩) 相同。`local` 和 `registry` 缓存后端支持这些选项。

例如，使用 `zstd` 压缩来压缩 `registry` 缓存：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=registry,ref=<注册表>/<缓存镜像名>,compression=zstd \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名> .
```

### OCI 媒体类型

缓存 OCI 选项与 [导出器 OCI 选项](../../exporters/_index.md#oci-媒体类型) 相同。`local` 和 `registry` 缓存后端支持这些选项。

例如，要导出 OCI 媒体类型缓存，请使用 `oci-mediatypes` 属性：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=registry,ref=<注册表>/<缓存镜像名>,oci-mediatypes=true \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名> .
```

此属性仅在配合 `--cache-to` 标志时有意义。获取缓存时，BuildKit 会自动检测要使用的正确媒体类型。

默认情况下，OCI 媒体类型会为缓存镜像生成一个镜像索引（image index）。某些 OCI 注册表（如 Amazon ECR）不支持镜像索引媒体类型 `application/vnd.oci.image.index.v1+json`。如果您向 ECR 或任何其他不支持镜像索引的注册表导出缓存镜像，请将 `image-manifest` 参数设置为 `true`，以为缓存镜像生成单个镜像清单（image manifest）而非镜像索引：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=registry,ref=<注册表>/<缓存镜像名>,oci-mediatypes=true,image-manifest=true \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名> .
```

> [!NOTE]
> 自 BuildKit v0.21 起，`image-manifest` 默认启用。