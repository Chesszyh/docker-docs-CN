---
title: 使用 Docker 助力公司成功
linkTitle: 管理员设置
summary: 通过简化工作流程、标准化开发环境并确保在整个公司内顺利部署，充分利用 Docker。
description: 了解如何引导你的公司并利用所有 Docker 产品和功能。
tags: [admin]
params:
  featured: true
  time: 20 分钟
  image: 
  resource_links:
    - title: Docker 管理概述
      url: /admin/
    - title: 单点登录
      url: /security/for-admins/single-sign-on/
    - title: 强制登录
      url: /security/for-admins/enforce-sign-in/
    - title: 角色和权限
      url: /security/for-admins/roles-and-permissions/
    - title: 设置管理
      url: /security/for-admins/hardened-desktop/settings-management/
    - title: 注册表访问管理
      url: /security/for-admins/hardened-desktop/registry-access-management/
    - title: 镜像访问管理
      url: /security/for-admins/hardened-desktop/image-access-management/
    - title: Docker 订阅信息
      url: /subscription/details/
---

Docker 的工具提供了一个可扩展、安全的平台，使你的开发人员能够更快地创建、交付和运行应用程序。作为管理员，你能够简化工作流程、标准化开发环��并确保在整个组织内顺利部署。

通过配置 Docker 产品以满足你公司的需求，你可以优化性能、简化用户管理并保持对资源的控制。本指南将帮助你设置和配置 Docker 产品，以最大限度地提高团队的生产力和成功率，同时满足合规性和安全策略。

## 适用人群

- 负责在其组织内管理 Docker 环境的管理员
- 希望简化开发和部署工作流程的 IT 领导者
- 旨在跨多个用户标准化应用程序环境的团队
- 寻求优化其 Docker 产品使用以实现更大可扩展性和效率的组织
- 拥有 [Docker Business 订阅](https://www.docker.com/pricing/)的组织。

## 你将学到什么

- 登录公司 Docker 组织以访问使用数据和增强功能的重要性。
- 如何标准化 Docker Desktop 版本和设置，为所有用户创建一致的基线，同时为高级开发人员提供灵活性。
- 实施 Docker 安全配置的策略，以满足公司 IT 和软件开发安全要求，而不会妨碍开发人员的生产力。

## 涵盖的功能

- 组织。这些是管理你的 Docker 环境的核心结构，对用户、团队和镜像存储库进行分组。你的组织是在你的订阅中创建的，并由一个或多个所有者管理。登录到该组织的用户将根据购买的订阅分配席位。
- 强制登录。默���情况下，Docker Desktop 不需要登录。但是，你可以配置设置以强制执行此操作，并确保你的开发人员登录到你的 Docker 组织。
- SSO。如果没有 SSO，Docker 组织中的用户管理是手动的。在你的身份提供商和 Docker 之间建立 SSO 连接可确保符合你的安全策略并自动执行用户配置。添加 SCIM 可进一步自动执行用户配置和取消配置。
- 常规和安全设置。配置关键设置将确保在你的环境中顺利引导和使用 Docker 产品。此外，你可以根据公司的特定安全需求启用安全功能。

## 需要哪些人参与？

- Docker 组织所有者：Docker 组织所有者必须参与该过程，并且在几个关键步骤中都需要他。
- DNS 团队：在 SSO 设置期间需要 DNS 团队来验证公司域。
- MDM 团队：负责将 Docker 特定的配置文件分发到开发人员计算机。
- 身份提供商团队：需要在设置期间配置身份提供商并建立 SSO 连接。
- 开发负责人：具有 Docker 配置知识的开发负责人，以帮助为开发人员设置建立基线。
- IT 团队：熟悉公司桌面策略的 IT 代表，以协助将 Docker 配置与这些策略保持一致。
- 信息安全：具有公司开发安全策略知识的安全团队成员，以帮助配置安全功能。
- Docker 测试人员：一小部分开发人员，在全面部署之前测试新的设置和配置。

## 工具集成

Okta、Entra ID SAML 2.0、Azure Connect (OIDC)、Intune 等 MDM 解决方案
