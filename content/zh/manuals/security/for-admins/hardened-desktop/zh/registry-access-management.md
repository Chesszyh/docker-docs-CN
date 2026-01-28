---
description: 使用镜像仓库访问管理控制对已批准镜像仓库的访问，确保 Docker Desktop 的安全使用
keywords: registry, access, management, permissions, Docker Business feature, security, admin
title: 镜像仓库访问管理
tags: [admin]
aliases:
 - /desktop/hardened-desktop/registry-access-management/
 - /admin/organization/registry-access/
 - /docker-hub/registry-access-management/
 - /security/for-admins/registry-access-management/
weight: 30
---

{{< summary-bar feature_name="Registry access management" >}}

使用镜像仓库访问管理（Registry Access Management，RAM），管理员可以确保使用 Docker Desktop 的开发人员只访问允许的镜像仓库。这是通过 Docker Hub 或 Docker Admin Console 中的镜像仓库访问管理仪表板完成的。

镜像仓库访问管理支持云端和本地镜像仓库。此功能在 DNS 级别运行，因此与所有镜像仓库兼容。您可以将任何想要包含在允许镜像仓库列表中的主机名或域名添加进去。但是，如果镜像仓库重定向到其他域（如 `s3.amazon.com`），则必须将这些域也添加到列表中。

管理员可以允许的镜像仓库示例包括：

 - Docker Hub。这是默认启用的。
 - Amazon ECR
 - GitHub Container Registry
 - Google Container Registry
 - GitLab Container Registry
 - Nexus
 - Artifactory

## 先决条件

您必须[强制登录](../enforce-sign-in/_index.md)。为使镜像仓库访问管理生效，Docker Desktop 用户必须向您的组织进行身份验证。强制登录可确保您的 Docker Desktop 开发人员始终向您的组织进行身份验证，即使他们可以在没有强制登录的情况下进行身份验证且功能也会生效。强制登录可保证功能始终生效。

> [!IMPORTANT]
>
> 您必须在镜像仓库访问管理中使用[个人访问令牌（PAT）](/manuals/security/for-developers/access-tokens.md)。组织访问令牌（OAT）不兼容。

## 配置镜像仓库访问管理权限

{{< tabs >}}
{{< tab name="Admin Console" >}}

{{% admin-registry-access product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-registry-access product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 验证限制

新的镜像仓库访问管理策略在开发人员使用其组织凭据成功登录 Docker Desktop 后生效。如果开发人员尝试通过 Docker CLI 从不允许的镜像仓库拉取镜像，他们将收到一条错误消息，表明组织已禁止此镜像仓库。

## 注意事项

使用镜像仓库访问管理时存在某些限制：

- 您最多可以添加 100 个镜像仓库/域。
- Windows 镜像拉取和镜像构建默认不受限制。要使镜像仓库访问管理在 Windows 容器模式下生效，您必须通过选择[为 Windows Docker 守护进程使用代理](/manuals/desktop/settings-and-maintenance/settings.md#proxies)设置来允许 Windows Docker 守护进程使用 Docker Desktop 的内部代理。
- 使用 Kubernetes 驱动程序的 `docker buildx` 等构建不受限制。
- 使用自定义 docker-container 驱动程序的 `docker buildx` 等构建不受限制。
- 阻止是基于 DNS 的。您必须使用镜像仓库的访问控制机制来区分"推送"和"拉取"。
- WSL 2 需要至少 5.4 系列的 Linux 内核（这不适用于更早的 Linux 内核系列）。
- 在 WSL 2 网络下，来自所有 Linux 发行版的流量都受到限制。这将在更新的 5.15 系列 Linux 内核中解决。
- 当启用 Docker Debug 或 Kubernetes 时，Docker Desktop 拉取的镜像默认不受限制，即使 RAM 阻止了 Docker Hub。
- 如果 RAM 限制了 Docker Hub 访问，即使镜像之前已被镜像仓库镜像缓存，对源自 Docker Hub 的镜像的拉取也会受到限制。请参阅[将镜像仓库访问管理（RAM）与镜像仓库镜像一起使用](/manuals/docker-hub/image-library/mirror.md)。

此外，镜像仓库访问管理在主机级别运行，而不是 IP 地址级别。开发人员可以在其域解析中绑过此限制，例如通过针对本地代理运行 Docker 或修改其操作系统的 `sts` 文件。阻止这些形式的操作不在 Docker Desktop 的职责范围内。

## 更多资源

- [视频：强化 Desktop 镜像仓库访问管理](https://www.youtube.com/watch?v=l9Z6WJdJC9A)
