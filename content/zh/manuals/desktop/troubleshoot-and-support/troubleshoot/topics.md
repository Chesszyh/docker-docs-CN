---
description: 探索 Docker Desktop 的常见故障排除主题
keywords: Linux, Mac, Windows, troubleshooting, 故障排除, 主题, Docker Desktop
title: Docker Desktop 故障排除主题
linkTitle: 常见主题
toc_max: 3
tags: [ Troubleshooting ]
weight: 10 
alias:
 - /desktop/troubleshoot/topics/
 - /manuals/desktop/troubleshoot-and-support/troubleshoot/workarounds/
---

> [!TIP]
>
> 如果在故障排除中未找到解决方案，可以浏览 GitHub 仓库或创建新问题：
>
> - [docker/for-mac](https://github.com/docker/for-mac/issues)
> - [docker/for-win](https://github.com/docker/for-win/issues)
> - [docker/for-linux](https://github.com/docker/for-linux/issues)

## 适用于所有平台的主题

### 证书设置不正确

#### 错误消息

尝试使用 `docker run` 从注册表拉取时，可能会遇到以下错误：

```console
Error response from daemon: Get http://192.168.203.139:5858/v2/: malformed HTTP response "\x15\x03\x01\x00\x02\x02"
```

此外，来自注册表的日志可能显示：

```console
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52882: tls: client didn't provide a certificate
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52883: tls: first record does not look like a TLS handshake
```

#### 可能的原因

- Docker Desktop 会忽略列在非安全注册表（insecure registries）下的证书。
- 客户端证书未发送到非安全注册表，导致握手失败。

#### 解决方案

- 确保您的注册表已正确配置了有效的 SSL 证书。
- 如果您的注册表是自签名的，请将证书添加到 Docker 的证书目录（Linux 上为 `/etc/docker/certs.d/`），配置 Docker 信任该证书。
- 如果问题仍然存在，请检查您的 Docker 守护进程配置并启用 TLS 身份验证。

### Docker Desktop UI 显示为绿色、扭曲或有视觉伪影

#### 原因

Docker Desktop 默认使用硬件加速图形，这可能会导致某些 GPU 出现问题。

#### 解决方案

禁用硬件加速：

1. 编辑 Docker Desktop 的 `settings-store.json` 文件（对于 Docker Desktop 4.34 及更早版本，该文件名为 `settings.json`）。您可以在以下路径找到此文件：

   - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
   - Windows: `C:\Users\[用户名]\AppData\Roaming\Docker\settings-store.json`
   - Linux: `~/.docker/desktop/settings-store.json`

2. 添加以下条目：

   ```JSON
   "disableHardwareAcceleration": true
   ```

3. 保存文件并重启 Docker Desktop。

### 使用挂载卷时出现运行时错误，提示找不到应用程序文件、访问卷挂载被拒绝或服务无法启动

#### 原因

如果您的项目目录位于家目录 (`/home/<user>`) 之外，Docker Desktop 需要文件共享权限才能访问它。

#### 解决方案

在 Mac 和 Linux 版 Docker Desktop 中启用文件共享：

1. 导航到 **Settings**，选择 **Resources**，然后选择 **File sharing**。
2. 添加包含 Dockerfile 和卷挂载路径的驱动器或文件夹。

在 Windows 版 Docker Desktop 中启用文件共享：

1. 在 **Settings** 中，选择 **Shared Folders**。
2. 共享包含 Dockerfile 和卷挂载路径的文件夹。

### `port already allocated` (端口已被占用) 错误

#### 错误消息

启动容器时，可能会看到如下错误：

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

或

```text
listen tcp:0.0.0.0:8080: bind: address is already in use
```

#### 原因

- 系统上的另一个应用程序已经在使用指定的端口。
- 之前运行的容器未正常停止，仍绑定在该端口上。

#### 解决方案

要查明是哪个软件占用了端口，可以：
- 使用 `resmon.exe` 图形界面，选择 **网络**，然后查看 **侦听端口**。
- 在 PowerShell 中，使用 `netstat -aon | find /i "listening "` 查找当前使用该端口的进程 PID（PID 是最右侧一列的数字）。

然后，决定是关闭该进程，还是在 Docker 应用中使用其他端口。

## 适用于 Linux 和 Mac 的主题

### Docker Desktop 在 Mac 或 Linux 平台上启动失败

#### 错误消息

由于 Unix 域套接字路径长度限制，Docker 无法启动：

```console
[vpnkit-bridge][F] listen unix <HOME>/Library/Containers/com.docker.docker/Data/http-proxy-control.sock: bind: invalid argument
```

```console
[com.docker.backend][E] listen(vsock:4099) failed: listen unix <HOME>/Library/Containers/com.docker.docker/Data/vms/0/00000002.00001003: bind: invalid argument
```

#### 原因

在 Mac 和 Linux 上，Docker Desktop 会创建用于进程间通信的 Unix 域套接字。这些套接字创建在用户的家目录下。

Unix 域套接字有最大路径长度限制：
 - Mac 上为 104 个字符
 - Linux 上为 108 个字符

如果您的家目录路径太长，Docker Desktop 将无法创建必要的套接字。

#### 解决方案

确保您的用户名足够短，以使路径保持在允许的范围内：
 - Mac: 用户名应 ≤ 33 个字符
 - Linux: 用户名应 ≤ 55 个字符

## 适用于 Mac 的主题

### 升级需要管理员权限

#### 原因

在 macOS 上，没有管理员权限的用户无法通过 Docker Desktop 控制面板执行应用内升级。

#### 解决方案

> [!IMPORTANT]
> 
> 升级前请勿卸载当前版本。这样做会删除所有本地 Docker 容器、镜像和卷。

要升级 Docker Desktop：

- 请管理员在现有版本上覆盖安装新版本。
- 如果您的配置适用，可以使用 [`--user` 安装标志](/manuals/desktop/setup/install/mac-install.md#安全与访问)。

### 持续提示“某应用程序已更改您的 Desktop 配置”的通知

#### 原因

您收到此通知是因为配置完整性检查功能检测到第三方应用程序更改了您的 Docker Desktop 配置。这通常是由于符号链接不正确或缺失造成的。该通知旨在确保您了解这些更改，以便您可以审查并修复任何潜在问题，从而维护系统的可靠性。

打开通知会弹出一个窗口，提供有关检测到的完整性问题的详细信息。

#### 解决方案

如果您选择忽略通知，它仅会在下次启动 Docker Desktop 时再次显示。如果您选择修复配置，则不会再收到提示。

如果您想关闭配置完整性检查通知，请导航到 Docker Desktop 的设置，在 **General** 选项卡中，取消勾选 **Automatically check configuration** 设置。

### 退出应用后 `com.docker.vmnetd` 仍在运行

特权辅助进程 `com.docker.vmnetd` 由 `launchd` 启动并运行在后台。除非 `Docker.app` 连接到它，否则该进程不会消耗任何资源，因此可以安全地忽略它。

### 检测到不兼容的 CPU

#### 原因

Docker Desktop 需要支持虚拟化的处理器（CPU），具体而言，需要支持 [Apple Hypervisor 框架](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/)。

#### 解决方案

检查：

 - 您是否安装了适用于您架构的正确 Docker Desktop 版本。
 - 您的 Mac 是否支持 Apple 的 Hypervisor 框架。要检查您的 Mac 是否支持 Hypervisor 框架，请在终端窗口中运行以下命令：

   ```console
   $ sysctl kern.hv_support
   ```

   如果您的 Mac 支持 Hypervisor 框架，该命令将输出 `kern.hv_support: 1`。

   如果不支持，则输出 `kern.hv_support: 0`。

另请参阅 Apple 文档中的 [Hypervisor 框架参考](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/)，以及 Docker Desktop [Mac 系统要求](/manuals/desktop/setup/install/mac-install.md#系统要求)。

### VPNKit 经常出现故障

#### 原因

在 Docker Desktop 4.19 版本中，gVisor 取代了 VPNKit，以增强在 macOS 13 及更高版本上使用 Virtualization 框架时的虚拟机网络性能。

#### 解决方案

要继续使用 VPNKit：

1. 打开位于 `~/Library/Group Containers/group.com.docker/settings-store.json` 的 `settings-store.json` 文件。
2. 添加：

   ```JSON
   "networkType":"vpnkit"
   ```
3. 保存文件并重启 Docker Desktop。

## 适用于 Windows 的主题

### 安装了杀毒软件导致 Docker Desktop 无法启动

#### 原因

某些杀毒软件可能与 Hyper-V 和 Microsoft Windows 10 构建版本不兼容。这种冲突通常发生在 Windows 更新之后，表现为 Docker 守护进程的错误响应以及 Docker Desktop 启动失败。

#### 解决方案

作为临时变通方法，请卸载杀毒软件，或者将 Docker 添加到杀毒软件的排除/例外列表中。

### 共享卷的数据目录权限错误

#### 原因

从 Windows 共享文件时，Docker Desktop 会将 [共享卷](/manuals/desktop/settings-and-maintenance/settings.md#文件共享) 的权限设置为默认值 [0777](https://chmodcommand.com/chmod-0777/)（即 `用户` 和 `组` 均具有 `读`、`写`、`执行` 权限）。

共享卷上的默认权限是不可配置的。

#### 解决方案

如果您使用的应用程序需要不同的权限，可以：
 - 使用非宿主机挂载的卷 (non-host-mounted volumes) 
 - 寻找一种让应用程序在默认文件权限下运行的方法

### 意外的语法错误，请在容器内使用 Unix 风格的换行符

#### 原因

Docker 容器预期使用 Unix 风格的换行符 `\n`，而不是 Windows 风格的 `\r\n`。这包括命令行引用的构建文件以及 Dockerfile 中的 RUN 命令。

在使用 Windows 工具编写脚本（如 shell 脚本）时请注意这一点，因为默认情况下可能是 Windows 风格的换行符。这些命令最终会被传递给基于 Unix 的容器内的 Unix 命令（例如传递给 `/bin/sh` 的 shell 脚本）。如果使用了 Windows 风格的换行符，`docker run` 将因语法错误而失败。

#### 解决方案

 - 使用以下工具将文件转换为 Unix 风格换行符：
   
   ```console
   $ dos2unix script.sh
   ```
- 在 VS Code 中，将换行符设置为 `LF` (Unix) 而不是 `CRLF` (Windows)。

### Windows 上的路径转换错误

#### 原因

与 Linux 不同，Windows 在进行卷挂载时需要显式的路径转换。

在 Linux 上，系统负责将一个路径挂载到另一个路径。例如，当您在 Linux 上运行以下命令时：

```console
$ docker run --rm -ti -v /home/user/work:/work alpine
```

它会在目标容器中添加一个 `/work` 目录来映射指定的路径。

#### 解决方案

更新源路径。例如，如果您使用的是旧版 Windows 命令行 (`cmd.exe`)，可以使用以下命令：

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
```

这会启动容器并确保卷变为可用。这是因为 Docker Desktop 会检测到 Windows 风格的路径，并提供适当的转换来挂载该目录。

Docker Desktop 还允许您使用 Unix 风格的路径。例如：

```console
$ docker run --rm -ti -v /c/Users/user/work:/work alpine ls /work
```

### Docker 命令在 Git Bash 中失败

#### 错误消息

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
docker: Error response from daemon: mkdir C:UsersUserwork: Access is denied.
```

```console
$ docker run --rm -ti -v $(pwd):/work alpine
docker: Error response from daemon: OCI runtime create failed: invalid mount {Destination:\Program Files\Git\work Type:bind Source:/run/desktop/mnt/host/c/Users/user/work;C Options:[rbind rprivate]}: mount destination \Program Files\Git\work not absolute: unknown.
```

#### 原因

Git Bash (或 MSYS) 在 Windows 上提供了一个类 Unix 环境。这些工具会对命令行进行自己的预处理。

这会影响 `$(pwd)`、冒号分隔的路径以及波浪号 (`~`)。

此外，在 Git Bash 中 `\` 字符具有特殊含义。

#### 解决方案

 - 暂时禁用 Git Bash 路径转换。例如，在运行命令时禁用 MSYS 路径转换：
    ```console
    $ MSYS_NO_PATHCONV=1 docker run --rm -ti -v $(pwd):/work alpine
    ```
 - 使用正确的路径格式：
    - 使用双正斜杠或双反斜杠 (`\\` 或 `//`) 代替单斜杠 (`\` 或 `/`)。
    - 如果引用 `$(pwd)`，请在前面多加一个 `/`。

脚本的可移植性不受影响，因为 Linux 会将多个 `/` 处理为单个。

### Docker Desktop 因虚拟化未运行而失败

#### 错误消息

典型的错误消息是 "Docker Desktop - Unexpected WSL error"，并提到错误代码 `Wsl/Service/RegisterDistro/CreateVm/HCS/HCS_E_HYPERV_NOT_INSTALLED`。手动执行 `wsl` 命令也会提示相同的错误代码。

#### 原因

- BIOS 中禁用了虚拟化设置。
- 缺少 Windows Hyper-V 或 WSL 2 组件。

请注意，某些第三方软件（如安卓模拟器）在安装时会禁用 Hyper-V。

#### 解决方案

您的机器必须具备以下特性，Docker Desktop 才能正常运行：

##### WSL 2 和 Windows 家庭版 (Home)

1. 虚拟机平台 (Virtual Machine Platform)
2. [适用于 Linux 的 Windows 子系统 (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
3. [在 BIOS 中启用虚拟化](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
   请注意，许多 Windows 设备已默认启用虚拟化，因此这可能不适用。
4. 在 Windows 启动时启用虚拟机管理程序 (Hypervisor)

![WSL 2 已启用](../../images/wsl2-enabled.png)

必须能够无误地运行 WSL 2 命令，例如：

```console
PS C:\users\> wsl -l -v
  NAME              STATE           VERSION
* Ubuntu            Running         2
  docker-desktop    Stopped         2
PS C:\users\> wsl -d docker-desktop echo WSL 2 is working
WSL 2 is working
```

如果功能已启用但命令无法运行，请首先检查 [虚拟化是否已开启](#必须开启虚拟化)，如有需要，请 [在 Windows 启动时启用虚拟机管理程序](#在-windows-启动时启用虚拟机管理程序)。如果在虚拟机中运行 Docker Desktop，请确保 [虚拟机管理程序已启用嵌套虚拟化](#开启嵌套虚拟化)。

##### Hyper-V

在 Windows 10 专业版 (Pro) 或企业版 (Enterprise) 上，您也可以在启用以下功能的情况下使用 Hyper-V：

1. [Hyper-V](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview) 已安装并正常工作
2. [在 BIOS 中启用虚拟化](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
3. 在 Windows 启动时启用虚拟机管理程序 (Hypervisor)

![Windows 功能中的 Hyper-V](../../images/hyperv-enabled.png)

Docker Desktop 需要安装并启用 Hyper-V 以及适用于 Windows PowerShell 的 Hyper-V 模块。Docker Desktop 安装程序会为您启用它。

Docker Desktop 使用 Hyper-V 还需要两项 CPU 硬件特性：虚拟化和二级地址转换 (SLAT)，后者也被称为快速虚拟化索引 (RVI)。在某些系统上，必须在 BIOS 中启用虚拟化。所需步骤因供应商而异，但通常 BIOS 选项被称为 `Virtualization Technology (VTx)` 或类似名称。运行命令 `systeminfo` 以检查所有必需的 Hyper-V 特性。有关更多详情，请参阅 [Windows 10 上 Hyper-V 的前提条件](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)。

要手动安装 Hyper-V，请参阅 [在 Windows 10 上安装 Hyper-V](https://msdn.microsoft.com/en-us/virtualization/hyperv_on_windows/quick_start/walkthrough_install)。安装后 *必须* 重启。如果您在未重启的情况下安装 Hyper-V，Docker Desktop 将无法正常工作。

在开始菜单中，输入 **启用或关闭 Windows 功能** 并按回车。在随后的屏幕中，确认 Hyper-V 已启用。

##### 必须开启虚拟化

除了 [Hyper-V](#hyper-v) 或 [WSL 2](/manuals/desktop/features/wsl/_index.md) 之外，还必须开启虚拟化。请检查任务管理器的“性能”选项卡。或者，您可以在终端中输入 `systeminfo`。如果您看到 `Hyper-V Requirements: A hypervisor has been detected. Features required for Hyper-V will not be displayed`，则说明虚拟化已启用。

![任务管理器](../../images/virtualization-enabled.png)

如果您手动卸载了 Hyper-V、WSL 2 或关闭了虚拟化，Docker Desktop 将无法启动。

要开启嵌套虚拟化，请参阅 [在 VM 或 VDI 环境中运行 Windows 版 Docker Desktop](/manuals/desktop/setup/vm-vdi.md#开启嵌套虚拟化)。

##### 在 Windows 启动时启用虚拟机管理程序

如果您已完成上述步骤，但仍遇到 Docker Desktop 启动问题，可能是因为虚拟机管理程序虽已安装，但在 Windows 启动时未启动。某些工具（如旧版 Virtual Box）和某些视频游戏安装程序会在引导时关闭虚拟机管理程序。要重新开启它：

1. 打开管理员控制台提示符。
2. 运行 `bcdedit /set hypervisorlaunchtype auto`。
3. 重启 Windows。

您还可以参考有关代码流保护 (CFG) 设置的 [Microsoft TechNet 文章](https://social.technet.microsoft.com/Forums/en-US/ee5b1d6b-09e2-49f3-a52c-820aafc316f9/hyperv-doesnt-work-after-upgrade-to-windows-10-1809?forum=win10itprovirt)。

##### 开启嵌套虚拟化

如果您使用的是 Hyper-V，且在 VDI 环境中运行 Docker Desktop 时收到以下错误消息：

```console
The Virtual Machine Management Service failed to start the virtual machine 'DockerDesktopVM' because one of the Hyper-V components is not running
```

请尝试 [开启嵌套虚拟化](/manuals/desktop/setup/vm-vdi.md#开启嵌套虚拟化)。

### 使用 Windows 容器的 Docker Desktop 失败，提示“介质受写保护”

#### 错误消息

`FSCTL_EXTEND_VOLUME \\?\Volume{GUID}: The media is write protected`

#### 原因

如果您在使用 Windows 容器运行 Docker Desktop 时遇到失败，可能是由于特定的 Windows 配置策略：FDVDenyWriteAccess。

该策略启用后，会导致 Windows 将所有未经过 BitLocker 加密的固定驱动器挂载为只读。这也影响到虚拟机卷，结果是 Docker Desktop 可能无法启动或正常运行容器，因为它需要对这些卷具有读写权限。

FDVDenyWriteAccess 是一项 Windows 组策略设置，启用后会阻止对未受 BitLocker 保护的固定数据驱动器的写访问。这通常用于注重安全性的环境，但会干扰 Docker 等开发工具。在 Windows 注册表中，它位于 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Policies\Microsoft\FVE\FDVDenyWriteAccess`。

#### 解决方案

Docker Desktop 不支持在启用了 FDVDenyWriteAccess 的系统上运行 Windows 容器。此设置会干扰 Docker 正确挂载卷的能力，而这对于容器功能至关重要。

要配合 Windows 容器使用 Docker Desktop，请确保禁用 FDVDenyWriteAccess。您可以在注册表中检查并更改此设置，或通过组策略编辑器 (`gpedit.msc`) 在以下路径下修改：

**计算机配置 (Computer Configuration)** > **管理模板 (Administrative Templates)** > **Windows 组件 (Windows Components)** > **BitLocker 驱动器加密 (BitLocker Drive Encryption)** > **固定数据驱动器 (Fixed Data Drives)** > **拒绝向未受 BitLocker 保护的固定驱动器写入数据 (Deny write access to fixed drives not protected by BitLocker)**

> [!NOTE]
> 
> 修改组策略设置可能需要管理员权限，并应符合您组织的 IT 策略。如果该设置在一段时间后被重置，通常意味着它被您 IT 部门的集中配置覆盖了。在进行任何更改前，请先咨询您的 IT 部门。

### 启动 Docker Desktop 时出现 `Docker Desktop Access Denied` (访问被拒绝) 错误消息

#### 错误消息

启动 Docker Desktop 时，出现以下错误：

```text
Docker Desktop - Access Denied
```

#### 原因

用户不属于 `docker-users` 组，而该组是获得相关权限所必需的。

#### 解决方案

如果您的管理员帐户与用户帐户不同，请添加：

1. 以管理员身份运行 **计算机管理 (Computer Management)**。
2. 导航到 **本地用户和组 (Local Users and Groups)** > **组 (Groups)** > **docker-users**。
3. 右键点击将用户添加到组中。
4. 注销并重新登录以使更改生效。

```