---
description: 关于在 Docker Compose 中使用多个 Compose 文件的不同方式的通用概览
keywords: compose, compose 文件, 合并, 继承, 包含, docker compose, -f 标志
linkTitle: 使用多个 Compose 文件
title: 使用多个 Compose 文件
weight: 80
aliases:
- /compose/multiple-compose-files/
---

本节包含关于如何使用多个 Compose 文件的信息。 

使用多个 Compose 文件可以让您为不同的环境或工作流自定义 Compose 应用程序。这对于可能使用数十个容器、所有权分布在多个团队的大型应用程序非常有用。例如，如果您的组织或团队使用单体仓库（monorepo），每个团队可能都有自己的“本地”Compose 文件来运行应用程序的一个子集。然后，他们需要依赖其他团队提供参考 Compose 文件，以定义运行其子集的预期方式。复杂性从代码转移到了基础设施和配置文件中。

使用多个 Compose 文件最快的方法是使用命令行中的 `-f` 标志来 [合并 (merge)](merge.md) Compose 文件，列出您所需的 Compose 文件。然而，[合并规则](merge.md#合并规则) 意味着这很快就会变得非常复杂。

Docker Compose 提供了另外两个选项来在处理多个 Compose 文件时管理这种复杂性。根据您的项目需求，您可以： 

- [扩展 (Extend) 一个 Compose 文件](extends.md)：通过引用另一个 Compose 文件并选择要在自己的应用程序中使用的部分，同时具备覆盖某些属性的能力。
- [包含 (Include) 其他 Compose 文件](include.md)：直接在您的 Compose 文件中引入。
