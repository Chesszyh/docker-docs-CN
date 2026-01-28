---
title: 缓存存储后端
description: |
  缓存后端允许你在外部管理构建缓存。
  外部缓存对于创建可以帮助加速内部循环和 CI 构建的共享缓存非常有用。
keywords: build, buildx, cache, backend, gha, azblob, s3, registry, local
aliases:
  - /build/building/cache/backends/
---

为了确保快速构建，BuildKit 会自动将构建结果缓存在其自己的内部缓存中。此外，BuildKit 还支持将构建缓存导出到外部位置，从而可以在未来的构建中导入。

在 CI/CD 构建环境中，外部缓存几乎变得必不可少。这类环境通常在运行之间几乎没有持久性，但保持镜像构建的运行时间尽可能低仍然很重要。

默认的 `docker` 驱动程序支持 `inline`、`local`、`registry` 和 `gha` 缓存后端，但前提是你已启用 [containerd 镜像存储](/manuals/desktop/features/containerd.md)。其他缓存后端需要你选择不同的[驱动程序](/manuals/build/builders/drivers/_index.md)。

> [!WARNING]
>
> 如果你在构建过程中使用密钥或凭据，请确保使用专用的
> [`--secret` 选项](/reference/cli/docker/buildx/build.md#secret)来处理它们。
> 使用 `COPY` 或 `ARG` 手动管理密钥可能导致凭据泄露。

## 后端

Buildx 支持以下缓存存储后端：

- `inline`：将构建缓存嵌入到镜像中。

  内联缓存被推送到与主输出结果相同的位置。这仅适用于 [`image` 导出器](../../exporters/image-registry.md)。

- `registry`：将构建缓存嵌入到单独的镜像中，并推送到与主输出分开的专用位置。

- `local`：将构建缓存写入文件系统上的本地目录。

- `gha`：将构建缓存上传到
  [GitHub Actions 缓存](https://docs.github.com/en/rest/actions/cache)（测试版）。

- `s3`：将构建缓存上传到
  [AWS S3 存储桶](https://aws.amazon.com/s3/)（未发布）。

- `azblob`：将构建缓存上传到
  [Azure Blob 存储](https://azure.microsoft.com/en-us/services/storage/blobs/)
  （未发布）。

## 命令语法

要使用任何缓存后端，你首先需要在构建时使用
[`--cache-to` 选项](/reference/cli/docker/buildx/build.md#cache-to)指定它，
以将缓存导出到你选择的存储后端。然后，使用
[`--cache-from` 选项](/reference/cli/docker/buildx/build.md#cache-from)
将存储后端中的缓存导入到当前构建中。与本地 BuildKit 缓存（始终启用）不同，所有缓存存储后端都必须显式导出到，并显式从中导入。

使用 `registry` 后端的示例 `buildx` 命令，使用导入和导出缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image>[,parameters...] .
```

> [!WARNING]
>
> 作为一般规则，每个缓存都写入某个位置。没有位置可以被写入两次而不覆盖先前缓存的数据。如果你想维护多个作用域的缓存（例如，每个 Git 分支一个缓存），那么请确保为导出的缓存使用不同的位置。

## 多个缓存

BuildKit 支持多个缓存导出器，允许你将缓存推送到多个目标。你也可以从任意多个远程缓存导入。例如，一个常见的模式是使用当前分支和主分支的缓存。以下示例展示了使用 registry 缓存后端从多个位置导入缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:main .
```

## 配置选项

本节描述了生成缓存导出时可用的一些配置选项。这里描述的选项对于至少两种或更多后端类型是通用的。此外，不同的后端类型还支持特定的参数。有关哪些配置参数适用的更多信息，请参阅每种后端类型的详细页面。

这里描述的通用参数是：

- [缓存模式](#cache-mode)
- [缓存压缩](#cache-compression)
- [OCI 媒体类型](#oci-media-types)

### 缓存模式

生成缓存输出时，`--cache-to` 参数接受一个 `mode` 选项，用于定义导出的缓存中包含哪些层。除了 `inline` 缓存外，所有缓存后端都支持此选项。

模式可以设置为两个选项之一：`mode=min` 或 `mode=max`。例如，要使用 registry 后端以 `mode=max` 构建缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,mode=max \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

此选项仅在使用 `--cache-to` 导出缓存时设置。导入缓存时（`--cache-from`），相关参数会自动检测。

在 `min` 缓存模式（默认）下，只有导出到结果镜像中的层会被缓存，而在 `max` 缓存模式下，所有层都会被缓存，包括中间步骤的层。

虽然 `min` 缓存通常更小（这加快了导入/导出时间并降低了存储成本），但 `max` 缓存更有可能获得更多缓存命中。根据构建的复杂性和位置，你应该尝试两个参数以找到最适合你的结果。

### 缓存压缩

缓存压缩选项与[导出器压缩选项](../../exporters/_index.md#compression)相同。`local` 和 `registry` 缓存后端支持此选项。

例如，要使用 `zstd` 压缩来压缩 `registry` 缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,compression=zstd \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

### OCI 媒体类型

缓存 OCI 选项与[导出器 OCI 选项](../../exporters/_index.md#oci-media-types)相同。`local` 和 `registry` 缓存后端支持这些选项。

例如，要导出 OCI 媒体类型缓存，使用 `oci-mediatypes` 属性：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

此属性仅在 `--cache-to` 标志中有意义。获取缓存时，BuildKit 会自动检测要使用的正确媒体类型。

默认情况下，OCI 媒体类型会为缓存镜像生成一个镜像索引。某些 OCI 注册表，如 Amazon ECR，不支持镜像索引媒体类型：`application/vnd.oci.image.index.v1+json`。如果你将缓存镜像导出到 ECR 或任何其他不支持镜像索引的注册表，请将 `image-manifest` 参数设置为 `true`，以为缓存镜像生成单个镜像清单而不是镜像索引：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true,image-manifest=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

> [!NOTE]
> 从 BuildKit v0.21 开始，`image-manifest` 默认启用。
