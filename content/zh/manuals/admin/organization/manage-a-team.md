---
title: 创建并管理团队
weight: 40
description: 了解如何为您的组织创建并管理团队
keywords: Docker, docker, registry, 团队, 组织, 计划, Dockerfile, Docker Hub, 文档, 存储库权限
aliases:
- /docker-hub/manage-a-team/
---

{{< summary-bar feature_name="管理组织" >}}

您可以在 Docker Hub 和 Docker 管理控制台（Admin Console）中为您的组织创建团队。您可以在 Docker Hub 中 [为团队配置存储库访问权限](#configure-repository-permissions-for-a-team)。

团队是属于某个组织的一组 Docker 用户。一个组织可以拥有多个团队。组织所有者可以使用 Docker ID 或电子邮件地址，并通过选择用户应所属的团队，来创建新团队或将成员添加到现有团队中。成员不一定非要属于某个团队才能与组织关联。

组织所有者可以通过分配所有者（owner）角色来添加额外的组织所有者，以协助管理组织中的用户、团队和存储库。

## 组织所有者

组织所有者是拥有以下权限的管理员：

- 管理存储库并向组织添加团队成员。
- 访问私有存储库、所有团队、账单信息和组织设置。
- 为组织中的每个团队指定 [权限](#permissions-reference)。
- 为组织启用 [SSO](../../security/for-admins/single-sign-on/_index.md)。

当为您的组织启用 SSO 时，组织所有者还可以管理用户。Docker 可以通过 SSO 强制执行，为新的最终用户或希望拥有单独公司用途 Docker ID 的用户自动配置 Docker ID。

组织所有者还可以添加额外的组织所有者，以协助管理组织中的用户、团队和存储库。

## 创建团队

{{< tabs >}}
{{< tab name="管理控制台" >}}

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
2. 选择 **Teams**（团队）。
3. 选择 **Create team**（创建团队）。
4. 填写您的团队信息并选择 **Create**（创建）。
5. [向您的团队添加成员](members.md#add-a-member-to-a-team)。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** 并选择您的组织。
3. 选择 **Teams**（团队），然后选择 **Create Team**（创建团队）。
4. 填写您的团队信息并选择 **Create**（创建）。
5. [向您的团队添加成员](members.md#add-a-member-to-a-team)。

{{< /tab >}}
{{< /tabs >}}

## 为团队配置存储库权限

组织所有者可以按团队配置存储库权限。例如，您可以指定组织内的所有团队对存储库 A 和 B 具有“读写（Read and Write）”访问权限，而只有特定团队具有“管理（Admin）”访问权限。请注意，组织所有者对组织内的所有存储库拥有完全的管理访问权限。

赋予团队对存储库的访问权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** 并选择您的组织。
3. 选择 **Teams**（团队），然后选择您想要配置存储库访问权限的团队。
4. 选择 **Permissions**（权限）选项卡，并从 **Repository**（存储库）下拉菜单中选择一个存储库。
5. 从 **Permissions**（权限）下拉列表中选择一项权限，然后选择 **Add**（添加）。

组织所有者还可以为成员分配编辑者（editor）角色以授予部分管理访问权限。有关编辑者角色的更多信息，请参阅 [角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 权限参考

- `Read-only`（只读）访问权限允许用户查看、搜索和拉取私有存储库，方式与公共存储库相同。
- `Read & Write`（读写）访问权限允许用户拉取、推送和查看存储库。此外，它还允许用户查看、取消、重试或触发构建。
- `Admin`（管理）访问权限允许用户拉取、推送、查看、编辑和删除存储库。您还可以编辑构建设置，更新存储库描述、协作者权限、公共/私有可见性以及删除操作。

权限是累积的。例如，如果您拥有“读写”权限，您将自动拥有“只读”权限：

| 操作 | 只读 (Read-only) | 读写 (Read & Write) | 管理 (Admin) |
|:------------------:|:---------:|:------------:|:-----:|
| 拉取存储库 | ✅ | ✅ | ✅ |
| 查看存储库 | ✅ | ✅ | ✅ |
| 推送存储库 | ❌ | ✅ | ✅ |
| 编辑存储库 | ❌ | ❌ | ✅ |
| 删除存储库 | ❌ | ❌ | ✅ |
| 更新存储库描述 | ❌ | ❌ | ✅ |
| 查看构建 | ✅ | ✅ | ✅ |
| 取消构建 | ❌ | ✅ | ✅ |
| 重试构建 | ❌ | ✅ | ✅ |
| 触发构建 | ❌ | ✅ | ✅ |
| 编辑构建设置 | ❌ | ❌ | ✅ |

> [!NOTE]
>
> 尚未验证电子邮件地址的用户对存储库仅拥有 `Read-only`（只读）访问权限，无论其团队成员身份赋予了他们何种权利。

## 查看团队对所有存储库的权限

查看团队在所有存储库中的权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** 并选择您的组织。
3. 选择 **Teams**（团队）并选择您的团队名称。
4. 选择 **Permissions**（权限）选项卡，您可以在此处查看该团队可以访问的存储库。

## 删除团队

组织所有者可以在 Docker Hub 或管理控制台（Admin Console）中删除团队。当您从组织中移除团队时，此操作会撤销成员对团队允许资源的访问权限。它不会将用户从他们所属的其他团队中移除，也不会删除任何资源。

{{< tabs >}}
{{< tab name="管理控制台" >}}

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Teams**（团队）。
3. 选择您想要删除的团队名称旁边的 **Actions**（操作）图标。
4. 选择 **Delete team**（删除团队）。
5. 查看确认消息，然后选择 **Delete**（删除）。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** 并选择您的组织。
3. 选择 **Teams**（团队）。
4. 选择您想要删除的团队名称。
5. 选择 **Settings**（设置）。
6. 选择 **Delete Team**（删除团队）。
7. 查看确认消息，然后选择 **Delete**（删除）。

{{< /tab >}}
{{< /tabs >}}

## 更多资源

- [视频：Docker 团队](https://youtu.be/WKlT1O-4Du8?feature=shared&t=348)
- [视频：角色、团队和存储库](https://youtu.be/WKlT1O-4Du8?feature=shared&t=435)
