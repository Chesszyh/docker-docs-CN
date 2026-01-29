---
description: 了解并更改 Docker Desktop 的设置
keywords: 设置, 偏好, 代理, 文件共享, 资源, kubernetes, Docker Desktop, Linux, Mac, Windows
title: 更改您的 Docker Desktop 设置
linkTitle: 更改设置
aliases:
 - /desktop/settings/mac/
 - /desktop/settings/windows/
 - /desktop/settings/linux/
 - /desktop/settings/
weight: 10
---

要导航到 **Settings**（设置），可以选择以下方式之一：

- 选择 Docker 菜单 {{< inline-image src="../images/whale-x.svg" alt="鲸鱼菜单" >}} 然后选择 **Settings**。
- 从 Docker Desktop 控制面板中选择 **Settings** 图标。

您也可以在以下位置找到 `settings-store.json` 文件（或者 Docker Desktop 4.34 及更早版本的 `settings.json`）：
 - Mac: `~/Library/Group\ Containers/group.com.docker/settings-store.json`
 - Windows: `C:\Users\[用户名]\AppData\Roaming\Docker\settings-store.json`
 - Linux: `~/.docker/desktop/settings-store.json`

## 常规 (General)

在 **General** 选项卡上，您可以配置何时启动 Docker 并指定其他设置：

- **Start Docker Desktop when you sign in to your computer**。勾选此项可在您登录机器时自动启动 Docker Desktop。

- **Open Docker Dashboard when Docker Desktop starts**。勾选此项可在启动 Docker Desktop 时自动打开控制面板。

- **Choose theme for Docker Desktop**。选择是为 Docker Desktop 应用 **Light**（浅色）还是 **Dark**（深色）主题。或者，您可以将 Docker Desktop 设置为 **Use system settings**（使用系统设置）。

- **Configure shell completions**。当您在终端输入时按 `<Tab>` 键，自动编辑您的 shell 配置并为您提供命令、标志和 Docker 对象（如容器和卷名称）的单词补全。有关更多信息，请参阅 [补全 (Completion)](/manuals/engine/cli/completion.md)。

- **Choose container terminal**。确定从容器打开终端时启动哪个终端。如果您选择集成终端，则可以直接从 Docker Desktop 控制面板在运行中的容器内运行命令。有关更多信息，请参阅 [探索容器](/manuals/desktop/use-desktop/container.md)。

- **Enable Docker terminal**。直接从 Docker Desktop 与宿主机交互并执行命令。

- **Enable Docker Debug by default**。勾选此项可在访问集成终端时默认使用 Docker Debug。有关更多信息，请参阅 [探索容器](/manuals/desktop/use-desktop/container.md#集成终端)。

- {{< badge color=blue text="仅限 Mac" >}}**Include VM in Time Machine backups**。勾选此项以备份 Docker Desktop 虚拟机。此选项默认关闭。

- **Use containerd for pulling and storing images**。开启 containerd 镜像库。这带来了新特性，如通过延迟拉取（lazy-pulling）镜像实现更快的容器启动性能，以及通过 Docker 运行 Wasm 应用程序的能力。有关更多信息，请参阅 [containerd 镜像库](/manuals/desktop/features/containerd.md)。

- {{< badge color=blue text="仅限 Windows" >}}**Expose daemon on tcp://localhost:2375 without TLS**。勾选此项以允许旧版客户端连接到 Docker 守护进程。由于在没有 TLS 的情况下暴露守护进程可能导致远程代码执行攻击，因此您必须谨慎使用此选项。

- {{< badge color=blue text="仅限 Windows" >}}**Use the WSL 2 based engine**。WSL 2 提供了比 Hyper-V 后端更好的性能。有关更多信息，请参阅 [Docker Desktop WSL 2 后端](/manuals/desktop/features/wsl/_index.md)。

- {{< badge color=blue text="仅限 Windows" >}}**Add the `*.docker.internal` names to the host's `/etc/hosts` file (Password required)**。允许您从宿主机和容器中解析 `*.docker.internal` DNS 名称。

- {{< badge color=blue text="仅限 Mac" >}} **Choose Virtual Machine Manager (VMM)**。选择用于创建和管理 Docker Desktop Linux 虚拟机的虚拟机管理器。
  - 选择 **Docker VMM** 以获得最新且性能最强的 Hypervisor/虚拟机管理器。此选项仅在运行 macOS 12.5 或更高版本的 Apple Silicon Mac 上可用，目前处于 Beta 阶段。
    > [!TIP]
    >
    > 开启此设置可让 Docker Desktop 运行得更快。
  - 或者，您可以选择 **Apple Virtualization framework**、**QEMU**（适用于 Apple Silicon）或 **HyperKit**（适用于 Intel Mac）。对于 macOS 12.5 及更高版本，Apple Virtualization framework 是默认设置。

   有关更多信息，请参阅 [虚拟机管理器 (VMM)](/manuals/desktop/features/vmm.md)。

- {{< badge color=blue text="仅限 Mac" >}}**Choose file sharing implementation for your containers**。选择是要使用 **VirtioFS**、**gRPC FUSE** 还是 **osxfs (Legacy)** 来共享文件。VirtioFS 仅适用于 macOS 12.5 及更高版本，且默认开启。
    > [!TIP]
    >
    > 使用 VirtioFS 实现快速文件共享。VirtioFS 将完成文件系统操作所需的时间缩短了 [高达 98%](https://github.com/docker/roadmap/issues/7#issuecomment-1044452206)。它是 Docker VMM 唯一支持的文件共享实现。

- {{< badge color=blue text="仅限 Mac" >}}**Use Rosetta for x86_64/amd64 emulation on Apple Silicon**。开启 Rosetta 以加速 Apple Silicon 上的 x86/AMD64 二进制模拟。此选项仅在您选择了 **Apple Virtualization framework** 作为虚拟机管理器且系统版本为 macOS 13 或更高版本时可用。

- **Send usage statistics**。勾选后，Docker Desktop 会发送诊断信息、崩溃报告和使用数据。这些信息有助于 Docker 改进应用程序并排除故障。取消勾选即可选择退出。Docker 可能会定期提示您提供更多信息。

- **Use Enhanced Container Isolation**。勾选此项通过防止容器突破 Linux 虚拟机来增强安全性。有关更多信息，请参阅 [增强型容器隔离 (ECI)](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)。
    > [!NOTE]
    >
    > 此设置仅在您登录 Docker Desktop 且拥有 Docker Business 订阅时可用。

- **Show CLI hints**。在 CLI 中运行 Docker 命令时显示 CLI 提示和技巧。此项默认开启。要从 CLI 开启或关闭 CLI 提示，请将 `DOCKER_CLI_HINTS` 分别设置为 `true` 或 `false`。

- **Enable Scout image analysis**。开启此选项后，在 Docker Desktop 中检查镜像会显示一个 **Start analysis**（开始分析）按钮，点击后将使用 Docker Scout 分析镜像。

- **Enable background SBOM indexing**。开启此选项后，Docker Scout 会自动分析您构建或拉取的镜像。

- {{< badge color=blue text="仅限 Mac" >}}**Automatically check configuration**。定期检查您的配置，以确保没有被其他应用程序进行意外更改。

  Docker Desktop 会检查安装期间配置的设置是否已被 Orbstack 等外部应用更改。Docker Desktop 检查：
    - Docker 二进制文件到 `/usr/local/bin` 的符号链接。
    - 默认 Docker 套接字的符号链接。 
  此外，Docker Desktop 确保启动时上下文切换到 `desktop-linux`。
  
  如果发现更改，您会收到通知，并能直接从通知中恢复配置。有关更多信息，请参阅 [FAQ](/manuals/desktop/troubleshoot-and-support/faqs/macfaqs.md#为什么我一直收到通知告诉我有应用程序更改了我的-Desktop-配置)。

## 资源 (Resources)

**Resources** 选项卡允许您配置 CPU、内存、磁盘、代理、网络和其他资源。

### 高级 (Advanced)

> [!NOTE]
>
> 在 Windows 上，**Advanced** 选项卡中的 **Resource allocation**（资源分配）选项仅在 Hyper-V 模式下可用，因为 Windows 在 WSL 2 模式和 Windows 容器模式下管理资源。在 WSL 2 模式下，您可以对分配给 [WSL 2 实用虚拟机](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig) 的内存、CPU 和交换文件大小配置限制。

在 **Advanced** 选项卡上，您可以限制 Docker Linux 虚拟机可用的资源。

高级设置包括：

- **CPU limit**。指定 Docker Desktop 可使用的最大 CPU 数量。默认情况下，Docker Desktop 设置为使用宿主机上的所有可用处理器。

- **Memory limit**。默认情况下，Docker Desktop 设置为使用宿主机多达 50% 的内存。要增加 RAM，请将其设置为更高的数字；要减少，请降低该数字。

- **Swap**。根据需要配置交换文件大小。默认值为 1 GB。

- **Disk usage limit**。指定引擎可以使用的最大磁盘空间量。

- **Disk image location**。指定存储容器和镜像的 Linux 卷的位置。

  您也可以将磁盘镜像移动到其他位置。如果您尝试将磁盘镜像移动到一个已经存在镜像的位置，系统会询问您是使用现有镜像还是替换它。

>[!TIP]
>
> 如果您感觉 Docker Desktop 开始变慢，或者您正在运行多容器工作负载，请增加内存和磁盘镜像空间分配。

- **Resource Saver**。启用或禁用 [资源节省模式 (Resource Saver mode)](/manuals/desktop/use-desktop/resource-saver.md)，该模式在 Docker Desktop 空闲（即没有容器运行）时通过自动关闭 Linux 虚拟机来显著降低宿主机的 CPU 和内存占用。

  您还可以配置资源节省超时时间，该值指示 Docker Desktop 在进入资源节省模式之前应空闲多长时间。默认值为 5 分钟。

  > [!NOTE]
  >
  > 当容器运行时，会自动退出资源节省模式。退出可能需要几秒钟（约 3 到 10 秒），因为 Docker Desktop 需要重启 Linux 虚拟机。


### 文件共享 (File sharing)

> [!NOTE]
>
> 在 Windows 上，**File sharing** 选项卡仅在 Hyper-V 模式下可用，因为在 WSL 2 模式和 Windows 容器模式下文件是自动共享的。

使用文件共享允许将您机器上的本地目录与 Linux 容器共享。这在宿主机上使用 IDE 编辑源代码，同时在容器中运行和测试代码时特别有用。

#### 同步文件共享 (Synchronized file shares)

同步文件共享是一种备选的文件共享机制，提供快速、灵活的宿主机到虚拟机的共享，通过使用同步的文件系统缓存来增强绑定挂载性能。适用于 Pro、Team 和 Business 订阅。

欲了解更多信息，请参阅 [同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md)。

#### 虚拟文件共享 (Virtual file shares)

默认情况下，`/Users`、`/Volumes`、`/private`、`/tmp` 和 `/var/folders` 目录是共享的。如果您的项目位于这些目录之外，则必须将其添加到列表中，否则可能会在运行时收到 `Mounts denied`（挂载被拒绝）或 `cannot start service`（无法启动服务）错误。

文件共享设置包括：

- **Add a Directory**。点击 `+` 并导航到您想要添加的目录。

- **Remove a Directory**。点击目录旁边的 `-` 将其移除。

- **Apply** 使目录对使用 Docker 绑定挂载 (`-v`) 功能的容器可用。

> [!TIP]
>
> * 仅与容器共享您需要的目录。文件共享会引入开销，因为宿主机上文件的任何更改都需要通知 Linux 虚拟机。共享过多文件可能导致高 CPU 负载和文件系统性能下降。
> * 共享文件夹旨在允许在宿主机上编辑应用程序代码，同时在容器中执行。对于非代码项（如缓存目录或数据库），如果它们存储在 Linux 虚拟机中，使用 [数据卷](/manuals/engine/storage/volumes.md)（具名卷）或 [数据容器](/manuals/engine/storage/volumes.md)，性能会好得多。
> * 如果您将整个主目录共享到容器中，macOS 可能会提示您授予 Docker 访问主目录中个人区域（如提醒事项或下载）的权限。
> * 默认情况下，Mac 文件系统是不区分大小写的，而 Linux 是区分大小写的。在 Linux 上，可以创建两个独立的文件：`test` 和 `Test`，而在 Mac 上，这些文件名实际上会指向同一个底层文件。这可能导致应用程序在开发人员的机器上正常工作（文件内容被共享），但在生产环境中的 Linux 上运行失败（文件内容是不同的）。为了避免这种情况，Docker Desktop 坚持要求所有共享文件都以其原始大小写进行访问。因此，如果创建了一个名为 `test` 的文件，就必须以 `test` 身份打开它。尝试打开 `Test` 将失败，并显示“No such file or directory”错误。同样，一旦创建了名为 `test` 的文件，尝试创建第二个名为 `Test` 的文件也将失败。
>
> 有关更多信息，请参阅 [对于 `/Users` 之外的任何项目目录，卷挂载都需要文件共享](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)。

#### 按需共享文件夹 (Shared folders on demand)

在 Windows 上，当容器第一次使用某个特定文件夹时，您可以“按需”共享该文件夹。

如果您在带有卷挂载的 shell 中运行 Docker 命令（如下例所示），或者启动了一个包含卷挂载的 Compose 文件，系统会弹出一个窗口询问您是否要共享指定的文件夹。

您可以选择 **Share it**（共享它），在这种情况下，该文件夹会被添加到您的 Docker Desktop 共享文件夹列表中并可供容器使用。或者，您也可以选择 **Cancel**（取消）不共享它。

![按需共享文件夹](../images/shared-folder-on-demand.png)

### 代理 (Proxies)

Docker Desktop 支持使用 HTTP/HTTPS 和 [SOCKS5 代理](/manuals/desktop/features/networking.md#socks5-代理支持)。

HTTP/HTTPS 代理可用于：

- 登录 Docker
- 拉取或推送镜像
- 在镜像构建期间获取构件
- 容器与外部网络交互
- 扫描镜像

如果宿主机使用了 HTTP/HTTPS 代理配置（静态配置或通过代理自动配置 (PAC)），Docker Desktop 会读取此配置并自动将这些设置用于登录 Docker、拉取和推送镜像以及容器互联网访问。如果代理需要授权，Docker Desktop 会动态向开发人员询问用户名和密码。所有密码都安全地存储在操作系统的凭据存储中。请注意，仅支持 `Basic` 代理身份验证方法，因此我们建议为您的 HTTP/HTTPS 代理使用 `https://` URL，以保护网络传输中的密码。Docker Desktop 在与代理通信时支持 TLS 1.3。

要为 Docker Desktop 设置不同的代理，请开启 **Manual proxy configuration**（手动代理配置）并输入一个格式为 `http://proxy:port` 或 `https://proxy:port` 的单一上游代理 URL。

为了防止开发人员意外更改代理设置，请参阅 [设置管理 (Settings Management)](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md#我可以使用设置管理配置哪些功能)。

用于扫描镜像的 HTTPS 代理设置是使用 `HTTPS_PROXY` 环境变量设置的。

> [!NOTE]
>
> 如果您使用的是托管在 Web 服务器上的 PAC 文件，请务必在服务器或网站上为 `.pac` 文件扩展名添加 MIME 类型 `application/x-ns-proxy-autoconfig`。如果没有此配置，PAC 文件可能无法正确解析。

> [!IMPORTANT]
> 您不能使用 Docker 守护进程配置文件 (`daemon.json`) 配置代理设置，我们建议您不要通过 Docker CLI 配置文件 (`config.json`) 配置代理设置。
>
> 要管理 Docker Desktop 的代理配置，请在 Docker Desktop 应用程序中配置设置或使用 [设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。

#### 代理身份验证

##### 基本身份验证 (Basic authentication)

如果您的代理使用基本身份验证，Docker Desktop 会提示开发人员输入用户名和密码，并缓存这些凭据。所有密码都安全地存储在操作系统的凭据存储中。如果该缓存被移除，它将请求重新认证。

建议为 HTTP/HTTPS 代理使用 `https://` URL，以保护网络传输期间的密码。Docker Desktop 在与代理通信时也支持 TLS 1.3。

##### Kerberos 和 NTLM 身份验证

> [!NOTE]
>
> 适用于使用 Docker Desktop for Windows 4.30 及更高版本的 Docker Business 订阅者。

由于身份验证已集中化，开发人员不再会被代理凭据提示所打断。这也降低了由于不正确的登录尝试导致账户锁定的风险。

如果您的代理在 407 (Proxy Authentication Required) 响应中提供了多种身份验证方案，Docker Desktop 默认选择基本身份验证方案。

对于 Docker Desktop 4.30 至 4.31 版本： 

要启用 Kerberos 或 NTLM 代理身份验证，除了指定代理 IP 地址和端口外，不需要额外的配置。

对于 Docker Desktop 4.32 及更高版本： 

要启用 Kerberos 或 NTLM 代理身份验证，您必须在通过命令行安装期间传递 `--proxy-enable-kerberosntlm` 安装标志，并确保您的代理服务器已正确配置为进行 Kerberos 或 NTLM 身份验证。

### 网络 (Network)

> [!NOTE]
>
> 在 Windows 上，由于 Windows 管理网络，**Network** 选项卡在 Windows 容器模式下不可用。

Docker Desktop 为内部服务（如 DNS 服务器和 HTTP 代理）使用私有 IPv4 网络。如果 Docker Desktop 选择的子网与您环境中的 IP 冲突，您可以使用 **Network** 设置指定自定义子网。

在 Windows 和 Mac 上，您还可以设置默认网络模式和 DNS 解析行为。有关更多信息，请参阅 [网络 (Networking)](/manuals/desktop/features/networking.md#mac-和-windows-的网络模式和-dns-行为)。

在 Mac 上，您还可以选择 **Use kernel networking for UDP** 设置。这允许您为 UDP 使用更高效的内核网络路径。这可能与您的 VPN 软件不兼容。

### WSL 集成 (WSL Integration)

在 Windows 的 WSL 2 模式下，您可以配置哪些 WSL 2 发行版将启用 Docker WSL 集成。

默认情况下，集成在您的默认 WSL 发行版上启用。要更改默认 WSL 发行版，请运行 `wsl --set-default <发行版名称>`。（例如，要将 Ubuntu 设置为您的默认 WSL 发行版，请运行 `wsl --set-default ubuntu`）。

您还可以选择任何其他想要启用 WSL 2 集成的发行版。

有关配置 Docker Desktop 以使用 WSL 2 的更多细节，请参阅 [Docker Desktop WSL 2 后端](/manuals/desktop/features/wsl/_index.md)。

## Docker 引擎 (Docker Engine)

**Docker Engine** 选项卡允许您配置用于在 Docker Desktop 中运行容器的 Docker 守护进程。

您使用 JSON 配置文件配置守护进程。文件内容可能如下所示：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false
}
```

您可以在 `$HOME/.docker/daemon.json` 找到此文件。要更改配置，可以直接从 Docker Desktop 的控制面板编辑 JSON 配置，或者使用您喜欢的文本编辑器打开并编辑该文件。

要查看所有可能的配置选项完整列表，请参阅 [dockerd 命令参考](/reference/cli/dockerd/)。

选择 **Apply**（应用）以保存您的设置。

## 构建器 (Builders)

如果您开启了 [Docker Desktop 构建视图](/manuals/desktop/use-desktop/builds.md)，可以使用 **Builders** 选项卡在 Docker Desktop 设置中检查和管理构建器。

### 检查 (Inspect)

要检查构建器，找到您想要检查的构建器并选择展开图标。您只能检查活动状态的构建器。

检查活动构建器会显示：

- BuildKit 版本
- 状态
- 驱动类型
- 支持的能力和平台
- 磁盘使用情况
- 端点地址

### 选择不同的构建器

**Selected builder**（已选构建器）部分显示了当前选中的构建器。要选择不同的构建器：

1. 在 **Available builders**（可用构建器）下找到您想要使用的构建器。
2. 打开构建器名称旁边的下拉菜单。
3. 选择 **Use** 切换到此构建器。

您的构建命令现在将默认使用所选的构建器。

### 创建构建器

要创建构建器，请使用 Docker CLI。请参阅 [创建新构建器](/build/builders/manage/#创建新构建器)。

### 移除构建器

如果您满足以下条件，则可以移除构建器：

- 该构建器不是您的 [已选构建器](/build/builders/#已选构建器)。
- 该构建器未 [与 Docker 上下文关联](/build/builders/#默认构建器)。

  要移除与 Docker 上下文关联的构建器，请使用 `docker context rm` 命令移除该上下文。

要移除构建器：

1. 在 **Available builders**（可用构建器）下找到您想要移除的构建器。
2. 打开下拉菜单。
3. 选择 **Remove** 移除此构建器。

如果构建器使用 `docker-container` 或 `kubernetes` 驱动程序，构建缓存也会随构建器一起被移除。

### 停止和启动构建器

使用 [`docker-container` 驱动程序](/build/builders/drivers/docker-container/) 的构建器在容器中运行 BuildKit 守护进程。您可以使用下拉菜单启动和停止 BuildKit 容器。

如果容器已停止，运行构建时会自动启动它。

您只能启动和停止使用 `docker-container` 驱动程序的构建器。

## Kubernetes

> [!NOTE]
>
> 在 Windows 上，**Kubernetes** 选项卡在 Windows 容器模式下不可用。

Docker Desktop 包含一个独立的 Kubernetes 服务器，以便您可以测试在 Kubernetes 上部署 Docker 工作负载。要开启 Kubernetes 支持并安装作为 Docker 容器运行的独立 Kubernetes 实例，请选择 **Enable Kubernetes**。

在 Docker Desktop 4.38 及更高版本中，您可以选择集群供应方法：
 - **Kubeadm** 创建单节点集群，版本由 Docker Desktop 设置。
 - **kind** 创建多节点集群，您可以设置版本和节点数量。 

在使用 Docker 命令时，选择 **Show system containers (advanced)** 可以查看内部容器。

选择 **Reset Kubernetes cluster**（重置 Kubernetes 集群）可以删除所有栈和 Kubernetes 资源。

有关结合 Docker Desktop 使用 Kubernetes 集成的更多信息，请参阅 [在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)。

## 软件更新 (Software Updates)

**Software Updates** 选项卡会通知您 Docker Desktop 的任何可用更新。当有新更新时，您可以选择立即下载更新，或选择 **Release Notes**（发行说明）选项来了解更新版本中包含的内容。

取消勾选 **Automatically check for updates** 复选框可以关闭更新检查。这会禁用 Docker 菜单中的通知以及 Docker Desktop 控制面板上出现的通知徽章。要手动检查更新，请选择 Docker 菜单中的 **Check for updates** 选项。

要允许 Docker Desktop 在后台自动下载新更新，请选择 **Always download updates**。这将在有更新可用时下载较新版本的 Docker Desktop。下载更新后，选择 **Apply and Restart**（应用并重启）来安装更新。您可以通过 Docker 菜单或 Docker Desktop 控制面板的 **Updates** 部分来执行此操作。

> [!TIP]
> 
> 在 Docker Desktop 4.38 及更高版本中，Docker Desktop 的组件（如 Docker Compose、Docker Scout 和 Docker CLI）可以独立更新，无需完全重启。此功能目前处于 Beta 阶段。 

## 扩展 (Extensions)

使用 **Extensions** 选项卡可以：

- **Enable Docker Extensions**（启用 Docker 扩展）
- **Allow only extensions distributed through the Docker Marketplace**（仅允许通过 Docker Marketplace 分发的扩展）
- **Show Docker Extensions system containers**（显示 Docker 扩展系统容器）

有关 Docker 扩展的更多信息，请参阅 [扩展 (Extensions)](/manuals/extensions/_index.md)。

## Beta 功能

Beta 功能允许访问未来的产品功能。这些功能仅供测试和反馈，因为它们可能会在不同版本之间发生变化且不预先警告，或者在未来版本中被完全移除。Beta 功能不得用于生产环境。Docker 不为 Beta 功能提供支持。

您也可以从 **Beta features** 选项卡注册参加 [开发者预览计划 (Developer Preview program)](https://www.docker.com/community/get-involved/developer-preview/)。

有关 Docker CLI 中当前实验性功能的列表，请参阅 [Docker CLI 实验性功能](https://github.com/docker/cli/blob/master/experimental/README.md)。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，在 **Features in development**（开发中的功能）页面下还有一个 **Experimental features**（实验性功能）选项卡。
>
> 与 Beta 功能一样，实验性功能不得在生产环境中使用。Docker 不为实验性功能提供支持。

## 通知 (Notifications)

使用 **Notifications** 选项卡开启或关闭以下事件的通知：

- **Status updates on tasks and processes**（任务和进程的状态更新）
- **Recommendations from Docker**（来自 Docker 的建议）
- **Docker announcements**（Docker 公告）
- **Docker surveys**（Docker 调查）

默认情况下，所有常规通知都是开启的。您始终会收到错误通知以及关于新 Docker Desktop 发布和更新的通知。

您还可以 [配置 Docker Scout 相关问题的通知设置](/manuals/scout/explore/dashboard.md#通知设置)。 

通知会暂时出现在 Docker Desktop 控制面板的右下角，然后移动到 **Notifications** 抽屉中，该抽屉可以从 Docker Desktop 控制面板的右上角访问。

## 高级 (Advanced)

在 Mac 上，您可以在 **Advanced** 选项卡上重新配置初始安装设置：

- **Choose how to configure the installation of Docker's CLI tools**（选择如何配置 Docker CLI 工具的安装）。
  - **System**：Docker CLI 工具安装在系统目录 `/usr/local/bin` 下。
  - **User**：Docker CLI 工具安装在用户目录 `$HOME/.docker/bin` 下。然后您必须将 `$HOME/.docker/bin` 添加到您的 PATH 中。添加步骤如下：
      1. 打开您的 shell 配置文件。如果您使用的是 bash shell，则是 `~/.bashrc` ；如果您使用的是 zsh shell，则是 `~/.zshrc` 。
      2. 复制并粘贴以下内容：
            ```console
            $ export PATH=$PATH:~/.docker/bin
            ```
     3. 保存并关闭文件。重启 shell 以将更改应用到 PATH 变量。

- **Allow the default Docker socket to be used (Requires password)**（允许使用默认的 Docker 套接字）。创建 `/var/run/docker.sock`，某些第三方客户端可能会使用它与 Docker Desktop 通信。有关更多信息，请参阅 [macOS 的权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#安装符号链接)。

- **Allow privileged port mapping (Requires password)**（允许特权端口映射）。启动特权助手进程，该进程绑定 1 到 1024 之间的端口。有关更多信息，请参阅 [macOS 的权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#绑定特权端口)。

有关每个配置及其用例的更多信息，请参阅 [权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md)。
