---
title: MCP
description: 了解如何通过 Gordon 使用 MCP 服务器
keywords: ai, mcp, gordon, docker desktop, docker, llm, 
grid:
- title: 内置工具
  description: 使用内置工具。
  icon: construction
  link: /ai/gordon/mcp/built-in-tools
- title: MCP 配置
  description: 按项目配置 MCP 工具。
  icon: manufacturing
  link: /ai/gordon/mcp/yaml
aliases:
 - /desktop/features/gordon/mcp/
---

## 什么是 MCP？

[模型上下文协议](https://modelcontextprotocol.io/introduction) (MCP) 是一种开放协议，它标准化了应用程序如何为大语言模型提供上下文和额外功能。MCP 作为一个客户端-服务器协议运行，其中客户端（例如 Gordon 这样的应用程序）发送请求，而服务器处理这些请求以向 AI 提供必要的上下文。这些上下文可以由 MCP 服务器通过执行某些代码来执行操作并获取操作结果、调用外部 API 等方式来收集。

Gordon 以及 Claude Desktop 或 Cursor 等其他 MCP 客户端可以与作为容器运行的 MCP 服务器进行交互。

{{< grid >}}
