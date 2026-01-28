---
title: 账单常见问题
linkTitle: 常见问题
description: 账单相关的常见问题
keywords: billing, renewal, payments, faq
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
- 使用[已验证](manuals/billing/payment-method.md#verify-a-bank-account)的美国银行账户进行 ACH 转账

### 支持哪种货币？

美元（USD）。

### 如果我的订阅付款失败会怎样？

如果您的订阅付款失败，有 15 天的宽限期，包括到期日。Docker 会按以下时间表重试收取付款 3 次：

- 到期日后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

Docker 还会在每次付款尝试失败后发送电子邮件通知 `Action Required - Credit Card Payment Failed`，并附带未付发票。

一旦宽限期结束且发票仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。

### 我可以手动重试失败的付款吗？

不可以。Docker 会按[重试时间表](/manuals/billing/faqs.md#what-happens-if-my-subscription-payment-fails)重试失败的付款。

要确保重试付款成功，请验证您的默认付款方式是否已
更新。如果您需要更新默认付款方式，请参阅
[管理付款方式](/manuals/billing/payment-method.md#manage-payment-method)。

### Docker 是否收取销售税和/或 VAT（增值税）？

Docker 从以下客户收取销售税和/或 VAT：

- 对于美国客户，Docker 从 2024 年 7 月 1 日开始收取销售税。
- 对于欧洲客户，Docker 从 2025 年 3 月 1 日开始收取 VAT。
- 对于英国客户，Docker 从 2025 年 5 月 1 日开始收取 VAT。

为确保税务评估正确，请确保您的账单
信息和 VAT/Tax ID（如适用）已更新。请参阅
[更新账单信息](/billing/details/)。

如果您享有销售税豁免，请参阅
[注册税务证明](/billing/tax-certificate/)。

### 如何证明我的免税状态？

如果您享有销售税豁免，您可以向 Docker 支持团队[注册有效的税务豁免证明](./tax-certificate.md)。[联系支持](https://hub.docker.com/support/contact)以开始。

### Docker 是否提供教育优惠价格？

请联系 [Docker 销售团队](https://www.docker.com/company/contact)。

### 我需要在订阅期结束时做什么吗？

不需要。所有月付和年付订阅都会在期限结束时使用原始付款方式自动续订。
