---
title: 管理组织成员
weight: 30
description: 了解如何在 Docker Hub 和 Docker Admin Console 中管理组织成员。
keywords: members, teams, organizations, invite members, manage team members
aliases:
- /docker-hub/members/
---

了解如何在 Docker Hub 和 Docker Admin Console 中管理组织成员。

## 邀请成员

{{< tabs >}}
{{< tab name="Admin Console" >}}

{{% admin-users product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-users product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 接受邀请

当邀请发送到用户的电子邮件地址时，他们会收到一个指向 Docker Hub 的链接，可以在那里接受或拒绝邀请。
要接受邀请：

1. 导航到您的电子邮件收件箱，打开包含加入 Docker 组织邀请的 Docker 电子邮件。
1. 要打开指向 Docker Hub 的链接，请选择 **click here** 链接。

   > [!WARNING]
   >
   > 邀请电子邮件链接在 14 天后过期。如果您的电子邮件链接已过期，您可以使用链接发送到的电子邮件地址登录 [Docker Hub](https://hub.docker.com/)，并从 **Notifications** 面板接受邀请。

1. Docker 创建帐户页面将打开。如果您已有帐户，请选择 **Already have an account? Sign in**。如果您还没有帐户，请使用收到邀请的同一电子邮件地址创建一个帐户。
1. 可选。如果您没有帐户并创建了一个，您必须返回电子邮件收件箱并使用 Docker 验证电子邮件验证您的电子邮件地址。
1. 登录 Docker Hub 后，从顶级导航菜单中选择 **My Hub**。
1. 在您的邀请上选择 **Accept**。

接受邀请后，您现在是组织的成员。

## 管理邀请

邀请成员后，您可以根据需要重新发送或移除邀请。

### 重新发送邀请

{{< tabs >}}
{{< tab name="Admin Console" >}}

您可以从 Admin Console 发送单个邀请或批量邀请。

要重新发送单个邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 选择被邀请者旁边的 **action menu**，然后选择 **Resend**。
1. 选择 **Invite** 确认。

要批量重新发送邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 使用 **Usernames** 旁边的 **checkboxes** 批量选择用户。
1. 选择 **Resend invites**。
1. 选择 **Resend** 确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要从 Docker Hub 重新发送邀请：

1. 登录 [Docker Hub](https://hub.docker.com/)。
1. 选择 **My Hub**、您的组织，然后选择 **Members**。
1. 在表格中，找到被邀请者，选择 **Actions** 图标，然后选择 **Resend invitation**。
1. 选择 **Invite** 确认。

您还可以使用 Docker Hub API 重新发送邀请。有关更多信息，请参阅[重新发送邀请](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1%7Bid%7D~1resend/patch) API 端点。

{{< /tab >}}
{{< /tabs >}}

### 移除邀请

{{< tabs >}}
{{< tab name="Admin Console" >}}

要从 Admin Console 移除邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 选择被邀请者旁边的 **action menu**，然后选择 **Remove invitee**。
1. 选择 **Remove** 确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要从 Docker Hub 移除成员的邀请：

1. 登录 [Docker Hub](https://hub.docker.com/)。
1. 选择 **My Hub**、您的组织，然后选择 **Members**。
1. 在表格中，选择 **Action** 图标，然后选择 **Remove member** 或 **Remove invitee**。
1. 按照屏幕上的说明移除成员或被邀请者。

您还可以使用 Docker Hub API 移除邀请。有关更多信息，请参阅[取消邀请](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1%7Bid%7D/delete) API 端点。

{{< /tab >}}
{{< /tabs >}}

## 管理团队成员

使用 Docker Hub 或 Admin Console 添加或移除团队成员。组织所有者可以将成员添加到组织内的一个或多个团队。

### 将成员添加到团队

{{< tabs >}}
{{< tab name="Admin Console" >}}

要使用 Admin Console 将成员添加到团队：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Teams**。
1. 选择团队名称。
1. 选择 **Add member**。您可以通过搜索成员的电子邮件地址或用户名来添加成员。

   > [!NOTE]
   >
   > 被邀请者必须先接受加入组织的邀请，然后才能被添加到团队。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要使用 Docker Hub 将成员添加到团队：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub**、您的组织，然后选择 **Members**。
1. 选择 **Action** 图标，然后选择 **Add to team**。

   > [!NOTE]
   >
   > 您还可以导航到 **My Hub** > **Your Organization** > **Teams** > **Your Team Name** 并选择 **Add Member**。从下拉列表中选择一个成员以将其添加到团队，或通过 Docker ID 或电子邮件搜索。
1. 选择团队，然后选择 **Add**。

   > [!NOTE]
   >
   > 被邀请者必须先接受加入组织的邀请，然后才能被添加到团队。

{{< /tab >}}
{{< /tabs >}}

### 从团队中移除成员

> [!NOTE]
>
> 如果您的组织使用启用了 [SCIM](/manuals/security/for-admins/provisioning/scim.md) 的单点登录（SSO），您应该从身份提供商（IdP）中移除成员。这将自动从 Docker 中移除成员。如果禁用了 SCIM，您必须在 Docker 中手动管理成员。

组织所有者可以在 Docker Hub 或 Admin Console 中从团队中移除成员。从团队中移除成员将撤销其对允许资源的访问权限。

{{< tabs >}}
{{< tab name="Admin Console" >}}

要使用 Admin Console 从特定团队中移除成员：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Teams**。
1. 选择团队名称。
1. 选择用户名旁边的 **X** 以将其从团队中移除。
1. 出现提示时，选择 **Remove** 确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要使用 Docker Hub 从特定团队中移除成员：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub**、您的组织、**Teams**，然后选择团队。
1. 选择用户名旁边的 **X** 以将其从团队中移除。
1. 出现提示时，选择 **Remove** 确认。

{{< /tab >}}
{{< /tabs >}}

### 更新成员角色

组织所有者可以管理组织内的[角色](/security/for-admins/roles-and-permissions/)。如果组织是公司的一部分，公司所有者也可以管理该组织的角色。如果您启用了 SSO，您可以使用 [SCIM 进行角色映射](/security/for-admins/provisioning/scim/)。

{{< tabs >}}
{{< tab name="Admin Console" >}}

要在 Admin Console 中更新成员角色：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 找到您要编辑角色的成员的用户名。选择 **Actions** 菜单，然后选择 **Edit role**。

> [!NOTE]
>
> 如果您是组织的唯一所有者，您需要先分配新所有者，然后才能编辑您的角色。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要在 Docker Hub 中更新成员角色：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub**、您的组织，然后选择 **Members**。
1. 找到您要编辑角色的成员的用户名。在表格中，选择 **Actions** 图标。
1. 选择 **Edit role**。
1. 选择其组织，选择您要分配的角色，然后选择 **Save**。

> [!NOTE]
>
> 如果您是组织的唯一所有者，您需要先分配新所有者，然后才能编辑您的角色。

{{< /tab >}}
{{< /tabs >}}

## 导出成员 CSV 文件

{{< summary-bar feature_name="Admin orgs" >}}

所有者可以导出包含所有成员的 CSV 文件。公司的 CSV 文件包含以下字段：

- Name：用户姓名
- Username：用户的 Docker ID
- Email：用户的电子邮件地址
- Member of Organizations：用户在公司内所属的所有组织
- Invited to Organizations：用户在公司内被邀请的所有组织
- Account Created：用户帐户创建的时间和日期

{{< tabs >}}
{{< tab name="Admin Console" >}}

要导出成员的 CSV 文件：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 选择 **download** 图标以导出所有成员的 CSV 文件。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要导出成员的 CSV 文件：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub**、您的组织，然后选择 **Members**。
1. 选择 **Action** 图标，然后选择 **Export users as CSV**。

{{< /tab >}}
{{< /tabs >}}
