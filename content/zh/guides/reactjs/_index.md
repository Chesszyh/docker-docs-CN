---
title: React.js 语言特定指南
linkTitle: React.js
description: 使用 Docker 容器化和开发 React.js 应用程序
keywords: getting started, React.js, react.js, docker, language, Dockerfile
summary: |
  本指南解释了如何使用 Docker 容器化 React.js 应用程序。
toc_min: 1
toc_max: 2
languages: [js]
params:
  time: 20 minutes

---

React.js 语言特定指南展示了如何使用 Docker 容器化 React.js 应用程序，遵循创建高效、生产就绪容器的最佳实践。

[React.js](https://react.dev/) 是一个广泛用于构建交互式用户界面的库。然而，有效地管理依赖项、环境和部署可能会很复杂。Docker 通过提供一致和容器化的环境简化了这一过程。

>
> **致谢**
>
> Docker 衷心感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 编写本指南。作为一名 Docker Captain 和经验丰富的前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识对社区来说是无价的，帮助开发人员驾驭和优化他们的 Docker 工作流程。

---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker 容器化并运行 React.js 应用程序。
- 在容器内设置 React.js 的本地开发环境。
- 在 Docker 容器内运行 React.js 应用程序的测试。
- 为你的容器化应用程序配置使用 GitHub Actions 的 CI/CD 管道。
- 将容器化的 React.js 应用程序部署到本地 Kubernetes 集群进行测试和调试。

首先，你将从容器化现有的 React.js 应用程序开始。

---

## 先决条件

在开始之前，请确保你熟悉以下内容：

- 对 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 或 [TypeScript](https://www.typescriptlang.org/) 有基本的了解。
- 具有 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 的基础知识，用于管理依赖项和运行脚本。
- 熟悉 [React.js](https://react.dev/) 基础知识。
- 理解 Docker 概念，如镜像、容器和 Dockerfile。如果你是 Docker 新手，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

一旦你完成了 React.js 入门模块，你就可以根据本指南中提供的示例和说明容器化你自己的 React.js 应用程序。
