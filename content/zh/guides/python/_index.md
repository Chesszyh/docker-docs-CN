---
title: Python 语言专属指南
linkTitle: Python
description: 使用 Docker 容器化 Python 应用
keywords: Docker, getting started, Python, language
summary: |
  本指南介绍如何使用 Docker 容器化 Python 应用程序。
toc_min: 1
toc_max: 2
aliases:
  - /language/python/
  - /guides/language/python/
languages: [python]
params:
  time: 20 分钟
---

> **致谢**
>
> 本指南由社区贡献。Docker 在此感谢
> [Esteban Maya](https://www.linkedin.com/in/esteban-x64/) 和 [Igor Aleksandrov](https://www.linkedin.com/in/igor-aleksandrov/) 对本指南的贡献。

Python 语言专属指南教您如何使用 Docker 容器化 Python 应用程序。在本指南中，您将学习如何：

- 容器化并运行 Python 应用程序
- 搭建本地开发环境，使用容器开发 Python 应用程序
- 代码检查、格式化、类型检查和最佳实践
- 使用 GitHub Actions 为容器化的 Python 应用程序配置 CI/CD 流水线
- 将容器化的 Python 应用程序部署到本地 Kubernetes 环境，以测试和调试您的部署

首先，让我们从容器化一个现有的 Python 应用程序开始。
