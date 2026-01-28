---
description: 使用 Docker 容器化和开发 Bun 应用程序。
keywords: getting started, bun
title: Bun 语言特定指南
summary: |
  了解如何使用 Bun 运行时容器化 JavaScript 应用程序。
linkTitle: Bun
languages: [js]
params:
  time: 10 minutes
---

Bun 入门指南教你如何使用 Docker 创建容器化的 Bun 应用程序。在本指南中，你将学习如何：

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 你将学到什么？

* 使用 Docker 容器化并运行 Bun 应用程序
* 设置本地环境以使用容器开发 Bun 应用程序
* 使用 GitHub Actions 为容器化 Bun 应用程序配置 CI/CD 管道
* 将容器化应用程序本地部署到 Kubernetes 以测试和调试部署

## 先决条件

- 假设你对 JavaScript 有基本的了解。
- 你必须熟悉 Docker 概念，如容器、镜像和 Dockerfile。如果你是 Docker 新手，可以从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Bun 入门模块后，你应该能够根据本指南中提供的示例和说明容器化你自己的 Bun 应用程序。

首先容器化一个现有的 Bun 应用程序。
