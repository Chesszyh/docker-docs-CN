---
title: 使用 WSL
description: 如何配合 Docker 和 WSL 2 进行开发，并了解针对 WSL 的 GPU 支持
keywords: wsl, wsl 2, 开发, develop, docker desktop, windows
aliases:
- /desktop/wsl/use-wsl/
---

以下部分介绍了如何使用 Docker 和 WSL 2 开始开发您的应用程序。为了在使用 Docker 和 WSL 2 时获得最佳开发体验，我们建议您将代码存放在默认的 Linux 发行版中。在 Docker Desktop 上开启 WSL 2 功能后，您就可以开始在 Linux 发行版内部处理代码，且理想情况下您的 IDE 仍保留在 Windows 中。如果您使用的是 [VS Code](https://code.visualstudio.com/download)，此工作流将非常简单。

## 使用 Docker 和 WSL 2 进行开发

1. 打开 VS Code 并安装 [Remote - WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) 扩展。此扩展允许您在 Windows 中使用 IDE 客户端的同时，通过 Linux 发行版中的远程服务器进行开发。
2. 打开终端并输入：

    ```console
    $ wsl
    ```
3. 导航到您的项目目录，然后输入：

    ```console
    $ code .
    ```

    这会打开一个新的 VS Code 窗口，远程连接到您的默认 Linux 发行版，您可以在屏幕底角看到连接状态。

或者，您也可以从 **开始 (Start)** 菜单打开默认的 Linux 发行版，导航到项目目录，然后运行 `code .`。