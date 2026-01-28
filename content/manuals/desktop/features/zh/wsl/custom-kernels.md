---
title: WSL 上的自定义内核
description: 在 WSL 2 上使用 Docker Desktop 时使用自定义内核
keywords: wsl, docker desktop, custom kernel
tags: [Best practices, troubleshooting]
---

Docker Desktop 依赖于 Microsoft 分发的默认 WSL 2 Linux 内核中内置的多个内核功能。因此，在 WSL 2 上使用 Docker Desktop 时使用自定义内核不受官方支持，可能会导致 Docker Desktop 启动或运行出现问题。

但是，在某些情况下可能需要运行自定义内核；Docker Desktop 不会阻止其使用，一些用户报告成功使用了自定义内核。

如果您选择使用自定义内核，建议您从 Microsoft 从其[官方仓库](https://github.com/microsoft/WSL2-Linux-Kernel)分发的内核树开始，然后在此基础上添加您需要的功能。

还建议您：
- 使用与最新 WSL2 版本分发的内核版本相同的版本。您可以在终端中运行 `wsl.exe --system uname -r` 来查找版本。
- 从 Microsoft 从其[仓库](https://github.com/microsoft/WSL2-Linux-Kernel)提供的默认内核配置开始，然后在此基础上添加您需要的功能。
- 确保您的内核构建环境包含 `pahole`，并且其版本正确反映在相应的内核配置中（`CONFIG_PAHOLE_VERSION`）。


