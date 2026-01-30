---
description: 使用镜像访问管理管理 Docker Hub 镜像访问，将开发人员限制为可信镜像以增强安全性
keywords: image, access, management, trusted content, permissions, Docker Business feature, security, admin
title: 镜像访问管理
tags: [admin]
aliases:
 - /docker-hub/image-access-management/
 - /desktop/hardened-desktop/image-access-management/
 - /admin/organization/image-access/
 - /security/for-admins/image-access-management/
weight: 40
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

镜像访问管理（Image Access Management）使您能够控制开发人员可以从 Docker Hub 拉取哪些类型的镜像，例如 Docker 官方镜像、Docker 认证发布者镜像或社区镜像。

例如，一个属于某组织的开发人员在构建新的容器化应用程序时，可能会意外地使用不受信任的社区镜像作为其应用程序的组件。该镜像可能是恶意的，对公司构成安全风险。使用镜像访问管理，组织所有者可以确保开发人员只能访问可信内容，如 Docker 官方镜像、Docker 认证发布者镜像或组织自己的镜像，从而防止此类风险。

## 先决条件

您首先需要[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)，以确保所有 Docker Desktop 开发人员都使用您的组织进行身份验证。由于镜像访问管理需要 Docker Business 订阅，强制登录可确保只有经过身份验证的用户才能访问，并且该功能在所有用户中始终生效，即使在没有强制登录的情况下它仍可能工作。

> [!IMPORTANT]
>
> 您必须在镜像访问管理中使用[个人访问令牌（PAT）](/manuals/security/for-developers/access-tokens.md)。组织访问令牌（OAT）不兼容。

## 配置

{{< tabs >}}
{{< tab name="Admin Console" >}}

{{% admin-image-access product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-image-access product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 更多资源

- [视频：强化 Desktop 镜像访问管理](https://www.youtube.com/watch?v=r3QRKHA1A5U)
