---
title: Angular 语言专项指南
linkTitle: Angular
description: 使用 Docker 容器化和开发 Angular 应用程序
keywords: getting started, angular, docker, language, Dockerfile
summary: |
  本指南介绍如何使用 Docker 容器化 Angular 应用程序。
toc_min: 1
toc_max: 2
languages: [js]
params:
  time: 20 分钟

---

Angular 语言专项指南将向您展示如何使用 Docker 容器化 Angular 应用程序，并遵循创建高效、生产就绪容器的最佳实践。

[Angular](https://angular.dev/) 是一个强大且被广泛采用的框架，用于构建动态的企业级 Web 应用程序。然而，随着应用程序规模的扩大，管理依赖项、环境和部署可能变得复杂。Docker 通过提供一致、隔离的开发和生产环境来简化这些挑战。

>
> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 表示诚挚的感谢，感谢他编写了本指南。作为 Docker Captain 和经验丰富的前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使本资源成为社区的必备资源，帮助开发人员导航和优化他们的 Docker 工作流程。

---

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化和运行 Angular 应用程序。
- 在容器内为 Angular 设置本地开发环境。
- 在 Docker 容器内运行 Angular 应用程序的测试。
- 使用 GitHub Actions 为容器化应用程序配置 CI/CD 流水线。
- 将容器化的 Angular 应用程序部署到本地 Kubernetes 集群以进行测试和调试。

您将从容器化现有的 Angular 应用程序开始，逐步进阶到生产级别的部署。

---

## 前提条件

在开始之前，请确保您具备以下工作知识：

- 对 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 的基本理解。
- 熟悉 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 来管理依赖项和运行脚本。
- 熟悉 [Angular](https://angular.io/) 基础知识。
- 理解 Docker 的核心概念，如镜像（image）、容器（container）和 Dockerfile。如果您是 Docker 新手，请从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Angular 入门模块后，您将完全准备好使用本指南中提供的详细示例和最佳实践来容器化您自己的 Angular 应用程序。
