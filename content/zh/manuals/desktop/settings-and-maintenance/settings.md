---
description: 了解并更改 Docker Desktop 的设置
keywords: settings, preferences, proxy, file sharing, resources, kubernetes, Docker
  Desktop, Linux, Mac, Windows
title: 更改 Docker Desktop 设置
linkTitle: 更改设置
aliases:
 - /desktop/settings/mac/
 - /desktop/settings/windows/
 - /desktop/settings/linux/
 - /desktop/settings/
weight: 10
---

要导航到**设置**，可以：

- 选择 Docker 菜单 {{< inline-image src="../images/whale-x.svg" alt="whale menu" >}}，然后选择 **Settings**
- 从 Docker Desktop 仪表板选择 **Settings** 图标。

您也可以在以下位置找到 `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本的 `settings.json`）：
 - Mac：`~/Library/Group\ Containers/group.com.docker/settings-store.json`
 - Windows：`C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
 - Linux：`~/.docker/desktop/settings-store.json`

## 常规

在 **General** 标签页上，您可以配置何时启动 Docker 以及指定其他设置：

- **Start Docker Desktop when you sign in to your computer**（登录计算机时启动 Docker Desktop）。选择此选项可在您登录计算机时自动启动 Docker Desktop。

- **Open Docker Dashboard when Docker Desktop starts**（Docker Desktop 启动时打开 Docker 仪表板）。选择此选项可在启动 Docker Desktop 时自动打开仪表板。

- **Choose theme for Docker Desktop**（选择 Docker Desktop 主题）。选择您想要将 **Light**（浅色）或 **Dark**（深色）主题应用于 Docker Desktop。或者，您可以设置 Docker Desktop 为 **Use system settings**（使用系统设置）。

- **Configure shell completions**（配置 shell 补全）。自动编辑您的 shell 配置，当您在终端中输入并按 `<Tab>` 键时，为命令、标志和 Docker 对象（如容器和卷名称）提供单词补全。更多信息请参阅 [Completion](/manuals/engine/cli/completion.md)。

- **Choose container terminal**（选择容器终端）。决定从容器打开终端时启动哪个终端。如果您选择集成终端，可以直接从 Docker Desktop 仪表板在运行的容器中执行命令。更多信息请参阅 [Explore containers](/manuals/desktop/use-desktop/container.md)。

- **Enable Docker terminal**（启用 Docker 终端）。与主机交互并直接从 Docker Desktop 执行命令。

- **Enable Docker Debug by default**（默认启用 Docker Debug）。选中此选项可在访问集成终端时默认使用 Docker Debug。更多信息请参阅 [Explore containers](/manuals/desktop/use-desktop/container.md#integrated-terminal)。

- {{< badge color=blue text="Mac only" >}}**Include VM in Time Machine backups**（在 Time Machine 备份中包含虚拟机）。选择此选项可备份 Docker Desktop 虚拟机。此选项默认关闭。

- **Use containerd for pulling and storing images**（使用 containerd 拉取和存储镜像）。启用 containerd 镜像存储。这带来了新功能，如通过延迟拉取镜像实现更快的容器启动性能，以及使用 Docker 运行 Wasm 应用程序的能力。更多信息请参阅 [containerd image store](/manuals/desktop/features/containerd.md)。

- {{< badge color=blue text="Windows only" >}}**Expose daemon on tcp://localhost:2375 without TLS**（在 tcp://localhost:2375 上公开守护进程而不使用 TLS）。选中此选项可让旧客户端连接到 Docker 守护进程。使用此选项时必须谨慎，因为在没有 TLS 的情况下公开守护进程可能导致远程代码执行攻击。

- {{< badge color=blue text="Windows only" >}}**Use the WSL 2 based engine**（使用基于 WSL 2 的引擎）。WSL 2 提供比 Hyper-V 后端更好的性能。更多信息请参阅 [Docker Desktop WSL 2 backend](/manuals/desktop/features/wsl/_index.md)。

- {{< badge color=blue text="Windows only" >}}**Add the `*.docker.internal` names to the host's `/etc/hosts` file (Password required)**（将 `*.docker.internal` 名称添加到主机的 `/etc/hosts` 文件，需要密码）。允许您从主机和容器解析 `*.docker.internal` DNS 名称。

- {{< badge color=blue text="Mac only" >}} **Choose Virtual Machine Manager (VMM)**（选择虚拟机管理器）。选择用于创建和管理 Docker Desktop Linux 虚拟机的虚拟机管理器。
  - 选择 **Docker VMM** 以获得最新和最高性能的 Hypervisor/虚拟机管理器。此选项仅在运行 macOS 12.5 或更高版本的 Apple Silicon Mac 上可用，目前处于 Beta 阶段。
    > [!TIP]
    >
    > 启用此设置可使 Docker Desktop 运行更快。
  - 或者，您可以选择 **Apple Virtualization framework**、**QEMU**（适用于 Apple Silicon）或 **HyperKit**（适用于 Intel Mac）。对于 macOS 12.5 及更高版本，Apple Virtualization framework 是默认设置。

   更多信息请参阅 [Virtual Machine Manager](/manuals/desktop/features/vmm.md)。

- {{< badge color=blue text="Mac only" >}}**Choose file sharing implementation for your containers**（为容器选择文件共享实现）。选择您想要使用 **VirtioFS**、**gRPC FUSE** 还是 **osxfs (Legacy)** 来共享文件。VirtioFS 仅适用于 macOS 12.5 及更高版本，并且默认开启。
    > [!TIP]
    >
    > 使用 VirtioFS 可实现快速文件共享。VirtioFS 将完成文件系统操作所需的时间减少了[高达 98%](https://github.com/docker/roadmap/issues/7#issuecomment-1044452206)。它是 Docker VMM 支持的唯一文件共享实现。

- {{< badge color=blue text="Mac only" >}}**Use Rosetta for x86_64/amd64 emulation on Apple Silicon**（在 Apple Silicon 上使用 Rosetta 进行 x86_64/amd64 模拟）。启用 Rosetta 以加速 Apple Silicon 上的 x86/AMD64 二进制模拟。此选项仅在您选择了 **Apple Virtualization framework** 作为虚拟机管理器时可用。您还必须使用 macOS 13 或更高版本。

- **Send usage statistics**（发送使用统计信息）。选择此选项可让 Docker Desktop 发送诊断、崩溃报告和使用数据。此信息帮助 Docker 改进和排查应用程序故障。清除复选框可选择退出。Docker 可能会定期提示您提供更多信息。

- **Use Enhanced Container Isolation**（使用增强容器隔离）。选择此选项可通过防止容器突破 Linux 虚拟机来增强安全性。更多信息请参阅 [Enhanced Container Isolation](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)。
    > [!NOTE]
    >
    > 此设置仅在您登录 Docker Desktop 并拥有 Docker Business 订阅时可用。

- **Show CLI hints**（显示 CLI 提示）。在 CLI 中运行 Docker 命令时显示 CLI 提示和技巧。此选项默认开启。要从 CLI 开启或关闭 CLI 提示，请将 `DOCKER_CLI_HINTS` 分别设置为 `true` 或 `false`。

- **Enable Scout image analysis**（启用 Scout 镜像分析）。启用此选项后，在 Docker Desktop 中检查镜像会显示 **Start analysis** 按钮，选择后会使用 Docker Scout 分析镜像。

- **Enable background SBOM indexing**（启用后台 SBOM 索引）。启用此选项后，Docker Scout 会自动分析您构建或拉取的镜像。

- {{< badge color=blue text="Mac only" >}}**Automatically check configuration**（自动检查配置）。定期检查您的配置以确保没有被其他应用程序意外更改。

  Docker Desktop 会检查您在安装期间配置的设置是否被 Orbstack 等外部应用程序更改。Docker Desktop 检查：
    - Docker 二进制文件到 `/usr/local/bin` 的符号链接。
    - 默认 Docker 套接字的符号链接。
  此外，Docker Desktop 确保在启动时将上下文切换到 `desktop-linux`。

  如果发现更改，您将收到通知，并可以直接从通知中恢复配置。更多信息请参阅 [FAQs](/manuals/desktop/troubleshoot-and-support/faqs/macfaqs.md#why-do-i-keep-getting-a-notification-telling-me-an-application-has-changed-my-desktop-configurations)。

## 资源

**Resources** 标签页允许您配置 CPU、内存、磁盘、代理、网络和其他资源。

### 高级

> [!NOTE]
>
> 在 Windows 上，**Advanced** 标签页中的 **Resource allocation**（资源分配）选项仅在 Hyper-V 模式下可用，因为 Windows 在 WSL 2 模式和 Windows 容器模式下管理资源。在 WSL 2 模式下，您可以配置分配给 [WSL 2 实用程序虚拟机](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig)的内存、CPU 和交换空间大小的限制。

在 **Advanced** 标签页上，您可以限制 Docker Linux 虚拟机可用的资源。

高级设置包括：

- **CPU limit**（CPU 限制）。指定 Docker Desktop 可使用的最大 CPU 数量。默认情况下，Docker Desktop 设置为使用主机上所有可用的处理器。

- **Memory limit**（内存限制）。默认情况下，Docker Desktop 设置为最多使用主机内存的 50%。要增加 RAM，请将此值设置得更高；要减少，请降低此数值。

- **Swap**（交换空间）。根据需要配置交换文件大小。默认值为 1 GB。

- **Disk usage limit**（磁盘使用限制）。指定引擎可以使用的最大磁盘空间量。

- **Disk image location**（磁盘镜像位置）。指定存储容器和镜像的 Linux 卷的位置。

  您也可以将磁盘镜像移动到不同的位置。如果您尝试将磁盘镜像移动到已有磁盘镜像的位置，系统会询问您是要使用现有镜像还是替换它。

>[!TIP]
>
> 如果您感觉 Docker Desktop 开始变慢或您正在运行多容器工作负载，请增加内存和磁盘镜像空间分配

- **Resource Saver**（资源节省）。启用或禁用[资源节省模式](/manuals/desktop/use-desktop/resource-saver.md)，该模式通过在 Docker Desktop 空闲时（即没有容器运行时）自动关闭 Linux 虚拟机来显著减少主机上的 CPU 和内存利用率。

  您还可以配置资源节省超时时间，该时间指示 Docker Desktop 应空闲多长时间后才启动资源节省模式。默认值为 5 分钟。

  > [!NOTE]
  >
  > 当容器运行时会自动退出资源节省模式。退出可能需要几秒钟（约 3 到 10 秒），因为 Docker Desktop 需要重新启动 Linux 虚拟机。


### 文件共享

> [!NOTE]
>
> 在 Windows 上，**File sharing** 标签页仅在 Hyper-V 模式下可用，因为文件在 WSL 2 模式和 Windows 容器模式下会自动共享。

使用文件共享可以让您计算机上的本地目录与 Linux 容器共享。这对于在主机上的 IDE 中编辑源代码同时在容器中运行和测试代码特别有用。

#### 同步文件共享

同步文件共享（Synchronized file shares）是一种替代的文件共享机制，通过使用同步的文件系统缓存提供快速灵活的主机到虚拟机文件共享，从而增强绑定挂载性能。适用于 Pro、Team 和 Business 订阅。

要了解更多信息，请参阅 [Synchronized file share](/manuals/desktop/features/synchronized-file-sharing.md)。

#### 虚拟文件共享

默认情况下，`/Users`、`/Volumes`、`/private`、`/tmp` 和 `/var/folders` 目录是共享的。如果您的项目在此目录之外，则必须将其添加到列表中，否则您可能会在运行时收到 `Mounts denied` 或 `cannot start service` 错误。

文件共享设置包括：

- **Add a Directory**（添加目录）。选择 `+` 并导航到您要添加的目录。

- **Remove a Directory**（删除目录）。选择要删除的目录旁边的 `-`

- **Apply**（应用）使该目录可用于使用 Docker 绑定挂载（`-v`）功能的容器。

> [!TIP]
>
> * 仅与容器共享您需要的目录。文件共享会带来开销，因为主机上文件的任何更改都需要通知 Linux 虚拟机。共享太多文件可能导致高 CPU 负载和慢文件系统性能。
> * 共享文件夹旨在允许在主机上编辑应用程序代码，同时在容器中执行。对于非代码项目（如缓存目录或数据库），如果使用[数据卷](/manuals/engine/storage/volumes.md)（命名卷）或[数据容器](/manuals/engine/storage/volumes.md)将它们存储在 Linux 虚拟机中，性能会更好。
> * 如果您将整个主目录共享到容器中，macOS 可能会提示您授予 Docker 访问主目录中个人区域（如提醒事项或下载）的权限。
> * 默认情况下，Mac 文件系统不区分大小写，而 Linux 区分大小写。在 Linux 上，可以创建两个单独的文件：`test` 和 `Test`，而在 Mac 上，这些文件名实际上指向同一个底层文件。这可能导致应用程序在开发者机器上（文件内容是共享的）正常工作，但在生产环境的 Linux 中运行时（文件内容是不同的）失败的问题。为避免这种情况，Docker Desktop 坚持所有共享文件都以其原始大小写形式访问。因此，如果创建了名为 `test` 的文件，则必须以 `test` 打开它。尝试打开 `Test` 将失败并显示错误"No such file or directory"。同样，一旦创建了名为 `test` 的文件，尝试创建名为 `Test` 的第二个文件也将失败。
>
> 更多信息请参阅 [Volume mounting requires file sharing for any project directories outside of `/Users`](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)

#### 按需共享文件夹

在 Windows 上，您可以在第一次使用特定文件夹时"按需"共享该文件夹。

如果您从 shell 运行带有卷挂载的 Docker 命令（如下例所示）或启动包含卷挂载的 Compose 文件，您会收到一个弹出窗口询问您是否要共享指定的文件夹。

您可以选择 **Share it**（共享），在这种情况下，它会被添加到您的 Docker Desktop 共享文件夹列表中并可供容器使用。或者，您可以选择 **Cancel**（取消）来选择不共享它。

![Shared folder on demand](../images/shared-folder-on-demand.png)

### 代理

Docker Desktop 支持使用 HTTP/HTTPS 和 [SOCKS5 代理](/manuals/desktop/features/networking.md#socks5-proxy-support)。

HTTP/HTTPS 代理可用于：

- 登录 Docker
- 拉取或推送镜像
- 在镜像构建过程中获取工件
- 容器与外部网络交互
- 扫描镜像

如果主机使用 HTTP/HTTPS 代理配置（静态或通过代理自动配置 PAC），Docker Desktop 会读取此配置并自动使用这些设置来登录 Docker、拉取和推送镜像以及容器互联网访问。如果代理需要授权，Docker Desktop 会动态询问开发者用户名和密码。所有密码都安全存储在操作系统凭据存储中。请注意，仅支持 `Basic` 代理认证方法，因此我们建议为您的 HTTP/HTTPS 代理使用 `https://` URL，以在网络传输过程中保护密码。Docker Desktop 在与代理通信时支持 TLS 1.3。

要为 Docker Desktop 设置不同的代理，请打开 **Manual proxy configuration**（手动代理配置）并输入格式为 `http://proxy:port` 或 `https://proxy:port` 的单个上游代理 URL。

要防止开发人员意外更改代理设置，请参阅 [Settings Management](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md#what-features-can-i-configure-with-settings-management)。

用于扫描镜像的 HTTPS 代理设置使用 `HTTPS_PROXY` 环境变量设置。

> [!NOTE]
>
> 如果您使用的是托管在 Web 服务器上的 PAC 文件，请确保在服务器或网站上为 `.pac` 文件扩展名添加 MIME 类型 `application/x-ns-proxy-autoconfig`。没有此配置，PAC 文件可能无法正确解析。

> [!IMPORTANT]
> 您无法使用 Docker 守护进程配置文件（`daemon.json`）配置代理设置，我们建议您不要通过 Docker CLI 配置文件（`config.json`）配置代理设置。
>
> 要管理 Docker Desktop 的代理配置，请在 Docker Desktop 应用程序中配置设置或使用 [Settings Management](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。

#### 代理认证

##### 基本认证

如果您的代理使用基本认证（Basic authentication），Docker Desktop 会提示开发者输入用户名和密码并缓存凭据。所有密码都安全存储在操作系统凭据存储中。如果缓存被删除，它将请求重新认证。

建议为 HTTP/HTTPS 代理使用 `https://` URL，以在网络传输过程中保护密码。Docker Desktop 还支持使用 TLS 1.3 与代理通信。

##### Kerberos 和 NTLM 认证

> [!NOTE]
>
> 适用于使用 Docker Desktop for Windows 4.30 及更高版本的 Docker Business 订阅者。

开发人员不再被代理凭据提示中断，因为认证是集中式的。这也降低了因错误登录尝试导致账户锁定的风险。

如果您的代理在 407（需要代理认证）响应中提供多种认证方案，Docker Desktop 默认选择基本认证方案。

对于 Docker Desktop 4.30 至 4.31 版本：

要启用 Kerberos 或 NTLM 代理认证，除了指定代理 IP 地址和端口外，无需额外配置。

对于 Docker Desktop 4.32 及更高版本：

要启用 Kerberos 或 NTLM 代理认证，您必须在通过命令行安装时传递 `--proxy-enable-kerberosntlm` 安装程序标志，并确保您的代理服务器已正确配置为 Kerberos 或 NTLM 认证。

### 网络

> [!NOTE]
>
> 在 Windows 上，**Network** 标签页在 Windows 容器模式下不可用，因为 Windows 管理网络。

Docker Desktop 为内部服务（如 DNS 服务器和 HTTP 代理）使用私有 IPv4 网络。如果 Docker Desktop 选择的子网与您环境中的 IP 冲突，您可以使用 **Network** 设置指定自定义子网。

在 Windows 和 Mac 上，您还可以设置默认网络模式和 DNS 解析行为。更多信息请参阅 [Networking](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

在 Mac 上，您还可以选择 **Use kernel networking for UDP**（为 UDP 使用内核网络）设置。这允许您为 UDP 使用更高效的内核网络路径。这可能与您的 VPN 软件不兼容。

### WSL 集成

在 Windows 的 WSL 2 模式下，您可以配置哪些 WSL 2 发行版将具有 Docker WSL 集成。

默认情况下，集成在您的默认 WSL 发行版上启用。要更改默认 WSL 发行版，请运行 `wsl --set-default <distribution name>`。（例如，要将 Ubuntu 设置为默认 WSL 发行版，请运行 `wsl --set-default ubuntu`）。

您还可以选择任何其他您想要启用 WSL 2 集成的发行版。

有关配置 Docker Desktop 使用 WSL 2 的更多详细信息，请参阅 [Docker Desktop WSL 2 backend](/manuals/desktop/features/wsl/_index.md)。

## Docker 引擎

**Docker Engine** 标签页允许您配置用于运行 Docker Desktop 容器的 Docker 守护进程。

您可以使用 JSON 配置文件配置守护进程。以下是文件可能的样子：

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

您可以在 `$HOME/.docker/daemon.json` 找到此文件。要更改配置，可以直接从 Docker Desktop 仪表板编辑 JSON 配置，或使用您喜欢的文本编辑器打开并编辑文件。

要查看可能的配置选项的完整列表，请参阅 [dockerd command reference](/reference/cli/dockerd/)。

选择 **Apply** 保存您的设置。

## 构建器

如果您已启用 [Docker Desktop Builds view](/manuals/desktop/use-desktop/builds.md)，您可以在 Docker Desktop 设置中使用 **Builders** 标签页来检查和管理构建器。

### 检查

要检查构建器，找到您要检查的构建器并选择展开图标。您只能检查活动的构建器。

检查活动构建器会显示：

- BuildKit 版本
- 状态
- 驱动程序类型
- 支持的功能和平台
- 磁盘使用量
- 端点地址

### 选择不同的构建器

**Selected builder**（已选择的构建器）部分显示当前选择的构建器。要选择不同的构建器：

1. 在 **Available builders**（可用构建器）下找到您要使用的构建器
2. 打开构建器名称旁边的下拉菜单。
3. 选择 **Use** 以切换到此构建器。

您的构建命令现在默认使用所选的构建器。

### 创建构建器

要创建构建器，请使用 Docker CLI。请参阅 [Create a new builder](/build/builders/manage/#create-a-new-builder)

### 删除构建器

您可以在以下情况下删除构建器：

- 该构建器不是您[选择的构建器](/build/builders/#selected-builder)
- 该构建器未[与 Docker 上下文关联](/build/builders/#default-builder)。

  要删除与 Docker 上下文关联的构建器，请使用 `docker context rm` 命令删除上下文。

要删除构建器：

1. 在 **Available builders** 下找到您要删除的构建器
2. 打开下拉菜单。
3. 选择 **Remove** 以删除此构建器。

如果构建器使用 `docker-container` 或 `kubernetes` 驱动程序，构建缓存也会随构建器一起删除。

### 停止和启动构建器

使用 [`docker-container` 驱动程序](/build/builders/drivers/docker-container/)的构建器在容器中运行 BuildKit 守护进程。您可以使用下拉菜单启动和停止 BuildKit 容器。

如果容器已停止，运行构建会自动启动容器。

您只能启动和停止使用 `docker-container` 驱动程序的构建器。

## Kubernetes

> [!NOTE]
>
> 在 Windows 上，**Kubernetes** 标签页在 Windows 容器模式下不可用。

Docker Desktop 包含一个独立的 Kubernetes 服务器，因此您可以测试在 Kubernetes 上部署您的 Docker 工作负载。要启用 Kubernetes 支持并安装作为 Docker 容器运行的独立 Kubernetes 实例，请选择 **Enable Kubernetes**（启用 Kubernetes）。

使用 Docker Desktop 4.38 及更高版本，您可以选择集群配置方法：
 - **Kubeadm** 创建单节点集群，版本由 Docker Desktop 设置。
 - **kind** 创建多节点集群，您可以设置版本和节点数量。

选择 **Show system containers (advanced)**（显示系统容器，高级）以在使用 Docker 命令时查看内部容器。

选择 **Reset Kubernetes cluster**（重置 Kubernetes 集群）以删除所有堆栈和 Kubernetes 资源。

有关将 Kubernetes 集成与 Docker Desktop 一起使用的更多信息，请参阅 [Deploy on Kubernetes](/manuals/desktop/features/kubernetes.md)。

## 软件更新

**Software Updates** 标签页会通知您 Docker Desktop 的任何可用更新。当有新更新时，您可以选择立即下载更新，或选择 **Release Notes** 选项了解更新版本中包含的内容。

通过清除 **Automatically check for updates**（自动检查更新）复选框来关闭更新检查。这将禁用 Docker 菜单中的通知以及 Docker Desktop 仪表板上显示的通知徽章。要手动检查更新，请在 Docker 菜单中选择 **Check for updates** 选项。

要允许 Docker Desktop 在后台自动下载新更新，请选择 **Always download updates**（始终下载更新）。当有更新可用时，这会下载较新版本的 Docker Desktop。下载更新后，选择 **Apply and Restart** 安装更新。您可以通过 Docker 菜单或 Docker Desktop 仪表板中的 **Updates** 部分执行此操作。

> [!TIP]
>
> 使用 Docker Desktop 4.38 及更高版本，Docker Desktop 的组件（如 Docker Compose、Docker Scout 和 Docker CLI）可以独立更新，无需完全重启。此功能仍处于 Beta 阶段。

## 扩展

使用 **Extensions** 标签页可以：

- **Enable Docker Extensions**（启用 Docker 扩展）
- **Allow only extensions distributed through the Docker Marketplace**（仅允许通过 Docker Marketplace 分发的扩展）
- **Show Docker Extensions system containers**（显示 Docker 扩展系统容器）

有关 Docker 扩展的更多信息，请参阅 [Extensions](/manuals/extensions/_index.md)。

## Beta 功能

Beta 功能提供对未来产品功能的访问。这些功能仅用于测试和反馈，因为它们可能会在版本之间更改而不发出警告，或者在未来版本中完全删除。Beta 功能不得在生产环境中使用。Docker 不为 Beta 功能提供支持。

您还可以从 **Beta features** 标签页注册 [Developer Preview program](https://www.docker.com/community/get-involved/developer-preview/)。

有关 Docker CLI 中当前实验性功能的列表，请参阅 [Docker CLI Experimental features](https://github.com/docker/cli/blob/master/experimental/README.md)。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，在 **Features in development** 页面下还有一个 **Experimental features**（实验性功能）标签页。
>
> 与 Beta 功能一样，实验性功能不得在生产环境中使用。Docker 不为实验性功能提供支持。

## 通知

使用 **Notifications** 标签页可以开启或关闭以下事件的通知：

- **Status updates on tasks and processes**（任务和进程的状态更新）
- **Recommendations from Docker**（来自 Docker 的建议）
- **Docker announcements**（Docker 公告）
- **Docker surveys**（Docker 调查）

默认情况下，所有常规通知都是开启的。您将始终收到错误通知以及有关新 Docker Desktop 版本和更新的通知。

您还可以[为 Docker Scout 相关问题配置通知设置](/manuals/scout/explore/dashboard.md#notification-settings)。

通知会短暂出现在 Docker Desktop 仪表板的右下角，然后移动到 **Notifications** 抽屉，可从 Docker Desktop 仪表板的右上角访问。

## 高级

在 Mac 上，您可以在 **Advanced** 标签页上重新配置初始安装设置：

- **Choose how to configure the installation of Docker's CLI tools**（选择如何配置 Docker CLI 工具的安装）。
  - **System**：Docker CLI 工具安装在 `/usr/local/bin` 下的系统目录中
  - **User**：Docker CLI 工具安装在 `$HOME/.docker/bin` 下的用户目录中。然后您必须将 `$HOME/.docker/bin` 添加到您的 PATH。要将 `$HOME/.docker/bin` 添加到您的路径：
      1. 打开您的 shell 配置文件。如果您使用 bash shell，这是 `~/.bashrc`，如果您使用 zsh shell，则是 `~/.zshrc`。
      2. 复制并粘贴以下内容：
            ```console
            $ export PATH=$PATH:~/.docker/bin
            ```
     3. 保存并关闭文件。重新启动您的 shell 以应用对 PATH 变量的更改。

- **Allow the default Docker socket to be used (Requires password)**（允许使用默认 Docker 套接字，需要密码）。创建 `/var/run/docker.sock`，某些第三方客户端可能使用它与 Docker Desktop 通信。更多信息请参阅 [permission requirements for macOS](/manuals/desktop/setup/install/mac-permission-requirements.md#installing-symlinks)。

- **Allow privileged port mapping (Requires password)**（允许特权端口映射，需要密码）。启动特权辅助进程，该进程绑定 1 到 1024 之间的端口。更多信息请参阅 [permission requirements for macOS](/manuals/desktop/setup/install/mac-permission-requirements.md#binding-privileged-ports)。

有关每个配置和用例的更多信息，请参阅 [Permission requirements](/manuals/desktop/setup/install/mac-permission-requirements.md)。
