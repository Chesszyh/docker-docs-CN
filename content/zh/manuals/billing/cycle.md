---
title: 更改账单周期
weight: 50
description: 了解如何更改 Docker 订阅的账单周期
keywords: billing, cycle, payments, subscription
---

您可以按月付或年付的账单周期支付订阅费用。您在购买订阅时选择
首选的账单周期。

> [!NOTE]
>
> Business 订阅仅提供年付账单周期。

如果您使用月付账单周期，可以选择切换到年付
账单周期。

> [!NOTE]
>
> 您无法从年付账单周期切换到月付周期。

当您更改账单周期的时长时：

- 下一个账单日期将反映新的周期。要查找您的下一个账单日期，
请参阅[查看续订日期](history.md#view-renewal-date)。
- 订阅的开始日期将重置。例如，如果
月付订阅的开始日期是 3 月 1 日，结束日期是 4 月 1 日，那么在
2024 年 3 月 15 日切换账单周期后，新的开始日期是 2024 年 3 月
15 日，新的结束日期是 2025 年 3 月 15 日。
- 任何未使用的月付订阅将按比例折算并作为抵用金应用于
新的年付周期。例如，如果您从每月 $10 的订阅切换到
每年 $100 的订阅，扣除未使用的月付价值
（在本例中为 $5），迁移费用变为 $95（$100 - $5）。2025 年 3 月 15 日
之后的续订费用为 $100。

{{% include "tax-compliance.md" %}}

## 个人账户

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要更改您的账单周期：

1. 登录 [Docker Home](https://app.docker.com/) 并选择
您的组织。
1. 选择 **Billing**。
1. 在计划和使用量页面，选择 **Switch to annual billing**。
1. 验证您的账单信息。
1. 选择 **Continue to payment**。
1. 验证付款信息并选择 **Upgrade subscription**。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，您必须验证该账户。有关
> 更多信息，请参阅
[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

账单计划和使用量页面现在将反映您新的年付订阅
详情。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要更改您的账单周期：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 在 **Plan** 标签页的右下角，选择 **Switch to annual billing**。
1. 查看 **Change to an Annual subscription**
页面上显示的信息，然后选择 **Accept Terms and Purchase** 确认。

{{< /tab >}}
{{< /tabs >}}

## 组织

> [!NOTE]
>
> 您必须是组织所有者才能更改付款信息。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要更改组织的账单周期：

1. 登录 [Docker Home](https://app.docker.com/) 并选择
您的组织。
1. 选择 **Billing**。
1. 在计划和使用量页面，选择 **Switch to annual billing**。
1. 验证您的账单信息。
1. 选择 **Continue to payment**。
1. 验证付款信息并选择 **Upgrade subscription**。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，您必须验证该账户。有关
> 更多信息，请参阅
> [验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要更改组织的账单周期：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 选择 **Switch to annual billing**。
1. 查看 **Change to an Annual subscription**
页面上显示的信息，然后选择 **Accept Terms and Purchase** 确认。

{{< /tab >}}
{{< /tabs >}}
