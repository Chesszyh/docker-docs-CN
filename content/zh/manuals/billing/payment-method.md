---
title: 添加或更新付款方式
weight: 20
description: 了解如何在 Docker Hub 中添加或更新付款方式
keywords: payments, billing, subscription, supported payment methods, failed payments, coupons
alisases:
    - /billing/core-billing/payment-method/
---

本页介绍如何为您的个人账户或组织添加或更新付款方式。

您可以随时添加付款方式或更新账户的现有付款方式。

> [!IMPORTANT]
>
> 如果您想删除所有付款方式，必须先将订阅降级为免费订阅。请参阅[降级](../subscription/change.md)。

支持以下付款方式：

- 银行卡
  - Visa
  - MasterCard
  - American Express
  - Discover
  - JCB
  - Diners
  - UnionPay
- 电子钱包
  - Stripe Link
- 银行账户
  - 使用[已验证](manuals/billing/payment-method.md#verify-a-bank-account)的美国银行账户进行 ACH 转账

所有货币（例如账单发票上列出的金额）均以美元（USD）计价。

{{% include "tax-compliance.md" %}}

## 管理付款方式

### 个人账户

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的
组织。
1. 选择 **Billing**。
1. 从左侧菜单选择 **Payment methods**。
1. 选择 **Add payment method**。
1. 输入您的新付款信息：
    - 如果您要添加银行卡：
        - 选择 **Card** 并填写银行卡信息表单。
    - 如果您要添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入您的 Link **email address** 和 **phone number**。
        - 如果您不是现有的 Link 客户，必须填写银行卡信息表单以存储用于 Link 付款的卡片。
    - 如果您要添加银行账户：
        - 选择 **US bank account**。
        - 验证您的 **Email** 和 **Full name**。
        - 如果列出了您的银行，请选择您银行的名称。
        - 如果未列出您的银行，请选择 **Search for your bank**。
        - 要验证您的银行账户，请参阅[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。
1. 选择 **Add payment method**。
1. 可选。您可以通过选择 **Set as default** 操作来设置新的默认付款方式。
1. 可选。您可以通过选择 **Delete** 操作来删除非默认付款方式。

> [!NOTE]
>
> 如果您想将美国银行账户设置为默认付款方式，必须
> 先验证该账户。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **Billing**。
1. 选择 **Payment methods** 链接。
1. 选择 **Add payment method**。
1. 输入您的新付款信息：
    - 如果您要添加银行卡：
        - 选择 **Card** 并填写银行卡信息表单。
    - 如果您要添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入您的 Link **email address** 和 **phone number**。
        - 如果您不是现有的 Link 客户，必须填写银行卡信息表单以存储用于 Link 付款的卡片。
1. 选择 **Add**。
1. 选择 **Actions** 图标，然后选择 **Make default** 以确保您的新付款方式应用于所有购买和订阅。
1. 可选。您可以通过选择 **Actions** 图标来删除非默认付款方式。然后，选择 **Delete**。

{{< /tab >}}
{{< /tabs >}}

### 组织

> [!NOTE]
>
> 您必须是组织所有者才能更改付款信息。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的
组织。
1. 选择 **Billing**。
1. 从左侧菜单选择 **Payment methods**。
1. 选择 **Add payment method**。
1. 输入您的新付款信息：
    - 如果您要添加银行卡：
        - 选择 **Card** 并填写银行卡信息表单。
    - 如果您要添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入您的 Link **email address** 和 **phone number**。
        - 如果您不是现有的 Link 客户，必须填写银行卡信息表单以存储用于 Link 付款的卡片。
    - 如果您要添加银行账户：
        - 选择 **US bank account**。
        - 验证您的 **Email** 和 **Full name**。
        - 如果列出了您的银行，请选择您银行的名称。
        - 如果未列出您的银行，请选择 **Search for your bank**。
        - 要验证您的银行账户，请参阅[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。
1. 选择 **Add payment method**。
1. 选择 **Add payment method**。
1. 可选。您可以通过选择 **Set as default** 操作来设置新的默认付款方式。
1. 可选。您可以通过选择 **Delete** 操作来删除非默认付款方式。

> [!NOTE]
>
> 如果您想将美国银行账户设置为默认付款方式，必须
> 先验证该账户。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 选择 **Payment methods** 链接。
1. 选择 **Add payment method**。
1. 输入您的新付款信息：
    - 如果您要添加银行卡：
        - 选择 **Card** 并填写银行卡信息表单。
    - 如果您要添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入您的 Link **email address** 和 **phone number**。
        - 如果您不是现有的 Link 客户，必须填写银行卡信息表单以存储用于 Link 付款的卡片。
1. 选择 **Add payment method**。
1. 选择 **Actions** 图标，然后选择 **Make default** 以确保您的新付款方式应用于所有购买和订阅。
1. 可选。您可以通过选择 **Actions** 图标来删除非默认付款方式。然后，选择 **Delete**。

{{< /tab >}}
{{< /tabs >}}

## 验证银行账户

有两种方式验证银行账户作为付款方式：

- 即时验证：Docker 支持多家主要银行的即时验证。
- 手动验证：所有其他银行必须手动验证。

### 即时验证

要即时验证您的银行账户，您必须从 Docker 账单流程中
登录您的银行账户：

1. 选择 **US bank account** 作为您的付款方式。
1. 验证您的 **Email** 和 **Full name**。
1. 如果列出了您的银行，请选择您银行的名称或选择 **Search for your bank**。
1. 登录您的银行并查看条款和条件。此协议
允许 Docker 从您关联的银行账户扣款。
1. 选择 **Agree and continue**。
1. 选择要关联和验证的账户，然后选择 **Connect account**。

账户验证成功后，您将在弹出模态窗口中看到成功消息。

### 手动验证

要手动验证您的银行账户，您必须输入银行对账单中的小额存款金额：

1. 选择 **US bank account** 作为您的付款方式。
1. 验证您的 **Email** 和 **First and last name**。
1. 选择 **Enter bank details manually instead**。
1. 输入您的银行详情：**Routing number** 和 **Account number**。
1. 选择 **Submit**。
1. 您将收到一封包含手动验证说明的电子邮件。

手动验证使用小额存款。您应该在 1-2 个工作日内在银行账户中看到一笔小额存款
（例如 $-0.01）。打开您的手动验证电子邮件并输入此存款金额以验证您的账户。

## 付款失败

> [!NOTE]
>
> 您无法手动重试失败的付款。Docker 将根据
重试时间表重试失败的付款。

如果您的订阅付款失败，有 15 天的宽限期，包括到期日。Docker 会按以下时间表重试收取付款 3 次：

- 到期日后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

Docker 还会在每次付款尝试失败后发送电子邮件通知 `Action Required - Credit Card Payment Failed`，并附带未付发票。

一旦宽限期结束且发票仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。

## 兑换优惠券

您可以为任何 Docker 付费订阅兑换优惠券。

优惠券可在以下情况下使用：
- 从免费订阅注册新的付费订阅
- 升级现有的付费订阅

在确认或输入付款方式时，系统会要求您输入优惠券代码。

如果您使用优惠券支付订阅费用，当优惠券到期时，您的付款方式将被收取订阅的全额费用。如果您没有保存的付款方式，您的账户将降级为免费订阅。
