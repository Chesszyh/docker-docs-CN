---
description: 了解如何为您的组织或公司配置单点登录。
keywords: 配置, sso, docker hub, hub, docker admin, admin, security, 安全
title: 配置单点登录
linkTitle: 配置
aliases:
  - /docker-hub/domains/
  - /docker-hub/sso-connection/
  - /docker-hub/enforcing-sso/
  - /single-sign-on/configure/
  - /admin/company/settings/sso-configuration/
  - /admin/organization/security-settings/sso-configuration/
---

{{< summary-bar feature_name="SSO" >}}

开始为您的组织或公司创建单点登录 (SSO) 连接。本指南将引导您完成添加和验证成员用于登录 Docker 的域名的步骤。

## 第一步：添加您的域名

> [!NOTE]
>
> Docker 支持多种身份提供者 (IdP) 配置。在多 IdP 配置下，一个域名可以与多个 SSO 身份提供者关联。

{{< tabs >}}
{{< tab name="管理控制台 (Admin Console)" >}}

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。注意，当组织是公司的一部分时，您必须选择该公司并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 选择 **Add a domain**。
1. 在文本框中输入您的域名，然后选择 **Add domain**。
1. 弹出窗口将提示您验证域名的步骤。复制 **TXT Record Value（TXT 记录值）**。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com/)。
1. 选择 **My Hub**，然后从列表中选择您的组织。
1. 在组织页面上，选择 **Settings**，然后选择 **Security**。
1. 选择 **Add a domain**。
1. 在文本框中输入您的域名，然后选择 **Add domain**。
1. 弹出窗口将提示您验证域名的步骤。复制 **TXT Record Value（TXT 记录值）**。

{{< /tab >}}
{{< /tabs >}}

## 第二步：验证您的域名

验证域名可确保 Docker 知道您拥有该域名。为了进行验证，您需要使用 Docker 提供的值向您的域名系统 (DNS) 托管商添加一条 TXT 记录。TXT 记录值证明了所有权，这向 DNS 发出信号以添加此记录。DNS 识别更改最多可能需要 72 小时。当更改反映在 DNS 中时，Docker 会自动检查该记录以确认您的所有权。

使用 Docker 提供的 **TXT Record Value**，并按照您的 DNS 托管商的步骤操作。如果您的提供商未列出，请使用其他提供商的说明。

> [!TIP]
>
> 记录名称（Record name）字段控制 TXT 记录在您的域名中的应用位置，例如根域名或子域名。通常，请参考以下添加记录名称的建议：
>
> - 根据您的提供商，对于像 `example.com` 这样的根域名，请使用 `@` 或保持记录名称为空。
> - 不要输入像 `docker`、`docker-verification`、`www` 或您的域名之类的值。这些值可能会导致指向错误的位置。
>
> 请查看您的 DNS 提供商的文档以核实记录名称的要求。

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 要向 AWS 添加 TXT 记录，请参阅[使用 Amazon Route 53 控制台创建记录](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html)。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台 (Admin Console)](https://app.docker.com/admin) 的 **Domain management** 页面，并选择域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 要向 Google Cloud DNS 添加 TXT 记录，请参阅[使用 TXT 记录验证您的域名](https://cloud.google.com/identity/docs/verify-domain-txt)。
1. TXT record TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台 (Admin Console)](https://app.docker.com/admin) 的 **Domain management** 页面，并选择域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 要向 GoDaddy 添加 TXT 记录，请参阅[添加 TXT 记录](https://www.godaddy.com/help/add-a-txt-record-19232)。
1. TXT record TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台 (Admin Console)](https://app.docker.com/admin) 的 **Domain management** 页面，并选择域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="其他提供商" >}}

1. 登录您的域名托管商后台。
1. 在 DNS 设置中添加一条 TXT 记录并保存记录。
1. TXT record TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台 (Admin Console)](https://app.docker.com/admin) 的 **Domain management** 页面，并选择域名旁边的 **Verify**。

{{< /tab >}}
{{< /tabs >}}

添加并验证域名后，您就可以在 Docker 和您的身份提供者 (IdP) 之间创建 SSO 连接了。

## 更多资源

以下视频演示了如何验证您的域名以在 Docker 中创建 SSO 连接。

- [视频：为 Okta SSO 验证您的域名](https://youtu.be/c56YECO4YP4?feature=shared&t=529)
- [视频：为 Azure AD (OIDC) SSO 验证您的域名](https://youtu.be/bGquA8qR9jU?feature=shared&t=496)

## 下一步

[连接 Docker 和您的 IdP](../single-sign-on/connect.md)。
