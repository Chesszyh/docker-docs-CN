---
description: 适用于所有平台的 Docker Desktop 常见问题
keywords: desktop, mac, windows, faqs, 常见问题
title: Docker Desktop 通用常见问题 (FAQ)
linkTitle: 通用
tags: [FAQ]
aliases:
- /mackit/faqs/
- /docker-for-mac/faqs/
- /docker-for-windows/faqs/
- /desktop/faqs/
- /desktop/faqs/general/
weight: 10
---

### 我可以离线使用 Docker Desktop 吗？

可以，您可以离线使用 Docker Desktop。但是，您无法访问需要活跃互联网连接的功能。此外，在离线使用 Docker Desktop 或在物理隔离（air-gapped）环境中，任何需要登录的功能都将无法使用。这包括：

- [学习中心](/manuals/desktop/use-desktop/_index.md) 中的资源
- 向 Docker Hub 推送或拉取镜像
- [镜像访问管理 (Image Access Management)](/manuals/security/for-developers/access-tokens.md)
- [静态漏洞扫描](/manuals/docker-hub/repos/manage/vulnerability-scanning.md)
- 在 Docker 控制面板（Dashboard）中查看远程镜像
- 使用 [BuildKit](/manuals/build/buildkit/_index.md#getting-started) 时进行 Docker 构建。您可以通过禁用 BuildKit 来规避此问题。运行 `DOCKER_BUILDKIT=0 docker build .` 即可禁用 BuildKit。
- [Kubernetes](/manuals/desktop/features/kubernetes.md)（镜像会在您首次启用 Kubernetes 时下载）
- 检查更新
- [应用内诊断](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#从应用内诊断)（包括 [自诊断工具](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#从应用内诊断)）
- 发送使用统计信息
- 当 `networkMode` 设置为 `mirrored` 时

### 如何连接到远程 Docker Engine API？

要连接到远程 Engine API，您可能需要为 Docker 客户端和开发工具提供 Engine API 的位置。

Mac 和 Windows WSL 2 用户可以通过 Unix 套接字连接到 Docker Engine：`unix:///var/run/docker.sock`。

如果您使用的应用程序（如 [Apache Maven](https://maven.apache.org/)）需要设置 `DOCKER_HOST` 和 `DOCKER_CERT_PATH` 环境变量，请指定这些变量以通过 Unix 套接字连接到 Docker 实例。

例如：

```console
$ export DOCKER_HOST=unix:///var/run/docker.sock
```

Docker Desktop Windows 用户可以通过 **命名管道 (Named pipe)** 连接到 Docker Engine：`npipe:////./pipe/docker_engine`，或通过此 URL 使用 **TCP 套接字**：`tcp://localhost:2375`。

详情请参阅 [Docker Engine API](/reference/api/engine/_index.md)。

### 如何从容器连接到宿主机上的服务？

宿主机的 IP 地址是变动的，或者如果您没有网络访问权限，则没有 IP。建议您连接到特殊的 DNS 名称 `host.docker.internal`，它会被解析为宿主机使用的内部 IP 地址。

有关更多信息和示例，请参阅 [如何从容器连接到宿主机上的服务](/manuals/desktop/features/networking.md#我想从容器连接到宿主机上的服务)。

### 我可以将 USB 设备透传给容器吗？

Docker Desktop 不支持直接的 USB 设备透传。但是，您可以使用 USB over IP 技术将常用的 USB 设备连接到 Docker Desktop 虚拟机，并进而转发到容器中。有关更多详细信息，请参阅 [在 Docker Desktop 中使用 USB/IP](/manuals/desktop/features/usbip.md)。

### 如何在没有管理员权限的情况下运行 Docker Desktop？

Docker Desktop 仅在安装时需要管理员权限。安装完成后，运行它不需要管理员权限。但是，为了让非管理员用户能够运行 Docker Desktop，必须使用特定的安装程序标志进行安装，并满足某些前提条件（因平台而异）。

{{< tabs >}}
{{< tab name="Mac" >}}

要在 Mac 上运行 Docker Desktop 而不需要管理员权限，请通过命令行进行安装并传递 `—user=<userid>` 安装程序标志：

```console
$ /Applications/Docker.app/Contents/MacOS/install --user=<userid>
```

然后，您可以使用指定的 ID 登录您的机器，并启动 Docker Desktop。

> [!NOTE]
> 
> 在启动 Docker Desktop 之前，如果 `~/Library/Group Containers/group.com.docker/` 目录中已经存在 `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本中的 `settings.json`），那么在您选择 **Finish** 时，会看到一个 **Finish setting up Docker Desktop** 窗口提示需要管理员权限。为了避免这种情况，请确保在启动应用程序之前删除任何以前安装留下的 `settings-store.json`（或 `settings.json`）文件。

{{< /tab >}}
{{< tab name="Windows" >}}

> [!NOTE]
>
> 如果您使用的是 WSL 2 后端，请首先确保您满足 WSL 2 的 [最低版本要求](/manuals/desktop/features/wsl/best-practices.md)。否则，请先更新 WSL 2。

要在 Windows 上运行 Docker Desktop 而不需要管理员权限，请通过命令行进行安装并传递 `—always-run-service` 安装程序标志。

```console
$ "Docker Desktop Installer.exe" install —always-run-service
```

{{< /tab >}}
{{< /tabs >}}
