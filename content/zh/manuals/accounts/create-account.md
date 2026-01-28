---
title: 创建账户
weight: 10
description: 了解如何注册 Docker ID 并登录您的账户
keywords: accounts, docker ID, billing, paid plans, support, Hub, Store, Forums, knowledge
  base, beta access, email, activation, verification
aliases:
- /docker-hub/accounts/
- /docker-id/
---

您可以使用电子邮件地址创建免费的 Docker 账户，也可以通过 Google 或 GitHub 账户注册。一旦您使用唯一的 Docker ID 创建了账户，就可以访问所有 Docker 产品，包括 Docker Hub。通过 Docker Hub，您可以访问仓库并浏览社区和经过验证的发布者提供的镜像。

您的 Docker ID 将成为您在托管 Docker 服务和 [Docker 论坛](https://forums.docker.com/)中的用户名。

> [!TIP]
>
> 探索 [Docker 的订阅计划](https://www.docker.com/pricing/)，了解 Docker 还能为您提供什么。

## 创建 Docker ID

### 使用电子邮件地址注册

1. 前往 [Docker 注册页面](https://app.docker.com/signup/)。

2. 输入一个唯一且有效的电子邮件地址。

3. 输入一个用户名作为您的 Docker ID。一旦创建了 Docker ID，如果您停用此账户，将来将无法重新使用该用户名。

    您的用户名：
    - 长度必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母

4. 输入一个至少 9 个字符的密码。

5. 选择 **Sign Up**。

6. 打开您的电子邮件客户端。Docker 会向您提供的地址发送一封验证邮件。

7. 验证您的电子邮件地址以完成注册流程。

> [!NOTE]
>
> 您必须验证电子邮件地址后才能完全访问 Docker 的功能。

### 使用 Google 或 GitHub 注册

> [!IMPORTANT]
>
> 要使用社交账号提供商注册，您必须在开始之前先通过该提供商验证您的电子邮件地址。

1. 前往 [Docker 注册页面](https://app.docker.com/signup/)。

2. 选择您的社交账号提供商，Google 或 GitHub。

3. 选择您想要关联到 Docker 账户的社交账号。

4. 选择 **Authorize Docker** 以允许 Docker 访问您的社交账号信息。您将被重定向到注册页面。

5. 输入一个用户名作为您的 Docker ID。

    您的用户名：
    - 长度必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母

6. 选择 **Sign up**。

## 登录

注册 Docker ID 并验证电子邮件地址后，您可以登录[您的 Docker 账户](https://login.docker.com/u/login/)。您可以：
- 使用电子邮件地址（或用户名）和密码登录。
- 使用社交账号提供商登录。更多信息，请参阅[使用社交账号提供商登录](#使用社交账号提供商登录)。
- 使用 `docker login` 命令通过 CLI 登录。更多信息，请参阅 [`docker login`](/reference/cli/docker/login.md)。

> [!WARNING]
>
> 当您使用 `docker login` 命令时，您的凭据会存储在您的主目录中的 `.docker/config.json` 文件中。密码在此文件中以 base64 编码存储。
>
> 我们建议使用 [Docker 凭据助手](https://github.com/docker/docker-credential-helpers)之一来安全存储密码。为了获得额外的安全性，您还可以使用[个人访问令牌](../security/for-developers/access-tokens.md)来登录，该令牌在此文件中仍然是编码的（如果没有 Docker 凭据助手），但不允许执行管理员操作（如更改密码）。

### 使用社交账号提供商登录

> [!IMPORTANT]
>
> 要使用社交账号提供商登录，您必须在开始之前先通过该提供商验证您的电子邮件地址。

您也可以使用 Google 或 GitHub 账户登录您的 Docker 账户。如果存在一个与您社交账号提供商的主要电子邮件地址相同的 Docker 账户，您的 Docker 账户将自动关联到该社交账号。这使您可以使用社交账号提供商登录。

如果您尝试使用社交账号提供商登录但还没有 Docker 账户，系统将为您创建一个新账户。按照屏幕上的说明使用您的社交账号提供商创建 Docker ID。

## 在登录时重置密码

要重置密码，请在[登录](https://login.docker.com/u/login)页面输入您的电子邮件地址并继续登录。当提示输入密码时，选择 **Forgot password?**。

## 故障排除

如果您拥有付费 Docker 订阅，可以[联系支持团队](https://hub.docker.com/support/contact/)获取帮助。

所有 Docker 用户都可以通过以下资源寻求故障排除信息和支持，Docker 或社区会尽最大努力进行响应：
   - [Docker 社区论坛](https://forums.docker.com/)
   - [Docker 社区 Slack](http://dockr.ly/comm-slack)
