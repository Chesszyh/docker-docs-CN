---
title: Docker Build
weight: 20
description: 了解 Docker Build 概览，用于打包并分发您的代码
keywords: build, buildx, buildkit, 构建
params:
  sidebar:
    group: 开源 (Open source)
grid:
- title: 软件打包
  description: '构建并打包您的应用程序，以便在任何地方运行：本地或云端。'
  icon: inventory_2
  link: /build/concepts/overview/
- title: 多阶段构建
  description: 通过最小依赖项保持镜像精简且安全。
  icon: stairs
  link: /build/building/multi-stage/
- title: 多平台镜像
  description: 在不同的计算机架构上无缝构建、推送、拉取和运行镜像。
  icon: content_copy
  link: /build/building/multi-platform/
- title: BuildKit
  description: 探索 BuildKit，这款开源的构建引擎。
  icon: construction
  link: /build/buildkit/
- title: 构建驱动
  description: 配置在何处以及如何运行您的构建。
  icon: engineering
  link: /build/builders/drivers/
- title: 导出器 (Exporters)
  description: 导出您喜欢的任何产物，而不仅仅是 Docker 镜像。
  icon: output
  link: /build/exporters/
- title: 构建缓存
  description: 避免昂贵操作（如软件包安装）的不必要重复执行。
  icon: cycle
  link: /build/cache/
- title: Bake
  description: 使用 Bake 编排您的构建任务。
  icon: cake
  link: /build/bake/
aliases:
- /buildx/working-with-buildx/
- /develop/develop-images/build_enhancements/
---

Docker Build 是 Docker Engine 中使用最频繁的特性之一。每当您创建镜像时，都在使用 Docker Build。构建是软件开发生命周期的关键环节，允许您打包代码并分发到任何地方。

Docker Build 不仅仅是一个构建镜像的命令，也不仅仅关乎打包代码。它是一个由工具和特性组成的完整生态系统，不仅支持常见的工作流任务，还能支持更复杂和高级的场景。

{{< grid >}}