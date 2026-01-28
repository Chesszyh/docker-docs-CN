---
title: 多平台构建
linkTitle: 多平台
weight: 40
description: 介绍什么是多平台构建以及如何使用 Docker Buildx 执行它们。
keywords: build, buildx, buildkit, multi-platform, cross-platform, cross-compilation, emulation, QEMU, ARM, x86, Windows, Linux, macOS
aliases:
- /build/buildx/multiplatform-images/
- /desktop/multi-arch/
- /docker-for-mac/multi-arch/
- /mackit/multi-arch/
- /build/guide/multi-platform/
---

多平台构建（multi-platform build）是指针对多个不同操作系统或 CPU 架构组合的单次构建调用。在构建镜像时，这让你可以创建一个可以在多个平台上运行的单一镜像，例如 `linux/amd64`、`linux/arm64` 和 `windows/amd64`。

## 为什么需要多平台构建？

Docker 通过将应用程序及其依赖项打包到容器中来解决"在我的机器上可以工作"的问题。这使得在不同环境（如开发、测试和生产环境）中运行相同的应用程序变得容易。

但容器化本身只解决了部分问题。容器共享主机内核，这意味着容器内运行的代码必须与主机架构兼容。这就是为什么你不能在 arm64 主机上运行 `linux/amd64` 容器（不使用模拟），或者在 Linux 主机上运行 Windows 容器。

多平台构建通过将同一应用程序的多个变体打包到单个镜像中来解决这个问题。这使你能够在不同类型的硬件上运行相同的镜像，例如运行 x86-64 的开发机器或云中基于 ARM 的 Amazon EC2 实例，而无需模拟。

### 单平台镜像和多平台镜像的区别

多平台镜像的结构与单平台镜像不同。单平台镜像包含一个指向单个配置和单组层的清单。多平台镜像包含一个清单列表，指向多个清单，每个清单指向不同的配置和层集。

![多平台镜像结构](/build/images/single-vs-multiplatform-image.svg)

当你将多平台镜像推送到注册表时，注册表会存储清单列表和所有单独的清单。当你拉取镜像时，注册表返回清单列表，Docker 会根据主机架构自动选择正确的变体。例如，如果你在基于 ARM 的 Raspberry Pi 上运行多平台镜像，Docker 会选择 `linux/arm64` 变体。如果你在 x86-64 笔记本电脑上运行相同的镜像，Docker 会选择 `linux/amd64` 变体（如果你使用的是 Linux 容器）。

## 前提条件

要构建多平台镜像，你首先需要确保你的 Docker 环境已设置为支持它。有两种方法可以做到这一点：

- 你可以从"经典"镜像存储切换到 containerd 镜像存储。
- 你可以创建并使用自定义构建器。

Docker 引擎的"经典"镜像存储不支持多平台镜像。切换到 containerd 镜像存储可确保你的 Docker 引擎可以推送、拉取和构建多平台镜像。

创建使用支持多平台的驱动程序（如 `docker-container` 驱动程序）的自定义构建器，将让你无需切换到不同的镜像存储即可构建多平台镜像。但是，你仍然无法将构建的多平台镜像加载到 Docker 引擎镜像存储中。不过，你可以使用 `docker build --push` 直接将它们推送到容器注册表。

{{< tabs >}}
{{< tab name="containerd 镜像存储" >}}

启用 containerd 镜像存储的步骤取决于你使用的是 Docker Desktop 还是独立的 Docker Engine：

- 如果你使用 Docker Desktop，在 [Docker Desktop 设置](/manuals/desktop/features/containerd.md)中启用 containerd 镜像存储。

- 如果你使用独立的 Docker Engine，使用[守护程序配置文件](/manuals/engine/storage/containerd.md)启用 containerd 镜像存储。

{{< /tab >}}
{{< tab name="自定义构建器" >}}

要创建自定义构建器，使用 `docker buildx create` 命令创建一个使用 `docker-container` 驱动程序的构建器。

```console
$ docker buildx create \
  --name container-builder \
  --driver docker-container \
  --bootstrap --use
```

> [!NOTE]
> 使用 `docker-container` 驱动程序的构建不会自动加载到你的 Docker 引擎镜像存储中。有关更多信息，请参阅[构建驱动程序](/manuals/build/builders/drivers/_index.md)。

{{< /tab >}}
{{< /tabs >}}

如果你使用独立的 Docker Engine 并且需要使用模拟构建多平台镜像，你还需要安装 QEMU，请参阅[手动安装 QEMU](#手动安装-qemu)。

## 构建多平台镜像

触发构建时，使用 `--platform` 标志定义构建输出的目标平台，例如 `linux/amd64` 和 `linux/arm64`：

```console
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

## 策略

你可以使用三种不同的策略构建多平台镜像，具体取决于你的用例：

1. 使用 [QEMU](#qemu) 进行模拟
2. 使用具有[多个原生节点](#多个原生节点)的构建器
3. 使用多阶段构建进行[交叉编译](#交叉编译)

### QEMU

使用 QEMU 进行模拟构建多平台镜像是最简单的入门方式，前提是你的构建器已经支持它。使用模拟不需要修改你的 Dockerfile，BuildKit 会自动检测可用于模拟的架构。

> [!NOTE]
>
> 使用 QEMU 进行模拟可能比原生构建慢得多，特别是对于编译和压缩或解压缩等计算密集型任务。
>
> 如果可能，请改用[多个原生节点](#多个原生节点)或[交叉编译](#交叉编译)。

Docker Desktop 默认支持在模拟下运行和构建多平台镜像。不需要配置，因为构建器使用 Docker Desktop 虚拟机中捆绑的 QEMU。

#### 手动安装 QEMU

如果你使用 Docker Desktop 之外的构建器，例如在 Linux 上使用 Docker Engine 或使用自定义远程构建器，你需要在主机操作系统上安装 QEMU 并注册可执行类型。安装 QEMU 的前提条件是：

- Linux 内核版本 4.8 或更高
- `binfmt-support` 版本 2.1.7 或更高
- QEMU 二进制文件必须静态编译并使用 `fix_binary` 标志注册

使用 [`tonistiigi/binfmt`](https://github.com/tonistiigi/binfmt) 镜像通过单个命令在主机上安装 QEMU 并注册可执行类型：

```console
$ docker run --privileged --rm tonistiigi/binfmt --install all
```

这会安装 QEMU 二进制文件并将它们注册到 [`binfmt_misc`](https://en.wikipedia.org/wiki/Binfmt_misc)，使 QEMU 能够执行非原生文件格式以进行模拟。

一旦在主机操作系统上安装了 QEMU 并注册了可执行类型，它们就可以在容器内透明地工作。你可以通过检查 `/proc/sys/fs/binfmt_misc/qemu-*` 中的标志是否包含 `F` 来验证你的注册。

### 多个原生节点

使用多个原生节点可以为 QEMU 无法处理的更复杂情况提供更好的支持，并且性能也更好。

你可以使用 `--append` 标志向构建器添加额外的节点。

以下命令从名为 `node-amd64` 和 `node-arm64` 的 Docker 上下文创建多节点构建器。此示例假设你已经添加了这些上下文。

```console
$ docker buildx create --use --name mybuild node-amd64
mybuild
$ docker buildx create --append --name mybuild node-arm64
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

虽然这种方法比模拟有优势，但管理多节点构建器会引入设置和管理构建器集群的一些开销。或者，你可以使用 Docker Build Cloud，这是一项在 Docker 基础设施上提供托管多节点构建器的服务。使用 Docker Build Cloud，你可以获得原生的多平台 ARM 和 X86 构建器，而无需承担维护它们的负担。使用云构建器还提供额外的好处，例如共享构建缓存。

注册 Docker Build Cloud 后，将构建器添加到你的本地环境并开始构建。

```console
$ docker buildx create --driver cloud <ORG>/<BUILDER_NAME>
cloud-<ORG>-<BUILDER_NAME>
$ docker build \
  --builder cloud-<ORG>-<BUILDER_NAME> \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --tag <IMAGE_NAME> \
  --push .
```

有关更多信息，请参阅 [Docker Build Cloud](/manuals/build-cloud/_index.md)。

### 交叉编译

根据你的项目，如果你使用的编程语言对交叉编译有良好的支持，你可以利用多阶段构建从构建器的原生架构为目标平台构建二进制文件。特殊的构建参数（如 `BUILDPLATFORM` 和 `TARGETPLATFORM`）会自动在你的 Dockerfile 中可用。

在以下示例中，`FROM` 指令被固定到构建器的原生平台（使用 `--platform=$BUILDPLATFORM` 选项）以防止模拟启动。然后预定义的 `$BUILDPLATFORM` 和 `$TARGETPLATFORM` 构建参数在 `RUN` 指令中被插值。在这种情况下，这些值只是用 `echo` 打印到标准输出，但这说明了如何将它们传递给编译器进行交叉编译。

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

以下是一些多平台构建的示例：

- [使用模拟的简单多平台构建](#使用模拟的简单多平台构建)
- [使用 Docker Build Cloud 的多平台 Neovim 构建](#使用-docker-build-cloud-的多平台-neovim-构建)
- [交叉编译 Go 应用程序](#交叉编译-go-应用程序)

### 使用模拟的简单多平台构建

此示例演示如何使用 QEMU 模拟构建简单的多平台镜像。该镜像包含一个打印容器架构的单个文件。

前提条件：

- Docker Desktop，或安装了 [QEMU](#手动安装-qemu) 的 Docker Engine
- 已启用 containerd 镜像存储

步骤：

1. 创建一个空目录并导航到该目录：

   ```console
   $ mkdir multi-platform
   $ cd multi-platform
   ```

2. 创建一个打印容器架构的简单 Dockerfile：

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM alpine
   RUN uname -m > /arch
   ```

3. 为 `linux/amd64` 和 `linux/arm64` 构建镜像：

   ```console
   $ docker build --platform linux/amd64,linux/arm64 -t multi-platform .
   ```

4. 运行镜像并打印架构：

   ```console
   $ docker run --rm multi-platform cat /arch
   ```

   - 如果你在 x86-64 机器上运行，你应该看到 `x86_64`。
   - 如果你在 ARM 机器上运行，你应该看到 `aarch64`。

### 使用 Docker Build Cloud 的多平台 Neovim 构建

此示例演示如何使用 Docker Build Cloud 运行多平台构建，为 `linux/amd64` 和 `linux/arm64` 平台编译和导出 [Neovim](https://github.com/neovim/neovim) 二进制文件。

Docker Build Cloud 提供托管的多节点构建器，支持原生多平台构建而无需模拟，使编译等 CPU 密集型任务更快。

前提条件：

- 你已[注册 Docker Build Cloud 并创建了构建器](/manuals/build-cloud/setup.md)

步骤：

1. 创建一个空目录并导航到该目录：

   ```console
   $ mkdir docker-build-neovim
   $ cd docker-build-neovim
   ```

2. 创建一个构建 Neovim 的 Dockerfile。

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
      --builder <cloud-builder> \
      --platform linux/amd64,linux/arm64 \
      --output ./bin .
   ```

   此命令使用云构建器构建镜像并将二进制文件导出到 `bin` 目录。

4. 验证两个平台的二进制文件都已构建。你应该看到 `linux/amd64` 和 `linux/arm64` 的 `nvim` 二进制文件。

   ```console
   $ tree ./bin
   ./bin
   ├── linux_amd64
   │   └── nvim
   └── linux_arm64
       └── nvim

   3 directories, 2 files
   ```

### 交叉编译 Go 应用程序

此示例演示如何使用多阶段构建为多个平台交叉编译 Go 应用程序。该应用程序是一个简单的 HTTP 服务器，监听端口 8080 并返回容器的架构。此示例使用 Go，但相同的原则适用于支持交叉编译的其他编程语言。

使用 Docker 构建进行交叉编译的工作原理是利用一系列预定义的（在 BuildKit 中）构建参数，这些参数为你提供有关构建器和构建目标平台的信息。你可以使用这些预定义的参数将平台信息传递给编译器。

在 Go 中，你可以使用 `GOOS` 和 `GOARCH` 环境变量指定要构建的目标平台。

前提条件：

- Docker Desktop 或 Docker Engine

步骤：

1. 创建一个空目录并导航到该目录：

   ```console
   $ mkdir go-server
   $ cd go-server
   ```

2. 创建一个构建 Go 应用程序的基础 Dockerfile：

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

   这个 Dockerfile 还不能使用交叉编译构建多平台。如果你尝试使用 `docker build` 构建这个 Dockerfile，构建器会尝试使用模拟为指定平台构建镜像。

3. 要添加交叉编译支持，更新 Dockerfile 以使用预定义的 `BUILDPLATFORM` 和 `TARGETPLATFORM` 构建参数。当你使用 `docker build` 的 `--platform` 标志时，这些参数会自动在 Dockerfile 中可用。

   - 使用 `--platform=$BUILDPLATFORM` 选项将 `golang` 镜像固定到构建器的平台。
   - 为 Go 编译阶段添加 `ARG` 指令，使 `TARGETOS` 和 `TARGETARCH` 构建参数在此阶段的命令中可用。
   - 将 `GOOS` 和 `GOARCH` 环境变量设置为 `TARGETOS` 和 `TARGETARCH` 的值。Go 编译器使用这些变量进行交叉编译。

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
   {{< tab name="旧 Dockerfile" >}}

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
   {{< tab name="差异" >}}

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

此示例展示了如何使用 Docker 构建为多个平台交叉编译 Go 应用程序。如何进行交叉编译的具体步骤可能因你使用的编程语言而异。请查阅你的编程语言文档以了解更多关于为不同平台进行交叉编译的信息。

> [!TIP]
> 你可能还想查看 [xx - Dockerfile 交叉编译辅助工具](https://github.com/tonistiigi/xx)。
> `xx` 是一个包含实用脚本的 Docker 镜像，可以使 Docker 构建的交叉编译更容易。
