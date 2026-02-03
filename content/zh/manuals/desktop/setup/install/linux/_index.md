---
description: 通过我们的分步骤安装指南轻松在 Linux 上安装 Docker，涵盖系统要求、受支持平台以及后续步骤。
keywords: linux, 安装 docker linux, docker linux, linux docker 安装, docker for linux, docker desktop for linux, 在 linux 上安装 docker, docker linux 下载, 如何在 linux 上安装 docker, linux 对比 docker engine, 切换 docker 上下文
title: 在 Linux 上安装 Docker Desktop
linkTitle: Linux
weight: 60
aliases:
- /desktop/linux/install/
- /desktop/install/linux-install/
- /desktop/install/linux/
---

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页包含有关通用系统要求、受支持平台的信息，以及如何在 Linux 上安装 Docker Desktop 的说明。

> [!IMPORTANT]
>
> Linux 版 Docker Desktop 运行一个虚拟机 (VM)，并在启动时创建并使用自定义的 Docker 上下文 `desktop-linux`。
>
> 这意味着在安装之前部署在 Linux Docker 引擎（Docker Engine）上的镜像和容器在 Linux 版 Docker Desktop 中是不可用的。
>
> {{< accordion title="Docker Desktop 对比 Docker Engine：有什么区别？" >}}

> [!IMPORTANT]
>
> 对于在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用通过 Docker Desktop 获取的 Docker Engine，需要[付费订阅](https://www.docker.com/pricing/)。

Linux 版 Docker Desktop 提供了一个用户友好的图形界面，简化了容器和服务的管理。它包含了 Docker Engine，因为这是驱动 Docker 容器的核心技术。Linux 版 Docker Desktop 还附带了 Docker Scout 和 Docker Extensions 等额外功能。

#### 同时安装 Docker Desktop 和 Docker Engine

Linux 版 Docker Desktop 和 Docker Engine 可以并排安装在同一台机器上。Linux 版 Docker Desktop 将容器和镜像存储在 VM 内的一个隔离存储位置，并提供控制其[资源占用](/manuals/desktop/settings-and-maintenance/settings.md#resources)的选项。由于 Docker Desktop 使用专用存储位置，因此它不会干扰同一台机器上的 Docker Engine 安装。

虽然可以同时运行 Docker Desktop 和 Docker Engine，但在某些情况下同时运行两者可能会导致问题。例如，在为容器映射网络端口 (`-p` / `--publish`) 时，Docker Desktop 和 Docker Engine 可能会尝试保留机器上的同一个端口，这会导致冲突（“端口已被占用”）。

我们通常建议在使用 Docker Desktop 时停止 Docker Engine，以防止 Docker Engine 消耗资源并避免上述冲突。

使用以下命令停止 Docker Engine 服务：

```console
$ sudo systemctl stop docker docker.socket containerd
```

根据您的安装情况，Docker Engine 可能会被配置为在机器启动时作为系统服务自动启动。使用以下命令禁用 Docker Engine 服务，并防止其自动启动：

```console
$ sudo systemctl disable docker docker.socket containerd
```

### 在 Docker Desktop 和 Docker Engine 之间切换

Docker CLI 可以用于与多个 Docker Engine 交互。例如，您可以使用同一个 Docker CLI 来控制本地的 Docker Engine，也可以控制云端运行的远程 Docker Engine 实例。[Docker 上下文 (Contexts)](/manuals/engine/manage-resources/contexts.md) 允许您在不同的 Docker Engine 实例之间切换。

安装 Docker Desktop 时，会创建一个专门的 `desktop-linux` 上下文用于与 Docker Desktop 交互。启动时，Docker Desktop 会自动将其自己的上下文 (`desktop-linux`) 设置为当前上下文。这意味着随后的 Docker CLI 命令都将针对 Docker Desktop 执行。关闭时，Docker Desktop 会将当前上下文重置为 `default`（默认）上下文。

使用 `docker context ls` 命令查看机器上可用的上下文。当前上下文会用星号 (`*`) 标出。

```console
$ docker context ls
NAME            DESCRIPTION                               DOCKER ENDPOINT                                  ...
default *       Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                      ...
desktop-linux                                             unix:///home/<user>/.docker/desktop/docker.sock  ...        
```

如果您在同一台机器上同时安装了 Docker Desktop 和 Docker Engine，可以运行 `docker context use` 命令在 Docker Desktop 和 Docker Engine 上下文之间切换。例如，使用 `default` 上下文与 Docker Engine 交互：

```console
$ docker context use default
default
Current context is now "default"
```
  
使用 `desktop-linux` 上下文与 Docker Desktop 交互：
 
```console
$ docker context use desktop-linux
desktop-linux
Current context is now "desktop-linux"
``` 
有关更多详细信息，请参阅 [Docker 上下文文档](/manuals/engine/manage-resources/contexts.md)。
{{< /accordion >}}

## 受支持的平台

Docker 为以下 Linux 发行版和架构提供 `.deb` 和 `.rpm` 软件包：

| 平台 | x86_64 / amd64 | 
|:------------------------|:-----------------------:|
| [Ubuntu](ubuntu.md)                         | ✅  |
| [Debian](debian.md)                         | ✅  |
| [Red Hat Enterprise Linux (RHEL)](rhel.md)  | ✅  |
| [Fedora](fedora.md)                         | ✅  |


[Arch](archlinux.md) 系发行版提供实验性软件包。Docker 尚未对该安装进行测试或验证。

Docker 对上述发行版的当前 LTS 版本及最新版本提供 Docker Desktop 支持。随着新版本的发布，Docker 将停止支持最旧的版本，转而支持最新版本。

## 通用系统要求

要成功安装 Docker Desktop，您的 Linux 宿主机必须满足以下通用要求：

- 64 位内核且 CPU 支持虚拟化。
- KVM 虚拟化支持。请按照 [KVM 虚拟化支持说明](#kvm-虚拟化支持) 检查 KVM 内核模块是否已启用，以及如何提供对 KVM 设备的访问权限。
- QEMU 版本必须为 5.2 或更高。建议升级到最新版本。
- systemd 初始化系统。
- GNOME、KDE 或 MATE 桌面环境。
  - 对于许多 Linux 发行版，GNOME 环境不支持托盘图标。要添加托盘图标支持，您需要安装 GNOME 扩展。例如：[AppIndicator](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 至少 4 GB 内存。
- 允许在用户命名空间中配置 ID 映射，请参阅[文件共享](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#how-do-i-enable-file-sharing)。请注意，对于 Docker Desktop 4.35 及更高版本，这不再是必需的。
- 推荐：[初始化 `pass`](/manuals/desktop/setup/sign-in.md#credentials-management-for-linux-users) 用于凭据管理。

Linux 版 Docker Desktop 会运行一个虚拟机 (VM)。有关原因的更多信息，请参阅[为什么 Linux 版 Docker Desktop 需要运行 VM](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#why-does-docker-desktop-for-linux-run-a-vm)。

> [!NOTE]
>
> Docker 不提供在嵌套虚拟化场景中运行 Linux 版 Docker Desktop 的支持。建议您在受支持的发行版上原生运行 Linux 版 Docker Desktop。

### KVM 虚拟化支持

Docker Desktop 运行的 VM 需要 [KVM 支持](https://www.linux-kvm.org)。

如果宿主机支持虚拟化，`kvm` 模块应该会自动加载。要手动加载模块，请运行：

```console
$ modprobe kvm
```

根据宿主机的处理器类型，必须加载相应的模块：

```console
$ modprobe kvm_intel  # Intel 处理器

$ modprobe kvm_amd    # AMD 处理器
```

如果上述命令失败，可以通过运行以下命令查看诊断信息：

```console
$ kvm-ok
```

要检查 KVM 模块是否已启用，请运行：

```console
$ lsmod | grep kvm
kvm_amd               167936  0
ccp                   126976  1 kvm_amd
kvm                  1089536  1 kvm_amd
irqbypass              16384  1 kvm
```

#### 设置 KVM 设备用户权限

要检查 `/dev/kvm` 的所有权，请运行：

```console
$ ls -al /dev/kvm
```

将您的用户添加到 `kvm` 组，以便访问 KVM 设备：

```console
$ sudo usermod -aG kvm $USER
```

注销并重新登录，以便重新评估您的组数组成员身份。

## 下一步

- 根据您具体的 Linux 发行版安装 Linux 版 Docker Desktop：
   - [在 Ubuntu 上安装](ubuntu.md)
   - [在 Debian 上安装](debian.md)
   - [在 Red Hat Enterprise Linux (RHEL) 上安装](rhel.md)
   - [在 Fedora 上安装](fedora.md)
   - [在 Arch 上安装](archlinux.md)
