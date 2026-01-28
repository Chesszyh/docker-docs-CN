---
title: 自动构建故障排除
description: 如何排除自动构建的故障
keywords: docker hub, troubleshoot, automated builds, autobuilds
tags: [ Troubleshooting ]
linkTitle: 故障排除
aliases:
- /docker-hub/builds/troubleshoot/
---

> [!NOTE]
>
> 自动构建需要 Docker Pro、Team 或 Business 订阅。

## 构建失败

如果构建失败，**General** 和 **Builds** 选项卡上的构建报告行旁边会出现一个 **Retry** 图标。**Build report** 页面和 **Timeline logs** 也会显示一个 **Retry** 按钮。

![显示重试构建按钮的时间线视图](images/retry-build.png)

> [!NOTE]
>
> 如果您正在查看属于组织的仓库的构建详情，只有当您对该仓库具有 `Read & Write` 访问权限时，**Cancel** 和 **Retry** 按钮才会出现。

自动构建有 4 小时的执行时间限制。如果构建达到此时间限制，它会被自动取消，构建日志会显示以下消息：

```text
2022-11-02T17:42:27Z The build was cancelled or exceeded the maximum execution time.
```

此日志消息与您主动取消构建时的消息相同。要确定构建是否被自动取消，请检查构建持续时间。


## 构建具有链接私有子模块的仓库

Docker Hub 在您的源代码仓库中设置了一个部署密钥，允许它克隆仓库并构建它。此密钥仅适用于单个特定的代码仓库。如果您的源代码仓库使用私有 Git 子模块，或者需要您克隆其他私有仓库来进行构建，Docker Hub 无法访问这些额外的仓库，您的构建无法完成，并且会在构建时间线中记录错误。

要解决此问题，您可以使用 `SSH_PRIVATE` 环境变量设置自动构建，以覆盖部署密钥并授予 Docker Hub 的构建系统访问这些仓库的权限。

> [!NOTE]
>
> 如果您正在为团队使用自动构建，请改用以下流程，并为您的源代码提供商配置服务用户。您也可以为个人账户执行此操作，以限制 Docker Hub 对您源仓库的访问。

1. 生成一个仅用于构建的 SSH 密钥对，并将公钥添加到您的源代码提供商账户。

    此步骤是可选的，但允许您撤销仅用于构建的密钥对而不移除其他访问权限。

2. 将密钥对的私钥部分复制到剪贴板。
3. 在 Docker Hub 中，导航到具有链接私有子模块的仓库的构建页面。（如有必要，请按照[此处](index.md#configure-automated-builds)的步骤配置自动构建。）
4. 在屏幕底部，选择 **Build Environment variables** 旁边的**加号**图标。
5. 输入 `SSH_PRIVATE` 作为新环境变量的名称。
6. 将密钥对的私钥部分粘贴到 **Value** 字段中。
7. 选择 **Save**，或 **Save and Build** 以验证构建现在可以完成。

> [!NOTE]
>
> 您必须使用 git clone over SSH（`git@submodule.tld:some-submodule.git`）而不是 HTTPS 来配置您的私有 git 子模块。
