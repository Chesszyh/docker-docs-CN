---
title: WSL 上的自定义内核
description: 在 WSL 2 中配合 Docker Desktop 使用自定义内核
keywords: wsl, docker desktop, custom kernel, 自定义内核
tags: [Best practices, troubleshooting]
---

Docker Desktop 依赖于 Microsoft 分发的默认 WSL 2 Linux 内核中所内置的几项内核特性。因此，在 WSL 2 上配合 Docker Desktop 使用自定义内核并未得到官方支持，且可能会导致 Docker Desktop 的启动或运行出现问题。

然而，在某些情况下，运行自定义内核可能是必要的；Docker Desktop 并不阻止使用自定义内核，也有一些用户报告了成功使用的案例。

如果您选择使用自定义内核，建议您从 Microsoft 在其[官方存储库](https://github.com/microsoft/WSL2-Linux-Kernel)中分发的内核源码树开始，并在此基础上添加您所需的特性。

此外，还建议您：
- **版本一致性**：使用与最新 WSL 2 发行版分发的内核相同的版本。您可以通过在终端中运行 `wsl.exe --system uname -r` 来查找该版本。
- **默认配置**：从 Microsoft 在其[存储库](https://github.com/microsoft/WSL2-Linux-Kernel)中提供的默认内核配置开始，并在此基础上添加所需特性。
- **构建环境**：确保您的内核构建环境包含 `pahole`，且其版本正确反映在相应的内核配置 (`CONFIG_PAHOLE_VERSION`) 中。