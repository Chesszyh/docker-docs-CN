---
title: 快速入门
description: 如何快速构建扩展的指南
keywords: quickstart, extensions
aliases:
 - desktop/extensions-sdk/tutorials/initialize/
 - /desktop/extensions-sdk/quickstart/
weight: 20
---

按照本指南开始创建基本的 Docker 扩展。快速入门指南会自动为您生成样板文件。

## 前提条件

- [Docker Desktop](/manuals/desktop/release-notes.md)
- [NodeJS](https://nodejs.org/)
- [Go](https://go.dev/dl/)

> [!NOTE]
>
> NodeJS 和 Go 仅在按照快速入门指南创建扩展时需要。它使用 `docker extension init` 命令自动生成样板文件。此命令使用基于 ReactJS 和 Go 应用程序的模板。

在 Docker Desktop 设置中，确保您可以安装正在开发的扩展。您可能需要导航到 Docker Desktop 设置中的 **Extensions** 选项卡，并取消选择 **Allow only extensions distributed through the Docker Marketplace**。

## 第一步：设置目录

要设置目录，使用 `init` 子命令并提供扩展的名称。

```console
$ docker extension init <my-extension>
```

该命令会询问一系列关于扩展的问题，如名称、描述和 Hub 仓库名称。这有助于 CLI 为您生成一组样板文件以便开始。它将样板文件存储在 `my-extension` 目录中。

自动生成的扩展包含：

- `backend` 文件夹中的 Go 后端服务，监听一个 socket。它有一个 `/hello` 端点，返回 JSON 负载。
- `frontend` 文件夹中的 React 前端，可以调用后端并输出后端的响应。

有关构建 UI 的更多信息和指南，请参阅[设计和 UI 样式部分](design/design-guidelines.md)。

## 第二步：构建扩展

要构建扩展，进入新创建的目录并运行：

```console
$ docker build -t <name-of-your-extension> .
```

`docker build` 构建扩展并生成与所选 hub 仓库同名的镜像。例如，如果您对以下问题的回答是 `john/my-extension`：

```console
? Hub repository (eg. namespace/repository on hub): john/my-extension`
```

`docker build` 会生成名为 `john/my-extension` 的镜像。

## 第三步：安装并预览扩展

要在 Docker Desktop 中安装扩展，运行：

```console
$ docker extension install <name-of-your-extension>
```

要在 Docker Desktop 中预览扩展，安装完成后，您应该会在 **Extensions** 菜单下看到一个 **Quickstart** 项。选择此项会打开扩展的前端。

> [!TIP]
>
> 在 UI 开发期间，使用热重载来测试更改而无需重建整个扩展会很有帮助。有关更多信息，请参阅[开发 UI 时预览](dev/test-debug.md#hot-reloading-whilst-developing-the-ui)。

您可能还想检查属于扩展的容器。默认情况下，扩展容器在 Docker Dashboard 中是隐藏的。您可以在 **Settings** 中更改此设置，有关更多信息，请参阅[如何显示扩展容器](dev/test-debug.md#show-the-extension-containers)。

## 第四步：将扩展提交并发布到市场

如果您想让所有 Docker Desktop 用户都可以使用您的扩展，您可以将其提交发布到市场。有关更多信息，请参阅[发布](extensions/_index.md)。

## 清理

要移除扩展，运行：

```console
$ docker extension rm <name-of-your-extension>
```

## 下一步

- 为您的扩展构建更[高级的前端](build/frontend-extension-tutorial.md)。
- 学习如何[测试和调试](dev/test-debug.md)您的扩展。
- 学习如何[为扩展设置 CI](dev/continuous-integration.md)。
- 了解更多关于扩展[架构](architecture/_index.md)的信息。
- 了解更多关于[设计 UI](design/design-guidelines.md) 的信息。
