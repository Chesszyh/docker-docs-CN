---
title: C++ 语言专项指南
linkTitle: C++
description: 使用 Docker 容器化和开发 C++ 应用程序。
keywords: getting started, c++
summary: |
  本指南介绍如何使用 Docker 容器化 C++ 应用程序。
toc_min: 1
toc_max: 2
aliases:
  - /language/cpp/
  - /guides/language/cpp/
languages: [cpp]
params:
  time: 20 分钟
---

C++ 入门指南将教您如何使用 Docker 创建容器化的 C++ 应用程序。在本指南中，您将学习如何：

> **致谢**
>
> Docker 在此感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 和 [Mohammad-Ali A'râbi](https://twitter.com/MohammadAliEN) 对本指南的贡献。

- 使用多阶段 Docker 构建来容器化和运行 C++ 应用程序
- 使用 Docker Compose 构建和运行 C++ 应用程序
- 设置本地环境，使用容器开发 C++ 应用程序
- 使用 GitHub Actions 为容器化的 C++ 应用程序配置 CI/CD 流水线
- 将容器化应用程序本地部署到 Kubernetes，以测试和调试您的部署
- 使用 BuildKit 在构建过程中生成 SBOM（软件物料清单）证明

完成 C++ 入门模块后，您应该能够根据本指南提供的示例和说明来容器化您自己的 C++ 应用程序。

首先从容器化现有的 C++ 应用程序开始。
