---
title: version 和 name 顶级元素
description: 了解何时以及是否需要设置 version 和 name 顶级元素
keywords: compose, compose specification, services, compose file reference
aliases:
 - /compose/compose-file/04-version-and-name/
weight: 10
---

## version 顶级元素（已废弃）

顶级 `version` 属性由 Compose 规范定义，用于向后兼容。它仅供参考，如果使用它，你将收到一条警告消息，表明它已废弃。

Compose 不使用 `version` 来选择精确的模式来验证 Compose 文件，而是在实现时优先使用最新的模式。

Compose 会验证是否能完全解析 Compose 文件。如果某些字段未知，通常是因为 Compose 文件是使用规范较新版本定义的字段编写的，你将收到一条警告消息。

## name 顶级元素

顶级 `name` 属性由 Compose 规范定义，作为在你未显式设置时使用的项目名称。
Compose 提供了一种覆盖此名称的方式，并在未设置顶级 `name` 元素时设置默认项目名称。

当项目名称由顶级 `name` 或某些自定义机制定义时，它会作为 `COMPOSE_PROJECT_NAME` 暴露给[变量插值](interpolation.md)和环境变量解析。

```yml
name: myapp

services:
  foo:
    image: busybox
    command: echo "I'm running ${COMPOSE_PROJECT_NAME}"
```

有关命名 Compose 项目的其他方式的更多信息，请参阅[指定项目名称](/manuals/compose/how-tos/project-name.md)。
