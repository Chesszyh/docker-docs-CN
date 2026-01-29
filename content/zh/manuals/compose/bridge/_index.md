---
description: 了解 Compose Bridge 如何将 Docker Compose 文件转换为 Kubernetes 清单，以实现无缝的平台转换
keywords: docker compose bridge, compose to kubernetes, docker compose kubernetes integration, docker compose kustomize, compose bridge docker desktop
title: Compose Bridge 概览
linkTitle: Compose Bridge
weight: 50
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 将您的 Docker Compose 配置转换为特定于平台的格式——主要是 Kubernetes 清单。默认转换会生成 Kubernetes 清单和 Kustomize 叠加层（overlay），这些是专为在启用了 Kubernetes 的 Docker Desktop 上部署而设计的。

它是一个灵活的工具，允许您利用 [默认转换](usage.md) 或 [创建自定义转换](customize.md) 以满足特定项目的需求和要求。

Compose Bridge 显著简化了从 Docker Compose 到 Kubernetes 的过渡，使您能够在保持 Docker Compose 的简单和高效的同时，更轻松地利用 Kubernetes 的强大功能。

## 工作原理

Compose Bridge 使用转换（transformations）功能让您将 Compose 模型转换为另一种形式。

转换被打包为一个 Docker 镜像，它接收完全解析后的 Compose 模型（作为 `/in/compose.yaml`），并可以在 `/out` 下生成任何目标格式的文件。

Compose Bridge 使用 Go 模板为 Kubernetes 提供了其自身的转换，因此通过替换或追加您自己的模板即可轻松进行扩展以实现自定义。

有关这些转换如何工作以及如何为您的项目自定义它们的更详细信息，请参阅 [自定义](customize.md)。

## 下一步

- [使用 Compose Bridge](usage.md)
- [探索如何自定义 Compose Bridge](customize.md)
