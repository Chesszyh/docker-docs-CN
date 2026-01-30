---
description: 单点登录用户管理常见问题解答
keywords: Docker, Docker Hub, SSO FAQ, 单点登录
title: SSO 和用户管理常见问题 (FAQ)
linkTitle: 用户管理
tags: [FAQ]
aliases:
- /single-sign-on/users-faqs/
- /faq/security/single-sign-on/users-faqs/
---

### 使用 SSO 时，我该如何管理用户？

您可以通过 Docker Hub 或管理控制台 (Admin Console) 中的组织来管理用户。当您在 Docker 中配置 SSO 时，需要确保在您的 IdP 帐户中为每个用户都建立了一个帐户。当用户首次使用其域名电子邮件地址登录 Docker 时，他们在成功身份验证后将自动添加到组织中。

### 我是否需要手动向我的组织添加用户？

不需要，您不需要手动在 Docker 或管理控制台中向组织添加用户。您只需要确保您的用户在 IdP 中已有帐户。当用户登录 Docker 时，他们会使用其域名电子邮件地址自动分配到组织中。

当用户首次使用其域名电子邮件地址登录 Docker 时，他们在成功身份验证后将自动添加到组织中。

### 我组织中的用户能否使用不同的电子邮件地址通过 SSO 进行身份验证？

在 SSO 设置期间，您必须指定允许进行身份验证的公司电子邮件域名。您组织中的所有用户都必须使用 SSO 设置期间指定的电子邮件域名进行身份验证。您的某些用户可能希望为个人项目保留一个不同的帐户。

如果未强制执行 SSO，使用与经验证域名不匹配的电子邮件地址的用户，可以使用用户名和密码登录并以访客 (Guest) 身份加入组织。

### Docker 组织和公司所有者能否先批准用户加入组织并占用席位，而不是在启用 SSO 时让他们自动添加？

组织所有者和公司所有者可以通过其 IdP 配置用户的权限来批准用户。如果在 IdP 中配置了用户帐户，只要有可用席位，该用户就会自动添加到 Docker Hub 中的组织。

### 用户将如何得知他们已被加入 Docker 组织？

启用 SSO 后，用户下次尝试登录 Docker Hub 或 Docker Desktop 时，将被提示通过 SSO 进行身份验证。系统会识别出最终用户具有一个与其尝试身份验证的 Docker ID 关联的域名电子邮件，并提示他们改用 SSO 电子邮件和凭据进行登录。

如果用户尝试通过 CLI 登录，他们必须使用个人访问令牌 (PAT) 进行身份验证。

### 是否可以强制 Docker Desktop 的用户进行身份验证，和/或使用其公司的域名进行身份验证？

可以。管理员可以使用注册表键、`.plist` 文件或 `registry.json` 文件 [强制用户在 Docker Desktop 上进行身份验证](../../for-admins/enforce-sign-in/_index.md)。

一旦在 Hub 上的 Docker Business 组织或公司中设置了 SSO 强制执行，当用户被强制在 Docker Desktop 上进行身份验证时，SSO 强制执行也将强制用户通过其 IdP 进行 SSO 身份验证 (而不是使用用户名和密码进行身份验证)。

用户可能仍然能够使用与经验证域名不匹配的电子邮件地址作为访客帐户进行身份验证。但是，他们只有在受邀的情况下才能以访客身份进行身份验证。

### 是否可以将现有的非 SSO 帐户用户转换为 SSO 帐户？

可以，您可以将现有用户转换为 SSO 帐户。要转换非 SSO 帐户的用户：

- 确保您的用户拥有公司域名电子邮件地址，且在您的 IdP 中已有帐户。
- 验证所有用户的机器上都安装了 Docker Desktop 4.4.2 或更高版本。
- 每个用户都已创建一个 PAT 来代替其密码，以便通过 Docker CLI 登录。
- 确认所有 CI/CD 管道自动化系统已将密码替换为 PAT。

有关详细的前提条件和如何启用 SSO 的说明，请参阅 [配置单点登录 (SSO)](../../../security/for-admins/single-sign-on/configure/_index.md)。

### 开始将用户引导至 SSO 帐户后，用户可以预期受到什么影响？

当 SSO 启用并强制执行后，您的用户只需使用经验证的域名电子邮件地址登录即可。

### Docker SSO 是否与 IdP 完全同步？

Docker SSO 默认提供即时 (Just-in-Time, JIT) 配置，并提供禁用 JIT 的选项。用户在通过 SSO 进行身份验证时被预置。如果用户离开组织，管理员必须登录 Docker 并手动从组织中 [移除该用户](../../../admin/organization/members.md#remove-a-member-or-invitee)。

[SCIM](../../../security/for-admins/provisioning/scim/) 可用于提供与用户和组的完全同步。当您使用 SCIM 自动预置用户时，推荐的配置是禁用 JIT，以便所有自动预置都由 SCIM 处理。

此外，您可以使用 [Docker Hub API](/reference/api/hub/latest/) 来完成此过程。

### 禁用即时 (Just-in-Time) 配置对用户登录有何影响？

当您使用管理控制台并启用 SCIM 时，可以选择禁用 JIT。如果用户尝试使用作为您 SSO 连接的验证域名的电子邮件地址登录 Docker，他们必须是组织的成员或拥有组织的待处理邀请才能访问。不符合这些标准的用户将遇到 `Access denied` (访问被拒绝) 错误，并需要管理员邀请他们加入组织。

参见 [在禁用 JIT 配置的情况下进行 SSO 身份验证](/security/for-admins/provisioning/just-in-time/#sso-authentication-with-jit-provisioning-disabled)。

要在没有 JIT 配置的情况下自动预置用户，您可以使用 [SCIM](/security/for-admins/provisioning/scim/)。

### 在没有 SSO 的情况下，预置 Docker 订阅的最佳方式是什么？

公司或组织所有者可以通过 Docker Hub 或管理控制台，通过电子邮件地址 (针对任何用户) 或 Docker ID (假设用户已有 Docker 帐户) 邀请用户。

### 有人可以在没有邀请的情况下加入组织吗？是否可以将特定用户添加到具有现有电子邮件帐户的组织中？

没有 SSO 的情况下不行。加入需要组织所有者的邀请。当强制执行 SSO 时，通过 SSO 验证的域名将允许用户在下次以分配了域名电子邮件的用户身份登录时自动加入组织。

### 当我们向用户发送邀请时，现有帐户会被合并并保留吗？

是的，现有的用户帐户将加入组织，并保留所有资产。

### 我该如何查看、更新和移除用户的多个电子邮件地址？

我们在 Docker 平台上仅支持每个用户对应一个电子邮件。

### 我该如何移除尚未登录的组织受邀者？

您可以前往 Docker Hub 或管理控制台中的组织 **Members** (成员) 页面，查看待处理的邀请，并根据需要移除受邀者。

### 服务帐户身份验证的流程是否与 UI 用户帐户不同？

不，我们在产品中不对两者进行区分。

### 用户信息在 Docker Hub 中是否可见？

所有的 Docker 帐户都有一个与其命名空间关联的公开个人资料。如果您不希望用户信息 (例如全名) 可见，可以从您的 SSO 和 SCIM 映射中移除这些属性。或者，您可以使用不同的标识符来替换用户的全名。

### 启用 SCIM 时，现有的已授权用户会发生什么？

启用 SCIM 不会立即移除或修改 Docker 组织中现有的已授权用户。他们保留当前的访问权限和角色，但在启用 SCIM 后，您将在身份提供者 (IdP) 中管理他们。如果稍后禁用了 SCIM，先前由 SCIM 管理的用户仍保留在 Docker 中，但不再根据您的 IdP 自动更新或移除。
