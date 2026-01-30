---
description: 了解如何优化 ZFS 驱动程序的使用。
keywords: 'container, storage, driver, ZFS, 容器, 存储, 驱动程序'
title: ZFS 存储驱动程序
aliases:
  - /storage/storagedriver/zfs-driver/
---

ZFS 是一种下一代文件系统，支持许多先进的存储技术，如卷管理、快照、校验和、压缩和去重、复制等。

它由 Sun Microsystems (现为甲骨文公司) 创建，并在 CDDL 许可证下开源。由于 CDDL 和 GPL 之间的许可证不兼容，ZFS 不能作为 Linux 主线内核的一部分发布。但是，ZFS On Linux (ZoL) 项目提供了一个树外 (out-of-tree) 内核模块和用户空间工具，可以单独安装。

ZFS on Linux (ZoL) 移植版本目前状态良好且日趋成熟。然而，除非您在 Linux 上拥有丰富的 ZFS 使用经验，否则目前不建议在生产环境中使用 `zfs` Docker 存储驱动程序。

> [!NOTE]
>
> Linux 平台上也有 ZFS 的 FUSE 实现。这不被推荐。原生 ZFS 驱动程序 (ZoL) 经过了更多测试，性能更好，且使用更广泛。本文档的其余部分均指原生 ZoL 移植版本。

## 前提条件

- ZFS 需要一个或多个专用块设备，最好是固态硬盘 (SSD)。
- `/var/lib/docker/` 目录必须挂载在 ZFS 格式的文件系统上。
- 更改存储 driver 会使您已创建的任何容器在本地系统上无法访问。请使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样您以后就无需重新创建它们。

> [!NOTE]
>
> 不需要使用 `MountFlags=slave`，因为 `dockerd` 和 `containerd` 位于不同的挂载命名空间 (mount namespaces) 中。

## 为 Docker 配置 `zfs` 存储驱动程序

1.  停止 Docker。

2.  将 `/var/lib/docker/` 的内容复制到 `/var/lib/docker.bk` 并清空 `/var/lib/docker/` 的内容。

    ```console
    $ sudo cp -au /var/lib/docker /var/lib/docker.bk

    $ sudo rm -rf /var/lib/docker/*
    ```

3.  在您的专用块设备上创建一个新的 `zpool`，并将其挂载到 `/var/lib/docker/`。请务必指定正确的设备，因为这是一个破坏性操作。本示例向池中添加了两个设备。

    ```console
    $ sudo zpool create -f zpool-docker -m /var/lib/docker /dev/xvdf /dev/xvdg
    ```

    该命令创建名为 `zpool-docker` 的 `zpool`。该名称仅用于显示目的，您可以使用其他名称。使用 `zfs list` 检查池是否已正确创建并挂载。

    ```console
    $ sudo zfs list

    NAME           USED  AVAIL  REFER  MOUNTPOINT
    zpool-docker    55K  96.4G    19K  /var/lib/docker
    ```

4.  配置 Docker 使用 `zfs`。编辑 `/etc/docker/daemon.json` 并将 `storage-driver` 设置为 `zfs`。如果文件之前为空，现在应如下所示：

    ```json
    {
      "storage-driver": "zfs"
    }
    ```

    保存并关闭文件。

5.  启动 Docker。使用 `docker info` 验证存储驱动程序是否为 `zfs`。

    ```console
    $ sudo docker info
      Containers: 0
       Running: 0
       Paused: 0
       Stopped: 0
      Images: 0
      Server Version: 17.03.1-ce
      Storage Driver: zfs
       Zpool: zpool-docker
       Zpool Health: ONLINE
       Parent Dataset: zpool-docker
       Space Used By Parent: 249856
       Space Available: 103498395648
       Parent Quota: no
       Compression: off
    <...>
    ```

## 管理 `zfs`

### 增加运行中设备的容量

要增加 `zpool` 的大小，您需要向 Docker 主机添加一个专用的块设备，然后使用 `zpool add` 命令将其添加到 `zpool` 中：

```console
$ sudo zpool add zpool-docker /dev/xvdh
```

### 限制容器的可写存储配额

如果您想针对每个镜像/数据集实现配额，可以设置 `size` 存储选项，以限制单个容器可用于其可写层的空间量。

编辑 `/etc/docker/daemon.json` 并添加以下内容：

```json
{
  "storage-driver": "zfs",
  "storage-opts": ["size=256M"]
}
```

在 [守护进程参考文档](/reference/cli/dockerd/#daemon-storage-driver) 中查看每个存储驱动程序的所有存储选项。

保存并关闭文件，然后重启 Docker。

## `zfs` 存储驱动程序的工作原理

ZFS 使用以下对象：

- **文件系统 (filesystems)**: 精简置备，根据需要从 `zpool` 分配空间。
- **快照 (snapshots)**: 文件系统在特定时间点的只读且节省空间的副本。
- **克隆 (clones)**: 快照的读写副本。用于存储与前一层的差异。

创建克隆的过程：

![ZFS 快照和克隆](images/zfs_clones.webp?w=450)


1.  从文件系统创建一个只读快照。
2.  从该快照创建一个可写克隆。这包含了与父层的任何差异。

文件系统、快照和克隆都从底层的 `zpool` 分配空间。

### 磁盘上的镜像和容器层

每个运行中容器的统一文件系统都挂载在 `/var/lib/docker/zfs/graph/` 中的一个挂载点上。继续阅读以了解统一文件系统的构成。

### 镜像分层与共享

镜像的基础层是一个 ZFS 文件系统。每个子层都是基于其下方一层的 ZFS 快照创建的 ZFS 克隆。容器是基于其所创建镜像顶层的 ZFS 快照创建的 ZFS 克隆。

下图显示了如何将这些部分组合在一起，其中包含一个基于两层镜像的运行中容器。

![适用于 Docker 容器的 ZFS 池](images/zfs_zpool.webp?w=600)

启动容器时，按顺序发生以下步骤：

1.  镜像的基础层作为 ZFS 文件系统存在于 Docker 主机上。

2.  其他的镜像层是其直接下方镜像层所在数据集的克隆。

    在图中，通过对基础层进行 ZFS 快照，然后从该快照创建克隆来添加“Layer 1”。克隆是可写的，并根据需要从 zpool 消耗空间。快照是只读的，使基础层保持为不可变对象。

3.  启动容器时，会在镜像上方添加一个可写层。

    在图中，通过对镜像顶层 (Layer 1) 进行快照并从该快照创建克隆来创建容器的读写层。

4.  随着容器修改其可写层的内容，系统会为更改的块分配空间。默认情况下，这些块的大小为 128k。


## `zfs` 下容器的读写工作原理

### 读取文件

每个容器的可写层都是一个 ZFS 克隆，它与创建它的数据集 (其父层的快照) 共享所有数据。读取操作很快，即使读取的数据来自深层。下图说明了块共享的工作原理：

![ZFS 块共享](images/zpool_blocks.webp?w=450)


### 写入文件

**写入新文件**: 根据需要从底层的 `zpool` 分配空间，并将块直接写入容器的可写层。

**修改现有文件**: 仅为更改的块分配空间，并使用写时复制 (CoW) 策略将这些块写入容器的可写层。这使层的大小最小化并提高了写入性能。

**删除文件或目录**:
  - 当您删除存在于较低层的文件或目录时，ZFS 驱动程序会在容器的可写层中遮蔽该文件或目录的存在，即使该文件或目录仍然存在于较低的只读层中。
  - 如果您在容器的可写层内创建然后删除一个文件或目录，块将被 `zpool` 回收。


## ZFS 与 Docker 性能

有几个因素会影响使用 `zfs` 存储驱动程序的 Docker 性能。

- **内存**: 内存对 ZFS 性能有重大影响。ZFS 最初是为具有大量内存的大型企业级服务器设计的。

- **ZFS 特性**: ZFS 包含去重功能。使用此功能可以节省磁盘空间，但会消耗大量内存。建议为您在 Docker 中使用的 `zpool` 禁用此功能，除非您使用的是 SAN、NAS 或其他硬件 RAID 技术。

- **ZFS 缓存**: ZFS 在名为适应性替换缓存 (ARC) 的内存结构中缓存磁盘块。ZFS 的 *Single Copy ARC* 特性允许单个缓存的块副本由多个克隆共享。通过此特性，多个运行中的容器可以共享单个缓存块副本。这使得 ZFS 成为 PaaS 和其他高密度用例的一个很好的选择。

- **碎片化 (Fragmentation)**: 碎片化是像 ZFS 这样的写时复制文件系统的自然副产品。ZFS 通过使用 128k 的小块大小来缓解这一问题。ZFS 意图日志 (ZIL) 和写入合并 (延迟写入) 也有助于减少碎片化。您可以使用 `zpool status` 监控碎片化情况。然而，除了重新格式化和恢复文件系统之外，没有办法对 ZFS 进行碎片整理。

- **使用适用于 Linux 的原生 ZFS 驱动程序**: 由于性能较差，不推荐使用 ZFS FUSE 实现。

### 性能最佳实践

- **使用快速存储**: 固态硬盘 (SSD) 比机械硬盘提供更快的读写速度。

- **对于写密集型工作负载使用卷**: 卷为写密集型工作负载提供最佳且最可预测的性能。这是因为它们绕过了存储驱动程序，不会产生由精简置备和写时复制引入的任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并且即使没有运行中的容器使用它们也会持久存在。
