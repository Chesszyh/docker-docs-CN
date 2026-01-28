---
title: 构建镜像
weight: 20
keywords: build images, Dockerfile, layers, tag, push, cache, multi-stage, 构建镜像, 层, 标记, 推送, 缓存, 多阶段
description: |
  学习如何从 Dockerfile 构建 Docker 镜像。您将了解 Dockerfile 的结构、如何构建镜像以及如何自定义构建过程。
summary: |
  构建容器镜像既是一项技术也是一门艺术。您希望保持镜像小巧且专注，以提高安全性，但也需要权衡潜在的取舍，例如缓存影响。在本系列中，您将深入研究镜像的秘密、它们的构建方式以及最佳实践。
layout: series
params:
  skill: Beginner
  time: 25 minutes
  prereq: None
---

## 关于本系列

学习如何构建生产就绪、精简且高效的 Docker 镜像，这对于最小化开销和增强生产环境中的部署至关重要。

## 您将学到什么

- 理解镜像层
- 编写 Dockerfile
- 构建、标记并发布镜像
- 使用构建缓存
- 多阶段构建