---
description: 了解 Mac 版 Docker Desktop 的权限要求及其各版本之间的差异
keywords: Docker Desktop, mac, 安全, 安装, 权限
title: 了解 Mac 版 Docker Desktop 的权限要求
linkTitle: Mac 权限要求
aliases:
- /docker-for-mac/privileged-helper/
- /desktop/mac/privileged-helper/
- /desktop/mac/permission-requirements/
- /desktop/install/mac-permission-requirements/
weight: 20
---

本页包含关于在 Mac 上运行和安装 Docker Desktop 的权限要求信息。

它还阐明了在容器中以 `root` 身份运行与在宿主机上拥有 `root` 权限之间的区别。

Mac 版 Docker Desktop 在设计时充分考虑了安全性。只有在绝对必要时才需要管理员权限。

## 权限要求

Mac 版 Docker Desktop 以非特权用户身份运行。然而，Docker Desktop 需要某些功能来执行有限的一组特权配置，例如：
 - 在 `/usr/local/bin` 中 [安装符号链接](#安装符号链接)。
 - [绑定小于 1024 的特权端口](#绑定特权端口)。虽然特权端口（1024 以下的端口）通常不被用作安全边界，但操作系统仍会阻止非特权进程绑定到这些端口，这会导致像 `docker run -p 127.0.0.1:80:80 docker/getting-started` 这样的命令失效。
 - [确保在 `/etc/hosts` 中定义了 `localhost` 和 `kubernetes.docker.internal`](#确保定义了-localhost-和-kubernetesdockerinternal)。一些旧的 macOS 安装在 `/etc/hosts` 中没有 `localhost`，这会导致 Docker 运行失败。定义 DNS 名称 `kubernetes.docker.internal` 允许 Docker 与容器共享 Kubernetes 上下文。
 - 安全地缓存镜像库访问管理（Registry Access Management）策略，该策略对开发人员是只读的。

特权访问在安装过程中授予。

Mac 版 Docker Desktop 首次启动时，会显示一个安装窗口，您可以选择使用默认设置（适用于大多数开发人员，且需要您授予特权访问权限），或者使用高级设置。

如果您在安全性要求较高的环境中工作，例如禁止本地管理员访问权限的环境，则可以使用高级设置来取消授予特权访问的需要。您可以配置：
- Docker CLI 工具在系统或用户目录中的位置
- 默认 Docker 套接字
- 特权端口映射

根据您配置的哪些高级设置，您可能需要输入密码进行确认。

您稍后可以在 **Settings**（设置）中的 **Advanced**（高级）页面更改这些配置。

### 安装符号链接

Docker 二进制文件默认安装在 `/Applications/Docker.app/Contents/Resources/bin` 中。Docker Desktop 会在 `/usr/local/bin` 中为二进制文件创建符号链接，这意味着它们在大多数系统上都会自动包含在 `PATH` 中。

在安装 Docker Desktop 期间，您可以选择是在 `/usr/local/bin` 还是 `$HOME/.docker/bin` 中安装符号链接。

如果选择了 `/usr/local/bin` ，且该位置对非特权用户不可写，Docker Desktop 需要获得授权来确认此选择，然后在 `/usr/local/bin` 中创建指向 Docker 二进制文件的符号链接。如果选择了 `$HOME/.docker/bin` ，则不需要授权，但您必须 [手动将 `$HOME/.docker/bin` 添加到您的 PATH 中](/manuals/desktop/settings-and-maintenance/settings.md#高级-advanced)。

您还可以选择启用 `/var/run/docker.sock` 符号链接的安装。创建此符号链接可确保依赖于默认 Docker 套接字路径的各种 Docker 客户端无需额外更改即可工作。

由于 `/var/run` 被挂载为 tmpfs，其内容在重启时会被删除，包括 Docker 套接字的符号链接。为了确保重启后 Docker 套接字仍然存在，Docker Desktop 设置了一个 `launchd` 启动任务，通过运行 `ln -s -f /Users/<user>/.docker/run/docker.sock /var/run/docker.sock` 来创建符号链接。这确保了您不会在每次启动时都被提示创建符号链接。如果您在安装时未启用此选项，则不会创建符号链接和启动任务，您可能必须在所使用的客户端中显式将 `DOCKER_HOST` 环境变量设置为 `/Users/<user>/.docker/run/docker.sock` 。Docker CLI 依赖当前上下文来检索套接字路径，在 Docker Desktop 启动时，当前上下文被设置为 `desktop-linux` 。

### 绑定特权端口

您可以选择在安装期间启用特权端口映射，或者在安装后通过 **Settings** 中的 **Advanced** 页面启用。Docker Desktop 需要授权来确认此选择。

### 确保定义了 `localhost` 和 `kubernetes.docker.internal`

您有责任确保 localhost 被解析为 `127.0.0.1` ，并且如果使用了 Kubernetes，确保 `kubernetes.docker.internal` 被解析为 `127.0.0.1` 。

## 从命令行安装

特权配置在安装期间通过 [安装命令](/manuals/desktop/setup/install/mac-install.md#从命令行安装) 上的 `--user` 标志应用。在这种情况下，Docker Desktop 首次运行时不会提示您授予 root 权限。具体来说，`--user` 标志会：
- 卸载之前存在的 `com.docker.vmnetd`（如果存在）
- 设置符号链接
- 确保 `localhost` 被解析为 `127.0.0.1`

这种方法的局限性在于，每台机器只能由一个用户账户运行 Docker Desktop，即 `--user` 标志中指定的那个账户。

## 特权助手 (Privileged helper)

在需要特权助手的有限情况下（例如绑定特权端口或缓存镜像库访问管理策略），特权助手由 `launchd` 启动并在后台运行，除非如前所述在运行时将其禁用。Docker Desktop 后端通过 UNIX 域套接字 `/var/run/com.docker.vmnetd.sock` 与特权助手通信。它执行的功能包括：
- 绑定小于 1024 的特权端口。
- 安全地缓存镜像库访问管理策略，该策略对开发人员是只读的。
- 卸载特权助手。

移除特权助手进程的方法与移除 `launchd` 进程的方法相同。

```console
$ ps aux | grep vmnetd
root             28739   0.0  0.0 34859128    228   ??  Ss    6:03PM   0:00.06 /Library/PrivilegedHelperTools/com.docker.vmnetd
user             32222   0.0  0.0 34122828    808 s000  R+   12:55PM   0:00.00 grep vmnetd

$ sudo launchctl unload -w /Library/LaunchDaemons/com.docker.vmnetd.plist
Password:

$ ps aux | grep vmnetd
user             32242   0.0  0.0 34122828    716 s000  R+   12:55PM   0:00.00 grep vmnetd

$ rm /Library/LaunchDaemons/com.docker.vmnetd.plist

$ rm /Library/PrivilegedHelperTools/com.docker.vmnetd
```

## 在 Linux 虚拟机中以 root 身份运行的容器

在 Docker Desktop 中，Docker 守护进程和容器运行在由 Docker 管理的轻量级 Linux 虚拟机中。这意味着尽管容器默认以 `root` 身份运行，但这并不会授予对 Mac 宿主机的 `root` 访问权限。Linux 虚拟机充当了安全边界，限制了可以从宿主机访问的资源。从宿主机绑定挂载到 Docker 容器中的任何目录仍然保留其原始权限。

## 增强型容器隔离 (Enhanced Container Isolation)

此外，Docker Desktop 支持 [增强型容器隔离 (ECI) 模式](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)，该模式仅对 Business 客户可用，它在不影响开发人员工作流的前提下进一步增强了容器的安全性。

ECI 会自动在 Linux 用户命名空间中运行所有容器，这样容器中的 root 会被映射到 Docker Desktop 虚拟机内部的一个非特权用户。ECI 利用这一技术和其他高级技术进一步保护 Docker Desktop Linux 虚拟机内的容器，使其与虚拟机内运行的 Docker 守护进程及其他服务进一步隔离。
