---
title: 强化 Docker Desktop 概述
linkTitle: 强化 Docker Desktop
description: 强化 Docker Desktop 的概述及其主要功能
keywords: security, hardened desktop, enhanced container isolation, registry access
  management, settings management root access, admins, docker desktop, image access
  management
tags: [admin]
aliases:
 - /desktop/hardened-desktop/
grid:
  - title: "设置管理"
    description: 了解设置管理如何保护开发人员的工作流程。
    icon: shield_locked
    link: /security/for-admins/hardened-desktop/settings-management/
  - title: "增强容器隔离"
    description: 了解增强容器隔离如何防止容器攻击。
    icon: "security"
    link: /security/for-admins/hardened-desktop/enhanced-container-isolation/
  - title: "镜像仓库访问管理"
    description: 控制开发人员在使用 Docker Desktop 时可以访问的镜像仓库。
    icon: "home_storage"
    link: /security/for-admins/hardened-desktop/registry-access-management/
  - title: "镜像访问管理"
    description: 控制开发人员可以从 Docker Hub 拉取的镜像。
    icon: "photo_library"
    link: /security/for-admins/hardened-desktop/image-access-management/
  - title: "离线容器"
    description: 限制容器访问不需要的网络资源。
    icon: "vpn_lock"
    link: /security/for-admins/hardened-desktop/air-gapped-containers/
weight: 60
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

强化 Docker Desktop（Hardened Docker Desktop）是一组安全功能，旨在以最小的影响提升开发人员环境的安全性，同时不影响开发人员的体验或生产力。

它允许您强制执行严格的安全设置，防止开发人员及其容器有意或无意地绑过这些控制。此外，您还可以增强容器隔离，以减轻潜在的安全威胁，例如恶意负载突破 Docker Desktop Linux 虚拟机和底层主机。

强化 Docker Desktop 将 Docker Desktop 配置的所有权边界转移到组织，这意味着您设置的任何安全控制都不能被 Docker Desktop 的用户更改。

它适用于以下具有安全意识的组织：
- 不给用户提供其机器上的 root 或管理员访问权限
- 希望 Docker Desktop 处于组织的集中控制之下
- 有某些合规性义务

### 它如何帮助我的组织？

强化 Desktop 的各项功能独立工作，但共同创建了深度防御策略，保护开发人员工作站免受各种功能层面的潜在攻击，例如配置 Docker Desktop、拉取容器镜像和运行容器镜像。这种多层防御方法确保了全面的安全性。它有助于减轻以下威胁：

 - 恶意软件和供应链攻击：镜像仓库访问管理（Registry Access Management）和镜像访问管理（Image Access Management）阻止开发人员访问某些容器镜像仓库和镜像类型，大大降低了恶意负载的风险。此外，增强容器隔离（Enhanced Container Isolation，ECI）通过在 Linux 用户命名空间内以非 root 权限运行容器来限制恶意负载容器的影响。
 - 横向移动：离线容器（Air-gapped containers）允许您为容器配置网络访问限制，从而防止恶意容器在组织网络内进行横向移动。
 - 内部威胁：设置管理（Settings Management）配置并锁定各种 Docker Desktop 设置，以便您可以强制执行公司策略，防止开发人员有意或无意地引入不安全的配置。

{{< grid >}}
