---
title: 管理组织成员
weight: 30
description: 了解如何在 Docker Hub 和 Docker 管理控制台中管理组织成员。
keywords: 成员, 团队, 组织, 邀请成员, 管理团队成员
aliases:
- /docker-hub/members/
---

了解如何在 Docker Hub 和 Docker 管理控制台中管理您的组织成员。

## 邀请成员

{{< tabs >}}
{{< tab name="管理员控制台" >}}

{{% admin-users product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-users product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 接受邀请

当邀请发送到用户的电子邮件地址时，他们会收到一个指向 Docker Hub 的链接，他们可以在其中接受或拒绝邀请。
要接受邀请：

1. 导航到您的电子邮件收件箱，打开包含加入 Docker 组织邀请的 Docker 电子邮件。
1. 要打开 Docker Hub 的链接，请选择**点击此处**链接。

   > [!WARNING]
   >
   > 邀请电子邮件链接在 14 天后过期。如果您的电子邮件链接已过期，
   > 您可以使用收到链接的电子邮件地址登录 [Docker Hub](https://hub.docker.com/)，并从**通知**面板接受邀请。

1. Docker 创建帐户页面将打开。如果您已有帐户，请选择**已有帐户？登录**。
如果您还没有帐户，请使用您收到邀请的电子邮件地址创建一个帐户。
1. 可选。如果您没有帐户并创建了一个，您必须返回您的电子邮件收件箱，并使用 Docker 验证电子邮件验证您的电子邮件地址。
1. 登录 Docker Hub 后，从顶部导航菜单中选择**我的 Hub**。
1. 在您的邀请上选择**接受**。

接受邀请后，您现在是组织的成员。

## 管理邀请

邀请成员后，您可以根据需要重新发送或删除邀请。

### 重新发送邀请

{{< tabs >}}
{{< tab name="管理员控制台" >}}

您可以从管理控制台发送个人邀请或批量邀请。

要重新发送个人邀请：

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**成员**。
1. 选择受邀者旁边的**操作菜单**，然后选择**重新发送**。
1. 选择**邀请**以确认。

要批量重新发送邀请：

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**成员**。
1. 使用**用户名**旁边的**复选框**批量选择用户。
1. 选择**重新发送邀请**。
1. 选择**重新发送**以确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要从 Docker Hub 重新发送邀请：

1. 登录 [Docker Hub](https://hub.docker.com/)。
1. 选择**我的 Hub**、您的组织，然后选择**成员**。
1. 在表格中，找到受邀者，选择**操作**图标，然后选择**重新发送邀请**。
1. 选择**邀请**以确认。

您还可以使用 Docker Hub API 重新发送邀请。有关更多信息，请参阅 [重新发送邀请](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1%7Bid%7D~1resend/patch) API 端点。

{{< /tab >}}
{{< /tabs >}}

### 删除邀请

{{< tabs >}}
{{< tab name="管理员控制台" >}}

要从管理控制台删除邀请：

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**成员**。
1. 选择受邀者旁边的**操作菜单**，然后选择**删除受邀者**。
1. 选择**删除**以确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要从 Docker Hub 删除成员的邀请：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub**、您的组织，然后选择**成员**。
1. 在表格中，选择**操作**图标，然后选择**删除成员**或**删除受邀者**。
1. 按照屏幕上的说明删除成员或受邀者。

您还可以使用 Docker Hub API 删除邀请。有关更多信息，请参阅 [取消邀请](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1%7Bid%7D/delete) API 端点。

{{< /tab >}}
{{< /tabs >}}

## 管理团队成员

使用 Docker Hub 或管理控制台添加或删除团队成员。组织所有者可以将成员添加到组织内的一个或多个团队。

### 将成员添加到团队

{{< tabs >}}
{{< tab name="管理员控制台" >}}

要使用管理控制台将成员添加到团队：

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**团队**。
1. 选择团队名称。
1. 选择**添加成员**。您可以通过搜索他们的电子邮件地址或用户名来添加成员。

   > [!NOTE]
   >
   > 受邀者必须首先接受加入组织的邀请，然后才能添加到团队中。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要使用 Docker Hub 将成员添加到团队：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub**、您的组织，然后选择**成员**。
1. 选择**操作**图标，然后选择**添加到团队**。

   > [!NOTE]
   >
   > 您还可以导航到**我的 Hub** > **您的组织** > **团队** > **您的团队名称**，然后选择**添加成员**。从下拉列表中选择一个成员以将其添加到团队，或按 Docker ID 或电子邮件搜索。
1. 选择团队，然后选择**添加**。

   > [!NOTE]
   >
   > 受邀者必须首先接受加入组织的邀请，然后才能添加到团队中。

{{< /tab >}}
{{< /tabs >}}

### 从团队中删除成员

> [!NOTE]
>
> 如果您的组织使用启用了 [SCIM](/manuals/security/for-admins/provisioning/scim.md) 的单点登录 (SSO)，则应从身份提供商 (IdP) 中删除成员。这将自动从 Docker 中删除成员。如果禁用了 SCIM，则必须在 Docker 中手动管理成员。

组织所有者可以从 Docker Hub 或管理控制台中的团队中删除成员。从团队中删除成员将撤销他们对允许资源的访问权限。

{{< tabs >}}
{{< tab name="管理员控制台" >}}

要使用管理控制台从特定团队中删除成员：

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**团队**。
1. 选择团队名称。
1. 选择用户姓名旁边的 **X** 以将其从团队中删除。
1. 出现提示时，选择**删除**以确认。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要使用 Docker Hub 从特定团队中删除成员：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub**、您的组织、**团队**，然后选择团队。
1. 选择用户姓名旁边的 **X** 以将其从团队中删除。
1. 出现提示时，选择**删除**以确认。

{{< /tab >}}
{{< /tabs >}}

### 更新成员角色

组织所有者可以在组织内管理[角色](/security/for-admins/roles-and-permissions/)。
如果组织是公司的一部分，则公司所有者也可以管理该组织的权限。如果启用了 SSO，则可以使用 [SCIM 进行角色映射](/security/for-admins/provisioning/scim/)。

{{< tabs >}}
{{< tab name="管理员控制台" >}}

要在管理控制台中更新成员角色：

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**成员**。
1. 找到您要编辑其角色的成员的用户名。选择**操作**菜单，然后选择**编辑角色**。

> [!NOTE]
>
> 如果您是组织的唯一所有者，
> 则需要先分配新所有者，然后才能编辑您的角色。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要在 Docker Hub 中更新成员角色：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub**、您的组织，然后选择**成员**。
1. 找到您要编辑其角色的成员的用户名。在表格中，选择**操作**图标。
1. 选择**编辑角色**。
1. 选择他们的组织，选择您要分配的角色，然后选择**保存**。

> [!NOTE]
>
> 如果您是组织的唯一所有者，
> 则需要先分配新所有者，然后才能编辑您的角色。

{{< /tab >}}
{{< /tabs >}}

## 导出成员 CSV 文件

{{< summary-bar feature_name="管理员组织" >}}

所有者可以导出包含所有成员的 CSV 文件。公司的 CSV 文件包含以下字段：

- 姓名：用户姓名
- 用户名：用户 Docker ID
- 电子邮件：用户电子邮件地址
- 所属组织：用户在公司内所属的所有组织
- 邀请到组织：用户在公司内被邀请到的所有组织
- 帐户创建：用户帐户创建的时间和日期

{{< tabs >}}
{{< tab name="管理员控制台" >}}

要导出成员的 CSV 文件：

1. 登录 [Docker 主页](https://app.docker.com/) 并选择您的组织。
1. 选择**成员**。
1. 选择**下载**图标以导出所有成员的 CSV 文件。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要导出成员的 CSV 文件：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择**我的 Hub**、您的组织，然后选择**成员**。
1. 选择**操作**图标，然后选择**导出用户为 CSV**。

{{< /tab >}}
{{< /tabs >}}