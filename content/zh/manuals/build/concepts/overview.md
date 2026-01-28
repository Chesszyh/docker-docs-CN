---
title: Docker Build 概述
weight: 10
description: 了解 Docker Build 及其组件。
keywords: build, buildkit, buildx, architecture
aliases:
- /build/install-buildx/
- /build/architecture/
---

Docker Build 实现了客户端-服务器架构，其中：

- 客户端：Buildx 是客户端，是运行和管理构建的用户界面。
- 服务器：BuildKit 是服务器（或称为构建器），处理构建执行。

当您调用构建时，Buildx 客户端向 BuildKit 后端发送构建请求。BuildKit 解析构建指令并执行构建步骤。构建输出要么发送回客户端，要么上传到注册表（如 Docker Hub）。

Buildx 和 BuildKit 都与 Docker Desktop 和 Docker Engine 一起开箱即用。当您调用 `docker build` 命令时，您正在使用 Buildx 运行构建，使用与 Docker 捆绑的默认 BuildKit。

## Buildx

Buildx 是您用来运行构建的 CLI 工具。`docker build` 命令是 Buildx 的包装器。当您调用 `docker build` 时，Buildx 解释构建选项并向 BuildKit 后端发送构建请求。

Buildx 客户端不仅可以运行构建。您还可以使用 Buildx 创建和管理 BuildKit 后端（称为构建器）。它还支持管理注册表中的镜像以及同时运行多个构建的功能。

Docker Buildx 默认与 Docker Desktop 一起安装。您也可以从源代码构建 CLI 插件，或从 GitHub 仓库获取二进制文件并手动安装。有关更多信息，请参阅 GitHub 上的 [Buildx README](https://github.com/docker/buildx#manual-download)。

> [!NOTE]
> 虽然 `docker build` 在底层调用 Buildx，但此命令与标准的 `docker buildx build` 之间存在细微差异。有关详细信息，请参阅 [`docker build` 和 `docker buildx build` 的区别](../builders/_index.md#difference-between-docker-build-and-docker-buildx-build)。

## BuildKit

BuildKit 是执行构建工作负载的守护进程。

构建执行从调用 `docker build` 命令开始。Buildx 解释您的构建命令并向 BuildKit 后端发送构建请求。构建请求包括：

- Dockerfile
- 构建参数
- 导出选项
- 缓存选项

BuildKit 解析构建指令并执行构建步骤。当 BuildKit 执行构建时，Buildx 监控构建状态并将进度打印到终端。

如果构建需要来自客户端的资源（如本地文件或构建密钥），BuildKit 会向 Buildx 请求所需的资源。

这是 BuildKit 比早期 Docker 版本中使用的传统构建器更高效的一种方式。BuildKit 只在需要时请求构建所需的资源。相比之下，传统构建器总是复制整个本地文件系统。

BuildKit 可以向 Buildx 请求的资源示例包括：

- 本地文件系统构建上下文
- 构建密钥
- SSH 套接字
- 注册表身份验证令牌

有关 BuildKit 的更多信息，请参阅 [BuildKit](/manuals/build/buildkit/_index.md)。
