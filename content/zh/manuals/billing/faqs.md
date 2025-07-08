---
title: 计费常见问题解答
linkTitle: 常见问题解答
description: 与计费相关的常见问题
keywords: 计费, 续订, 付款, 常见问题解答
tags: [FAQ]
weight: 60
---

### 支持哪些信用卡和借记卡？

- Visa
- MasterCard
- American Express
- Discover
- JCB
- Diners
- UnionPay
- Link
- ACH 转账（通过[已验证](manuals/billing/payment-method.md#verify-a-bank-account)的美国银行账户）

### 支持哪种货币？

美元 (USD)。

### 如果我的订阅付款失败怎么办？

如果您的订阅付款失败，则有 15 天的宽限期，包括到期日。Docker 将按照以下时间表重试收款 3 次：

- 到期日后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

每次付款失败后，Docker 还会发送一封电子邮件通知“需要操作 - 信用卡付款失败”，并附上未付款的发票。

一旦宽限期结束且发票仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。

### 我可以手动重试失败的付款吗？

不可以。Docker 将根据[重试计划](/manuals/billing/faqs.md#what-happens-if-my-subscription-payment-fails)重试失败的付款。

为确保重试付款成功，请验证您的默认付款是否已更新。如果您需要更新默认付款方式，请参阅[管理付款方式](/manuals/billing/payment-method.md#manage-payment-method)。

### Docker 是否收取销售税和/或增值税？

Docker 从以下地区收取销售税和/或增值税：

- 对于美国客户，Docker 于 2024 年 7 月 1 日开始收取销售税。
- 对于欧洲客户，Docker 于 2025 年 3 月 1 日开始收取增值税。
- 对于英国客户，Docker 于 2025 年 5 月 1 日开始收取增值税。

为确保税收评估正确，请确保您的计费信息和增值税/税务 ID（如果适用）已更新。请参阅[更新计费信息](/billing/details/)。

如果您免征销售税，请参阅[注册税务证明](/billing/tax-certificate/)。

### 我如何证明我的免税身份？

如果您免征销售税，您可以向 Docker 的支持团队[注册有效的免税证明](./tax-certificate.md)。[联系支持](https://hub.docker.com/support/contact)以开始。

### Docker 是否提供学术定价？

请联系 [Docker 销售团队](https://www.docker.com/company/contact)。

### 我的订阅期结束时需要做任何事情吗？

不需要。所有按月和按年订阅都会在期末使用原始付款方式自动续订。
