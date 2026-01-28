---
description: 了解标签，一种管理 Docker 对象元数据的工具。
keywords: labels, metadata, docker, annotations
title: Docker 对象标签
aliases:
  - /engine/userguide/labels-custom-metadata/
  - /config/labels-custom-metadata/
---

标签（Label）是一种将元数据应用到 Docker 对象的机制，包括：

- 镜像
- 容器
- 本地守护进程
- 卷
- 网络
- Swarm 节点
- Swarm 服务

你可以使用标签来组织你的镜像、记录许可信息、注释
容器、卷和网络之间的关系，或以任何对你的
业务或应用有意义的方式使用。

## 标签键和值

标签是一个键值对，以字符串形式存储。你可以为
一个对象指定多个标签，但每个键在一个对象内必须是唯一的。如果
同一个键被赋予多个值，最近写入的值会覆盖
所有之前的值。

### 键格式建议

标签键是键值对的左侧部分。键是字母数字
字符串，可以包含句点（`.`）、下划线（`_`）、斜杠（`/`）和连字符（`-`）。大多数 Docker 用户使用
由其他组织创建的镜像，以下指南有助于
防止对象之间标签的无意重复，特别是如果你计划
使用标签作为自动化机制的话。

- 第三方工具的作者应该在每个标签键前加上
  他们拥有的域名的反向 DNS 表示法，例如 `com.example.some-label`。

- 未经域名所有者许可，不要在标签键中使用该域名。

- `com.docker.*`、`io.docker.*` 和 `org.dockerproject.*` 命名空间
  由 Docker 保留供内部使用。

- 标签键应以小写字母开头和结尾，并且只应
  包含小写字母数字字符、句点字符（`.`）和
  连字符字符（`-`）。不允许连续的句点或连字符。

- 句点字符（`.`）分隔命名空间"字段"。没有
  命名空间的标签键保留给 CLI 使用，允许 CLI 用户使用更短的便于输入的字符串来交互式
  标记 Docker 对象。

这些指南目前没有强制执行，额外的指南可能适用于
特定的使用场景。

### 值指南

标签值可以包含任何可以表示为字符串的数据类型，
包括（但不限于）JSON、XML、CSV 或 YAML。唯一的要求是
值必须首先序列化为字符串，使用特定于
该结构类型的机制。例如，要将 JSON 序列化为字符串，你可以
使用 `JSON.stringify()` JavaScript 方法。

由于 Docker 不会反序列化值，你无法在按标签值查询或过滤时
将 JSON 或 XML 文档作为嵌套结构处理，除非
你将此功能构建到第三方工具中。

## 管理对象上的标签

每种支持标签的对象类型都有添加和
管理标签的机制，以及使用与该类型对象相关的标签。这些链接
提供了一个很好的起点来学习如何在你的
Docker 部署中使用标签。

镜像、容器、本地守护进程、卷和网络上的标签在
对象的生命周期内是静态的。要更改这些标签，你必须重新创建对象。
Swarm 节点和服务上的标签可以动态更新。

- 镜像和容器

  - [向镜像添加标签](/reference/dockerfile.md#label)
  - [在运行时覆盖容器的标签](/reference/cli/docker/container/run.md#label)
  - [检查镜像或容器上的标签](/reference/cli/docker/inspect.md)
  - [按标签过滤镜像](/reference/cli/docker/image/ls.md#filter)
  - [按标签过滤容器](/reference/cli/docker/container/ls.md#filter)

- 本地 Docker 守护进程

  - [在运行时向 Docker 守护进程添加标签](/reference/cli/dockerd.md)
  - [检查 Docker 守护进程的标签](/reference/cli/docker/system/info.md)

- 卷

  - [向卷添加标签](/reference/cli/docker/volume/create.md)
  - [检查卷的标签](/reference/cli/docker/volume/inspect.md)
  - [按标签过滤卷](/reference/cli/docker/volume/ls.md#filter)

- 网络

  - [向网络添加标签](/reference/cli/docker/network/create.md)
  - [检查网络的标签](/reference/cli/docker/network/inspect.md)
  - [按标签过滤网络](/reference/cli/docker/network/ls.md#filter)

- Swarm 节点

  - [添加或更新 Swarm 节点的标签](/reference/cli/docker/node/update.md#label-add)
  - [检查 Swarm 节点的标签](/reference/cli/docker/node/inspect.md)
  - [按标签过滤 Swarm 节点](/reference/cli/docker/node/ls.md#filter)

- Swarm 服务
  - [创建 Swarm 服务时添加标签](/reference/cli/docker/service/create.md#label)
  - [更新 Swarm 服务的标签](/reference/cli/docker/service/update.md)
  - [检查 Swarm 服务的标签](/reference/cli/docker/service/inspect.md)
  - [按标签过滤 Swarm 服务](/reference/cli/docker/service/ls.md#filter)
