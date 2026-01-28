---
title: 管理组织成员
weight: 30
description: 了解如何在 Docker Hub 和 Docker 管理控制台中管理组织成员。
keywords: 成员, 团队, 组织, 邀请成员, 管理团队成员
aliases:
- /docker-hub/members/
---

学习如何在 Docker Hub 和 Docker 管理控制台（Admin Console）中管理您的组织成员。

## 邀请成员

{{< tabs >}}
{{< tab name="管理控制台" >}}

{{% admin-users product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-users product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 接受邀请

当邀请发送到用户的电子邮件地址时，他们会收到一个指向 Docker Hub 的链接，可以在其中接受或拒绝邀请。接受邀请的步骤如下：

1. 导航到您的电子邮件收件箱，打开包含加入 Docker 组织邀请的 Docker 邮件。
2. 选择 **click here**（点击此处）链接以打开 Docker Hub 的链接。

   > [!WARNING]
   >
   > 邀请邮件链接在 14 天后过期。如果您的邮件链接已过期，您可以使用接收链接的电子邮件地址登录 [Docker Hub](https://hub.docker.com/)，并从 **Notifications**（通知）面板中接受邀请。

3. 随后将打开 Docker 创建账户页面。如果您已有账户，请选择 **Already have an account? Sign in**（已有账户？登录）。如果您还没有账户，请使用接收邀请时所用的同一电子邮件地址创建一个账户。
4. 可选：如果您没有账户并创建了一个账户，您必须返回电子邮件收件箱并使用 Docker 发送的验证邮件验证您的电子邮件地址。
5. 登录 Docker Hub 后，从顶级导航菜单中选择 **My Hub**。
6. 在您的邀请上选择 **Accept**（接受）。

接受邀请后，您即成为该组织的成员。

## 管理邀请

邀请成员后，您可以根据需要重新发送或删除邀请。

### 重新发送邀请

{{< tabs >}}
{{< tab name="管理控制台" >}}

您可以在管理控制台中发送单个邀请或批量发送邀请。

重新发送单个邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Members**（成员）。
3. 选择受邀者旁边的 **操作菜单**（action menu），然后选择 **Resend**（重新发送）。
4. 选择 **Invite**（邀请）以进行确认。

批量重新发送邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Members**（成员）。
3. 使用 **Usernames**（用户名）旁边的 **复选框** 批量选择用户。
4. 选择 **Resend invites**（重新发送邀请）。
5. 选择 **Resend**（重新发送）以进行确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

从 Docker Hub 重新发送邀请：

1. 登录 [Docker Hub](https://hub.docker.com/)。
2. 选择 **My Hub**、您的组织，然后选择 **Members**（成员）。
3. 在表格中找到受邀者，选择 **Actions**（操作）图标，然后选择 **Resend invitation**（重新发送邀请）。
4. 选择 **Invite**（邀请）以进行确认。

您还可以使用 Docker Hub API 重新发送邀请。有关更多信息，请参阅 [Resend an invite](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1%7Bid%7D~1resend/patch) API 端点。

{{< /tab >}}
{{< /tabs >}}

### 删除邀请

{{< tabs >}}
{{< tab name="管理控制台" >}}

从管理控制台删除邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Members**（成员）。
3. 选择受邀者旁边的 **操作菜单**，然后选择 **Remove invitee**（移除受邀者）。
4. 选择 **Remove**（移除）以进行确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

从 Docker Hub 删除成员的邀请：

1. 登录 [Docker Hub](https://hub.docker.com/)。
2. 选择 **My Hub**、您的组织，然后选择 **Members**（成员）。
3. 在表格中选择 **Action**（操作）图标，然后选择 **Remove member**（移除成员）或 **Remove invitee**（移除受邀者）。
4. 按照屏幕上的说明移除成员或受邀者。

您还可以使用 Docker Hub API 删除邀请。有关更多信息，请参阅 [Cancel an invite](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1%7Bid%7D/delete) API 端点。

{{< /tab >}}
{{< /tabs >}}

## 管理团队成员

使用 Docker Hub 或管理控制台（Admin Console）添加或移除团队成员。组织所有者可以将成员添加到组织内的一个或多个团队中。

### 向团队添加成员

{{< tabs >}}
{{< tab name="管理控制台" >}}

使用管理控制台向团队添加成员：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Teams**（团队）。
3. 选择团队名称。
4. 选择 **Add member**（添加成员）。您可以通过搜索其电子邮件地址或用户名来添加成员。

   > [!NOTE]
   >
   > 受邀者必须先接受加入组织的邀请，然后才能被添加到团队中。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

使用 Docker Hub 向团队添加成员：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**、您的组织，然后选择 **Members**（成员）。
3. 选择 **Action**（操作）图标，然后选择 **Add to team**（添加到团队）。

   > [!NOTE]
   >
   > 您还可以导航到 **My Hub** > **您的组织** > **Teams** > **您的团队名称**，然后选择 **Add Member**。从下拉列表中选择一名成员以将其添加到团队中，或者按 Docker ID 或电子邮件进行搜索。
4. 选择团队，然后选择 **Add**（添加）。

   > [!NOTE]
   >
   > 受邀者必须先接受加入组织的邀请，然后才能被添加到团队中。

{{< /tab >}}
{{< /tabs >}}

### 从团队中移除成员

> [!NOTE]
>
> 如果您的组织使用启用了 [SCIM](/manuals/security/for-admins/provisioning/scim.md) 的单点登录 (SSO)，您应该从身份提供商 (IdP) 中移除成员。这将自动从 Docker 中移除成员。如果禁用了 SCIM，您必须在 Docker 中手动管理成员。

组织所有者可以在 Docker Hub 或管理控制台（Admin Console）中从团队中移除成员。从团队中移除成员将撤销他们对被允许资源的访问权限。

{{< tabs >}}
{{< tab name="管理控制台" >}}

使用管理控制台从特定团队中移除成员：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Teams**（团队）。
3. 选择团队名称。
4. 选择用户名旁边的 **X** 以将其从团队中移除。
5. 出现提示时，选择 **Remove**（移除）以进行确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

从特定团队中移除成员：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**、您的组织、**Teams**（团队），然后选择该团队。
3. 选择用户名旁边的 **X** 以将其从团队中移除。
4. 出现提示时，选择 **Remove**（移除）以进行确认。

{{< /tab >}}
{{< /tabs >}}

### 更新成员角色

组织所有者可以管理组织内的 [角色](/security/for-admins/roles-and-permissions/)。如果组织是公司的一部分，公司所有者也可以管理该组织的角色。如果您启用了 SSO，可以使用 [SCIM 进行角色映射](/security/for-admins/provisioning/scim/)。

{{< tabs >}}
{{< tab name="管理控制台" >}}

在管理控制台中更新成员角色：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Members**（成员）。
3. 找到您想要编辑其角色的成员用户名。选择 **Actions**（操作）菜单，然后选择 **Edit role**（编辑角色）。

> [!NOTE]
>
> 如果您是该组织的唯一所有者，您需要在编辑自己的角色之前指定一名新的所有者。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

在 Docker Hub 中更新成员角色：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**、您的组织，然后选择 **Members**（成员）。
3. 找到您想要编辑其角色的成员用户名。在表格中，选择 **Actions**（操作）图标。
4. 选择 **Edit role**（编辑角色）。
5. 选择他们的组织，选择您想要分配的角色，然后选择 **Save**（保存）。

> [!NOTE]
>
> 如果您是该组织的唯一所有者，您需要在编辑自己的角色之前指定一名新的所有者。

{{< /tab >}}
{{< /tabs >}}

## 导出成员 CSV 文件

{{< summary-bar feature_name="管理组织" >}}

所有者可以导出包含所有成员的 CSV 文件。公司级 CSV 文件包含以下字段：

- Name：用户姓名
- Username：用户的 Docker ID
- Email：用户的电子邮件地址
- Member of Organizations：用户在公司内所属的所有组织
- Invited to Organizations：用户在公司内受邀的所有组织
- Account Created：用户账户创建的时间和日期

{{< tabs >}}
{{< tab name="管理控制台" >}}

导出成员 CSV 文件：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Members**（成员）。
3. 选择 **download**（下载）图标以导出所有成员的 CSV 文件。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

导出成员 CSV 文件：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**、您的组织，然后选择 **Members**（成员）。
3. 选择 **Action**（操作）图标，然后选择 **Export users as CSV**（以 CSV 格式导出用户）。

{{< /tab >}}
{{< /tabs >}}
