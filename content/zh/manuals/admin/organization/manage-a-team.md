---
title: 创建和管理团队
weight: 40
description: 了解如何为您的组织创建和管理团队
keywords: Docker, docker, 注册表, 团队, 组织, 计划, Dockerfile, Docker Hub, 文档, 文档, 仓库权限
aliases:
- /docker-hub/manage-a-team/
---

{{< summary-bar feature_name="管理员组织" >}}

您可以在 Docker Hub 和 Docker 管理控制台中为您的组织创建团队。您可以在 Docker Hub 中[为团队配置仓库访问权限](#configure-repository-permissions-for-a-team)。

团队是属于组织的 Docker 用户组。一个组织可以有多个团队。组织所有者可以创建新团队，并使用他们的 Docker ID 或电子邮件地址将成员添加到现有团队，并通过选择用户应属于的团队。成员不需要成为团队的一部分才能与组织关联。

组织所有者可以通过分配所有者角色来添加其他组织所有者，以帮助他们管理组织中的用户、团队和仓库。

## 组织所有者

组织所有者是具有以下权限的管理员：

- 管理仓库并将团队成员添加到组织。
- 访问私有仓库、所有团队、账单信息和组织设置。
- 为组织中的每个团队指定[权限](#permissions-reference)。
- 为组织启用 [SSO](../../security/for-admins/single-sign-on/_index.md)。

当为您的组织启用 SSO 时，组织所有者还可以管理用户。Docker 可以通过 SSO 强制执行为新最终用户或希望拥有单独 Docker ID 以供公司使用的用户自动配置 Docker ID。

组织所有者还可以添加其他组织所有者，以帮助他们管理组织中的用户、团队和仓库。

## 创建团队

{{< tabs >}}
{{< tab name="管理员控制台" >}}

1. 登录 [Docker 主页](https://app.docker.com) 并选择您的组织。
1. 选择**团队**。
1. 选择**创建团队**。
1. 填写您的团队信息并选择**创建**。
1. [将成员添加到您的团队](members.md#add-a-member-to-a-team)。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub** 并选择您的组织。
1. 选择**团队**，然后选择**创建团队**。
1. 填写您的团队信息并选择**创建**。
1. [将成员添加到您的团队](members.md#add-a-member-to-a-team)。

{{< /tab >}}
{{< /tabs >}}

## 为团队配置仓库权限

组织所有者可以按团队配置仓库权限。例如，您可以指定组织内的所有团队对仓库 A 和 B 具有“读写”访问权限，而只有特定团队具有“管理员”访问权限。请注意，组织所有者对组织内的所有仓库具有完全管理访问权限。

要授予团队访问仓库的权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub** 并选择您的组织。
1. 选择**团队**并选择您要配置仓库访问权限的团队。
1. 选择**权限**选项卡，然后从**仓库**下拉列表中选择一个仓库。
1. 从**权限**下拉列表中选择一个权限并选择**添加**。

组织所有者还可以为成员分配编辑者角色，以授予部分管理访问权限。有关编辑者角色的更多信息，请参阅[角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 权限参考

- `只读` 访问权限允许用户以与公共仓库相同的方式查看、搜索和拉取私有仓库。
- `读写` 访问权限允许用户拉取、推送和查看仓库。此外，它还允许用户查看、取消、重试或触发构建。
- `管理员` 访问权限允许用户拉取、推送、查看、编辑和删除仓库。您还可以编辑构建设置，并更新仓库描述、协作者权限、公共/私有可见性以及删除。

权限是累积的。例如，如果您拥有“读写”权限，则您自动拥有“只读”权限：

| 操作 | 只读 | 读写 | 管理员 |
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
> 未验证电子邮件地址的用户仅对仓库具有 `只读` 访问权限，无论其团队成员资格授予他们何种权限。

## 查看团队对所有仓库的权限

要查看团队对所有仓库的权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub** 并选择您的组织。
1. 选择**团队**并选择您的团队名称。
1. 选择**权限**选项卡，您可以在其中查看此团队可以访问的仓库。

## 删除团队

组织所有者可以在 Docker Hub 或管理控制台中删除团队。当您从组织中删除团队时，此操作会撤销成员对团队允许资源的访问权限。它不会将用户从他们所属的其他团队中删除，也不会删除任何资源。

{{< tabs >}}
{{< tab name="管理员控制台" >}}

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**团队**。
1. 选择要删除的团队名称旁边的**操作**图标。
1. 选择**删除团队**。
1. 查看确认消息，然后选择**删除**。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub** 并选择您的组织。
1. 选择**团队**。
1. 选择要删除的团队名称。
1. 选择**设置**。
1. 选择**删除团队**。
1. 查看确认消息，然后选择**删除**。

{{< /tab >}}
{{< /tabs >}}

## 更多资源

- [视频：Docker 团队](https://youtu.be/WKlT1O-4Du8?feature=shared&t=348)
- [视频：角色、团队和仓库](https://youtu.be/WKlT1O-4Du8?feature=shared&t=435)