---
description: 关于在 Docker Compose 中使用多个 compose 文件的不同方式的概述
keywords: compose, compose file, merge, extends, include, docker compose, -f flag
linkTitle: 使用多个 Compose 文件
title: 使用多个 Compose 文件
weight: 80
aliases:
- /compose/multiple-compose-files/
---

本节包含关于使用多个 Compose 文件的不同方式的信息。

使用多个 Compose 文件可以让你为不同的环境或工作流自定义 Compose 应用程序。这对于可能使用数十个容器的大型应用程序非常有用，其所有权分布在多个团队之间。例如，如果你的组织或团队使用单体仓库（monorepo），每个团队可能有自己的"本地"Compose 文件来运行应用程序的一个子集。然后他们需要依赖其他团队提供的参考 Compose 文件，该文件定义了运行他们自己子集的预期方式。复杂性从代码转移到了基础设施和配置文件中。

使用多个 Compose 文件最快的方法是在命令行中使用 `-f` 标志[合并](merge.md) Compose 文件，列出你想要的 Compose 文件。但是，[合并规则](merge.md#merging-rules)意味着这很快就会变得相当复杂。

Docker Compose 提供了另外两个选项来管理使用多个 Compose 文件时的这种复杂性。根据你项目的需要，你可以：

- [扩展 Compose 文件](extends.md)，通过引用另一个 Compose 文件并选择你想在自己的应用程序中使用的部分，并能够覆盖某些属性。
- 在你的 Compose 文件中直接[包含其他 Compose 文件](include.md)。

