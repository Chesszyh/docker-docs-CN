---
title: Docker Build 概览
weight: 10
description: 了解 Docker Build 及其组件。
keywords: build, buildkit, buildx, 架构
aliases:
- /build/install-buildx/
- /build/architecture/
---

Docker Build 采用了客户端-服务器架构，其中：

- 客户端：Buildx 是运行和管理构建的客户端和用户界面。
- 服务器：BuildKit 是处理构建执行的服务器，即构建器。

当您启动构建时，Buildx 客户端会向 BuildKit 后端发送构建请求。BuildKit 解析构建指令并执行构建步骤。构建输出要么发送回客户端，要么上传到镜像库（如 Docker Hub）。

Buildx 和 BuildKit 均随 Docker Desktop 和 Docker Engine 开箱即用。当您调用 `docker build` 命令时，您正在使用 Buildx 通过 Docker 捆绑的默认 BuildKit 运行构建。

## Buildx

Buildx 是用于运行构建的 CLI 工具。`docker build` 命令是 Buildx 的包装器。当您调用 `docker build` 时，Buildx 会解释构建选项并将构建请求发送到 BuildKit 后端。

Buildx 客户端的功能不仅仅是运行构建。您还可以使用 Buildx 创建和管理 BuildKit 后端（称为构建器）。它还支持管理镜像库中的镜像，以及并发运行多个构建。

Docker Buildx 默认随 Docker Desktop 安装。您也可以从源码构建 CLI 插件，或者从 GitHub 仓库获取二进制文件并手动安装。有关更多信息，请参阅 GitHub 上的 [Buildx README](https://github.com/docker/buildx#manual-download)。

> [!NOTE]
> 虽然 `docker build` 在后台调用了 Buildx，但该命令与标准的 `docker buildx build` 之间存在细微差别。详情请参阅 [`docker build` 与 `docker buildx build` 的区别](../builders/_index.md#difference-between-docker-build-and-docker-buildx-build)。

## BuildKit

BuildKit 是执行构建工作负载的守护进程。

构建执行始于调用 `docker build` 命令。Buildx 解析您的构建命令并将构建请求发送到 BuildKit 后端。构建请求包括：

- Dockerfile
- 构建参数
- 导出选项
- 缓存选项

BuildKit 解析构建指令并执行构建步骤。在 BuildKit 执行构建时，Buildx 会监控构建状态并将进度打印到终端。

如果构建需要来自客户端的资源（如本地文件或构建密钥），BuildKit 会向 Buildx 请求它所需的资源。

这是 BuildKit 与早期 Docker 版本中使用的传统构建器相比更高效的一个方面。BuildKit 仅在需要时才请求构建所需的资源。相比之下，传统构建器总是获取本地文件系统的副本。

BuildKit 可以向 Buildx 请求的资源示例包括：

- 本地文件系统构建上下文
- 构建密钥
- SSH 套接字 (sockets)
- 镜像库身份验证令牌

有关 BuildKit 的更多信息，请参阅 [BuildKit](/manuals/build/buildkit/_index.md)。
