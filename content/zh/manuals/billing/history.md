---
title: 查看账单历史
weight: 40
description: 了解如何在 Docker Hub 中查看账单历史
keywords: payments, billing, subscription, invoices, renewals, invoice management, billing administration
aliases:
    - /billing/core-billing/history/
---

在本节中，了解如何查看账单历史、管理发票和验证续订日期。所有月付和年付订阅都会在期限结束时使用原始付款方式自动续订。

{{% include "tax-compliance.md" %}}

## 发票

您的发票包含以下内容：

- 发票编号
- 开具日期
- 到期日期
- 您的"账单寄送"信息
- 应付金额（美元）
- 订单描述、数量（如适用）、单价和金额（美元）

发票 **Bill to** 部分列出的信息基于您的账单信息。并非所有字段都是必填的。账单信息包括以下内容：

- 姓名（必填）：管理员或公司名称
- 电子邮件地址（必填）：接收该账户所有账单相关电子邮件的地址
- 地址（必填）
- 电话号码
- Tax ID 或 VAT

您无法对已付或未付的账单发票进行更改。当您更新账单信息时，此更改不会更新现有发票。如果您需要更新账单信息，请确保在订阅续订日期（发票最终确定时）之前进行更新。有关更多信息，请参阅[更新账单信息](details.md)。

### 查看续订日期

{{< tabs >}}
{{< tab name="Docker subscription" >}}

您会在订阅续订时收到发票。要验证续订日期，请登录 [Docker Billing](https://app.docker.com/billing)。您的续订日期和金额会显示在订阅卡片上。


{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

您会在订阅续订时收到发票。要验证续订日期：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的用户头像以打开下拉菜单。
3. 选择 **Billing**。
4. 选择用户或组织账户以查看账单详情。在这里您可以找到续订日期和续订金额。

{{< /tab >}}
{{< /tabs >}}

### 在发票上包含您的 VAT 号码

> [!NOTE]
>
> 如果 VAT 号码字段不可用，请填写[联系支持表单](https://hub.docker.com/support/contact/)。此字段可能需要手动添加。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要添加或更新您的 VAT 号码：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的
组织。
1. 选择 **Billing**。
1. 从左侧菜单选择 **Billing information**。
1. 在您的账单信息卡片上选择 **Change**。
1. 确保 **I'm purchasing as a business** 复选框已勾选。
1. 在 Tax ID 部分输入您的 VAT 号码。

    > [!IMPORTANT]
    >
    > 您的 VAT 号码必须包含国家前缀。例如，如果您
    输入德国的 VAT 号码，您应输入 `DE123456789`。

1. 选择 **Update**。

您的 VAT 号码将包含在下一张发票中。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要添加或更新您的 VAT 号码：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 选择 **Billing address** 链接。
1. 在 **Billing Information** 部分，选择 **Update information**。
1. 在 Tax ID 部分输入您的 VAT 号码。

    > [!IMPORTANT]
    >
    > 您的 VAT 号码必须包含国家前缀。例如，如果您
    输入德国的 VAT 号码，您应输入 `DE123456789`。

1. 选择 **Save**。

您的 VAT 号码将包含在下一张发票中。

{{< /tab >}}
{{< /tabs >}}

## 查看账单历史

您可以查看个人账户或组织的账单历史并下载过往发票。

### 个人账户

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要查看账单历史：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的
组织。
1. 选择 **Billing**。
1. 从左侧菜单选择 **Invoices**。
1. 可选。选择 **Invoice number** 以打开发票详情。
1. 可选。选择 **Download** 按钮以下载发票。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要查看账单历史：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 选择 **Payment methods and billing history** 链接。

您可以在 **Invoice History** 部分找到过往发票，
并在此下载发票。

{{< /tab >}}
{{< /tabs >}}

### 组织

> [!NOTE]
>
> 您必须是组织所有者才能查看账单历史。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要查看账单历史：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的
组织。
1. 选择 **Billing**。
1. 从左侧菜单选择 **Invoices**。
1. 可选。选择 **invoice number** 以打开发票详情。
1. 可选。选择 **download** 按钮以下载发票。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要查看账单历史：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 选择 **Payment methods and billing history** 链接。

您可以在 **Invoice History** 部分找到过往发票，
并在此下载发票。

{{< /tab >}}
{{< /tabs >}}
