---
title: R 语言专属指南
linkTitle: R
description: 使用 Docker 容器化 R 应用
keywords: Docker, getting started, R, language
summary: |
  本指南详细介绍如何使用 Docker 容器化 R 应用程序。
toc_min: 1
toc_max: 2
aliases:
  - /languages/r/
  - /guides/languages/r/
languages: [r]
params:
  time: 10 分钟
---

R 语言专属指南教您如何使用 Docker 容器化 R 应用程序。在本指南中，您将学习如何：

- 容器化并运行 R 应用程序
- 搭建本地开发环境，使用容器开发 R 应用程序
- 使用 GitHub Actions 为容器化的 R 应用程序配置 CI/CD 流水线
- 将容器化的 R 应用程序部署到本地 Kubernetes 环境，以测试和调试您的部署

首先，让我们从容器化一个现有的 R 应用程序开始。
