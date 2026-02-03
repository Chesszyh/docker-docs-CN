---
title: 多平台构建 (Multi-platform builds)
linkTitle: 多平台
weight: 40
description: 了解什么是多平台构建，以及如何使用 Docker Buildx 执行多平台构建。
keywords: build, buildx, buildkit, multi-platform, cross-platform, cross-compilation, emulation, QEMU, ARM, x86, Windows, Linux, macOS, 多平台, 交叉编译, 模拟
aliases:
- /build/buildx/multiplatform-images/
- /desktop/multi-arch/
- /docker-for-mac/multi-arch/
- /mackit/multi-arch/
- /build/guide/multi-platform/
---

多平台构建是指针对多种不同的操作系统或 CPU 架构组合执行的一次性构建调用。在构建镜像时，这允许您创建一个可以在多个平台（如 `linux/amd64`、`linux/arm64` 和 `windows/amd64`）上运行的镜像。

## 为什么需要多平台构建？

Docker 通过将应用程序及其依赖项打包到容器中，解决了“在我的机器上可以运行”的问题。这使得在开发、测试和生产等不同环境中运行同一个应用程序变得容易。

但容器化本身只能解决部分问题。容器共享宿主机的内核，这意味着在容器内部运行的代码必须与宿主机的架构兼容。这就是为什么您无法在 arm64 宿主机上运行 `linux/amd64` 容器（除非使用模拟技术），或者在 Linux 宿主机上运行 Windows 容器的原因。

多平台构建通过将同一个应用程序的多个变体打包进单个镜像中，解决了这个问题。这使您能够在不同类型的硬件上运行相同的镜像，例如运行 x86-64 的开发机或云端基于 ARM 的 Amazon EC2 实例，而无需进行模拟。

### 单平台镜像与多平台镜像的区别

多平台镜像与单平台镜像具有不同的结构。单平台镜像包含一个指向单一配置和一组层的清单 (manifest)。多平台镜像则包含一个清单列表 (manifest list)，指向多个清单，每个清单又指向不同的配置和层集。

![多平台镜像结构](/build/images/single-vs-multiplatform-image.svg)

当您将多平台镜像推送到注册表时，注册表会存储该清单列表以及所有独立的清单。当您拉取镜像时，注册表会返回清单列表，Docker 会根据宿主机的架构自动选择正确的变体。例如，如果您在基于 ARM 的树莓派上运行多平台镜像，Docker 会选择 `linux/arm64` 变体。如果您在 x86-64 笔记本电脑上运行相同的镜像，Docker 会选择 `linux/amd64` 变体（如果您使用的是 Linux 容器）。

## 前提条件

要构建多平台镜像，您首先需要确保您的 Docker 环境已配置为支持该功能。有两种实现方式：

- 您可以从“经典 (classic)”镜像库切换到 containerd 镜像存储库。
- 您可以创建并使用自定义构建器。

Docker Engine 的“经典”镜像库不支持多平台镜像。切换到 containerd 镜像存储可以确保您的 Docker Engine 能够推送、拉取和构建多平台镜像。

创建一个使用支持多平台驱动（如 `docker-container` 驱动）的自定义构建器，可以让您在不切换镜像库的情况下构建多平台镜像。但是，您仍然无法将构建的多平台镜像加载到 Docker Engine 镜像库中。但您可以直接通过 `docker build --push` 将它们推送到容器注册表。

{{< tabs >}}
{{< tab name="containerd 镜像存储" >}}

启用 containerd 镜像存储的步骤取决于您使用的是 Docker Desktop 还是独立的 Docker Engine：

- 如果您使用的是 Docker Desktop，请在 [Docker Desktop 设置](/manuals/desktop/features/containerd.md) 中启用 containerd 镜像存储。

- 如果您使用的是独立 Docker Engine，请通过 [守护进程配置文件](/manuals/engine/storage/containerd.md) 启用 containerd 镜像存储。

{{< /tab >}}
{{< tab name="自定义构建器" >}}

要创建自定义构建器，请使用 `docker buildx create` 命令创建一个使用 `docker-container` 驱动的构建器。

```console
$ docker buildx create \
  --name container-builder \
  --driver docker-container \
  --bootstrap --use
```

> [!NOTE]
> 使用 `docker-container` 驱动的构建结果不会自动加载到您的 Docker Engine 镜像库中。有关更多信息，请参阅 [构建驱动](/manuals/build/builders/drivers/_index.md)。

{{< /tab >}}
{{< /tabs >}}

如果您使用的是独立 Docker Engine 并且需要通过模拟方式构建多平台镜像，您还需要安装 QEMU，参见 [手动安装 QEMU](#手动安装-qemu)。

## 构建多平台镜像

触发构建时，使用 `--platform` 标志来定义构建输出的目标平台，例如 `linux/amd64` 和 `linux/arm64`：

```console
$ docker build --platform linux/amd64,linux/arm64 .
```

## 构建策略

您可以根据您的使用场景，通过三种不同的策略构建多平台镜像：

1. 使用模拟，通过 [QEMU](#qemu)
2. 使用具有 [多个原生节点](#多个原生节点) 的构建器
3. 使用带有多阶段构建的 [交叉编译 (cross-compilation)](#交叉编译)

### QEMU

如果您的构建器已经支持 QEMU，那么在模拟环境下构建多平台镜像是最简单的起步方式。使用模拟无需更改 Dockerfile，BuildKit 会自动检测可用于模拟的架构。

> [!NOTE]
> 
> 使用 QEMU 进行模拟的速度可能远慢于原生构建，特别是对于编译、压缩或解压等计算密集型任务。
> 
> 如果可能，请改用 [多个原生节点](#多个原生节点) 或 [交叉编译](#交叉编译) 策略。

Docker Desktop 默认支持在模拟环境下运行和构建多平台镜像。由于构建器使用了 Docker Desktop 虚拟机内捆绑的 QEMU，因此无需任何配置。

#### 手动安装 QEMU

如果您在 Docker Desktop 之外使用构建器，例如在 Linux 上使用 Docker Engine，或者使用自定义远程构建器，您需要安装 QEMU 并在宿主机操作系统上注册执行类型。安装 QEMU 的前提条件包括：

- Linux 内核版本 4.8 或更高
- `binfmt-support` 版本 2.1.7 或更高
- QEMU 二进制文件必须是静态编译的，并使用 `fix_binary` 标志注册

使用 [`tonistiigi/binfmt`](https://github.com/tonistiigi/binfmt) 镜像，只需一条命令即可安装 QEMU 并在宿主机上注册执行类型：

```console
$ docker run --privileged --rm tonistiigi/binfmt --install all
```

这将安装 QEMU 二进制文件并将其注册到 [`binfmt_misc`](https://en.wikipedia.org/wiki/Binfmt_misc) 中，从而使 QEMU 能够执行非原生文件格式以进行模拟。

一旦安装了 QEMU 并注册了执行类型，它们在容器内部就是透明工作的。您可以通过检查 `/proc/sys/fs/binfmt_misc/qemu-*` 中的标志是否包含 `F` 来验证注册是否成功。

### 多个原生节点 (Multiple native nodes)

使用多个原生节点能为 QEMU 无法处理的复杂案例提供更好的支持，并提供更佳的性能。

您可以使用 `--append` 标志向构建器添加额外的节点。

以下命令从名为 `node-amd64` 和 `node-arm64` 的 Docker 上下文创建了一个多节点构建器。本示例假设您已经添加了这些上下文。

```console
$ docker buildx create --use --name mybuild node-amd64
mybuild
$ docker buildx create --append --name mybuild node-arm64
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

虽然这种方法优于模拟，但管理多节点构建器会带来设置和维护构建器集群的额外开销。另一种选择是使用 Docker Build Cloud，这是一项在 Docker 基础设施上提供托管多节点构建器的服务。通过 Docker Build Cloud，您可以获得原生的多平台 ARM 和 X86 构建器，而无需承担维护负担。使用云构建器还具有其他优势，例如共享构建缓存。

注册 Docker Build Cloud 后，将构建器添加到您的本地环境并开始构建。

```console
$ docker buildx create --driver cloud <组织名>/<构建器名称>
cloud-<组织名>-<构建器名称>
$ docker build \
  --builder cloud-<组织名>-<构建器名称> \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --tag <镜像名> \
  --push .
```

更多信息请参阅 [Docker Build Cloud](/manuals/build-cloud/_index.md)。

### 交叉编译 (Cross-compilation)

取决于您的项目，如果您使用的编程语言对交叉编译有很好的支持，您可以利用多阶段构建，在构建器的原生架构上为目标平台构建二进制文件。在 Dockerfile 中会自动提供如 `BUILDPLATFORM` 和 `TARGETPLATFORM` 等特殊的构建参数供您使用。

在以下示例中，`FROM` 指令被固定到构建器的原生平台（使用 `--platform=$BUILDPLATFORM` 选项）以防止触发模拟。然后，预定义的 `$BUILDPLATFORM` 和 `$TARGETPLATFORM` 构建参数在 `RUN` 指令中进行插值。在这个例子中，这些值只是通过 `echo` 打印到 stdout，但这演示了您该如何将它们传递给编译器进行交叉编译。

```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log
FROM alpine
COPY --from=build /log /log
```

## 示例

以下是多平台构建的一些示例：

- [使用模拟进行简单的多平台构建](#使用模拟进行简单的多平台构建)
- [使用 Docker Build Cloud 进行多平台 Neovim 构建](#使用-docker-build-cloud-进行多平台-neovim-构建)
- [交叉编译 Go 应用程序](#交叉编译-go-应用程序)

### 使用模拟进行简单的多平台构建

本示例演示如何使用 QEMU 模拟构建一个简单的多平台镜像。该镜像包含一个打印容器架构的单一文件。

前提条件：

- Docker Desktop，或者安装了 [QEMU](#手动安装-qemu) 的 Docker Engine
- 已启用 containerd 镜像存储

步骤：

1. 创建一个空目录并进入：

   ```console
   $ mkdir multi-platform
   $ cd multi-platform
   ```

2. 创建一个简单的 Dockerfile 来打印容器的架构：

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM alpine
   RUN uname -m > /arch
   ```

3. 为 `linux/amd64` 和 `linux/arm64` 构建镜像：

   ```console
   $ docker build --platform linux/amd64,linux/arm64 -t multi-platform .
   ```

4. 运行镜像并打印架构信息：

   ```console
   $ docker run --rm multi-platform cat /arch
   ```

   - 如果您在 x86-64 机器上运行，您应该看到 `x86_64`。
   - 如果您在 ARM 机器上运行，您应该看到 `aarch64`。

### 使用 Docker Build Cloud 进行多平台 Neovim 构建

本示例演示如何运行多平台构建，利用 Docker Build Cloud 为 `linux/amd64` 和 `linux/arm64` 平台编译并导出 [Neovim](https://github.com/neovim/neovim) 二进制文件。

Docker Build Cloud 提供托管的多节点构建器，支持原生多平台构建而无需模拟，使得执行编译等 CPU 密集型任务的速度大大加快。

前提条件：

- 您已 [注册 Docker Build Cloud 并创建了构建器](/manuals/build-cloud/setup.md)

步骤：

1. 创建一个空目录并进入：

   ```console
   $ mkdir docker-build-neovim
   $ cd docker-build-neovim
   ```

2. 创建构建 Neovim 的 Dockerfile。

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM debian:bookworm AS build
   WORKDIR /work
   RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
       --mount=type=cache,target=/var/lib/apt,sharing=locked \
       apt-get update && apt-get install -y \
       build-essential \
       cmake \
       curl \
       gettext \
       ninja-build \
       unzip
   ADD https://github.com/neovim/neovim.git#stable .
   RUN make CMAKE_BUILD_TYPE=RelWithDebInfo
   
   FROM scratch
   COPY --from=build /work/build/bin/nvim /
   ```

3. 使用 Docker Build Cloud 为 `linux/amd64` 和 `linux/arm64` 构建镜像：

   ```console
   $ docker build \
      --builder <云构建器名称> \
      --platform linux/amd64,linux/arm64 \
      --output ./bin .
   ```

   此命令使用云构建器构建镜像，并将二进制文件导出到 `bin` 目录。

4. 验证二进制文件是否已为两个平台构建完成。您应该能在 `linux/amd64` 和 `linux/arm64` 目录下都看到 `nvim` 二进制文件。

   ```console
   $ tree ./bin
   ./bin
   ├── linux_amd64
   │   └── nvim
   └── linux_arm64
       └── nvim
   
   3 directories, 2 files
   ```

### 交叉编译 Go 应用程序

本示例演示如何利用多阶段构建为多个平台交叉编译 Go 应用程序。该应用程序是一个简单的 HTTP 服务器，监听 8080 端口并返回容器的架构信息。本示例使用 Go 语言，但相同的原则也适用于其他支持交叉编译的编程语言。

配合 Docker 构建进行交叉编译的工作原理是利用一系列预定义的（在 BuildKit 中）构建参数，这些参数为您提供关于构建器平台和构建目标平台的信息。您可以使用这些预定义参数将平台信息传递给编译器。

在 Go 中，您可以使用 `GOOS` 和 `GOARCH` 环境变量来指定要构建的目标平台。

前提条件：

- Docker Desktop 或 Docker Engine

步骤：

1. 创建一个空目录并进入：

   ```console
   $ mkdir go-server
   $ cd go-server
   ```

2. 创建构建 Go 应用程序的基础 Dockerfile：

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM golang:alpine AS build
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   RUN go build -o server .
   
   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   这个 Dockerfile 目前还无法通过交叉编译实现多平台构建。如果您尝试用 `docker build` 构建此 Dockerfile，构建器将尝试使用模拟技术为指定平台构建镜像。

3. 为了增加交叉编译支持，更新 Dockerfile 以使用预定义的 `BUILDPLATFORM` 和 `TARGETPLATFORM` 构建参数。当您在 `docker build` 中使用 `--platform` 标志时，这些参数在 Dockerfile 中是自动可用的。

   - 使用 `--platform=$BUILDPLATFORM` 选项将 `golang` 镜像固定到构建器的平台。
   - 为 Go 编译阶段添加 `ARG` 指令，使 `TARGETOS` 和 `TARGETARCH` 构建参数对该阶段的命令可用。
   - 将 `GOOS` 和 `GOARCH` 环境变量设置为 `TARGETOS` 和 `TARGETARCH` 的值。Go 编译器利用这些变量执行交叉编译。

   {{< tabs >}}
   {{< tab name="更新后的 Dockerfile" >}}

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM --platform=$BUILDPLATFORM golang:alpine AS build
   ARG TARGETOS
   ARG TARGETARCH
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .
   
   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   {{< /tab >}}
   {{< tab name="旧的 Dockerfile" >}}

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM golang:alpine AS build
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   RUN go build -o server .
   
   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   {{< /tab >}}
   {{< tab name="差异对比 (Diff)" >}}

   ```diff
   # syntax=docker/dockerfile:1
   -FROM golang:alpine AS build
   +FROM --platform=$BUILDPLATFORM golang:alpine AS build
   +ARG TARGETOS
   +ARG TARGETARCH
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   -RUN go build -o server .
   +RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .
   
   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   {{< /tab >}}
   {{< /tabs >}}

4. 为 `linux/amd64` 和 `linux/arm64` 构建镜像：

   ```console
   $ docker build --platform linux/amd64,linux/arm64 -t go-server .
   ```

本示例展示了如何配合 Docker 构建为多个平台交叉编译 Go 应用程序。执行交叉编译的具体步骤可能会因您使用的编程语言而异。请咨询您所用编程语言的文档，了解更多关于针对不同平台进行交叉编译的信息。

> [!TIP]
> 您可能还想了解一下 [xx - Dockerfile 交叉编译辅助工具](https://github.com/tonistiigi/xx)。`xx` 是一个包含实用脚本的 Docker 镜像，能让配合 Docker 构建执行交叉编译变得更加容易。