---
description: 了解 Docker Compose 用于容器化应用程序开发和部署的优势和典型用例
keywords: docker compose, compose use cases, compose benefits, container orchestration, development environments, testing containers, yaml file
title: 为什么使用 Compose？
weight: 20
aliases:
- /compose/features-uses/
---

## Docker Compose 的主要优势

使用 Docker Compose 提供了多项优势，简化了容器化应用程序的开发、部署和管理：

- 简化控制：在单个 YAML 文件中定义和管理多容器应用程序，简化编排和复制。

- 高效协作：可共享的 YAML 文件支持开发人员和运维人员之间的顺畅协作，改善工作流程和问题解决，从而提高整体效率。

- 快速应用程序开发：Compose 缓存用于创建容器的配置。当您重启未更改的服务时，Compose 会重用现有容器。重用容器意味着您可以非常快速地对环境进行更改。

- 跨环境可移植性：Compose 支持 Compose 文件中的变量。您可以使用这些变量为不同的环境或不同的用户自定义您的组合。

## Docker Compose 的常见用例

Compose 可以以多种不同的方式使用。下面概述了一些常见用例。

### 开发环境

在开发软件时，能够在隔离环境中运行应用程序并与之交互至关重要。Compose 命令行工具可用于创建环境并与之交互。

[Compose 文件](/reference/compose-file/_index.md)提供了一种方式来记录和配置应用程序的所有服务依赖项（数据库、队列、缓存、Web 服务 API 等）。使用 Compose 命令行工具，您可以通过单个命令（`docker compose up`）为每个依赖项创建并启动一个或多个容器。

总之，这些功能为您提供了一种便捷的方式来开始项目。Compose 可以将多页的"开发人员入门指南"简化为一个机器可读的 Compose 文件和几个命令。

### 自动化测试环境

任何持续部署或持续集成过程的重要组成部分是自动化测试套件。自动化端到端测试需要一个运行测试的环境。Compose 提供了一种便捷的方式来为您的测试套件创建和销毁隔离的测试环境。通过在 [Compose 文件](/reference/compose-file/_index.md)中定义完整环境，您只需几个命令即可创建和销毁这些环境：

```console
$ docker compose up -d
$ ./run_tests
$ docker compose down
```

### 单主机部署

Compose 传统上专注于开发和测试工作流程，但随着每个版本的发布，我们在更多面向生产的功能方面取得进展。

有关使用面向生产功能的详细信息，请参阅[在生产环境中使用 Compose](/manuals/compose/how-tos/production.md)。

## 下一步是什么？

- [了解 Compose 的历史](history.md)
- [了解 Compose 如何工作](compose-application-model.md)
- [尝试快速入门指南](../gettingstarted.md)
