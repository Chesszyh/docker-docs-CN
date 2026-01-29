---
title: Compose 中的环境变量
linkTitle: 使用环境变量
weight: 40
description: 说明如何在 Docker Compose 中设置、使用和管理环境变量。
keywords: compose, 编排, 环境, env 文件
---

Docker Compose 中的环境变量和插值（interpolation）可帮助您创建可重用的、灵活的配置。这使得容器化应用程序在不同环境中的管理和部署变得更加容易。

> [!TIP]
>
> 在使用环境变量之前，请先阅读所有相关信息，以全面了解 Docker Compose 中的环境变量。

本节涵盖以下内容：

- [如何在容器环境内设置环境变量](set-environment-variables.md)。
- [容器环境内环境变量的优先级是如何工作的](envvars-precedence.md)。
- [预定义的环境变量](envvars.md)。

本节还涵盖： 
- 如何使用 [插值](variable-interpolation.md) 在 Compose 文件中设置变量，以及它与容器环境的关系。
- 一些 [最佳实践](best-practices.md)。
