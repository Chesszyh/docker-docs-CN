---
title: 企业级部署常见问题 (FAQ)
linkTitle: 常见问题 (FAQ)
description: 有关大规模部署 Docker Desktop 的常见问题
keywords: msi, 部署, deploy, docker desktop, faqs, pkg, mdm, jamf, intune, windows, mac, 企业, 管理, admin
tags: [FAQ, admin]
aliases:
- /desktop/install/msi/faq/
- /desktop/setup/install/msi/faq/
---

## MSI

有关使用 MSI 安装程序安装 Docker Desktop 的常见问题。

### 如果用户已有较旧版本的 Docker Desktop 安装（即 `.exe`），其用户数据会怎样？

在安装新的 MSI 版本之前，用户必须[卸载](/manuals/desktop/uninstall.md)旧的 `.exe` 安装程序。这将删除机器本地的所有 Docker 容器、镜像、卷以及其他 Docker 相关数据，并移除由 Docker Desktop 生成的文件。

为了在卸载前保留现有数据，用户应当[备份](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)其容器和卷。

对于 Docker Desktop 4.30 及更高版本，`.exe` 安装程序包含一个 `-keep-data` 标志，可以在移除 Docker Desktop 的同时保留底层资源（如容器虚拟机）：

```powershell
& 'C:\Program Files\Docker\Docker\Docker Desktop Installer.exe' uninstall -keep-data
```

### 如果用户的机器上安装了旧版 `.exe` 会发生什么？

MSI 安装程序会检测旧版 `.exe` 安装，并阻止安装，直到卸载前一版本。它会提示用户在重试安装 MSI 版本之前，先卸载其当前/旧版本。

### 我的安装失败了，我该如何查明原因？

MSI 安装可能会静默失败，提供的诊断反馈很少。

要调试失败的安装，请重新运行安装并启用详细日志记录：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log"
```

安装失败后，打开日志文件并搜索 `value 3`。这是 Windows Installer 在失败时输出的退出代码。在该行上方，您通常可以找到失败的原因。

### 为什么安装程序在每次全新安装结束时都提示重启？

安装程序提示重启是因为它认为系统已发生更改，需要重启才能完成配置。

例如，如果您选择了 WSL 引擎，安装程序会添加所需的 Windows 功能。安装这些功能后，系统需要重启以完成配置，从而使 WSL 引擎能够正常工作。

您可以通过在命令行启动安装程序时使用 `/norestart` 选项来抑制重启：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /norestart
```

### 为什么在使用 Intune 或其他 MDM 解决方案安装 MSI 时没有自动填充 `docker-users` 组？

MDM 解决方案通常在系统帐户（system account）上下文中安装应用程序。这意味着 `docker-users` 组不会被填充为用户的帐户，因为系统帐户无权访问用户的上下文。

作为一个例子，您可以通过在提升的命令提示符中使用 `psexec` 运行安装程序来复现此情况：

```powershell
psexec -i -s msiexec /i "DockerDesktop.msi"
```
安装应该会成功完成，但 `docker-users` 组不会被填充。

作为一种变通方法，您可以创建一个在用户帐户上下文中运行的脚本。

该脚本负责创建 `docker-users` 组并向其中添加正确的用户。

以下是一个创建 `docker-users` 组并将当前用户添加其中的示例脚本（具体要求可能因环境而异）：

```powershell
$Group = "docker-users"
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

# 创建组
New-LocalGroup -Name $Group

# 将用户添加到组
Add-LocalGroupMember -Group $Group -Member $CurrentUser
```

> [!NOTE]
>
> 将新用户添加到 `docker-users` 组后，用户必须注销并重新登录才能使更改生效。

## MDM

有关使用移动设备管理 (MDM) 工具（如 Jamf、Intune 或 Workspace ONE）部署 Docker Desktop 的常见问题。

### 为什么我的 MDM 工具无法一次性应用所有 Docker Desktop 配置设置？

某些 MDM 工具（如 Workspace ONE）可能不支持在单个 XML 文件中应用多个配置设置。在这种情况下，您可能需要将每个设置部署在单独的 XML 文件中。

请参阅您的 MDM 提供商文档，了解具体的部署要求或限制。
