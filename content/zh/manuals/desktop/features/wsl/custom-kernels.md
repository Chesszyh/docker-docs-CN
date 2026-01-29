---
title: WSL 上的自定义内核
description: 在 WSL 2 上结合使用自定义内核与 Docker Desktop
keywords: wsl, docker desktop, 自定义内核
tags: [最佳实践, 故障排除]
---

Docker Desktop 依赖于由微软分发的默认 WSL 2 Linux 内核中内置的几项内核特性。因此，在 WSL 2 上的 Docker Desktop 中使用自定义内核并非官方支持，并且可能会导致 Docker Desktop 的启动或操作出现问题。

然而，在某些情况下可能需要运行自定义内核；Docker Desktop 并不禁止使用它们，且一些用户已报告成功使用。

如果您选择使用自定义内核，建议您从微软在其 [官方仓库](https://github.com/microsoft/WSL2-Linux-Kernel) 分发的内核树开始，然后在该基础上添加您需要的功能。

此外，建议您：
- 使用与最新 WSL2 版本分发的相同内核版本。您可以在终端运行 `wsl.exe --system uname -r` 来查找该版本。
- 从微软在其 [仓库](https://github.com/microsoft/WSL2-Linux-Kernel) 中提供的默认内核配置开始，并在该基础上添加您需要的功能。
- 确保您的内核构建环境包含 `pahole`，且其版本在相应的内核配置 (`CONFIG_PAHOLE_VERSION`) 中得到了正确反映。
