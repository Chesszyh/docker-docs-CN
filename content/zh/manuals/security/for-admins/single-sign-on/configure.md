---
description: 了解如何为您的组织或公司配置单点登录。
keywords: configure, sso, docker hub, hub, docker admin, admin, security
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

开始为您的组织或公司创建单点登录（SSO）连接。本指南将介绍添加和验证成员用于登录 Docker 的域的步骤。

## 第一步：添加您的域

> [!NOTE]
>
> Docker 支持多个身份提供商（IdP）配置。使用多 IdP 配置时，一个域可以与多个 SSO 身份提供商关联。

{{< tabs >}}
{{< tab name="Admin Console" >}}

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的组织。请注意，当组织属于公司的一部分时，您必须选择公司并在公司级别为组织配置域。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 选择 **Add a domain**。
1. 在文本框中输入您的域，然后选择 **Add domain**。
1. 弹出模态框将提示您验证域的步骤。复制 **TXT Record Value**。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录到 [Docker Hub](https://hub.docker.com/)。
1. 选择 **My Hub**，然后从列表中选择您的组织。
1. 在您的组织页面上，选择 **Settings**，然后选择 **Security**。
1. 选择 **Add a domain**。
1. 在文本框中输入您的域，然后选择 **Add domain**。
1. 弹出模态框将提示您验证域的步骤。复制 **TXT Record Value**。

{{< /tab >}}
{{< /tabs >}}

## 第二步：验证您的域

验证您的域可确保 Docker 知道您拥有该域。要进行验证，您需要使用 Docker 提供的值向您的域名系统（DNS）主机添加一条 TXT 记录。TXT Record Value 证明所有权，这将指示 DNS 添加此记录。DNS 识别更改可能需要长达 72 小时。当更改在 DNS 中反映出来时，Docker 会自动检查记录以确认您的所有权。

使用 Docker 提供的 **TXT Record Value** 并根据您的 DNS 主机按照以下步骤操作。如果您的提供商未列出，请使用其他提供商的说明。

> [!TIP]
>
> 记录名称字段控制 TXT 记录在您的域中应用的位置，例如根域或子域。通常，添加记录名称时请参考以下提示：
>
> - 根据您的提供商，对于 `example.com` 这样的根域，使用 `@` 或将记录名称留空。
> - 不要输入诸如 `docker`、`docker-verification`、`www` 或您的域名等值。这些值可能会指向错误的位置。
>
> 请查看您的 DNS 提供商的文档以验证记录名称要求。

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 要将您的 TXT 记录添加到 AWS，请参阅 [Creating records by using the Amazon Route 53 console](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html)。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，然后选择您的域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 要将您的 TXT 记录添加到 Google Cloud DNS，请参阅 [Verifying your domain with a TXT record](https://cloud.google.com/identity/docs/verify-domain-txt)。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，然后选择您的域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 要将您的 TXT 记录添加到 GoDaddy，请参阅 [Add a TXT record](https://www.godaddy.com/help/add-a-txt-record-19232)。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，然后选择您的域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="Other providers" >}}

1. 登录到您的域主机。
1. 将 TXT 记录添加到您的 DNS 设置并保存记录。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，然后选择您的域名旁边的 **Verify**。

{{< /tab >}}
{{< /tabs >}}

添加并验证您的域后，您就可以在 Docker 和您的身份提供商（IdP）之间创建 SSO 连接了。

## 更多资源

以下视频将引导您完成验证域以在 Docker 中创建 SSO 连接的过程。

- [视频：使用 Okta 验证您的 SSO 域](https://youtu.be/c56YECO4YP4?feature=shared&t=529)
- [视频：使用 Azure AD (OIDC) 验证您的 SSO 域](https://youtu.be/bGquA8qR9jU?feature=shared&t=496)

## 下一步

[连接 Docker 和您的 IdP](../single-sign-on/connect.md)。
