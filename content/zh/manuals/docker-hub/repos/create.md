---
description: 了解如何在 Docker Hub 上创建仓库
keywords: Docker Hub, Hub, repositories, create
title: 创建仓库
linkTitle: 创建
toc_max: 3
weight: 20
---

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 在右上角附近，选择 **Create repository**。
4. 选择一个 **Namespace**（命名空间）。

   您可以选择将其放在您自己的用户账户下，或者放在您是所有者或编辑者的任何组织下。

5. 指定 **Repository Name**（仓库名称）。

   仓库名称需要：
    - 唯一
    - 在 2 到 255 个字符之间
    - 仅包含小写字母、数字、连字符（`-`）和下划线（`_`）

   > [!NOTE]
   >
   > 一旦创建，您就无法重命名 Docker Hub 仓库。

6. 指定 **Short description**（简短描述）。

   描述最多可以有 100 个字符。它会出现在搜索结果中。

7. 选择默认可见性。

   - **Public**（公开）：仓库会出现在 Docker Hub 搜索结果中，任何人都可以拉取。
   - **Private**（私有）：仓库不会出现在 Docker Hub 搜索结果中，只有您和协作者可以访问。此外，如果您选择了组织的命名空间，则具有适用角色或权限的人可以访问该仓库。有关更多详情，请参阅[角色和权限](../../security/for-admins/roles-and-permissions.md)。

   > [!NOTE]
   >
   > 对于创建新仓库的组织，如果您不确定选择哪种可见性，Docker 建议您选择 **Private**。

8. 选择 **Create**。

仓库创建后，**General** 页面会出现。您现在可以管理：

- [仓库信息](./manage/information.md)
- [访问控制](./manage/access.md)
- [镜像](./manage/hub-images/_index.md)
- [自动构建](./manage/builds/_index.md)
- [Webhooks](./manage/webhooks.md)
- [镜像安全洞察](./manage/vulnerability-scanning.md)
