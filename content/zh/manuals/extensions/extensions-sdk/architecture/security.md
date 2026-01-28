---
title: 扩展安全
linkTitle: 安全
description: 扩展安全模型的各个方面
keywords: Docker, extensions, sdk, security
aliases:
 - /desktop/extensions-sdk/guides/security/
 - /desktop/extensions-sdk/architecture/security/
---

## 扩展能力

扩展可以包含以下可选部分：
* 以 HTML 或 JavaScript 编写的用户界面，显示在 Docker Desktop 仪表板中
* 作为容器运行的后端部分
* 部署在主机上的可执行文件。

扩展以与 Docker Desktop 用户相同的权限执行。扩展能力包括运行任何 Docker 命令（包括运行容器和挂载文件夹）、运行扩展二进制文件，以及访问运行 Docker Desktop 的用户可访问的机器上的文件。

Extensions SDK 提供了一组 JavaScript API，用于从扩展 UI 代码调用命令或调用这些二进制文件。扩展还可以提供一个后端部分，在后台启动一个长时间运行的容器。

> [!IMPORTANT]
>
> 安装扩展时，请确保您信任扩展的发布者或作者，因为扩展具有与运行 Docker Desktop 的用户相同的访问权限。
