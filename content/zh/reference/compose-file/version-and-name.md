---
title: 版本和名称顶级元素
description: 了解何时以及是否设置版本和名称顶级元素
keywords: compose, compose 规范, 服务, compose 文件参考
aliases:
 - /compose/compose-file/04-version-and-name/
weight: 10
---

## 版本顶级元素（已过时）

顶级 `version` 属性由 Compose 规范定义，用于向后兼容。它仅供参考，如果使用，您将收到一条警告消息，指出它已过时。

Compose 不使用 `version` 来选择精确的模式来验证 Compose 文件，而是
在实现时优先使用最新模式。

Compose 会验证它是否可以完全解析 Compose 文件。如果某些字段未知，通常
是因为 Compose 文件是使用较新版本的规范定义的字段编写的，您将收到一条警告消息。

## 名称顶级元素

顶级 `name` 属性由 Compose 规范定义为如果您未明确设置，则使用的项目名称。
Compose 提供了一种覆盖此名称的方法，并设置一个
默认项目名称，如果未设置顶级 `name` 元素，则使用该名称。

无论项目名称是通过顶级 `name` 还是通过某些自定义机制定义的，它都将作为 `COMPOSE_PROJECT_NAME` 公开用于
[插值](interpolation.md) 和环境变量解析

```yml
name: myapp

services:
  foo:
    image: busybox
    command: echo "I'm running ${COMPOSE_PROJECT_NAME}"
```

有关命名 Compose 项目的其他方式的更多信息，请参阅 [指定项目名称](/manuals/compose/how-tos/project-name.md)。
