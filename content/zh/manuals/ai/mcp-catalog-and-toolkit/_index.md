---
title: Docker MCP Catalog 与 Toolkit
linkTitle: MCP Catalog 与 Toolkit
params:
  sidebar:
    group: AI
    badge:
      color: blue
      text: Beta
weight: 30
description: 了解 Docker Hub 上的 Docker MCP catalog
keywords: Docker, ai, mcp servers, ai agents, extension, docker desktop, llm, docker hub
grid:
 - title: MCP Catalog
   description: 了解 MCP Catalog 的优势、如何使用以及如何贡献
   icon: hub
   link: /ai/mcp-catalog-and-toolkit/catalog/
 - title: MCP Toolkit
   description: 了解用于管理 MCP 服务器和客户端的 MCP toolkit
   icon: /icons/toolkit.svg
   link: /ai/mcp-catalog-and-toolkit/toolkit/
---

模型上下文协议（MCP，Model Context Protocol）是一种现代标准，它将 AI 代理从被动响应者转变为以行动为导向的系统。通过标准化工具的描述、发现和调用方式，MCP 使代理能够安全地查询 API、访问数据，并在不同环境中执行服务。

随着代理进入生产环境，MCP 通过在代理和工具之间提供一致、解耦且可扩展的接口，解决了常见的集成挑战——互操作性、可靠性和安全性。正如容器重新定义了软件部署，MCP 正在重塑 AI 系统与世界的交互方式。

> **示例**
>
> 简单来说，MCP 服务器是 LLM 与外部系统交互的一种方式。
>
> 例如：
> 如果你让模型创建一个会议，它需要与你的日历应用程序通信才能完成。
> 日历应用程序的 MCP 服务器提供执行原子操作的_工具_，例如：
> "获取会议详情"或"创建新会议"。

## 什么是 Docker MCP Catalog 与 Toolkit？

Docker MCP Catalog 与 Toolkit 是一个用于安全构建、共享和运行 MCP 工具的综合解决方案。它在以下关键领域简化了开发者体验：

- 发现：具有经过验证、版本化工具的中央目录
- 凭证管理：基于 OAuth，默认安全
- 执行：工具在隔离的容器化环境中运行
- 可移植性：跨 Claude、Cursor、VS Code 等使用 MCP 工具——无需代码更改

通过 Docker Hub 和 MCP Toolkit，你可以：

- 在几秒钟内启动 MCP 服务器
- 通过 CLI 或 GUI 添加工具
- 依赖 Docker 的基于拉取的基础设施进行可信交付

{{< grid >}}
