---
title: 3D Secure 身份验证
description: 了解 Docker 账单的 3D Secure 支持。
keywords: billing, renewal, payments, subscriptions
weight: 40
---

> [!NOTE]
>
> [Docker 订阅](../subscription/setup.md)付款支持 3D Secure 身份验证。

3D Secure（3DS）身份验证为信用卡交易增加了一个额外的安全层。如果您在需要 3DS 的地区为 Docker 账单付款，或者使用需要 3DS 的付款方式，您需要验证身份才能完成任何交易。用于验证身份的方法因您的银行机构而异。

如果您的付款方式需要，以下交易将使用 3DS 身份验证。

- 开始[新的付费订阅](../subscription/setup.md)
- 将您的[账单周期](/billing/cycle/)从月付更改为年付
- [升级您的订阅](../subscription/change.md)
- 向现有订阅[添加席位](../subscription/manage-seats.md)

## 故障排除

如果您在完成付款时因 3DS 遇到错误，可以通过以下方式进行故障排除。

1. 重试您的交易和身份验证。
2. 联系您的银行以确定是否是他们那边的错误。
3. 尝试使用不需要 3DS 的其他付款方式。

> [!TIP]
>
> 确保您在浏览器中允许第三方脚本，并在尝试完成付款时禁用您可能使用的任何广告拦截器。
