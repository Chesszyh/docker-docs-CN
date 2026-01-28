---
title: MCP
description: 学习如何在 Gordon 中使用 MCP 服务器
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

[模型上下文协议](https://modelcontextprotocol.io/introduction)（MCP，Model Context Protocol）是一个开放协议，它标准化了应用程序如何向大型语言模型提供上下文和额外功能。MCP 作为客户端-服务器协议运行，其中客户端（例如像 Gordon 这样的应用程序）发送请求，服务器处理这些请求以向 AI 提供必要的上下文。MCP 服务器可以通过执行某些代码来执行操作并获取操作结果、调用外部 API 等方式来收集此上下文。

Gordon 以及其他 MCP 客户端（如 Claude Desktop 或 Cursor）可以与作为容器运行的 MCP 服务器进行交互。

{{< grid >}}
