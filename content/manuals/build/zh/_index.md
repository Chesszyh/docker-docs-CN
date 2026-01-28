---
title: Docker Build
weight: 20
description: 获取 Docker Build 概述，用于打包和捆绑您的代码并将其发送到任何地方
keywords: build, buildx, buildkit
params:
  sidebar:
    group: Open source
grid:
- title: 打包您的软件
  description: '构建并打包您的应用程序，使其可以在任何地方运行：本地或云端。'
  icon: inventory_2
  link: /build/concepts/overview/
- title: 多阶段构建
  description: 通过最小化依赖项来保持镜像的小巧和安全。
  icon: stairs
  link: /build/building/multi-stage/
- title: 多平台镜像
  description: 在不同的计算机架构上无缝构建、推送、拉取和运行镜像。
  icon: content_copy
  link: /build/building/multi-platform/
- title: BuildKit
  description: 探索 BuildKit，这是一个开源构建引擎。
  icon: construction
  link: /build/buildkit/
- title: 构建驱动程序
  description: 配置在何处以及如何运行您的构建。
  icon: engineering
  link: /build/builders/drivers/
- title: 导出器
  description: 导出任何您喜欢的构件，不仅仅是 Docker 镜像。
  icon: output
  link: /build/exporters/
- title: 构建缓存
  description: 避免不必要地重复执行代价高昂的操作，例如软件包安装。
  icon: cycle
  link: /build/cache/
- title: Bake
  description: 使用 Bake 编排您的构建。
  icon: cake
  link: /build/bake/
aliases:
- /buildx/working-with-buildx/
- /develop/develop-images/build_enhancements/
---

Docker Build 是 Docker Engine 最常用的功能之一。每当您创建镜像时，您都在使用 Docker Build。Build 是软件开发生命周期的关键部分，它允许您打包和捆绑代码并将其发送到任何地方。

Docker Build 不仅仅是一个用于构建镜像的命令，它也不仅仅是打包您的代码。它是一个完整的工具和功能生态系统，不仅支持常见的工作流任务，还为更复杂和高级的场景提供支持。

{{< grid >}}
