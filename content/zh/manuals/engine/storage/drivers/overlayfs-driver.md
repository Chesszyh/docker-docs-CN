---
description: 了解如何优化 OverlayFS 驱动程序的使用。
keywords: container, storage, driver, OverlayFS, overlay2, overlay, 容器, 存储, 驱动程序
title: OverlayFS 存储驱动程序
aliases:
  - /storage/storagedriver/overlayfs-driver/
---

OverlayFS 是一个联合文件系统 (union filesystem)。

本页将 Linux 内核驱动程序称为 `OverlayFS`，将 Docker 存储驱动程序称为 `overlay2`。

> [!NOTE]
>
> 对于 `fuse-overlayfs` 驱动程序，请查阅 [无根模式文档](/manuals/engine/security/rootless.md)。

## 前提条件

OverlayFS 是推荐的存储驱动程序，如果您满足以下前提条件，则受支持：

- Linux 内核版本 4.0 或更高，或者是使用 3.10.0-514 或更高版本内核的 RHEL 或 CentOS。
- `overlay2` 驱动程序在 `xfs` 底层文件系统上受支持，但必须启用 `d_type=true`。

  使用 `xfs_info` 验证 `ftype` 选项是否设置为 `1`。要正确格式化 `xfs` 文件系统，请使用标志 `-n ftype=1`。

- 更改存储驱动程序会使现有的容器和镜像在本地系统上无法访问。在更改存储驱动程序之前，请使用 `docker save` 保存您构建的任何镜像，或将其推送到 Docker Hub 或私有注册表，这样您以后就无需重新创建它们。

## 为 Docker 配置 `overlay2` 存储驱动程序

在执行此过程之前，您必须首先满足所有 [前提条件](#prerequisites)。

以下步骤概述了如何配置 `overlay2` 存储驱动程序。

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2. 将 `/var/lib/docker` 的内容复制到临时位置。

   ```console
   $ cp -au /var/lib/docker /var/lib/docker.bk
   ```

3. 如果您想使用与 `/var/lib/` 所用不同的独立底层文件系统，请格式化该文件系统并将其挂载到 `/var/lib/docker`。确保将此挂载添加到 `/etc/fstab` 中使其持久化。

4. 编辑 `/etc/docker/daemon.json`。如果该文件尚不存在，请创建它。假设该文件之前为空，添加以下内容：

   ```json
   {
     "storage-driver": "overlay2"
   }
   ```

   如果 `daemon.json` 文件包含无效的 JSON，Docker 将无法启动。

5. 启动 Docker。

   ```console
   $ sudo systemctl start docker
   ```

6. 验证守护进程是否正在使用 `overlay2` 存储驱动程序。使用 `docker info` 命令并查找 `Storage Driver` 和 `Backing filesystem`。

   ```console
   $ docker info

   Containers: 0
   Images: 0
   Storage Driver: overlay2
    Backing Filesystem: xfs
    Supports d_type: true
    Native Overlay Diff: true
   <...>
   ```

Docker 现在正在使用 `overlay2` 存储驱动程序，并已自动创建了带有必要 `lowerdir`、`upperdir`、`merged` 和 `workdir` 结构的 overlay 挂载。

继续阅读有关 OverlayFS 在 Docker 容器中如何工作的详细信息，以及性能建议和有关其与不同底层文件系统兼容性限制的信息。

## `overlay2` 驱动程序的工作原理

OverlayFS 在单个 Linux 主机上将两个目录分层，并将它们呈现为单个目录。这些目录被称为层 (layers)，统一过程被称为联合挂载 (union mount)。OverlayFS 将较低的目录称为 `lowerdir`，将较高的目录称为 `upperdir`。统一的视图通过其自身名为 `merged` 的目录暴露出来。

`overlay2` 驱动程序原生支持多达 128 个较低的 OverlayFS 层。这种能力为与层相关的 Docker 命令 (如 `docker build` 和 `docker commit`) 提供了更好的性能，并在底层文件系统上消耗更少的索引节点 (inodes)。

### 磁盘上的镜像和容器层

下载一个五层镜像 (使用 `docker pull ubuntu`) 后，您可以在 `/var/lib/docker/overlay2` 下看到六个目录。

> [!WARNING]
>
> 不要直接操作 `/var/lib/docker/` 内的任何文件或目录。这些文件和目录由 Docker 管理。

```console
$ ls -l /var/lib/docker/overlay2

total 24
drwx------ 5 root root 4096 Jun 20 07:36 223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7
drwx------ 3 root root 4096 Jun 20 07:36 3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b
drwx------ 5 root root 4096 Jun 20 07:36 4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1
drwx------ 5 root root 4096 Jun 20 07:36 e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5
drwx------ 5 root root 4096 Jun 20 07:36 eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed
drwx------ 2 root root 4096 Jun 20 07:36 l
```

新的 `l` (小写 `L`) 目录包含作为符号链接的缩短层标识符。这些标识符用于避免在 `mount` 命令的参数中超出页面大小限制。

```console
$ ls -l /var/lib/docker/overlay2/l

total 20
lrwxrwxrwx 1 root root 72 Jun 20 07:36 6Y5IM2XC7TSNIJZZFLJCS6I4I4 -> ../3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 B3WWEFKBG3PLLV737KZFIASSW7 -> ../4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 JEYMODZYFCZFYSDABYXD5MF6YO -> ../eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 NFYKDW6APBCCUCTOUSYDH4DXAT -> ../223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 UL2MW33MSE3Q5VYIKBRN4ZAGQP -> ../e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5/diff
```

最低层包含一个名为 `link` 的文件 (包含缩短标识符的名称) 以及一个名为 `diff` 的目录 (包含层的内容)。

```console
$ ls /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/

diff  link

$ cat /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/link

6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls  /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff

bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

倒数第二层以及之上的每一层都包含一个名为 `lower` 的文件 (表示其父层) 以及一个名为 `diff` 的目录 (包含其内容)。它还包含一个 `merged` 目录 (包含其父层与其自身的统一内容) 以及一个 `work` 目录 (由 OverlayFS 内部使用)。

```console
$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7

diff  link  lower  merged  work

$ cat /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/lower

l/6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff/

etc  sbin  usr  var
```

要查看在 Docker 中使用 `overlay` 存储驱动程序时存在的挂载，请使用 `mount` 命令。为了可读性，以下输出经过了截断。

```console
$ mount | grep overlay

overlay on /var/lib/docker/overlay2/9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/merged
type overlay (rw,relatime,
lowerdir=l/DJA75GUWHWG7EWICFYX54FIOVT:l/B3WWEFKBG3PLLV737KZFIASSW7:l/JEYMODZYFCZFYSDABYXD5MF6YO:l/UL2MW33MSE3Q5VYIKBRN4ZAGQP:l/NFYKDW6APBCCUCTOUSYDH4DXAT:l/6Y5IM2XC7TSNIJZZFLJCS6I4I4,
upperdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/diff,
workdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/work)
```

第二行的 `rw` 显示 `overlay` 挂载是读写的。

下图显示了 Docker 镜像和 Docker 容器是如何分层的。镜像层是 `lowerdir`，容器层是 `upperdir`。如果镜像有多个层，则使用多个 `lowerdir` 目录。统一的视图通过一个名为 `merged` 的目录暴露出来，该目录实际上就是容器的挂载点。

![Docker 结构如何映射到 OverlayFS 结构](images/overlay_constructs.webp)

当镜像层和容器层包含相同的文件时，容器层 (`upperdir`) 具有更高的优先级，并遮蔽镜像层中相同文件的存在。

为了创建一个容器，`overlay2` 驱动程序结合了代表镜像顶层的目录加上一个为容器准备的新目录。镜像的层是 overlay 中的 `lowerdirs` 且为只读。容器的新目录是 `upperdir` 且为可写。

### 磁盘上的镜像和容器层

以下 `docker pull` 命令显示了 Docker 主机下载一个包含五层的 Docker 镜像。

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu

5ba4f30e5bea: Pull complete
9d7d19c9dc56: Pull complete
ac6ad7efd0f9: Pull complete
e7491a747824: Pull complete
a3ed95caeb02: Pull complete
Digest: sha256:46fb5d001b88ad904c5c732b086b596b92cfb4a4840a3abd0e35dbb6870585e4
Status: Downloaded newer image for ubuntu:latest
```

#### 镜像层

每个镜像层在 `/var/lib/docker/overlay/` 中都有自己的目录，包含其内容，如下例所示。镜像层 ID 不对应目录 ID。

> [!WARNING]
>
> 不要直接操作 `/var/lib/docker/` 内的任何文件或目录。这些文件和目录由 Docker 管理。

```console
$ ls -l /var/lib/docker/overlay/

total 20
drwx------ 3 root root 4096 Jun 20 16:11 38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8
drwx------ 3 root root 4096 Jun 20 16:11 55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
drwx------ 3 root root 4096 Jun 20 16:11 824c8a961a4f5e8fe4f4243dab57c5be798e7fd195f6d88ab06aea92ba931654
drwx------ 3 root root 4096 Jun 20 16:11 ad0fe55125ebf599da124da175174a4b8c1878afe6907bf7c78570341f308461
drwx------ 3 root root 4096 Jun 20 16:11 edab9b5e5bf73f2997524eebeac1de4cf9c8b904fa8ad3ec43b3504196aa3801
```

镜像层目录包含该层独有的文件，以及指向与较低层共享的数据的硬链接。这实现了磁盘空间的高效利用。

```console
$ ls -i /var/lib/docker/overlay2/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls

19793696 /var/lib/docker/overlay2/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls

$ ls -i /var/lib/docker/overlay2/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls

19793696 /var/lib/docker/overlay2/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls
```

#### 容器层

容器也存在于 Docker 主机文件系统中的 `/var/lib/docker/overlay/` 下。如果您使用 `ls -l` 命令列出运行中容器的子目录，会发现存在三个目录和一个文件：

```console
$ ls -l /var/lib/docker/overlay2/<directory-of-running-container>

total 16
-rw-r--r-- 1 root root   64 Jun 20 16:39 lower-id
drwxr-xr-x 1 root root 4096 Jun 20 16:39 merged
drwxr-xr-x 4 root root 4096 Jun 20 16:39 upper
drwx------ 3 root root 4096 Jun 20 16:39 work
```

`lower-id` 文件包含容器所基于镜像的最顶层的 ID，即 OverlayFS 的 `lowerdir`。

```console
$ cat /var/lib/docker/overlay2/ec444863a55a9f1ca2df72223d459c5d940a721b2288ff86a3f27be28b53be6c/lower-id

55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
```

`upper` 目录包含容器读写层的内容，对应 OverlayFS 的 `upperdir`。

`merged` 目录是 `lowerdir` 和 `upperdirs` 的联合挂载，构成了从运行中容器内部看到的文件系统视图。

`work` 目录供 OverlayFS 内部使用。

要查看使用 `overlay2` 存储驱动程序时存在的挂载，请使用 `mount` 命令。以下输出为提高可读性已截断。

```console
$ mount | grep overlay

overlay on /var/lib/docker/overlay2/l/ec444863a55a.../merged
type overlay (rw,relatime,lowerdir=/var/lib/docker/overlay2/l/55f1e14c361b.../root,
upperdir=/var/lib/docker/overlay2/l/ec444863a55a.../upper,
workdir=/var/lib/docker/overlay2/l/ec444863a55a.../work)
```

第二行的 `rw` 显示 `overlay` 挂载是读写的。

## `overlay2` 下容器的读写工作原理

### 读取文件

在使用 overlay 的容器打开文件进行读取访问时，考虑以下三种场景：

#### 文件不存在于容器层中

如果容器打开一个文件进行读取访问，而该文件尚未存在于容器 (`upperdir`) 中，则从镜像 (`lowerdir`) 中读取。这产生的性能开销非常小。

#### 文件仅存在于容器层中

如果容器打开一个文件进行读取访问，且该文件存在于容器 (`upperdir`) 中而不在镜像 (`lowerdir`) 中，则直接从容器中读取。

#### 文件同时存在于容器层和镜像层中

如果容器打开一个文件进行读取访问，且该文件同时存在于镜像层和容器层中，则读取容器层中的文件版本。容器层 (`upperdir`) 中的文件会遮蔽镜像层 (`lowerdir`) 中具有相同名称的文件。

### 修改文件或目录

考虑容器中文件被修改的一些场景：

#### 第一次写入文件

容器第一次向现有文件写入内容时，该文件尚不存在于容器 (`upperdir`) 中。`overlay2` 驱动程序执行 `copy_up` 操作，将文件从镜像 (`lowerdir`) 复制到容器 (`upperdir`)。然后容器将更改写入容器层中该文件的新副本。

但是，OverlayFS 工作在文件级别而不是块级别。这意味着所有的 OverlayFS `copy_up` 操作都会复制整个文件，即使文件很大且仅修改了其中的一小部分。这会对容器的写入性能产生显著影响。但是，有两点值得注意：

- `copy_up` 操作仅在第一次写入给定文件时发生。随后对同一文件的写入将针对已复制到容器的文件副本进行操作。

- OverlayFS 支持多层。这意味着在具有多层的镜像中搜索文件时，性能可能会受到影响。

#### 删除文件和目录

- 在容器内删除 *文件* 时，会在容器 (`upperdir`) 中创建一个 *遮蔽 (whiteout)* 文件。镜像层 (`lowerdir`) 中的文件版本不会被删除 (因为 `lowerdir` 是只读的)。但是，遮蔽文件会阻止它对容器可用。

- 在容器内删除 *目录* 时，会在容器 (`upperdir`) 中创建一个 *不透明目录 (opaque directory)*。这与遮蔽文件的工作方式相同，可以有效地防止目录被访问，即使它仍然存在于镜像 (`lowerdir`) 中。

#### 重命名目录

仅当源路径和目标路径都在最顶层时，才允许对目录调用 `rename(2)`。否则，它会返回 `EXDEV` 错误 (“不允许跨设备链接”)。您的应用程序需要设计为能够处理 `EXDEV` 并回退到“复制并取消链接”策略。

## OverlayFS 与 Docker 性能

`overlay2` 的性能可能优于 `btrfs`。但是，请注意以下细节：

### 页面缓存 (Page caching)

OverlayFS 支持页面缓存共享。访问同一个文件的多个容器共享该文件的单个页面缓存条目。这使得 `overlay2` 驱动程序能高效利用内存，是 PaaS 等高密度用例的理想选择。

### Copyup

与其他写时复制文件系统一样，每当容器第一次向文件写入内容时，OverlayFS 都会执行 copy-up 操作。这会给写入操作增加延迟，特别是对于大文件。但是，一旦文件被复制上去，随后对该文件的所有写入都发生在顶层，无需进一步的 copy-up 操作。

### 性能最佳实践

以下通用的性能最佳实践适用于 OverlayFS。

#### 使用快速存储

固态硬盘 (SSD) 比机械硬盘提供更快的读写速度。

#### 对于写密集型工作负载使用卷

对于写密集型工作负载，卷提供了最佳且最可预测的性能。这是因为它们绕过了存储驱动程序，不会产生由于精简置备和写时复制引入的任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并且即使没有运行中的容器使用它们，数据也会持久存在。

## OverlayFS 兼容性限制

总结一下 OverlayFS 与其他文件系统不兼容的方面：

[`open(2)`](https://linux.die.net/man/2/open)
: OverlayFS 仅实现了 POSIX 标准的一个子集。这可能导致某些 OverlayFS 操作违反 POSIX 标准。其中一个操作就是 copy-up 操作。假设您的应用程序调用 `fd1=open("foo", O_RDONLY)`，然后调用 `fd2=open("foo", O_RDWR)`。在这种情况下，您的应用程序期望 `fd1` 和 `fd2` 指向同一个文件。然而，由于在第二次调用 `open(2)` 后发生了 copy-up 操作，这两个描述符实际上指向了不同的文件。`fd1` 继续指向镜像 (`lowerdir`) 中的文件，而 `fd2` 指向容器 (`upperdir`) 中的文件。解决此问题的一个变通方法是 `touch` 文件，这会触发 copy-up 操作发生。随后所有的 `open(2)` 操作，无论读写模式如何，都将指向容器 (`upperdir`) 中的文件。

  已知 `yum` 会受此影响，除非安装了 `yum-plugin-ovl` 软件包。如果您的发行版 (如 6.8 或 7.2 之前的 RHEL/CentOS) 中没有 `yum-plugin-ovl` 包，您可能需要在运行 `yum install` 之前运行 `touch /var/lib/rpm/*`。该软件包为 `yum` 实现了上述引用的 `touch` 变通方法。

[`rename(2)`](https://linux.die.net/man/2/rename)
: OverlayFS 不完全支持 `rename(2)` 系统调用。您的应用程序需要检测其失败并回退到“复制并取消链接”策略。
