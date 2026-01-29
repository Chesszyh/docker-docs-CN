---
title: 3D Secure 认证
description: 了解 Docker 账单对 3D Secure 的支持。
keywords: 账单, 续订, 付款, 订阅
weight: 40
---

> [!NOTE]
>
> [Docker 订阅](../subscription/setup.md) 付款支持 3D Secure 认证。

3D Secure (3DS) 认证为信用卡交易增加了一个额外的安全层。如果您在需要 3DS 的地区进行 Docker 账单支付，或者使用的付款方式需要 3DS，则需要验证身份才能完成交易。用于验证身份的方法因您的银行机构而异。

如果您的付款方式需要，以下交易将使用 3DS 认证。

- 开始 [新的付费订阅](../subscription/setup.md)
- 将 [账单周期](/billing/cycle/) 从按月更改为按年
- [升级您的订阅](../subscription/change.md)
- 为现有订阅 [添加席位](../subscription/manage-seats.md)

## 故障排除

如果您由于 3DS 导致无法完成付款，可以通过以下方式排除故障。

1. 重新尝试交易并验证身份。
2. 联系您的银行以确定其端是否存在任何错误。
3. 尝试另一种不需要 3DS 的付款方式。

> [!TIP]
>
> 在尝试完成付款时，请确保在浏览器中允许第三方脚本，并禁用您可能使用的任何广告拦截器。
