---
title: 创建帐户
weight: 10
description: 了解如何注册 Docker ID 并登录您的帐户
keywords: 帐户, docker ID, 账单, 付费计划, 支持, Hub, Store, 论坛, 知识库, beta 访问, 电子邮件, 激活, 验证
aliases:
- /docker-hub/accounts/
- /docker-id/
---

您可以使用您的电子邮件地址或通过 Google 或 GitHub 帐户注册来创建免费的 Docker 帐户。创建具有唯一 Docker ID 的帐户后，您可以访问所有 Docker 产品，包括 Docker Hub。通过 Docker Hub，您可以访问仓库并探索社区和经过验证的发布者提供的镜像。

您的 Docker ID 将成为您托管 Docker 服务和 [Docker 论坛](https://forums.docker.com/) 的用户名。

> [!TIP]
>
> 探索 [Docker 的订阅](https://www.docker.com/pricing/)，了解 Docker 还能为您提供什么。

## 创建 Docker ID

### 使用您的电子邮件地址注册

1. 转到 [Docker 注册页面](https://app.docker.com/signup/)。

2. 输入一个唯一、有效的电子邮件地址。

3. 输入一个用作您的 Docker ID 的用户名。一旦您创建了 Docker ID，如果您停用此帐户，将来就不能再重复使用它。

    您的用户名：
    - 必须介于 4 到 30 个字符之间
    - 只能包含数字和小写字母

4. 输入至少 9 个字符长的密码。

5. 选择**注册**。

6. 打开您的电子邮件客户端。Docker 会向您提供的地址发送一封验证电子邮件。

7. 验证您的电子邮件地址以完成注册过程。

> [!NOTE]
>
> 您必须验证您的电子邮件地址才能完全访问 Docker 的功能。

### 使用 Google 或 GitHub 注册

> [!IMPORTANT]
>
> 要使用您的社交提供商注册，您必须在开始之前验证您的电子邮件地址。

1. 转到 [Docker 注册页面](https://app.docker.com/signup/)。

2. 选择您的社交提供商，Google 或 GitHub。

3. 选择您要链接到 Docker 帐户的社交帐户。

4. 选择**授权 Docker** 以允许 Docker 访问您的社交帐户信息。您将被重定向到注册页面。

5. 输入一个用作您的 Docker ID 的用户名。

    您的用户名：
    - 必须介于 4 到 30 个字符之间
    - 只能包含数字和小写字母

6. 选择**注册**。

## 登录

注册 Docker ID 并验证您的电子邮件地址后，您可以登录 [您的 Docker 帐户](https://login.docker.com/u/login/)。您可以选择：
- 使用您的电子邮件地址（或用户名）和密码登录。
- 使用您的社交提供商登录。有关更多信息，请参阅 [使用您的社交提供商登录](#sign-in-with-your-social-provider)。
- 使用 `docker login` 命令通过 CLI 登录。有关更多信息，请参阅 [`docker login`](/reference/cli/docker/login.md)。

> [!WARNING]
>
> 当您使用 `docker login` 命令时，您的凭据将存储在您的主目录中的 `.docker/config.json` 中。密码在此文件中进行 base64 编码。
>
> 我们建议使用 [Docker 凭据助手](https://github.com/docker/docker-credential-helpers) 之一来安全存储密码。为了额外的安全性，您还可以使用[个人访问令牌](../security/for-developers/access-tokens.md) 登录，该令牌仍在此文件中编码（没有 Docker 凭据助手），但不允许管理员操作（例如更改密码）。

### 使用您的社交提供商登录

> [!IMPORTANT]
>
> 要使用您的社交提供商登录，您必须在开始之前验证您的电子邮件地址。

您还可以使用您的 Google 或 GitHub 帐户登录您的 Docker 帐户。如果存在与您的社交提供商主电子邮件地址相同的 Docker 帐户，您的 Docker 帐户将自动链接到社交资料。这允许您使用您的社交提供商登录。

如果您尝试使用您的社交提供商登录但尚未拥有 Docker 帐户，则会为您创建一个新帐户。按照屏幕上的说明使用您的社交提供商创建 Docker ID。

## 登录时重置密码

要重置密码，请在 [登录](https://login.docker.com/u/login) 页面输入您的电子邮件地址并继续登录。当提示输入密码时，选择**忘记密码？**。

## 故障排除

如果您有付费的 Docker 订阅，您可以[联系支持团队](https://hub.docker.com/support/contact/)寻求帮助。

所有 Docker 用户都可以通过以下资源寻求故障排除信息和支持，Docker 或社区将尽力回复：
   - [Docker 社区论坛](https://forums.docker.com/)
   - [Docker 社区 Slack](http://dockr.ly/comm-slack)