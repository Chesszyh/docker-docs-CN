---
description: 了解 Linux 用户推荐的 Docker Engine 安装后步骤，
  包括如何以非 root 用户身份运行 Docker 等。
keywords: run docker without sudo, docker running as root, docker post install, docker
  post installation, run docker as non root, docker non root user, how to run docker
  in linux, how to run docker linux, how to start docker in linux, run docker on linux
title: Docker Engine 的 Linux 安装后步骤
linkTitle: 安装后步骤
weight: 90
aliases:
- /engine/installation/linux/docker-ee/linux-postinstall/
- /engine/installation/linux/linux-postinstall/
- /install/linux/linux-postinstall/
---

这些可选的安装后步骤描述了如何配置您的
Linux 主机以更好地与 Docker 配合使用。

## 以非 root 用户身份管理 Docker

Docker 守护进程绑定到 Unix 套接字，而不是 TCP 端口。默认情况下，Unix 套接字由
`root` 用户拥有，其他用户只能使用
`sudo` 访问它。Docker 守护进程始终以 `root` 用户身份运行。

如果您不想在 `docker` 命令前加上 `sudo`，请创建一个名为 `docker` 的 Unix
组并向其添加用户。当 Docker 守护进程启动时，它会
创建一个可供 `docker` 组成员访问的 Unix 套接字。在某些 Linux
发行版上，使用包管理器安装 Docker Engine 时，系统会自动创建此组。在这种情况下，您无需
手动创建该组。

<!-- prettier-ignore -->
> [!WARNING]
>
> `docker` 组授予用户 root 级别的权限。有关
> 这如何影响系统安全性的详细信息，请参阅
> [Docker 守护进程攻击面](../security/_index.md#docker-daemon-attack-surface)。

> [!NOTE]
>
> 要在没有 root 权限的情况下运行 Docker，请参阅
> [以非 root 用户身份运行 Docker 守护进程（Rootless 模式）](../security/rootless.md)。

要创建 `docker` 组并添加您的用户：

1. 创建 `docker` 组。

   ```console
   $ sudo groupadd docker
   ```

2. 将您的用户添加到 `docker` 组。

   ```console
   $ sudo usermod -aG docker $USER
   ```

3. 注销并重新登录，以便重新评估您的组成员资格。

   > 如果您在虚拟机中运行 Linux，可能需要
   > 重新启动虚拟机才能使更改生效。

   您也可以运行以下命令来激活对组的更改：

   ```console
   $ newgrp docker
   ```

4. 验证您可以在没有 `sudo` 的情况下运行 `docker` 命令。

   ```console
   $ docker run hello-world
   ```

   此命令下载一个测试镜像并在容器中运行它。当
   容器运行时，它会打印一条消息并退出。

   如果您在将用户添加到 `docker` 组之前最初使用 `sudo` 运行了 Docker CLI 命令，
   您可能会看到以下错误：

   ```none
   WARNING: Error loading config file: /home/user/.docker/config.json -
   stat /home/user/.docker/config.json: permission denied
   ```

   此错误表明 `~/.docker/` 目录的权限设置不正确，
   这是由于之前使用了 `sudo` 命令导致的。

   要解决此问题，可以删除 `~/.docker/` 目录（它会被自动
   重新创建，但任何自定义设置都会丢失），或者使用以下命令更改其所有权和
   权限：

   ```console
   $ sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
   $ sudo chmod g+rwx "$HOME/.docker" -R
   ```

## 配置 Docker 使用 systemd 开机自启

许多现代 Linux 发行版使用 [systemd](https://systemd.io/) 来
管理系统启动时启动哪些服务。在 Debian 和 Ubuntu 上，
Docker 服务默认在启动时启动。要在使用 systemd 的其他 Linux 发行版上
自动启动 Docker 和 containerd，请运行
以下命令：

```console
$ sudo systemctl enable docker.service
$ sudo systemctl enable containerd.service
```

要停止此行为，请改用 `disable`。

```console
$ sudo systemctl disable docker.service
$ sudo systemctl disable containerd.service
```

您可以使用 systemd 单元文件在启动时配置 Docker 服务，
例如添加 HTTP 代理、为 Docker 运行时文件设置不同的目录或分区，
或其他自定义设置。有关示例，请参阅
[配置守护进程使用代理](/manuals/engine/daemon/proxy.md#systemd-unit-file)。

## 配置默认日志驱动程序

Docker 提供[日志驱动程序](/manuals/engine/logging/_index.md)用于
收集和查看主机上运行的所有容器的日志数据。
默认的日志驱动程序 `json-file` 将日志数据写入
主机文件系统上的 JSON 格式文件。随着时间的推移，这些日志文件会增大，
可能导致磁盘资源耗尽。

为避免因日志数据过度使用磁盘而导致的问题，请考虑以下
选项之一：

- 配置 `json-file` 日志驱动程序以开启
  [日志轮转](/manuals/engine/logging/drivers/json-file.md)。
- 使用默认执行日志轮转的
  [替代日志驱动程序](/manuals/engine/logging/configure.md#configure-the-default-logging-driver)，
  例如["local" 日志驱动程序](/manuals/engine/logging/drivers/local.md)。
- 使用将日志发送到远程日志聚合器的日志驱动程序。

## 后续步骤

- 查看 [Docker 研讨会](/get-started/workshop/_index.md)，了解如何构建镜像并将其作为容器化应用程序运行。
