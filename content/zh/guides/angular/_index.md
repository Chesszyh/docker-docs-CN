---
title: Angular 特定语言指南
linkTitle: Angular
description: 使用 Docker 容器化和开发 Angular 应用程序
keywords: 入门, angular, docker, 语言, Dockerfile
summary: |
  本指南介绍了如何使用 Docker 对 Angular 应用程序进行容器化。
toc_min: 1
toc_max: 2
languages: [js]
params:
  time: 20 分钟

---

Angular 特定语言指南向你展示了如何使用 Docker 对 Angular 应用程序进行容器化，并遵循创建高效、生产就绪容器的最佳实践。

[Angular](https://angular.dev/) 是一个强大且被广泛采用的框架，用于构建动态的企业级 Web 应用程序。然而，随着应用程序的扩展，管理依赖项、环境和部署可能会变得复杂。Docker 通过为开发和生产提供一致、隔离的环境来简化这些挑战。

> 
> **致谢**
>
> Docker 衷心感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 撰写本指南。作为 Docker Captain 和经验丰富的前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使该资源成为社区必不可少��资源，帮助开发人员导航和优化其 Docker 工作流程。

---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker 容器化并运行 Angular 应用程序。
- 在容器内为 Angular 设置本地开发环境。
- 在 Docker 容器内为你的 Angular 应用程序运行测试。
- 使用 GitHub Actions 为你的容器化应用程序配置 CI/CD 管道。
- 将容器化的 Angular 应用程序部署到本地 Kubernetes 集群以进行测试和调试。

你将从容器化现有的 Angular 应用程序开始，逐步学习到生产级部署。

---

## 先决条件

在开始之前，请确保你具备以下方面的基本知识：

- 对 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 的基本了解。
- 熟悉 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 以管理依赖项和运行脚本。
- 熟悉 [Angular](https://angular.io/) 基础知识。
- 了解核心 Docker 概念，例如镜像、容器和 Dockerfile。如果你是 Docker 新手，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南开始。

完成 Angular 入门模块后，你将完全准备好使用本指南中概述的详细示例和最佳实践来容器化你自己的 Angular 应用程序。
