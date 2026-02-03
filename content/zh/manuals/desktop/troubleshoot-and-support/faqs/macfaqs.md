---
description: Mac 版 Docker Desktop 的常见问题
keywords: desktop, mac, faqs, 常见问题
title: Mac 版 Docker Desktop 常见问题 (FAQ)
linkTitle: Mac
tags: [FAQ]
aliases:
- /desktop/mac/space/
- /docker-for-mac/space/
- /desktop/faqs/macfaqs/
weight: 20
---

### 什么是 HyperKit？

HyperKit 是一款构建在 macOS Hypervisor.framework 之上的虚拟机管理程序（Hypervisor）。它完全在用户空间运行，没有其他依赖。

Docker 使用 HyperKit 来消除对其他虚拟机产品（如 Oracle VirtualBox 或 VMware Fusion）的需求。

### HyperKit 的优势是什么？

HyperKit 比 VirtualBox 和 VMware Fusion 更轻量，且内置的版本是专为 Mac 上的 Docker 工作负载定制的。

### Docker Desktop 将 Linux 容器和镜像存储在哪里？

Docker Desktop 将 Linux 容器和镜像存储在 Mac 文件系统中的单个大型“磁盘镜像”文件中。这与 Linux 上的 Docker 不同，后者通常将容器和镜像存储在 `/var/lib/docker` 目录中。

#### 磁盘镜像文件在哪里？

要找到磁盘镜像文件，请在 Docker Desktop 控制面板中选择 **Settings**，然后选择 **Resources** 选项卡下的 **Advanced**。

**Advanced** 选项卡会显示磁盘镜像的位置。它还会显示磁盘镜像的最大容量以及其实际占用的空间。请注意，其他工具可能会以最大文件大小而非实际文件大小来显示该文件的空间占用情况。

#### 如果文件太大怎么办？

如果磁盘镜像文件太大，您可以：

- 将其移动到更大的驱动器
- 删除不需要的容器和镜像
- 减小文件的最大允许容量

##### 如何将文件移动到更大的驱动器？

要将磁盘镜像文件移动到其他位置：

1. 在 **Resources** 选项卡下选择 **Settings** -> **Advanced**。

2. 在 **Disk image location** 部分，选择 **Browse** 并为磁盘镜像选择一个新位置。

3. 选择 **Apply** 使更改生效。

> [!IMPORTANT]
>
> 不要直接在访达 (Finder) 中移动该文件，否则会导致 Docker Desktop 无法追踪到该文件。

##### 如何删除不需要的容器和镜像？

检查您是否有任何不需要的容器和镜像。如果您的客户端和守护进程 API 版本为 1.25 或更高（使用客户端上的 `docker version` 命令检查），可以通过运行以下命令查看详细的空间占用信息：

```console
$ docker system df -v
```

或者，列出所有镜像：

```console
$ docker image ls
```

列出所有容器：

```console
$ docker container ls -a
```

如果存在大量冗余对象，请运行以下命令：

```console
$ docker system prune
```

此命令将移除所有已停止的容器、未使用的网络、悬空 (dangling) 镜像以及构建缓存。

根据磁盘镜像文件的格式，宿主机可能需要几分钟才能回收空间。如果文件名为：

- `Docker.raw`：宿主机上的空间应在几秒钟内回收。
- `Docker.qcow2`：空间将在几分钟后由后台进程释放。

空间仅在删除镜像时释放。在运行中的容器内删除文件不会自动释放空间。要随时触发空间回收，请运行以下命令：

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

请注意，许多工具报告的是最大文件大小，而非实际文件大小。要通过终端查询宿主机上文件的实际大小，请运行：

```console
$ cd ~/Library/Containers/com.docker.docker/Data/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

在此示例中，磁盘的实际大小为 `2333548` KB，而磁盘的最大容量为 `64` GB。

##### 如何减小文件的最大容量？

要减小磁盘镜像文件的最大容量：

1. 在 **Resources** 选项卡下选择 **Settings** -> **Advanced**。

2. **Disk image size** 部分包含一个滑块，允许您更改磁盘镜像的最大容量。调节滑块设置一个较低的限制。

3. 选择 **Apply**。

当您减小最大容量时，当前的磁盘镜像文件将被删除，因此所有的容器和镜像都将丢失。

### 如何添加 TLS 证书？

您可以向 Docker 守护进程添加受信任的证书颁发机构 (CA)（用于验证注册表服务器证书）和客户端证书（用于对注册表进行身份验证）。

#### 添加自定义 CA 证书（服务器端）

支持所有受信任的 CA（根 CA 或中间 CA）。Docker Desktop 会根据 Mac 钥匙串（Keychain）创建一个包含所有用户信任 CA 的证书包，并将其附加到 Moby 受信任证书中。因此，如果宿主机用户信任某个企业 SSL 证书，Docker Desktop 也会信任它。

要手动添加自定义自签名证书，首先将证书添加到 macOS 钥匙串中，Docker Desktop 会自动读取它。示例如下：

```console
$ sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ca.crt
```

或者，如果您只想将证书添加到您自己的本地钥匙串（而不是针对所有用户），请运行以下命令：

```console
$ security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain ca.crt
```

另请参阅 [证书的目录结构](#证书的目录结构)。

> [!NOTE]
>
> 在对钥匙串或 `~/.docker/certs.d` 目录进行任何更改后，您需要重启 Docker Desktop 才能使更改生效。

有关如何操作的完整说明，请参阅博客文章 [向 Docker 和 Mac 版 Docker Desktop 添加自签名注册表证书](https://blog.container-solutions.com/adding-self-signed-registry-certs-docker-mac)。

#### 添加客户端证书

您可以将客户端证书放在 `~/.docker/certs.d/<注册表地址>:<端口>/client.cert` 和 `~/.docker/certs.d/<注册表地址>:<端口>/client.key` 中。

当 Docker Desktop 应用程序启动时，它会将您 Mac 上的 `~/.docker/certs.d` 文件夹复制到 Moby（Docker Desktop 的虚拟机）上的 `/etc/docker/certs.d` 目录中。

> [!NOTE]
>
> * 在对钥匙串或 `~/.docker/certs.d` 目录进行任何更改后，您需要重启 Docker Desktop 才能使更改生效。
>
> * 注册表不能被列为 _非安全注册表 (insecure registry)_。Docker Desktop 会忽略列在非安全注册表下的证书，并且不会发送客户端证书。尝试从该注册表拉取镜像的命令（如 `docker run`）会在命令行以及注册表端产生错误消息。

#### 证书的目录结构

如果您采用以下目录结构，则无需手动将 CA 证书添加到 Mac OS 系统登录：

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
   ├── ca.crt
   ├── client.cert
   └── client.key
```

以下进一步说明并解释了带有自定义证书的配置：

```text
/etc/docker/certs.d/        <-- 证书目录
└── localhost:5000          <-- 主机名:端口
   ├── client.cert          <-- 客户端证书
   ├── client.key           <-- 客户端密钥
   └── ca.crt               <-- 签署注册表证书的 CA
```

只要您的钥匙串中也有该 CA 证书，您也可以使用以下目录结构：

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
    ├── client.cert
    └── client.key
```

要了解更多关于如何为注册表安装 CA 根证书以及如何设置客户端 TLS 证书进行验证的信息，请参阅 Docker Engine 主题中的 [使用证书验证存储库客户端](/manuals/engine/security/certificates.md)。
