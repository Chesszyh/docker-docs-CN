---
title: Docker Build
weight: 20
description: 概述 Docker Build，用于打包和捆绑您的代码并将其发布到任何地方
keywords: build, buildx, buildkit
params:
  sidebar:
    group: 开源
grid:
- title: 打包您的软件
  description: '构建和打包您的应用程序，以便在任何地方运行：本地或云端。'
  icon: inventory_2
  link: /build/concepts/overview/
- title: 多阶段构建
  description: 使用最少的依赖项，保持镜像小巧安全。
  icon: stairs
  link: /build/building/multi-stage/
- title: 多平台镜像
  description: 在不同计算机架构上无缝构建、推送、拉取和运行镜像。
  icon: content_copy
  link: /build/building/multi-platform/
- title: BuildKit
  description: 探索开源构建引擎 BuildKit。
  icon: construction
  link: /build/buildkit/
- title: 构建驱动程序
  description: 配置构建的运行位置和方式。
  icon: engineering
  link: /build/builders/drivers/
- title: 导出器
  description: 导出您喜欢的任何工件，而不仅仅是 Docker 镜像。
  icon: output
  link: /build/exporters/
- title: 构建缓存
  description: 避免不必要的重复昂贵操作，例如包安装。
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

Docker Build 是 Docker Engine 最常用的功能之一。无论何时创建镜像，您都在使用 Docker Build。Build 是您软件开发生命周期的关键部分，它允许您打包和捆绑您的代码并将其发布到任何地方。

Docker Build 不仅仅是构建镜像的命令，它也不仅仅是打包您的代码。它是一个完整的工具和功能生态系统，不仅支持常见的工作流任务，还为更复杂和高级的场景提供支持。

{{< grid >}}
