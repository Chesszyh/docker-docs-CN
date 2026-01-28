---
title: 为您的 C++ 应用程序创建多阶段构建
linkTitle: 使用多阶段构建容器化您的应用
weight: 5
keywords: C++, containerize, multi-stage
description: 学习如何为 C++ 应用程序创建多阶段构建。
aliases:
- /language/cpp/multistage/
- /guides/language/cpp/multistage/
---

## 前提条件

- 您需要有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 概述

本节将引导您为 C++ 应用程序创建多阶段 Docker 构建。
多阶段构建是 Docker 的一项功能，它允许您在构建过程的不同阶段使用不同的基础镜像，
从而优化最终镜像的大小，并将构建依赖与运行时依赖分离。

对于像 C++ 这样的编译型语言，标准做法是设置一个编译代码的构建阶段和一个运行编译后二进制文件的运行时阶段，
因为构建依赖在运行时不需要。

## 获取示例应用程序

让我们使用一个简单的 C++ 应用程序，它在终端打印 `Hello, World!`。为此，请克隆示例仓库以配合本指南使用：

```bash
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

本节的示例位于仓库的 `hello` 目录中。进入该目录并查看文件：

```bash
$ cd c-plus-plus-docker/hello
$ ls
```

您应该看到以下文件：

```text
Dockerfile  hello.cpp
```

## 检查 Dockerfile

在 IDE 或文本编辑器中打开 `Dockerfile`。`Dockerfile` 包含构建 Docker 镜像的指令。

```Dockerfile
# Stage 1: Build stage
FROM ubuntu:latest AS build

# Install build-essential for compiling C++ code
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Copy the source code into the container
COPY hello.cpp .

# Compile the C++ code statically to ensure it doesn't depend on runtime libraries
RUN g++ -o hello hello.cpp -static

# Stage 2: Runtime stage
FROM scratch

# Copy the static binary from the build stage
COPY --from=build /app/hello /hello

# Command to run the binary
CMD ["/hello"]
```

`Dockerfile` 有两个阶段：

1. **构建阶段**：此阶段使用 `ubuntu:latest` 镜像来编译 C++ 代码并创建静态二进制文件。
2. **运行时阶段**：此阶段使用 `scratch` 镜像（一个空镜像），从构建阶段复制静态二进制文件并运行它。

## 构建 Docker 镜像

要构建 Docker 镜像，请在 `hello` 目录中运行以下命令：

```bash
$ docker build -t hello .
```

`-t` 标志将镜像标记为名称 `hello`。

## 运行 Docker 容器

要运行 Docker 容器，请使用以下命令：

```bash
$ docker run hello
```

您应该在终端中看到输出 `Hello, World!`。

## 总结

在本节中，您学习了如何为 C++ 应用程序创建多阶段构建。多阶段构建帮助您优化最终镜像的大小，并将构建依赖与运行时依赖分离。
在这个示例中，最终镜像只包含静态二进制文件，不包含任何构建依赖。

由于镜像的基础是空的，常用的操作系统工具也不存在。因此，例如，您无法在容器中运行简单的 `ls` 命令：

```bash
$ docker run hello ls
```

这使得镜像非常轻量且安全。
