---
description: Docker Desktop for Linux 的常见问题
keywords: desktop, linux, faqs
title: Docker Desktop for Linux 常见问题
linkTitle: Linux
tags: [FAQ]
aliases:
- /desktop/linux/space/
- /desktop/faqs/linuxfaqs/
weight: 40
---

### 为什么 Docker Desktop for Linux 要运行虚拟机？

Docker Desktop for Linux 运行虚拟机（VM）的原因如下：

1. 确保 Docker Desktop 跨平台提供一致的体验。

    在调研中，用户希望使用 Docker Desktop for Linux 的最常被提及的原因是确保在所有主要操作系统上获得一致的 Docker Desktop 体验和功能对等性。使用 VM 可以确保 Linux 用户的 Docker Desktop 体验与 Windows 和 macOS 高度一致。

2. 利用新的内核功能。

    有时我们希望使用新的操作系统功能。因为我们控制 VM 内的内核和操作系统，我们可以立即将这些功能推送给所有用户，即使是那些故意坚持使用其机器操作系统 LTS 版本的用户。

3. 增强安全性。

    容器镜像漏洞会对主机环境构成安全风险。大量非官方镜像不保证经过已知漏洞验证。恶意用户可以将镜像推送到公共仓库，并使用各种方法诱骗用户拉取和运行它们。VM 方法可以缓解这一威胁，因为任何获得 root 权限的恶意软件都被限制在 VM 环境中，无法访问主机。

    为什么不使用 rootless Docker？虽然这样做表面上可以限制对 root 用户的访问，在"top"中看起来更安全，但它允许非特权用户在自己的用户命名空间中获得 `CAP_SYS_ADMIN` 权限，并访问不期望被非特权用户使用的内核 API，从而导致[漏洞](https://www.openwall.com/lists/oss-security/2022/01/18/7)。

4. 以最小的性能影响提供功能对等性和增强安全性的优势。

    Docker Desktop for Linux 使用的 VM 采用 [`VirtioFS`](https://virtio-fs.gitlab.io)，这是一个共享文件系统，允许虚拟机访问位于主机上的目录树。我们的内部基准测试表明，通过为 VM 分配适当的资源，VirtioFS 可以实现接近原生的文件系统性能。

    因此，我们调整了 Docker Desktop for Linux 中 VM 的默认可用内存。您可以通过 Docker Desktop 的 **Settings** > **Resources** 选项卡中的 **Memory** 滑块来根据您的具体需求调整此设置。

### 如何启用文件共享？

Docker Desktop for Linux 使用 [VirtioFS](https://virtio-fs.gitlab.io/) 作为默认（也是目前唯一）的机制来启用主机和 Docker Desktop VM 之间的文件共享。

{{< accordion title="Docker Desktop 4.34 及更早版本的附加信息" >}}

为了不需要提升权限，同时也不会不必要地限制对共享文件的操作，Docker Desktop 在用户命名空间（参见 `user_namespaces(7)`）内运行文件共享服务（`virtiofsd`），并配置了 UID 和 GID 映射。因此，Docker Desktop 依赖于主机配置为允许当前用户使用从属 ID 委托。要使此功能生效，必须存在 `/etc/subuid`（参见 `subuid(5)`）和 `/etc/subgid`（参见 `subgid(5)`）文件。Docker Desktop 仅支持通过文件配置的从属 ID 委托。Docker Desktop 将当前用户 ID 和 GID 映射到容器中的 0。它使用 `/etc/subuid` 和 `/etc/subgid` 中与当前用户对应的第一个条目来设置容器中大于 0 的 ID 映射。

| 容器中的 ID | 主机上的 ID                                                                       |
| --------------- | -------------------------------------------------------------------------------- |
| 0 (root)        | 运行 Docker Desktop 的用户 ID（例如 1000）                                            |
| 1               | 0 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围起始值（例如 100000） |
| 2               | 1 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围起始值（例如 100001） |
| 3               | 2 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围起始值（例如 100002） |
| ...             | ...                                                                              |

如果 `/etc/subuid` 和 `/etc/subgid` 不存在，需要创建它们。
两个文件都应包含以下格式的条目 -
`<username>:<start of id range>:<id range size>`。例如，要允许当前用户使用 100 000 到 165 535 之间的 ID：

```console
$ grep "$USER" /etc/subuid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subuid)
$ grep "$USER" /etc/subgid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subgid)
```

要验证配置是否正确创建，请检查其内容：

```console
$ echo $USER
exampleuser
$ cat /etc/subuid
exampleuser:100000:65536
$ cat /etc/subgid
exampleuser:100000:65536
```

在这种情况下，如果在 Docker Desktop 容器内对共享文件执行 `chown`，使其属于 UID 为 1000 的用户，那么在主机上它将显示为属于 UID 为 100999 的用户。这有一个不幸的副作用，即阻止在主机上轻松访问此类文件。解决此问题的方法是创建一个具有新 GID 的组并将我们的用户添加到其中，或者为与 Docker Desktop VM 共享的文件夹设置递归 ACL（参见 `setfacl(1)`）。

{{< /accordion >}}

### Docker Desktop 将 Linux 容器存储在哪里？

Docker Desktop 将 Linux 容器和镜像存储在 Linux 文件系统中的一个大型"磁盘镜像"文件中。这与 Linux 上的 Docker 不同，后者通常将容器和镜像存储在主机文件系统的 `/var/lib/docker` 目录中。

#### 磁盘镜像文件在哪里？

要定位磁盘镜像文件，从 Docker Desktop Dashboard 选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

**Advanced** 选项卡显示磁盘镜像的位置。它还显示磁盘镜像的最大大小和磁盘镜像实际消耗的空间。请注意，其他工具可能会按最大文件大小而不是实际文件大小显示空间使用情况。

##### 如果文件太大怎么办？

如果磁盘镜像文件太大，您可以：

- 将其移动到更大的驱动器
- 删除不必要的容器和镜像
- 减少文件的最大允许大小

##### 如何将文件移动到更大的驱动器？

要将磁盘镜像文件移动到其他位置：

1. 选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

2. 在 **Disk image location** 部分，选择 **Browse** 并为磁盘镜像选择新位置。

3. 选择 **Apply** 使更改生效。

不要直接在 Finder 中移动文件，因为这可能导致 Docker Desktop 无法追踪该文件。

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

根据磁盘镜像文件的格式，在主机上回收空间可能需要几分钟：

- 如果文件名为 `Docker.raw`：主机上的空间应在几秒钟内回收。
- 如果文件名为 `Docker.qcow2`：空间将在几分钟后由后台进程释放。

只有在删除镜像时才会释放空间。在运行中的容器内删除文件时不会自动释放空间。要在任何时候触发空间回收，运行以下命令：

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

请注意，许多工具报告的是最大文件大小，而不是实际文件大小。
要从终端查询主机上文件的实际大小，运行：

```console
$ cd ~/.docker/desktop/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

在此示例中，磁盘的实际大小是 `2333548` KB，而磁盘的最大大小是 `64` GB。

##### 如何减少文件的最大大小？

要减少磁盘镜像文件的最大大小：

1. 从 Docker Desktop Dashboard 选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

2. **Disk image size** 部分包含一个滑块，允许您更改磁盘镜像的最大大小。调整滑块以设置较低的限制。

3. 选择 **Apply**。

当您减少最大大小时，当前磁盘镜像文件将被删除，因此所有容器和镜像都将丢失。
