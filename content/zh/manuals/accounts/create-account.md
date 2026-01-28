---
title: 创建账户
weight: 10
description: 了解如何注册 Docker ID 并登录您的账户
keywords: 账户, docker ID, 账单, 付费计划, 支持, Hub, Store, 论坛, 知识库, beta 访问, 电子邮件, 激活, 验证
aliases:
- /docker-hub/accounts/
- /docker-id/
---

您可以使用您的电子邮件地址或通过使用您的 Google 或 GitHub 账户注册来创建一个免费的 Docker 账户。一旦您使用唯一的 Docker ID 创建了账户，您就可以访问所有 Docker 产品，包括 Docker Hub。通过 Docker Hub，您可以访问存储库并探索来自社区和经过验证的发布者的镜像。

您的 Docker ID 将成为您在托管的 Docker 服务以及 [Docker 论坛](https://forums.docker.com/) 上的用户名。

> [!TIP]
>
> 探索 [Docker 的订阅计划](https://www.docker.com/pricing/)，看看 Docker 还能为您提供什么。

## 创建 Docker ID

### 使用电子邮件地址注册

1. 前往 [Docker 注册页面](https://app.docker.com/signup/)。

2. 输入一个唯一且有效的电子邮件地址。

3. 输入一个用户名作为您的 Docker ID。一旦您创建了 Docker ID，如果您停用此账户，将来将无法再次使用它。

    您的用户名：
    - 必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母

4. 输入一个至少 9 个字符长的密码。

5. 选择 **Sign Up**（注册）。

6. 打开您的电子邮件客户端。Docker 会向您提供的地址发送一封验证邮件。

7. 验证您的电子邮件地址以完成注册过程。

> [!NOTE]
>
> 在获得 Docker 功能的全部访问权限之前，您必须先验证您的电子邮件地址。

### 使用 Google 或 GitHub 注册

> [!IMPORTANT]
>
> 要使用社交提供商注册，您必须在开始之前先在提供商处验证您的电子邮件地址。

1. 前往 [Docker 注册页面](https://app.docker.com/signup/)。

2. 选择您的社交提供商，Google 或 GitHub。

3. 选择您想要链接到 Docker 账户的社交账户。

4. 选择 **Authorize Docker**（授权 Docker）以允许 Docker 访问您的社交账户信息。您将被重新引导至注册页面。

5. 输入一个用户名作为您的 Docker ID。

    您的用户名：
    - 必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母

6. 选择 **Sign up**（注册）。

## 登录

一旦您注册了 Docker ID 并验证了电子邮件地址，您就可以登录 [您的 Docker 账户](https://login.docker.com/u/login/)。您可以：
- 使用您的电子邮件地址（或用户名）和密码登录。
- 使用您的社交提供商登录。有关更多信息，请参阅 [使用社交提供商登录](#sign-in-with-your-social-provider)。
- 通过 CLI 使用 `docker login` 命令登录。有关更多信息，请参阅 [`docker login`](/reference/cli/docker/login.md)。

> [!WARNING]
>
> 当您使用 `docker login` 命令时，您的凭据存储在主目录的 `.docker/config.json` 中。密码在该文件中以 base64 编码。
>
> 我们建议使用 [Docker 凭据助手](https://github.com/docker/docker-credential-helpers) 之一来安全存储密码。为了额外的安全性，您还可以使用 [个人访问令牌](../security/for-developers/access-tokens.md) 来登录，它仍然会在该文件中编码（如果没有 Docker 凭据助手），但不允许管理员操作（例如更改密码）。

### 使用社交提供商登录

> [!IMPORTANT]
>
> 要使用社交提供商登录，您必须在开始之前先在提供商处验证您的电子邮件地址。

您还可以使用 Google 或 GitHub 账户登录您的 Docker 账户。如果存在一个 Docker 账户，其电子邮件地址与您的社交提供商的主电子邮件地址相同，那么您的 Docker 账户将自动链接到该社交个人资料。这允许您使用社交提供商登录。

如果您尝试使用社交提供商登录但尚未拥有 Docker 账户，系统将为您创建一个新账户。按照屏幕上的说明使用社交提供商创建 Docker ID。

## 在登录时重置密码

要重置密码，请在 [登录](https://login.docker.com/u/login) 页面输入您的电子邮件地址并继续登录。当提示输入密码时，选择 **Forgot password?**（忘记密码？）。

## 故障排除

如果您拥有付费的 Docker 订阅，可以 [联系支持团队](https://hub.docker.com/support/contact/) 寻求帮助。

所有 Docker 用户都可以通过以下资源寻求故障排除信息和支持，Docker 或社区将本着尽力而为的原则进行回应：
   - [Docker 社区论坛](https://forums.docker.com/)
   - [Docker 社区 Slack](http://dockr.ly/comm-slack)
