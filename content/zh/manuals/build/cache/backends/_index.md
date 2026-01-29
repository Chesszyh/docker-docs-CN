---
title: 缓存存储后端
description: 缓存后端允许您从外部管理构建缓存。
keywords: build, buildx, cache, backend, gha, azblob, s3, registry, local
alias:
  - /build/building/cache/backends/
---

为了确保快速构建，BuildKit 会自动将构建结果缓存到其内部缓存中。此外，BuildKit 还支持将构建缓存导出到外部位置，从而可以在未来的构建中导入。

在 CI/CD 构建环境中，外部缓存几乎变得必不可少。此类环境通常在运行之间几乎没有持久性，但尽可能缩短镜像构建的运行时仍然非常重要。

默认的 `docker` 驱动程序支持 `inline`、`local`、`registry` 和 `gha` 缓存后端，但前提是您已启用 [containerd 镜像库](/manuals/desktop/features/containerd.md)。其他缓存后端需要您选择不同的 [驱动程序](/manuals/build/builders/drivers/_index.md)。

> [!WARNING]
> 
> 如果您在构建过程中使用密钥或凭据，请确保使用专用的 [`--secret` 选项](/reference/cli/docker/buildx/build.md#secret) 来操作它们。使用 `COPY` 或 `ARG` 手动管理密钥可能会导致凭据泄露。

## 后端

Buildx 支持以下缓存存储后端：

- `inline`：将构建缓存嵌入镜像中。

  内联缓存会被推送到与主输出结果相同的位置。这仅适用于 [`image` 导出器](../../exporters/image-registry.md)。

- `registry`：将构建缓存嵌入到一个单独的镜像中，并推送到与主输出分离的专用位置。

- `local`：将构建缓存写入文件系统中的本地目录。

- `gha`：将构建缓存上传到 [GitHub Actions 缓存](https://docs.github.com/en/rest/actions/cache)（Beta）。

- `s3`：将构建缓存上传到 [AWS S3 存储桶](https://aws.amazon.com/s3/)（尚未发布）。

- `azblob`：将构建缓存上传到 [Azure Blob 存储](https://azure.microsoft.com/en-us/services/storage/blobs/)（尚未发布）。

## 命令语法

要使用任何缓存后端，您首先需要在构建时使用 [`--cache-to` 选项](/reference/cli/docker/buildx/build.md#cache-to) 指定它，以便将缓存导出到您选择的存储后端。然后，使用 [`--cache-from` 选项](/reference/cli/docker/buildx/build.md#cache-from) 从存储后端将缓存导入当前构建。与本地 BuildKit 缓存（始终启用）不同，所有的缓存存储后端都必须显式导出和显式导入。

使用 `registry` 后端进行导入和导出缓存的 `buildx` 命令示例：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image>[,parameters...] .
```

> [!WARNING]
> 
> 一般而言，每个缓存都会写入某个位置。如果没有覆盖之前缓存的数据，任何位置都不能被写入两次。如果您想维护多个作用域缓存（例如，每个 Git 分支一个缓存），请确保为导出的缓存使用不同的位置。

## 多个缓存

BuildKit 支持多个缓存导出器，允许您将缓存推送到多个目的地。您也可以根据需要从任意多个远程缓存中导入。例如，一个常见的模式是同时使用当前分支和主分支的缓存。以下示例显示了使用 `registry` 缓存后端从多个位置导入缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:main .
```

## 配置选项

本节介绍生成缓存导出时可用的一些配置选项。此处描述的选项对于至少两种或更多后端类型是通用的。此外，不同的后端类型还支持特定的参数。有关适用哪些配置参数的更多信息，请参阅每个后端类型的详细页面。

此处描述的通用参数包括：

- [缓存模式](#缓存模式)
- [缓存压缩](#缓存压缩)
- [OCI 媒体类型](#oci-媒体类型)

### 缓存模式

在生成缓存输出时，`--cache-to` 参数接受一个 `mode` 选项，用于定义导出的缓存中应包含哪些层。除 `inline` 缓存外，所有缓存后端都支持此选项。

模式可以设置为两个选项之一：`mode=min` 或 `mode=max`。例如，使用 `registry` 后端以 `mode=max` 构建缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,mode=max \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

此选项仅在导出缓存（使用 `--cache-to`）时设置。在导入缓存（`--cache-from`）时，会自动检测相关参数。

在 `min`（最小）缓存模式（默认值）下，仅缓存导出到最终镜像中的层；而在 `max`（最大）缓存模式下，所有层都会被缓存，即使是中间步骤的层。

虽然 `min` 缓存通常更小（从而加快导入/导出时间并降低存储成本），但 `max` 缓存更有可能获得更多缓存命中。根据构建的复杂性和位置，您应该尝试这两个参数以找到最适合您的结果。

### 缓存压缩

缓存压缩选项与 [导出器压缩选项](../../exporters/_index.md#compression) 相同。`local` 和 `registry` 缓存后端支持此功能。

例如，使用 `zstd` 压缩来压缩 `registry` 缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,compression=zstd \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

### OCI 媒体类型

缓存 OCI 选项与 [导出器 OCI 选项](../../exporters/_index.md#oci-media-types) 相同。`local` 和 `registry` 缓存后端支持这些选项。

例如，要导出 OCI 媒体类型缓存，请使用 `oci-mediatypes` 属性：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

此属性仅在配合 `--cache-to` 标志时有意义。在获取缓存时，BuildKit 将自动检测要使用的正确媒体类型。

默认情况下，OCI 媒体类型会为缓存镜像生成一个镜像索引（image index）。某些 OCI 镜像库（如 Amazon ECR）不支持镜像索引媒体类型：`application/vnd.oci.image.index.v1+json`。如果您将缓存镜像导出到 ECR 或任何其他不支持镜像索引的镜像库，请将 `image-manifest` 参数设置为 `true`，以便为缓存镜像生成单个镜像清单（manifest），而不是镜像索引：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true,image-manifest=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

> [!NOTE]
> 自 BuildKit v0.21 起，`image-manifest` 默认启用。
