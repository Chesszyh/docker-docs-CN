---
title: 创建您的组织
weight: 10
description: 了解如何创建组织。
keywords: Docker, docker, 注册表, 团队, 组织, 计划, Dockerfile, Docker Hub, 文档, 文档
aliases:
- /docker-hub/orgs/
---

{{< summary-bar feature_name="管理员组织" >}}

本节介绍如何创建组织。在开始之前：

- 您需要一个 [Docker ID](/accounts/create-account/)
- 查看 [Docker 订阅和功能](../../subscription/details.md) 以确定为您的组织选择哪种订阅

## 创建组织

有多种方法可以创建组织。您可以选择：
- 使用 Docker Hub 中的**创建组织**选项创建新组织
- 将现有用户帐户转换为组织

以下部分包含有关如何创建新组织的说明。有关将现有用户帐户转换为组织的先决条件和详细说明，请参阅
[将帐户转换为组织](/manuals/admin/organization/convert-account.md)。

{{< tabs >}}
{{< tab name="管理员控制台" >}}

要创建组织：

1. 登录 [Docker 主页](https://app.docker.com/) 并导航到组织列表底部。
1. 选择**创建新组织**。
1. 为您的组织选择订阅、账单周期，并指定您需要的席位数量。有关 Team 和 Business 订阅中提供的功能的详细信息，请参阅 [Docker 定价](https://www.docker.com/pricing/)。
1. 选择**继续到个人资料**。
1. 选择**创建组织**以创建一个新组织。
1. 输入**组织命名空间**。这是您组织在 Docker Hub 中的官方唯一名称。创建后无法更改组织的名称。

   > [!NOTE]
   >
   > 您不能为组织和您的 Docker ID 使用相同的名称。如果您想使用您的 Docker ID 作为组织名称，则必须首先[将您的帐户转换为组织](/manuals/admin/organization/convert-account.md)。

1. 输入您的**公司名称**。这是您公司的全名。Docker 会在您的组织页面和您发布的任何公共镜像的详细信息中显示公司名称。您可以随时通过导航到组织的**设置**页面来更新公司名称。
1. 选择**继续到账单**以继续。
1. 输入您组织的账单信息，然后选择**继续到付款**以继续到账单门户。
1. 提供您的付款详细信息并选择**购买**。

您现在已创建了一个组织。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 使用您的 Docker ID、电子邮件地址或社交提供商登录 [Docker Hub](https://hub.docker.com/)。
1. 选择**我的 Hub**，选择帐户下拉菜单，然后选择**创建组织**以创建新组织。
1. 为您的组织选择订阅、账单周期，并指定您需要的席位数量。有关 Team 和 Business 订阅中提供的功能的详细信息，请参阅 [Docker 定价](https://www.docker.com/pricing/)。
1. 选择**继续到个人资料**。
1. 输入**组织命名空间**。这是您组织在 Docker Hub 中的官方唯一名称。创建后无法更改组织的名称。

   > [!NOTE]
   >
   > 您不能为组织和您的 Docker ID 使用相同的名称。如果您想使用您的 Docker ID 作为组织名称，则必须首先[将您的帐户转换为组织](/manuals/admin/organization/convert-account.md)。

1. 输入您的**公司名称**。这是您公司的全名。Docker 会在您的组织页面和您发布的任何公共镜像的详细信息中显示公司名称。您可以随时通过导航到组织的**设置**页面来更新公司名称。
1. 选择**继续到账单**以继续。
1. 输入您组织的账单信息，然后选择**继续到付款**以继续到账单门户。
1. 提供您的卡详细信息并选择**购买**。

您现在已创建了一个组织。

{{< /tab >}}
{{< /tabs >}}

## 查看组织

{{< tabs >}}
{{< tab name="管理员控制台" >}}

要在管理控制台中查看组织：

1. 登录 [Docker 主页](https://app.docker.com) 并选择您的组织。
1. 从左侧导航菜单中，选择**管理员控制台**。

管理控制台包含许多选项，可让您配置组织。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

要查看组织：

1. 使用属于组织中任何团队的帐户登录 [Docker Hub](https://hub.docker.com)。

      > [!NOTE]
      >
      > 您不能*直接*登录组织。如果您通过[转换用户帐户](/manuals/admin/organization/convert-account.md)创建组织，这一点尤其重要，因为转换意味着您将失去登录该“帐户”的能力，因为它不再存在。要查看组织，您需要使用在转换期间分配的新所有者帐户或作为成员添加的另一个帐户登录。如果您登录后没有看到组织，则您既不是该组织的成员也不是所有者。组织管理员需要将您添加为组织的成员。

1. 在顶部导航栏中选择**我的 Hub**，然后从列表中选择您的组织。

组织登录页面显示各种选项，可让您配置组织。

- **成员**：显示团队成员列表。您可以使用**邀请成员**按钮邀请新成员。有关详细信息，请参阅[管理成员](./members.md)。
- **团队**：显示现有团队列表和每个团队中的成员数量。有关详细信息，请参阅[创建团队](./manage-a-team.md)。
- **仓库**：显示与组织关联的仓库列表。有关使用仓库的详细信息，请参阅[仓库](../../docker-hub/repos/_index.md)。
- **活动**：显示审计日志，即组织和仓库级别发生的活动的按时间顺序排列的列表。它为组织所有者提供所有团队成员活动的报告。有关详细信息，请参阅[审计日志](./activity-logs.md)。
- **设置**：显示有关您组织的信息，并允许您查看和更改您的仓库隐私设置，配置组织权限，例如[镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md)，配置通知设置，以及[停用](/manuals/admin/organization/deactivate-account.md#deactivate-an-organization)。您还可以更新显示在组织登录页面上的组织名称和公司名称。您必须是所有者才能访问组织的**设置**页面。
- **账单**：显示有关您现有 [Docker 订阅](../../subscription/_index.md) 的信息，包括席位数量和下一次付款到期日。有关如何访问组织的账单历史记录和付款方式，请参阅[查看账单历史记录](../../billing/history.md)。

{{< /tab >}}
{{< /tabs >}}

## 合并组织

> [!WARNING]
>
> 如果您要合并组织，建议在账单周期*结束时*进行。当您合并一个组织并降级另一个组织时，您将失去降级组织中的席位。Docker 不会为降级提供退款。

如果您有多个组织要合并为一个，请完成以下操作：

1. 根据辅助组织的席位数量，为要保留的主组织帐户[购买额外席位](../../subscription/manage-seats.md)。
1. 手动将用户添加到主组织，并从辅助组织中删除现有用户。
1. 手动移动您的数据，包括所有仓库。
1. 完成所有用户和数据移动后，将辅助帐户[降级](../../subscription/change.md)为免费订阅。请注意，Docker 不会为账单周期中途降级的组织提供退款。

> [!TIP]
>
> 如果您的组织拥有带有采购订单的 Docker Business 订阅，请联系 Docker 的支持或客户经理。

## 更多资源

- [视频：Docker Hub 组织](https://www.youtube.com/watch?v=WKlT1O-4Du8)