---
description: 了解如何排查常见的 SSO 问题。
keywords: sso, troubleshoot, single sign-on
title: 单点登录故障排除
linkTitle: SSO 故障排除
tags: [Troubleshooting]
toc_max: 2
aliases:
    - "/security/for-admins/single-sign-on/troubleshoot/"
---

在配置或使用单点登录（Single Sign-On，SSO）时，您可能会遇到源自身份提供商（Identity Provider，IdP）或 Docker 配置的问题。以下部分描述了一些常见的 SSO 错误及可能的解决方案。

## 检查错误

如果您遇到 SSO 问题，请首先检查 Docker Admin Console 和您的身份提供商（IdP）中的错误。

### 检查 Docker 错误日志

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **View error logs**。
1. 要获取特定错误的更多详细信息，请选择错误消息旁边的 **View error details**。
1. 记录您在此页面上看到的任何错误，以便进一步排查。

### 检查 IdP 中的错误

1. 查看您的 IdP 的日志或审计跟踪，了解任何失败的身份验证或配置尝试。
2. 确认您的 IdP 的 SSO 设置与 Docker 中提供的值匹配。
3. 如果适用，确认您已正确配置用户配置并在 IdP 中启用了它。
4. 如果适用，验证您的 IdP 是否正确映射了 Docker 所需的用户属性。
5. 尝试从您的 IdP 配置一个测试用户，并验证他们是否出现在 Docker 中。

如需进一步排查，请查阅您的 IdP 文档。您也可以联系他们的支持团队以获取有关错误消息的指导。

## 群组格式不正确

### 错误消息

当发生此问题时，常见的错误消息如下：
```text
Some of the groups assigned to the user are not formatted as '<organization name>:<team name>'. Directory groups will be ignored and user will be provisioned into the default organization and team.
```

### 可能的原因

- 您的身份提供商（IdP）中的群组名称格式不正确：Docker 要求群组遵循 `<organization>:<team>` 格式。如果分配给用户的群组不遵循此格式，它们将被忽略。
- IdP 和 Docker 组织之间的群组不匹配：如果您的 IdP 中的群组在 Docker 中没有对应的团队，它将不会被识别，用户将被放置在默认组织和团队中。

### 受影响的环境

- 使用 Okta 或 Azure AD 等 IdP 的 Docker 单点登录设置
- 在 Docker 中使用基于群组的角色分配的组织

### 复现步骤

要复现此问题：
1. 尝试使用 SSO 登录 Docker。
2. 用户在 IdP 中被分配了群组，但没有被放置在预期的 Docker 团队中。
3. 查看 Docker 日志或 IdP 日志以查找错误消息。

### 解决方案

在您的 IdP 中更新群组名称：
1. 转到您的 IdP 的群组管理部分。
2. 检查分配给受影响用户的群组。
3. 确保每个群组遵循所需的格式：`<organization>:<team>`
4. 更新任何格式不正确的群组以匹配此模式。
5. 保存更改并重试使用 SSO 登录。

## 用户未分配到组织

### 错误消息

当发生此问题时，常见的错误消息如下：
```text
User '$username' is not assigned to this SSO organization. Contact your administrator. TraceID: XXXXXXXXXXXXX
```

### 可能的原因

- 用户未分配到组织：如果即时配置（Just-in-Time，JIT）已禁用，用户可能未被分配到您的组织。
- 用户未被邀请到组织：如果 JIT 已禁用且您不想启用它，必须手动邀请用户。
- SCIM 配置错误：如果您使用 SCIM 进行用户配置，它可能未能正确从您的 IdP 同步用户。

### 解决方案

**启用 JIT 配置**

当您启用 SSO 时，JIT 默认启用。如果您已禁用 JIT 并需要重新启用：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **Enable JIT provisioning**。
1. 选择 **Enable** 确认。

**手动邀请用户**

当 JIT 禁用时，用户在通过 SSO 进行身份验证时不会自动添加到您的组织。
要手动邀请用户，请参阅[邀请成员](/manuals/admin/organization/members.md#invite-members)

**配置 SCIM 配置**

如果您启用了 SCIM，请使用以下步骤排查您的 SCIM 连接：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **View error logs**。要获取特定错误的更多详细信息，请选择错误消息旁边的 **View error details**。记录您在此页面上看到的任何错误。
1. 返回 Admin Console 的 **SSO and SCIM** 页面并验证您的 SCIM 配置：
    - 确保您的 IdP 中的 SCIM Base URL 和 API Token 与 Docker Admin Console 中提供的匹配。
    - 验证 SCIM 在 Docker 和您的 IdP 中都已启用。
1. 确保从您的 IdP 同步的属性与 Docker 的 SCIM [支持的属性](/manuals/security/for-admins/provisioning/scim.md#supported-attributes)匹配。
1. 通过尝试从您的 IdP 配置一个测试用户来测试用户配置，并验证他们是否出现在 Docker 中。

## IdP 发起的登录未为连接启用

### 错误消息

当发生此问题时，常见的错误消息如下：
```text
IdP-Initiated sign in is not enabled for connection '$ssoConnection'.
```

### 可能的原因

Docker 不支持 IdP 发起的 SAML 流程。当用户尝试从您的 IdP 进行身份验证时会发生此错误，例如在登录页面上使用 Docker SSO 应用图标。

### 解决方案

**从 Docker 应用进行身份验证**

用户必须从 Docker 应用（Hub、Desktop 等）发起身份验证。用户需要在 Docker 应用中输入其电子邮件地址，然后将被重定向到为其域配置的 SSO IdP。

**隐藏 Docker SSO 应用**

您可以在 IdP 中对用户隐藏 Docker SSO 应用。这可以防止用户尝试从 IdP 仪表板发起身份验证。您必须在 IdP 中隐藏和配置此项。

## 组织中没有足够的席位

### 错误消息

当发生此问题时，常见的错误消息如下：
```text
Not enough seats in organization '$orgName'. Add more seats or contact your administrator.
```

### 可能的原因

当通过即时配置（JIT）或 SCIM 配置用户时，组织没有可用的席位给用户，就会发生此错误。

### 解决方案

**为组织添加更多席位**

购买额外的 Docker Business 订阅席位。有关详细信息，请参阅[管理订阅席位](/manuals/subscription/manage-seats.md)。

**移除用户或待处理的邀请**

查看您的组织成员和待处理的邀请。移除不活跃的用户或待处理的邀请以释放席位。更多详细信息，请参阅[管理组织成员](/manuals/admin/organization/members.md)。

## 域未为 SSO 连接验证

### 错误消息

当发生此问题时，常见的错误消息如下：
```text
Domain '$emailDomain' is not verified for your SSO connection. Contact your company administrator. TraceID: XXXXXXXXXXXXXX
```

### 可能的原因

如果 IdP 通过 SSO 对用户进行了身份验证，但返回给 Docker 的用户主体名称（User Principal Name，UPN）与 Docker 中配置的 SSO 连接关联的任何已验证域都不匹配，就会发生此错误。

### 解决方案

**验证 UPN 属性映射**

确保 IdP SSO 连接在断言属性中返回正确的 UPN 值。

**添加并验证所有域**

添加并验证您的 IdP 用作 UPN 的所有域和子域，并将它们与您的 Docker SSO 连接关联。有关详细信息，请参阅[配置单点登录](/manuals/security/for-admins/single-sign-on/configure.md)。

## 无法找到会话

### 错误消息

当发生此问题时，常见的错误消息如下：
```text
We couldn't find your session. You may have pressed the back button, refreshed the page, opened too many sign-in dialogs, or there is some issue with cookies. Try signing in again. If the issue persists, contact your administrator.
```

### 可能的原因

以下原因可能导致此问题：
- 用户在身份验证期间按了后退或刷新按钮。
- 身份验证流程丢失了对初始请求的跟踪，导致无法完成。

### 解决方案

**不要中断身份验证流程**

登录期间不要按后退或刷新按钮。

**重新开始身份验证**

关闭浏览器标签页，从 Docker 应用（Desktop、Hub 等）重新开始身份验证流程。

## Name ID 不是电子邮件地址

### 错误消息

当发生此问题时，常见的错误消息如下：
```text
The name ID sent by the identity provider is not an email address. Contact your company administrator.
```

### 可能的原因

以下原因可能导致此问题：
- IdP 发送的 Name ID（UPN）不符合 Docker 要求的电子邮件格式。
- Docker SSO 要求 Name ID 是用户的主要电子邮件地址。

### 解决方案

在您的 IdP 中，确保 Name ID 属性格式正确：
1. 验证您的 IdP 中的 Name ID 属性格式设置为 `EmailAddress`。
2. 调整您的 IdP 设置以返回正确的 Name ID 格式。
