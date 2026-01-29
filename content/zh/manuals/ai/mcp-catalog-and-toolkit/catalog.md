---
title: Docker MCP 目录
description: 了解 MCP 目录的优势、使用方法以及如何贡献
keywords: docker hub, mcp, mcp 服务器, ai 代理, 目录, docker
---

[Docker MCP 目录](https://hub.docker.com/mcp) 是一个集中的、值得信赖的注册表，用于发现、共享和运行兼容 MCP 的工具。它与 Docker Hub 无缝集成，提供经过验证、具有版本控制且经过策划的、以 Docker 镜像形式打包的 MCP 服务器。该目录在 Docker Desktop 中也可用。

该目录解决了常见的 MCP 服务器挑战：

- 环境冲突：工具通常需要特定的运行时，这可能会与现有的设置发生冲突。
- 缺乏隔离：传统的设置存在暴露宿主系统的风险。
- 设置复杂：手动安装和配置导致采用速度慢。
- 跨平台不一致：工具在不同操作系统上的行为可能难以预测。

通过 Docker，每个 MCP 服务器都作为一个独立的容器运行，因此它是便携的、隔离的且一致的。您可以使用 Docker CLI 或 Docker Desktop 立即启动工具，而无需担心依赖项或兼容性。

## 主要功能

- 在一处提供超过 100 个经验证的 MCP 服务器
- 发布者验证和版本化发布
- 使用 Docker 的基础设施进行基于拉取的分发
- 由 New Relic、Stripe、Grafana 等合作伙伴提供的工具

## 工作原理

MCP 目录中的每个工具都以带有元数据的 Docker 镜像形式打包：

- 通过 Docker Hub 在 `mcp/` 命名空间下发现工具。
- 通过 [MCP 工具包](toolkit.md) 的简单配置，将工具连接到其偏好的代理。
- 使用 Docker Desktop 或 CLI 拉取并运行工具。

每个目录条目显示：

- 工具描述和元数据
- 版本历史
- MCP 服务器提供的工具列表
- 代理集成的示例配置

## 使用目录中的 MCP 服务器

要使用目录中的 MCP 服务器，请参阅 [MCP 工具包](toolkit.md)。

## 向目录贡献 MCP 服务器

MCP 服务器注册表位于 https://github.com/docker/mcp-registry。要提交 MCP 服务器，请遵循 [贡献指南](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)。

当您的拉取请求经过审查并获得批准后，您的 MCP 服务器将在 24 小时内出现在以下位置：

- Docker Desktop 的 [MCP 工具包功能](toolkit.md)
- [Docker MCP 目录](https://hub.docker.com/mcp)
- [Docker Hub](https://hub.docker.com/u/mcp) 的 `mcp` 命名空间（针对由 Docker 构建的 MCP 服务器）
