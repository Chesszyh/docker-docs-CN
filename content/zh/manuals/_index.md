---
title: 使用手册
description: 了解如何安装、设置、配置和使用 Docker 产品，包含用户指南合集
keywords: docker, docs, manuals, products, user guides, how-to, 产品, 用户指南, 手册
# hard-code the URL of this page
url: /manuals/
layout: wide
params:
  icon: description
  sidebar:
    groups:
      - Open source
      - AI
      - Products
      - Platform
  notoc: true
  open-source:
  - title: Docker Build
    description: 构建任意应用并发布到任何地方。
    icon: build
    link: /build/
  - title: Docker Engine
    description: 行业领先的容器运行时。
    icon: developer_board
    link: /engine/
  - title: Docker Compose
    description: 定义并运行多容器应用程序。
    icon: /icons/Compose.svg
    link: /compose/
  - title: Testcontainers
    description: 使用您偏好的编程语言通过编程方式运行容器。
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
  - title: MCP Catalog and Toolkit
    description: 使用 MCP 服务器增强您的 AI 工作流程。
    icon: /icons/toolkit.svg
    link: /ai/mcp-catalog-and-toolkit/
  products:
  - title: Docker Desktop
    description: 您容器开发的指挥中心。
    icon: /icons/Whale.svg
    link: /desktop/
  - title: Docker Hardened Images
    description: 用于可信软件交付的安全、最小化镜像。
    icon: /icons/dhi.svg
    link: /dhi/
  - title: Build Cloud
    description: 在云端更快地构建您的镜像。
    icon: /icons/logo-build-cloud.svg
    link: /build-cloud/
  - title: Docker Hub
    description: 发现、分享和集成容器镜像。
    icon: hub
    link: /docker-hub/
  - title: Docker Scout
    description: 镜像分析与策略评估。
    icon: /icons/Scout.svg
    link: /scout/
  - title: Docker for GitHub Copilot
    description: 将 Docker 的功能集成到 GitHub Copilot 中。
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
  - title: Administration
    description: 面向公司和组织的集中式可观测性。
    icon: admin_panel_settings
    link: /admin/
  - title: Billing
    description: 管理账单和支付方式。
    icon: payments
    link: /billing/
  - title: Accounts
    description: 管理您的 Docker 账户。
    icon: account_circle
    link: /accounts/
  - title: Security
    description: 面向管理员和开发人员的安全防护。
    icon: lock
    link: /security/
  - title: Subscription
    description: Docker 产品的商业使用许可。
    icon: card_membership
    link: /subscription/
---

本部分包含关于如何安装、设置、配置和使用 Docker 产品的用户指南。

## 开源

开源开发与容器化技术。

{{< grid items=open-source >}}

## AI

所有 Docker AI 工具的一站式获取中心。

{{< grid items=ai >}}

## 产品

面向创新团队的端到端开发者解决方案。

{{< grid items=products >}}

## 平台

与 Docker 平台相关的文档，例如面向组织及其成员的管理和订阅管理。

{{< grid items=platform >}}