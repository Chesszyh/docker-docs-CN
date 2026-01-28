---
description: 链接到 GitHub 和 BitBucket
keywords: Docker, docker, registry, accounts, plans, Dockerfile, Docker Hub, trusted,
  builds, trusted builds, automated builds, GitHub
title: 配置来自 GitHub 和 BitBucket 的自动构建
linkTitle: 链接账户
weight: 20
aliases:
- /docker-hub/github/
- /docker-hub/bitbucket/
- /docker-hub/builds/link-source/
---

> [!NOTE]
>
> 自动构建需要 Docker Pro、Team 或 Business 订阅。


要自动构建和测试您的镜像，您需要将托管的源代码服务链接到 Docker Hub，以便它可以访问您的源代码仓库。您可以为用户账户或组织配置此链接。

如果您要链接源代码提供商以为团队创建自动构建，请按照说明先为团队[创建服务账户](index.md#service-users-for-team-autobuilds)，然后再按照下面的说明链接账户。

## 链接到 GitHub 用户账户

1. 登录 Docker Hub。

2. 选择 **My Hub** > **Settings** > **Linked accounts**。

3. 为您想要链接的源代码提供商选择 **Link provider**。

    如果您想取消链接当前的 GitHub 账户并重新链接到新的 GitHub 账户，请确保在通过 Docker Hub 链接之前完全退出 [GitHub](https://github.com/)。


4. 查看 **Docker Hub Builder** OAuth 应用程序的设置。

    ![授予访问 GitHub 账户的权限](images/authorize-builder.png)

    > [!NOTE]
    >
    > 如果您是任何 GitHub 组织的所有者，您可能会在此界面上看到授予 Docker Hub 访问这些组织的选项。您还可以单独编辑组织的第三方访问设置以授予或撤销 Docker Hub 的访问权限。请参阅[授予访问 GitHub 组织的权限](link-source.md#grant-access-to-a-github-organization)了解更多信息。

5. 选择 **Authorize docker** 保存链接。

### 授予访问 GitHub 组织的权限

如果您是 GitHub 组织的所有者，您可以授予或撤销 Docker Hub 对该组织仓库的访问权限。根据 GitHub 组织的设置，您可能需要是组织所有者。

如果该组织之前没有被特别授予或撤销过访问权限，您通常可以在链接用户账户的同时授予访问权限。在这种情况下，组织名称旁边会出现一个 **Grant access** 按钮，如下所示。如果此按钮没有出现，您必须手动授予应用程序的访问权限。

要手动授予 Docker Hub 访问 GitHub 组织的权限：

1. 使用上述说明链接您的用户账户。

2. 从您的 GitHub 账户设置中，找到左下角的 **Organization settings** 部分。

3. 选择您想要授予 Docker Hub 访问权限的组织。

4. 选择 **Third-party access**。

    页面会显示第三方应用程序及其访问状态的列表。

5. 选择 **Docker Hub Builder** 旁边的铅笔图标。

6. 选择组织旁边的 **Grant access**。

### 撤销对 GitHub 组织的访问权限

要撤销 Docker Hub 对组织 GitHub 仓库的访问权限：

1. 从您的 GitHub 账户设置中，找到左下角的 **Organization settings** 部分。

2. 选择您想要撤销 Docker Hub 访问权限的组织。

3. 从 Organization Profile 菜单中，选择 **Third-party access**。
    页面会显示第三方应用程序及其访问状态的列表。

4. 选择 Docker Hub Builder 旁边的铅笔图标。

5. 在下一页中，选择 **Deny access**。

### 取消链接 GitHub 用户账户

要撤销 Docker Hub 对您 GitHub 账户的访问权限，您必须同时从 Docker Hub 和您的 GitHub 账户中取消链接。

1. 选择 **My Hub** > **Settings** > **Linked accounts**。

2. 选择您想要移除的源代码提供商旁边的 **Unlink provider**。

3. 转到您的 GitHub 账户的 **Settings** 页面。

4. 在左侧导航栏中选择 **Applications**。

5. 选择 Docker Hub Builder 应用程序右侧的 `...` 菜单，然后选择 **Revoke**。

> [!NOTE]
>
> 每个配置为自动构建源的仓库都包含一个 webhook，用于通知 Docker Hub 仓库中的更改。当您撤销对源代码提供商的访问权限时，此 webhook 不会自动移除。

## 链接到 Bitbucket 用户账户

1. 使用您的 Docker ID 登录 Docker Hub。

2. 选择 **My Hub** > **Settings** > **Linked accounts**。

3. 为您想要链接的源代码提供商选择 **Link provider**。

4. 如有必要，请登录 Bitbucket。

5. 在出现的页面上，选择 **Grant access**。

### 取消链接 Bitbucket 用户账户

要永久撤销 Docker Hub 对您 Bitbucket 账户的访问权限，您必须同时从 Docker Hub 取消链接，并在您的 Bitbucket 账户中撤销授权。

1. 登录 Docker Hub。

2. 选择 **My Hub** > **Settings** > **Linked accounts**。

3. 选择您想要移除的源代码提供商旁边的 **Unlink provider**。

> [!IMPORTANT]
> 在 Docker Hub 上取消链接账户后，您还必须在 Bitbucket 端撤销授权。

要在您的 Bitbucket 账户中撤销授权：

1. 转到您的 Bitbucket 账户并导航到 [**Bitbucket settings**](https://bitbucket.org/account/settings/app-authorizations/)。

2. 在出现的页面上，选择 **OAuth**。

3. 选择 Docker Hub 行旁边的 **Revoke**。

![Bitbucket 授权撤销页面](images/bitbucket-revoke.png)

> [!NOTE]
>
> 每个配置为自动构建源的仓库都包含一个 webhook，用于通知 Docker Hub 仓库中的更改。当您撤销对源代码提供商的访问权限时，此 webhook 不会自动移除。
