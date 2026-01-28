---
title: Docker Compose 的历史与发展
linkTitle: 历史与发展
description: 探索 Docker Compose 从 v1 到 v2 的演变，包括 CLI 变化、YAML 版本控制和 Compose Specification。
keywords: compose, compose yaml, swarm, migration, compatibility, docker compose vs docker-compose
weight: 30
aliases:
- /compose/history/
---

本页面提供：
 - Docker Compose CLI 开发的简要历史
 - 对组成 Compose v1 和 Compose v2 的主要版本和文件格式的清晰解释
 - Compose v1 和 Compose v2 之间的主要区别

## 介绍

![显示 Compose v1 和 Compose v2 之间主要区别的图片](../images/v1-versus-v2.png)

上图显示当前支持的 Docker Compose CLI 版本是 Compose v2，它由 [Compose Specification（Compose 规范）](/reference/compose-file/_index.md)定义。

它还提供了文件格式、命令行语法和顶级元素差异的快速概览。以下各节将更详细地介绍这些内容。

### Docker Compose CLI 版本控制

Docker Compose 命令行二进制文件的第一版于 2014 年首次发布。它是用 Python 编写的，通过 `docker-compose` 调用。通常，Compose v1 项目在 `compose.yaml` 文件中包含顶级 `version` 元素，其值范围从 `2.0` 到 `3.8`，这些值指的是特定的[文件格式](#compose-文件格式版本控制)。

Docker Compose 命令行二进制文件的第二版于 2020 年宣布，用 Go 编写，通过 `docker compose` 调用。Compose v2 忽略 `compose.yaml` 文件中的 `version` 顶级元素。

### Compose 文件格式版本控制

Docker Compose CLI 由特定的文件格式定义。

Compose v1 发布了三个主要版本的 Compose 文件格式：
- 2014 年 Compose 1.0.0 的 Compose 文件格式 1
- 2016 年 Compose 1.6.0 的 Compose 文件格式 2.x
- 2017 年 Compose 1.10.0 的 Compose 文件格式 3.x

Compose 文件格式 1 与所有后续格式有很大不同，因为它缺少顶级 `services` 键。它的使用是历史性的，以这种格式编写的文件无法在 Compose v2 中运行。

Compose 文件格式 2.x 和 3.x 彼此非常相似，但后者引入了许多针对 Swarm 部署的新选项。

为了解决 Compose CLI 版本控制、Compose 文件格式版本控制以及根据是否使用 Swarm 模式而产生的功能对等性方面的困惑，文件格式 2.x 和 3.x 被合并到 [Compose Specification（Compose 规范）](/reference/compose-file/_index.md)中。

Compose v2 使用 Compose Specification 进行项目定义。与之前的文件格式不同，Compose Specification 是滚动更新的，并使 `version` 顶级元素成为可选的。Compose v2 还使用可选规范——[Deploy](/reference/compose-file/deploy.md)、[Develop](/reference/compose-file/develop.md) 和 [Build](/reference/compose-file/build.md)。

为了使[迁移](/manuals/compose/releases/migrate.md)更容易，Compose v2 对 Compose 文件格式 2.x/3.x 和 Compose Specification 之间已弃用或更改的某些元素具有向后兼容性。

## 下一步是什么？

- [Compose 如何工作](compose-application-model.md)
- [Compose Specification 参考](/reference/compose-file/_index.md)
- [从 Compose v1 迁移到 v2](/manuals/compose/releases/migrate.md)
