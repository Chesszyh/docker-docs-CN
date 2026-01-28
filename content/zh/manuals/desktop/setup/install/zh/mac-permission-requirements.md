---
description: 了解 Docker Desktop for Mac 的权限要求以及不同版本之间的差异
keywords: Docker Desktop, mac, security, install, permissions
title: 了解 Mac 上 Docker Desktop 的权限要求
linkTitle: Mac 权限要求
aliases:
- /docker-for-mac/privileged-helper/
- /desktop/mac/privileged-helper/
- /desktop/mac/permission-requirements/
- /desktop/install/mac-permission-requirements/
weight: 20
---

本页面包含有关在 Mac 上运行和安装 Docker Desktop 的权限要求的信息。

它还阐明了以 `root` 身份运行容器与在主机上拥有 `root` 访问权限之间的区别。

Mac 上的 Docker Desktop 在设计时考虑了安全性。仅在绝对必要时才需要管理员权限。

## 权限要求

Docker Desktop for Mac 以非特权用户身份运行。但是，Docker Desktop 需要某些功能来执行有限的一组特权配置，例如：
 - [安装符号链接](#installing-symlinks)到 `/usr/local/bin`。
 - [绑定特权端口](#binding-privileged-ports)，即小于 1024 的端口。虽然特权端口（1024 以下的端口）通常不用作安全边界，但操作系统仍会阻止非特权进程绑定到它们，这会导致像 `docker run -p 127.0.0.1:80:80 docker/getting-started` 这样的命令失败。
 - [确保 `localhost` 和 `kubernetes.docker.internal` 已定义](#ensuring-localhost-and-kubernetesdockerinternal-are-defined)在 `/etc/hosts` 中。某些旧的 macOS 安装在 `/etc/hosts` 中没有 `localhost`，这会导致 Docker 失败。定义 DNS 名称 `kubernetes.docker.internal` 允许 Docker 与容器共享 Kubernetes 上下文。
 - 安全缓存注册表访问管理策略，该策略对开发者是只读的。

特权访问在安装期间授予。

Docker Desktop for Mac 首次启动时，会显示一个安装窗口，您可以在其中选择使用默认设置（适用于大多数开发者，需要授予特权访问权限）或使用高级设置。

如果您在具有较高安全要求的环境中工作，例如禁止本地管理员访问的环境，则可以使用高级设置来消除授予特权访问的需要。您可以配置：
- Docker CLI 工具的位置，可以在系统目录或用户目录中
- 默认 Docker 套接字
- 特权端口映射

根据您配置的高级设置，您必须输入密码进行确认。

您可以稍后从 **Settings** 中的 **Advanced** 页面更改这些配置。

### 安装符号链接

Docker 二进制文件默认安装在 `/Applications/Docker.app/Contents/Resources/bin`。Docker Desktop 在 `/usr/local/bin` 中为这些二进制文件创建符号链接，这意味着它们在大多数系统上会自动包含在 `PATH` 中。

您可以在安装 Docker Desktop 期间选择将符号链接安装在 `/usr/local/bin` 或 `$HOME/.docker/bin` 中。

如果选择 `/usr/local/bin`，而非特权用户无法写入此位置，Docker Desktop 在创建指向 Docker 二进制文件的符号链接之前需要授权以确认此选择。如果选择 `$HOME/.docker/bin`，则不需要授权，但您必须[手动将 `$HOME/.docker/bin`](/manuals/desktop/settings-and-maintenance/settings.md#advanced) 添加到您的 PATH。

您还可以选择启用 `/var/run/docker.sock` 符号链接的安装。创建此符号链接可确保依赖默认 Docker 套接字路径的各种 Docker 客户端无需额外更改即可工作。

由于 `/var/run` 作为 tmpfs 挂载，其内容在重启时会被删除，包括指向 Docker 套接字的符号链接。为确保 Docker 套接字在重启后存在，Docker Desktop 设置了一个 `launchd` 启动任务，通过运行 `ln -s -f /Users/<user>/.docker/run/docker.sock /var/run/docker.sock` 来创建符号链接。这确保您不会在每次启动时被提示创建符号链接。如果您在安装时未启用此选项，则不会创建符号链接和启动任务，您可能需要在使用的客户端中显式设置 `DOCKER_HOST` 环境变量为 `/Users/<user>/.docker/run/docker.sock`。Docker CLI 依赖当前上下文来检索套接字路径，当前上下文在 Docker Desktop 启动时设置为 `desktop-linux`。

### 绑定特权端口

您可以在安装期间或安装后从 **Settings** 中的 **Advanced** 页面选择启用特权端口映射。Docker Desktop 需要授权以确认此选择。

### 确保 `localhost` 和 `kubernetes.docker.internal` 已定义

您有责任确保 localhost 解析为 `127.0.0.1`，如果使用 Kubernetes，确保 `kubernetes.docker.internal` 解析为 `127.0.0.1`。

## 从命令行安装

在安装期间使用 [install 命令](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line)的 `--user` 标志来应用特权配置。在这种情况下，您在首次运行 Docker Desktop 时不会被提示授予 root 权限。具体来说，`--user` 标志：
- 如果存在，卸载之前的 `com.docker.vmnetd`
- 设置符号链接
- 确保 `localhost` 解析为 `127.0.0.1`

这种方法的限制是 Docker Desktop 只能由每台机器上的一个用户账户运行，即 `-–user` 标志中指定的那个。

## 特权助手

在需要特权助手的有限情况下，例如绑定特权端口或缓存注册表访问管理策略，特权助手由 `launchd` 启动并在后台运行，除非如前所述在运行时被禁用。Docker Desktop 后端通过 UNIX 域套接字 `/var/run/com.docker.vmnetd.sock` 与特权助手通信。它执行的功能有：
- 绑定小于 1024 的特权端口。
- 安全缓存注册表访问管理策略，该策略对开发者是只读的。
- 卸载特权助手。

特权助手进程的移除方式与移除 `launchd` 进程的方式相同。

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

## 在 Linux 虚拟机内以 root 身份运行容器

使用 Docker Desktop 时，Docker 守护进程和容器在 Docker 管理的轻量级 Linux 虚拟机中运行。这意味着虽然容器默认以 `root` 身份运行，但这不会授予对 Mac 主机的 `root` 访问权限。Linux 虚拟机充当安全边界，限制可以从主机访问的资源。从主机绑定挂载到 Docker 容器的任何目录仍保留其原始权限。

## 增强容器隔离

此外，Docker Desktop 支持[增强容器隔离（Enhanced Container Isolation）模式](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)（ECI），仅适用于 Business 客户，它在不影响开发者工作流程的情况下进一步保护容器。

ECI 自动在 Linux 用户命名空间内运行所有容器，使得容器中的 root 被映射到 Docker Desktop 虚拟机内的非特权用户。ECI 使用这种和其他高级技术进一步保护 Docker Desktop Linux 虚拟机内的容器，使它们与 Docker 守护进程和虚拟机内运行的其他服务进一步隔离。
