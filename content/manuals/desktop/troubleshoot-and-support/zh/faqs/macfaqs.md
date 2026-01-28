---
description: Docker Desktop for Mac 的常见问题
keywords: desktop, mac, faqs
title: Docker Desktop for Mac 常见问题
linkTitle: Mac
tags: [FAQ]
aliases:
- /desktop/mac/space/
- /docker-for-mac/space/
- /desktop/faqs/macfaqs/
weight: 20
---

### 什么是 HyperKit？

HyperKit 是基于 macOS 中 Hypervisor.framework 构建的虚拟机监控程序。它完全运行在用户空间中，没有其他依赖。

Docker 使用 HyperKit 来消除对其他 VM 产品的需求，例如 Oracle VirtualBox 或 VMware Fusion。

### HyperKit 有什么优势？

HyperKit 比 VirtualBox 和 VMware Fusion 更轻量，其包含的版本是针对 Mac 上的 Docker 工作负载定制的。

### Docker Desktop 将 Linux 容器和镜像存储在哪里？

Docker Desktop 将 Linux 容器和镜像存储在 Mac 文件系统中的一个大型"磁盘镜像"文件中。这与 Linux 上的 Docker 不同，后者通常将容器和镜像存储在 `/var/lib/docker` 目录中。

#### 磁盘镜像文件在哪里？

要定位磁盘镜像文件，从 Docker Desktop Dashboard 选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

**Advanced** 选项卡显示磁盘镜像的位置。它还显示磁盘镜像的最大大小和磁盘镜像实际消耗的空间。请注意，其他工具可能会按最大文件大小而不是实际文件大小显示空间使用情况。

#### 如果文件太大怎么办？

如果磁盘镜像文件太大，您可以：

- 将其移动到更大的驱动器
- 删除不必要的容器和镜像
- 减少文件的最大允许大小

##### 如何将文件移动到更大的驱动器？

要将磁盘镜像文件移动到其他位置：

1. 选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

2. 在 **Disk image location** 部分，选择 **Browse** 并为磁盘镜像选择新位置。

3. 选择 **Apply** 使更改生效。

> [!IMPORTANT]
>
> 不要直接在 Finder 中移动文件，因为这可能导致 Docker Desktop 无法追踪该文件。

##### 如何删除不必要的容器和镜像？

检查是否有不必要的容器和镜像。如果您的客户端和守护进程 API 运行的是 1.25 或更高版本（在客户端上使用 `docker version` 命令检查您的客户端和守护进程 API 版本），您可以通过运行以下命令查看详细的空间使用信息：

```console
$ docker system df -v
```

或者，要列出镜像，运行：

```console
$ docker image ls
```

要列出容器，运行：

```console
$ docker container ls -a
```

如果有大量冗余对象，运行以下命令：

```console
$ docker system prune
```

此命令会删除所有已停止的容器、未使用的网络、悬空镜像和构建缓存。

根据磁盘镜像文件的格式，在主机上回收空间可能需要几分钟。如果文件名为：

- `Docker.raw`，主机上的空间会在几秒钟内回收。
- `Docker.qcow2`，空间将在几分钟后由后台进程释放。

只有在删除镜像时才会释放空间。在运行中的容器内删除文件时不会自动释放空间。要在任何时候触发空间回收，运行以下命令：

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

请注意，许多工具报告的是最大文件大小，而不是实际文件大小。
要从终端查询主机上文件的实际大小，运行：

```console
$ cd ~/Library/Containers/com.docker.docker/Data/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

在此示例中，磁盘的实际大小是 `2333548` KB，而磁盘的最大大小是 `64` GB。

##### 如何减少文件的最大大小？

要减少磁盘镜像文件的最大大小：

1. 选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

2. **Disk image size** 部分包含一个滑块，允许您更改磁盘镜像的最大大小。调整滑块以设置较低的限制。

3. 选择 **Apply**。

当您减少最大大小时，当前磁盘镜像文件将被删除，因此所有容器和镜像都将丢失。

### 如何添加 TLS 证书？

您可以将受信任的证书颁发机构（CA）（用于验证注册表服务器证书）和客户端证书（用于向注册表进行身份验证）添加到您的 Docker 守护进程。

#### 添加自定义 CA 证书（服务器端）

支持所有受信任的 CA（根证书或中间证书）。Docker Desktop 基于 Mac 钥匙串创建所有用户信任的 CA 的证书包，并将其附加到 Moby 的受信任证书中。因此，如果企业 SSL 证书在主机上被用户信任，它也会被 Docker Desktop 信任。

要手动添加自定义的自签名证书，首先将证书添加到 macOS 钥匙串，Docker Desktop 会自动获取该证书。以下是一个示例：

```console
$ sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ca.crt
```

或者，如果您只想将证书添加到自己的本地钥匙串（而不是为所有用户），请运行以下命令：

```console
$ security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain ca.crt
```

另请参阅[证书目录结构](#directory-structures-for-certificates)。

> [!NOTE]
>
> 对钥匙串或 `~/.docker/certs.d` 目录进行任何更改后，需要重新启动 Docker Desktop 才能使更改生效。

有关如何执行此操作的完整说明，请参阅博客文章[为 Docker 和 Docker Desktop for Mac 添加自签名注册表证书](https://blog.container-solutions.com/adding-self-signed-registry-certs-docker-mac)。

#### 添加客户端证书

您可以将客户端证书放在
`~/.docker/certs.d/<MyRegistry>:<Port>/client.cert` 和
`~/.docker/certs.d/<MyRegistry>:<Port>/client.key`。

当 Docker Desktop 应用程序启动时，它会将 Mac 上的 `~/.docker/certs.d` 文件夹复制到 Moby（Docker Desktop 的 `xhyve` 虚拟机）上的 `/etc/docker/certs.d` 目录。

> [!NOTE]
>
> * 对钥匙串或 `~/.docker/certs.d` 目录进行任何更改后，需要重新启动 Docker Desktop 才能使更改生效。
>
> * 注册表不能被列为_不安全的注册表_。Docker Desktop 会忽略不安全注册表下列出的证书，并且不会发送客户端证书。尝试从注册表拉取的命令（如 `docker run`）会在命令行和注册表上产生错误消息。

#### 证书目录结构

如果您有以下目录结构，则无需手动将 CA 证书添加到 Mac OS 系统登录：

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
   ├── ca.crt
   ├── client.cert
   └── client.key
```

以下进一步说明和解释了使用自定义证书的配置：

```text
/etc/docker/certs.d/        <-- 证书目录
└── localhost:5000          <-- 主机名:端口
   ├── client.cert          <-- 客户端证书
   ├── client.key           <-- 客户端密钥
   └── ca.crt               <-- 签署注册表证书的证书颁发机构
```

只要 CA 证书也在您的钥匙串中，您也可以使用以下目录结构。

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
    ├── client.cert
    └── client.key
```

要了解有关如何为注册表安装 CA 根证书以及如何设置用于验证的客户端 TLS 证书的更多信息，请参阅 Docker Engine 主题中的[使用证书验证仓库客户端](/manuals/engine/security/certificates.md)。
