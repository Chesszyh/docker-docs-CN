---
description: 了解如何完成单点登录连接，以及启用 SSO 的后续步骤。
keywords: 配置, sso, docker hub, hub, docker admin, admin, security, 安全
title: 创建 SSO 连接
linkTitle: 连接
---

{{< summary-bar feature_name="SSO" >}}

创建单点登录 (SSO) 连接需要先在 Docker 中设置连接，然后在您的身份提供者 (IdP) 中设置连接。本指南提供了在 Docker 和 IdP 中设置 SSO 连接的步骤。

> [!TIP]
>
> 本指南需要在 Docker 和您的 IdP 中复制并粘贴相关值。为了确保连接过程顺畅，请在一次会话中完成本指南中的所有步骤，并分别为 Docker 和您的 IdP 打开独立的浏览器窗口。

## 前提条件

在开始之前，请确保已完成以下操作：

- 您的域名已验证
- 您已经在某个 IdP 中设置了帐户
- 您已经完成了[配置单点登录](../single-sign-on/configure.md)指南中的步骤

## 第一步：在 Docker 中创建 SSO 连接

>[!NOTE]
>
> 在 Docker 中创建 SSO 连接之前，您必须验证至少一个域名。

{{< tabs >}}
{{< tab name="管理控制台 (Admin Console)" >}}

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。注意，当组织是公司的一部分时，您必须选择该公司并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 选择 **Create Connection** 并为连接提供一个名称。
1. 选择身份验证方法：**SAML** 或 **Azure AD (OIDC)**。
1. 复制以下字段以添加到您的 IdP 中：
    - Okta SAML：**Entity ID**、**ACS URL**
    - Azure OIDC：**Redirect URL**
1. 保持此窗口打开，以便您在本指南结束时可以将 IdP 中的连接信息粘贴到此处。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 Docker Hub。
1. 选择 **My Hub**，然后从列表中选择您的组织。
1. 在组织页面上，选择 **Settings**，然后选择 **Security**。
1. 在 SSO 连接表中，选择 **Create Connection** 并为连接提供一个名称。
1. 选择身份验证方法：**SAML** 或 **Azure AD (OIDC)**。
1. 复制以下字段以添加到您的 IdP 中：
    - Okta SAML：**Entity ID**、**ACS URL**
    - Azure OIDC：**Redirect URL**
1. 保持此窗口打开，以便您在本指南结束时可以将 IdP 中的连接信息粘贴到此处。

{{< /tab >}}
{{< /tabs >}}

## 第二步：在您的 IdP 中创建 SSO 连接

您的 IdP 用户界面可能与以下步骤略有不同。请参阅您的 IdP 文档进行核实。

{{< tabs >}}
{{< tab name="Okta SAML" >}}

1. 登录您的 Okta 帐户。
1. 选择 **Admin** 以打开 Okta 管理员门户。
1. 从左侧导航栏中选择 **Administration**。
1. 选择 **Administration** -> **Create App Integration**。
1. 选择 **SAML 2.0**，然后选择 **Next**。
1. 输入 "Docker Hub" 作为您的 **App Name**。
1. （可选）上传图标。
1. 选择 **Next**。
1. 将 Docker 中的以下值输入到相应的 Okta 字段中：
    - Docker ACS URL：**Single Sign On URL**
    - Docker Entity ID：**Audience URI (SP Entity ID)**
1. 在 Okta 中配置以下设置：
    - Name ID format: `EmailAddress`
    - Application username: `Email`
    - Update application on: `Create and update`
1. （可选）添加 SAML 属性。有关 SSO 属性表，请参阅 [SSO 属性](/manuals/security/for-admins/provisioning/_index.md#sso-attributes)。
1. 选择 **Next**。
1. 勾选 **This is an internal app that we have created** 复选框。
1. 选择 **Finish**。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

1. 登录您的 Azure AD 管理员门户。
1. 选择 **默认目录 (Default Directory)**，然后选择 **添加 (Add)**。
1. 选择 **企业应用程序 (Enterprise Application)**，然后选择 **创建你自己的应用程序 (Create your own application)**。
1. 输入 "Docker" 作为应用程序名称，并选择 **非库 (non-gallery)** 选项。
1. 创建应用程序后，转到 **单点登录 (Single Sign-On)** 并选择 **SAML**。
1. 在 **基本 SAML 配置 (Basic SAML configuration)** 部分选择 **编辑 (Edit)**。
1. 将 Docker 中的以下值输入到相应的 Azure 字段中：
    - Docker Entity ID：**标识符 (Identifier)**
    - Docker ACS URL：**回复 URL (Reply URL)**
1. （可选）添加 SAML 属性。有关 SSO 属性表，请参阅 [SSO 属性](/manuals/security/for-admins/provisioning/_index.md#sso-attributes)。
1. 保存配置。
1. 从 **SAML 签名证书 (SAML Signing Certificate)** 部分下载您的 **证书 (Base64) (Certificate (Base64))**。

{{< /tab >}}
{{< tab name="Azure Connect (OIDC)" >}}

要创建 Azure Connect (OIDC) 连接，您必须创建应用注册、客户端密码，并为 Docker 配置 API 权限：

### 创建应用注册

1. 登录您的 Azure AD 管理员门户。
1. 选择 **应用注册 (App Registration)** -> **新注册 (New Registration)**。
1. 输入 "Docker Hub SSO" 或类似的应用程序名称。
1. 在 **支持的帐户类型 (Supported account types)** 下，指定谁可以使用此应用程序或访问此应用。
1. 在 **重定向 URI (Redirect URI)** 部分，从下拉菜单中选择 **Web**，并将 Docker 控制台中的 **Redirect URI** 值粘贴到此字段中。
1. 选择 **注册 (Register)** 以注册应用。
1. 从应用的概览页面复制 **客户端 ID (Client ID)**。您需要此信息来继续在 Docker 中配置 SSO。

### 创建客户端密码

1. 在 Azure AD 中打开您的应用，然后选择 **证书和密码 (Certificates & secrets)**。
1. 选择 **+ 新客户端密码 (+ New client secret)**。
1. 指定密码描述并设置密钥的使用期限。
1. 选择 **添加 (Add)** 继续。
1. 复制机密 **值 (Value)** 字段。您需要此信息来继续在 Docker 中配置 SSO。

### 配置 API 权限

1. 在 Azure AD 中打开您的应用，并导航到应用设置。
1. 选择 **API 权限 (API permission)**，然后选择 **代表 [您的租户名称] 授予管理员同意 (Grant admin consent for [your tenant name])**。
1. 选择 **是 (Yes)** 进行确认。
1. 确认后，选择 **添加权限 (Add a permission)**，然后选择 **委托权限 (Delegated permissions)**。
1. 搜索 `User.Read` 并选择此选项。
1. 选择 **添加权限 (Add permissions)** 进行确认。
1. 通过检查 **状态 (Status)** 列，验证每个权限是否已获得管理员同意。

{{< /tab >}}
{{< /tabs >}}

## 第三步：连接 Docker 和您的 IdP

在 Docker 和您的 IdP 中创建完连接后，您可以对它们进行交叉连接以完成 SSO 连接：

{{< tabs >}}
{{< tab name="Okta SAML" >}}

1. 打开您在 Okta 中创建的应用，选择 **View SAML setup instructions**。
1. 从 Okta SAML 设置说明页面复制以下值：
    - **SAML Sign-in URL**
    - **x509 Certificate**

        > [!IMPORTANT]
        >
        > 您必须复制 **x509 Certificate** 的全部内容，包括 `----BEGIN CERTIFICATE----` 和 `----END CERTIFICATE----` 行。

1. 打开 Docker Hub 或管理控制台（Admin Console）。您的 SSO 配置页面应该仍保持在从本指南第一步开始的状态。
1. 选择 **Next** 以打开 **Update single-sign on connection** 页面。
1. 将 Okta 的 **SAML Sign-in URL** 和 **x509 Certificate** 值粘贴到 Docker 中。
1. 选择 **Next**。
1. （可选）选择一个默认团队用于预配用户，然后选择 **Next**。
1. 核实您的 SSO 连接详情，然后选择 **Create Connection**。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

1. 在 Azure AD 中打开您的应用。
1. 在文本编辑器中打开下载的 **证书 (Base64) (Certificate (Base64))**。
1. 复制以下值：
    - 来自 Azure AD：**登录 URL (Login URL)**
    - 从文本编辑器复制 **证书 (Base64) (Certificate (Base64))** 文件的内容

        > [!IMPORTANT]
        >
        > 您必须复制 **证书 (base64) (Certificate (base64))** 的全部内容，包括 `----BEGIN CERTIFICATE----` 和 `----END CERTIFICATE----` 行。

1. 打开 Docker Hub 或管理控制台（Admin Console）。您的 SSO 配置页面应该仍保持在从本指南第一步开始的状态。
1. 将 **登录 URL (Login URL)** 和 **证书 (Base64) (Certificate (Base64))** 值粘贴到 Docker 中。
1. 选择 **Next**。
1. （可选）选择一个默认团队用于预配用户，然后选择 **Next**。
1. 核实您的 SSO 连接详情，然后选择 **Create Connection**。

{{< /tab >}}
{{< tab name="Azure Connect (OIDC)" >}}

1. 打开 Docker Hub 或管理控制台（Admin Console）。您的 SSO 配置页面应该仍保持在从本指南第一步开始的状态。
1. 将 Azure AD 中的以下值粘贴到 Docker 中：
    - **客户端 ID (Client ID)**
    - **客户端密码 (Client Secret)**
    - **Azure AD 域名 (Azure AD Domain)**
1. 选择 **Next**。
1. （可选）选择一个默认团队用于预配用户，然后选择 **Next**。
1. 核实您的 SSO 连接详情，然后选择 **Create Connection**。

{{< /tab >}}
{{< /tabs >}}

## 第四步：测试您的连接

在 Docker 中完成 SSO 连接过程后，我们建议您对其进行测试：

1. 打开隐身浏览器窗口。
1. 使用您的 **公司域名电子邮件地址** 登录管理控制台（Admin Console）。
1. 浏览器将重定向到您的身份提供者的登录页面进行身份验证。如果您有[多个 IdP](#可选配置多个-idp)，请选择登录选项 **Continue with SSO**。
1. 通过您的公司域名电子邮件而不是使用您的 Docker ID 进行身份验证。

您也可以通过命令行界面 (CLI) 测试您的 SSO 连接。如果您想通过 CLI 进行测试，您的用户必须拥有个人访问令牌 (PAT)。

## 可选：配置多个 IdP

Docker 支持多种 IdP 配置。配置多个 IdP 后，一个域名可以与多个 SSO 身份提供者关联。要配置多个 IdP，请为每个 IdP 重复本指南中的步骤 1-4。确保每个 IdP 配置使用相同的域名。

当用户登录拥有多个 IdP 的 Docker 组织时，在登录页面上，他们必须选择 **Continue with SSO**。这将提示他们选择身份提供者并利用其公司域名电子邮件进行身份验证。

## 可选：强制执行 SSO (Enforce SSO)

> [!IMPORTANT]
>
> 如果不强制执行 SSO，用户可以选择使用 Docker 用户名和密码登录，或者使用 SSO 登录。

强制执行 SSO 要求用户在登录 Docker 时必须使用 SSO。这可以集中身份验证并强制执行由 IdP 设置的策略。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。注意，当组织是公司的一部分时，您必须选择该公司并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 图标，然后选择 **Enable enforcement**。强制执行 SSO 后，您的用户将无法修改其电子邮件地址和密码、无法将用户帐户转换为组织，也无法通过 Docker Hub 设置双重身份验证 (2FA)。如果您想使用 2FA，必须通过您的 IdP 启用 2FA。
1. 按照屏幕上的说明继续操作，并核实您已完成所有任务。
1. 选择 **Turn on enforcement** 以完成设置。

您的用户现在必须使用 SSO 登录 Docker。

> [!NOTE]
>
> 强制执行 SSO 后，[用户无法使用密码访问 Docker CLI](/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced)。用户必须使用[个人访问令牌](/manuals/security/for-admins/access-tokens.md) (PAT) 进行身份验证以访问 Docker CLI。

## 更多资源

以下视频演示了如何强制执行 SSO。

- [视频：使用 Okta SAML 强制执行 SSO](https://youtu.be/c56YECO4YP4?feature=shared&t=1072)
- [视频：使用 Azure AD (OIDC) 强制执行 SSO](https://youtu.be/bGquA8qR9jU?feature=shared&t=1087)


## 下一步

- [预配用户](/manuals/security/for-admins/provisioning/_index.md)
- [强制登录](../enforce-sign-in/_index.md)
- [创建访问令牌](/manuals/security/for-admins/access-tokens.md)
