---
description: 管理员组映射指南
keywords: 组映射, Group Mapping, SCIM, Docker Hub, Docker Admin, 管理, 安全, security
title: 组映射
aliases:
- /admin/company/settings/group-mapping/
- /admin/organization/security-settings/group-mapping/
- /docker-hub/group-mapping/
- /security/for-admins/group-mapping/
weight: 40
---

{{< summary-bar feature_name="SSO" >}}

组映射允许您将身份提供者（IdP）中的用户组与 Docker 组织中的团队（Team）同步。这实现了团队成员管理的自动化，让您的 Docker 团队根据 IdP 中的更改保持最新。您可以在配置完 [单点登录 (SSO)](../single-sign-on/_index.md) 后使用组映射。

> [!TIP]
>
> 组映射非常适合将用户添加到多个组织或一个组织内的多个团队。如果您不需要设置多组织或多团队分配，可以使用 SCIM [用户级属性](scim.md#set-up-role-mapping)。

## 组映射的工作原理

启用组映射后，当用户通过 SSO 进行身份验证时，您的 IdP 会与 Docker 共享关键属性，如用户的电子邮件地址、姓名和组。Docker 使用这些属性来创建或更新用户资料，并管理他们的团队和组织分配。通过组映射，用户在 Docker 中的团队成员身份将自动反映您的 IdP 组中所做的更改。

需要注意的是，Docker 使用用户的电子邮件地址作为唯一标识符。每个 Docker 帐户必须始终拥有唯一的电子邮件地址。

## 使用组映射

要通过 IdP 将用户分配到 Docker 团队，您必须在 IdP 中按照 `organization:team` 命名模式创建组。例如，如果您的组织名为 "moby"，并且您想要管理 "developers" 团队，则 IdP 中的组名应为 `moby:developers`。在此示例中，任何添加到 IdP 中该组的用户都会自动分配到 Docker 中的 "developers" 团队。

您还可以使用此格式将用户分配到多个组织。例如，要将用户添加到 "moby" 组织中的 "backend" 团队和 "whale" 组织中的 "desktop" 团队，组名将分别为 `moby:backend` 和 `whale:desktop`。

> [!TIP]
>
> 请确保 IdP 中的组名与您的 Docker 团队名称匹配。同步组时，如果团队尚不存在，Docker 会自动创建一个。

下表列出了支持的组映射属性：

| 属性 | 描述 |
|:--------- | :---------- |
| id | 组在 UUID 格式下的唯一 ID。此属性为只读。 |
| displayName | 遵循组映射格式的组名：`organization:team`。 |
| members | 该组成员的用户列表。 |
| members(x).value | 该组成员用户的唯一 ID。成员通过 ID 进行引用。 |

使用组映射的一般步骤如下：

1. 在您的 IdP 中，以 `organization:team` 格式创建组。
2. 将用户添加到组中。
3. 将您在 IdP 中创建的 Docker 应用程序添加到组中。
4. 在 IdP 中添加属性。
5. 将组推送到 Docker。

具体配置可能因您的 IdP 而异。您可以[配合 SSO 使用组映射](#配合-sso-使用组映射)，或者在[启用 SCIM](#配合-scim-使用组映射) 的情况下配合 SSO 使用。

### 配合 SSO 使用组映射

以下步骤描述了如何在使用 SAML 身份验证方法的 SSO 连接中设置和使用组映射。请注意，Azure AD (OIDC) 身份验证方法不支持配合 SSO 使用组映射。此外，这些配置不需要 SCIM。

{{< tabs >}}
{{< tab name="Okta" >}}

您的 IdP 用户界面可能与以下步骤略有不同。您可以参考 [Okta 文档](https://help.okta.com/oie/en-us/content/topics/apps/define-group-attribute-statements.htm)进行核实。

设置组映射：

1. 登录 Okta 并打开您的应用程序。
2. 导航到应用程序的 **SAML Settings** 页面。
3. 在 **Group Attribute Statements (optional)** 部分，进行如下配置：
   - **Name**: `groups`
   - **Name format**: `Unspecified`
   - **Filter**: `Starts with` + `organization:`（其中 `organization` 是您的组织名称）
   过滤选项将过滤掉与您的 Docker 组织无关的组。
4. 通过选择 **Directory** -> **Groups** 来创建您的组。
5. 使用 `organization:team` 格式添加您的组，确保其与 Docker 中的组织名和团队名匹配。
6. 将用户分配到您创建的组。

下次您将组与 Docker 同步时，您的用户将映射到您定义的 Docker 组。

{{< /tab >}}
{{< tab name="Entra ID" >}}

您的 IdP 用户界面可能与以下步骤略有不同。您可以参考 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes)进行核实。

设置组映射：

1. 登录 Entra ID 并打开您的应用程序。
2. 选择 **管理 (Manage)** -> **单点登录 (Single sign-on)**。
3. 选择 **添加组声明 (Add a group claim)**。
4. 在“组声明”部分，选择 **分配给应用程序的组 (Groups assigned to the application)**，源属性选择 **仅限云的组显示名称 (预览) (Cloud-only group display names (Preview))**。
5. 选择 **高级选项 (Advanced options)**，然后选择 **过滤组 (Filter groups)** 选项。
6. 按如下方式配置属性：
   - **要匹配的属性 (Attribute to match)**：`Display name`
   - **匹配方式 (Match with)**：`Contains`
   - **字符串 (String)**：`:`
7. 选择 **保存 (Save)**。
8. 选择 **组 (Groups)** -> **所有组 (All groups)** -> **新建组 (New group)** 来创建您的组。
9. 将用户分配到您创建的组。

下次您将组与 Docker 同步时，您的用户将映射到您定义的 Docker 组。

{{< /tab >}}
{{< /tabs >}}

### 配合 SCIM 使用组映射

以下步骤描述了如何设置和使用配合 SCIM 的组映射。在开始之前，请确保您已先[设置 SCIM](./scim.md#enable-scim)。

{{< tabs >}}
{{< tab name="Okta" >}}

您的 IdP 用户界面可能与以下步骤略有不同。您可以参考 [Okta 文档](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm)进行核实。

设置您的组：

1. 登录 Okta 并打开您的应用程序。
2. 选择 **Applications** -> **Provisioning** -> **Integration**。
3. 选择 **Edit** 以在连接上启用组，然后选择 **Push groups**。
4. 选择 **Save**。保存此配置将在您的应用程序中添加 **Push Groups** 选项卡。
5. 导航到 **Directory** 并选择 **Groups** 来创建您的组。
6. 使用 `organization:team` 格式添加您的组，确保其与 Docker 中的组织名和团队名匹配。
7. 将用户分配到您创建的组。
8. 返回 **Integration** 页面，然后选择 **Push Groups** 选项卡，打开可以控制和管理如何预配组的视图。
9. 选择 **Push Groups** -> **Find groups by rule**。
10. 按如下方式配置规则：
    - 输入规则名称，例如 `Sync groups with Docker Hub`
    - 按名称匹配组，例如以 `docker:` 开头，或者对于多组织情况包含 `:`
    - 如果您启用 **Immediately push groups by rule**，则只要组或组分配发生更改，就会立即进行同步。如果您不想手动推送组，请启用此项。

在 **Pushed Groups** 列的 **By rule** 下找到您的新规则。匹配该规则的组将列在右侧的组表中。

要从该表中推送组：

1. 选择 **Group in Okta**。
2. 选择 **Push Status** 下拉菜单。
3. 选择 **Push Now**。

{{< /tab >}}
{{< tab name="Entra ID" >}}

您的 IdP 用户界面可能与以下步骤略有不同。您可以参考 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes)进行核实。

在配置组映射之前，请完成以下操作：

1. 登录 Entra ID 并转到您的应用程序。
2. 在应用程序中，选择 **预配 (Provisioning)** -> **映射 (Mappings)**。
3. 选择 **预配 Microsoft Entra ID 组 (Provision Microsoft Entra ID Groups)**。
4. 选择 **显示高级选项 (Show advanced options)** -> **编辑属性列表 (Edit attribute list)**。
5. 将 `externalId` 类型更新为 `reference`，然后勾选 **多值 (Multi-Value)** 复选框，并选择引用的对象属性 `urn:ietf:params:scim:schemas:core:2.0:Group`。
6. 选择 **保存 (Save)** -> **是 (Yes)** 进行确认。
7. 转到 **预配 (Provisioning)**。
8. 将 **预配状态 (Provision Status)** 切换为 **开启 (On)**，然后选择 **保存 (Save)**。

接下来，设置组映射：

1. 转到应用程序概览页面。
2. 在 **预配用户帐户 (Provision user accounts)** 下，选择 **开始 (Get started)**。
3. 选择 **添加用户/组 (Add user/group)**。
4. 使用 `organization:team` 格式创建您的组。
5. 将组分配给预配组。
6. 选择 **开始预配 (Start provisioning)** 以开始同步。

要验证同步情况，请选择 **监控 (Monitor)** -> **预配日志 (Provisioning logs)**，查看您的组是否已成功预配。在您的 Docker 组织中，您可以检查组是否已正确预配，以及成员是否已添加到相应的团队中。

{{< /tab >}}
{{< /tabs >}}

完成后，通过 SSO 登录 Docker 的用户将自动添加到 IdP 中映射的组织和团队中。

> [!TIP]
>
> [启用 SCIM](scim.md) 以利用自动用户预配和去预配功能。如果您不启用 SCIM，用户仅会被自动预配。您必须手动对他们进行去预配（移除）。

## 更多资源

以下视频演示了如何在启用 SCIM 的情况下配合您的 IdP 使用组映射：

- [视频：Okta 组映射](https://youtu.be/c56YECO4YP4?feature=shared&t=3023)
- [视频：Entra ID (Azure) 属性和组映射](https://youtu.be/bGquA8qR9jU?feature=shared&t=2039)
