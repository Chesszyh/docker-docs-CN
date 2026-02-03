---
description: Linux 版 Docker Desktop 的常见问题
keywords: desktop, linux, faqs, 常见问题
title: Linux 版 Docker Desktop 常见问题 (FAQ)
linkTitle: Linux
tags: [FAQ]
aliases:
- /desktop/linux/space/
- /desktop/faqs/linuxfaqs/
weight: 40
---

### 为什么 Linux 版 Docker Desktop 需要运行虚拟机 (VM)？

Linux 版 Docker Desktop 运行虚拟机的原因如下：

1. **确保跨平台的一致体验**：
    在调研过程中，用户希望推出 Linux 版 Docker Desktop 最常提到的原因是确保在所有主流操作系统上拥有功能对等且一致的 Docker Desktop 体验。利用虚拟机可以确保 Linux 用户的 Docker Desktop 体验与 Windows 和 macOS 紧密匹配。

2. **利用新的内核特性**：
    有时我们需要利用新的操作系统特性。由于我们可以控制虚拟机内部的内核和操作系统，因此我们可以立即向所有用户推送这些特性，即使是那些有意停留在宿主机操作系统 LTS 版本的用户。

3. **增强安全性**：
    容器镜像漏洞会对宿主机环境构成安全风险。市面上存在大量未经可信验证已知漏洞的非官方镜像。恶意用户可能会向公共注册表推送镜像，并使用各种手段诱导用户拉取并运行它们。虚拟机方案缓解了这种威胁，因为任何获得 root 权限的恶意软件都将被限制在虚拟机环境中，无法访问宿主机。

    为什么不运行 rootless Docker？虽然 rootless Docker 在表面上有通过限制 root 用户访问来使 `top` 命令看起来更安全的优点，但它允许非特权用户在其自己的用户命名空间中获得 `CAP_SYS_ADMIN` 权限，并访问那些本不该由非特权用户使用的内核 API，从而导致 [漏洞](https://www.openwall.com/lists/oss-security/2022/01/18/7)。

4. **在性能影响最小的情况下提供功能对等和增强的安全性**：
    Linux 版 Docker Desktop 使用的虚拟机采用 [`VirtioFS`](https://virtio-fs.gitlab.io)，这是一种共享文件系统，允许虚拟机访问位于宿主机上的目录树。我们的内部基准测试显示，通过为虚拟机分配适当的资源，使用 VirtioFS 可以实现接近原生的文件系统性能。

    因此，我们调整了 Linux 版 Docker Desktop 中虚拟机的默认可用内存。您可以通过 Docker Desktop 的 **Settings** > **Resources** 选项卡中的 **Memory** 滑块，根据您的具体需求调整此设置。

### 如何启用文件共享？

Linux 版 Docker Desktop 使用 [VirtioFS](https://virtio-fs.gitlab.io/) 作为默认（且目前唯一）的机制，用于在宿主机和 Docker Desktop 虚拟机之间实现文件共享。

{{< accordion title="Docker Desktop 4.34 及更早版本的附加信息" >}}

为了在不需要提升权限的同时不对共享文件的操作进行不必要的限制，Docker Desktop 在配置了 UID 和 GID 映射的用户命名空间（参见 `user_namespaces(7)`）内运行文件共享服务 (`virtiofsd`)。因此，Docker Desktop 依赖于宿主机配置，以使当前用户能够使用从属 ID 委托（subordinate ID delegation）。为此，必须存在 `/etc/subuid`（参见 `subuid(5)`）和 `/etc/subgid`（参见 `subgid(5)`）文件。Docker Desktop 仅支持通过文件配置的从属 ID 委托。Docker Desktop 将容器中的当前用户 ID 和 GID 映射为 0。它使用 `/etc/subuid` 和 `/etc/subgid` 中对应于当前用户的第一个条目，为容器中大于 0 的 ID 设置映射。

| 容器中的 ID | 宿主机上的 ID |
| --------------- | -------------------------------------------------------------------------------- |
| 0 (root)        | 运行 Docker Desktop 的用户 ID（例如 1000） |
| 1               | 0 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围起始值（例如 100000） |
| 2               | 1 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围起始值（例如 100001） |
| 3               | 2 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围起始值（例如 100002） |
| ...             | ... |

如果缺少 `/etc/subuid` 和 `/etc/subgid`，则需要创建它们。两个文件都应包含格式为 `<用户名>:<ID 范围起始值>:<ID 范围大小>` 的条目。例如，允许当前用户使用从 100,000 到 165,535 的 ID：

```console
$ grep "$USER" /etc/subuid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subuid)
$ grep "$USER" /etc/subgid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subgid)
```

要验证配置是否已正确创建，请检查其内容：

```console
$ echo $USER
exampleuser
$ cat /etc/subuid
exampleuser:100000:65536
$ cat /etc/subgid
exampleuser:100000:65536
```

在这种场景下，如果在一个 UID 为 1000 的用户所拥有的 Docker Desktop 容器内对一个共享文件执行 `chown` 操作，在宿主机上该文件将显示为 UID 为 100999 的用户所有。这产生了一个负面副作用，即无法在宿主机上轻松访问此类文件。该问题可以通过创建一个具有新 GID 的组并将当前用户添加进去，或者通过为与 Docker Desktop 虚拟机共享的文件夹设置递归 ACL（参见 `setfacl(1)`）来解决。

{{< /accordion >}}

### Docker Desktop 将 Linux 容器存储在哪里？

Linux 版 Docker Desktop 将 Linux 容器和镜像存储在 Linux 文件系统中的单个大型“磁盘镜像”文件中。这与 Linux 上的原生 Docker 不同，后者通常将容器和镜像存储在宿主机文件系统的 `/var/lib/docker` 目录中。

#### 磁盘镜像文件在哪里？

要找到磁盘镜像文件，请在 Docker Desktop 控制面板中选择 **Settings**，然后选择 **Resources** 选项卡下的 **Advanced**。

**Advanced** 选项卡会显示磁盘镜像的位置。它还会显示磁盘镜像的最大容量以及其实际占用的空间。请注意，其他工具可能会以最大文件大小而非实际文件大小来显示该文件的空间占用情况。

##### 如果文件太大怎么办？

如果磁盘镜像文件太大，您可以：

- 将其移动到更大的驱动器
- 删除不需要的容器和镜像
- 减小文件的最大允许容量

##### 如何将文件移动到更大的驱动器？

要将磁盘镜像文件移动到其他位置：

1. 在 **Resources** 选项卡下选择 **Settings** -> **Advanced**。

2. 在 **Disk image location** 部分，选择 **Browse** 并为磁盘镜像选择一个新位置。

3. 选择 **Apply** 使更改生效。

不要直接在文件管理器中移动该文件，否则会导致 Docker Desktop 无法追踪到该文件。

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

此命令将移除所有已停止的容器、未使用的网络、悬空（dangling）镜像以及构建缓存。

根据磁盘镜像文件的格式，宿主机可能需要几分钟才能回收空间：

- 如果文件名为 `Docker.raw`：宿主机上的空间应在几秒钟内回收。
- 如果文件名为 `Docker.qcow2`：空间将在几分钟后由后台进程释放。

空间仅在删除镜像时释放。在运行中的容器内删除文件不会自动释放空间。要随时触发空间回收，请运行以下命令：

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

请注意，许多工具报告的是最大文件大小，而非实际文件大小。要通过终端查询宿主机上文件的实际大小，请运行：

```console
$ cd ~/.docker/desktop/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

在此示例中，磁盘的实际大小为 `2333548` KB，而磁盘的最大容量为 `64` GB。

##### 如何减小文件的最大容量？

要减小磁盘镜像文件的最大容量：

1. 在 Docker Desktop 控制面板中选择 **Resources** 选项卡下的 **Settings** -> **Advanced**。

2. **Disk image size** 部分包含一个滑块，允许您更改磁盘镜像的最大容量。调节滑块设置一个较低的限制。

3. 选择 **Apply**。

当您减小最大容量时，当前的磁盘镜像文件将被删除，因此所有的容器和镜像都将丢失。
