---
title: 从 Microsoft Store 在 Windows 上安装 Docker Desktop
linkTitle: MS Store
description: 通过 Microsoft Store 安装 Docker Desktop for Windows。了解其更新行为和限制。
keywords: microsoft store, windows, docker desktop, install, deploy, configure, admin, mdm, intune, winget
tags: [admin]
weight: 30
---

您可以通过 [Microsoft app store](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB) 部署 Docker Desktop for Windows。

Microsoft Store 版本的 Docker Desktop 提供与标准安装程序相同的功能，但其更新行为有所不同，具体取决于开发人员是自己安装还是由 MDM 工具（如 Intune）处理安装。这将在以下部分说明。

请选择最符合您环境要求和管理实践的安装方法。

## 更新行为

### 开发人员管理的安装

对于直接安装 Docker Desktop 的开发人员：

- Microsoft Store 不会自动为大多数用户更新像 Docker Desktop 这样的 Win32 应用。
- 只有一小部分用户（约 20%）可能会在 Microsoft Store 页面收到更新通知。
- 大多数用户必须在 Store 中手动检查并应用更新。

### Intune 管理的安装

在使用 Intune 管理的环境中：
- Intune 大约每 8 小时检查一次更新。
- 当检测到新版本时，Intune 会触发 `winget` 升级。
- 如果配置了适当的策略，更新可以在无需用户干预的情况下自动进行。
- 更新由 Intune 的管理基础设施处理，而不是 Microsoft Store 本身。

## WSL 注意事项

Docker Desktop for Windows 与 WSL 紧密集成。从 Microsoft Store 安装的 Docker Desktop 在更新时：
- 确保您已退出 Docker Desktop 且不再运行，以便更新能够成功完成
- 在某些环境中，虚拟硬盘 (VHDX) 文件锁可能会阻止更新完成。

## Intune 管理建议

如果使用 Intune 管理 Docker Desktop for Windows：
- 确保您的 Intune 策略配置为处理应用程序更新
- 请注意更新过程使用 WinGet API 而不是直接的 Store 机制
- 考虑在受控环境中测试更新过程以验证功能正常
