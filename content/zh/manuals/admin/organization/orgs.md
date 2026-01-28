---
title: 创建您的组织
weight: 10
description: 了解如何创建组织。
keywords: Docker, docker, registry, 团队, 组织, 计划, Dockerfile, Docker Hub, 文档
aliases:
- /docker-hub/orgs/
---

{{< summary-bar feature_name="管理组织" >}}

本节介绍了如何创建组织。在开始之前：

- 您需要一个 [Docker ID](/accounts/create-account/)
- 查阅 [Docker 订阅和功能](../../subscription/details.md) 以确定为您的组织选择哪种订阅

## 创建组织

创建组织有多种方式。您可以：
- 使用 Docker Hub 中的 **Create Organization**（创建组织）选项创建一个新组织
- 将现有的用户账户转换为组织

以下部分包含有关如何创建新组织的说明。有关将现有用户账户转换为组织的前提条件和详细说明，请参阅 [将账户转换为组织](/manuals/admin/organization/convert-account.md)。

{{< tabs >}}
{{< tab name="管理控制台" >}}

创建组织的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并导航至组织列表的底部。
2. 选择 **Create new organization**（创建新组织）。
3. 为您的组织选择订阅、账单周期，并指定您需要的席位数量。有关 Team 和 Business 订阅提供的功能详情，请参阅 [Docker 定价](https://www.docker.com/pricing/)。
4. 选择 **Continue to profile**（继续填写资料）。
5. 选择 **Create an organization**（创建组织）以创建一个新组织。
6. 输入 **Organization namespace**（组织命名空间）。这是您的组织在 Docker Hub 中的官方唯一名称。组织创建后，无法更改其名称。

   > [!NOTE]
   >
   > 您不能将同一个名称用于组织和您的 Docker ID。如果您想使用您的 Docker ID 作为组织名称，则必须先 [将您的账户转换为组织](/manuals/admin/organization/convert-account.md)。

7. 输入您的 **Company name**（公司名称）。这是您公司的全称。Docker 会在您的组织页面以及您发布的任何公共镜像的详细信息中显示公司名称。您可以随时导航至组织的 **Settings**（设置）页面来更新公司名称。
8. 选择 **Continue to billing**（继续进行账单设置）。
9. 输入您组织的账单信息，然后选择 **Continue to payment**（继续付款）以进入账单门户。
10. 提供您的付款详情并选择 **Purchase**（购买）。

您现在已经创建了一个组织。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 使用您的 Docker ID、电子邮件地址或社交账号登录 [Docker Hub](https://hub.docker.com/)。
2. 选择 **My Hub**，选择账户下拉菜单，然后选择 **Create Organization**（创建组织）以创建一个新组织。
3. 为您的组织选择订阅、账单周期，并指定您需要的席位数量。有关 Team 和 Business 订阅提供的功能详情，请参阅 [Docker 定价](https://www.docker.com/pricing/)。
4. 选择 **Continue to profile**（继续填写资料）。
5. 输入 **Organization namespace**（组织命名空间）。这是您的组织在 Docker Hub 中的官方唯一名称。组织创建后，无法更改其名称。

   > [!NOTE]
   >
   > 您不能将同一个名称用于组织和您的 Docker ID。如果您想使用您的 Docker ID 作为组织名称，则必须先 [将您的账户转换为组织](/manuals/admin/organization/convert-account.md)。

6. 输入您的 **Company name**（公司名称）。这是您公司的全称。Docker 会在您的组织页面以及您发布的任何公共镜像的详细信息中显示公司名称。您可以随时导航至组织的 **Settings**（设置）页面来更新公司名称。
7. 选择 **Continue to billing**（继续进行账单设置）。
8. 输入您组织的账单信息，然后选择 **Continue to payment**（继续付款）以进入账单门户。
9. 提供您的卡片详情并选择 **Purchase**（购买）。

您现在已经创建了一个组织。

{{< /tab >}}
{{< /tabs >}}

## 查看组织

{{< tabs >}}
{{< tab name="管理控制台" >}}

在管理控制台中查看组织的步骤：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
2. 从左侧导航菜单中选择 **Admin Console**（管理控制台）。

管理控制台包含许多允许您配置组织的选项。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

查看组织的步骤：

1. 使用属于该组织任何团队成员的用户账户登录 [Docker Hub](https://hub.docker.com)。

      > [!NOTE]
      >
      > 您不能 *直接* 登录组织。如果您通过 [转换用户账户](/manuals/admin/organization/convert-account.md) 创建了组织，这一点尤为重要，因为转换意味着您失去了登录该“账户”的能力，因为它已不再存在。要查看该组织，您需要使用转换期间指定的新的所有者账户登录，或者使用另一个被添加为成员的账户登录。如果登录后看不到该组织，说明您既不是该组织的成员也不是所有者。组织管理员需要将您添加为组织成员。

2. 选择顶部导航栏中的 **My Hub**，然后从列表中选择您的组织。

组织着陆页显示了允许您配置组织的各种选项。

- **Members**（成员）：显示团队成员列表。您可以使用 **Invite members**（邀请成员）按钮邀请新成员。有关详情，请参阅 [管理成员](./members.md)。
- **Teams**（团队）：显示现有团队的列表以及每个团队中的成员数量。有关详情，请参阅 [创建团队](./manage-a-team.md)。
- **Repositories**（存储库）：显示与该组织关联的存储库列表。有关使用存储库的详细信息，请参阅 [存储库](../../docker-hub/repos/_index.md)。
- **Activity**（活动）：显示审计日志，即组织和存储库层级发生的活动的按时间顺序排列的列表。它为组织所有者提供所有团队成员活动的报告。有关详情，请参阅 [审计日志](./activity-logs.md)。
- **Settings**（设置）：显示有关您组织的信息，并允许您查看和更改存储库隐私设置、配置组织权限（如 [镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md)）、配置通知设置以及 [停用](/manuals/admin/organization/deactivate-account.md#deactivate-an-organization) 组织。您还可以更新显示在组织着陆页上的组织名称和公司名称。您必须是所有者才能访问组织的 **Settings**（设置）页面。
- **Billing**（账单）：显示有关您现有 [Docker 订阅](../../subscription/_index.md) 的信息，包括席位数量和下次付款截止日期。有关如何访问您组织的账单历史和付款方式，请参阅 [查看账单历史](../../billing/history.md)。

{{< /tab >}}
{{< /tabs >}}

## 合并组织

> [!WARNING]
>
> 如果您正在合并组织，建议在账单周期 *结束* 时进行。当您合并一个组织并降级另一个组织时，您将失去降级组织上的席位。对于降级，Docker 不提供退款。

如果您有多个想要合并为一个的组织，请完成以下操作：

1. 根据次要组织的席位数量，为您想要保留的主要组织账户 [购买额外的席位](../../subscription/manage-seats.md)。
2. 手动将用户添加到主要组织，并将现有用户从次要组织中移除。
3. 手动迁移您的数据，包括所有存储库。
4. 完成所有用户和数据的迁移后，将次要账户 [降级](../../subscription/change.md) 为免费订阅。请注意，对于在账单周期中期降级组织，Docker 不提供退款。

> [!TIP]
>
> 如果您的组织拥有带有采购订单的 Docker Business 订阅，请联系 Docker 支持或您的客户经理。

## 更多资源

- [视频：Docker Hub 组织](https://www.youtube.com/watch?v=WKlT1O-4Du8)
