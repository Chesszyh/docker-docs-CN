---
description: 了解如何为您的组织或公司管理单点登录。
keywords: 管理, 单点登录, SSO, 登录, docker hub, 管理控制台, admin console, admin, security, 安全
title: 管理单点登录
linkTitle: 管理
aliases:
- /admin/company/settings/sso-management/
- /single-sign-on/manage/
---

{{< summary-bar feature_name="SSO" >}}

## 管理组织 (Manage organizations)

> [!NOTE]
>
> 您必须拥有一个[公司 (Company)](/admin/company/) 才能管理多个组织。

{{% admin-sso-management-orgs product="admin" %}}

## 管理域名 (Manage domains)

{{< tabs >}}
{{< tab name="管理控制台 (Admin Console)" >}}

{{% admin-sso-management product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-sso-management product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 管理 SSO 连接 (Manage SSO connections)

{{< tabs >}}
{{< tab name="管理控制台 (Admin Console)" >}}

{{% admin-sso-management-connections product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-sso-management-connections product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 管理用户 (Manage users)

> [!IMPORTANT]
>
> 默认情况下，SSO 已启用即时 (JIT) 预配，除非您已[将其禁用](/security/for-admins/provisioning/just-in-time/#sso-authentication-with-jit-provisioning-disabled)。这意味着您的用户会自动预配到您的组织中。
>
> 您可以根据每个应用的情况更改此设置。为了防止自动预配用户，您可以在 IdP 中创建一个安全组，并配置 SSO 应用仅对该安全组中的用户进行身份验证和授权。请按照您的 IdP 提供的说明操作：
>
> - [Okta](https://help.okta.com/en-us/Content/Topics/Security/policies/configure-app-signon-policies.htm)
> - [Entra ID (原 Azure AD)](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-restrict-your-app-to-a-set-of-users)
>
> 或者，请参阅[预配概览](/manuals/security/for-admins/provisioning/_index.md)指南。


### SSO 启用时添加访客用户 (Add guest users when SSO is enabled)

要添加未通过 IdP 验证的访客：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 选择 **Invite**。
1. 按照屏幕上的说明邀请用户。

### 从 SSO 公司中移除用户 (Remove users from the SSO company)

要移除用户：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**。
1. 选择用户姓名旁边的操作图标，如果您是组织，请选择 **Remove member**；如果您是公司，请选择 **Remove user**。
1. 按照屏幕上的说明移除用户。

## 管理预配 (Manage provisioning)

默认情况下，用户是通过即时 (JIT) 预配进行预配的。如果您启用了 SCIM，则可以禁用 JIT。有关更多信息，请参阅[预配概览](/manuals/security/for-admins/provisioning/_index.md)指南。

## 下一步

- [设置 SCIM](../provisioning/scim.md)
- [启用组映射](../provisioning/group-mapping.md)
