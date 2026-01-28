---
description: 了解 Docker Hub 中的仓库个人设置
keywords: Docker Hub, Hub, repositories, settings
title: 仓库的个人设置
linkTitle: 个人设置
toc_max: 3
weight: 50
---

对于您的账户，您可以设置仓库的个人设置，包括默认仓库隐私和自动构建通知。

## 默认仓库隐私

在 Docker Hub 中创建新仓库时，您可以指定仓库可见性。您也可以随时在 Docker Hub 中更改可见性。

当您使用 `docker push` 命令推送到尚不存在的仓库时，默认设置非常有用。在这种情况下，Docker Hub 会使用您的默认仓库隐私设置自动创建仓库。

### 配置默认仓库隐私

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Settings** > **Default privacy**。
3. 为任何新创建的仓库选择 **Default privacy**（默认隐私）。

   - **Public**（公开）：所有新仓库都会出现在 Docker Hub 搜索结果中，任何人都可以拉取。
   - **Private**（私有）：所有新仓库不会出现在 Docker Hub 搜索结果中，只有您和协作者可以访问。此外，如果仓库是在组织的命名空间中创建的，则具有适用角色或权限的人可以访问该仓库。

4. 选择 **Save**。

## 自动构建通知

您可以为所有使用自动构建的仓库发送通知到您的电子邮件。

### 配置自动构建通知

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories** > **Settings** > **Notifications**。
3. 选择要通过电子邮件接收的通知。

   - **Off**（关闭）：无通知。
   - **Only failures**（仅失败）：仅通知构建失败。
   - **Everything**（全部）：通知成功和失败的构建。

4. 选择 **Save**。
