---
description: 容器化 Golang 应用程序并使用 Prometheus 和 Grafana 对其进行监控。
keywords: golang, prometheus, grafana, monitoring, containerize
title: 使用 Prometheus 和 Grafana 监控 Golang 应用程序
summary: |
  了解如何容器化 Golang 应用程序并使用 Prometheus 和 Grafana 对其进行监控。
linkTitle: 使用 Prometheus 和 Grafana 进行监控
languages: [go]
params:
  time: 45 minutes
---

本指南教你如何容器化 Golang 应用程序并使用 Prometheus 和 Grafana 对其进行监控。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 概览

为了确保你的应用程序按预期工作，监控非常重要。最受欢迎的监控工具之一是 Prometheus。Prometheus 是一个开源监控和警报工具包，专为可靠性和可扩展性而设计。它通过抓取受监控目标上的指标 HTTP 端点来从这些目标收集指标。要可视化指标，你可以使用 Grafana。Grafana 是一个用于监控和可观测性的开源平台，允许你查询、可视化、警报和了解你的指标，无论它们存储在哪里。

在本指南中，你将创建一个带有一些端点的 Golang 服务器来模拟真实应用程序。然后，你将使用 Prometheus 公开服务器的指标。最后，你将使用 Grafana 可视化指标。你将容器化 Golang 应用程序，并使用 Docker Compose 文件连接所有服务：Golang、Prometheus 和 Grafana。

## 你将学到什么？

* 创建具有自定义 Prometheus 指标的 Golang 应用程序。
* 容器化 Golang 应用程序。
* 使用 Docker Compose 运行多个服务并将它们连接在一起，以便使用 Prometheus 和 Grafana 监控 Golang 应用程序。
* 使用 Grafana 仪表板可视化指标。

## 先决条件

- 假设你对 Golang 有很好的了解。
- 你必须熟悉 Prometheus 并在 Grafana 中创建仪表板。
- 你必须熟悉 Docker 概念，如容器、镜像和 Dockerfile。如果你是 Docker 新手，可以从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

## 后续步骤

你将创建一个 Golang 服务器并使用 Prometheus 公开指标。
