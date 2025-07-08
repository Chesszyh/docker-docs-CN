---
title: Compose 中的环境变量
linkTitle: 使用环境变量
weight: 40
description: 介绍如何在 Docker Compose 中设置、使用和管理环境变量。
keywords: compose, orchestration, environment, env file, 编排, 环境, 环境变量文件
aliases:
- /compose/environment-variables/
---

Docker Compose 中的环境变量和插值可帮助您创建可重用、灵活的配置。这使得 Docker 化应用程序更易于在不同环境中管理和部署。

> [!TIP]
>
> 在使用环境变量之前，请先通读所有信息，以全面了解 Docker Compose 中的环境变量。

本节内容包括：

- [如何在容器环境中设置环境变量](set-environment-variables.md)。
- [环境变量在容器环境中的优先级如何工作](envvars-precedence.md)。
- [预定义的环境变量](envvars.md)。

它还包括：
- 如何使用[插值](variable-interpolation.md)在您的 Compose 文件中设置变量，以及它与容器环境的关系。
- 一些[最佳实践](best-practices.md)。
