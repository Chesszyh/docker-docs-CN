---
title: 导出器 (Exporters) 概览
linkTitle: 导出器 (Exporters)
weight: 90
description: 构建导出器定义了构建结果的输出格式
keywords: build, buildx, buildkit, exporter, image, registry, local, tar, oci, docker, cacheonly, 导出器, 输出格式
alias:
  - /build/building/exporters/
---

导出器（Exporters）用于将构建结果保存为指定的输出类型。您可以使用 [`--output` CLI 选项](/reference/cli/docker/buildx/build.md#output) 来指定要使用的导出器。Buildx 支持以下导出器：

- `image`：将构建结果导出为容器镜像。
- `registry`：将构建结果导出为容器镜像，并将其推送到指定的注册表。
- `local`：将构建的根文件系统导出到本地目录。
- `tar`：将构建的根文件系统打包为本地 tar 包。
- `oci`：以 [OCI 镜像布局](https://github.com/opencontainers/image-spec/blob/v1.0.1/image-layout.md) 格式将构建结果导出到本地文件系统。
- `docker`：以 [Docker 镜像规范 v1.2.0](https://github.com/moby/moby/blob/v25.0.0/image/spec/v1.2.md) 格式将构建结果导出到本地文件系统。
- `cacheonly`：不导出任何构建输出，但运行构建并创建缓存。

## 使用导出器

要指定导出器，请使用以下命令语法：

```console
$ docker buildx build --tag <注册表>/<镜像名> \
  --output type=<类型> .
```

大多数常见的用例并不需要您显式指定使用哪个导出器。只有当您打算自定义输出或想将其保存到磁盘时，才需要指定导出器。`--load` 和 `--push` 选项允许 Buildx 自动推断要使用的导出器设置。

例如，如果您结合使用 `--push` 选项和 `--tag`，Buildx 会自动使用 `image` 导出器，并配置该导出器将结果推送到指定的注册表。

要充分发挥 BuildKit 提供的各种导出器的灵活性，可以使用 `--output` 标志来配置导出器选项。

## 使用场景

每种导出器类型都是为不同的使用场景设计的。以下章节描述了一些常见场景，以及您如何使用导出器来生成所需的输出。

### 加载到镜像库

Buildx 经常用于构建可以加载到镜像库中的容器镜像。这就是 `docker` 导出器的用武之地。以下示例展示了如何使用 `docker` 导出器构建镜像，并利用 `--output` 选项将该镜像加载到本地镜像库：

```console
$ docker buildx build \
  --output type=docker,name=<注册表>/<镜像名> .
```

如果您提供了 `--tag` 和 `--load` 选项，Buildx CLI 会自动使用 `docker` 导出器并将其加载到镜像库：

```console
$ docker buildx build --tag <注册表>/<镜像名> --load .
```

使用 `docker` 驱动构建的镜像会自动加载到本地镜像库中。

加载到镜像库中的镜像在构建完成后即可立即供 `docker run` 使用，并且当您运行 `docker images` 命令时，可以在镜像列表中看到它们。

### 推送到注册表

要将构建好的镜像推送到容器注册表，您可以使用 `registry` 或 `image` 导出器。

当您向 Buildx CLI 传递 `--push` 选项时，即指示 BuildKit 将构建好的镜像推送到指定的注册表：

```console
$ docker buildx build --tag <注册表>/<镜像名> --push .
```

在底层，这使用了 `image` 导出器，并设置了 `push` 参数。这等同于使用 `--output` 选项执行以下长命令：

```console
$ docker buildx build \
  --output type=image,name=<注册表>/<镜像名>,push=true .
```

您也可以使用 `registry` 导出器，其效果相同：

```console
$ docker buildx build \
  --output type=registry,name=<注册表>/<镜像名> .
```

### 将镜像布局导出为文件

您可以使用 `oci` 或 `docker` 导出器将构建结果作为镜像布局保存到本地文件系统中。这两个导出器都会生成一个包含对应镜像布局的 tar 归档文件。`dest` 参数定义了该 tar 包的目标输出路径。

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
│   └── sha256
│       ├── 9b18e9b68314027565b90ff6189d65942c0f7986da80df008b8431276885218e
│       ├── c78795f3c329dbbbfb14d0d32288dea25c3cd12f31bd0213be694332a70c7f13
│       ├── d1cf38078fa218d15715e2afcf71588ee482352d697532cf316626164699a0e2
│       ├── e84fa1df52d2abdfac52165755d5d1c7621d74eda8e12881f6b0d38a36e01775
│       └── fe9e23793a27fe30374308988283d40047628c73f91f577432a0d05ab0160de7
├── index.json
├── manifest.json
└── oci-layout
```

### 导出文件系统

如果您不想从构建结果中构建镜像，而是想导出构建出的文件系统，可以使用 `local` 和 `tar` 导出器。

`local` 导出器将文件系统解压到指定位置的目录结构中。`tar` 导出器则创建一个 tar 包归档文件。

```console
$ docker buildx build --output type=local,dest=<输出路径> .
```

`local` 导出器在 [多阶段构建](../building/multi-stage.md) 中非常有用，因为它允许您仅导出极少量的构建产物，例如自包含的二进制文件。

### 仅导出缓存 (Cache-only)

如果您只想运行一次构建而不导出任何输出，可以使用 `cacheonly` 导出器。例如，当您想运行一次测试构建，或者想先运行构建并随后通过后续命令创建导出时，这会非常有用。`cacheonly` 导出器会创建构建缓存，因此后续的任何构建都是即时的。

```console
$ docker buildx build --output type=cacheonly
```

如果您未指定导出器，且未提供如 `--load` 这样会自动选择合适导出器的快捷选项，Buildx 默认使用 `cacheonly` 导出器。除非您使用的是 `docker` 驱动进行构建，在这种情况下您使用的是 `docker` 导出器。

当默认使用 `cacheonly` 时，Buildx 会记录一条警告消息：

```console
$ docker buildx build .
WARNING: No output specified with docker-container driver.
         Build result will only remain in the build cache.
         To push result image into registry use --push or
         to load image into docker use --load
```

## 多个导出器

{{< summary-bar feature_name="多导出器构建" >}}

通过多次指定 `--output` 标志，您可以为任何给定的构建任务使用多个导出器。这要求 **Buildx 和 BuildKit** 的版本均在 0.13.0 或更高。

以下示例运行单次构建，使用了三种不同的导出器：

- `registry` 导出器将镜像推送到注册表
- `local` 导出器将构建结果提取到本地文件系统
- `--load` 标志（`image` 导出器的快捷方式）将结果加载到本地镜像库。

```console
$ docker buildx build \
  --output type=registry,tag=<注册表>/<镜像名> \
  --output type=local,dest=<输出路径> \
  --load .
```

## 配置选项

本节描述了一些可用于导出器的配置选项。

此处描述的选项至少适用于两种或更多导出器类型。此外，不同的导出器类型还支持特定的参数。请参阅关于每种导出器的详细页面，了解适用的配置参数。

此处描述的通用参数包括：

- [压缩](#压缩)
- [OCI 媒体类型](#oci-媒体类型)

### 压缩

当您导出压缩输出时，可以配置具体的压缩算法和级别。虽然默认值已经提供了良好的开箱即用体验，但您可能希望调整参数以优化存储成本或计算成本。更改压缩参数可以减少所需的存储空间并提高镜像下载速度，但会增加构建时间。

要选择压缩算法，可以使用 `compression` 选项。例如，使用 `compression=zstd` 构建 `image`：

```console
$ docker buildx build \
  --output type=image,name=<注册表>/<镜像名>,push=true,compression=zstd .
```

配合 `compression` 参数使用 `compression-level=<值>` 选项，为支持它的算法选择压缩级别：

- 对于 `gzip` 和 `estargz` 为 0-9
- 对于 `zstd` 为 0-22

通常规律是：数字越高，生成的文件越小，但压缩所需的时间越长。

如果请求的压缩算法与之前的不同，使用 `force-compression=true` 选项可以强制对从先前镜像导入的层进行重新压缩。

> [!NOTE]
> 
> `gzip` 和 `estargz` 压缩方法使用 [`compress/gzip` 包](https://pkg.go.dev/compress/gzip)，而 `zstd` 使用 [`github.com/klauspost/compress/zstd` 包](https://github.com/klauspost/compress/tree/master/zstd)。

### OCI 媒体类型

`image`、`registry`、`oci` 和 `docker` 导出器都会创建容器镜像。这些导出器同时支持 Docker 媒体类型（默认）和 OCI 媒体类型。

要导出设置了 OCI 媒体类型的镜像，请使用 `oci-mediatypes` 属性。

```console
$ docker buildx build \
  --output type=image,name=<注册表>/<镜像名>,push=true,oci-mediatypes=true .
```

## 下一步

阅读关于每种导出器的详细说明，了解它们的工作原理及使用方法：

- [镜像与注册表导出器 (Image and registry exporters)](image-registry.md)
- [OCI 与 Docker 导出器 (OCI and Docker exporters)](oci-docker.md)
- [本地与 Tar 导出器 (Local and tar exporters)](local-tar.md)