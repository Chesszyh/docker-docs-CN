---
title: 查看账单历史
weight: 40
description: 了解如何在 Docker Hub 中查看账单历史
keywords: 付款, 账单, 订阅, 发票, 续订, 发票管理, 账单管理
---

在本节中，学习如何查看您的账单历史、管理发票以及核实您的续订日期。所有月度和年度订阅都会在期限结束时使用原始付款方式自动续订。

{{% include "tax-compliance.md" %}}

## 发票

您的发票包括以下内容：

- 发票号码
- 签发日期
- 截止日期
- 您的“付款人”信息
- 应付金额（美元）
- 您的订单描述、数量（如果适用）、单价和金额（美元）

发票中 **Bill to**（付款人）部分列出的信息基于您的账单信息。并非所有字段都是必填的。账单信息包括以下内容：

- 姓名/名称（必填）：管理员或公司的名称
- 电子邮件地址（必填）：接收该账户所有账单相关邮件的电子邮件地址
- 地址（必填）
- 电话号码
- 税务 ID 或增值税 (VAT)

您不能对已付或未付的账单发票进行更改。当您更新账单信息时，此更改不会更新现有的发票。如果您需要更新账单信息，请确保在发票最终确定的订阅续订日期之前完成。有关更多信息，请参阅 [更新账单信息](details.md)。

### 查看续订日期

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

您将在订阅续订时收到发票。要核实您的续订日期，请登录 [Docker Billing](https://app.docker.com/billing)。您的续订日期和金额将显示在您的订阅卡片上。


{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

您将在订阅续订时收到发票。要核实您的续订日期：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的用户头像以打开下拉菜单。
3. 选择 **Billing**（账单）。
4. 选择用户或组织账户以查看账单详情。在这里您可以找到续订日期和续订金额。

{{< /tab >}}
{{< /tabs >}}

### 在发票中包含您的 VAT 号码

> [!NOTE]
>
> 如果增值税 (VAT) 号码字段不可用，请填写 [联系支持表单](https://hub.docker.com/support/contact/)。该字段可能需要手动添加。

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

添加或更新您的 VAT 号码：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Billing information**（账单信息）。
4. 在您的账单信息卡片上选择 **Change**（更改）。
5. 确保勾选了 **I'm purchasing as a business**（我作为企业购买）复选框。
6. 在税务 ID 部分输入您的 VAT 号码。

    > [!IMPORTANT]
    >
    > 您的增值税 (VAT) 号码必须包含国家前缀。例如，如果您输入德国的 VAT 号码，应输入 `DE123456789`。

7. 选择 **Update**（更新）。

您的 VAT 号码将包含在您的下一张发票中。

{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

添加或更新您的 VAT 号码：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Billing address**（账单地址）链接。
4. 在 **Billing Information**（账单信息）部分，选择 **Update information**（更新信息）。
5. 在税务 ID 部分输入您的 VAT 号码。

    > [!IMPORTANT]
    >
    > 您的增值税 (VAT) 号码必须包含国家前缀。例如，如果您输入德国的 VAT 号码，应输入 `DE123456789`。

6. 选择 **Save**（保存）。

您的 VAT 号码将包含在您的下一张发票中。

{{< /tab >}}
{{< /tabs >}}

## 查看账单历史

您可以查看个人账户或组织的账单历史并下载过往发票。

### 个人账户

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

查看账单历史的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Invoices**（发票）。
4. 可选：选择 **Invoice number**（发票号码）以打开发票详情。
5. 可选：选择 **Download**（下载）按钮以下载发票。

{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

查看账单历史的步骤：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Payment methods and billing history**（付款方式和账单历史）链接。

您可以在 **Invoice History**（发票历史）部分找到您过往的发票，并在那里下载发票。

{{< /tab >}}
{{< /tabs >}}

### 组织

> [!NOTE]
>
> 您必须是组织的所有者才能查看账单历史。

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

查看账单历史的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Invoices**（发票）。
4. 可选：选择 **invoice number**（发票号码）以打开发票详情。
5. 可选：选择 **download**（下载）按钮以下载发票。

{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

查看账单历史的步骤：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Payment methods and billing history**（付款方式和账单历史）链接。

您可以在 **Invoice History**（发票历史）部分找到您过往的发票，并在那里下载发票。

{{< /tab >}}
{{< /tabs >}}
