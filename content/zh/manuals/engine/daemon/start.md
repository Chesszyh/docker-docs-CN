---
title: 启动守护进程
weight: 10
description: 手动启动 Docker 守护进程
keywords: docker, daemon, configuration, troubleshooting, 启动, 守护进程
---

本页介绍如何启动守护进程，无论是手动启动还是使用操作系统工具启动。

## 使用操作系统工具启动守护进程

在典型的安装中，Docker 守护进程由系统工具启动，而不是由用户手动启动。这使得机器重启时自动启动 Docker 变得更加容易。

启动 Docker 的命令取决于您的操作系统。请查阅 [安装 Docker](/manuals/engine/install/_index.md) 下的对应页面。

### 使用 systemd 启动

在某些操作系统 (如 Ubuntu 和 Debian) 上，Docker 守护进程服务会自动启动。使用以下命令手动启动它：

```console
$ sudo systemctl start docker
```

如果您希望 Docker 在开机时启动，请参阅 [配置 Docker 开机自启](/manuals/engine/install/linux-postinstall.md#configure-docker-to-start-on-boot-with-systemd)。

## 手动启动守护进程

如果您不想使用系统工具来管理 Docker 守护进程，或者只是想测试一下，可以使用 `dockerd` 命令手动运行它。根据您的操作系统配置，您可能需要使用 `sudo`。

当您以这种方式启动 Docker 时，它在前台运行并将其日志直接发送到您的终端。

```console
$ dockerd

INFO[0000] +job init_networkdriver()
INFO[0000] +job serveapi(unix:///var/run/docker.sock)
INFO[0000] Listening for HTTP on unix (/var/run/docker.sock)
```

要停止手动启动的 Docker，请在终端中按 `Ctrl+C`。
