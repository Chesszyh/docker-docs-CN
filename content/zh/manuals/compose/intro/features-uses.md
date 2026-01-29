---
description: 了解 Docker Compose 在容器化应用程序开发和部署中的优势及典型用例
keywords: docker compose, compose 用例, compose 优势, 容器编排, 开发环境, 测试容器, yaml 文件
title: 为什么使用 Compose？
weight: 20
aliases: 
- /compose/features-uses/
---

## Docker Compose 的主要优势

使用 Docker Compose 具有多项优势，可以简化容器化应用程序的开发、部署和管理：

- 简化控制：在单个 YAML 文件中定义并管理多容器应用程序，从而简化了编排和复制过程。

- 高效协作：可共享的 YAML 文件支持开发人员和运维人员之间的顺畅协作，改进了工作流程和问题解决方式，从而提高了整体效率。

- 快速应用开发：Compose 会缓存用于创建容器的配置。当您重启未发生更改的服务时，Compose 会重用现有容器。重用容器意味着您可以非常迅速地对环境进行更改。

- 跨环境的可移植性：Compose 支持在 Compose 文件中使用变量。您可以使用这些变量为不同的环境或不同的用户自定义您的组合。

## Docker Compose 的常见用例

Compose 可以以多种不同的方式使用。下面概述了一些常见的用例。

### 开发环境

在开发软件时，能够在一个隔离的环境中运行应用程序并与其交互是至关重要的。Compose 命令行工具可用于创建此类环境并与之交互。

[Compose 文件](/reference/compose-file/_index.md) 提供了一种记录和配置应用程序所有服务依赖项（数据库、队列、缓存、Web 服务 API 等）的方法。使用 Compose 命令行工具，您只需一条命令 (`docker compose up`) 即可为每个依赖项创建并启动一个或多个容器。

这些功能共同为您开始一个项目提供了一种便捷的方式。Compose 可以将长达数页的“开发者入门指南”简化为一个机器可读的 Compose 文件和几条命令。

### 自动化测试环境

自动化测试套件是任何持续部署或持续集成流程的重要组成部分。自动化端到端测试需要一个运行测试的环境。Compose 提供了一种便捷的方法，可以为您测试套件创建和销毁隔离的测试环境。通过在 [Compose 文件](/reference/compose-file/_index.md)中定义完整环境，您只需几条命令即可创建和销毁这些环境：

```console
$ docker compose up -d
$ ./run_tests
$ docker compose down
```

### 单机部署

Compose 传统上一直专注于开发和测试工作流，但随着每个版本的发布，我们在面向生产环境的功能方面不断取得进展。

有关使用面向生产环境功能的详细信息，请参阅 [在生产环境中使用 Compose](/manuals/compose/how-tos/production.md)。

## 下一步

- [了解 Compose 的历史](history.md)
- [了解 Compose 的工作原理](compose-application-model.md)
- [尝试快速入门指南](../gettingstarted.md)
