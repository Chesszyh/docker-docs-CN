---
title: 下一步是什么
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 浏览分步指南，帮助您了解核心 Docker 概念、构建镜像和运行容器。
aliases:
 - /guides/getting-started/whats-next/
summary: |
  现在您已经设置了 Docker Desktop，使用容器进行了开发，并构建
  和推送了您的第一个镜像，您已准备好迈出下一步，深入
  了解什么是容器以及它是如何工作的。
notoc: true
weight: 4

the-basics:
- title: 什么是容器？
  description: 了解如何运行您的第一个容器。
  link: /get-started/docker-concepts/the-basics/what-is-a-container/
- title: 什么是镜像？
  description: 了解镜像层的基础知识。
  link: /get-started/docker-concepts/the-basics/what-is-an-image/
- title: 什么是仓库？
  description: 了解容器仓库，探索它们的互操作性，并与仓库进行交互。
  link: /get-started/docker-concepts/the-basics/what-is-a-registry/
- title: 什么是 Docker Compose？
  description: 更好地了解 Docker Compose。
  link: /get-started/docker-concepts/the-basics/what-is-docker-compose/

building-images:
- title: 了解镜像层
  description: 了解容器镜像的层。
  link: /get-started/docker-concepts/building-images/understanding-image-layers/
- title: 编写 Dockerfile
  description: 了解如何使用 Dockerfile 创建镜像。
  link: /get-started/docker-concepts/building-images/writing-a-dockerfile/
- title: 构建、标记和发布镜像
  description: 了解如何构建、标记和发布镜像到 Docker Hub 或任何其他仓库。
  link: /get-started/docker-concepts/building-images/build-tag-and-publish-an-image/
- title: 使用构建缓存
  description: 了解构建缓存、哪些更改会使缓存失效以及如何有效地使用构建缓存。
  link: /get-started/docker-concepts/building-images/using-the-build-cache/
- title: 多阶段构建
  description: 更好地了解多阶段构建及其好处。
  link: /get-started/docker-concepts/building-images/multi-stage-builds/

running-containers:
- title: 发布端口
  description: 了解在 Docker 中发布和公开端口的重要性。
  link: /get-started/docker-concepts/running-containers/publishing-ports/
- title: 覆盖容器默认值
  description: 了解如何使用 `docker run` 命令覆盖容器默认值。
  link: /get-started/docker-concepts/running-containers/overriding-container-defaults/
- title: 持久化容器数据
  description: 了解 Docker 中数据持久性的重要性。
  link: /get-started/docker-concepts/running-containers/persisting-container-data/
- title: 与容器共享本地文件
  description: 探索 Docker 中可用的各种存储选项及其常见用法。
  link: /get-started/docker-concepts/running-containers/sharing-local-files/
- title: 多容器应用程序
  description: 了解多容器应用程序的重要性以及它们与单容器应用程序的不同之处。
  link: /get-started/docker-concepts/running-containers/multi-container-applications/
---

以下部分提供了分步指南，可帮助您了解核心 Docker 概念、构建镜像和运行容器。

## 基础知识

开始学习容器、镜像、仓库和 Docker Compose 的核心概念。

{{< grid items="the-basics" >}}

## 构建镜像

使用 Dockerfile、构建缓存和多阶段构建来制作优化的容器镜像。

{{< grid items="building-images" >}}

## 运行容器

掌握公开端口、覆盖默认值、持久化数据、共享文件和管理多容器应用程序的基本技术。

{{< grid items="running-containers" >}}
