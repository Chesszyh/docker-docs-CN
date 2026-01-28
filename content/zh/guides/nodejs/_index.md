---
title: Node.js 语言特定指南
linkTitle: Node.js
description: 使用 Docker 容器化和开发 Node.js 应用
keywords: getting started, node, node.js
summary: |
  本指南介绍如何使用 Docker 容器化 Node.js 应用程序。
toc_min: 1
toc_max: 2
aliases:
  - /language/nodejs/
  - /guides/language/nodejs/
languages: [js]
params:
  time: 20 分钟
---

Node.js 语言特定指南将教你如何使用 Docker 容器化 Node.js 应用程序。在本指南中，你将学习如何：

- 容器化并运行 Node.js 应用程序
- 设置本地环境，使用容器开发 Node.js 应用程序
- 使用容器为 Node.js 应用程序运行测试
- 使用 GitHub Actions 为容器化的 Node.js 应用程序配置 CI/CD 流水线
- 将容器化的 Node.js 应用程序本地部署到 Kubernetes，以测试和调试你的部署

首先让我们容器化一个现有的 Node.js 应用程序。
