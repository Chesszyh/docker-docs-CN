---
title: 导出器概述
linkTitle: 导出器
weight: 90
description: 构建导出器定义构建结果的输出格式
keywords: build, buildx, buildkit, exporter, image, registry, local, tar, oci, docker, cacheonly
aliases:
  - /build/building/exporters/
---

导出器（Exporter）将您的构建结果保存到指定的输出类型。您可以使用 [`--output` CLI 选项](/reference/cli/docker/buildx/build.md#output) 指定要使用的导出器。Buildx 支持以下导出器：

- `image`：将构建结果导出为容器镜像。
- `registry`：将构建结果导出为容器镜像，并推送到指定的注册表。
- `local`：将构建根文件系统导出到本地目录。
- `tar`：将构建根文件系统打包为本地 tarball。
- `oci`：以 [OCI 镜像布局](https://github.com/opencontainers/image-spec/blob/v1.0.1/image-layout.md) 格式将构建结果导出到本地文件系统。
- `docker`：以 [Docker 镜像规范 v1.2.0](https://github.com/moby/moby/blob/v25.0.0/image/spec/v1.2.md) 格式将构建结果导出到本地文件系统。
- `cacheonly`：不导出构建输出，但运行构建并创建缓存。

## 使用导出器

要指定导出器，请使用以下命令语法：

```console
$ docker buildx build --tag <registry>/<image> \
  --output type=<TYPE> .
```

大多数常见用例不需要您显式指定使用哪个导出器。只有当您打算自定义输出或想将其保存到磁盘时，才需要指定导出器。`--load` 和 `--push` 选项允许 Buildx 推断要使用的导出器设置。

例如，如果您将 `--push` 选项与 `--tag` 结合使用，Buildx 会自动使用 `image` 导出器，并配置导出器将结果推送到指定的注册表。

要充分利用 BuildKit 提供的各种导出器的灵活性，您可以使用 `--output` 标志来配置导出器选项。

## 用例

每种导出器类型都是为不同的用例设计的。以下部分描述了一些常见场景，以及如何使用导出器生成您需要的输出。

### 加载到镜像存储

Buildx 通常用于构建可以加载到镜像存储的容器镜像。这就是 `docker` 导出器的用武之地。以下示例展示了如何使用 `docker` 导出器构建镜像，并使用 `--output` 选项将该镜像加载到本地镜像存储：

```console
$ docker buildx build \
  --output type=docker,name=<registry>/<image> .
```

如果您提供 `--tag` 和 `--load` 选项，Buildx CLI 将自动使用 `docker` 导出器并将其加载到镜像存储：

```console
$ docker buildx build --tag <registry>/<image> --load .
```

使用 `docker` 驱动程序构建的镜像会自动加载到本地镜像存储。

加载到镜像存储的镜像在构建完成后立即可用于 `docker run`，并且当您运行 `docker images` 命令时会在镜像列表中看到它们。

### 推送到注册表

要将构建的镜像推送到容器注册表，您可以使用 `registry` 或 `image` 导出器。

当您向 Buildx CLI 传递 `--push` 选项时，您指示 BuildKit 将构建的镜像推送到指定的注册表：

```console
$ docker buildx build --tag <registry>/<image> --push .
```

在底层，这使用 `image` 导出器，并设置 `push` 参数。这与使用 `--output` 选项的以下长格式命令相同：

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true .
```

您也可以使用 `registry` 导出器，它做同样的事情：

```console
$ docker buildx build \
  --output type=registry,name=<registry>/<image> .
```

### 将镜像布局导出到文件

您可以使用 `oci` 或 `docker` 导出器将构建结果保存为本地文件系统上的镜像布局。这两个导出器都生成包含相应镜像布局的 tar 归档文件。`dest` 参数定义 tarball 的目标输出路径。

```console
$ docker buildx build --output type=oci,dest=./image.tar .
[+] Building 0.8s (7/7) FINISHED
 ...
 => exporting to oci image format                                                                     0.0s
 => exporting layers                                                                                  0.0s
 => exporting manifest sha256:c1ef01a0a0ef94a7064d5cbce408075730410060e253ff8525d1e5f7e27bc900        0.0s
 => exporting config sha256:eadab326c1866dd247efb52cb715ba742bd0f05b6a205439f107cf91b3abc853          0.0s
 => sending tarball                                                                                   0.0s
$ mkdir -p out && tar -C out -xf ./image.tar
$ tree out
out
├── blobs
│   └── sha256
│       ├── 9b18e9b68314027565b90ff6189d65942c0f7986da80df008b8431276885218e
│       ├── c78795f3c329dbbbfb14d0d32288dea25c3cd12f31bd0213be694332a70c7f13
│       ├── d1cf38078fa218d15715e2afcf71588ee482352d697532cf316626164699a0e2
│       ├── e84fa1df52d2abdfac52165755d5d1c7621d74eda8e12881f6b0d38a36e01775
│       └── fe9e23793a27fe30374308988283d40047628c73f91f577432a0d05ab0160de7
├── index.json
├── manifest.json
└── oci-layout
```

### 导出文件系统

如果您不想从构建结果创建镜像，而是导出构建的文件系统，您可以使用 `local` 和 `tar` 导出器。

`local` 导出器将文件系统解包为指定位置的目录结构。`tar` 导出器创建 tarball 归档文件。

```console
$ docker buildx build --output type=local,dest=<path/to/output> .
```

`local` 导出器在[多阶段构建](../building/multi-stage.md)中很有用，因为它允许您仅导出最少数量的构建产物，例如独立的二进制文件。

### 仅缓存导出

如果您只想运行构建而不导出任何输出，可以使用 `cacheonly` 导出器。例如，如果您想运行测试构建，这可能很有用。或者，如果您想先运行构建，然后使用后续命令创建导出，也可以使用它。`cacheonly` 导出器创建构建缓存，因此任何后续构建都是即时的。

```console
$ docker buildx build --output type=cacheonly
```

如果您不指定导出器，也不提供像 `--load` 这样自动选择适当导出器的简写选项，Buildx 默认使用 `cacheonly` 导出器。除非您使用 `docker` 驱动程序构建，在这种情况下您使用 `docker` 导出器。

当默认使用 `cacheonly` 时，Buildx 会记录一条警告消息：

```console
$ docker buildx build .
WARNING: No output specified with docker-container driver.
         Build result will only remain in the build cache.
         To push result image into registry use --push or
         to load image into docker use --load
```

## 多个导出器

{{< summary-bar feature_name="Build multiple exporters" >}}

您可以通过多次指定 `--output` 标志为任何给定的构建使用多个导出器。这需要 **Buildx 和 BuildKit** 版本 0.13.0 或更高版本。

以下示例使用三个不同的导出器运行单个构建：

- `registry` 导出器将镜像推送到注册表
- `local` 导出器将构建结果提取到本地文件系统
- `--load` 标志（`image` 导出器的简写）将结果加载到本地镜像存储。

```console
$ docker buildx build \
  --output type=registry,tag=<registry>/<image> \
  --output type=local,dest=<path/to/output> \
  --load .
```

## 配置选项

本节描述导出器可用的一些配置选项。

这里描述的选项对于至少两种或更多导出器类型是通用的。此外，不同的导出器类型还支持特定的参数。有关哪些配置参数适用的更多信息，请参阅每个导出器的详细页面。

这里描述的通用参数是：

- [压缩](#compression)
- [OCI 媒体类型](#oci-media-types)

### 压缩 {#compression}

当您导出压缩输出时，您可以配置要使用的确切压缩算法和级别。虽然默认值提供了良好的开箱即用体验，但您可能希望调整参数以优化存储与计算成本。更改压缩参数可以减少所需的存储空间并改善镜像下载时间，但会增加构建时间。

要选择压缩算法，您可以使用 `compression` 选项。例如，构建使用 `compression=zstd` 的 `image`：

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true,compression=zstd .
```

将 `compression-level=<value>` 选项与 `compression` 参数一起使用，以为支持它的算法选择压缩级别：

- `gzip` 和 `estargz` 为 0-9
- `zstd` 为 0-22

一般规则是，数字越高，生成的文件越小，压缩运行时间越长。

使用 `force-compression=true` 选项强制重新压缩从先前镜像导入的层，如果请求的压缩算法与先前的压缩算法不同。

> [!NOTE]
>
> `gzip` 和 `estargz` 压缩方法使用 [`compress/gzip` 包](https://pkg.go.dev/compress/gzip)，而 `zstd` 使用 [`github.com/klauspost/compress/zstd` 包](https://github.com/klauspost/compress/tree/master/zstd)。

### OCI 媒体类型 {#oci-media-types}

`image`、`registry`、`oci` 和 `docker` 导出器创建容器镜像。这些导出器支持 Docker 媒体类型（默认）和 OCI 媒体类型。

要导出设置了 OCI 媒体类型的镜像，请使用 `oci-mediatypes` 属性。

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true,oci-mediatypes=true .
```

## 下一步

阅读有关每个导出器的信息，了解它们的工作原理以及如何使用它们：

- [Image 和 registry 导出器](image-registry.md)
- [OCI 和 Docker 导出器](oci-docker.md)
- [Local 和 tar 导出器](local-tar.md)
