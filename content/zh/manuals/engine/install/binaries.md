---
description: 了解如何以二进制文件形式安装 Docker。这些说明最适合测试目的。
keywords: binaries, installation, docker, documentation, linux, install docker engine
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
> 本页面包含有关如何使用二进制文件安装 Docker 的信息。这些
> 说明主要适用于测试目的。我们不建议
> 在生产环境中使用二进制文件安装 Docker，因为它们没有自动安全更新。本页面描述的 Linux 二进制文件
> 是静态链接的，这意味着构建时
> 依赖项中的漏洞不会被您的 Linux
> 发行版的安全更新自动修补。
>
> 与使用包管理器或通过 Docker Desktop 安装的 Docker 软件包相比，
> 更新二进制文件也略微复杂一些，因为它需要
> 在 Docker 发布新版本时（手动）更新已安装的版本。
>
> 此外，静态二进制文件可能不包含动态
> 软件包提供的所有功能。
>
> 在 Windows 和 Mac 上，我们建议您改为安装 [Docker Desktop](/manuals/desktop/_index.md)。
> 对于 Linux，我们建议您按照针对
> 您发行版的具体说明进行操作。

如果您想尝试 Docker 或在测试环境中使用它，但您不在
支持的平台上，可以尝试从静态二进制文件安装。如果可能的话，
您应该使用为您的操作系统构建的软件包，并使用您操作系统的
包管理系统来管理 Docker 安装和升级。

Docker 守护进程二进制文件的静态二进制文件仅适用于 Linux（作为
`dockerd`）和 Windows（作为 `dockerd.exe`）。
Docker 客户端的静态二进制文件适用于 Linux、Windows 和 macOS（作为 `docker`）。

本主题讨论 Linux、Windows 和 macOS 的二进制安装：

- [在 Linux 上安装守护进程和客户端二进制文件](#install-daemon-and-client-binaries-on-linux)
- [在 macOS 上安装客户端二进制文件](#install-client-binaries-on-macos)
- [在 Windows 上安装服务器和客户端二进制文件](#install-server-and-client-binaries-on-windows)

## 在 Linux 上安装守护进程和客户端二进制文件 {#install-daemon-and-client-binaries-on-linux}

### 前提条件

在尝试从二进制文件安装 Docker 之前，请确保您的主机
满足以下前提条件：

- 64 位安装
- Linux 内核版本 3.10 或更高。建议使用您平台可用的最新版本内核。
- `iptables` 版本 1.4 或更高
- `git` 版本 1.7 或更高
- 一个 `ps` 可执行文件，通常由 `procps` 或类似软件包提供。
- [XZ Utils](https://tukaani.org/xz/) 4.9 或更高
- 一个[正确挂载的](
  https://github.com/tianon/cgroupfs-mount/blob/master/cgroupfs-mount)
  `cgroupfs` 层次结构；单一的、包含所有内容的 `cgroup` 挂载
  点是不够的。请参阅 Github 问题
  [#2683](https://github.com/moby/moby/issues/2683)、
  [#3485](https://github.com/moby/moby/issues/3485)、
  [#4568](https://github.com/moby/moby/issues/4568)）。

#### 尽可能保护您的环境安全

##### 操作系统注意事项

如果可能，请启用 SELinux 或 AppArmor。

如果您的 Linux 发行版支持 AppArmor 或 SELinux，建议使用
其中之一。这有助于提高安全性并阻止某些
类型的漏洞利用。请查阅您的 Linux 发行版文档以获取
启用和配置 AppArmor 或 SELinux 的说明。

> **安全警告**
>
> 如果启用了任一安全机制，请不要将其禁用作为
> 使 Docker 或其容器运行的变通方法。而是正确配置它
> 以解决任何问题。

##### Docker 守护进程注意事项

- 如果可能，请启用 `seccomp` 安全配置文件。请参阅
  [为 Docker 启用 `seccomp`](../security/seccomp.md)。

- 如果可能，请启用用户命名空间。请参阅
  [守护进程用户命名空间选项](/reference/cli/dockerd/#daemon-user-namespace-options)。

### 安装静态二进制文件

1.  下载静态二进制文件归档文件。前往
    [https://download.docker.com/linux/static/stable/](https://download.docker.com/linux/static/stable/)，
    选择您的硬件平台，然后下载与您要安装的
    Docker Engine 版本相关的 `.tgz` 文件。

2.  使用 `tar` 实用程序解压归档文件。`dockerd` 和 `docker`
    二进制文件会被解压出来。

    ```console
    $ tar xzvf /path/to/<FILE>.tar.gz
    ```

3.  **可选**：将二进制文件移动到可执行路径上的目录，例如
    `/usr/bin/`。如果跳过此步骤，则在调用 `docker` 或 `dockerd` 命令时
    必须提供可执行文件的路径。

    ```console
    $ sudo cp docker/* /usr/bin/
    ```

4.  启动 Docker 守护进程：

    ```console
    $ sudo dockerd &
    ```

    如果需要使用其他选项启动守护进程，请相应地修改上述
    命令或创建并编辑文件 `/etc/docker/daemon.json`
    以添加自定义配置选项。

5.  通过运行 `hello-world` 镜像来验证 Docker 是否正确安装。

    ```console
    $ sudo docker run hello-world
    ```

    此命令下载一个测试镜像并在容器中运行它。当
    容器运行时，它会打印一条消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

## 在 macOS 上安装客户端二进制文件 {#install-client-binaries-on-macos}

> [!NOTE]
>
> 以下说明主要适用于测试目的。macOS
> 二进制文件仅包含 Docker 客户端。它不包含运行容器所需的 `dockerd` 守护进程。因此，我们建议您改为安装
> [Docker Desktop](/manuals/desktop/_index.md)。

Mac 的二进制文件也不包含：

- 运行时环境。您必须在虚拟机中或远程 Linux 机器上设置一个可用的引擎。
- Docker 组件，如 `buildx` 和 `docker compose`。

要安装客户端二进制文件，请执行以下步骤：

1.  下载静态二进制文件归档文件。前往
    [https://download.docker.com/mac/static/stable/](https://download.docker.com/mac/static/stable/) 并选择 `x86_64`（用于 Intel 芯片的 Mac）或 `aarch64`（用于 Apple 芯片的 Mac），
    然后下载与您要安装的 Docker Engine 版本相关的 `.tgz` 文件。

2.  使用 `tar` 实用程序解压归档文件。`docker` 二进制文件会被
    解压出来。

    ```console
    $ tar xzvf /path/to/<FILE>.tar.gz
    ```

3.  清除扩展属性以允许其运行。

    ```console
    $ sudo xattr -rc docker
    ```

    现在，当您运行以下命令时，您可以看到 Docker CLI 使用说明：

    ```console
    $ docker/docker
    ```

4.  **可选**：将二进制文件移动到可执行路径上的目录，例如
    `/usr/local/bin/`。如果跳过此步骤，则在调用 `docker` 或 `dockerd` 命令时
    必须提供可执行文件的路径。

    ```console
    $ sudo cp docker/docker /usr/local/bin/
    ```

5.  通过运行 `hello-world` 镜像来验证 Docker 是否正确安装。`<hostname>` 的值是运行
    Docker 守护进程且客户端可访问的主机名或 IP 地址。

    ```console
    $ sudo docker -H <hostname> run hello-world
    ```

    此命令下载一个测试镜像并在容器中运行它。当
    容器运行时，它会打印一条消息并退出。

## 在 Windows 上安装服务器和客户端二进制文件 {#install-server-and-client-binaries-on-windows}

> [!NOTE]
>
> 以下部分描述如何在 Windows
> Server 上安装 Docker 守护进程，这仅允许您运行 Windows 容器。当您在
> Windows Server 上安装 Docker 守护进程时，该守护进程不包含 Docker 组件，
> 如 `buildx` 和 `compose`。如果您运行的是 Windows 10 或 11，
> 我们建议您改为安装 [Docker Desktop](/manuals/desktop/_index.md)。

Windows 上的二进制软件包同时包含 `dockerd.exe` 和 `docker.exe`。在 Windows 上，
这些二进制文件仅提供运行原生 Windows 容器（而非
Linux 容器）的能力。

要安装服务器和客户端二进制文件，请执行以下步骤：

1. 下载静态二进制文件归档文件。前往
    [https://download.docker.com/win/static/stable/x86_64](https://download.docker.com/win/static/stable/x86_64) 并从列表中选择最新版本。

2. 运行以下 PowerShell 命令以安装并将归档文件解压到您的程序文件：

    ```powershell
    PS C:\> Expand-Archive /path/to/<FILE>.zip -DestinationPath $Env:ProgramFiles
    ```

3. 注册服务并启动 Docker Engine：

    ```powershell
    PS C:\> &$Env:ProgramFiles\Docker\dockerd --register-service
    PS C:\> Start-Service docker
    ```

4.  通过运行 `hello-world` 镜像来验证 Docker 是否正确安装。

    ```powershell
    PS C:\> &$Env:ProgramFiles\Docker\docker run hello-world:nanoserver
    ```

    此命令下载一个测试镜像并在容器中运行它。当
    容器运行时，它会打印一条消息并退出。

## 升级静态二进制文件

要升级手动安装的 Docker Engine，首先停止本地运行的任何
`dockerd` 或 `dockerd.exe` 进程，然后按照
常规安装步骤在现有版本之上安装新版本。

## 后续步骤

- 继续阅读 [Linux 安装后步骤](linux-postinstall.md)。
