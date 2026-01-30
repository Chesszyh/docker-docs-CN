---
description: 了解如何优化 AUFS 驱动程序的使用。
keywords: 'container, storage, driver, AUFS, 容器, 存储, 驱动程序'
title: AUFS 存储驱动程序
sitemap: false
---

> **已弃用**
>
> AuFS 存储驱动程序已弃用，并已在 Docker Engine v24.0 中移除。如果您正在使用 AuFS，必须在升级到 Docker Engine v24.0 之前迁移到受支持的存储驱动程序。请阅读 [Docker 存储驱动程序](select-storage-driver.md) 页面以了解受支持的存储驱动程序。

AUFS 是一个 *联合文件系统 (union filesystem)*。`aufs` 存储驱动程序以前是用于在 Ubuntu 以及 Stretch 之前的 Debian 版本上管理 Docker 镜像和层的默认存储驱动程序。如果您的 Linux 内核版本为 4.0 或更高，并且您使用 Docker Engine - Community，请考虑使用较新的 [overlay2](overlayfs-driver.md)，它比 `aufs` 存储驱动程序具有潜在的性能优势。

## 前提条件

- 对于 Docker Engine - Community，AUFS 支持 Ubuntu 以及 Stretch 之前的 Debian 版本。
- 如果您使用 Ubuntu，需要将 AUFS 模块添加到内核中。如果您不安装这些软件包，则需要使用 `overlay2`。
- AUFS 不能使用以下底层文件系统：`aufs`、`btrfs` 或 `ecryptfs`。这意味着包含 `/var/lib/docker/aufs` 的文件系统不能是这些文件系统类型之一。

## 为 Docker 配置 `aufs` 存储驱动程序

如果启动 Docker 时 AUFS 驱动程序已加载到内核中，且没有配置其他存储驱动程序，则 Docker 默认使用它。

1.  使用以下命令验证您的内核是否支持 AUFS。

    ```console
    $ grep aufs /proc/filesystems

    nodev   aufs
    ```

2.  检查 Docker 正在使用哪个存储驱动程序。

    ```console
    $ docker info

    <truncated output>
    Storage Driver: aufs
     Root Dir: /var/lib/docker/aufs
     Backing Filesystem: extfs
     Dirs: 0
     Dirperm1 Supported: true
    <truncated output>
    ```

3.  如果您使用的是其他存储驱动程序，要么是内核中不包含 AUFS (在这种情况下会使用其他默认驱动程序)，要么是 Docker 已显式配置为使用其他驱动程序。检查 `/etc/docker/daemon.json` 或 `ps auxw | grep dockerd` 的输出，查看 Docker 启动时是否带有了 `--storage-driver` 标志。

## `aufs` 存储驱动程序的工作原理

AUFS 是一个 *联合文件系统*，这意味着它在单个 Linux 主机上将多个目录分层，并将它们呈现为单个目录。这些目录在 AUFS 术语中称为 *分支 (branches)*，在 Docker 术语中称为 *层 (layers)*。

统一过程被称为 *联合挂载 (union mount)*。

下图显示了一个基于 `ubuntu:latest` 镜像的 Docker 容器。

![Ubuntu 容器层](images/aufs_layers.webp) 

每个镜像层以及容器层在 Docker 主机上都表示为 `/var/lib/docker/` 内的子目录。联合挂载提供了所有层的统一视图。目录名称并不直接对应于层本身的 ID。

AUFS 使用写时复制 (Copy-on-Write, CoW) 策略来最大限度地提高存储效率并最小化开销。

### 示例：磁盘上的镜像和容器结构

以下 `docker pull` 命令显示了 Docker 主机下载一个包含五层的 Docker 镜像。

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
b6f892c0043b: Pull complete
55010f332b04: Pull complete
2955fb827c94: Pull complete
3deef3fcbd30: Pull complete
cf9722e506aa: Pull complete
Digest: sha256:382452f82a8bbd34443b2c727650af46aced0f94a44463c62a9848133ecb1aa8
Status: Downloaded newer image for ubuntu:latest
```

#### 镜像层

> [!WARNING]: 不要直接操作 `/var/lib/docker/` 内的任何文件或目录。这些文件和目录由 Docker 管理。

关于镜像层和容器层的所有信息都存储在 `/var/lib/docker/aufs/` 的子目录中。

- `diff/`: 每个层的 **内容**，分别存储在独立的子目录中。
- `layers/`: 关于镜像层如何堆叠的元数据。此目录为 Docker 主机上的每个镜像或容器层包含一个文件。每个文件包含栈中其下方所有层的 ID (即其父层)。
- `mnt/`: 挂载点，每个镜像或容器层一个，用于组装和挂载容器的统一文件系统。对于只读的镜像，这些目录始终为空。

#### 容器层

如果容器正在运行，`/var/lib/docker/aufs/` 的内容会发生以下变化：

- `diff/`: 在可写容器层中引入的差异，例如新文件或修改过的文件。
- `layers/`: 关于可写容器层父层的元数据。
- `mnt/`: 每个运行中容器的统一文件系统的挂载点，与从容器内部看到的完全一致。

## `aufs` 下容器的读写工作原理

### 读取文件

考虑在使用 aufs 的容器打开文件进行读取访问的三种场景。

- **文件不存在于容器层中**: 如果容器打开一个文件进行读取访问，而该文件尚未存在于容器层中，存储驱动程序将在镜像层中搜索该文件，从紧挨着容器层下方的层开始。它将从找到该文件的层读取。

- **文件仅存在于容器层中**: 如果容器打开一个文件进行读取访问，且该文件存在于容器层中，则从那里读取。

- **文件同时存在于容器层和镜像层中**: 如果容器打开一个文件进行读取访问，且该文件同时存在于容器层和一个或多个镜像层中，则从容器层读取。容器层中的文件会遮蔽镜像层中具有相同名称的文件。

### 修改文件或目录

考虑容器中文件被修改的一些场景。

- **第一次写入文件**: 容器第一次写入现有文件时，该文件不存在于容器 (`upperdir`) 中。`aufs` 驱动程序执行 *copy_up* 操作，将文件从其存在的镜像层复制到可写容器层。然后，容器将更改写入容器层中该文件的新副本。

  但是，AUFS 工作在文件级别而不是块级别。这意味着所有的 copy_up 操作都会复制整个文件，即使文件非常大且仅修改了其中的一小部分。这会对容器的写入性能产生显著影响。在搜索具有许多层的镜像中的文件时，AUFS 可能会遇到明显的延迟。不过，值得注意的是，copy_up 操作仅在第一次写入给定文件时发生。随后对同一文件的写入将针对已复制到容器的文件副本进行操作。

- **删除文件和目录**:

  - 在容器内删除 *文件* 时，会在容器层中创建一个 *遮蔽 (whiteout)* 文件。镜像层中的文件版本不会被删除 (因为镜像层是只读的)。但是，遮蔽文件会阻止它对容器可用。

  - 在容器内删除 *目录* 时，会在容器层中创建一个 *不透明文件 (opaque file)*。这与遮蔽文件的工作方式相同，可以有效地防止目录被访问，即使它仍然存在于镜像层中。

- **重命名目录**: AUFS 并不完全支持对目录调用 `rename(2)`。它会返回 `EXDEV` (“不允许跨设备链接”)，即使源路径和目标路径都在同一个 AUFS 层上，除非该目录没有子项。您的应用程序需要设计为能够处理 `EXDEV` 并回退到“复制并取消链接 (copy and unlink)”策略。

## AUFS 与 Docker 性能

总结一下已经提到的一些与性能相关的方面：

- AUFS 存储驱动程序的性能低于 `overlay2` 驱动程序，但对于 PaaS 和其他类似容器密度很重要的用例来说是一个不错的选择。这是因为 AUFS 能在多个运行中的容器之间高效共享镜像，从而实现快速的容器启动时间和最小的磁盘空间占用。

- AUFS 在镜像层和容器之间共享文件的底层机制非常高效地利用了页面缓存 (page cache)。

- AUFS 存储驱动程序可能会给容器写入性能带来显著延迟。这是因为容器第一次写入任何文件时，需要定位该文件并将其复制到容器顶层的可写层。当这些文件存在于许多镜像层之下且文件本身很大时，这些延迟会增加并复合。

### 性能最佳实践

以下通用的性能最佳实践也适用于 AUFS。

- **固态硬盘 (SSD)** 比机械硬盘提供更快的读写速度。

- **对于写密集型工作负载使用卷**: 卷为写密集型工作负载提供最佳且最可预测的性能。这是因为它们绕过了存储驱动程序，不会产生由精简置备和写时复制引入的任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并且即使没有运行中的容器使用它们也会持久存在。

## 相关信息

- [卷 (Volumes)](../volumes.md)
- [了解镜像、容器和存储驱动程序](index.md)
- [选择存储驱动程序](select-storage-driver.md)
