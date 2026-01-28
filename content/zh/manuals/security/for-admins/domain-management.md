---
description: 了解如何在管理控制台中管理域名和用户
keywords: domain management, security, identify users, manage users
title: 域名管理
weight: 55
---

{{< summary-bar feature_name="Domain management" >}}

域名管理（Domain management）允许您添加和验证域名，并为用户启用自动配置（auto-provisioning）。当用户使用与已验证域名匹配的电子邮件地址登录时，自动配置会将用户添加到您的组织。

这简化了用户管理，确保一致的安全设置，并降低了未受管用户在没有可见性或控制的情况下访问 Docker 的风险。

## 添加域名

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 选择 **Add a domain**。
1. 输入您的域名并选择 **Add domain**。
1. 在弹出的模态框中，复制 **TXT Record Value** 以验证您的域名。

## 验证域名

验证域名可确认您拥有该域名。要进行验证，请使用 Docker 提供的值将 TXT 记录添加到您的域名系统（DNS）主机。该值用于证明所有权并指示您的 DNS 发布该记录。

DNS 更改可能需要最多 72 小时才能生效。一旦识别到更改，Docker 会自动检查记录并确认所有权。

请按照您的 DNS 提供商的文档添加 **TXT Record Value**。如果您的提供商未在下面列出，请使用其他提供商的步骤。

> [!TIP]
>
> 记录名称字段决定 TXT 记录在您的域名中添加的位置（根域名或子域名）。通常，添加记录名称时请参考以下提示：
>
> - 对于 `example.com` 等根域名，根据您的提供商，使用 `@` 或将记录名称留空。
> - 不要输入 `docker`、`docker-verification`、`www` 或您的域名等值。这些值可能会指向错误的位置。
>
> 请查阅您的 DNS 提供商文档以验证记录名称要求。

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 要将 TXT 记录添加到 AWS，请参阅 [Creating records by using the Amazon Route 53 console](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html)。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回[管理控制台](https://app.docker.com/admin)的 **Domain management** 页面，在您的域名旁边选择 **Verify**。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 要将 TXT 记录添加到 Google Cloud DNS，请参阅 [Verifying your domain with a TXT record](https://cloud.google.com/identity/docs/verify-domain-txt)。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回[管理控制台](https://app.docker.com/admin)的 **Domain management** 页面，在您的域名旁边选择 **Verify**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 要将 TXT 记录添加到 GoDaddy，请参阅 [Add a TXT record](https://www.godaddy.com/help/add-a-txt-record-19232)。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回[管理控制台](https://app.docker.com/admin)的 **Domain management** 页面，在您的域名旁边选择 **Verify**。

{{< /tab >}}
{{< tab name="Other providers" >}}

1. 登录您的域名主机。
1. 将 TXT 记录添加到您的 DNS 设置并保存记录。
1. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证完成后，返回[管理控制台](https://app.docker.com/admin)的 **Domain management** 页面，在您的域名旁边选择 **Verify**。

{{< /tab >}}
{{< /tabs >}}

## 删除域名

删除域名会移除已分配的 TXT 记录值。要删除域名：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 对于要删除的域名，选择 **Actions** 菜单，然后选择 **Delete domain**。
1. 要确认，请在弹出的模态框中选择 **Delete domain**。

## 自动配置

您必须先添加并验证域名，然后才能启用自动配置。这可以确认您的组织拥有该域名。一旦域名通过验证，Docker 可以自动将匹配的用户与您的组织关联。自动配置不需要 SSO 连接。

> [!IMPORTANT]
>
> 对于属于 SSO 连接的域名，即时配置（Just-in-Time，JIT）会覆盖自动配置来将用户添加到组织。

### 工作原理

当为已验证的域名启用自动配置后，下次用户使用与您已验证域名关联的电子邮件地址登录 Docker 时，他们会自动被添加到您的组织。自动配置不会为新用户创建账户，它会将现有的未关联用户添加到您的组织。用户*不会*体验到任何登录或用户体验方面的变化。

当新用户被自动配置时，公司和组织所有者将收到电子邮件通知，告知有新用户已添加到其组织。如果您需要为组织添加更多席位以容纳新用户，请参阅[管理席位](/manuals/subscription/manage-seats.md)。

### 启用自动配置

自动配置按用户启用。要启用自动配置：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 在要为其启用自动配置的用户旁边选择 **Actions menu**。
1. 选择 **Enable auto-provisioning**。
1. 可选。如果在公司级别启用自动配置，请为用户选择一个组织。
1. 选择 **Enable** 确认。

**Auto-provisioning** 列将更新为 **Enabled**。

### 禁用自动配置

要为用户禁用自动配置：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 在您的用户旁边选择 **Actions menu**。
1. 选择 **Disable auto-provisioning**。
1. 选择 **Disable**。
