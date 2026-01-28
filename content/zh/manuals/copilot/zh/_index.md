---
title: Docker for GitHub Copilot
params:
  sidebar:
    group: Products
    badge:
      color: violet
      text: EA
weight: 50
description: |
  了解如何使用 Docker for GitHub Copilot 扩展简化 Docker 相关任务。此集成帮助您生成 Docker 资产、分析漏洞，并通过各种开发环境中的 GitHub Copilot Chat 实现容器化自动化。
keywords: Docker, GitHub Copilot, extension, Visual Studio Code, chat, ai, containerization
---

{{< summary-bar feature_name="Docker GitHub Copilot" >}}

[Docker for GitHub Copilot](https://github.com/marketplace/docker-for-github-copilot)
扩展将 Docker 的功能与 GitHub Copilot 集成，为应用程序容器化、生成 Docker 资产以及分析项目漏洞提供帮助。此扩展帮助您在任何可以使用 GitHub Copilot Chat 的地方简化 Docker 相关任务。

## 主要功能

Docker for GitHub Copilot 扩展的主要功能包括：

- 在任何可以使用 GitHub Copilot Chat 的场景中（例如在 GitHub.com 和 Visual Studio Code 中）提问并获得关于容器化的回答。
- 自动为项目生成 Dockerfile、Docker Compose 文件和 `.dockerignore` 文件。
- 直接从聊天界面使用生成的 Docker 资产创建拉取请求（Pull Request）。
- 从 [Docker Scout](/manuals/scout/_index.md) 获取项目漏洞摘要，并通过 CLI 获取后续步骤。

## 数据隐私

Docker 代理（agent）仅基于 Docker 的文档和工具进行训练，以协助完成容器化及相关任务。除了您所提问的上下文之外，它无法访问您项目的数据。

当使用 Docker Extension for GitHub Copilot 时，如果用户授权，GitHub Copilot 可能会在其请求中包含对当前打开文件的引用。Docker 代理可以读取该文件以提供上下文感知的回答。

如果代理被要求检查漏洞或生成 Docker 相关资产，它将把引用的仓库克隆到内存存储中以执行必要的操作。

源代码或项目元数据永远不会被持久存储。问题和答案会保留用于分析和故障排除。Docker 代理处理的数据永远不会与第三方共享。

## 支持的语言

Docker Extension for GitHub Copilot 支持以下编程语言，用于从头开始容器化项目的任务：

- Go
- Java
- JavaScript
- Python
- Rust
- TypeScript
