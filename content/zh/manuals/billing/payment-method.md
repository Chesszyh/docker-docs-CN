---
title: 添加或更新付款方式
weight: 20
description: 了解如何在 Docker Hub 中添加或更新付款方式
keywords: 付款, 账单, 订阅, 支持的付款方式, 付款失败, 优惠券
alisases:
    - /billing/core-billing/payment-method/
---

本页面介绍了如何为您的个人账户或组织添加或更新付款方式。

您可以随时添加付款方式或更新账户现有的付款方式。

> [!IMPORTANT]
>
> 如果您想移除所有付款方式，必须先将订阅降级为免费订阅。请参阅 [降级](../subscription/change.md)。

支持以下付款方式：

- 卡片
  - Visa
  - MasterCard
  - American Express
  - Discover
  - JCB
  - Diners
  - 银联 (UnionPay)
- 钱包
  - Stripe Link
- 银行账户
  - 使用[已验证](manuals/billing/payment-method.md#验证银行账户)的美国银行账户进行 ACH 转账

所有货币（例如账单发票上列出的金额）均以美元 (USD) 为单位。

{{% include "tax-compliance.md" %}}

## 管理付款方式

### 个人账户

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

添加付款方式的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Payment methods**（付款方式）。
4. 选择 **Add payment method**（添加付款方式）。
5. 输入您的新付款信息：
    - 如果您正在添加卡片：
        - 选择 **Card**（卡片）并填写卡片信息表单。
    - 如果您正在添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link**（使用 Link 进行安全、一键结账）并输入您的 Link **电子邮件地址** 和 **电话号码**。
        - 如果您还不是 Link 客户，则必须填写卡片信息表单以存储用于 Link 付款的卡片。
    - 如果您正在添加银行账户：
        - 选择 **US bank account**（美国银行账户）。
        - 验证您的 **Email**（电子邮件）和 **Full name**（全名）。
        - 如果您的银行已列出，请选择银行名称。
        - 如果您的银行未列出，请选择 **Search for your bank**（搜索您的银行）。
        - 要验证您的银行账户，请参阅 [验证银行账户](manuals/billing/payment-method.md#验证银行账户)。
6. 选择 **Add payment method**（添加付款方式）。
7. 可选：您可以通过选择 **Set as default**（设为默认）操作来设置新的默认付款方式。
8. 可选：您可以通过选择 **Delete**（删除）操作来移除非默认付款方式。

> [!NOTE]
>
> 如果您想将美国银行账户设置为默认付款方式，必须先验证该账户。

{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

添加付款方式的步骤：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **Billing**（账单）。
3. 选择 **Payment methods**（付款方式）链接。
4. 选择 **Add payment method**（添加付款方式）。
5. 输入您的新付款信息：
    - 如果您正在添加卡片：
        - 选择 **Card**（卡片）并填写卡片信息表单。
    - 如果您正在添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入您的 Link **电子邮件地址** 和 **电话号码**。
        - 如果您还不是 Link 客户，则必须填写卡片信息表单以存储用于 Link 付款的卡片。
6. 选择 **Add**（添加）。
7. 选择 **Actions**（操作）图标，然后选择 **Make default**（设为默认），以确保您的新付款方式适用于所有购买和订阅。
8. 可选：您可以通过选择 **Actions**（操作）图标并选择 **Delete**（删除）来移除非默认付款方式。

{{< /tab >}}
{{< /tabs >}}

### 组织

> [!NOTE]
>
> 您必须是组织所有者才能更改付款信息。

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

添加付款方式的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Payment methods**（付款方式）。
4. 选择 **Add payment method**（添加付款方式）。
5. 输入您的新付款信息：
    - 如果您正在添加卡片：
        - 选择 **Card**（卡片）并填写卡片信息表单。
    - 如果您正在添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入您的 Link **电子邮件地址** 和 **电话号码**。
        - 如果您还不是 Link 客户，则必须填写卡片信息表单以存储用于 Link 付款的卡片。
    - 如果您正在添加银行账户：
        - 选择 **US bank account**（美国银行账户）。
        - 验证您的 **Email**（电子邮件）和 **Full name**（全名）。
        - 如果您的银行已列出，请选择银行名称。
        - 如果您的银行未列出，请选择 **Search for your bank**（搜索您的银行）。
        - 要验证您的银行账户，请参阅 [验证银行账户](manuals/billing/payment-method.md#验证银行账户)。
6. 选择 **Add payment method**（添加付款方式）。
7. 选择 **Add payment method**（添加付款方式）。
8. 可选：您可以通过选择 **Set as default**（设为默认）操作来设置新的默认付款方式。
9. 可选：您可以通过选择 **Delete**（删除）操作来移除非默认付款方式。

> [!NOTE]
>
> 如果您想将美国银行账户设置为默认付款方式，必须先验证该账户。

{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

添加付款方式的步骤：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Payment methods**（付款方式）链接。
4. 选择 **Add payment method**（添加付款方式）。
5. 输入您的新付款信息：
    - 如果您正在添加卡片：
        - 选择 **Card**（卡片）并填写卡片信息表单。
    - 如果您正在添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入您的 Link **电子邮件地址** 和 **电话号码**。
        - 如果您还不是 Link 客户，则必须填写卡片信息表单以存储用于 Link 付款的卡片。
6. 选择 **Add payment method**（添加付款方式）。
7. 选择 **Actions**（操作）图标，然后选择 **Make default**（设为默认），以确保您的新付款方式适用于所有购买和订阅。
8. 可选：您可以通过选择 **Actions**（操作）图标并选择 **Delete**（删除）来移除非默认付款方式。

{{< /tab >}}
{{< /tabs >}}

## 验证银行账户

有两种方法可以将银行账户验证为付款方式：

- 即时验证：Docker 支持多家主要银行进行即时验证。
- 手动验证：所有其他银行必须手动验证。

### 即时验证

要即时验证您的银行账户，您必须从 Docker 计费流程中登录您的银行账户：

1. 选择 **US bank account**（美国银行账户）作为您的付款方式。
2. 验证您的 **Email**（电子邮件）和 **Full name**（全名）。
3. 如果您的银行已列出，请选择银行名称，或者选择 **Search for your bank**（搜索您的银行）。
4. 登录您的银行并查看条款和条件。此协议允许 Docker 从您连接的银行账户中扣款。
5. 选择 **Agree and continue**（同意并继续）。
6. 选择一个要关联并验证的账户，然后选择 **Connect account**（连接账户）。

账户验证成功后，您将在弹出窗口中看到成功消息。

### 手动验证

要手动验证您的银行账户，您必须输入银行对账单中的微额存款金额：

1. 选择 **US bank account**（美国银行账户）作为您的付款方式。
2. 验证您的 **Email**（电子邮件）和 **First and last name**（姓名）。
3. 选择 **Enter bank details manually instead**（改为手动输入银行详情）。
4. 输入您的银行详情：**Routing number**（路由号码）和 **Account number**（账号）。
5. 选择 **Submit**（提交）。
6. 您将收到一封包含如何手动验证说明的电子邮件。

手动验证使用微额存款。您应该在 1-2 个工作日内看到银行账户中有一笔小额存款（例如 $-0.01）。打开手动验证邮件，输入这笔存款的金额以验证您的账户。

## 付款失败

> [!NOTE]
>
> 您不能手动重试失败的付款。Docker 将根据重试时间表重试失败的付款。

如果您的订阅付款失败，将有 15 天的宽限期（包括截止日期）。Docker 会按照以下时间表尝试重新收取 3 次费用：

- 截止日期后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

每次付款尝试失败后，Docker 还会发送一封名为 `Action Required - Credit Card Payment Failed` 的电子邮件通知，并附上未付发票。

宽限期结束后，如果发票仍未支付，订阅将降级为免费订阅，并且所有付费功能都将被禁用。

## 兑换优惠券

您可以为任何付费的 Docker 订阅兑换优惠券。

可以在以下情况下使用优惠券：
- 从免费订阅注册新的付费订阅
- 升级现有的付费订阅

当您确认或输入付款方式时，系统会要求您输入优惠券代码。

如果您使用优惠券支付订阅费用，当优惠券过期时，您的付款方式将被收取订阅的全额费用。如果您没有保存付款方式，您的账户将降级为免费订阅。
