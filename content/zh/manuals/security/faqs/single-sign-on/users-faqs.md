---
description: 单点登录用户管理常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on
title: SSO 和用户管理常见问题
linkTitle: 用户管理
tags: [FAQ]
aliases:
- /single-sign-on/users-faqs/
- /faq/security/single-sign-on/users-faqs/
---

### 使用 SSO 时如何管理用户？

您可以通过 Docker Hub 或 Admin Console 中的组织来管理用户。当您在 Docker 中配置 SSO 时，您需要确保您的 IdP 账户中每个用户都有一个账户。当用户第一次使用其域名电子邮件地址登录 Docker 时，他们将在成功身份验证后自动添加到组织中。

### 我需要手动将用户添加到我的组织吗？

不需要，您不需要在 Docker 或 Admin Console 中手动将用户添加到您的组织。您只需要确保您的用户在您的 IdP 中有账户。当用户登录 Docker 时，他们会使用其域名电子邮件地址自动分配到组织。

当用户第一次使用其域名电子邮件地址登录 Docker 时，他们将在成功身份验证后自动添加到组织中。

### 我组织中的用户可以使用不同的电子邮件地址通过 SSO 进行身份验证吗？

在 SSO 设置期间，您需要指定允许进行身份验证的公司电子邮件域名。您组织中的所有用户必须使用 SSO 设置期间指定的电子邮件域名进行身份验证。您的一些用户可能希望为其个人项目维护一个不同的账户。

如果未强制执行 SSO，电子邮件地址与已验证电子邮件域名不匹配的用户可以使用用户名和密码登录，作为访客加入组织。

### Docker 组织和公司所有者可以批准用户加入组织并使用席位，而不是在启用 SSO 时自动添加他们吗？

组织所有者和公司所有者可以通过其 IdP 配置用户权限来批准用户。如果用户账户在 IdP 中配置，只要有可用席位，用户将自动添加到 Docker Hub 中的组织。

### 用户如何得知他们正在被添加到 Docker 组织？

当启用 SSO 时，用户下次尝试登录 Docker Hub 或 Docker Desktop 时将被提示通过 SSO 进行身份验证。系统会看到最终用户尝试进行身份验证的 Docker ID 关联了一个域名电子邮件，并提示他们改用 SSO 电子邮件和凭据登录。

如果用户尝试通过 CLI 登录，他们必须使用个人访问令牌 (PAT) 进行身份验证。

### 是否可以强制 Docker Desktop 用户进行身份验证，和/或使用其公司域名进行身份验证？

是的。管理员可以使用注册表项、`.plist` 文件或 `registry.json` 文件[强制用户使用 Docker Desktop 进行身份验证](../../for-admins/enforce-sign-in/_index.md)。

一旦在 Hub 上为其 Docker Business 组织或公司设置了 SSO 强制执行，当用户被强制使用 Docker Desktop 进行身份验证时，SSO 强制执行还将强制用户通过其 IdP 使用 SSO 进行身份验证（而不是使用其用户名和密码进行身份验证）。

用户仍然可以使用与已验证域名不匹配的电子邮件地址作为访客账户进行身份验证。但是，他们只有在该非域名电子邮件被邀请的情况下才能作为访客进行身份验证。

### 是否可以将现有用户从非 SSO 转换为 SSO 账户？

是的，您可以将现有用户转换为 SSO 账户。要从非 SSO 账户转换用户：

- 确保您的用户拥有公司域名电子邮件地址，并且他们在您的 IdP 中有账户。
- 验证所有用户的机器上都安装了 Docker Desktop 4.4.2 或更高版本。
- 每个用户都创建了 PAT 以替换其密码，以便他们可以通过 Docker CLI 登录。
- 确认所有 CI/CD 管道自动化系统都已用 PAT 替换了其密码。

有关如何启用 SSO 的详细先决条件和说明，请参阅[配置单点登录](../../../security/for-admins/single-sign-on/configure/_index.md)。

### 一旦我们开始将用户迁移到 SSO 账户，用户会有什么影响？

当启用并强制执行 SSO 时，您的用户只需使用已验证的域名电子邮件地址登录即可。

### Docker SSO 是否与 IdP 完全同步？

Docker SSO 默认提供即时 (JIT) 配置，并提供禁用 JIT 的选项。用户在使用 SSO 进行身份验证时进行配置。如果用户离开组织，管理员必须登录 Docker 并手动[从组织中删除用户](../../../admin/organization/members.md#remove-a-member-or-invitee)。

[SCIM](../../../security/for-admins/provisioning/scim/) 可用于提供与用户和组的完全同步。当您使用 SCIM 自动配置用户时，建议的配置是禁用 JIT，以便所有自动配置都由 SCIM 处理。

此外，您可以使用 [Docker Hub API](/reference/api/hub/latest/) 完成此过程。

### 禁用即时配置如何影响用户登录？

当您使用 Admin Console 并启用 SCIM 时，可以使用禁用 JIT 的选项。如果用户尝试使用作为 SSO 连接已验证域名的电子邮件地址登录 Docker，他们需要是组织的成员才能访问，或者有待处理的组织邀请。不满足这些条件的用户将遇到 `Access denied` 错误，需要管理员邀请他们加入组织。

请参阅[禁用 JIT 配置时的 SSO 身份验证](/security/for-admins/provisioning/just-in-time/#sso-authentication-with-jit-provisioning-disabled)。

要在不使用 JIT 配置的情况下自动配置用户，您可以使用 [SCIM](/security/for-admins/provisioning/scim/)。

### 不使用 SSO 配置 Docker 订阅的最佳方式是什么？

公司或组织所有者可以通过 Docker Hub 或 Admin Console 通过电子邮件地址（适用于任何用户）或 Docker ID（假设用户拥有现有的 Docker 账户）邀请用户。

### 某人可以在没有邀请的情况下加入组织吗？是否可以将具有现有电子邮件账户的特定用户添加到组织？

不使用 SSO 则不可以。加入需要组织所有者的邀请。当强制执行 SSO 时，通过 SSO 验证的域名将允许用户在下次作为拥有域名电子邮件的用户登录时自动加入组织。

### 当我们向用户发送邀请时，现有账户会被合并并保留吗？

是的，现有用户账户将加入组织并保留所有资产。

### 如何查看、更新和删除用户的多个电子邮件地址？

我们在 Docker 平台上只支持每个用户一个电子邮件。

### 如何删除尚未登录的组织邀请者？

您可以在 Docker Hub 或 Admin Console 中转到组织的 **Members**（成员）页面，查看待处理的邀请，并根据需要删除邀请者。

### 服务账户身份验证的流程与 UI 用户账户不同吗？

不，我们在产品中不区分这两者。

### 用户信息在 Docker Hub 中是否可见？

所有 Docker 账户都有一个与其命名空间关联的公共配置文件。如果您不希望用户信息（例如全名）可见，您可以从 SSO 和 SCIM 映射中删除这些属性。或者，您可以使用不同的标识符来替换用户的全名。

### 启用 SCIM 后，现有的许可用户会发生什么？

启用 SCIM 不会立即删除或修改 Docker 组织中的现有许可用户。他们保留其当前的访问权限和角色，但在启用 SCIM 后，您将在身份提供商 (IdP) 中管理他们。如果稍后禁用 SCIM，以前由 SCIM 管理的用户将保留在 Docker 中，但不再根据您的 IdP 自动更新或删除。
