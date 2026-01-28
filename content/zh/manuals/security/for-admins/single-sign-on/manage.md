---
description: 了解如何管理您的组织或公司的单点登录。
keywords: manage, single sign-on, SSO, sign-on, docker hub, admin console, admin, security
title: 管理单点登录
linkTitle: 管理
aliases:
- /admin/company/settings/sso-management/
- /single-sign-on/manage/
---

{{< summary-bar feature_name="SSO" >}}

## 管理组织

> [!NOTE]
>
> 您必须拥有一个[公司](/admin/company/)才能管理多个组织。

{{% admin-sso-management-orgs product="admin" %}}

## 管理域

{{< tabs >}}
{{< tab name="Admin Console" >}}

{{% admin-sso-management product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-sso-management product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 管理 SSO 连接

{{< tabs >}}
{{< tab name="Admin Console" >}}

{{% admin-sso-management-connections product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-sso-management-connections product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 管理用户

> [!IMPORTANT]
>
> 除非您已[禁用即时配置](/security/for-admins/provisioning/just-in-time/#sso-authentication-with-jit-provisioning-disabled)，否则 SSO 默认启用即时配置（Just-In-Time，JIT）。这意味着您的用户会被自动配置到您的组织。
>
> 您可以按应用单独更改此设置。要防止自动配置用户，您可以在 IdP 中创建一个安全组，并将 SSO 应用配置为仅对该安全组中的用户进行身份验证和授权。请按照您的 IdP 提供的说明操作：
>
> - [Okta](https://help.okta.com/en-us/Content/Topics/Security/policies/configure-app-signon-policies.htm)
> - [Entra ID（原 Azure AD）](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-restrict-your-app-to-a-set-of-users)
>
> 或者，请参阅[配置概述](/manuals/security/for-admins/provisioning/_index.md)指南。


### 在启用 SSO 的情况下添加访客用户

要添加未通过您的 IdP 验证的访客：

1. 登录到 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 选择 **Invite**。
1. 按照屏幕上的说明邀请用户。

### 从 SSO 公司中移除用户

要移除用户：

1. 登录到 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 选择用户名称旁边的操作图标，然后选择 **Remove member**（如果您是组织）或 **Remove user**（如果您是公司）。
1. 按照屏幕上的说明移除用户。

## 管理配置

默认情况下，用户通过即时配置（JIT）进行配置。如果您启用 SCIM，则可以禁用 JIT。有关更多信息，请参阅[配置概述](/manuals/security/for-admins/provisioning/_index.md)指南。

## 下一步

- [设置 SCIM](../provisioning/scim.md)
- [启用组映射](../provisioning/group-mapping.md)
