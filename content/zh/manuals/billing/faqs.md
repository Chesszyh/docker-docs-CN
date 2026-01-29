---
title: 账单 FAQ
linkTitle: FAQ
description: 与账单相关的常见问题
keywords: 账单, 续订, 付款, FAQ
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
- 银联 (UnionPay)
- Link
- 使用[已验证](manuals/billing/payment-method.md#验证银行账户)的美国银行账户进行 ACH 转账

### 支持哪种货币？

美元 (USD)。

### 如果我的订阅付款失败会怎样？

如果您的订阅付款失败，将有 15 天的宽限期（包括截止日期）。Docker 会按照以下时间表尝试重新收取 3 次费用：

- 截止日期后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

每次付款尝试失败后，Docker 还会发送一封名为 `Action Required - Credit Card Payment Failed`（需要采取行动 - 信用卡付款失败）的电子邮件通知，并附上未付发票。

宽限期结束后，如果发票仍未支付，订阅将降级为免费订阅，并且所有付费功能都将被禁用。

### 我可以手动重试失败的付款吗？

不可以。Docker 会按照 [重试时间表](/manuals/billing/faqs.md#如果我的订阅付款失败会怎样) 自动重试失败的付款。

为了确保重试付款成功，请验证您的默认付款方式已更新。如果您需要更新默认付款方式，请参阅 [管理付款方式](/manuals/billing/payment-method.md#管理付款方式)。

### Docker 是否收取销售税和/或增值税 (VAT)？

Docker 对以下情况收取销售税和/或增值税 (VAT)：

- 对于美国客户，Docker 从 2024 年 7 月 1 日开始收取销售税。
- 对于欧洲客户，Docker 从 2025 年 3 月 1 日开始收取增值税 (VAT)。
- 对于英国客户，Docker 从 2025 年 5 月 1 日开始收取增值税 (VAT)。

为了确保税收评估准确，请确保您的账单信息和增值税/税务 ID（如果适用）已更新。请参阅 [更新账单信息](/billing/details/)。

如果您免征销售税，请参阅 [登记免税证明](/billing/tax-certificate/)。

### 我如何证明我的免税状态？

如果您免征销售税，您可以在 Docker 支持团队登记 [有效的免税证明](./tax-certificate.md)。请 [联系支持团队](https://hub.docker.com/support/contact) 开始办理。

### Docker 提供学术定价吗？

请联系 [Docker 销售团队](https://www.docker.com/company/contact)。

### 在我的订阅期限结束时，我需要做些什么吗？

不需要。所有月度和年度订阅都会在期限结束时使用原始付款方式自动续订。
