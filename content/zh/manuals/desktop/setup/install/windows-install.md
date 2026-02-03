---
description: Windows 版 Docker 入门。本指南涵盖了系统要求、下载地址以及安装和更新说明。
keywords: docker for windows, docker windows, docker desktop for windows, docker on windows, 安装 docker windows, 安装 docker on windows, docker windows 10, docker run on windows, 安装 docker for windows, windows 容器, wsl, hyper-v
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

> **Docker Desktop 条约**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页提供了 Windows 版 Docker Desktop 的下载链接、系统要求和详细的安装说明。

{{< button text="Docker Desktop for Windows - x86_64" url="https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64" >}}
{{< button text="在 Microsoft Store 下载 Docker Desktop for Windows - x86_64" url="https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB" >}}
{{< button text="Docker Desktop for Windows - Arm (早期体验)" url="https://desktop.docker.com/win/main/arm64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-arm64" >}}

*有关校验和（Checksums），请参阅[发行说明](/manuals/desktop/release-notes.md)*

## 系统要求

> [!TIP]
>
> **我应该使用 Hyper-V 还是 WSL？**
>
> Docker Desktop 在 WSL 和 Hyper-V 上的功能保持一致，对这两种架构没有特定偏好。Hyper-V 和 WSL 各有优缺点，取决于您的具体配置和计划的使用场景。

{{< tabs >}}
{{< tab name="WSL 2 后端, x86_64" >}}

- WSL 版本 2.1.5 或更高。
- Windows 11 64 位：家庭版 (Home) 或专业版 (Pro) 22H2 或更高版本，或者企业版 (Enterprise) 或教育版 (Education) 22H2 或更高版本。
- Windows 10 64 位：最低要求为家庭版或专业版 22H2（内部版本 19045）或更高版本，或者企业版或教育版 22H2（内部版本 19045）或更高版本。
- 在 Windows 上开启 WSL 2 功能。详细说明请参考 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 在 Windows 10 或 Windows 11 上成功运行 WSL 2 需要满足以下硬件前提条件：
  - 具有 [二级地址转换 (SLAT)](https://en.wikipedia.org/wiki/Second_Level_Address_Translation) 的 64 位处理器
  - 4GB 系统内存
  - 在 BIOS/UEFI 中启用硬件虚拟化。有关更多信息，请参阅[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#docker-desktop-fails-due-to-virtualization-not-working)。

有关在 Docker Desktop 中设置 WSL 2 的更多信息，请参阅 [WSL](/manuals/desktop/features/wsl/_index.md)。

> [!NOTE]
>
> Docker 仅对仍处于 [Microsoft 服务时间线内](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet)的 Windows 版本提供 Windows 版 Docker Desktop 支持。Docker Desktop 不支持 Windows 服务器版本，如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 Windows 容器，您需要 Windows 10 或 Windows 11 的专业版 (Professional) 或企业版 (Enterprise)。Windows 家庭版 (Home) 或教育版 (Education) 仅允许运行 Linux 容器。

{{< /tab >}}
{{< tab name="Hyper-V 后端, x86_64" >}}

- Windows 11 64 位：企业版、专业版或教育版 22H2 或更高版本。
- Windows 10 64 位：企业版、专业版或教育版 22H2（内部版本 19045）或更高版本。
- 开启 Windows 功能中的 Hyper-V 和 Containers（容器）。
- 在 Windows 10 上成功运行客户端 Hyper-V 需要满足以下硬件前提条件：

  - 具有 [二级地址转换 (SLAT)](https://en.wikipedia.org/wiki/Second_Level_Address_Translation) 的 64 位处理器
  - 4GB 系统内存
  - 在 BIOS/UEFI 设置中开启 BIOS/UEFI 级别的硬件虚拟化支持。有关更多信息，请参阅[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!NOTE]
>
> Docker 仅对仍处于 [Microsoft 服务时间线内](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet)的 Windows 版本提供 Windows 版 Docker Desktop 支持。Docker Desktop 不支持 Windows 服务器版本，如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 Windows 容器，您需要 Windows 10 或 Windows 11 的专业版 (Professional) 或企业版 (Enterprise)。Windows 家庭版 (Home) 或教育版 (Education) 仅允许运行 Linux 容器。

{{< /tab >}}
{{< tab name="WSL 2 后端, Arm (早期体验)" >}}

- WSL 版本 2.1.5 或更高。
- Windows 11 64 位：家庭版 (Home) 或专业版 (Pro) 22H2 或更高版本，或者企业版 (Enterprise) 或教育版 (Education) 22H2 或更高版本。
- Windows 10 64 位：最低要求为家庭版或专业版 22H2（内部版本 19045）或更高版本，或者企业版或教育版 22H2（内部版本 19045）或更高版本。
- 在 Windows 上开启 WSL 2 功能。详细说明请参考 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 在 Windows 10 或 Windows 11 上成功运行 WSL 2 需要满足以下硬件前提条件：
  - 具有 [二级地址转换 (SLAT)](https://en.wikipedia.org/wiki/Second_Level_Address_Translation) 的 64 位处理器
  - 4GB 系统内存
  - 在 BIOS/UEFI 中启用硬件虚拟化。有关更多信息，请参阅[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!IMPORTANT]
>
> 不支持 Windows 容器。

{{< /tab >}}
{{< /tabs >}}

在使用 Docker Desktop 安装的机器上，所创建的容器和镜像是所有用户帐户共享的。这是因为所有的 Windows 帐户都使用同一个 VM 来构建和运行容器。请注意，在使用 Docker Desktop WSL 2 后端时，无法在用户帐户之间共享容器和镜像。

Docker Business 客户支持在 VMware ESXi 或 Azure VM 中运行 Docker Desktop。这需要先在虚拟机管理程序上启用嵌套虚拟化。有关更多信息，请参阅[在 VM 或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md)。

{{< accordion title="如何在 Windows 和 Linux 容器之间切换？" >}}

通过 Docker Desktop 菜单，您可以切换 Docker CLI 通信的守护进程（Linux 或 Windows）。选择 **Switch to Windows containers** 以使用 Windows 容器，或者选择 **Switch to Linux containers** 以使用 Linux 容器（默认）。

有关 Windows 容器的更多信息，请参考以下文档：

- Microsoft 关于 [Windows 容器](https://docs.microsoft.com/en-us/virtualization/windowscontainers/about/index) 的文档。

- [构建并运行您的第一个 Windows Server 容器 (博客文章)](https://www.docker.com/blog/build-your-first-docker-windows-server-container/) 快速演示了如何在 Windows 10 和 Windows Server 2016 评估版上构建和运行原生的 Docker Windows 容器。

- [Windows 容器入门 (实验室)](https://github.com/docker/labs/blob/master/windows/windows-containers/README.md) 向您展示如何将 [MusicStore](https://github.com/aspnet/MusicStore/) 应用程序与 Windows 容器配合使用。MusicStore 是一个标准的 .NET 应用程序，[此处已 fork 并容器化](https://github.com/friism/MusicStore)，是多容器应用程序的一个很好示例。

- 要了解如何从本地主机连接到 Windows 容器，请参阅[我想从主机连接到容器](/manuals/desktop/features/networking.md#i-want-to-connect-to-a-container-from-the-host)

> [!NOTE]
>
> 当您切换到 Windows 容器时，**Settings（设置）** 仅显示活动且适用于 Windows 容器的选项卡。

如果您在 Windows 容器模式下设置了代理或守护进程配置，这些仅适用于 Windows 容器。如果您切换回 Linux 容器，代理和守护进程配置将恢复为您为 Linux 容器设置的内容。您的 Windows 容器设置会被保留，并在您切换回来时再次生效。

{{< /accordion >}}

## 管理员权限和安装要求

安装 Docker Desktop 需要管理员权限。但是，一旦安装完成，可以在没有管理员权限的情况下使用。不过，某些操作仍然需要提升权限。有关更多详细信息，请参阅[了解 Windows 的权限要求](./windows-permission-requirements.md)。

如果您的用户没有管理员权限且计划执行需要提升权限的操作，请务必使用 `--always-run-service` 安装程序标志安装 Docker Desktop。这可以确保这些操作在执行时不会提示用户帐户控制 (UAC) 权限提升。有关更多详细信息，请参阅[安装程序标志](#安装程序标志)。

## WSL：验证与设置

如果您选择使用 WSL，请先在终端中运行以下命令，验证安装的版本是否符合系统要求：

```console
wsl --version
```

如果未显示版本详情，说明您可能正在使用 Windows 内置的旧版 WSL。该版本不支持现代功能，必须进行更新。

您可以使用以下方法之一更新或安装 WSL：

### 选项 1：通过终端安装或更新 WSL

1. 以管理员模式打开 PowerShell 或 Windows 命令提示符。
2. 运行安装或更新命令。可能会提示您重启机器。有关更多信息，请参考 [安装 WSL](https://learn.microsoft.com/en-us/windows/wsl/install)。
```console
wsl --install

wsl --update
```

### 选项 2：通过 MSI 软件包安装 WSL

如果因安全策略阻止了 Microsoft Store 的访问：
1. 前往官方 [WSL GitHub 发行页面 (Releases)](https://github.com/microsoft/WSL/releases)。
2. 从最新的稳定版本中下载 `.msi` 安装程序（在 Assets 下拉菜单下）。
3. 运行下载的安装程序并按照设置说明操作。

## 在 Windows 上安装 Docker Desktop

> [!TIP]
>
> 有关如何在不需要管理员权限的情况下安装和运行 Docker Desktop，请参阅 [常见问题解答 (FAQ)](/manuals/desktop/troubleshoot-and-support/faqs/general.md#how-do-i-run-docker-desktop-without-administrator-privileges)。

### 交互式安装

1. 使用页面顶部的下载按钮或从[发行说明](/manuals/desktop/release-notes.md)下载安装程序。

2. 双击 `Docker Desktop Installer.exe` 以运行安装程序。默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。

3. 出现提示时，根据您对后端的选择，确保选中或取消选中配置页面上的 **Use WSL 2 instead of Hyper-V** 选项。

    在仅支持一种后端的系统上，Docker Desktop 会自动选择可用选项。

4. 按照安装向导上的说明授权安装程序并继续安装。

5. 安装成功后，选择 **Close（关闭）** 以完成安装过程。

6. [启动 Docker Desktop](#启动-docker-desktop)。

如果您的管理员帐户与用户帐户不同，则必须将该用户添加到 **docker-users** 组，以便访问需要更高权限的功能，例如创建和管理 Hyper-V VM，或使用 Windows 容器：

1. 以 **管理员** 身份运行 **计算机管理 (Computer Management)**。
2. 导航到 **本地用户和组 (Local Users and Groups)** > **组 (Groups)** > **docker-users**。
3. 右键点击将该用户添加到组中。
4. 注销并重新登录以使更改生效。

### 通过命令行安装

下载 `Docker Desktop Installer.exe` 后，在终端中运行以下命令来安装 Docker Desktop：

```console
$ "Docker Desktop Installer.exe" install
```

如果您使用的是 PowerShell，则应运行：

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
> 如果您使用的是 PowerShell，则需要在任何标志之前使用 `ArgumentList` 参数。
> 例如：
> ```powershell
> Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'
> ```

如果您的管理员帐户与用户帐户不同，必须将该用户添加到 **docker-users** 组，以访问需要更高权限的功能，例如创建和管理 Hyper-V VM，或使用 Windows 容器。

```console
$ net localgroup docker-users <user> /add
```

`install` 命令接受以下标志：

##### 安装行为

- `--quiet`：运行安装程序时抑制信息输出
- `--accept-license`：立即接受 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)，而不需要在首次运行应用程序时接受
- `--installation-dir=<path>`：更改默认安装位置 (`C:\Program Files\Docker\Docker`)
- `--backend=<backend name>`：选择用于 Docker Desktop 的默认后端：`hyper-v`、`windows` 或 `wsl-2`（默认）
- `--always-run-service`：安装完成后，启动 `com.docker.service` 并将服务启动类型设置为“自动”。这绕过了启动 `com.docker.service` 所需的管理员权限需求。Windows 容器和 Hyper-V 后端需要 `com.docker.service`。

##### 安全与访问控制

- `--allowed-org=<org name>`：要求用户在运行应用程序时登录并属于指定的 Docker Hub 组织
- `--admin-settings`：自动创建一个 `admin-settings.json` 文件，管理员可以使用该文件控制其组织内客户机上的某些 Docker Desktop 设置。有关更多信息，请参阅[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。
  - 必须与 `--allowed-org=<org name>` 标志配合使用。
  - 例如：`--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`
- `--no-windows-containers`：禁用 Windows 容器集成。这可以提高安全性。有关更多信息，请参阅 [Windows 容器](/manuals/desktop/setup/install/windows-permission-requirements.md#windows-containers)。

##### 代理配置

- `--proxy-http-mode=<mode>`：设置 HTTP 代理模式：`system`（默认）或 `manual`
- `--override-proxy-http=<URL>`：设置传出 HTTP 请求必须使用的 HTTP 代理 URL，要求 `--proxy-http-mode` 为 `manual`
- `--override-proxy-https=<URL>`：设置传出 HTTPS 请求必须使用的 HTTP 代理 URL，要求 `--proxy-http-mode` 为 `manual`
- `--override-proxy-exclude=<hosts/domains>`：为指定的主机和域名绕过代理设置。使用逗号分隔的列表。
- `--proxy-enable-kerberosntlm`：启用 Kerberos 和 NTLM 代理身份验证。如果您启用了此项，请确保您的代理服务器已正确配置 Kerberos/NTLM 身份验证。适用于 Docker Desktop 4.32 及更高版本。

##### 数据根目录和磁盘位置

- `--hyper-v-default-data-root=<path>`：指定 Hyper-V VM 磁盘的默认位置。
- `--windows-containers-default-data-root=<path>`：指定 Windows 容器的默认位置。
- `--wsl-default-data-root=<path>`：指定 WSL 发行版磁盘的默认位置。

## 启动 Docker Desktop

安装完成后，Docker Desktop 不会自动启动。启动 Docker Desktop：

1. 搜索 Docker，并在搜索结果中选择 **Docker Desktop**。

2. Docker 菜单 ({{< inline-image src="images/whale-x.svg" alt="鲸鱼菜单" >}}) 将显示 Docker 订阅服务协议。

   {{% include "desktop-license-update.md" %}}

3. 选择 **Accept（接受）** 继续。接受条款后，Docker Desktop 将启动。

   请注意，如果您不同意条款，Docker Desktop 将无法运行。您可以稍后通过打开 Docker Desktop 来选择接受条款。

   有关更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement/)。建议您阅读 [常见问题解答 (FAQ)](https://www.docker.com/pricing/faq)。

> [!TIP]
>
> 作为 IT 管理员，您可以使用终端管理 (MDM) 软件来识别环境中的 Docker Desktop 实例数量及其版本。这可以提供准确的许可报告，帮助确保您的机器使用最新版本的 Docker Desktop，并允许您[强制执行登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
> - [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> - [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> - [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> - [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> - [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## 下一步

- 探索 [Docker 订阅方案](https://www.docker.com/pricing/)，了解 Docker 还能为您提供什么。
- [Docker 入门教程](/get-started/introduction/_index.md)。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有特性。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 介绍了常见问题、解决方案以及如何获取支持。
- [常见问题解答 (FAQ)](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的解答。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发行版相关的组件更新、新功能和改进。
- [备份与还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和还原 Docker 相关数据的说明。