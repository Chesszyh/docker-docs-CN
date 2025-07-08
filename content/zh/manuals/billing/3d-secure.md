---
title: 3D Secure 身份验证
description: 了解 Docker 计费对 3D Secure 的支持。
keywords: 计费, 续订, 付款, 订阅
weight: 40
---

> [!NOTE]
>
> [Docker 订阅](../subscription/setup.md)付款支持 3D Secure 身份验证。

3D Secure (3DS) 身份验证为信用卡交易增加了额外的安全层。如果您在需要 3DS 的地区为 Docker 账单付款，或者使用需要 3DS 的付款方式，您需要验证您的身份才能完成任何交易。验证身份的方法因您的银行机构而异。

如果您的付款方式需要 3DS，以下交易将使用 3DS 身份验证。

- 启动[新的付费订阅](../subscription/setup.md)
- 将您的[计费周期](/billing/cycle/)从每月更改为每年
- [升级您的订阅](../subscription/change.md)
- [向现有订阅添加席位](../subscription/manage-seats.md)

## 故障排除

如果您遇到因 3DS 导致的付款错误，您可以通过以下方式进行故障排除。

1. 重试您的交易和身份验证。
2. 联系您的银行以确定其是否存在任何错误。
3. 尝试不需要 3DS 的其他付款方式。

> [!TIP]
>
> 确保您在浏览器中允许第三方脚本，并且在尝试完成付款时禁用您可能使用的任何广告拦截器。
