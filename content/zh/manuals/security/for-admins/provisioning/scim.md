---
keywords: SCIM, SSO, 用户预配, 去预配, 角色映射, 分配用户, user provisioning, de-provisioning, role mapping, assign users
title: SCIM 预配
linkTitle: SCIM
description: 了解跨域身份管理系统的工作原理以及如何进行设置。
aliases:
  - /security/for-admins/scim/
  - /docker-hub/scim/
weight: 30
---

{{< summary-bar feature_name="SSO" >}}

跨域身份管理系统 (System for Cross-domain Identity Management, SCIM) 可供 Docker Business 客户使用。本指南概述了 SCIM 预配。

## SCIM 的工作原理

SCIM 通过您的身份提供者 (IdP) 自动执行 Docker 的用户预配和去预配（de-provisioning）。启用 SCIM 后，IdP 中分配给您的 Docker 应用程序的任何用户都将被自动预配并添加到您的 Docker 组织中。当用户在 IdP 的 Docker 应用程序中被移除时，SCIM 会停用该用户并将其从您的 Docker 组织中移除。

除了预配和移除外，SCIM 还会同步 IdP 中所做的资料更新（例如姓名更改）。您可以将 SCIM 与 Docker 默认的即时 (JIT) 预配结合使用，也可以在禁用 JIT 的情况下单独使用。

SCIM 自动执行：

- 创建用户
- 更新用户资料
- 移除和停用用户
- 重新激活用户
- 组映射

> [!NOTE]
>
> SCIM 仅管理启用 SCIM 后通过 IdP 预配的用户。它无法移除在设置 SCIM 之前手动添加到 Docker 组织中的用户。
>
> 要移除这些用户，请在您的 Docker 组织中手动删除他们。有关更多信息，请参阅[管理组织成员](/manuals/admin/organization/members.md)。

## 支持的属性

SCIM 使用属性（例如姓名、电子邮件）在您的 IdP 和 Docker 之间同步用户信息。在 IdP 中正确映射这些属性可确保用户预配顺利进行，并防止在使用单点登录 (SSO) 时出现重复用户帐户等问题。

Docker 支持以下 SCIM 属性：

| 属性 | 描述 |
|:---------------------------------------------------------------|:-------------------------------------------------------------------------------------------|
| userName             | 用户的主要电子邮件地址，用作唯一标识符 |
| name.givenName | 用户的名字 (First name) |
| name.familyName | 用户的姓氏 (Surname) |
| active | 指示用户是启用还是禁用，设置为 “false” 以去预配用户 |

有关支持的属性和 SCIM 的更多详细信息，请参阅 [Docker Hub API SCIM 参考](/reference/api/hub/latest/#tag/scim)。

> [!IMPORTANT]
>
> 默认情况下，Docker 对 SSO 使用即时 (JIT) 预配。如果启用了 SCIM，JIT 值仍具有优先级，并且会覆盖由 SCIM 设置的属性值。为避免冲突，请确保您的 JIT 属性值与 SCIM 值匹配。
>
> 或者，您可以禁用 JIT 预配以完全依赖 SCIM。有关详情，请参阅[即时预配](/manuals/security/for-admins/provisioning/just-in-time.md)。

## 前提条件

- 您已在 Docker 中[设置了 SSO](/manuals/security/for-admins/single-sign-on/_index.md) 并验证了域名。
- 您拥有身份提供者管理员门户的访问权限，并具有创建和管理应用程序的权限。

## 在 Docker 中启用 SCIM

在启用 SCIM 之前，您必须先[配置 SSO](../single-sign-on/configure/_index.md)。使用 SCIM 并不强制要求强制执行 SSO。

{{< tabs >}}
{{< tab name="管理控制台 (Admin Console)" >}}

{{% admin-scim product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-scim %}}

{{< /tab >}}
{{< /tabs >}}

## 在您的 IdP 中启用 SCIM

您的 IdP 用户界面可能与以下步骤略有不同。您可以参考 IdP 的文档进行核实。有关更多详细信息，请参阅您的 IdP 文档：

- [Okta](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_SCIM.htm)
- [Entra ID/Azure AD SAML 2.0](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/user-provisioning)

> [!NOTE]
>
> Microsoft 目前不支持在 Entra ID 的同一个非库（non-gallery）应用程序中同时使用 SCIM 和 OIDC。本指南提供了一个经过验证的解决方法，即使用一个单独的非库应用来进行 SCIM 预配。虽然 Microsoft 没有正式记录这种设置，但它在实践中被广泛使用并得到支持。

{{< tabs >}}
{{< tab name="Okta" >}}

### 第一步：启用 SCIM

1. 登录 Okta 并选择 **Admin** 以打开管理员门户。
1. 打开您在配置 SSO 连接时创建的应用程序。
1. 在应用程序页面上，选择 **General** 选项卡，然后选择 **Edit App Settings**。
1. 启用 SCIM 预配，然后选择 **Save**。
1. 现在您可以访问 Okta 中的 **Provisioning** 选项卡。导航到此选项卡，然后选择 **Edit SCIM Connection**。
1. 要在 Okta 中配置 SCIM，请使用以下值和设置设置您的连接：
    - SCIM Base URL：SCIM 连接器基 URL（从 Docker Hub 复制）
    - Unique identifier field for users：`email`
    - Supported provisioning actions：**Push New Users** 和 **Push Profile Updates**
    - Authentication Mode：HTTP Header
    - SCIM Bearer Token：HTTP Header Authorization Bearer Token（从 Docker Hub 复制）
1. 选择 **Test Connector Configuration**。
1. 查看测试结果并选择 **Save**。

### 第二步：启用同步

1. 在 Okta 中，选择 **Provisioning**。
1. 选择 **To App**，然后选择 **Edit**。
1. 启用 **Create Users**、**Update User Attributes** 和 **Deactivate Users**。
1. 选择 **Save**。
1. 移除不必要的映射。必要的映射包括：
    - Username
    - Given name
    - Family name
    - Email

{{< /tab >}}
{{< tab name="Entra ID (OIDC)" >}}

Microsoft 不支持在同一个非库应用程序中同时使用 SCIM 和 OIDC。您必须在 Entra ID 中创建第二个非库应用程序用于 SCIM 预配。

### 第一步：创建一个单独的 SCIM 应用

1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **企业应用程序 (Enterprise Applications)** > **新建应用程序 (New application)**。
1. 选择 **创建你自己的应用程序 (Create your own application)**。
1. 为您的应用程序命名，并选择 **集成你在库中找不到的任何其他应用程序 (Integrate any other application you don't find in the gallery)**。
1. 选择 **创建 (Create)**。

### 第二步：配置 SCIM 预配

1. 在您的新 SCIM 应用程序中，转到 **预配 (Provisioning)** > **开始 (Get started)**。
1. 将 **预配模式 (Provisioning Mode)** 设置为 **自动 (Automatic)**。
1. 在 **管理员凭据 (Admin Credentials)** 下：
    - **租户 URL (Tenant URL)**：粘贴来自 Docker 的 **SCIM Base URL**。
    - **机密令牌 (Secret Token)**：粘贴来自 Docker 的 **SCIM API token**。
1. 选择 **测试连接 (Test Connection)** 进行验证。
1. 选择 **保存 (Save)** 以存储凭据。

接下来，[设置角色映射](#设置角色映射)。

{{< /tab >}}
{{< tab name="Entra ID (SAML 2.0)" >}}

### 配置 SCIM 预配

1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **企业应用程序 (Enterprise Applications)**，然后选择您的 Docker SAML 应用。
1. 选择 **预配 (Provisioning)** > **开始 (Get started)**。
1. 将 **预配模式 (Provisioning Mode)** 设置为 **自动 (Automatic)**。
1. 在 **管理员凭据 (Admin Credentials)** 下：
    - **租户 URL (Tenant URL)**：粘贴来自 Docker 的 **SCIM Base URL**。
    - **机密令牌 (Secret Token)**：粘贴来自 Docker 的 **SCIM API token**。
1. 选择 **测试连接 (Test Connection)** 进行验证。
1. 选择 **保存 (Save)** 以存储凭据。

接下来，[设置角色映射](#设置角色映射)。

{{< /tab >}}
{{< /tabs >}}

## 设置角色映射

您可以通过在 IdP 中添加可选的 SCIM 属性来向用户分配 [Docker 角色](/security/for-admins/roles-and-permissions/)。这些属性将覆盖您的 SSO 配置中设置的默认角色和团队值。

> [!NOTE]
>
> SCIM 和即时 (JIT) 预配都支持角色映射。对于 JIT，角色映射仅在用户首次预配时应用。

下表列出了支持的可选用户级属性：

| 属性 | 可能的值 | 备注 |
| --------- | ------------------ | -------------- |
| `dockerRole` | `member`、`editor` 或 `owner` | 如果未设置，用户默认为 `member` 角色。设置此属性会覆盖默认值。<br><br>有关角色定义，请参阅[角色和权限](manuals/security/for-admins/roles-and-permissions.md)。 |
| `dockerOrg` | Docker `organizationName` (例如 `moby`) | 覆盖 SSO 连接中配置的默认组织。<br><br>如果未设置，用户将被预配到默认组织。如果同时设置了 `dockerOrg` 和 `dockerTeam`，则用户将被预配到指定组织内的团队。 |
| `dockerTeam` | Docker `teamName` (例如 `developers`) | 将用户预配到默认组织或指定组织中的指定团队。如果团队不存在，它将被自动创建。<br><br>您仍然可以使用[组映射](/security/for-admins/provisioning/group-mapping/)将用户分配到跨组织的多个团队。 |

这些属性使用的外部命名空间为：`urn:ietf:params:scim:schemas:extension:docker:2.0:User`。在您的 IdP 中为 Docker 创建自定义 SCIM 属性时需要此值。

{{< tabs >}}
{{< tab name="Okta" >}}

### 第一步：在 Okta 中设置角色映射

1. 首先设置 [SSO](../single-sign-on/configure/_index.md) 和 SCIM。
1. 在 Okta 管理门户中，转到 **Directory**，选择 **Profile Editor**，然后选择 **User (Default)**。
1. 选择 **Add Attribute**，并为您想要添加的角色、组织或团队配置值。不需要完全一致的命名。
1. 返回 **Profile Editor** 并选择您的应用程序。
1. 选择 **Add Attribute** 并输入所需的值。**External Name** 和 **External Namespace** 必须完全准确。组织/团队/角色映射的外部名称值分别为 `dockerOrg`、`dockerTeam` 和 `dockerRole`（如前表所列）。所有这些的外部命名空间都是相同的：`urn:ietf:params:scim:schemas:extension:docker:2.0:User`。
1. 创建属性后，导航到页面顶部并选择 **Mappings**，然后选择 **Okta User to YOUR APP**。
1. 转到新创建的属性，将变量名映射到外部名称，然后选择 **Save Mappings**。如果您正在使用 JIT 预配，请继续以下步骤。
1. 导航到 **Applications** 并选择 **YOUR APP**。
1. 选择 **General** -> **SAML Settings** -> **Edit**。
1. 选择 **Step 2** 并配置从用户属性到 Docker 变量的映射。

### 第二步：按用户分配角色

1. 在 Okta 管理门户中，选择 **Directory** -> **People**。
1. 选择 **Profile** -> **Edit**。
1. 选择 **Attributes** 并将属性更新为所需的值。

### 第三步：按组分配角色

1. 在 Okta 管理门户中，选择 **Directory** -> **People**。
1. 选择 **YOUR GROUP** -> **Applications**。
1. 打开 **YOUR APPLICATION** 并选择 **Edit** 图标。
1. 将属性更新为所需的值。

如果用户尚未设置属性，则被添加到该组的用户在预配时将继承这些属性。

{{< /tab >}}
{{< tab name="Entra ID/Azure AD (SAML 2.0 和 OIDC)" >}}

### 第一步：配置属性映射

1. 完成 [SCIM 预配设置](#在-docker-中启用-scim)。
1. 在 Azure 门户中，打开 **Microsoft Entra ID** > **企业应用程序 (Enterprise Applications)**，然后选择您的 SCIM 应用程序。
1. 转到 **预配 (Provisioning)** > **映射 (Mappings)** > **预配 Azure Active Directory 用户 (Provision Azure Active Directory Users)**。
1. 添加或更新以下映射：
    - `userPrincipalName` -> `userName`
    - `mail` -> `emails.value`
    - （可选）使用[映射方法](#第二步选择角色映射方法)之一映射 `dockerRole`、`dockerOrg` 或 `dockerTeam`。
1. 移除任何不受支持的属性，以防止同步错误。
1. （可选）转到 **映射 (Mappings)** > **预配 Azure Active Directory 组 (Provision Azure Active Directory Groups)**：
    - 如果组预配导致错误，请将 **已启用 (Enabled)** 设置为 **否 (No)**。
    - 如果启用，请仔细测试组映射。
1. 选择 **保存 (Save)** 以应用映射。

### 第二步：选择角色映射方法

您可以使用以下方法之一映射 `dockerRole`、`dockerOrg` 或 `dockerTeam`：

#### 表达式映射 (Expression mapping)

如果您只需要分配 `member`、`editor` 或 `owner` 等 Docker 角色，请使用此方法。

1. 在 **编辑属性 (Edit Attribute)** 视图中，将映射类型设置为 **表达式 (Expression)**。
2. 在 **表达式 (Expression)** 字段中：
    1. 如果您的应用角色（App Role）与 Docker 角色完全匹配，请使用：`SingleAppRoleAssignment([appRoleAssignments])`
    2. 如果不匹配，请使用 switch 表达式：`Switch(SingleAppRoleAssignment([appRoleAssignments]), "My Corp Admins", "owner", "My Corp Editors", "editor", "My Corp Users", "member")`
1. 设置：
    - **目标属性 (Target attribute)**：`urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
    - **使用此属性匹配对象 (Match objects using this attribute)**：否 (No)
    - **应用此映射 (Apply this mapping)**：始终 (Always)
1. 保存更改。

> [!WARNING]
>
> 您不能通过此方法使用 `dockerOrg` 或 `dockerTeam`。表达式映射仅与一个属性兼容。

#### 直接映射 (Direct mapping)

如果您需要映射多个属性（例如 `dockerRole` + `dockerTeam`），请使用此方法。

1. 对于每个 Docker 属性，选择一个唯一的 Entra 扩展属性（例如 `extensionAttribute1`、`extensionAttribute2` 等）。
1. 在 **编辑属性 (Edit Attribute)** 视图中：
    - 将映射类型设置为 **直接 (Direct)**。
    - 将 **源属性 (Source attribute)** 设置为您选择的扩展属性（例如 `extensionAttribute1`）。
    - 将 **目标属性 (Target attribute)** 设置为以下之一：
        - `dockerRole: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
        - `dockerOrg: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerOrg`
        - `dockerTeam: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerTeam`
    - 将 **应用此映射 (Apply this mapping)** 设置为 **始终 (Always)**。
1. 保存更改。

要分配值，您需要使用 Microsoft Graph API。

### 第三步：分配用户和组

对于任何一种映射方法：

1. 在 SCIM 应用中，转到 **用户和组 (Users and Groups)** > **添加用户/组 (Add user/group)**。
1. 选择要预配到 Docker 的用户或组。
1. 选择 **分配 (Assign)**。

如果您使用的是表达式映射：

1. 转到 **应用注册 (App registrations)** > 您的 SCIM 应用 > **应用角色 (App Roles)**。
1. 创建与 Docker 角色匹配的应用角色。
1. 在 **用户和组 (Users and Groups)** 下将用户或组分配给应用角色。

如果您使用的是直接映射：

1. 转到 [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) 并以租户管理员身份登录。
1. 使用 Microsoft Graph API 分配属性值。PATCH 请求示例：

```bash
PATCH https://graph.microsoft.com/v1.0/users/{user-id}
Content-Type: application/json

{
  "extensionAttribute1": "owner",
  "extensionAttribute2": "moby",
  "extensionAttribute3": "developers"
}
```

> [!NOTE]
>
> 必须为每个 SCIM 字段使用不同的扩展属性。

{{< /tab >}}
{{< /tabs >}}

有关更多详细信息，请参阅您的 IdP 文档：

- [Okta](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-add-custom-user-attributes.htm)
- [Entra ID/Azure AD](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes#provisioning-a-custom-extension-attribute-to-a-scim-compliant-application)

## 测试 SCIM 预配

完成角色映射后，您可以手动测试配置。


{{< tabs >}}
{{< tab name="Okta" >}}

1. 在 Okta 管理门户中，转到 **Directory > People**。
1. 选择分配给您的 SCIM 应用程序的用户。
1. 选择 **Provision User**。
1. 等待几秒钟，然后检查 Docker [管理控制台 (Admin Console)](https://app.docker.com/admin) 的 **Members** 下。
1. 如果用户未出现，请在 **Reports > System Log** 中查看日志，并确认应用中的 SCIM 设置。

{{< /tab >}}
{{< tab name="Entra ID/Azure AD (OIDC 和 SAML 2.0)" >}}

1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **企业应用程序 (Enterprise Applications)**，然后选择您的 SCIM 应用。
1. 转到 **预配 (Provisioning)** > **按需预配 (Provision on demand)**。
1. 选择一个用户或组，然后选择 **预配 (Provision)**。
1. 确认该用户出现在 Docker [管理控制台 (Admin Console)](https://app.docker.com/admin) 的 **Members** 下。
1. 如果需要，请检查 **预配日志 (Provisioning logs)** 以获取错误信息。

{{< /tab >}}
{{< /tabs >}}

## 禁用 SCIM

如果禁用了 SCIM，任何通过 SCIM 预配的用户都将保留在组织中。用户的未来更改将不再从您的 IdP 同步。只有通过手动从组织中移除用户才能实现用户去预配。

{{< tabs >}}
{{< tab name="管理控制台 (Admin Console)" >}}

{{% admin-scim-disable product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-scim-disable %}}

{{< /tab >}}
{{< /tabs >}}

## 更多资源

以下视频演示了如何为您的 IdP 配置 SCIM：

- [视频：使用 Okta 配置 SCIM](https://youtu.be/c56YECO4YP4?feature=shared&t=1314)
- [视频：使用 Okta 进行属性映射](https://youtu.be/c56YECO4YP4?feature=shared&t=1998)
- [视频：使用 Entra ID/Azure AD 配置 SCIM](https://youtu.be/bGquA8qR9jU?feature=shared&t=1668)
- [视频：使用 Entra ID/Azure AD 进行属性和组映射](https://youtu.be/bGquA8qR9jU?feature=shared&t=2039)

如果需要，请参考以下故障排除指南：

- [排查预配故障](/manuals/security/troubleshoot/troubleshoot-provisioning.md)
