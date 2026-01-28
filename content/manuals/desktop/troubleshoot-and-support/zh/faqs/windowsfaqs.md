---
description: Docker Desktop for Windows 的常见问题
keywords: desktop, windows, faqs
title: Docker Desktop for Windows 常见问题
linkTitle: Windows
tags: [FAQ]
weight: 30
---

### 我可以同时使用 VirtualBox 和 Docker Desktop 吗？

可以，如果您在机器上启用了 [Windows Hypervisor Platform](https://docs.microsoft.com/en-us/virtualization/api/) 功能，您可以同时运行 VirtualBox 和 Docker Desktop。

### 为什么需要 Windows 10 或 Windows 11？

Docker Desktop 使用 Windows Hyper-V 功能。虽然旧版本的 Windows 有 Hyper-V，但它们的 Hyper-V 实现缺少 Docker Desktop 工作所需的关键功能。

### 我可以在 Windows Server 上运行 Docker Desktop 吗？

不可以，不支持在 Windows Server 上运行 Docker Desktop。

### 符号链接在 Windows 上如何工作？

Docker Desktop 支持两种类型的符号链接：Windows 原生符号链接和在容器内创建的符号链接。

Windows 原生符号链接在容器内显示为符号链接，而在容器内创建的符号链接则表示为 [mfsymlinks](https://wiki.samba.org/index.php/UNIX_Extensions#Minshall.2BFrench_symlinks)。这些是具有特殊元数据的普通 Windows 文件。因此，在容器内创建的符号链接在容器内显示为符号链接，但在主机上不是。

### Kubernetes 和 WSL 2 的文件共享

Docker Desktop 将 Windows 主机文件系统挂载到运行 Kubernetes 的容器内的 `/run/desktop` 下。
请参阅 [Stack Overflow 帖子](https://stackoverflow.com/questions/67746843/clear-persistent-volume-from-a-kubernetes-cluster-running-on-docker-desktop/69273405#69273)了解如何配置 Kubernetes Persistent Volume 来表示主机上的目录的示例。

### 如何添加自定义 CA 证书？

您可以将受信任的证书颁发机构（CA）添加到 Docker 守护进程以验证注册表服务器证书，以及添加客户端证书以向注册表进行身份验证。

Docker Desktop 支持所有受信任的证书颁发机构（CA）（根证书或中间证书）。Docker 识别存储在 Trust Root Certification Authorities 或 Intermediate Certification Authorities 下的证书。

Docker Desktop 基于 Windows 证书存储创建所有用户信任的 CA 的证书包，并将其附加到 Moby 的受信任证书中。因此，如果企业 SSL 证书在主机上被用户信任，它也会被 Docker Desktop 信任。

要了解有关如何为注册表安装 CA 根证书的更多信息，请参阅 Docker Engine 主题中的[使用证书验证仓库客户端](/manuals/engine/security/certificates.md)。

### 如何添加客户端证书？

您可以将客户端证书添加到
`~/.docker/certs.d/<MyRegistry><Port>/client.cert` 和
`~/.docker/certs.d/<MyRegistry><Port>/client.key`。您不需要使用 `git` 命令推送您的证书。

当 Docker Desktop 应用程序启动时，它会将 Windows 系统上的 `~/.docker/certs.d` 文件夹复制到 Moby（在 Hyper-V 上运行的 Docker Desktop 虚拟机）上的 `/etc/docker/certs.d` 目录。

对钥匙串或 `~/.docker/certs.d` 目录进行任何更改后，需要重新启动 Docker Desktop 才能使更改生效。

注册表不能被列为不安全的注册表（参见 [Docker 守护进程](/manuals/desktop/settings-and-maintenance/settings.md#docker-engine)）。Docker Desktop 会忽略不安全注册表下列出的证书，并且不会发送客户端证书。尝试从注册表拉取的命令（如 `docker run`）会在命令行和注册表上产生错误消息。

要了解有关如何设置用于验证的客户端 TLS 证书的更多信息，请参阅 Docker Engine 主题中的[使用证书验证仓库客户端](/manuals/engine/security/certificates.md)。
