---
description: 了解如何以二进制文件形式安装 Docker。这些说明最适合用于测试目的。
keywords: 二进制文件, binaries, 安装, docker, 文档, linux, 安装 docker engine
title: 从二进制文件安装 Docker Engine
linkTitle: 二进制文件
weight: 80
aliases:
- /engine/installation/binaries/
- /engine/installation/linux/docker-ce/binaries/
- /install/linux/docker-ce/binaries/
- /installation/binaries/
---

> [!IMPORTANT]
>
> 本页包含有关如何使用二进制文件安装 Docker 的信息。这些说明主要适用于测试目的。我们不建议在生产环境中使用二进制文件安装 Docker，因为它们没有自动的安全更新。本页描述的 Linux 二进制文件是静态链接的，这意味着构建时依赖项中的漏洞不会通过 Linux 发行版安全更新自动打补丁。
>
> 与使用软件包管理器或通过 Docker Desktop 安装的 Docker 软件包相比，更新二进制文件也稍微复杂一些，因为每当有新版本的 Docker 发布时，都需要 (手动) 更新安装的版本。
>
> 此外，静态二进制文件可能不包含动态软件包提供的所有功能。
>
> 在 Windows 和 Mac 上，我们建议您安装 [Docker Desktop](/manuals/desktop/_index.md)。对于 Linux，我们建议您遵循特定于您发行版的说明。

如果您想尝试 Docker 或在测试环境中使用它，但您不在受支持的平台上，可以尝试从静态二进制文件安装。如果可能，您应该使用为您的操作系统构建的软件包，并使用操作系统的软件包管理系统来管理 Docker 的安装和升级。

Docker 守护进程二进制文件的静态二进制文件仅适用于 Linux (名为 `dockerd`) 和 Windows (名为 `dockerd.exe`)。Docker 客户端的静态二进制文件适用于 Linux、Windows 和 macOS (名为 `docker`)。

本主题讨论 Linux、Windows 和 macOS 的二进制安装：

- [在 Linux 上安装守护进程和客户端二进制文件](#install-daemon-and-client-binaries-on-linux)
- [在 macOS 上安装客户端二进制文件](#install-client-binaries-on-macos)
- [在 Windows 上安装服务器和客户端二进制文件](#install-server-and-client-binaries-on-windows)

## 在 Linux 上安装守护进程和客户端二进制文件

### 前提条件

在尝试从二进制文件安装 Docker 之前，请确保您的主机满足以下前提条件：

- 64 位系统
- 3.10 或更高版本的 Linux 内核。建议使用适用于您平台的最新内核版本。
- `iptables` 1.4 或更高版本
- `git` 1.7 或更高版本
- `ps` 可执行文件，通常由 `procps` 或类似的软件包提供。
- [XZ Utils](https://tukaani.org/xz/) 4.9 或更高版本
- [正确挂载](https://github.com/tianon/cgroupfs-mount/blob/master/cgroupfs-mount)的 `cgroupfs` 层次结构；单个、包罗万象的 `cgroup` 挂载点是不够的。参见 Github 问题 [#2683](https://github.com/moby/moby/issues/2683)、[#3485](https://github.com/moby/moby/issues/3485)、[#4568](https://github.com/moby/moby/issues/4568)。

#### 尽可能确保环境安全

##### 操作系统注意事项

如果可能，请启用 SELinux 或 AppArmor。

如果您的 Linux 发行版支持 AppArmor 或 SELinux，建议使用其中之一。这有助于提高安全性并阻止某些类型的漏洞利用。请查阅您的 Linux 发行版文档，了解启用和配置 AppArmor 或 SELinux 的说明。

> **安全警告**
>
> 如果启用了其中一种安全机制，请不要为了让 Docker 或其容器运行而禁用它。相反，应正确配置它以解决任何问题。

##### Docker 守护进程注意事项

- 如果可能，启用 `seccomp` 安全配置文件。参见 [为 Docker 启用 `seccomp`](../security/seccomp.md)。

- 如果可能，启用用户命名空间 (user namespaces)。参见 [守护进程用户命名空间选项](/reference/cli/dockerd/#daemon-user-namespace-options)。

### 安装静态二进制文件

1. 下载静态二进制归档文件。访问 [https://download.docker.com/linux/static/stable/](https://download.docker.com/linux/static/stable/)，选择您的硬件平台，并下载与您要安装的 Docker Engine 版本相关的 `.tgz` 文件。

2. 使用 `tar` 工具解压归档文件。`dockerd` 和 `docker` 二进制文件将被解压。

    ```console
    $ tar xzvf /path/to/<FILE>.tar.gz
    ```

3. **可选**：将二进制文件移动到可执行路径中的目录，例如 `/usr/bin/`。如果跳过此步骤，则在调用 `docker` 或 `dockerd` 命令时必须提供可执行文件的路径。

    ```console
    $ sudo cp docker/* /usr/bin/
    ```

4. 启动 Docker 守护进程：

    ```console
    $ sudo dockerd &
    ```

    如果您需要使用其他选项启动守护进程，请相应地修改上述命令，或者创建并编辑 `/etc/docker/daemon.json` 文件以添加自定义配置选项。

5. 通过运行 `hello-world` 镜像验证 Docker 是否已正确安装。

    ```console
    $ sudo docker run hello-world
    ```

    此命令会下载一个测试镜像并在容器中运行。当容器运行时，它会打印一条消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

## 在 macOS 上安装客户端二进制文件

> [!NOTE]
>
> 以下说明主要适用于测试目的。macOS 二进制文件仅包含 Docker 客户端。它不包含运行容器所需的 `dockerd` 守护进程。因此，我们建议您改为安装 [Docker Desktop](/manuals/desktop/_index.md)。

适用于 Mac 的二进制文件也不包含：

- 运行时环境。您必须在虚拟机或远程 Linux 机器上设置一个功能完备的引擎。
- Docker 组件，如 `buildx` 和 `docker compose`。

要安装客户端二进制文件，请执行以下步骤：

1. 下载静态二进制归档文件。访问 [https://download.docker.com/mac/static/stable/](https://download.docker.com/mac/static/stable/) 并选择 `x86_64` (适用于搭载 Intel 芯片的 Mac) 或 `aarch64` (适用于搭载 Apple 芯片的 Mac)，然后下载与您要安装的 Docker Engine 版本相关的 `.tgz` 文件。

2. 使用 `tar` 工具解压归档文件。`docker` 二进制文件将被解压。

    ```console
    $ tar xzvf /path/to/<FILE>.tar.gz
    ```

3. 清除扩展属性以允许其运行。

    ```console
    $ sudo xattr -rc docker
    ```

    现在，当您运行以下命令时，您可以看到 Docker CLI 的使用说明：

    ```console
    $ docker/docker
    ```

4. **可选**：将二进制文件移动到可执行路径中的目录，例如 `/usr/local/bin/`。如果跳过此步骤，则在调用 `docker` 或 `dockerd` 命令时必须提供可执行文件的路径。

    ```console
    $ sudo cp docker/docker /usr/local/bin/
    ```

5. 通过运行 `hello-world` 镜像验证 Docker 是否已正确安装。`<hostname>` 的值是运行 Docker 守护进程且客户端可访问的主机名或 IP 地址。

    ```console
    $ sudo docker -H <hostname> run hello-world
    ```

    此命令会下载一个测试镜像并在容器中运行。当容器运行时，它会打印一条消息并退出。

## 在 Windows 上安装服务器和客户端二进制文件

> [!NOTE]
>
> 以下部分介绍如何在 Windows Server 上安装 Docker 守护进程，这仅允许您运行 Windows 容器。当您在 Windows Server 上安装 Docker 守护进程时，守护进程不包含 Docker 组件，如 `buildx` 和 `compose`。如果您使用的是 Windows 10 或 11，我们建议您改为安装 [Docker Desktop](/manuals/desktop/_index.md)。

Windows 上的二进制包包含 `dockerd.exe` 和 `docker.exe`。在 Windows 上，这些二进制文件仅提供运行原生 Windows 容器 (而非 Linux 容器) 的能力。

要安装服务器和客户端二进制文件，请执行以下步骤：

1. 下载静态二进制归档文件。访问 [https://download.docker.com/win/static/stable/x86_64](https://download.docker.com/win/static/stable/x86_64) 并从列表中选择最新版本。

2. 运行以下 PowerShell 命令以安装并将归档文件解压到您的程序文件中：

    ```powershell
    PS C:\> Expand-Archive /path/to/<FILE>.zip -DestinationPath $Env:ProgramFiles
    ```

3. 注册服务并启动 Docker Engine：

    ```powershell
    PS C:\> &$Env:ProgramFiles\Docker\dockerd --register-service
    PS C:\> Start-Service docker
    ```

4. 通过运行 `hello-world` 镜像验证 Docker 是否已正确安装。

    ```powershell
    PS C:\> &$Env:ProgramFiles\Docker\docker run hello-world:nanoserver
    ```

    此命令会下载一个测试镜像并在容器中运行。当容器运行时，它会打印一条消息并退出。

## 升级静态二进制文件

要升级手动安装的 Docker Engine，请先停止本地运行的所有 `dockerd` 或 `dockerd.exe` 进程，然后按照常规安装步骤在现有版本之上安装新版本。

## 后续步骤

- 继续阅读 [Linux 安装后的步骤](linux-postinstall.md)。
