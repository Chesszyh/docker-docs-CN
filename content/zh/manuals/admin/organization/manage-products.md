---
title: 管理 Docker 产品
weight: 45
description: 了解如何为您的组织管理 Docker 产品
keywords: 组织, 工具, 产品
---

{{< summary-bar feature_name="管理员组织" >}}

在本节中，了解如何管理对 Docker 产品的访问和查看其使用情况。有关每个产品的更详细信息，包括如何设置和配置它们，请参阅以下手册：

- [Docker Build Cloud](../../build-cloud/_index.md)
- [Docker Desktop](../../desktop/_index.md)
- [Docker Hub](../../docker-hub/_index.md)
- [Docker Scout](../../scout/_index.md)
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started)

## 管理对 Docker 产品的访问

您的订阅中包含的 Docker 产品默认对所有用户启用。包含的产品有：

- Docker Hub
- Docker Build Cloud
- Docker Desktop
- Docker Scout

Testcontainers Cloud 默认不启用。要启用 Testcontainers Cloud，请参阅 Testcontainers [入门](https://testcontainers.com/cloud/docs/#getting-started) 指南。

以下部分介绍如何启用或禁用对这些产品的访问。

### 管理对 Docker Build Cloud 的访问

要了解如何初步设置和配置 Docker Build Cloud，请登录 [Docker Build Cloud 控制台](https://app.docker.com/build) 并按照屏幕上的说明进行操作。

要管理对 Docker Build Cloud 的访问，请以组织所有者身份登录 [Docker Build Cloud](http://app.docker.com/build)，选择**帐户设置**，然后在**锁定 Docker Build Cloud** 下管理访问权限。

### 管理对 Docker Scout 的访问

要了解如何初步设置和配置 Docker Scout 以用于远程仓库，请登录 [Docker Scout 控制台](https://scout.docker.com/) 并按照屏幕上的说明进行操作。

要管理对 Docker Scout 的访问以用于 Docker Desktop 的本地镜像，请使用[设置管理](../../security/for-admins/hardened-desktop/settings-management/_index.md)并将 `sbomIndexing` 设置为 `false` 以禁用，或设置为 `true` 以启用。

### 管理对 Docker Hub 的访问

要管理对 Docker Hub 的访问，请登录 [Docker 管理控制台](https://app.docker.com/admin) 并配置[注册表访问管理](../../security/for-admins/hardened-desktop/registry-access-management.md)或[镜像访问管理](../../security/for-admins/hardened-desktop/image-access-management.md)。

### 管理对 Testcontainers Cloud 的访问

要了解如何初步设置和配置 Testcontainers Cloud，请登录 [Testcontainers Cloud](https://app.testcontainers.cloud/) 并按照屏幕上的说明进行操作。

要管理对 Testcontainers Cloud 的访问，请以组织所有者身份登录 [Testcontainers Cloud 设置页面](https://app.testcontainers.cloud/dashboard/settings)，然后在**锁定 Testcontainers Cloud** 下管理访问权限。

### 管理对 Docker Desktop 的访问

要管理对 Docker Desktop 的访问，您可以[强制登录](../../security/for-admins/enforce-sign-in/_index.md)，然后[手动](./members.md)管理成员或使用[配置](../../security/for-admins/provisioning/_index.md)。强制登录后，只有作为组织成员的用户才能在登录后使用 Docker Desktop。

## 查看 Docker 产品使用情况

在以下页面查看产品使用情况：

- Docker Build Cloud：在 [Docker Build Cloud 控制台](http://app.docker.com/build) 中查看**构建分钟数**页面。

- Docker Scout：在 Docker Scout 控制台中查看[**仓库设置**页面](https://scout.docker.com/settings/repos)。

- Docker Hub：在 Docker Hub 中查看[**使用情况**页面](https://hub.docker.com/usage)。

- Testcontainers Cloud：在 Testcontainers Cloud 控制台中查看[**账单**页面](https://app.testcontainers.cloud/dashboard/billing)。

- Docker Desktop：在 [Docker 主页](https://app.docker.com/) 中查看**洞察力**页面。有关更多详细信息，请参阅[洞察力](./insights.md)。

如果您的使用量超过您的订阅金额，您可以[扩展您的订阅](../../subscription/scale.md)以满足您的需求。