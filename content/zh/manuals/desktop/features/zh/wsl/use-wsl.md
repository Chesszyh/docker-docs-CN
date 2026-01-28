---
title: 使用 WSL
description: 如何使用 Docker 和 WSL 2 进行开发以及了解 WSL 的 GPU 支持
keywords: wsl, wsl 2, develop, docker desktop, windows
aliases:
- /desktop/wsl/use-wsl/
---

以下部分介绍如何开始使用 Docker 和 WSL 2 开发应用程序。我们建议您将代码放在默认 Linux 发行版中，以便使用 Docker 和 WSL 2 获得最佳开发体验。在 Docker Desktop 上开启 WSL 2 功能后，您可以开始在 Linux 发行版中使用您的代码进行工作，理想情况下您的 IDE 仍在 Windows 中。如果您使用 [VS Code](https://code.visualstudio.com/download)，此工作流程非常简单。

## 使用 Docker 和 WSL 2 进行开发

1. 打开 VS Code 并安装 [Remote - WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) 扩展。此扩展允许您使用 Linux 发行版中的远程服务器工作，而 IDE 客户端仍在 Windows 上。
2. 打开终端并输入：

    ```console
    $ wsl
    ```
3. 导航到您的项目目录，然后输入：

    ```console
    $ code .
    ```

    这将打开一个新的 VS Code 窗口，远程连接到您的默认 Linux 发行版，您可以在屏幕底角查看。


或者，您可以从**开始**菜单打开默认 Linux 发行版，导航到您的项目目录，然后运行 `code .`

