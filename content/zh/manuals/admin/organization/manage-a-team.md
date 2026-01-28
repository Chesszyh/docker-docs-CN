---
title: 创建和管理团队
weight: 40
description: 了解如何为您的组织创建和管理团队
keywords: Docker, docker, registry, teams, organizations, plans, Dockerfile, Docker
  Hub, docs, documentation, repository permissions
aliases:
- /docker-hub/manage-a-team/
---

{{< summary-bar feature_name="Admin orgs" >}}

您可以在 Docker Hub 和 Docker Admin Console 中为您的组织创建团队。您可以在 Docker Hub 中[为团队配置仓库访问权限](#为团队配置仓库权限)。

团队是属于组织的一组 Docker 用户。一个组织可以有多个团队。组织所有者可以创建新团队，并使用成员的 Docker ID 或电子邮件地址将成员添加到现有团队，并选择用户应加入的团队。成员不需要是团队的一部分才能与组织关联。

组织所有者可以通过分配所有者角色来添加额外的组织所有者，以帮助他们管理组织中的用户、团队和仓库。

## 组织所有者

组织所有者是具有以下权限的管理员：

- 管理仓库并将团队成员添加到组织。
- 访问私有仓库、所有团队、账单信息和组织设置。
- 为组织中的每个团队指定[权限](#权限参考)。
- 为组织启用 [SSO](../../security/for-admins/single-sign-on/_index.md)。

当为您的组织启用 SSO 时，组织所有者还可以管理用户。Docker 可以通过 SSO 强制为新最终用户或希望拥有单独 Docker ID 用于公司使用的用户自动配置 Docker ID。

组织所有者还可以添加额外的组织所有者来帮助他们管理组织中的用户、团队和仓库。

## 创建团队

{{< tabs >}}
{{< tab name="Admin Console" >}}

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Teams**。
1. 选择 **Create team**。
1. 填写团队信息并选择 **Create**。
1. [将成员添加到您的团队](members.md#将成员添加到团队)。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub** 并选择您的组织。
1. 选择 **Teams**，然后选择 **Create Team**。
1. 填写团队信息并选择 **Create**。
1. [将成员添加到您的团队](members.md#将成员添加到团队)。

{{< /tab >}}
{{< /tabs >}}

## 为团队配置仓库权限

组织所有者可以按团队配置仓库权限。例如，您可以指定组织内的所有团队对仓库 A 和 B 具有"读写"访问权限，而只有特定团队具有"管理员"访问权限。请注意，组织所有者对组织内的所有仓库具有完全管理访问权限。

要授予团队对仓库的访问权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub** 并选择您的组织。
1. 选择 **Teams** 并选择您想要配置仓库访问权限的团队。
1. 选择 **Permissions** 选项卡，然后从 **Repository** 下拉列表中选择一个仓库。
1. 从 **Permissions** 下拉列表中选择权限，然后选择 **Add**。

组织所有者还可以分配成员编辑者角色以授予部分管理访问权限。有关编辑者角色的更多信息，请参阅[角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 权限参考

- `Read-only` 访问权限允许用户以与公共仓库相同的方式查看、搜索和拉取私有仓库。
- `Read & Write` 访问权限允许用户拉取、推送和查看仓库。此外，还允许用户查看、取消、重试或触发构建。
- `Admin` 访问权限允许用户拉取、推送、查看、编辑和删除仓库。您还可以编辑构建设置，以及更新仓库描述、协作者权限、公共/私有可见性和删除。

权限是累积的。例如，如果您有"读写"权限，您将自动拥有"只读"权限：

| 操作 | Read-only | Read & Write | Admin |
|:------------------:|:---------:|:------------:|:-----:|
| 拉取仓库 | ✅ | ✅ | ✅ |
| 查看仓库 | ✅ | ✅ | ✅ |
| 推送仓库 | ❌ | ✅ | ✅ |
| 编辑仓库 | ❌ | ❌ | ✅ |
| 删除仓库 | ❌ | ❌ | ✅ |
| 更新仓库描述 | ❌ | ❌ | ✅ |
| 查看构建 | ✅ | ✅ | ✅ |
| 取消构建 | ❌ | ✅ | ✅ |
| 重试构建 | ❌ | ✅ | ✅ |
| 触发构建 | ❌ | ✅ | ✅ |
| 编辑构建设置 | ❌ | ❌ | ✅ |

> [!NOTE]
>
> 未验证电子邮件地址的用户只有对仓库的 `Read-only` 访问权限，无论其团队成员身份授予他们什么权限。

## 查看团队对所有仓库的权限

要查看团队对所有仓库的权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub** 并选择您的组织。
1. 选择 **Teams** 并选择您的团队名称。
1. 选择 **Permissions** 选项卡，您可以在其中查看此团队可以访问的仓库。

## 删除团队

组织所有者可以在 Docker Hub 或 Admin Console 中删除团队。当您从组织中移除团队时，此操作会撤销成员对团队允许资源的访问权限。它不会将用户从他们所属的其他团队中移除，也不会删除任何资源。

{{< tabs >}}
{{< tab name="Admin Console" >}}

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Teams**。
1. 选择要删除的团队名称旁边的 **Actions** 图标。
1. 选择 **Delete team**。
1. 查看确认消息，然后选择 **Delete**。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub** 并选择您的组织。
1. 选择 **Teams**。
1. 选择您要删除的团队的名称。
1. 选择 **Settings**。
1. 选择 **Delete Team**。
1. 查看确认消息，然后选择 **Delete**。

{{< /tab >}}
{{< /tabs >}}

## 更多资源

- [视频：Docker 团队](https://youtu.be/WKlT1O-4Du8?feature=shared&t=348)
- [视频：角色、团队和仓库](https://youtu.be/WKlT1O-4Du8?feature=shared&t=435)
