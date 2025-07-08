---
title: Docker MCP 目录
description: 了解 MCP 目录的优势、如何使用它以及如何贡献
keywords: docker hub, mcp, mcp 服务器, ai 代理, 目录, docker
---

[Docker MCP 目录](https://hub.docker.com/mcp) 是一个集中式、可信的注册表，用于发现、共享和运行 MCP 兼容工具。它无缝集成到 Docker Hub 中，提供经过验证、版本化和精选的 MCP 服务器，这些服务器打包为 Docker 镜像。该目录也可在 Docker Desktop 中使用。

该目录解决了常见的 MCP 服务器挑战：

- 环境冲突：工具通常需要特定的运行时，这可能与现有设置冲突。
- 缺乏隔离：传统设置存在暴露主机系统的风险。
- 设置复杂性：手动安装和配置导致采用缓慢。
- 跨平台不一致：工具在不同的操作系统上可能表现不可预测。

通过 Docker，每个 MCP 服务器都作为独立的容器运行，因此它具有可移植性、隔离性和一致性。您可以使用 Docker CLI 或 Docker Desktop 即时启动工具，无需担心依赖项或兼容性。

## 主要功能

- 超过 100 个经过验证的 MCP 服务器集中在一个地方
- 发布者验证和版本化发布
- 使用 Docker 基础设施进行拉取式分发
- 由 New Relic、Stripe、Grafana 等合作伙伴提供的工具

## 工作原理

MCP 目录中的每个工具都打包为带有元数据的 Docker 镜像：

- 通过 Docker Hub 在 `mcp/` 命名空间下发现工具。
- 通过 [MCP 工具包](toolkit.md) 的简单配置将工具连接到其首选代理。
- 使用 Docker Desktop 或 CLI 拉取和运行工具。

每个目录条目显示：

- 工具描述和元数据
- 版本历史
- MCP 服务器提供的工具列表
- 代理集成示例配置

## 从目录中使用 MCP 服务器

要从目录中使用 MCP 服务器，请参阅 [MCP 工具包](toolkit.md)。

## 向目录贡献 MCP 服务器

MCP 服务器注册表位于 https://github.com/docker/mcp-registry。要提交 MCP 服务器，请遵循[贡献指南](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)。

当您的拉取请求经过审查并批准后，您的 MCP 服务器将在 24 小时内提供在：

- Docker Desktop 的 [MCP 工具包功能](toolkit.md)
- [Docker MCP 目录](https://hub.docker.com/mcp)
- [Docker Hub](https://hub.docker.com/u/mcp) `mcp` 命名空间（适用于 Docker 构建的 MCP 服务器）