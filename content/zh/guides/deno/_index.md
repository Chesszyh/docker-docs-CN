---
description: 使用 Docker 容器化和开发 Deno 应用程序。
keywords: getting started, deno
title: Deno 语言专项指南
summary: |
  学习如何使用 Docker 容器化基于 Deno 运行时的 JavaScript 应用程序。
linkTitle: Deno
languages: [js]
params:
  time: 10 分钟
---

Deno 入门指南将教您如何使用 Docker 创建容器化的 Deno 应用程序。在本指南中，您将学习如何：

> **致谢**
>
> Docker 在此感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 您将学到什么？

* 使用 Docker 容器化和运行 Deno 应用程序
* 设置本地环境，使用容器开发 Deno 应用程序
* 使用 Docker Compose 运行应用程序
* 使用 GitHub Actions 为容器化的 Deno 应用程序配置 CI/CD 流水线
* 将容器化应用程序本地部署到 Kubernetes，以测试和调试您的部署

## 前提条件

- 假设您具备 JavaScript 的基本知识。
- 您必须熟悉 Docker 概念，如容器、镜像和 Dockerfile。如果您是 Docker 新手，可以从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南开始。

完成 Deno 入门模块后，您应该能够根据本指南提供的示例和说明来容器化您自己的 Deno 应用程序。

首先从容器化现有的 Deno 应用程序开始。
