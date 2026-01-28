---
description: 了解如何更改您的 Docker 订阅
keywords: Docker Hub, upgrade, downgrade, subscription, Pro, Team, business, pricing
title: 更改您的订阅
aliases:
- /docker-hub/upgrade/
- /docker-hub/billing/upgrade/
- /subscription/upgrade/
- /subscription/downgrade/
- /subscription/core-subscription/upgrade/
- /subscription/core-subscription/downgrade/
- /docker-hub/cancel-downgrade/
- /docker-hub/billing/downgrade/
- /billing/scout-billing/
- /billing/subscription-management/
weight: 30
---

{{% include "tax-compliance.md" %}}

以下部分描述了当您拥有 Docker 订阅或旧版 Docker 订阅时如何更改计划。

> [!NOTE]
>
> 旧版 Docker 计划适用于最后一次购买或续订订阅在 2024 年 12 月 10 日之前的 Docker 订阅者。这些订阅者将保持其当前订阅和定价，直到其下一个续订日期在 2024 年 12 月 10 日或之后。要查看购买或续订历史记录，请查看您的[账单历史记录](../billing/history.md)。有关旧版订阅的更多详情，请参阅[宣布升级 Docker 计划](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

## 升级您的订阅

当您升级 Docker 订阅时，您可以立即访问 Docker 订阅中提供的所有功能和权益。有关每个订阅中可用功能的详细信息，请参阅 [Docker 定价](https://www.docker.com/pricing)。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要升级您的 Docker 订阅：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您要升级的组织。
1. 选择 **Billing**。
1. 可选。如果您从免费 Personal 订阅升级到 Team 订阅并希望保留您的用户名，请[将您的用户账户转换为组织](../admin/organization/convert-account.md)。
1. 选择 **Upgrade**。
1. 按照屏幕上的说明完成升级。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，您必须验证该账户。有关更多信息，请参阅[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

您可以将旧版 Docker Core、Docker Build Cloud 或 Docker Scout 订阅升级为包含所有工具访问权限的 Docker 订阅。

联系 [Docker 销售团队](https://www.docker.com/pricing/contact-sales/)以升级您的旧版 Docker 订阅。

{{< /tab >}}
{{< /tabs >}}

## 降级您的订阅

您可以在续订日期之前随时降级您的 Docker 订阅。订阅的未使用部分不予退款或抵扣。

当您降级订阅时，付费功能的访问权限将持续到下一个计费周期。降级将在下一个计费周期生效。

> [!IMPORTANT]
>
> 如果您将个人账户从 Pro 订阅降级为 Personal 订阅，请注意 [Personal 订阅](details.md#docker-personal)不包括私有仓库的协作者。Personal 订阅只包含一个私有仓库。当您降级时，所有协作者将被移除，额外的私有仓库将被锁定。
> 在降级之前，请考虑以下事项：
> - 团队规模：您可能需要减少团队成员数量，并将任何私有仓库转换为公共仓库或将其删除。有关每个层级可用功能的信息，请参阅 [Docker 定价](https://www.docker.com/pricing)。
> - SSO 和 SCIM：如果您想降级 Docker Business 订阅，并且您的组织使用单点登录 (SSO) 进行用户身份验证，您需要在降级之前移除 SSO 连接和已验证的域。移除 SSO 连接后，任何自动配置的组织成员（例如，通过 SCIM）需要设置密码才能在没有 SSO 的情况下登录。为此，用户可以[在登录时重置密码](/accounts/create-account/#reset-your-password-at-sign-in)。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

如果您有[销售协助的 Docker Business 订阅](details.md#sales-assisted)，请联系您的客户经理来降级您的订阅。

要降级您的 Docker 订阅：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您要降级的组织。
1. 选择 **Billing**。
1. 选择操作图标，然后选择 **Cancel subscription**。
1. 填写反馈调查以继续取消操作。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

如果您有[销售协助的 Docker Business 订阅](details.md#sales-assisted)，请联系您的客户经理来降级您的订阅。

### 降级旧版 Docker 订阅

要降级您的旧版 Docker 订阅：

1. 登录 [Docker Hub](https://hub.docker.com/billing)。
1. 选择您要降级的组织，然后选择 **Billing**。
1. 要降级，您必须导航到升级计划页面。选择 **Upgrade**。
1. 在升级页面，在 **Free Team** 计划卡片中选择 **Downgrade**。
1. 按照屏幕上的说明完成降级。

### 降级 Docker Build Cloud 订阅

要降级您的 Docker Build Cloud 订阅：

1. 登录 [Docker Home](https://app.docker.com) 并选择 **Build Cloud**。
1. 选择 **Account settings**，然后选择 **Downgrade**。
1. 要确认降级，在文本字段中输入 **DOWNGRADE** 并选择 **Yes, continue**。
1. 账户设置页面将更新，显示通知栏告知您降级日期（下一个计费周期开始）。

{{< /tab >}}
{{< /tabs >}}

## 暂停订阅

您不能暂停或延迟订阅。如果订阅发票在到期日未付款，则有 15 天的宽限期，包括到期日。
