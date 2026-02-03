---
title: 创建和管理访问令牌 (Access tokens)
linkTitle: 访问令牌
description: 了解如何创建和管理您的个人 Docker 访问令牌，以便以编程方式安全地推送和拉取镜像。
keywords: docker hub, hub, security, PAT, personal access token, 个人访问令牌
aliases:
- /docker-hub/access-tokens/
---

您可以创建一个个人访问令牌 (Personal Access Token, PAT) 来代替密码用于 Docker CLI 身份验证。

与密码相比，PAT 具有以下优势：

- 您可以查看 PAT 的最后使用时间，如果发现任何可疑活动，可以将其禁用或删除。
- 使用访问令牌时，无法对帐户执行任何管理操作，包括更改密码。如果您的计算机遭到入侵，这可以保护您的帐户。
- 访问令牌对于构建集成非常有用，因为您可以发布多个令牌（每个集成一个），并随时撤销它们。

## 创建访问令牌

> [!IMPORTANT]
>
> 请像对待密码一样对待访问令牌，并保持其机密性。例如，将您的令牌安全地存储在凭据管理器中。

使用 Docker 管理控制台（Admin Console）创建访问令牌。

1. 登录 [Docker Home](https://app.docker.com/)。
1. 选择右上角的头像，然后从下拉菜单中选择 **Account settings（帐户设置）**。
1. 选择 **Personal access tokens（个人访问令牌）**。
1. 选择 **Generate new token（生成新令牌）**。
1. 为您的令牌添加描述。请使用能说明令牌用途或目的的描述。
1. 选择令牌的过期日期。
1. 设置访问权限。
   访问权限是设置存储库限制的作用域（Scopes）。例如，对于 Read & Write（读写）权限，自动化流水线可以构建镜像并将其推送到存储库。但是，它无法删除存储库。
1. 选择 **Generate（生成）**，然后复制屏幕上显示的令牌并保存。一旦关闭此提示，您将无法再次检索该令牌。

## 使用访问令牌

当您使用 Docker CLI 登录时，可以使用访问令牌代替密码。

使用以下命令从 Docker CLI 客户端登录，将 `<YOUR_USERNAME>` 替换为您的 Docker ID：

```console
$ docker login --username <YOUR_USERNAME>
```

当提示输入密码时，请输入您的个人访问令牌而不是密码。

> [!NOTE]
>
> 如果您启用了[双重身份验证 (2FA)](2fa/_index.md)，则在从 Docker CLI 登录时必须使用个人访问令牌。2FA 是一种可选但更安全的身份验证方法。

### 公平使用 (Fair use)

在使用 PAT 时，用户应意识到过度创建 PAT 可能会导致限流或产生额外费用。为了确保资源的公平使用并维持服务质量，Docker 保留对过度使用 PAT 的帐户施加限制或收取额外费用的权利。

## 修改现有令牌

> [!NOTE]
>
> 您无法编辑现有令牌的过期日期。如果您需要设置新的过期日期，必须创建一个新的 PAT。

您可以根据需要重命名、激活、停用或删除令牌。您可以在帐户设置中管理您的令牌。

1. 登录 [Docker Home](https://app.docker.com/login)。
1. 选择右上角的头像，然后从下拉菜单中选择 **Account settings（帐户设置）**。
1. 选择 **Personal access tokens（个人访问令牌）**。

   此页面显示了您所有令牌的概览，并列出了令牌是手动生成的还是[自动生成的](#自动生成的令牌)。您还可以查看令牌的作用域、哪些令牌处于活动或非活动状态、创建时间、最后使用时间以及过期日期。
1. 选择令牌行最右侧的操作菜单，然后选择 **Deactivate（停用）** 或 **Activate（激活）**、**Edit（编辑）** 或 **Delete（删除）** 以修改令牌。
1. 编辑令牌后，选择 **Save token（保存令牌）**。

## 自动生成的令牌

当您使用 Docker Desktop 登录 Docker 帐户时，Docker Desktop 会代表您生成一个身份验证令牌。当您使用 Docker CLI 与 Docker Hub 交互时，CLI 会使用此令牌进行身份验证。该令牌的作用域具有读取、写入和删除权限。如果您的 Docker Desktop 会话过期，令牌会自动在本地移除。

您的帐户最多可以关联 5 个自动生成的令牌。这些令牌会根据使用情况和创建日期自动删除和创建。您也可以根据需要删除自动生成的令牌。有关更多信息，请参阅[修改现有令牌](#修改现有令牌)。
