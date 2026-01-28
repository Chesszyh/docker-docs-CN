---
title: 管理 Docker 产品
weight: 45
description: 了解如何为您的组织管理 Docker 产品
keywords: organization, tools, products
---

{{< summary-bar feature_name="Admin orgs" >}}

在本节中，了解如何管理组织的 Docker 产品访问权限和查看使用情况。有关每个产品的更详细信息，包括如何设置和配置它们，请参阅以下手册：

- [Docker Build Cloud](../../build-cloud/_index.md)
- [Docker Desktop](../../desktop/_index.md)
- [Docker Hub](../../docker-hub/_index.md)
- [Docker Scout](../../scout/_index.md)
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started)

## 管理 Docker 产品访问权限

订阅中包含的 Docker 产品的访问权限默认为所有用户启用。包含的产品有：

- Docker Hub
- Docker Build Cloud
- Docker Desktop
- Docker Scout

Testcontainers Cloud 默认未启用。要启用 Testcontainers Cloud，请参阅 Testcontainers [入门指南](https://testcontainers.com/cloud/docs/#getting-started)。

以下章节介绍如何启用或禁用这些产品的访问权限。

### 管理 Docker Build Cloud 访问权限

要了解如何初始设置和配置 Docker Build Cloud，请登录 [Docker Build Cloud Dashboard](https://app.docker.com/build) 并按照屏幕上的说明操作。

要管理 Docker Build Cloud 的访问权限，请以组织所有者身份登录 [Docker Build Cloud](http://app.docker.com/build)，选择 **Account settings**，然后在 **Lock Docker Build Cloud** 下管理访问权限。

### 管理 Docker Scout 访问权限

要了解如何初始设置和配置 Docker Scout 用于远程仓库，请登录 [Docker Scout Dashboard](https://scout.docker.com/) 并按照屏幕上的说明操作。

要管理 Docker Scout 用于远程仓库的访问权限，请登录 [Docker Scout Dashboard](https://scout.docker.com/) 并配置[集成](../../scout/explore/dashboard.md#integrations)和[仓库设置](../../scout/explore/dashboard.md#repository-settings)。

要管理 Docker Scout 在 Docker Desktop 中用于本地镜像的访问权限，请使用[设置管理](../../security/for-admins/hardened-desktop/settings-management/_index.md)并将 `sbomIndexing` 设置为 `false` 以禁用，或设置为 `true` 以启用。

### 管理 Docker Hub 访问权限

要管理 Docker Hub 的访问权限，请登录 [Docker Admin Console](https://app.docker.com/admin) 并配置[注册表访问管理](../../security/for-admins/hardened-desktop/registry-access-management.md)或[镜像访问管理](../../security/for-admins/hardened-desktop/image-access-management.md)。

### 管理 Testcontainers Cloud 访问权限

要了解如何初始设置和配置 Testcontainers Cloud，请登录 [Testcontainers Cloud](https://app.testcontainers.cloud/) 并按照屏幕上的说明操作。

要管理 Testcontainers Cloud 的访问权限，请以组织所有者身份登录 [Testcontainers Cloud 设置页面](https://app.testcontainers.cloud/dashboard/settings)，然后在 **Lock Testcontainers Cloud** 下管理访问权限。

### 管理 Docker Desktop 访问权限

要管理 Docker Desktop 的访问权限，您可以[强制登录](../../security/for-admins/enforce-sign-in/_index.md)，然后[手动](./members.md)管理成员或使用[配置](../../security/for-admins/provisioning/_index.md)。强制登录后，只有您组织的成员才能在登录后使用 Docker Desktop。

## 查看 Docker 产品使用情况

在以下页面查看产品使用情况：

- Docker Build Cloud：在 [Docker Build Cloud Dashboard](http://app.docker.com/build) 中查看 **Build minutes** 页面。

- Docker Scout：在 Docker Scout Dashboard 中查看 [**Repository settings** 页面](https://scout.docker.com/settings/repos)。

- Docker Hub：在 Docker Hub 中查看 [**Usage** 页面](https://hub.docker.com/usage)。

- Testcontainers Cloud：在 Testcontainers Cloud Dashboard 中查看 [**Billing** 页面](https://app.testcontainers.cloud/dashboard/billing)。

- Docker Desktop：在 [Docker Home](https://app.docker.com/) 中查看 **Insights** 页面。有关更多详细信息，请参阅[洞察](./insights.md)。

如果您的使用量超过订阅额度，您可以[扩展您的订阅](../../subscription/scale.md)以满足您的需求。
