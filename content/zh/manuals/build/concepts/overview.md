---
title: Docker Build 概览
weight: 10
description: 了解 Docker Build 及其组成部分。
keywords: build, buildkit, buildx, architecture, 架构
aliases:
- /build/install-buildx/
- /build/architecture/
---

Docker Build 采用客户端-服务器架构，其中：

- **客户端 (Client)**：Buildx 是用于运行和管理构建任务的客户端及用户界面。
- **服务器 (Server)**：BuildKit 是处理构建执行的服务器，也就是构建器 (builder)。

当您调用构建任务时，Buildx 客户端向 BuildKit 后端发送构建请求。BuildKit 解析构建指令并执行构建步骤。构建输出要么发回给客户端，要么上传到 Docker Hub 等注册表中。

Buildx 和 BuildKit 都是 Docker Desktop 和 Docker Engine 的开箱即用组件。当您调用 `docker build` 命令时，您实际上是在使用 Buildx 配合 Docker 捆绑的默认 BuildKit 运行构建任务。

## Buildx

Buildx 是您用于运行构建的 CLI 工具。`docker build` 命令是 Buildx 的一个封装。当您执行 `docker build` 时，Buildx 会解释构建选项并将构建请求发送到 BuildKit 后端。

Buildx 客户端不仅能运行构建。您还可以使用 Buildx 创建和管理 BuildKit 后端（称为构建器）。它还支持管理注册表中的镜像以及并发运行多个构建任务等功能。

Docker Buildx 默认随 Docker Desktop 安装。您也可以从源码构建该 CLI 插件，或从 GitHub 仓库获取二进制文件并手动安装。更多信息请参阅 GitHub 上的 [Buildx README](https://github.com/docker/buildx#manual-download)。

> [!NOTE]
> 虽然 `docker build` 在底层调用了 Buildx，但该命令与标准的 `docker buildx build` 之间存在细微差异。详情请参阅 [`docker build` 与 `docker buildx build` 的区别](../builders/_index.md#docker-build-与-docker-buildx-build-的区别)。

## BuildKit

BuildKit 是执行构建负载的守护进程。

构建执行始于调用 `docker build` 命令。Buildx 解释您的 build 命令并将构建请求发送到 BuildKit 后端。构建请求包括：

- Dockerfile
- 构建参数 (Build arguments)
- 导出选项 (Export options)
- 缓存选项 (Caching options)

BuildKit 解析构建指令并执行构建步骤。在 BuildKit 执行构建期间，Buildx 监控构建状态并将进度打印到终端。

如果构建需要来自客户端的资源（如本地文件或构建机密），BuildKit 会向 Buildx 请求其所需的资源。

这也是 BuildKit 比早期 Docker 版本使用的旧版构建器更高效的原因之一。BuildKit 仅在需要时请求构建所需的资源。相比之下，旧版构建器总是会对本地文件系统进行完整备份。

BuildKit 可能向 Buildx 请求的资源示例包括：

- 本地文件系统构建上下文
- 构建机密 (Build secrets)
- SSH 套接字
- 注册表身份验证令牌

有关 BuildKit 的更多信息，请参阅 [BuildKit](/manuals/build/buildkit/_index.md)。