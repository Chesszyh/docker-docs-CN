---
description: 扩展
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows,
title: 非市场扩展
weight: 20
aliases:
 - /desktop/extensions/non-marketplace/
---

## 安装市场中没有的扩展

> [!WARNING]
>
> 不在市场中的 Docker 扩展未经过 Docker 的审核流程。
> 扩展可以安装二进制文件、调用命令并访问您机器上的文件。安装它们的风险由您自行承担。

扩展市场是在 Docker Desktop 内安装扩展的受信任官方场所。这些扩展已经过 Docker 的审核流程。但是，如果您信任扩展作者，也可以在 Docker Desktop 中安装其他扩展。

鉴于 Docker 扩展的本质（即 Docker 镜像），您可以在其他地方找到用户发布其扩展源代码的位置。例如在 GitHub、GitLab，甚至托管在 DockerHub 或 GHCR 等镜像仓库中。
您可以安装由社区开发的扩展，或安装公司内部由同事开发的扩展。您不仅限于只从市场安装扩展。

> [!NOTE]
>
> 确保已禁用 **Allow only extensions distributed through the Docker Marketplace**（仅允许通过 Docker 市场分发的扩展）选项。否则，这会阻止通过扩展 SDK 工具安装任何未在市场中列出的扩展。
> 您可以在 **Settings** 中更改此选项。

要安装市场中没有的扩展，您可以使用 Docker Desktop 捆绑的扩展 CLI。

在终端中，输入 `docker extension install IMAGE[:TAG]` 以通过镜像引用和可选的标签来安装扩展。使用 `-f` 或 `--force` 标志可以避免交互式确认。

前往 Docker Desktop 仪表板查看新安装的扩展。

## 列出已安装的扩展

无论扩展是从市场安装的还是使用扩展 CLI 手动安装的，您都可以使用 `docker extension ls` 命令显示已安装的扩展列表。
输出内容包括扩展 ID、提供者、版本、标题以及它是否运行后端容器或已在主机上部署二进制文件，例如：

```console
$ docker extension ls
ID                  PROVIDER            VERSION             UI                    VM                  HOST
john/my-extension   John                latest              1 tab(My-Extension)   Running(1)          -
```

前往 Docker Desktop 仪表板，选择 **Add Extensions**，然后在 **Managed** 选项卡中查看新安装的扩展。
请注意，会显示一个 `UNPUBLISHED` 标签，表示该扩展不是从市场安装的。

## 更新扩展

要更新市场中没有的扩展，请在终端中输入 `docker extension update IMAGE[:TAG]`，其中 `TAG` 应与已安装的扩展不同。

例如，如果您使用 `docker extension install john/my-extension:0.0.1` 安装了一个扩展，您可以通过运行 `docker extension update john/my-extension:0.0.2` 来更新它。
前往 Docker Desktop 仪表板查看更新后的扩展。

> [!NOTE]
>
> 未通过市场安装的扩展不会收到来自 Docker Desktop 的更新通知。

## 卸载扩展

要卸载市场中没有的扩展，您可以导航到市场中的 **Managed** 选项卡并选择 **Uninstall** 按钮，或者在终端中输入 `docker extension uninstall IMAGE[:TAG]`。
