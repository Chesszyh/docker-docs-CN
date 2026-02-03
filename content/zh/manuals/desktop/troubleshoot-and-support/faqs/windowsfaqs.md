---
description: Windows 版 Docker Desktop 的常见问题
keywords: desktop, windows, faqs, 常见问题
title: Windows 版 Docker Desktop 常见问题 (FAQ)
linkTitle: Windows
tags: [FAQ]
weight: 30
---

### 我可以同时使用 VirtualBox 和 Docker Desktop 吗？

可以。如果您的机器上开启了 [Windows Hypervisor Platform](https://docs.microsoft.com/en-us/virtualization/api/) 功能，就可以同时运行 VirtualBox 和 Docker Desktop。

### 为什么需要 Windows 10 或 Windows 11？

Docker Desktop 使用了 Windows Hyper-V 特性。虽然较旧版本的 Windows 也有 Hyper-V，但其实现缺乏 Docker Desktop 运行所需的关键特性。

### 我可以在 Windows Server 上运行 Docker Desktop 吗？

不可以，不支持在 Windows Server 上运行 Docker Desktop。

### 符号链接 (Symlinks) 在 Windows 上是如何工作的？

Docker Desktop 支持两种类型的符号链接：Windows 原生符号链接和在容器内部创建的符号链接。

Windows 原生符号链接在容器内部可见为符号链接，而容器内部创建的符号链接则表示为 [mfsymlinks](https://wiki.samba.org/index.php/UNIX_Extensions#Minshall.2BFrench_symlinks)。这些是带有特殊元数据的普通 Windows 文件。因此，容器内部创建的符号链接在容器内显示为符号链接，但在宿主机上并非如此。

### 配合 Kubernetes 和 WSL 2 进行文件共享

Docker Desktop 将 Windows 宿主机文件系统挂载到运行 Kubernetes 的容器内部的 `/run/desktop` 路径下。
参考 [Stack Overflow 帖子](https://stackoverflow.com/questions/67746843/clear-persistent-volume-from-a-kubernetes-cluster-running-on-docker-desktop/69273405#69273) 了解如何配置 Kubernetes 持久卷 (Persistent Volume) 以表示宿主机上的目录示例。

### 如何添加自定义 CA 证书？

您可以向 Docker 守护进程添加受信任的证书颁发机构 (CA) 以验证注册表服务器证书，还可以添加客户端证书以对注册表进行身份验证。

Docker Desktop 支持所有受信任的证书颁发机构 (CA)（根 CA 或中间 CA）。Docker 识别存储在“受信任的根证书颁发机构”或“中间证书颁发机构”下的证书。

Docker Desktop 会根据 Windows 证书存储区创建一个包含所有用户受信任 CA 的证书包，并将其附加到 Moby 受信任证书中。因此，如果宿主机用户信任某个企业 SSL 证书，Docker Desktop 也会信任它。

要了解有关如何为注册表安装 CA 根证书的更多信息，请参阅 Docker Engine 主题中的 [使用证书验证存储库客户端](/manuals/engine/security/certificates.md)。

### 如何添加客户端证书？

您可以将客户端证书放在 `~/.docker/certs.d/<注册表地址><端口>/client.cert` 和 `~/.docker/certs.d/<注册表地址><端口>/client.key` 中。您不需要使用 `git` 命令推送证书。

当 Docker Desktop 应用程序启动时，它会将您 Windows 系统上的 `~/.docker/certs.d` 文件夹复制到 Moby（在 Hyper-V 上运行的 Docker Desktop 虚拟机）上的 `/etc/docker/certs.d` 目录中。

在对钥匙串或 `~/.docker/certs.d` 目录进行任何更改后，您需要重启 Docker Desktop 才能使更改生效。

注册表不能列在“非安全注册表 (insecure registry)”中（参见 [Docker 守护进程](/manuals/desktop/settings-and-maintenance/settings.md#docker-引擎)）。Docker Desktop 会忽略列在非安全注册表下的证书，并且不会发送客户端证书。尝试从该注册表拉取的命令（如 `docker run`）会在命令行以及注册表端产生错误消息。

要了解有关如何设置客户端 TLS 证书进行验证的更多信息，请参阅 Docker Engine 主题中的 [使用证书验证存储库客户端](/manuals/engine/security/certificates.md)。
