---
title: MSI 安装程序
description: 了解如何使用 MSI 安装程序。同时探索其他配置选项。
keywords: msi, windows, docker desktop, install, deploy, configure, admin, mdm
tags: [admin]
weight: 10
aliases:
- /desktop/install/msi/install-and-configure/
- /desktop/setup/install/msi/install-and-configure/
- /desktop/install/msi/
- /desktop/setup/install/msi/
---

{{< summary-bar feature_name="MSI installer" >}}

MSI 软件包支持各种 MDM（移动设备管理）解决方案，非常适合批量安装，无需个人用户手动设置。借助此软件包，IT 管理员可以确保 Docker Desktop 的标准化、策略驱动安装，提高其组织的效率和软件管理水平。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 从 **Windows OS** 选项卡中，选择 **Download MSI installer** 按钮。
4. 下载完成后，双击 `Docker Desktop Installer.msi` 运行安装程序。
5. 接受许可协议后，选择安装位置。默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。
6. 配置 Docker Desktop 安装。您可以：

    - 创建桌面快捷方式

    - 将 Docker Desktop 服务启动类型设置为自动

    - 禁用 Windows 容器使用

    - 选择 Docker Desktop 后端：WSL 或 Hyper-V。如果您的系统只支持其中一个，您将无法选择。
7. 按照安装向导上的说明授权安装程序并继续安装。
8. 安装成功后，选择 **Finish** 完成安装过程。

如果您的管理员帐户与用户帐户不同，您必须将用户添加到 **docker-users** 组才能访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机或使用 Windows 容器：

1. 以 **管理员** 身份运行 **计算机管理**。
2. 导航到 **本地用户和组** > **组** > **docker-users**。
3. 右键单击以将用户添加到组。
4. 注销并重新登录以使更改生效。

> [!NOTE]
>
> 使用 MSI 安装 Docker Desktop 时，应用内更新会自动禁用。这确保组织可以保持版本一致性并防止未经批准的更新。对于使用 .exe 安装程序安装的 Docker Desktop，应用内更新仍然受支持。
>
> Docker Desktop 会在有更新可用时通知您。要更新 Docker Desktop，请从 Docker Admin Console 下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要了解最新版本，请查看[发行说明](/manuals/desktop/release-notes.md)页面。

## 从命令行安装

本节介绍使用 PowerShell 从命令行安装 Docker Desktop。它提供了您可以运行的常用安装命令。您还可以添加[配置选项](#配置选项)中概述的其他参数。

安装 Docker Desktop 时，您可以选择交互式或非交互式安装。

交互式安装，不指定 `/quiet` 或 `/qn`，会显示用户界面并让您选择自己的属性。

通过用户界面安装时可以：

- 选择目标文件夹
- 创建桌面快捷方式
- 配置 Docker Desktop 服务启动类型
- 禁用 Windows 容器
- 在 WSL 或 Hyper-V 引擎之间选择

非交互式安装是静默的，任何其他配置必须作为参数传递。

### 常用安装命令

> [!IMPORTANT]
>
> 运行以下任何命令都需要管理员权限。

#### 带详细日志的交互式安装

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log"
```

#### 不带详细日志的交互式安装

```powershell
msiexec /i "DockerDesktop.msi"
```

#### 带详细日志的非交互式安装

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet
```

#### 非交互式安装并抑制重启

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart
```

#### 带管理员设置的非交互式安装

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart ADMINSETTINGS="{"configurationFileVersion":2,"enhancedContainerIsolation":{"value":true,"locked":false}}" ALLOWEDORG="your-organization"
```

#### 交互式安装并允许用户无需管理员权限切换到 Windows 容器

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart ALLOWEDORG="your-organization" ALWAYSRUNSERVICE=1
```

#### 使用被动显示选项安装

当您想执行非交互式安装但显示进度对话框时，可以使用 `/passive` 显示选项代替 `/quiet`。

在被动模式下，安装程序不会向用户显示任何提示或错误消息，安装也无法取消。

例如：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /passive /norestart
```

> [!TIP]
>
> 创建期望 JSON 字符串的值时：
>
> - 属性期望 JSON 格式的字符串
> - 字符串应该用双引号包裹
> - 字符串不应包含任何空白
> - 属性名称应该用双引号包裹

### 常用卸载命令

卸载 Docker Desktop 时，您需要使用最初用于安装应用程序的同一个 `.msi` 文件。

如果您不再拥有原始的 `.msi` 文件，您需要使用与安装关联的产品代码。要查找产品代码，请运行：

```powershell
Get-WmiObject Win32_Product | Select-Object IdentifyingNumber, Name | Where-Object {$_.Name -eq "Docker Desktop"}
```

它应该返回类似以下的输出：

```text
IdentifyingNumber                      Name
-----------------                      ----
{10FC87E2-9145-4D7D-B493-2E99E8D8E103} Docker Desktop
```
> [!NOTE]
>
> 此命令可能需要一些时间，具体取决于已安装应用程序的数量。

`IdentifyingNumber` 是应用程序的产品代码，可用于卸载 Docker Desktop。例如：

```powershell
msiexec /x {10FC87E2-9145-4D7D-B493-2E99E8D8E103} /L*V ".\msi.log" /quiet
```

#### 带详细日志的交互式卸载

```powershell
msiexec /x "DockerDesktop.msi" /L*V ".\msi.log"
```

#### 不带详细日志的交互式卸载

```powershell
msiexec /x "DockerDesktop.msi"
```

#### 带详细日志的非交互式卸载

```powershell
msiexec /x "DockerDesktop.msi" /L*V ".\msi.log" /quiet
```

#### 不带详细日志的非交互式卸载

```powershell
msiexec /x "DockerDesktop.msi" /quiet
```

### 配置选项

> [!IMPORTANT]
>
> 除了以下自定义属性外，Docker Desktop MSI 安装程序还支持标准的 [Windows Installer 命令行选项](https://learn.microsoft.com/en-us/windows/win32/msi/standard-installer-command-line-options)。

| 属性 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `ENABLEDESKTOPSHORTCUT` | 创建桌面快捷方式。 | 1 |
| `INSTALLFOLDER` | 指定 Docker Desktop 安装的自定义位置。 | C:\Program Files\Docker |
| `ADMINSETTINGS` | 自动创建 `admin-settings.json` 文件，用于在组织内的客户端机器上[控制某些 Docker Desktop 设置](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。必须与 `ALLOWEDORG` 属性一起使用。 | 无 |
| `ALLOWEDORG` | 要求用户登录并在运行应用程序时成为指定 Docker Hub 组织的成员。这会在 `HKLM\Software\Policies\Docker\Docker Desktop` 中创建名为 `allowedOrgs` 的注册表项。 | 无 |
| `ALWAYSRUNSERVICE` | 允许用户无需管理员权限切换到 Windows 容器 | 0 |
| `DISABLEWINDOWSCONTAINERS` | 禁用 Windows 容器集成 | 0 |
| `ENGINE` | 设置用于运行容器的 Docker 引擎。可以是 `wsl`、`hyperv` 或 `windows` | `wsl` |
| `PROXYENABLEKERBEROSNTLM` | 设置为 1 时，启用 Kerberos 和 NTLM 代理身份验证支持。适用于 Docker Desktop 4.33 及更高版本 | 0 |
| `PROXYHTTPMODE` | 设置 HTTP 代理模式。可以是 `system` 或 `manual` | `system` |
| `OVERRIDEPROXYHTTP` | 设置用于传出 HTTP 请求的 HTTP 代理 URL。 | 无 |
| `OVERRIDEPROXYHTTPS` | 设置用于传出 HTTPS 请求的 HTTP 代理 URL。 | 无 |
| `OVERRIDEPROXYEXCLUDE` | 为主机和域绕过代理设置。使用逗号分隔的列表。 | 无 |
| `HYPERVDEFAULTDATAROOT` | 指定 Hyper-V 虚拟机磁盘的默认位置。 | 无 |
| `WINDOWSCONTAINERSDEFAULTDATAROOT` | 指定 Windows 容器的默认位置。 | 无 |
| `WSLDEFAULTDATAROOT` | 指定 WSL 发行版磁盘的默认位置。 | 无 |
| `DISABLEANALYTICS` | 设置为 1 时，将禁用 MSI 的分析收集。有关更多信息，请参阅[分析](#分析)。 | 0 |


此外，您还可以使用 `/norestart` 或 `/forcerestart` 来控制重启行为。

默认情况下，安装程序在成功安装后重启机器。静默运行时，重启是自动的，不会提示用户。

## 分析

MSI 安装程序仅收集与安装相关的匿名使用统计数据。这是为了更好地了解用户行为，并通过识别和解决问题或优化热门功能来改善用户体验。

### 如何选择退出

{{< tabs >}}
{{< tab name="从 GUI" >}}

从默认安装程序 GUI 安装 Docker Desktop 时，选择位于 **Welcome** 对话框左下角的 **Disable analytics** 复选框。

{{< /tab >}}
{{< tab name="从命令行" >}}

从命令行安装 Docker Desktop 时，使用 `DISABLEANALYTICS` 属性。

```powershell
msiexec /i "win\msi\bin\en-US\DockerDesktop.msi" /L*V ".\msi.log" DISABLEANALYTICS=1
```

{{< /tab >}}
{{< /tabs >}}

### 持久性

如果您决定为安装禁用分析，您的选择将被保存在注册表中，并在未来的升级和卸载中得到尊重。

但是，当 Docker Desktop 被卸载时，该键会被移除，必须通过之前的方法之一重新配置。

注册表项如下：

```powershell
SOFTWARE\Docker Inc.\Docker Desktop\DisableMsiAnalytics
```

当分析被禁用时，此键设置为 `1`。

## 其他资源

- [探索常见问题](faq.md)
