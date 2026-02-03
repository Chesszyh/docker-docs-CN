---
title: 手册 (Manuals)
description: 通过这一系列用户指南，了解如何安装、设置、配置和使用 Docker 产品
keywords: docker, docs, manuals, 手册, 产品, 用户指南, user guides, how-to
# hard-code the URL of this page
url: /manuals/
layout: wide
params:
  icon: description
  sidebar:
    groups:
      - 开源 (Open source)
      - 人工智能 (AI)
      - 产品 (Products)
      - 平台 (Platform)
  notoc: true
  open-source:
  - title: Docker Build
    description: 随时随地构建并交付任何应用程序。
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
    description: 使用您偏好的编程语言以编程方式运行容器。
    icon: /icons/Testcontainers.svg
    link: /testcontainers/
  ai:
  - title: Ask Gordon
    description: 通过您的个人 AI 助手简化工作流程并充分利用 Docker 生态系统。
    icon: note_add
    link: /ai/gordon/
  - title: Docker Model Runner
    description: 查看并管理您的本地模型。
    icon: view_in_ar
    link: /ai/model-runner/
  - title: MCP 目录与工具包
    description: 使用 MCP 服务器增强您的 AI 工作流程。
    icon: /icons/toolkit.svg
    link: /ai/mcp-catalog-and-toolkit/
  products:
  - title: Docker Desktop
    description: 您的容器开发指挥中心。
    icon: /icons/Whale.svg
    link: /desktop/
  - title: Docker 硬化镜像 (Hardened Images)
    description: 用于可信软件交付的安全、精简镜像。
    icon: /icons/dhi.svg
    link: /dhi/
  - title: Build Cloud
    description: 在云端更快速地构建您的镜像。
    icon: /icons/logo-build-cloud.svg
    link: /build-cloud/
  - title: Docker Hub
    description: 发现、分享并集成容器镜像。
    icon: hub
    link: /docker-hub/
  - title: Docker Scout
    description: 镜像分析与策略评估。
    icon: /icons/Scout.svg
    link: /scout/
  - title: Docker for GitHub Copilot
    description: 将 Docker 的能力与 GitHub Copilot 相集成。
    icon: chat
    link: /copilot/
  - title: Docker 扩展 (Extensions)
    description: 自定义您的 Docker Desktop 工作流程。
    icon: extension
    link: /extensions/
  - title: Testcontainers Cloud
    description: 在云端使用真实依赖项运行集成测试。
    icon: package_2
    link: https://testcontainers.com/cloud/docs/
  platform:
  - title: 管理 (Administration)
    description: 为公司和组织提供集中的可观测性。
    icon: admin_panel_settings
    link: /admin/
  - title: 计费 (Billing)
    description: 管理计费和支付方式。
    icon: payments
    link: /billing/
  - title: 账户 (Accounts)
    description: 管理您的 Docker 账户。
    icon: account_circle
    link: /accounts/
  - title: 安全 (Security)
    description: 为管理员和开发人员提供的安全护栏。
    icon: lock
    link: /security/
  - title: 订阅 (Subscription)
    description: Docker 产品的商业使用许可。
    icon: card_membership
    link: /subscription/
---

本章节包含关于如何安装、设置、配置和使用 Docker 产品的用户指南。

## 开源 (Open source)

开源开发和容器化技术。

{{< grid items=open-source >}}

## 人工智能 (AI)

所有 Docker AI 工具的一站式入口。

{{< grid items=ai >}}

## 产品 (Products)

为创新团队提供的端到端开发人员解决方案。

{{< grid items=products >}}

## 平台 (Platform)

与 Docker 平台相关的文档，例如组织管理和订阅管理。

{{< grid items=platform >}}