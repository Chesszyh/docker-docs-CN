---
description: 了解如何在 Docker Hub 上管理仓库访问权限。
keywords: Docker Hub, Hub, repository access, repository collaborators, repository privacy
title: 访问管理
LinkTItle: 访问控制
weight: 50
aliases:
- /docker-hub/repos/access/
---

在本主题中，了解管理仓库访问权限的可用功能。这包括可见性、协作者、角色、团队和组织访问令牌。

## 仓库可见性

最基本的仓库访问权限是通过可见性控制的。仓库的可见性可以是公开或私有。

设置为公开可见性时，仓库会出现在 Docker Hub 搜索结果中，任何人都可以拉取。要管理对公开个人仓库的推送访问权限，您可以使用协作者。要管理对公开组织仓库的推送访问权限，您可以使用角色、团队或组织访问令牌。

设置为私有可见性时，仓库不会出现在 Docker Hub 搜索结果中，只有被授予权限的人才能访问。要管理对私有个人仓库的推送和拉取访问权限，您可以使用协作者。要管理对私有组织仓库的推送和拉取访问权限，您可以使用角色、团队或组织访问令牌。

### 更改仓库可见性

在 Docker Hub 中创建仓库时，您可以设置仓库可见性。此外，您可以在个人仓库设置中设置创建仓库时的默认仓库可见性。以下描述如何在仓库创建后更改可见性。

要更改仓库可见性：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 选择一个仓库。

   仓库的 **General** 页面会出现。

4. 选择 **Settings** 标签。
5. 在 **Visibility settings** 下，选择以下选项之一：

   - **Make public**：仓库会出现在 Docker Hub 搜索结果中，任何人都可以拉取。
   - **Make private**：仓库不会出现在 Docker Hub 搜索结果中，只有您和协作者可以访问。此外，如果仓库在组织的命名空间中，则具有适用角色或权限的人可以访问该仓库。

6. 输入仓库名称以验证更改。
7. 选择 **Make public** 或 **Make private**。

## 协作者

协作者是您想要授予个人仓库 `push`（推送）和 `pull`（拉取）访问权限的人。协作者无法执行任何管理任务，如删除仓库或将其可见性从私有更改为公开。此外，协作者无法添加其他协作者。

只有个人仓库可以使用协作者。您可以为公开仓库添加无限数量的协作者，Docker Pro 账户可以为私有仓库添加最多 1 个协作者。

组织仓库不能使用协作者，但可以使用成员角色、团队或组织访问令牌来管理访问权限。

### 管理协作者

1. 登录 [Docker Hub](https://hub.docker.com)。

2. 选择 **My Hub** > **Repositories**。

   您的仓库列表会出现。

3. 选择一个仓库。

   仓库的 **General** 页面会出现。

4. 选择 **Collaborators** 标签。

5. 根据 Docker 用户名添加或删除协作者。

您可以从仓库的 **Settings** 页面选择协作者并管理他们对私有仓库的访问权限。

## 组织角色

组织可以使用角色授予个人不同的组织权限。有关更多详情，请参阅[角色和权限](/manuals/security/for-admins/roles-and-permissions.md)。

## 组织团队

组织可以使用团队。可以为团队分配细粒度的仓库访问权限。

### 配置团队仓库权限

在配置仓库权限之前，您必须先创建团队。有关更多详情，请参阅[创建和管理团队](/manuals/admin/organization/manage-a-team.md)。

要配置团队仓库权限：

1. 登录 [Docker Hub](https://hub.docker.com)。

2. 选择 **My Hub** > **Repositories**。

   您的仓库列表会出现。

3. 选择一个仓库。

   仓库的 **General** 页面会出现。

4. 选择 **Permissions** 标签。

5. 添加、修改或删除团队的仓库权限。

   - 添加：指定 **Team**，选择 **Permission**，然后选择 **Add**。
   - 修改：在团队旁边指定新权限。
   - 删除：选择团队旁边的 **Remove permission** 图标。

## 组织访问令牌（OATs）

组织可以使用 OATs（Organization Access Tokens，组织访问令牌）。OATs 让您可以为令牌分配细粒度的仓库访问权限。有关更多详情，请参阅[组织访问令牌](/manuals/security/for-admins/access-tokens.md)。

## 受控分发

{{< summary-bar feature_name="Gated distribution" >}}

受控分发（Gated distribution）允许发布者安全地与外部客户或合作伙伴共享私有容器镜像，而无需授予他们完整的组织访问权限或对您的团队、协作者或其他仓库的可见性。

此功能非常适合希望控制谁可以拉取特定镜像，同时在内部用户和外部消费者之间保持清晰分离的商业软件发布者。

如果您对受控分发感兴趣，请联系 [Docker 销售团队](https://www.docker.com/pricing/contact-sales/)获取更多信息。

### 主要功能

- **私有仓库分发**：内容存储在私有仓库中，只有被明确邀请的用户才能访问。

- **无需组织成员身份的外部访问**：外部用户无需添加到您的内部组织即可拉取镜像。

- **仅拉取权限**：外部用户只获得拉取权限，无法推送或修改仓库内容。

- **仅邀请访问**：通过经过身份验证的电子邮件邀请授予访问权限，通过 API 进行管理。

### 通过 API 邀请分发者成员

> [!NOTE]
> 当您邀请成员时，您会为他们分配一个角色。请参阅[角色和权限](/manuals/security/for-admins/roles-and-permissions.md)了解每个角色的访问权限详情。

分发者成员（用于受控分发）只能使用 Docker Hub API 邀请。此角色目前不支持基于 UI 的邀请。要邀请分发者成员，请使用批量创建邀请 API 端点。

要邀请分发者成员：

1. 使用[身份验证 API](https://docs.docker.com/reference/api/hub/latest/#tag/authentication-api/operation/AuthCreateAccessToken) 为您的 Docker Hub 账户生成 bearer token。

2. 在 Hub UI 中创建团队或使用[团队 API](https://docs.docker.com/reference/api/hub/latest/#tag/groups/paths/~1v2~1orgs~1%7Borg_name%7D~1groups/post)。

3. 授予团队仓库访问权限：
   - 在 Hub UI 中：导航到您的仓库设置并添加具有"Read-only"权限的团队
   - 使用[仓库团队 API](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1repositories~1%7Bnamespace%7D~1%7Brepository%7D~1groups/post)：将团队分配到具有"read-only"访问级别的仓库

4. 使用[批量创建邀请端点](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post)发送带有分发者成员角色的电子邮件邀请。在请求体中，将"role"字段设置为"distributor_member"。

5. 被邀请的用户将收到一封包含接受邀请链接的电子邮件。使用他们的 Docker ID 登录后，他们将作为分发者成员获得对指定私有仓库的仅拉取访问权限。
