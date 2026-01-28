---
title: 手册
description: 了解如何安装、设置、配置和使用 Docker 产品，请参阅此用户指南合集
keywords: docker, 文档, 手册, 产品, 用户指南, 操作指南
# hard-code the URL of this page
url: /manuals/
layout: wide
params:
  icon: description
  sidebar:
    groups:
      - 开源
      - AI
      - 产品
      - 平台
  notoc: true
  open-source:
  - title: Docker Build
    description: 构建并交付任何应用到任何地方。
    icon: build
    link: /build/
  - title: Docker Engine
    description: 业界领先的容器运行时。
    icon: developer_board
    link: /engine/
  - title: Docker Compose
    description: 定义和运行多容器应用程序。
    icon: /icons/Compose.svg
    link: /compose/
  - title: Testcontainers
    description: 使用您偏好的编程语言以编程方式运行容器。
    icon: /icons/Testcontainers.svg
    link: /testcontainers/
  ai:
  - title: Ask Gordon
    description: 使用您的个人 AI 助手简化工作流程并充分利用 Docker 生态系统。
    icon: note_add
    link: /ai/gordon/
  - title: Docker Model Runner
    description: 查看和管理您的本地模型。
    icon: view_in_ar
    link: /ai/model-runner/
  - title: MCP 目录和工具包
    description: 使用 MCP 服务器增强您的 AI 工作流程。
    icon: /icons/toolkit.svg
    link: /ai/mcp-catalog-and-toolkit/
  products:
  - title: Docker Desktop
    description: 您的容器开发指挥中心。
    icon: /icons/Whale.svg
    link: /desktop/
  - title: Docker Hardened Images
    description: 用于可信软件交付的安全、最小化镜像。
    icon: /icons/dhi.svg
    link: /dhi/
  - title: Build Cloud
    description: 在云端更快速地构建您的镜像。
    icon: /icons/logo-build-cloud.svg
    link: /build-cloud/
  - title: Docker Hub
    description: 发现、共享和集成容器镜像。
    icon: hub
    link: /docker-hub/
  - title: Docker Scout
    description: 镜像分析和策略评估。
    icon: /icons/Scout.svg
    link: /scout/
  - title: Docker for GitHub Copilot
    description: 将 Docker 的功能与 GitHub Copilot 集成。
    icon: chat
    link: /copilot/
  - title: Docker Extensions
    description: 自定义您的 Docker Desktop 工作流程。
    icon: extension
    link: /extensions/
  - title: Testcontainers Cloud
    description: 在云端运行具有真实依赖项的集成测试。
    icon: package_2
    link: https://testcontainers.com/cloud/docs/
  platform:
  - title: 管理
    description: 针对公司和组织的集中可观测性。
    icon: admin_panel_settings
    link: /admin/
  - title: 账单
    description: 管理账单和付款方式。
    icon: payments
    link: /billing/
  - title: 账户
    description: 管理您的 Docker 账户。
    icon: account_circle
    link: /accounts/
  - title: 安全
    description: 为管理员和开发人员提供的安全防护。
    icon: lock
    link: /security/
  - title: 订阅
    description: Docker 产品的商业使用许可证。
    icon: card_membership
    link: /subscription/
---

本部分包含关于如何安装、设置、配置和使用 Docker 产品的用户指南。

## 开源

开源开发和容器化技术。

{{< grid items=open-source >}}

## AI

所有 Docker AI 工具都在一个易于访问的位置。

{{< grid items=ai >}}

## 产品

面向创新团队的端到端开发者解决方案。

{{< grid items=products >}}

## 平台

与 Docker 平台相关的文档，例如组织的管理和订阅管理。

{{< grid items=platform >}}
