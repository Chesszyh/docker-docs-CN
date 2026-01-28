---
title: Docker MCP Catalog
description: 了解 MCP Catalog 的优势、如何使用以及如何贡献
keywords: docker hub, mcp, mcp servers, ai agents, catalog, docker
---

[Docker MCP Catalog](https://hub.docker.com/mcp) 是一个集中式、可信的注册表，用于发现、共享和运行与 MCP 兼容的工具。它无缝集成到 Docker Hub 中，提供经过验证、版本化和精选的 MCP 服务器，打包为 Docker 镜像。该目录也可在 Docker Desktop 中使用。

该目录解决了常见的 MCP 服务器挑战：

- 环境冲突：工具通常需要特定的运行时，可能与现有设置发生冲突。
- 缺乏隔离：传统设置存在暴露主机系统的风险。
- 设置复杂性：手动安装和配置导致采用缓慢。
- 跨平台不一致：工具在不同操作系统上可能表现不可预测。

使用 Docker，每个 MCP 服务器都作为自包含容器运行，因此它是可移植的、隔离的和一致的。你可以使用 Docker CLI 或 Docker Desktop 即时启动工具，无需担心依赖项或兼容性。

## 主要功能

- 超过 100 个经过验证的 MCP 服务器集中在一处
- 发布者验证和版本化发布
- 使用 Docker 基础设施的基于拉取的分发
- 由 New Relic、Stripe、Grafana 等合作伙伴提供的工具

## 工作原理

MCP Catalog 中的每个工具都打包为带有元数据的 Docker 镜像：

- 通过 `mcp/` 命名空间在 Docker Hub 上发现工具。
- 通过 [MCP Toolkit](toolkit.md) 的简单配置将工具连接到首选代理。
- 使用 Docker Desktop 或 CLI 拉取和运行工具。

每个目录条目显示：

- 工具描述和元数据
- 版本历史
- MCP 服务器提供的工具列表
- 代理集成的示例配置

## 使用目录中的 MCP 服务器

要使用目录中的 MCP 服务器，请参阅 [MCP toolkit](toolkit.md)。

## 向目录贡献 MCP 服务器

MCP 服务器注册表位于 https://github.com/docker/mcp-registry。要提交 MCP 服务器，请遵循[贡献指南](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)。

当你的拉取请求被审核并批准后，你的 MCP 服务器将在 24 小时内在以下位置可用：

- Docker Desktop 的 [MCP Toolkit 功能](toolkit.md)
- [Docker MCP catalog](https://hub.docker.com/mcp)
- [Docker Hub](https://hub.docker.com/u/mcp) 的 `mcp` 命名空间（用于 Docker 构建的 MCP 服务器）
