---
description: 探索学习中心并了解登录 Docker Desktop 的好处
keywords: Docker 控制面板, 管理, 容器, gui, dashboard, 镜像, 用户手册, 学习中心, 指南, 登录
title: 登录 Docker Desktop
linkTitle: 登录
weight: 40
aliases:
- /desktop/linux/
- /desktop/linux/index/
- /desktop/mac/
- /desktop/mac/index/
- /desktop/windows/
- /desktop/windows/index/
- /docker-for-mac/
- /docker-for-mac/index/
- /docker-for-mac/osx/
- /docker-for-mac/started/
- /docker-for-windows/
- /docker-for-windows/index/
- /docker-for-windows/started/
- /mac/
- /mackit/
- /mackit/getting-started/
- /win/
- /windows/
- /winkit/
- /winkit/getting-started/
- /desktop/get-started/
---

Docker 建议通过 Docker 控制面板（Dashboard）右上角的 **Sign in**（登录）选项进行登录。

在管理员权限受限的大型企业中，管理员可以 [强制执行登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。 

> [!TIP]
>
> 探索 [Docker 的核心订阅计划](https://www.docker.com/pricing/)，看看 Docker 还能为您提供什么。 

## 登录的好处

- 直接从 Docker Desktop 访问您的 Docker Hub 仓库。

- 与匿名用户相比，提高您的拉取速率限制。请参阅 [使用情况和限制](/manuals/docker-hub/usage/_index.md)。

- 通过 [强化的 Desktop (Hardened Desktop)](/manuals/security/for-admins/hardened-desktop/_index.md) 增强您组织在容器化开发方面的安全状况。

> [!NOTE]
>
> Docker Desktop 会在 90 天后或 30 天未活动后自动将您登出。 

## 在 Linux 版 Docker Desktop 上登录

Linux 版 Docker Desktop 依赖 [`pass`](https://www.passwordstore.org/) 在 GPG 加密文件中存储凭据。在使用您的 [Docker ID](/accounts/create-account/) 登录 Docker Desktop 之前，您必须初始化 `pass`。如果未配置 `pass`，Docker Desktop 会显示警告。

1. 生成 GPG 密钥。您可以使用 GPG 密钥来初始化 pass。要生成 GPG 密钥，请运行：

   ``` console
   $ gpg --generate-key
   ``` 
2. 出现提示时输入您的姓名和电子邮件。 

   确认后，GPG 会创建一对密钥。查找包含您 GPG ID 的 `pub` 行，例如：

   ```text
   ...
   pubrsa3072 2022-03-31 [SC] [expires: 2024-03-30]
    3ABCD1234EF56G78
   uid          Molly <molly@example.com>
   ```
3. 复制 GPG ID 并使用它来初始化 `pass`：

   ```console
   $ pass init <您生成的_gpg-id_公钥>
   ``` 

   您应该会看到类似以下的输出： 

   ```text
   mkdir: created directory '/home/molly/.password-store/'
   Password store initialized for <生成的_gpg-id_公钥>
   ```

初始化 `pass` 后，您就可以登录并拉取您的私有镜像了。当 Docker CLI 或 Docker Desktop 使用凭据时，可能会弹出用户提示，要求输入您在生成 GPG 密钥期间设置的密码。

```console
$ docker pull molly/privateimage
Using default tag: latest
latest: Pulling from molly/privateimage
3b9cc81c3203: Pull complete 
Digest: sha256:3c6b73ce467f04d4897d7a7439782721fd28ec9bf62ea2ad9e81a5fb7fb3ff96
Status: Downloaded newer image for molly/privateimage:latest
docker.io/molly/privateimage:latest
```

## 下一步

- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其功能。 
- 更改您的 [Docker Desktop 设置](/manuals/desktop/settings-and-maintenance/settings.md)。
- [浏览常见问题 (FAQ)](/manuals/desktop/troubleshoot-and-support/faqs/general.md)。
