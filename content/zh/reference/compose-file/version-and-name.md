---
title: 版本和名称顶级元素
description: 了解何时以及是否设置版本和名称顶级元素
keywords: compose, compose specification, services, compose file reference, compose 规范, 服务, compose 文件参考
aliases:
 - /compose/compose-file/04-version-and-name/
weight: 10
---

## Version 顶级元素（已过时）

顶级 `version` 属性由 Compose 规范定义，旨在用于向后兼容。它仅供参考，如果使用该属性，你将收到一条警告消息，提示它已过时。

Compose 不使用 `version` 来选择确切的模式以验证 Compose 文件，而是优先使用已实现的最新模式。

Compose 会验证其是否能完整解析 Compose 文件。如果存在未知字段（通常是因为 Compose 文件使用了较新版本规范中定义的字段编写），你将收到一条警告消息。

## Name 顶级元素

顶级 `name` 属性由 Compose 规范定义，用于在你未显式设置项目名称时作为项目名称使用。
Compose 提供了一种覆盖此名称的方法，并且在未设置顶级 `name` 元素时，会设置一个默认的项目名称。

无论项目名称是通过顶级 `name` 定义的，还是通过其他自定义机制定义的，它都会作为 `COMPOSE_PROJECT_NAME` 暴露出来，以供 [插值](interpolation.md) 和环境变量解析使用。

```yml
name: myapp

services:
  foo:
    image: busybox
    command: echo "I'm running ${COMPOSE_PROJECT_NAME}"
```

有关命名 Compose 项目的其他方法的更多信息，请参阅 [指定项目名称](/manuals/compose/how-tos/project-name.md)。