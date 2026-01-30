--- 
description: 了解如何优化 Device Mapper 驱动程序的使用。
keywords: container, storage, driver, device mapper, 容器, 存储, 驱动程序
title: Device Mapper 存储驱动程序 (已弃用)
alias:
  - /storage/storagedriver/device-mapper-driver/
---

> **已弃用**
> 
> Device Mapper 驱动程序 [/manuals/engine/deprecated.md#device-mapper-storage-driver](/manuals/engine/deprecated.md#device-mapper-storage-driver)，并已在 Docker Engine v25.0 中移除。如果您正在使用 Device Mapper，必须在升级到 Docker Engine v25.0 之前迁移到受支持的存储驱动程序。请阅读 [Docker 存储驱动程序](select-storage-driver.md) 页面以了解受支持的存储驱动程序。

Device Mapper 是一个基于内核的框架，支撑着 Linux 上许多先进的卷管理技术。Docker 的 `devicemapper` 存储驱动程序利用该框架的精简置备 (thin provisioning) 和快照功能进行镜像和容器管理。本文将 Device Mapper 存储驱动程序简称为 `devicemapper`，而将内核框架简称为 *Device Mapper*。

对于支持该驱动程序的系统，`devicemapper` 支持已包含在 Linux 内核中。但是，要在 Docker 中使用它，需要进行特定的配置。

`devicemapper` 驱动程序使用专用于 Docker 的块设备，并在块级 (而不是文件级) 运行。通过向 Docker 主机添加物理存储，可以扩展这些设备，且其性能优于在操作系统 (OS) 级别使用文件系统。

## 前提条件

- `devicemapper` 在运行于 CentOS、Fedora、SLES 15、Ubuntu、Debian 或 RHEL 的 Docker Engine - Community 上受支持。
- `devicemapper` 需要安装 `lvm2` 和 `device-mapper-persistent-data` 软件包。
- 更改存储驱动程序会使您已创建的任何容器在本地系统上无法访问。请使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样您以后就无需重新创建它们。

## 为 Docker 配置 `devicemapper` 存储驱动程序

在遵循这些步骤之前，必须首先满足所有 [前提条件](#prerequisites)。

### 为测试配置 `loop-lvm` 模式

此配置仅适用于测试。`loop-lvm` 模式利用“回环 (loopback)”机制，允许将本地磁盘上的文件像实际的物理磁盘或块设备一样进行读写。
然而，由于增加了回环机制以及与 OS 文件系统层的交互，IO 操作可能会很慢且耗费资源。使用回环设备还可能引入竞态条件。
不过，设置 `loop-lvm` 模式有助于在尝试启用 `direct-lvm` 模式所需的更复杂设置之前，识别基本问题 (如缺少用户空间软件包、内核驱动程序等)。因此，`loop-lvm` 模式仅应在配置 `direct-lvm` 之前用于执行初步测试。

对于生产系统，请参阅 [为生产配置 direct-lvm 模式](#configure-direct-lvm-mode-for-production)。

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2.  编辑 `/etc/docker/daemon.json`。如果该文件尚不存在，请创建它。假设该文件为空，添加以下内容：

    ```json
    {
      "storage-driver": "devicemapper"
    }
    ```

    在 [守护进程参考文档](/reference/cli/dockerd/#options-per-storage-driver) 中查看每个存储驱动程序的所有存储选项。

    如果 `daemon.json` 文件包含格式错误的 JSON，Docker 将无法启动。

3.  启动 Docker。

    ```console
    $ sudo systemctl start docker
    ```

4.  验证守护进程是否正在使用 `devicemapper` 存储驱动程序。使用 `docker info` 命令并查找 `Storage Driver`。

    ```console
    $ docker info

      Containers: 0
        Running: 0
        Paused: 0
        Stopped: 0
      Images: 0
      Server Version: 17.03.1-ce
      Storage Driver: devicemapper
      Pool Name: docker-20:1-8413957-pool
      Pool Blocksize: 65.54 kB
      Base Device Size: 10.74 GB
      Backing Filesystem: xfs
      Data file: /dev/loop0
      Metadata file: /dev/loop1
      Data Space Used: 11.8 MB
      Data Space Total: 107.4 GB
      Data Space Available: 7.44 GB
      Metadata Space Used: 581.6 kB
      Metadata Space Total: 2.147 GB
      Metadata Space Available: 2.147 GB
      Thin Pool Minimum Free Space: 10.74 GB
      Udev Sync Supported: true
      Deferred Removal Enabled: false
      Deferred Deletion Enabled: false
      Deferred Deleted Device Count: 0
      Data loop file: /var/lib/docker/devicemapper/data
      Metadata loop file: /var/lib/docker/devicemapper/metadata
      Library Version: 1.02.135-RHEL7 (2016-11-16)
    <...>
    ```

  此主机运行在 `loop-lvm` 模式下，生产系统 **不** 支持该模式。这由 `Data loop file` 和 `Metadata loop file` 位于 `/var/lib/docker/devicemapper` 下的文件这一事实表明。这些是回环挂载的稀疏文件。对于生产系统，请参阅 [为生产配置 direct-lvm 模式](#configure-direct-lvm-mode-for-production)。


### 为生产配置 direct-lvm 模式

使用 `devicemapper` 存储驱动程序的生产主机必须使用 `direct-lvm` 模式。此模式使用块设备创建精简池 (thin pool)。这比使用回环设备更快，系统资源利用更高效，并且块设备可以根据需要增长。但是，它比 `loop-lvm` 模式需要更多的设置。

在满足 [前提条件](#prerequisites) 后，按照以下步骤配置 Docker 在 `direct-lvm` 模式下使用 `devicemapper` 存储驱动程序。

> [!WARNING]
> 更改存储驱动程序会使您已创建的任何容器在本地系统上无法访问。请使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样您以后就无需重新创建它们。

#### 允许 Docker 配置 direct-lvm 模式

Docker 可以为您管理块设备，简化 `direct-lvm` 模式的配置。**这仅适用于全新的 Docker 设置。** 您只能使用单个块设备。如果您需要使用多个块设备，请改为 [手动配置 direct-lvm 模式](#configure-direct-lvm-mode-manually)。
以下是可用的新配置选项：

| 选项                            | 描述                                                                                                                                                                        | 是否必填 | 默认值 | 示例                               |
|:--------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------|:--------|:-----------------------------------|
| `dm.directlvm_device`           | 为 `direct-lvm` 配置的块设备的路径。                                                                                                                        | 是       |         | `dm.directlvm_device="/dev/xvdf"`  |
| `dm.thinp_percent`              | 从传入的块设备中用于存储的空间百分比。                                                                                                        | 否        | 95      | `dm.thinp_percent=95`              |
| `dm.thinp_metapercent`          | 从传入的块设备中用于元数据存储的空间百分比。                                                                                                   | 否        | 1       | `dm.thinp_metapercent=1`           |
| `dm.thinp_autoextend_threshold` | LVM 应自动扩展精简池的阈值，以总存储空间的百分比表示。                                                                                                  | 否        | 80      | `dm.thinp_autoextend_threshold=80` |
| `dm.thinp_autoextend_percent`   | 触发自动扩展时精简池增加的百分比。                                                                                                       | 否        | 20      | `dm.thinp_autoextend_percent=20`   |
| `dm.directlvm_device_force`     | 是否格式化块设备，即使其上已存在文件系统。如果设置为 `false` 且存在文件系统，则会记录错误并保持文件系统完整。 | 否        | false   | `dm.directlvm_device_force=true`   |

编辑 `daemon.json` 文件并设置适当的选项，然后重启 Docker 以使更改生效。以下 `daemon.json` 配置设置了上表中的所有选项：

```json
{
  "storage-driver": "devicemapper",
  "storage-opts": [
    "dm.directlvm_device=/dev/xdf",
    "dm.thinp_percent=95",
    "dm.thinp_metapercent=1",
    "dm.thinp_autoextend_threshold=80",
    "dm.thinp_autoextend_percent=20",
    "dm.directlvm_device_force=false"
  ]
}
```

在 [守护进程参考文档](/reference/cli/dockerd/#options-per-storage-driver) 中查看每个存储驱动程序的所有存储选项。

重启 Docker 以使更改生效。Docker 会调用命令为您配置块设备。

> [!WARNING]
> 在 Docker 为您准备好块设备后，不支持更改这些值，否则会导致错误。

您仍然需要 [执行定期维护任务](#manage-devicemapper)。

#### 手动配置 direct-lvm 模式

以下过程创建一个配置为精简池的逻辑卷，用作存储池的后端。它假设您在 `/dev/xvdf` 有一个闲置的块设备，且有足够的空闲空间来完成任务。设备标识符和卷大小在您的环境中可能不同，您应在整个过程中替换为您自己的值。该过程还假设 Docker 守护进程处于 `stopped` (已停止) 状态。

1.  确定您要使用的块设备。该设备位于 `/dev/` 下 (如 `/dev/xvdf`)，并且需要足够的空闲空间来存储该主机运行的工作负载的镜像和容器层。固态硬盘 (SSD) 是理想之选。

2.  停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

3.  安装以下软件包：

    - **RHEL / CentOS**: `device-mapper-persistent-data`、`lvm2` 及其所有依赖项。

    - **Ubuntu / Debian / SLES 15**: `thin-provisioning-tools`、`lvm2` 及其所有依赖项。

4.  使用 `pvcreate` 命令在步骤 1 的块设备上创建一个物理卷。将 `/dev/xvdf` 替换为您的设备名称。

    > [!WARNING]
    > 接下来的几个步骤具有破坏性，请务必确保指定了正确的设备。

    ```console
    $ sudo pvcreate /dev/xvdf

    Physical volume "/dev/xvdf" successfully created.
    ```

5.  使用 `vgcreate` 命令在同一设备上创建一个 `docker` 卷组。

    ```console
    $ sudo vgcreate docker /dev/xvdf

    Volume group "docker" successfully created
    ```

6.  使用 `lvcreate` 命令创建两个名为 `thinpool` 和 `thinpoolmeta` 的逻辑卷。最后一个参数指定了当空间不足时允许自动扩展数据或元数据的空闲空间量，作为临时缓冲。这些是推荐值。

    ```console
    $ sudo lvcreate --wipesignatures y -n thinpool docker -l 95%VG

    Logical volume "thinpool" created.

    $ sudo lvcreate --wipesignatures y -n thinpoolmeta docker -l 1%VG

    Logical volume "thinpoolmeta" created.
    ```

7.  使用 `lvconvert` 命令将这些卷转换为精简池以及精简池元数据的存储位置。

    ```console
    $ sudo lvconvert -y \
    --zero n \
    -c 512K \
    --thinpool docker/thinpool \
    --poolmetadata docker/thinpoolmeta

    WARNING: Converting logical volume docker/thinpool and docker/thinpoolmeta to
    thin pool's data and metadata volumes with metadata wiping.
    THIS WILL DESTROY CONTENT OF LOGICAL VOLUME (filesystem etc.)
    Converted docker/thinpool to thin pool.
    ```

8.  通过 `lvm` 配置文件配置精简池的自动扩展。

    ```console
    $ sudo vi /etc/lvm/profile/docker-thinpool.profile
    ```

9.  指定 `thin_pool_autoextend_threshold` 和 `thin_pool_autoextend_percent` 的值。

    `thin_pool_autoextend_threshold` 是在 `lvm` 尝试自动扩展可用空间之前已使用的空间百分比 (100 = 禁用，不推荐)。

    `thin_pool_autoextend_percent` 是自动扩展时添加到设备的容量百分比 (0 = 禁用)。

    下面的示例在磁盘使用率达到 80% 时增加 20% 的容量。

    ```none
    activation {
      thin_pool_autoextend_threshold=80
      thin_pool_autoextend_percent=20
    }
    ```

    保存文件。

10. 使用 `lvchange` 命令应用 LVM 配置文件。

    ```console
    $ sudo lvchange --metadataprofile docker-thinpool docker/thinpool

    Logical volume docker/thinpool changed.
    ```

11. 确保逻辑卷的监控已启用。

    ```console
    $ sudo lvs -o+seg_monitor

    LV       VG     Attr       LSize  Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert Monitor
    thinpool docker twi-a-t--- 95.00g             0.00   0.01                             not monitored
    ```

    如果 `Monitor` 列的输出如上所述显示为 `not monitored`，则需要显式启用监控。没有这一步，无论应用配置文件中的设置如何，逻辑卷都不会自动扩展。

    ```console
    $ sudo lvchange --monitor y docker/thinpool
    ```

    再次运行 `sudo lvs -o+seg_monitor` 命令，仔细检查监控是否已启用。`Monitor` 列现在应显示逻辑卷正在被 `monitored`。

12. 如果您之前曾在此主机上运行过 Docker，或者如果 `/var/lib/docker/` 存在，请将其移开，以便 Docker 可以使用新的 LVM 池来存储镜像和容器的内容。

    ```console
    $ sudo su -
    # mkdir /var/lib/docker.bk
    # mv /var/lib/docker/* /var/lib/docker.bk
    # exit
    ```

    如果以下任何步骤失败且您需要恢复，可以删除 `/var/lib/docker` 并将其替换为 `/var/lib/docker.bk`。

13. 编辑 `/etc/docker/daemon.json` 并配置 `devicemapper` 存储驱动程序所需的选项。如果该文件之前为空，现在应包含以下内容：

    ```json
    {
        "storage-driver": "devicemapper",
        "storage-opts": [
        "dm.thinpooldev=/dev/mapper/docker-thinpool",
        "dm.use_deferred_removal=true",
        "dm.use_deferred_deletion=true"
        ]
    }
    ```

14. 启动 Docker。

    **systemd**:

    ```console
    $ sudo systemctl start docker
    ```

    **service**:

    ```console
    $ sudo service docker start
    ```

15. 使用 `docker info` 验证 Docker 是否正在使用新配置。

    ```console
    $ docker info

    Containers: 0
     Running: 0
     Paused: 0
     Stopped: 0
    Images: 0
    Server Version: 17.03.1-ce
    Storage Driver: devicemapper
     Pool Name: docker-thinpool
     Pool Blocksize: 524.3 kB
     Base Device Size: 10.74 GB
     Backing Filesystem: xfs
     Data file:
     Metadata file:
     Data Space Used: 19.92 MB
     Data Space Total: 102 GB
     Data Space Available: 102 GB
     Metadata Space Used: 147.5 kB
     Metadata Space Total: 1.07 GB
     Metadata Space Available: 1.069 GB
     Thin Pool Minimum Free Space: 10.2 GB
     Udev Sync Supported: true
     Deferred Removal Enabled: true
     Deferred Deletion Enabled: true
     Deferred Deleted Device Count: 0
     Library Version: 1.02.135-RHEL7 (2016-11-16)
    <...>
    ```

    如果 Docker 配置正确，`Data file` 和 `Metadata file` 为空，且池名称为 `docker-thinpool`。

16. 验证配置正确后，可以删除包含先前配置的 `/var/lib/docker.bk` 目录。

    ```console
    $ sudo rm -rf /var/lib/docker.bk
    ```

## 管理 devicemapper

### 监控精简池

不要仅仅依赖 LVM 自动扩展。卷组会自动扩展，但卷仍然可能会填满。您可以使用 `lvs` 或 `lvs -a` 监控卷上的空闲空间。考虑在 OS 级别使用监控工具，如 Nagios。

要查看 LVM 日志，可以使用 `journalctl`：

```console
$ sudo journalctl -fu dm-event.service
```

如果您反复遇到精简池的问题，可以在 `/etc/docker/daemon.json` 中将存储选项 `dm.min_free_space` 设置为一个值 (表示百分比)。例如，将其设置为 `10` 可确保当空闲空间等于或接近 10% 时操作失败并发出警告。参见 [Engine 守护进程参考中的存储驱动程序选项](/reference/cli/dockerd/#daemon-storage-driver)。

### 增加运行中设备的容量

您可以增加运行中的精简池设备的池容量。当数据的逻辑卷已满且卷组已达到最大容量时，这非常有用。具体过程取决于您使用的是 [`loop-lvm` 精简池](#resize-a-loop-lvm-thin-pool) 还是 [`direct-lvm` 精简池](#resize-a-direct-lvm-thin-pool)。

#### 调整 loop-lvm 精简池的大小

调整 `loop-lvm` 精简池大小最简单的方法是 [使用 device_tool 实用工具](#use-the-device_tool-utility)，但您也可以 [使用操作系统实用工具](#use-operating-system-utilities) 代替。

##### 使用 device_tool 实用工具

在 [moby/moby](https://github.com/moby/moby/tree/master/contrib/docker-device-tool) Github 仓库中提供了一个名为 `device_tool.go` 的社区贡献脚本。您可以使用此工具调整 `loop-lvm` 精简池的大小，避免上述繁琐的过程。此工具不保证有效，但您只应在非生产系统上使用 `loop-lvm`。

如果您不想使用 `device_tool`，可以改为 [手动调整精简池的大小](#use-operating-system-utilities)。

1.  要使用该工具，请克隆 Github 仓库，进入 `contrib/docker-device-tool` 目录，并按照 `README.md` 中的说明编译该工具。

2.  使用该工具。以下示例将精简池大小调整为 200GB。

    ```console
    $ ./device_tool resize 200GB
    ```

##### 使用操作系统实用工具

如果您不想 [使用 device-tool 实用工具](#use-the-device_tool-utility)，可以使用以下过程手动调整 `loop-lvm` 精简池的大小。

在 `loop-lvm` 模式下，一个回环设备用于存储数据，另一个用于存储元数据。`loop-lvm` 模式仅支持测试，因为它在性能和稳定性方面存在显著缺陷。

如果您正在使用 `loop-lvm` 模式，`docker info` 的输出会显示 `Data loop file` 和 `Metadata loop file` 的文件路径：

```console
$ docker info |grep 'loop file'

 Data loop file: /var/lib/docker/devicemapper/data
 Metadata loop file: /var/lib/docker/devicemapper/metadata
```

按照以下步骤增加精简池的大小。在本示例中，精简池大小为 100 GB，并增加到 200 GB。

1.  列出设备的大小。

    ```console
    $ sudo ls -lh /var/lib/docker/devicemapper/

    total 1175492
    -rw------- 1 root root 100G Mar 30 05:22 data
    -rw------- 1 root root 2.0G Mar 31 11:17 metadata
    ```

2.  使用 `truncate` 命令将 `data` 文件的大小增加到 200 G，该命令用于增加 **或** 减少文件的大小。请注意，减小大小是一个破坏性操作。

    ```console
    $ sudo truncate -s 200G /var/lib/docker/devicemapper/data
    ```

3.  验证文件大小已更改。

    ```console
    $ sudo ls -lh /var/lib/docker/devicemapper/

    total 1.2G
    -rw------- 1 root root 200G Apr 14 08:47 data
    -rw------- 1 root root 2.0G Apr 19 13:27 metadata
    ```

4.  回环文件已在磁盘上更改，但在内存中未更改。列出内存中回环设备的大小 (以 GB 为单位)。重新加载它，然后再次列出大小。重新加载后，大小应为 200 GB。

    ```console
    $ echo $[ $(sudo blockdev --getsize64 /dev/loop0) / 1024 / 1024 / 1024 ]

    100

    $ sudo losetup -c /dev/loop0

    $ echo $[ $(sudo blockdev --getsize64 /dev/loop0) / 1024 / 1024 / 1024 ]

    200
    ```

5.  重新加载 devicemapper 精简池。

    a. 首先获取池名称。池名称是第一个字段，由 `:` 分隔。此命令提取它。

    ```console
    $ sudo dmsetup status | grep ' thin-pool ' | awk -F ': ' {'print $1'}
docker-8:1-123141-pool
    ```

    b. 转储精简池的设备映射器表。

    ```console
    $ sudo dmsetup table docker-8:1-123141-pool
    0 209715200 thin-pool 7:1 7:0 128 32768 1 skip_block_zeroing
    ```

    c. 使用输出的第二个字段计算精简池的总扇区数。该数值以 512-k 扇区表示。一个 100G 的文件有 209715200 个 512-k 扇区。如果您将此数字翻倍到 200G，您将得到 419430400 个 512-k 扇区。

    d. 使用以下三个 `dmsetup` 命令重新加载具有新扇区数的精简池。

    ```console
    $ sudo dmsetup suspend docker-8:1-123141-pool
    $ sudo dmsetup reload docker-8:1-123141-pool --table '0 419430400 thin-pool 7:1 7:0 128 32768 1 skip_block_zeroing'
    $ sudo dmsetup resume docker-8:1-123141-pool
    ```

#### 调整 direct-lvm 精简池的大小

要扩展 `direct-lvm` 精简池，您需要首先向 Docker 主机附加一个新的块设备，并记下内核分配给它的名称。在本示例中，新的块设备是 `/dev/xvdg`。

按照此过程扩展 `direct-lvm` 精简池，根据您的情况替换块设备和其他参数。

1.  收集有关您的卷组的信息。

    使用 `pvdisplay` 命令查找精简池当前正在使用的物理块设备以及卷组的名称。

    ```console
    $ sudo pvdisplay |grep 'VG Name'

    PV Name               /dev/xvdf
    VG Name               docker
    ```

    在接下来的步骤中，根据需要替换块设备或卷组名称。

2.  使用 `vgextend` 命令和上一步中的 `VG Name` 以及您的 **新** 块设备名称扩展卷组。

    ```console
    $ sudo vgextend docker /dev/xvdg

    Physical volume "/dev/xvdg" successfully created.
    Volume group "docker" successfully extended
    ```

3.  扩展 `docker/thinpool` 逻辑卷。此命令立即使用 100% 的卷，不使用自动扩展。要改为扩展元数据精简池，请使用 `docker/thinpool_tmeta`。

    ```console
    $ sudo lvextend -l+100%FREE -n docker/thinpool

    Size of logical volume docker/thinpool_tdata changed from 95.00 GiB (24319 extents) to 198.00 GiB (50688 extents).
    Logical volume docker/thinpool_tdata successfully resized.
    ```

4.  使用 `docker info` 输出中的 `Data Space Available` 字段验证新的精简池大小。如果您扩展的是 `docker/thinpool_tmeta` 逻辑卷，请查找 `Metadata Space Available`。

    ```bash
    Storage Driver: devicemapper
     Pool Name: docker-thinpool
     Pool Blocksize: 524.3 kB
     Base Device Size: 10.74 GB
     Backing Filesystem: xfs
     Data file:
     Metadata file:
     Data Space Used: 212.3 MB
     Data Space Total: 212.6 GB
     Data Space Available: 212.4 GB
     Metadata Space Used: 286.7 kB
     Metadata Space Total: 1.07 GB
     Metadata Space Available: 1.069 GB
    <...>
    ```

## `devicemapper` 存储驱动程序的工作原理

> [!WARNING]
> 不要直接操作 `/var/lib/docker/` 内的任何文件或目录。这些文件和目录由 Docker 管理。

使用 `lsblk` 命令从操作系统的角度查看设备及其池：

```console
$ sudo lsblk

NAME                    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
xvda                    202:0    0    8G  0 disk
└─xvda1                 202:1    0    8G  0 part /
xvdf                    202:80   0  100G  0 disk
├─docker-thinpool_tmeta 253:0    0 1020M  0 lvm
│ └─docker-thinpool     253:2    0   95G  0 lvm
└─docker-thinpool_tdata 253:1    0   95G  0 lvm
  └─docker-thinpool     253:2    0   95G  0 lvm
```

使用 `mount` 命令查看 Docker 正在使用的挂载点：

```console
$ mount |grep devicemapper
/dev/xvda1 on /var/lib/docker/devicemapper type xfs (rw,relatime,seclabel,attr2,inode64,noquota)
```

当您使用 `devicemapper` 时，Docker 将镜像和层内容存储在精简池中，并通过将它们挂载到 `/var/lib/docker/devicemapper/` 的子目录下将其暴露给容器。

### 磁盘上的镜像和容器层

`/var/lib/docker/devicemapper/metadata/` 目录包含有关 Devicemapper 配置本身以及存在的每个镜像和容器层的元数据。`devicemapper` 存储驱动程序使用快照，这些元数据包含有关这些快照的信息。这些文件采用 JSON 格式。

`/var/lib/docker/devicemapper/mnt/` 目录包含存在的每个镜像和容器层的挂载点。镜像层挂载点是空的，但容器的挂载点显示了从容器内部看到的容器文件系统。


### 镜像分层与共享

`devicemapper` 存储驱动程序使用专用块设备而不是格式化的文件系统，并在块级对文件进行操作，以便在写时复制 (CoW) 操作期间获得最大性能。

#### 快照 (Snapshots)

`devicemapper` 的另一个特性是其对快照的使用 (有时也称为 *精简设备 thin devices* 或 *虚拟设备 virtual devices*)，快照将每一层中引入的差异存储为非常小、轻量级的精简池。快照提供了许多好处：

- 容器之间共有的层在磁盘上仅存储一次，除非它们是可写的。例如，如果您有 10 个不同的镜像都基于 `alpine`，那么 `alpine` 镜像及其所有父镜像在磁盘上各仅存储一次。

- 快照是写时复制 (CoW) 策略的一种实现。这意味着只有当给定的文件或目录被该容器修改或删除时，它才会被复制到容器的可写层。

- 由于 `devicemapper` 在块级运行，因此可写层中的多个块可以同时被修改。

- 可以使用标准的 OS 级别备份实用工具对快照进行备份。只需复制 `/var/lib/docker/devicemapper/` 即可。

#### Devicemapper 工作流

当您使用 `devicemapper` 存储驱动程序启动 Docker 时，所有与镜像和容器层相关的对象都存储在 `/var/lib/docker/devicemapper/` 中，该目录由一个或多个块级设备 (回环设备 (仅测试) 或物理磁盘) 提供后端支持。

- *基础设备 (base device)* 是最低级别的对象。这就是精简池本身。您可以使用 `docker info` 检查它。它包含一个文件系统。这个基础设备是每个镜像和容器层的起点。基础设备是 Device Mapper 的实现细节，而不是 Docker 层。

- 关于基础设备及每个镜像或容器层的元数据以 JSON 格式存储在 `/var/lib/docker/devicemapper/metadata/` 中。这些层是写时复制快照，这意味着在它们与父层发生偏离之前，它们是空的。

- 每个容器的可写层挂载在 `/var/lib/docker/devicemapper/mnt/` 的一个挂载点上。每个只读镜像层和每个已停止的容器都有一个空目录。

每个镜像层都是其下方一层的快照。每个镜像的最底层是池中存在的基础设备的快照。当您运行一个容器时，它是该容器所基于镜像的一个快照。以下示例显示了一个具有两个运行中容器的 Docker 主机。

![Ubuntu 和 busybox 镜像层](images/two_dm_container.webp?w=450&h=100)

## `devicemapper` 下容器的读写工作原理

### 读取文件

使用 `devicemapper`，读取发生在块级。下图显示了在示例容器中读取单个块 (`0x44f`) 的高级过程。

![使用 devicemapper 读取一个块](images/dm_container.webp?w=650)

应用程序向容器发出对块 `0x44f` 的读取请求。由于容器是一个镜像的精简快照，它没有该块，但它有一个指向该块存在的最近父镜像的指针，并从那里读取该块。该块现在存在于容器的内存中。

### 写入文件

**写入新文件**: 使用 `devicemapper` 驱动程序，向容器写入新数据是通过 *按需分配 (allocate-on-demand)* 操作完成的。新文件的每个块都在容器的可写层中分配，并将该块写入其中。

**更新现有文件**: 从文件所在的最近层读取相关的块。当容器写入文件时，只有修改后的块会被写入容器的可写层。

**删除文件或目录**: 当您在容器的可写层中删除文件或目录时，或者当镜像层删除了存在于其父层中的文件时，`devicemapper` 存储驱动程序会拦截对该文件或目录的进一步读取尝试，并响应称该文件或目录不存在。

**写入然后删除文件**: 如果容器向一个文件写入内容，随后又删除了该文件，则所有这些操作都发生在容器的可写层中。在这种情况下，如果您使用的是 `direct-lvm`，这些块会被释放。如果您使用的是 `loop-lvm`，这些块可能不会被释放。这是不在生产环境中使用 `loop-lvm` 的另一个原因。

## Device Mapper 与 Docker 性能

- **`allocate-on-demand` 性能影响**: 

  `devicemapper` 存储驱动程序使用 `allocate-on-demand` 操作从精简池中向容器的可写层分配新块。每个块为 64KB，因此这是写入操作使用的最小空间。

- **写时复制性能影响**: 容器第一次修改特定块时，该块会被写入容器的可写层。由于这些写入发生在块级别而不是文件级别，因此性能影响被降至最低。但是，写入大量块仍可能对性能产生负面影响，在这种情况下，`devicemapper` 存储驱动程序的表现实际上可能比其他存储驱动程序差。对于写密集型工作负载，您应该使用数据卷，它完全绕过了存储驱动程序。

### 性能最佳实践

在使用 `devicemapper` 存储驱动程序时，请记住以下几点以最大化性能。

- **使用 `direct-lvm`**: `loop-lvm` 模式性能不佳，切勿在生产环境中使用。

- **使用快速存储**: 固态硬盘 (SSD) 比机械硬盘提供更快的读写速度。

- **内存使用**: `devicemapper` 比其他一些存储驱动程序消耗更多内存。每个启动的容器都会将其文件的副本加载到内存中，具体取决于同时修改了同一个文件的多少个块。由于内存压力，对于高密度用例中的某些工作负载，`devicemapper` 存储驱动程序可能不是正确的选择。

- **对于写密集型工作负载使用卷**: 卷为写密集型工作负载提供最佳且最可预测的性能。这是因为它们绕过了存储驱动程序，不会产生由精简置备和写时复制引入的任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并且即使没有运行中的容器使用它们也会持久存在。

  > [!NOTE]
  > 
  > 在使用 `devicemapper` 和 `json-file` 日志驱动程序时，容器生成的日志文件仍然存储在 Docker 的数据根目录中 (默认 `/var/lib/docker`)。如果您的容器生成大量日志消息，这可能会导致磁盘使用量增加，或者由于磁盘空间已满而导致无法管理系统。您可以配置 [日志驱动程序](/manuals/engine/logging/configure.md) 以外部方式存储容器日志。

## 相关信息

- [卷 (Volumes)](../volumes.md)
- [了解镜像、容器和存储驱动程序](./_index.md)
- [选择存储驱动程序](select-storage-driver.md)
