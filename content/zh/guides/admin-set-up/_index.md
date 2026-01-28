---
title: 为您的公司设置 Docker 以取得成功
linkTitle: 管理员设置
summary: 通过简化工作流程、标准化开发环境并确保在整个公司范围内顺利部署，充分发挥 Docker 的优势。
description: 了解如何为您的公司配置并充分利用 Docker 的所有产品和功能。
tags: [admin]
params:
  featured: true
  time: 20 minutes
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
    - title: 镜像仓库访问管理
      url: /security/for-admins/hardened-desktop/registry-access-management/
    - title: 镜像访问管理
      url: /security/for-admins/hardened-desktop/image-access-management/
    - title: Docker 订阅信息
      url: /subscription/details/
---

Docker 的工具提供了一个可扩展、安全的平台，使您的开发人员能够更快地创建、发布和运行应用程序。作为管理员，您可以简化工作流程、标准化开发环境，并确保在整个组织范围内顺利部署。

通过配置 Docker 产品以满足公司需求，您可以优化性能、简化用户管理并保持对资源的控制。本指南将帮助您设置和配置 Docker 产品，以最大限度地提高团队的生产力和成功率，同时满足合规性和安全策略要求。

## 本指南适用于谁？

- 负责管理组织内 Docker 环境的管理员
- 希望简化开发和部署工作流程的 IT 领导者
- 希望在多个用户之间标准化应用程序环境的团队
- 希望优化 Docker 产品使用以实现更大可扩展性和效率的组织
- 拥有 [Docker Business 订阅](https://www.docker.com/pricing/)的组织

## 您将学到什么

- 登录公司 Docker 组织的重要性，以便访问使用数据和增强功能。
- 如何标准化 Docker Desktop 版本和设置，为所有用户创建一致的基准，同时为高级开发人员保留灵活性。
- 实施 Docker 安全配置的策略，以满足公司 IT 和软件开发安全要求，同时不妨碍开发人员的生产力。

## 涵盖的功能

- 组织。这是管理 Docker 环境的核心结构，用于分组用户、团队和镜像仓库。您的组织是在订阅时创建的，由一个或多个所有者管理。登录到组织的用户将根据购买的订阅分配席位。
- 强制登录。默认情况下，Docker Desktop 不要求登录。但是，您可以配置设置来强制执行此操作，确保您的开发人员登录到您的 Docker 组织。
- SSO（单点登录）。没有 SSO，Docker 组织中的用户管理是手动的。在您的身份提供商和 Docker 之间设置 SSO 连接可确保符合您的安全策略并自动化用户配置。添加 SCIM（跨域身份管理系统）可进一步自动化用户的配置和取消配置。
- 通用和安全设置。配置关键设置将确保在您的环境中顺利完成 Docker 产品的入门和使用。此外，您可以根据公司的特定安全需求启用安全功能。

## 需要哪些人员参与？

- Docker 组织所有者：Docker 组织所有者必须参与该过程，并且在几个关键步骤中是必需的。
- DNS 团队：在 SSO 设置期间需要 DNS 团队来验证公司域名。
- MDM 团队：负责将 Docker 特定的配置文件分发到开发人员机器。
- 身份提供商团队：在设置期间需要配置身份提供商并建立 SSO 连接。
- 开发负责人：具有 Docker 配置知识的开发负责人，帮助建立开发人员设置的基准。
- IT 团队：熟悉公司桌面策略的 IT 代表，协助将 Docker 配置与这些策略保持一致。
- 信息安全团队：了解公司开发安全策略的安全团队成员，帮助配置安全功能。
- Docker 测试人员：一小组开发人员，在全面部署之前测试新的设置和配置。

## 工具集成

Okta、Entra ID SAML 2.0、Azure Connect (OIDC)、MDM 解决方案（如 Intune）
