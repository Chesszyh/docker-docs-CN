---
title: 构建镜像
weight: 20
keywords: build images, Dockerfile, layers, tag, push, cache, multi-stage
description: |
  学习如何从 Dockerfile 构建 Docker 镜像。您将了解 Dockerfile 的结构、如何构建镜像以及如何自定义构建过程。
summary: |
  构建容器镜像既是技术工作也是一门艺术。您希望保持镜像小巧且专注以提高安全性，但也需要平衡潜在的权衡，例如缓存影响。在本系列中，您将深入了解镜像的奥秘、它们是如何构建的以及最佳实践。
layout: series
params:
  skill: 初学者
  time: 25 分钟
  prereq: 无
---

## 关于本系列

学习如何构建精简高效的生产就绪镜像，这对于最小化开销和增强生产环境中的部署至关重要。

## 您将学到什么

- 理解镜像层
- 编写 Dockerfile
- 构建、标记和发布镜像
- 使用构建缓存
- 多阶段构建
