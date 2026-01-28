---
description: 开始使用 Docker for Windows。本指南涵盖系统要求、下载位置以及安装和更新说明。
keywords: docker for windows, docker windows, docker desktop for windows, docker on
  windows, install docker windows, install docker on windows, docker windows 10, docker
  run on windows, installing docker for windows, windows containers, wsl, hyper-v
title: 在 Windows 上安装 Docker Desktop
linkTitle: Windows
weight: 30
aliases:
- /desktop/windows/install/
- /docker-ee-for-windows/install/
- /docker-for-windows/install-windows-home/
- /docker-for-windows/install/
- /ee/docker-ee/windows/docker-ee/
- /engine/installation/windows/
- /engine/installation/windows/docker-ee/
- /install/windows/docker-ee/
- /install/windows/ee-preview/
- /installation/windows/
- /desktop/win/configuring-wsl/
- /desktop/install/windows-install/
---

> **Docker Desktop 条款**
>
> 在大型企业（员工超过 250 人或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页面提供 Docker Desktop on Windows 的下载链接、系统要求和分步安装说明。

{{< button text="Docker Desktop for Windows - x86_64" url="https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64" >}}
{{< button text="Docker Desktop for Windows - x86_64 on the Microsoft Store" url="https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB" >}}
{{< button text="Docker Desktop for Windows - Arm (Early Access)" url="https://desktop.docker.com/win/main/arm64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-arm64" >}}

_有关校验和，请参阅[发行说明](/manuals/desktop/release-notes.md)_

## 系统要求

> [!TIP]
>
> **我应该使用 Hyper-V 还是 WSL？**
>
> Docker Desktop 在 WSL 和 Hyper-V 上的功能保持一致，对任一架构没有偏好。Hyper-V 和 WSL 各有优缺点，具体取决于您的特定设置和计划的使用场景。

{{< tabs >}}
{{< tab name="WSL 2 后端，x86_64" >}}

- WSL 版本 2.1.5 或更高。
- Windows 11 64 位：Home 或 Pro 版本 22H2 或更高，或 Enterprise 或 Education 版本 22H2 或更高。
- Windows 10 64 位：最低要求是 Home 或 Pro 22H2（内部版本 19045）或更高，或 Enterprise 或 Education 22H2（内部版本 19045）或更高。
- 在 Windows 上启用 WSL 2 功能。有关详细说明，请参阅 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 在 Windows 10 或 Windows 11 上成功运行 WSL 2 需要以下硬件先决条件：
  - 具有[二级地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 4GB 系统内存
  - 在 BIOS/UEFI 中启用硬件虚拟化。有关更多信息，请参阅[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#docker-desktop-fails-due-to-virtualization-not-working)。

有关使用 Docker Desktop 设置 WSL 2 的更多信息，请参阅 [WSL](/manuals/desktop/features/wsl/_index.md)。

> [!NOTE]
>
> Docker 仅在仍在 [Microsoft 服务时间线](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet)内的 Windows 版本上支持 Docker Desktop on Windows。Docker Desktop 不支持服务器版本的 Windows，如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 的官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 Windows 容器，您需要 Windows 10 或 Windows 11 Professional 或 Enterprise 版本。
> Windows Home 或 Education 版本只允许您运行 Linux 容器。

{{< /tab >}}
{{< tab name="Hyper-V 后端，x86_64" >}}

- Windows 11 64 位：Enterprise、Pro 或 Education 版本 22H2 或更高。
- Windows 10 64 位：Enterprise、Pro 或 Education 版本 22H2（内部版本 19045）或更高。
- 启用 Hyper-V 和容器 Windows 功能。
- 在 Windows 10 上成功运行客户端 Hyper-V 需要以下硬件先决条件：

  - 具有[二级地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 4GB 系统内存
  - 在 BIOS/UEFI 设置中启用 BIOS/UEFI 级别的硬件虚拟化支持。有关更多信息，请参阅[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!NOTE]
>
> Docker 仅在仍在 [Microsoft 服务时间线](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet)内的 Windows 版本上支持 Docker Desktop on Windows。Docker Desktop 不支持服务器版本的 Windows，如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 的官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 Windows 容器，您需要 Windows 10 或 Windows 11 Professional 或 Enterprise 版本。
> Windows Home 或 Education 版本只允许您运行 Linux 容器。

{{< /tab >}}
{{< tab name="WSL 2 后端，Arm（抢先体验）" >}}

- WSL 版本 2.1.5 或更高。
- Windows 11 64 位：Home 或 Pro 版本 22H2 或更高，或 Enterprise 或 Education 版本 22H2 或更高。
- Windows 10 64 位：最低要求是 Home 或 Pro 22H2（内部版本 19045）或更高，或 Enterprise 或 Education 22H2（内部版本 19045）或更高。
- 在 Windows 上启用 WSL 2 功能。有关详细说明，请参阅 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 在 Windows 10 或 Windows 11 上成功运行 WSL 2 需要以下硬件先决条件：
  - 具有[二级地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 4GB 系统内存
  - 在 BIOS/UEFI 中启用硬件虚拟化。有关更多信息，请参阅[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!IMPORTANT]
>
> 不支持 Windows 容器。

{{< /tab >}}
{{< /tabs >}}

使用 Docker Desktop 创建的容器和镜像在安装了 Docker Desktop 的机器上的所有用户账户之间共享。这是因为所有 Windows 账户使用相同的虚拟机来构建和运行容器。请注意，使用 Docker Desktop WSL 2 后端时，无法在用户账户之间共享容器和镜像。

Docker Business 客户支持在 VMware ESXi 或 Azure 虚拟机内运行 Docker Desktop。
这需要首先在虚拟化管理程序上启用嵌套虚拟化。
有关更多信息，请参阅[在虚拟机或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md)。

{{< accordion title="如何在 Windows 和 Linux 容器之间切换？" >}}

从 Docker Desktop 菜单中，您可以切换 Docker CLI 与哪个守护进程（Linux 或 Windows）通信。选择 **Switch to Windows containers** 使用 Windows 容器，或选择 **Switch to Linux containers** 使用 Linux 容器（默认）。

有关 Windows 容器的更多信息，请参阅以下文档：

- Microsoft 关于 [Windows 容器](https://docs.microsoft.com/en-us/virtualization/windowscontainers/about/index)的文档。

- [构建并运行您的第一个 Windows Server 容器（博客文章）](https://www.docker.com/blog/build-your-first-docker-windows-server-container/)快速介绍了如何在 Windows 10 和 Windows Server 2016 评估版上构建和运行原生 Docker Windows 容器。

- [Windows 容器入门（实验室）](https://github.com/docker/labs/blob/master/windows/windows-containers/README.md)向您展示如何使用 [MusicStore](https://github.com/aspnet/MusicStore/) 应用程序与 Windows 容器。MusicStore 是一个标准的 .NET 应用程序，[在此处分支以使用容器](https://github.com/friism/MusicStore)，是一个很好的多容器应用程序示例。

- 要了解如何从本地主机连接到 Windows 容器，请参阅[我想从主机连接到容器](/manuals/desktop/features/networking.md#i-want-to-connect-to-a-container-from-the-host)

> [!NOTE]
>
> 当您切换到 Windows 容器时，**Settings** 仅显示活动并适用于 Windows 容器的选项卡。

如果您在 Windows 容器模式下设置代理或守护进程配置，这些设置仅适用于 Windows 容器。如果您切换回 Linux 容器，代理和守护进程配置将恢复为您为 Linux 容器设置的内容。您的 Windows 容器设置会被保留，并在您切换回时再次可用。

{{< /accordion >}}

## 管理员权限和安装要求

安装 Docker Desktop 需要管理员权限。但是，一旦安装完成，可以在没有管理员权限的情况下使用。不过，某些操作仍需要提升的权限。请参阅[了解 Windows 的权限要求](./windows-permission-requirements.md)以获取更多详细信息。

如果您的用户没有管理员权限并计划执行需要提升权限的操作，请确保使用 `--always-run-service` 安装程序标志安装 Docker Desktop。这确保这些操作仍然可以执行，而无需提示用户账户控制（UAC）提升。有关更多详细信息，请参阅[安装程序标志](#installer-flags)。

## WSL：验证和设置

如果您选择使用 WSL，首先通过在终端中运行以下命令来验证您安装的版本是否满足系统要求：

```console
wsl --version
```

如果版本详细信息没有显示，您可能正在使用收件箱版本的 WSL。此版本不支持现代功能，必须更新。

您可以使用以下方法之一更新或安装 WSL：

### 选项 1：通过终端安装或更新 WSL

1. 以管理员模式打开 PowerShell 或 Windows 命令提示符。
2. 运行安装或更新命令。系统可能会提示您重新启动机器。有关更多信息，请参阅[安装 WSL](https://learn.microsoft.com/en-us/windows/wsl/install)。
```console
wsl --install

wsl --update
```

### 选项 2：通过 MSI 包安装 WSL

如果由于安全策略而阻止访问 Microsoft Store：
1. 前往官方 [WSL GitHub 发布页面](https://github.com/microsoft/WSL/releases)。
2. 从最新稳定版本（在 Assets 下拉菜单下）下载 `.msi` 安装程序。
3. 运行下载的安装程序并按照设置说明操作。

## 在 Windows 上安装 Docker Desktop

> [!TIP]
>
> 请参阅[常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md#how-do-i-run-docker-desktop-without-administrator-privileges)，了解如何在不需要管理员权限的情况下安装和运行 Docker Desktop。

### 交互式安装

1. 使用页面顶部的下载按钮或从[发行说明](/manuals/desktop/release-notes.md)下载安装程序。

2. 双击 `Docker Desktop Installer.exe` 运行安装程序。默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。

3. 出现提示时，确保根据您选择的后端，在配置页面上选择或不选择 **Use WSL 2 instead of Hyper-V** 选项。

    在只支持一种后端的系统上，Docker Desktop 会自动选择可用的选项。

4. 按照安装向导上的说明授权安装程序并继续安装。

5. 安装成功后，选择 **Close** 完成安装过程。

6. [启动 Docker Desktop](#start-docker-desktop)。

如果您的管理员账户与用户账户不同，您必须将用户添加到 **docker-users** 组才能访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机或使用 Windows 容器：

1. 以**管理员**身份运行**计算机管理**。
2. 导航到**本地用户和组** > **组** > **docker-users**。
3. 右键单击将用户添加到组。
4. 注销并重新登录以使更改生效。

### 从命令行安装

下载 `Docker Desktop Installer.exe` 后，在终端中运行以下命令来安装 Docker Desktop：

```console
$ "Docker Desktop Installer.exe" install
```

如果您使用 PowerShell，应运行：

```powershell
Start-Process 'Docker Desktop Installer.exe' -Wait install
```

如果使用 Windows 命令提示符：

```sh
start /w "" "Docker Desktop Installer.exe" install
```

默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。

#### 安装程序标志

> [!NOTE]
>
> 如果您使用 PowerShell，需要在任何标志之前使用 `ArgumentList` 参数。
> 例如：
> ```powershell
> Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'
> ```

如果您的管理员账户与用户账户不同，您必须将用户添加到 **docker-users** 组才能访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机或使用 Windows 容器。

```console
$ net localgroup docker-users <user> /add
```

`install` 命令接受以下标志：

##### 安装行为

- `--quiet`：运行安装程序时抑制信息输出
- `--accept-license`：立即接受 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)，而不是在首次运行应用程序时要求接受
- `--installation-dir=<path>`：更改默认安装位置（`C:\Program Files\Docker\Docker`）
- `--backend=<backend name>`：选择 Docker Desktop 使用的默认后端，`hyper-v`、`windows` 或 `wsl-2`（默认）
- `--always-run-service`：安装完成后，启动 `com.docker.service` 并将服务启动类型设置为自动。这避免了需要管理员权限的需要，否则启动 `com.docker.service` 需要管理员权限。Windows 容器和 Hyper-V 后端需要 `com.docker.service`。

##### 安全和访问控制

- `--allowed-org=<org name>`：要求用户在运行应用程序时登录并成为指定 Docker Hub 组织的成员
- `--admin-settings`：自动创建一个 `admin-settings.json` 文件，管理员使用该文件来控制其组织内客户端机器上的某些 Docker Desktop 设置。有关更多信息，请参阅[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。
  - 必须与 `--allowed-org=<org name>` 标志一起使用。
  - 例如：`--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`
- `--no-windows-containers`：禁用 Windows 容器集成。这可以提高安全性。有关更多信息，请参阅 [Windows 容器](/manuals/desktop/setup/install/windows-permission-requirements.md#windows-containers)。

##### 代理配置

- `--proxy-http-mode=<mode>`：设置 HTTP 代理模式，`system`（默认）或 `manual`
- `--override-proxy-http=<URL>`：设置必须用于传出 HTTP 请求的 HTTP 代理的 URL，需要 `--proxy-http-mode` 设置为 `manual`
- `--override-proxy-https=<URL>`：设置必须用于传出 HTTPS 请求的 HTTP 代理的 URL，需要 `--proxy-http-mode` 设置为 `manual`
- `--override-proxy-exclude=<hosts/domains>`：绕过主机和域的代理设置。使用逗号分隔的列表。
- `--proxy-enable-kerberosntlm`：启用 Kerberos 和 NTLM 代理身份验证。如果启用此功能，请确保您的代理服务器已正确配置 Kerberos/NTLM 身份验证。适用于 Docker Desktop 4.32 及更高版本。

##### 数据根目录和磁盘位置

- `--hyper-v-default-data-root=<path>`：指定 Hyper-V 虚拟机磁盘的默认位置。
- `--windows-containers-default-data-root=<path>`：指定 Windows 容器的默认位置。
- `--wsl-default-data-root=<path>`：指定 WSL 分发磁盘的默认位置。

## 启动 Docker Desktop

Docker Desktop 在安装后不会自动启动。要启动 Docker Desktop：

1. 搜索 Docker，然后在搜索结果中选择 **Docker Desktop**。

2. Docker 菜单（{{< inline-image src="images/whale-x.svg" alt="whale menu" >}}）显示 Docker 订阅服务协议。

   {{% include "desktop-license-update.md" %}}

3. 选择 **Accept** 继续。接受条款后 Docker Desktop 启动。

   请注意，如果您不同意条款，Docker Desktop 将不会运行。您可以稍后通过打开 Docker Desktop 来选择接受条款。

   有关更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement/)。建议您阅读[常见问题解答](https://www.docker.com/pricing/faq)。

> [!TIP]
>
> 作为 IT 管理员，您可以使用端点管理（MDM）软件来识别您环境中 Docker Desktop 实例的数量及其版本。这可以提供准确的许可证报告，帮助确保您的机器使用最新版本的 Docker Desktop，并使您能够[强制要求登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
> - [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> - [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> - [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> - [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> - [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## 接下来做什么

- 探索 [Docker 的订阅计划](https://www.docker.com/pricing/)，了解 Docker 能为您提供什么。
- [开始使用 Docker](/get-started/introduction/_index.md)。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)描述了常见问题、解决方法以及如何获取支持。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md)提供常见问题的答案。
- [发行说明](/manuals/desktop/release-notes.md)列出了与 Docker Desktop 版本相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)提供了备份和恢复与 Docker 相关的数据的说明。
