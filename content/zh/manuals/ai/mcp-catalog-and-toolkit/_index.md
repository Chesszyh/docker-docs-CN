---
title: Docker MCP 目录和工具包
linkTitle: MCP 目录和工具包
params:
  sidebar:
    group: AI
    badge:
      color: blue
      text: Beta
weight: 30
description: 了解 Docker Hub 上的 MCP 目录
keywords: Docker, ai, mcp 服务器, ai 代理, 扩展, docker desktop, llm, docker hub
grid:
 - title: MCP 目录
   description: 了解 MCP 目录的优势、使用方法以及如何贡献
   icon: hub
   link: /ai/mcp-catalog-and-toolkit/catalog/
 - title: MCP 工具包
   description: 了解用于管理 MCP 服务器和客户端的 MCP 工具包
   icon: /icons/toolkit.svg
   link: /ai/mcp-catalog-and-toolkit/toolkit/
---

模型上下文协议 (MCP) 是一种现代标准，它将 AI 代理（Agents）从被动的响应者转变为以行动为导向的系统。通过标准化工具的描述、发现和调用方式，MCP 使代理能够安全地在各种环境中查询 API、访问数据并执行服务。

随着代理投入生产，MCP 通过在代理和工具之间提供一致、解耦且可扩展的接口，解决了互操作性、可靠性和安全性等常见的集成挑战。正如容器重新定义了软件部署一样，MCP 正在重塑 AI 系统与世界的交互方式。

> **示例**
> 
> 简单来说，MCP 服务器是 LLM 与外部系统交互的一种方式。
> 
> 例如：
> 如果您要求模型创建一个会议，它需要与您的日历应用通信才能做到这一点。
> 日历应用的 MCP 服务器提供了执行原子操作的 _工具_，例如：
> “获取会议详情”或“创建新会议”。

## 什么是 Docker MCP 目录和工具包？

Docker MCP 目录和工具包是一个全面的解决方案，用于安全地构建、共享和运行 MCP 工具。它在以下关键领域简化了开发者体验：

- 发现：一个包含经验证且具有版本的工具的中央目录
- 凭据管理：基于 OAuth，默认安全
- 执行：工具在隔离的容器化环境中运行
- 便携性：在 Claude、Cursor、VS Code 等工具中使用 MCP 工具，无需更改代码

通过 Docker Hub 和 MCP 工具包，您可以：

- 在几秒钟内启动 MCP 服务器
- 通过 CLI 或 GUI 添加工具
- 依赖 Docker 的拉取式基础设施实现可信交付

{{< grid >}}
