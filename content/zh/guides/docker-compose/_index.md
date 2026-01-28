---
title: 使用 Docker Compose 定义和运行多容器应用程序
linkTitle: Docker Compose
summary: |
  简化定义、配置和运行多容器 Docker 应用程序的过程。
description: 了解如何使用 Docker Compose 定义和运行多容器 Docker 应用程序。
tags: [product-demo]
aliases:
  - /learning-paths/docker-compose/
params:
  image: images/learning-paths/compose.png
  time: 10 分钟
  resource_links:
    - title: Docker Compose CLI 概述
      url: /compose/reference/
    - title: Docker Compose 概述
      url: /compose/
    - title: Compose 工作原理
      url: /compose/intro/compose-application-model/
    - title: 在 Compose 中使用配置文件
      url: /compose/how-tos/profiles/
    - title: 使用 Compose 控制启动和关闭顺序
      url: /compose/how-tos/startup-order/
    - title: Compose 构建规范
      url: /compose/compose-file/build/
---

开发者在使用多容器 Docker 应用程序时面临诸多挑战，包括复杂的配置、依赖管理以及维护一致的环境。网络、资源分配、数据持久化、日志和监控增加了难度。安全问题和故障排查进一步使流程复杂化，需要有效的工具和实践来进行高效管理。

Docker Compose 通过提供一种简单的方式来定义、配置和运行应用程序所需的所有容器，解决了管理多容器 Docker 应用程序的问题——只需使用单个 YAML 文件。这种方法帮助开发者轻松设置、共享和维护一致的开发、测试和生产环境，确保复杂应用程序可以在所有依赖项和服务正确配置和编排的情况下进行部署。

## 您将学到

- 什么是 Docker Compose 以及它的作用
- 如何定义服务
- Docker Compose 的使用场景
- 没有 Docker Compose 时情况会有何不同

## 适用人群

- 需要在多个环境中高效定义、管理和编排多容器 Docker 应用程序的开发者和 DevOps 工程师。
- 希望通过简化开发工作流程和减少设置时间来提高生产力的开发团队。

## 工具集成

与 Docker CLI、CI/CD 工具和容器编排工具配合良好。

<div id="compose-lp-survey-anchor"></div>
