---
title: 导出二进制文件
weight: 50
description: 使用 Docker build 创建并导出可执行二进制文件
keywords: build, buildkit, buildx, guide, tutorial, build arguments, arg, 导出, 二进制文件
aliases:
  - /build/guide/export/
---

您知道可以使用 Docker 将应用程序构建为独立的二进制文件吗？有时，您并不想将应用程序作为 Docker 镜像进行打包和分发。使用 Docker 构建您的应用程序，并使用导出器（exporters）将输出保存到磁盘上。

`docker build` 的默认输出格式是容器镜像。该镜像会被自动加载到您的本地镜像库中，您可以从中运行容器，或将其推送到注册表。在底层，这使用的是名为 `docker` 的默认导出器。

如果您想将构建结果导出为文件，可以使用 `--output` 标志（简写为 `-o`）。`--output` 标志允许您更改构建的输出格式。

## 从构建中导出二进制文件

如果您为 `docker build --output` 标志指定了一个文件路径，Docker 会在构建结束时将构建容器的内容导出到宿主机文件系统上的指定位置。这使用的是 `local` [导出器](/manuals/build/exporters/local-tar.md)。

这种做法的巧妙之处在于，您可以利用 Docker 强大的隔离性和构建特性来创建独立的二进制文件。这非常适合 Go、Rust 以及其他可以编译为单个二进制文件的语言。

以下示例创建了一个简单的 Rust 程序，打印 "Hello, World!"，并将生成的二进制文件导出到宿主机文件系统中。

1. 为本示例创建一个新目录并进入：

   ```console
   $ mkdir hello-world-bin
   $ cd hello-world-bin
   ```

2. 创建一个包含以下内容的 Dockerfile：

   ```Dockerfile
   # syntax=docker/dockerfile:1
   FROM rust:alpine AS build
   WORKDIR /src
   COPY <<EOT hello.rs
   fn main() {
       println!("Hello World!");
   }
   EOT
   RUN rustc -o /bin/hello hello.rs
   
   FROM scratch
   COPY --from=build /bin/hello /
   ENTRYPOINT ["/hello"]
   ```

   > [!TIP]
   > `COPY <<EOT` 语法是一个 [here-document](/reference/dockerfile.md#here-documents)。它允许您在 Dockerfile 中编写多行字符串。在这里，它被用于在 Dockerfile 中内联创建一个简单的 Rust 程序。

   此 Dockerfile 使用多阶段构建，在第一阶段编译程序，在第二阶段将二进制文件复制到 scratch 镜像中。最终生成的镜像是仅包含二进制文件的最小化镜像。对于不需要完整操作系统即可运行的程序，使用 `scratch` 镜像来创建最小化构建产物是一种常见的做法。

3. 构建 Dockerfile 并将二进制文件导出到当前工作目录：

   ```console
   $ docker build --output=. .
   ```

   此命令构建 Dockerfile 并将二进制文件导出到当前工作目录。二进制文件名为 `hello`，并创建在当前工作目录中。

## 导出多平台构建结果

您可以结合使用 `local` 导出器和 [多平台构建](/manuals/build/building/multi-platform.md) 来导出二进制文件。只要您使用的编译器支持目标平台，这允许您一次性编译多个二进制文件，并可在任何架构的任何机器上运行。

继续使用[从构建中导出二进制文件](#从构建中导出二进制文件)部分的示例 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM rust:alpine AS build
WORKDIR /src
COPY <<EOT hello.rs
fn main() {
    println!("Hello World!");
}
EOT
RUN rustc -o /bin/hello hello.rs

FROM scratch
COPY --from=build /bin/hello /
ENTRYPOINT ["/hello"]
```

您可以在 `docker build` 命令中使用 `--platform` 标志为多个平台构建此 Rust 程序。配合 `--output` 标志，构建任务会将每个目标的二进制文件导出到指定的目录。

例如，同时为 `linux/amd64` 和 `linux/arm64` 构建程序：

```console
$ docker build --platform=linux/amd64,linux/arm64 --output=out .
$ tree out/
out/
├── linux_amd64
│   └── hello
└── linux_arm64
    └── hello

3 directories, 2 files
```

## 额外信息

除了 `local` 导出器外，还有其他可用的导出器。要了解更多关于可用导出器及其使用方法的信息，请参阅 [导出器 (Exporters)](/manuals/build/exporters/_index.md) 文档。