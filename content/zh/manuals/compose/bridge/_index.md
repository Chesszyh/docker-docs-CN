---
description: 了解 Compose Bridge 如何将 Docker Compose 文件转换为 Kubernetes 清单，以实现无缝的平台转换
keywords: docker compose bridge, compose to kubernetes, docker compose kubernetes integration, docker compose kustomize, compose bridge docker desktop, 转换, 集成, 自定义
title: Compose Bridge 概述
linkTitle: Compose Bridge
weight: 50
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 将您的 Docker Compose 配置转换为特定于平台的格式——主要是 Kubernetes 清单。默认转换会生成 Kubernetes 清单和一个 Kustomize 覆盖，这些清单和覆盖专为在启用了 Kubernetes 的 Docker Desktop 上部署而设计。

它是一个灵活的工具，可让您利用[默认转换](usage.md)或[创建自定义转换](customize.md)以满足特定的项目需求和要求。

Compose Bridge 极大地简化了从 Docker Compose 到 Kubernetes 的过渡，使您更容易利用 Kubernetes 的强大功能，同时保持 Docker Compose 的简单性和效率。

## 工作原理

Compose Bridge 使用转换让您可以将 Compose 模型转换为另一种形式。

转换被打包为一个 Docker 镜像，它接收完全解析的 Compose 模型作为 `/in/compose.yaml`，并可以在 `/out` 下生成任何目标格式的文件。

Compose Bridge 使用 Go 模板为 Kubernetes 提供自己的转换，以便通过替换或附加您自己的模板轻松进行自定义扩展。

有关这些转换如何工作以及如何为您的项目自定义它们的更多详细信息，请参阅[自定义](customize.md)。

## 下一步是什么？

- [使用 Compose Bridge](usage.md)
- [探索如何自定义 Compose Bridge](customize.md)
