---
title: 使用 WSL
description: 了解如何结合使用 Docker 和 WSL 2 进行开发，并理解 WSL 对 GPU 的支持
keywords: wsl, wsl 2, 开发, docker desktop, windows
aliases:
- /desktop/wsl/use-wsl/
---

以下部分介绍了如何开始使用 Docker 和 WSL 2 开发应用程序。为了获得结合使用 Docker 和 WSL 2 进行开发的最佳体验，我们建议将代码存放在您的默认 Linux 发行版中。在开启 Docker Desktop 的 WSL 2 功能后，您可以开始在 Linux 发行版内处理代码，理想情况下您的 IDE 仍保留在 Windows 中。如果您使用的是 [VS Code](https://code.visualstudio.com/download)，这个工作流会非常简单。

## 结合使用 Docker 和 WSL 2 进行开发

1. 打开 VS Code 并安装 [Remote - WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) 扩展。此扩展让您能够与 Linux 发行版中的远程服务器配合工作，而您的 IDE 客户端仍保留在 Windows 上。
2. 打开终端并输入：

    ```console
    $ wsl
    ```
3. 导航到您的项目目录，然后输入：

    ```console
    $ code .
    ```

    这将打开一个连接到您的默认 Linux 发行版的远程 VS Code 新窗口，您可以在屏幕左下角进行确认。


或者，您可以从 **开始** 菜单打开您的默认 Linux 发行版，导航到您的项目目录，然后运行 `code .`。
