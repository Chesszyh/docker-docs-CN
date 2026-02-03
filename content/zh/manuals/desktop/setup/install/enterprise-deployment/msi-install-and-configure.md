---
title: MSI 安装程序
description: 了解如何使用 MSI 安装程序，并探索其他配置选项。
keywords: msi, windows, docker desktop, 安装, 部署, 配置, 管理员, admin, mdm
tags: [admin]
weight: 10
aliases:
- /desktop/install/msi/install-and-configure/
- /desktop/setup/install/msi/install-and-configure/
- /desktop/install/msi/
- /desktop/setup/install/msi/
---

{{< summary-bar feature_name="MSI 安装程序" >}}

MSI 软件包支持各种 MDM（移动设备管理）解决方案，非常适合批量安装，并消除了单个用户手动设置的需要。通过此软件包，IT 管理员可以确保 Docker Desktop 的标准化、策略驱动安装，从而提高整个组织的效率和软件管理水平。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console（管理控制台）**，然后选择 **Enterprise deployment（企业级部署）**。
3. 在 **Windows OS** 选项卡中，选择 **Download MSI installer（下载 MSI 安装程序）** 按钮。
4. 下载完成后，双击 `Docker Desktop Installer.msi` 运行安装程序。
5. 接受许可协议后，选择安装位置。默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。
6. 配置 Docker Desktop 安装选项。您可以：

    - 创建桌面快捷方式

    - 将 Docker Desktop 服务的启动类型设置为自动

    - 禁用 Windows 容器 (Windows Container) 的使用

    - 选择 Docker Desktop 后端：WSL 或 Hyper-V。如果您的系统仅支持其中一种，您将无法选择。
7. 按照安装向导的说明授权安装程序并继续安装。
8. 安装成功后，选择 **Finish（完成）** 以完成安装过程。

如果您的管理员帐户与用户帐户不同，则必须将该用户添加到 **docker-users** 组，以便访问需要更高权限的功能，例如创建和管理 Hyper-V VM，或使用 Windows 容器：

1. 以 **管理员** 身份运行 **计算机管理 (Computer Management)**。
2. 导航到 **本地用户和组 (Local Users and Groups)** > **组 (Groups)** > **docker-users**。
3. 右键点击将该用户添加到组中。
4. 注销并重新登录以使更改生效。

> [!NOTE]
>
> 使用 MSI 安装 Docker Desktop 时，应用内更新会自动禁用。这确保了组织可以保持版本一致性并防止未经批准的更新。对于使用 .exe 安装程序安装的 Docker Desktop，仍支持应用内更新。
>
> 当有更新可用时，Docker Desktop 会通知您。要更新 Docker Desktop，请从 Docker 管理控制台下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要了解最新版本信息，请查看 [发行说明](/manuals/desktop/release-notes.md) 页面。

## 通过命令行安装

本节涵盖使用 PowerShell 命令行安装 Docker Desktop 的方法。它提供了您可以运行的常用安装命令。您还可以添加其他参数，具体见[配置选项](#配置选项)。

安装 Docker Desktop 时，您可以选择交互式或非交互式安装。

交互式安装（不指定 `/quiet` 或 `/qn` 参数）会显示用户界面并允许您选择自己的属性。

通过用户界面安装时，可以：

- 选择目标文件夹
- 创建桌面快捷方式
- 配置 Docker Desktop 服务启动类型
- 禁用 Windows 容器
- 在 WSL 或 Hyper-V 引擎之间选择

非交互式安装是静默进行的，任何额外配置都必须作为参数传递。

### 常用安装命令

> [!IMPORTANT]
>
> 运行以下任何命令都需要管理员权限。

#### 交互式安装并开启详细日志记录

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log"
```

#### 交互式安装且不开启详细日志记录

```powershell
msiexec /i "DockerDesktop.msi"
```

#### 非交互式安装并开启详细日志记录

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet
```

#### 非交互式安装并抑制重启

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart
```

#### 使用管理员设置进行非交互式安装

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart ADMINSETTINGS="{"configurationFileVersion":2,"enhancedContainerIsolation":{"value":true,"locked":false}}" ALLOWEDORG="your-organization"
```

#### 以交互方式安装，并允许用户在无管理员权限的情况下切换到 Windows 容器

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart ALLOWEDORG="your-organization" ALWAYSRUNSERVICE=1
```

#### 使用被动显示选项安装

当您想要执行非交互式安装但显示进度对话框时，可以使用 `/passive` 显示选项代替 `/quiet`。

在被动模式下，安装程序不会向用户显示任何提示或错误消息，且安装无法取消。

例如：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /passive /norestart
```

> [!TIP]
>
> 在创建需要 JSON 字符串的值时：
>
> - 属性需要一个符合 JSON 格式的字符串
> - 该字符串应包含在双引号内
> - 该字符串不应包含任何空格
> - 属性名应在双引号内

### 常用卸载命令

卸载 Docker Desktop 时，您需要使用当初用于安装该应用程序的同一个 `.msi` 文件。

如果您不再保留原始的 `.msi` 文件，则需要使用与该安装关联的产品代码 (Product Code)。要查找产品代码，请运行：

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

#### 交互式卸载并开启详细日志记录

```powershell
msiexec /x "DockerDesktop.msi" /L*V ".\msi.log"
```

#### 交互式卸载且不开启详细日志记录

```powershell
msiexec /x "DockerDesktop.msi"
```

#### 非交互式卸载并开启详细日志记录

```powershell
msiexec /x "DockerDesktop.msi" /L*V ".\msi.log" /quiet
```

#### 非交互式卸载且不开启详细日志记录

```powershell
msiexec /x "DockerDesktop.msi" /quiet
```

### 配置选项

> [!IMPORTANT]
>
> 除了以下自定义属性外，Docker Desktop MSI 安装程序还支持标准的 [Windows Installer 命令行选项](https://learn.microsoft.com/en-us/windows/win32/msi/standard-installer-command-line-options)。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ENABLEDESKTOPSHORTCUT` | 创建桌面快捷方式。 | 1 |
| `INSTALLFOLDER` | 指定 Docker Desktop 的自定义安装位置。 | C:\Program Files\Docker |
| `ADMINSETTINGS` | 自动创建一个 `admin-settings.json` 文件，用于在组织内的客户机上[控制某些 Docker Desktop 设置](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。它必须与 `ALLOWEDORG` 属性配合使用。 | 无 |
| `ALLOWEDORG` | 要求用户在运行应用程序时登录并属于指定的 Docker Hub 组织。这会在 `HKLM\Software\Policies\Docker\Docker Desktop` 中创建一个名为 `allowedOrgs` 的注册表项。 | 无 |
| `ALWAYSRUNSERVICE` | 允许用户在不需要管理员权限的情况下切换到 Windows 容器 | 0 |
| `DISABLEWINDOWSCONTAINERS` | 禁用 Windows 容器集成 | 0 |
| `ENGINE` | 设置用于运行容器的 Docker 引擎。可以是 `wsl`、`hyperv` 或 `windows` | `wsl` |
| `PROXYENABLEKERBEROSNTLM` | 设置为 1 时，启用对 Kerberos 和 NTLM 代理身份验证的支持。适用于 Docker Desktop 4.33 及更高版本 | 0 |
| `PROXYHTTPMODE` | 设置 HTTP 代理模式。可以是 `system` 或 `manual` | `system` |
| `OVERRIDEPROXYHTTP` | 设置用于传出 HTTP 请求的 HTTP 代理 URL。 | 无 |
| `OVERRIDEPROXYHTTPS` | 设置用于传出 HTTPS 请求的 HTTP 代理 URL。 | 无 |
| `OVERRIDEPROXYEXCLUDE` | 为指定的主机和域名绕过代理设置。使用逗号分隔的列表。 | 无 |
| `HYPERVDEFAULTDATAROOT` | 指定 Hyper-V VM 磁盘的默认位置。 | 无 |
| `WINDOWSCONTAINERSDEFAULTDATAROOT` | 指定 Windows 容器的默认数据位置。 | 无 |
| `WSLDEFAULTDATAROOT` | 指定 WSL 发行版磁盘的默认位置。 | 无 |
| `DISABLEANALYTICS` | 设置为 1 时，将对 MSI 禁用分析数据收集。有关更多信息，请参阅[分析 (Analytics)](#分析)。 | 0 |


此外，您还可以使用 `/norestart` 或 `/forcerestart` 来控制重启行为。

默认情况下，安装程序在安装成功后会重启机器。在静默模式运行时，重启是自动进行的，不会提示用户。

## 分析 (Analytics)

MSI 安装程序仅收集与安装相关的匿名使用统计信息。这是为了更好地了解用户行为，并通过识别和解决问题或优化常用功能来改善用户体验。

### 如何选择退出 (Opt-out)

{{< tabs >}}
{{< tab name="通过图形界面 (GUI)" >}}

从默认安装程序 GUI 安装 Docker Desktop 时，勾选 **Welcome** 对话框左下角的 **Disable analytics（禁用分析）** 复选框。

{{< /tab >}}
{{< tab name="通过命令行" >}}

通过命令行安装 Docker Desktop 时，使用 `DISABLEANALYTICS` 属性。

```powershell
msiexec /i "win\msi\bin\en-US\DockerDesktop.msi" /L*V ".\msi.log" DISABLEANALYTICS=1
```

{{< /tab >}}
{{< /tabs >}}

### 持久性 (Persistence)

如果您决定在安装时禁用分析，您的选择将持久保存在注册表中，并在未来的升级和卸载中得到遵循。

但是，该注册表项在卸载 Docker Desktop 时会被移除，必须通过上述方法之一再次进行配置。

注册表项如下：

```powershell
SOFTWARE\Docker Inc.\Docker Desktop\DisableMsiAnalytics
```

当分析被禁用时，此项被设置为 `1`。

## 额外资源

- [浏览常见问题解答 (FAQ)](faq.md)
