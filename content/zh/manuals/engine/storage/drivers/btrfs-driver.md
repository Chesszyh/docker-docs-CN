---
description: 了解如何优化 Btrfs 驱动程序的使用。
keywords: container, storage, driver, Btrfs, 容器, 存储, 驱动程序
title: BTRFS 存储驱动程序
---

> [!IMPORTANT]
>
> 在大多数情况下，您应该使用 `overlay2` 存储驱动程序 —— 仅仅因为您的系统使用 Btrfs 作为其根文件系统，并不意味着必须使用 `btrfs` 存储驱动程序。
>
> Btrfs 驱动程序存在已知问题。有关更多信息，请参阅 [Moby 问题 #27653](https://github.com/moby/moby/issues/27653)。

Btrfs 是一个支持许多高级存储技术的写时复制 (copy-on-write) 文件系统，非常适合 Docker。Btrfs 已包含在主流 Linux 内核中。

Docker 的 `btrfs` 存储驱动程序利用了 Btrfs 的许多功能来进行镜像和容器管理。这些功能包括块级操作、精简置备 (thin provisioning)、写时复制快照以及易于管理。您可以将多个物理块设备组合成一个 Btrfs 文件系统。

本页将 Docker 的 Btrfs 存储驱动程序简称为 `btrfs`，将整体的 Btrfs 文件系统简称为 Btrfs。

> [!NOTE]
>
> `btrfs` 存储驱动程序仅在 SLES、Ubuntu 和 Debian 系统上的 Docker Engine CE 中受支持。

## 前提条件

如果您满足以下前提条件，则支持 `btrfs`：

- `btrfs` 仅建议在 Ubuntu 或 Debian 系统上与 Docker CE 配合使用。

- 更改存储驱动程序会使您已创建的任何容器在本地系统上无法访问。请使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样以后就无需重新创建它们。

- `btrfs` 需要一个专用的块存储设备，例如物理磁盘。此块设备必须格式化为 Btrfs 格式并挂载到 `/var/lib/docker/` 中。下面的配置说明将引导您完成此过程。默认情况下，SLES 的 `/` 文件系统格式化为 Btrfs，因此对于 SLES，您不需要使用单独的块设备，但出于性能原因，您可以选择这样做。

- 内核中必须存在 `btrfs` 支持。要检查这一点，运行以下命令：

  ```console
  $ grep btrfs /proc/filesystems

  btrfs
  ```

- 要在操作系统级别管理 Btrfs 文件系统，您需要 `btrfs` 命令。如果您没有此命令，请安装 `btrfsprogs` 软件包 (SLES) 或 `btrfs-tools` 软件包 (Ubuntu)。

## 为 Docker 配置 btrfs 存储驱动程序

此过程在 SLES 和 Ubuntu 上基本相同。

1. 停止 Docker。

2. 将 `/var/lib/docker/` 的内容复制到备份位置，然后清空 `/var/lib/docker/` 的内容：

   ```console
   $ sudo cp -au /var/lib/docker /var/lib/docker.bk
   $ sudo rm -rf /var/lib/docker/*
   ```

3. 将您的专用块设备格式化为 Btrfs 文件系统。本示例假设您使用的是两个名为 `/dev/xvdf` 和 `/dev/xvdg` 的块设备。请仔细检查块设备名称，因为这是一个破坏性操作。

   ```console
   $ sudo mkfs.btrfs -f /dev/xvdf /dev/xvdg
   ```

   Btrfs 还有更多选项，包括条带化和 RAID。请参阅 [Btrfs 文档](https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices)。

4. 将新的 Btrfs 文件系统挂载到 `/var/lib/docker/` 挂载点。您可以指定用于创建 Btrfs 文件系统的任何块设备。

   ```console
   $ sudo mount -t btrfs /dev/xvdf /var/lib/docker
   ```

   > [!NOTE]
   >
   > 通过在 `/etc/fstab` 中添加一个条目，使此更改在重启后依然有效。

5. 将 `/var/lib/docker.bk` 的内容复制到 `/var/lib/docker/`。

   ```console
   $ sudo cp -au /var/lib/docker.bk/* /var/lib/docker/
   ```

6. 配置 Docker 以使用 `btrfs` 存储驱动程序。即使 `/var/lib/docker/` 现在正在使用 Btrfs 文件系统，这也是必需的。
   编辑或创建 `/etc/docker/daemon.json` 文件。如果是新文件，请添加以下内容。如果是现有文件，请仅添加键和值，并注意如果该行不是结束大括号 (`}`) 之前的最后一行，请以逗号结尾。

   ```json
   {
     "storage-driver": "btrfs"
   }
   ```

   在 [守护进程参考文档](/reference/cli/dockerd/#options-per-storage-driver) 中查看每个存储驱动程序的所有存储选项。

7. 启动 Docker。运行后，验证 `btrfs` 是否被用作存储驱动程序。

   ```console
   $ docker info

   Containers: 0
    Running: 0
    Paused: 0
    Stopped: 0
   Images: 0
   Server Version: 17.03.1-ce
   Storage Driver: btrfs
    Build Version: Btrfs v4.4
    Library Version: 101
   <...>
   ```

8. 准备就绪后，删除 `/var/lib/docker.bk` 目录。

## 管理 Btrfs 卷

Btrfs 的优势之一是易于管理，无需卸载文件系统或重启 Docker 即可管理 Btrfs 文件系统。

当空间不足时，Btrfs 会以大约 1 GB 的块自动扩展卷。

要向 Btrfs 卷添加块设备，请使用 `btrfs device add` 和 `btrfs filesystem balance` 命令。

```console
$ sudo btrfs device add /dev/svdh /var/lib/docker

$ sudo btrfs filesystem balance /var/lib/docker
```

> [!NOTE]
>
> 虽然您可以在 Docker 运行时执行这些操作，但性能会受到影响。最好计划一个停机窗口来平衡 Btrfs 文件系统。

## `btrfs` 存储驱动程序的工作原理

`btrfs` 存储驱动程序与其他存储驱动程序的不同之处在于，您的整个 `/var/lib/docker/` 目录都存储在一个 Btrfs 卷上。

### 磁盘上的镜像和容器层

关于镜像层和可写容器层的信息存储在 `/var/lib/docker/btrfs/subvolumes/` 中。此子目录为每个镜像或容器层包含一个目录，其统一文件系统由该层及其所有父层构建而成。子卷 (Subvolumes) 原生支持写时复制，并根据需要从底层的存储池中分配空间。它们也可以被嵌套和创建快照。下图显示了 4 个子卷。“Subvolume 2”和“Subvolume 3”是嵌套的，而“Subvolume 4”显示了其内部目录树。

![子卷示例](images/btfs_subvolume.webp?w=350&h=100)

只有镜像的基础层存储为真正的子卷。所有其他层都存储为快照，这些快照仅包含该层中引入的差异。您可以像下图所示创建快照的快照。

![快照图示](images/btfs_snapshots.webp?w=350&h=100)

在磁盘上，快照的外观和感觉与子卷完全一样，但实际上它们要小得多，空间利用率更高。使用写时复制来最大限度地提高存储效率并最小化层的大小，容器可写层中的写入是在块级管理的。下图显示了一个子卷及其快照共享数据的情况。

![快照和子卷共享数据](images/btfs_pool.webp?w=450&h=200)

为了最大限度地提高效率，当容器需要更多空间时，会以大约 1 GB 大小的块进行分配。

Docker 的 `btrfs` 存储驱动程序将每个镜像层和容器存储在各自的 Btrfs 子卷或快照中。镜像的基础层存储为子卷，而子镜像层和容器则存储为快照。如下图所示。

![Btrfs 容器层](images/btfs_container_layer.webp?w=600)

在运行 `btrfs` 驱动程序的 Docker 主机上创建镜像和容器的高级过程如下：

1. 镜像的基础层存储在 `/var/lib/docker/btrfs/subvolumes` 下的一个 Btrfs *子卷 (subvolume)* 中。

2. 后续镜像层存储为父层子卷或快照的一个 Btrfs *快照 (snapshot)*，但带有该层引入的更改。这些差异存储在块级。

3. 容器的可写层是最终镜像层的一个 Btrfs 快照，带有运行中的容器引入的更改。这些差异同样存储在块级。

## `btrfs` 下容器的读写工作原理

### 读取文件

容器是一个镜像的高效快照。快照中的元数据指向存储池中实际的数据块。这与子卷的情况相同。因此，针对快照执行的读取操作与针对子卷执行的读取操作在本质上是相同的。

### 写入文件

作为一个通用的警告，在 Btrfs 中写入和更新大量小文件可能会导致性能下降。

考虑容器在使用 Btrfs 打开文件进行写入访问时的三种场景。

#### 写入新文件

向容器写入新文件会触发按需分配操作，以为容器的快照分配新的数据块。然后将文件写入这个新空间。按需分配操作是 Btrfs 中所有写入操作的原生操作，与向子卷写入新数据相同。因此，向容器快照写入新文件的操作以原生 Btrfs 速度运行。

#### 修改现有文件

在容器中更新现有文件是一个写时复制操作 (在 Btrfs 术语中称为重定向写入 redirect-on-write)。从文件当前所在的层读取原始数据，只有修改过的块会被写入容器的可写层。接下来，Btrfs 驱动程序更新快照中的文件系统元数据，使其指向这些新数据。此行为会产生较小的开销。

#### 删除文件或目录

如果容器删除了存在于较低层的文件或目录，Btrfs 会掩盖较低层中该文件或目录的存在。如果容器创建了一个文件然后又将其删除，则此操作将在 Btrfs 文件系统本身中执行，空间将被回收。

## Btrfs 与 Docker 性能

在使用 `btrfs` 存储驱动程序时，有几个因素会影响 Docker 的性能。

> [!NOTE]
>
> 通过为写密集型工作负载使用 Docker 卷，而不是依赖在容器的可写层中存储数据，可以减轻许多这些因素的影响。但是，对于 Btrfs 而言，除非 `/var/lib/docker/volumes/` 下的文件系统不是由 Btrfs 支撑的，否则 Docker 卷仍然会受到这些缺陷的影响。

### 页面缓存 (Page caching)

Btrfs 不支持页面缓存共享。这意味着访问同一个文件的每个进程都会将该文件复制到 Docker 主机的内存中。因此，`btrfs` 驱动程序可能不是高密度用例 (如 PaaS) 的最佳选择。

### 小额写入 (Small writes)

执行大量小额写入的容器 (这种使用模式也与在短时间内启动和停止许多容器的情况相匹配) 可能会导致对 Btrfs 块 (chunks) 的利用率不高。这可能会过早地填满 Btrfs 文件系统，并导致 Docker 主机出现空间不足的情况。使用 `btrfs filesys show` 密切监控 Btrfs 设备上的可用空间量。

### 顺序写入 (Sequential writes)

Btrfs 在向磁盘写入时使用日志技术。这可能会影响顺序写入的性能，性能最高可能降低 50%。

### 碎片化 (Fragmentation)

碎片化是写时复制文件系统 (如 Btrfs) 的自然副产品。许多随机的小额写入会加剧这个问题。使用 SSD 时碎片化可能表现为 CPU 峰值，而在使用机械硬盘时则表现为磁头频繁寻道。这些问题都会损害性能。

如果您的 Linux 内核版本为 3.9 或更高，可以在挂载 Btrfs 卷时启用 `autodefrag` 功能。在投入生产之前，请针对您自己的工作负载测试此功能，因为某些测试显示它对性能有负面影响。

### SSD 性能

Btrfs 包含对 SSD 介质的原生优化。要启用这些功能，请使用 `-o ssd` 挂载选项挂载 Btrfs 文件系统。这些优化包括通过避免不适用于固态介质的寻道优化等方式来增强 SSD 的写入性能。

### 经常平衡 Btrfs 文件系统

使用操作系统实用程序 (如 `cron` 任务) 在非高峰时段定期平衡 Btrfs 文件系统。这会回收未分配的块，并有助于防止文件系统被不必要地填满。除非向文件系统添加额外的物理块设备，否则无法重新平衡完全填满的 Btrfs 文件系统。

参见 [Btrfs Wiki](https://btrfs.wiki.kernel.org/index.php/Balance_Filters#Balancing_to_fix_filesystem_full_errors)。

### 使用快速存储

固态硬盘 (SSD) 比机械硬盘提供更快的读写速度。

### 对于写密集型工作负载使用卷

对于写密集型工作负载，卷提供了最佳且最可预测的性能。这是因为它们绕过了存储驱动程序，不会产生由于精简置备和写时复制引入的任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并且即使没有运行中的容器使用它们也会持久存在。

## 相关信息

- [卷 (Volumes)](../volumes.md)
- [了解镜像、容器和存储驱动程序](index.md)
- [选择存储驱动程序](select-storage-driver.md)
