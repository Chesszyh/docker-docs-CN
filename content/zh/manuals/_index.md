---
title: 手册
description: 通过本用户指南合集，学习如何安装、设置、配置和使用 Docker 产品
keywords: docker, docs, manuals, products, user guides, how-to
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
    description: 在任何地方构建和发布任何应用程序。
    icon: build
    link: /build/
  - title: Docker Engine
    description: 行业领先的容器运行时。
    icon: developer_board
    link: /engine/
  - title: Docker Compose
    description: 定义和运行多容器应用程序。
    icon: /icons/Compose.svg
    link: /compose/
  - title: Testcontainers
    description: 使用您首选的编程语言以编程方式运行容器。
    icon: /icons/Testcontainers.svg
    link: /testcontainers/
  ai:
  - title: Ask Gordon
    description: 借助您的个人 AI 助手，简化工作流程并充分利用 Docker 生态系统。
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
    description: 容器开发的指挥中心。
    icon: /icons/Whale.svg
    link: /desktop/
  - title: Docker Hardened Images
    description: 用于可信软件交付的安全、精简镜像。
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
    description: 在云端运行集成测试，使用真实的依赖项。
    icon: package_2
    link: https://testcontainers.com/cloud/docs/
  platform:
  - title: 管理
    description: 为公司和组织提供集中化的可观测性。
    icon: admin_panel_settings
    link: /admin/
  - title: 计费
    description: 管理计费和付款方式。
    icon: payments
    link: /billing/
  - title: 账户
    description: 管理您的 Docker 账户。
    icon: account_circle
    link: /accounts/
  - title: 安全
    description: 为管理员和开发者提供安全防护。
    icon: lock
    link: /security/
  - title: 订阅
    description: Docker 产品的商业使用许可。
    icon: card_membership
    link: /subscription/
---

本节包含关于如何安装、设置、配置和使用 Docker 产品的用户指南。

## 开源

开源开发和容器化技术。

{{< grid items=open-source >}}

## AI

所有 Docker AI 工具集中在一个便于访问的位置。

{{< grid items=ai >}}

## 产品

为创新团队提供的端到端开发者解决方案。

{{< grid items=products >}}

## 平台

与 Docker 平台相关的文档，例如组织的管理和订阅管理。

{{< grid items=platform >}}
