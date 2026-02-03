---
description: 了解如何排查常见的 SSO 问题。
keywords: sso, troubleshoot, single sign-on, 单点登录, 排查
title: 排查单点登录故障
linkTitle: 排查 SSO 故障
tags: [Troubleshooting]
toc_max: 2
aliases:
    - "/security/for-admins/single-sign-on/troubleshoot/"
---

在配置或使用单点登录 (SSO) 时，您可能会遇到由身份提供者 (IdP) 或 Docker 配置引起的问题。以下部分描述了一些常见的 SSO 错误及其可能的解决方案。

## 检查错误

如果您遇到 SSO 问题，请先在 Docker 管理控制台和您的身份提供者 (IdP) 中检查错误。

### 检查 Docker 错误日志

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console（管理控制台）**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action（操作）** 菜单，然后选择 **View error logs（查看错误日志）**。
1. 要查看特定错误的更多详情，请选择错误消息旁边的 **View error details（查看错误详情）**。
1. 记下此页面上看到的任何错误，以便进一步排查。

### 在您的 IdP 中检查错误

1. 查看您的 IdP 日志或审计轨迹，了解任何失败的身份验证或预配尝试。
2. 确认您的 IdP 的 SSO 设置与 Docker 中提供的值匹配。
3. （如果适用）确认您已正确配置用户预配，并且已在您的 IdP 中启用。
4. （如果适用）验证您的 IdP 是否正确映射了 Docker 所需的用户属性。
5. 尝试从您的 IdP 预配一个测试用户，并验证他们是否出现在 Docker 中。

如需进一步排查，请查看您的 IdP 文档。您也可以联系其支持团队获取有关错误消息的指导。

## 组格式不正确 (Groups are not formatted correctly)

### 错误信息

发生此问题时，通常会出现以下错误信息：
```text
Some of the groups assigned to the user are not formatted as '<organization name>:<team name>'. Directory groups will be ignored and user will be provisioned into the default organization and team.
```

### 可能的原因

- 身份提供者 (IdP) 中的组名格式不正确：Docker 要求组遵循 `<organization>:<team>` 格式。如果分配给用户的组不符合此格式，它们将被忽略。
- IdP 组与 Docker 组织团队不匹配：如果您的 IdP 中的某个组在 Docker 中没有对应的团队，它将不被识别，用户将被放入默认的组织和团队中。

### 受影响的环境

- 使用 Okta 或 Azure AD 等 IdP 设置的 Docker 单点登录
- 在 Docker 中使用基于组的角色分配的组织

### 复现步骤

复现此问题：
1. 尝试使用 SSO 登录 Docker。
2. 用户在 IdP 中被分配了组，但没有进入预期的 Docker 团队。
3. 查看 Docker 日志或 IdP 日志以找到错误信息。

### 解决方案

更新您 IdP 中的组名：
1. 转到您的 IdP 的组管理部分。
2. 检查分配给受影响用户的组。
3. 确保每个组都遵循要求的格式：`<organization>:<team>`
4. 更新任何格式不正确的组以符合此模式。
5. 保存更改并重试使用 SSO 登录。

## 用户未分配到组织 (User is not assigned to the organization)

### 错误信息

发生此问题时，通常会出现以下错误信息：
```text
User '$username' is not assigned to this SSO organization. Contact your administrator. TraceID: XXXXXXXXXXXXX
```

### 可能的原因

- 用户未分配到组织：如果禁用了即时 (JIT) 预配，用户可能未被分配到您的组织。
- 用户未受邀加入组织：如果禁用了 JIT 且您不想启用它，则必须手动邀请用户。
- SCIM 预配配置错误：如果您使用 SCIM 进行用户预配，它可能没有正确地从您的 IdP 同步用户。

### 解决方案

**启用 JIT 预配**

启用 SSO 时，JIT 默认处于开启状态。如果您禁用了 JIT 并且需要重新启用：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console（管理控制台）**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action（操作）** 菜单，然后选择 **Enable JIT provisioning（启用 JIT 预配）**。
1. 选择 **Enable（启用）** 进行确认。

**手动邀请用户**

禁用 JIT 后，用户在通过 SSO 进行身份验证时不会被自动添加到您的组织中。
要手动邀请用户，请参阅[邀请成员](/manuals/admin/organization/members.md#invite-members)

**配置 SCIM 预配**

如果您启用了 SCIM，请按照以下步骤排查您的 SCIM 连接：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console（管理控制台）**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action（操作）** 菜单，然后选择 **View error logs（查看错误日志）**。要查看特定错误的更多详情，请选择错误消息旁边的 **View error details（查看错误详情）**。记下您在此页面上看到的任何错误。
1. 导航回管理控制台的 **SSO and SCIM** 页面，并验证您的 SCIM 配置：
    - 确保您的 IdP 中的 SCIM 基 URL (Base URL) 和 API 令牌 (API Token) 与 Docker 管理控制台中提供的匹配。
    - 验证 Docker 和您的 IdP 中是否都启用了 SCIM。
1. 确保从您的 IdP 同步的属性与 Docker 针对 SCIM [支持的属性](/manuals/security/for-admins/provisioning/scim.md#supported-attributes)匹配。
1. 通过您的 IdP 尝试预配一个测试用户来测试用户预配，并验证他们是否出现在 Docker 中。

## 连接未启用 IdP 发起的登录 (IdP-initiated sign in is not enabled for connection)

### 错误信息

发生此问题时，通常会出现以下错误信息：
```text
IdP-Initiated sign in is not enabled for connection '$ssoConnection'.
```

### 可能的原因

Docker 不支持 IdP 发起的 SAML 流程。当用户尝试从您的 IdP 发起身份验证时（例如使用登录页面上的 Docker SSO 应用磁贴），会发生此错误。

### 解决方案

**从 Docker 应用进行身份验证**

用户必须从 Docker 应用程序（Hub、Desktop 等）发起身份验证。用户需要在 Docker 应用中输入他们的电子邮件地址，他们将被重定向到为其域名配置的 SSO IdP。

**隐藏 Docker SSO 应用**

您可以在 IdP 中对用户隐藏 Docker SSO 应用。这可以防止用户尝试从 IdP 控制面板开始身份验证。您必须在您的 IdP 中进行此项隐藏和配置。

## 组织中的席位不足 (Not enough seats in organization)

### 错误信息

发生此问题时，通常会出现以下错误信息：
```text
Not enough seats in organization '$orgName'. Add more seats or contact your administrator.
```

### 可能的原因

当通过即时 (JIT) 预配或 SCIM 进行预配时，如果组织没有可用的席位给该用户，就会发生此错误。

### 解决方案

**为组织增加更多席位**

购买额外的 Docker Business 订阅席位。有关详情，请参阅[管理订阅席位](/manuals/subscription/manage-seats.md)。

**移除用户或待处理的邀请**

查看您的组织成员和待处理的邀请。移除不活跃的用户或待处理的邀请以腾出席位。有关更多详情，请参阅[管理组织成员](/manuals/admin/organization/members.md)。

## 域名未针对 SSO 连接进行验证 (Domain is not verified for SSO connection)

### 错误信息

发生此问题时，通常会出现以下错误信息：
```text
Domain '$emailDomain' is not verified for your SSO connection. Contact your company administrator. TraceID: XXXXXXXXXXXXXX
```

### 可能的原因

如果 IdP 通过 SSO 对用户进行了身份验证，且返回给 Docker 的用户主要名称 (UPN) 与 Docker 中配置的 SSO 连接所关联的任何已验证域名都不匹配，就会发生此错误。

### 解决方案

**验证 UPN 属性映射**

确保 IdP SSO 连接在断言属性中返回了正确的 UPN 值。

**添加并验证所有域名**

添加并验证您的 IdP 用作 UPN 的所有域名和子域名，并将它们与您的 Docker SSO 连接关联。有关详情，请参阅[配置单点登录](/manuals/security/for-admins/single-sign-on/configure.md)。

## 无法找到会话 (Unable to find session)

### 错误信息

发生此问题时，通常会出现以下错误信息：
```text
We couldn't find your session. You may have pressed the back button, refreshed the page, opened too many sign-in dialogs, or there is some issue with cookies. Try signing in again. If the issue persists, contact your administrator.
```

### 可能的原因

以下原因可能会导致此问题：
- 用户在身份验证期间按了后退或刷新按钮。
- 身份验证流程失去了对初始请求的跟踪，导致无法完成。

### 解决方案

**不要中断身份验证流程**

登录期间请勿按后退或刷新按钮。

**重新启动身份验证**

关闭浏览器选项卡，并从 Docker 应用程序（Desktop、Hub 等）重新启动身份验证流程。

## 名字 ID 不是电子邮件地址 (Name ID is not an email address)

### 错误信息

发生此问题时，通常会出现以下错误信息：
```text
The name ID sent by the identity provider is not an email address. Contact your company administrator.
```

### 可能的原因

以下原因可能会导致此问题：
- IdP 发送的名称 ID (UPN) 不符合 Docker 要求的电子邮件格式。
- Docker SSO 要求名称 ID 必须是用户的主要电子邮件地址。

### 解决方案

在您的 IdP 中，确保名称 ID 属性格式正确：
1. 验证您的 IdP 中的名称 ID 属性格式是否设置为 `EmailAddress`。
2. 调整您的 IdP 设置以返回正确的名称 ID 格式。
