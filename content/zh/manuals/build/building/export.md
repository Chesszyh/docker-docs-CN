---
title: 导出二进制文件
weight: 50
description: 使用 Docker 构建来创建并导出可执行二进制文件
keywords: build, buildkit, buildx, 指南, 教程, 构建参数, arg
aliases:
  - /build/guide/export/
---

您知道可以使用 Docker 将应用程序构建为独立的二进制文件吗？有时，您不想将应用程序打包并分发为 Docker 镜像。使用 Docker 构建您的应用程序，并使用导出器（exporters）将输出保存到磁盘。

`docker build` 的默认输出格式是容器镜像。该镜像会自动加载到您的本地镜像库中，您可以在那里从该镜像运行容器，或者将其推送到镜像库。在后台，这使用了默认的导出器，即 `docker` 导出器。

要将构建结果导出为文件，可以使用 `--output` 标志（或简称 `-o`）。`--output` 标志允许您更改构建的输出格式。

## 从构建中导出二进制文件

如果您在 `docker build --output` 标志中指定了一个文件路径，Docker 会在构建结束时将构建容器的内容导出到宿主机文件系统的指定位置。这使用的是 `local`（本地）[导出器](/manuals/build/exporters/local-tar.md)。

这种做法的巧妙之处在于，您可以利用 Docker 强大的隔离和构建功能来创建独立的二进制文件。这非常适合 Go、Rust 以及其他可以编译为单个二进制文件的语言。

以下示例创建了一个打印 "Hello, World!" 的简单 Rust 程序，并将二进制文件导出到宿主机文件系统。

1. 为此示例创建一个新目录并进入该目录：

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
   > `COPY <<EOT` 语法是一个 [here-document（在此文档）](/reference/dockerfile.md#here-documents)。它允许您在 Dockerfile 中编写多行字符串。在这里，它用于在 Dockerfile 中内联创建一个简单的 Rust 程序。

   此 Dockerfile 使用多阶段构建，在第一阶段编译程序，然后在第二阶段将二进制文件复制到 scratch 镜像中。最终镜像是仅包含二进制文件的最小镜像。对于不需要完整操作系统即可运行的程序，使用 `scratch` 镜像来创建最小化构建产物是常见的做法。

3. 构建 Dockerfile 并将二进制文件导出到当前工作目录：

   ```console
   $ docker build --output=. .
   ```

   此命令构建 Dockerfile 并将二进制文件导出到当前工作目录。该二进制文件名为 `hello`，并在当前工作目录中创建。

## 导出多平台构建

您可以将 `local` 导出器与 [多平台构建](/manuals/build/building/multi-platform.md) 结合使用来导出二进制文件。只要您使用的编译器支持目标平台，这就能让您一次性编译多个可运行在任何架构机器上的二进制文件。

延续 [从构建中导出二进制文件](#从构建中导出二进制文件) 节中的 Dockerfile 示例：

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

您可以使用带有 `--platform` 标志的 `docker build` 命令为多个平台构建此 Rust 程序。结合 `--output` 标志，构建会将每个目标的二进制文件导出到指定目录。

例如，同时为 `linux/amd64` 和 `linux/arm64` 构建该程序：

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

## 其他信息

除了 `local` 导出器外，还有其他导出器可用。要了解更多关于可用导出器及其使用方法的信息，请参阅 [导出器 (Exporters)](/manuals/build/exporters/_index.md) 文档。
