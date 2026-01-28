---
title: 创建和管理访问令牌
linkTitle: 访问令牌
description: 了解如何创建和管理您的个人 Docker 访问令牌，以安全地通过编程方式推送和拉取镜像。
keywords: docker hub, hub, security, PAT, personal access token
aliases:
- /docker-hub/access-tokens/
---

您可以创建个人访问令牌（Personal Access Token，PAT）作为密码的替代方案，用于 Docker CLI 身份验证。

与密码相比，PAT 具有以下优势：

- 您可以查看 PAT 的最后使用时间，如果发现任何可疑活动，可以禁用或删除它。
- 使用访问令牌时，您无法对账户执行任何管理操作，包括更改密码。这可以在您的计算机被入侵时保护您的账户。
- 访问令牌对于构建集成非常有价值，因为您可以为每个集成发放多个令牌，并随时撤销它们。

## 创建访问令牌

> [!IMPORTANT]
>
> 请像对待密码一样保护访问令牌，并对其保密。例如，将令牌安全地存储在凭据管理器中。

使用 Docker Admin Console 创建访问令牌。

1. 登录 [Docker Home](https://app.docker.com/)。
1. 选择右上角的头像，然后从下拉菜单中选择 **Account settings**。
1. 选择 **Personal access tokens**。
1. 选择 **Generate new token**。
1. 为令牌添加描述。使用能够说明令牌用例或用途的内容。
1. 选择令牌的过期日期。
1. 设置访问权限。
   访问权限是在仓库中设置限制的范围。例如，对于读写权限，自动化流水线可以构建镜像然后将其推送到仓库。但是，它不能删除仓库。
1. 选择 **Generate**，然后复制屏幕上显示的令牌并保存。关闭此提示后，您将无法再次获取该令牌。

## 使用访问令牌

使用 Docker CLI 登录时，您可以使用访问令牌代替密码。

使用以下命令从 Docker CLI 客户端登录，将 `YOUR_USERNAME` 替换为您的 Docker ID：

```console
$ docker login --username <YOUR_USERNAME>
```

当提示输入密码时，输入您的个人访问令牌而不是密码。

> [!NOTE]
>
> 如果您启用了[双因素认证（2FA）](2fa/_index.md)，则在从 Docker CLI 登录时必须使用个人访问令牌。2FA 是一种可选但更安全的身份验证方法。

### 合理使用

使用 PAT 时，用户应注意过度创建 PAT 可能会导致限流或额外收费。为确保资源的合理使用并维护服务质量，Docker 保留对过度使用 PAT 的账户施加限制或收取额外费用的权利。

## 修改现有令牌

> [!NOTE]
>
> 您无法编辑现有令牌的过期日期。如果需要设置新的过期日期，必须创建新的 PAT。

您可以根据需要重命名、激活、停用或删除令牌。您可以在账户设置中管理令牌。

1. 登录 [Docker Home](https://app.docker.com/login)。
1. 选择右上角的头像，然后从下拉菜单中选择 **Account settings**。
1. 选择 **Personal access tokens**。

   此页面显示所有令牌的概览，并列出令牌是手动生成的还是[自动生成](#自动生成的令牌)的。您还可以查看令牌的范围、哪些令牌处于激活或未激活状态、创建时间、最后使用时间以及过期日期。
1. 选择令牌行最右侧的操作菜单，然后选择 **Deactivate** 或 **Activate**、**Edit** 或 **Delete** 来修改令牌。
1. 编辑令牌后，选择 **Save token**。

## 自动生成的令牌

当您使用 Docker Desktop 登录 Docker 账户时，Docker Desktop 会代表您生成一个身份验证令牌。当您使用 Docker CLI 与 Docker Hub 交互时，CLI 会使用此令牌进行身份验证。该令牌范围具有读取、写入和删除权限。如果您的 Docker Desktop 会话过期，该令牌会自动从本地删除。

您的账户最多可以关联 5 个自动生成的令牌。这些令牌会根据使用情况和创建日期自动删除和创建。您也可以根据需要删除自动生成的令牌。更多信息，请参阅[修改现有令牌](#修改现有令牌)。
