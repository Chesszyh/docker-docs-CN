---
title: 在 Windows 上通过 Microsoft Store 安装 Docker Desktop
linkTitle: Microsoft Store
description: 通过 Microsoft Store 安装 Windows 版 Docker Desktop。了解其更新行为及限制。
keywords: microsoft store, windows, docker desktop, 安装, 部署, 配置, 管理员, admin, mdm, intune, winget, 微软商店
tags: [admin]
weight: 30
---

您可以通过 [Microsoft 应用商店](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB) 部署 Windows 版 Docker Desktop。

Microsoft Store 版本的 Docker Desktop 提供与标准安装程序相同的功能，但其更新行为会根据开发人员是自行安装，还是由 Intune 等 MDM 工具统一管理安装而有所不同。具体描述如下。

请选择最符合您环境需求和管理实践的安装方法。

## 更新行为

### 开发人员自行安装

对于直接安装 Docker Desktop 的开发人员：

- 对于大多数用户，Microsoft Store 不会自动更新像 Docker Desktop 这样的 Win32 应用。
- 只有少数用户（约 20%）可能会在 Microsoft Store 页面上收到更新通知。
- 大多数用户必须在商店内手动检查并应用更新。

### Intune 管理的安装

在由 Intune 管理的环境中：
- Intune 约每 8 小时检查一次更新。
- 当检测到新版本时，Intune 会触发 `winget` 升级。
- 如果配置了适当的策略，更新可以自动进行，无需用户干预。
- 更新由 Intune 的管理基础设施处理，而非 Microsoft Store 本身。

## WSL 相关注意事项

Windows 版 Docker Desktop 与 WSL 紧密集成。在更新从 Microsoft Store 安装的 Docker Desktop 时：
- 请确保已退出 Docker Desktop 且不再运行，以便更新能够成功完成。
- 在某些环境下，虚拟硬盘 (VHDX) 文件锁可能会阻止更新完成。

## Intune 管理建议

如果使用 Intune 管理 Windows 版 Docker Desktop：
- 确保您的 Intune 策略已配置为处理应用程序更新。
- 请注意，更新过程使用的是 WinGet API，而非直接的应用商店机制。
- 考虑在受控环境中测试更新过程，以验证功能是否正常。
