---
title: Docker Compose 的历史与发展
linkTitle: 历史与发展
description: 探索 Docker Compose 从 v1 到 v2 的演进，包括 CLI 的变化、YAML 版本控制以及 Compose 规范。
keywords: compose, compose yaml, swarm, 迁移, 兼容性, docker compose 与 docker-compose 的区别
weight: 30
---

本页提供：
 - Docker Compose CLI 发展的简史
 - 对构成 Compose v1 和 Compose v2 的主要版本及文件格式的清晰解释
 - Compose v1 和 Compose v2 之间的主要区别 

## 简介

![展示 Compose v1 和 Compose v2 主要区别的图表](../images/v1-versus-v2.png)

上图显示，目前受支持的 Docker Compose CLI 版本是基于 [Compose 规范](/reference/compose-file/_index.md) 定义的 Compose v2。

它还简要展示了文件格式、命令行语法和顶级元素方面的差异。这些内容将在随后的章节中进行更详细的介绍。

### Docker Compose CLI 版本控制

Docker Compose 命令行二进制文件的第一个版本发布于 2014 年。它是用 Python 编写的，通过 `docker-compose` 调用。通常，Compose v1 项目在 `compose.yaml` 文件中包含一个顶级的 `version` 元素，其值在 `2.0` 到 `3.8` 之间，代表特定的 [文件格式](#Compose-文件格式版本控制)。

Docker Compose 命令行二进制文件的第二个版本于 2020 年发布，它是用 Go 语言编写的，通过 `docker compose` 调用。Compose v2 会忽略 `compose.yaml` 文件中的 `version` 顶级元素。

### Compose 文件格式版本控制

Docker Compose CLI 是由特定的文件格式定义的。 

为 Compose v1 发布了三个主要版本的 Compose 文件格式：
- Compose 文件格式 1，随 2014 年的 Compose 1.0.0 发布
- Compose 文件格式 2.x，随 2016 年的 Compose 1.6.0 发布
- Compose 文件格式 3.x，随 2017 年的 Compose 1.10.0 发布

Compose 文件格式 1 与后续所有格式都有很大不同，因为它缺少顶级的 `services` 键。它的使用已成为历史，用该格式编写的文件无法在 Compose v2 中运行。

Compose 文件格式 2.x 和 3.x 彼此非常相似，但后者引入了许多针对 Swarm 部署的新选项。

为了解决围绕 Compose CLI 版本、Compose 文件格式版本以及根据是否使用 Swarm 模式而产生的功能差异所带来的困扰，文件格式 2.x 和 3.x 已合并为 [Compose 规范](/reference/compose-file/_index.md)。 

Compose v2 使用 Compose 规范进行项目定义。与之前的文件格式不同，Compose 规范是滚动更新的，且将 `version` 顶级元素设为可选。Compose v2 还利用了一些可选规范——[部署 (Deploy)](/reference/compose-file/deploy.md)、[开发 (Develop)](/reference/compose-file/develop.md) 和 [构建 (Build)](/reference/compose-file/build.md)。

为了简化 [迁移](/manuals/compose/releases/migrate.md) 过程， Compose v2 对在 Compose 文件格式 2.x/3.x 与 Compose 规范之间已弃用或更改的某些元素提供了向后兼容性。

## 下一步

- [Compose 工作原理](compose-application-model.md)
- [Compose 规范参考](/reference/compose-file/_index.md)
- [从 Compose v1 迁移到 v2](/manuals/compose/releases/migrate.md)
