---
title: Docker Compose
weight: 30
description: 详细了解如何使用 Docker Compose 定义和运行多容器应用程序。
keywords: docker compose, docker-compose, compose.yaml, docker compose 命令, 多容器应用程序, 容器编排, docker cli
params:
  sidebar:
    group: 开源
grid:
- title: 为什么使用 Compose？
  description: 了解 Docker Compose 的主要优势
  icon: feature_search
  link: /compose/intro/features-uses/
- title: Compose 如何工作
  description: 了解 Compose 的工作原理
  icon: category
  link: /compose/intro/compose-application-model/
- title: 安装 Compose
  description: 按照说明安装 Docker Compose。
  icon: download
  link: /compose/install
- title: 快速入门
  description: 在构建一个简单的 Python Web 应用程序的同时学习 Docker Compose 的核心概念。
  icon: explore
  link: /compose/gettingstarted
- title: 查看发行说明
  description: 了解最新的功能增强和 Bug 修复。
  icon: note_add
  link: /compose/release-notes
- title: 探索 Compose 文件参考
  description: 查找关于为 Docker 应用程序定义服务、网络和卷的信息。
  icon: polyline
  link: /reference/compose-file
- title: 使用 Compose Bridge
  description: 将您的 Compose 配置文件转换为适用于不同平台（如 Kubernetes）的配置文件。
  icon: move_down
  link: /compose/bridge
- title: 浏览常见问题 (FAQ)
  description: 探索常见问题并了解如何提供反馈。
  icon: help
  link: /compose/faq
- title: 迁移到 Compose v2
  description: 了解如何从 Compose v1 迁移到 v2
  icon: folder_delete
  link: /compose/releases/migrate/
aliases:
- /compose/cli-command/
- /compose/networking/swarm/
- /compose/overview/
- /compose/swarm/
- /compose/completion/
---

Docker Compose 是一个用于定义和运行多容器应用程序的工具。它是开启流线型、高效开发和部署体验的关键。

Compose 简化了对整个应用程序栈的控制，通过单个 YAML 配置文件即可轻松管理服务、网络和卷。然后，只需一个命令，您就可以根据配置文件创建并启动所有服务。

Compose 适用于所有环境——生产、预发布、开发、测试以及 CI 工作流。它还提供了管理应用程序整个生命周期的命令：

 - 启动、停止和重新构建服务
 - 查看运行中服务的状态
 - 实时查看运行中服务的日志输出
 - 在服务上运行一次性命令

{{< grid >}}
