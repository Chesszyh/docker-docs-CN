---
description: 了解如何优化 VFS 驱动程序的使用。
keywords: container, storage, driver, vfs, 容器, 存储, 驱动程序
title: VFS 存储驱动程序
aliases:
  - /storage/storagedriver/vfs-driver/
---

VFS 存储驱动程序不是联合文件系统。每一层都是磁盘上的一个目录，且没有写时复制 (copy-on-write) 支持。要创建一个新层，会对前一层进行“深拷贝 (deep copy)”。这导致性能较低，且比其他存储驱动程序占用更多的磁盘空间。然而，它健壮、稳定，且适用于每种环境。它还可以作为一种机制，在测试环境中验证其他存储后端。

## 为 Docker 配置 `vfs` 存储驱动程序

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2.  编辑 `/etc/docker/daemon.json`。如果该文件尚不存在，请创建它。假设该文件之前为空，添加以下内容：

    ```json
    {
      "storage-driver": "vfs"
    }
    ```

    如果您想设置配额来控制 VFS 存储驱动程序可以使用的最大大小，请在 `storage-opts` 键上设置 `size` 选项。

    ```json
    {
      "storage-driver": "vfs",
      "storage-opts": ["size=256M"]
    }
    ```

    如果 `daemon.json` 文件包含无效的 JSON，Docker 将无法启动。

3.  启动 Docker。

    ```console
    $ sudo systemctl start docker
    ```

4.  验证守护进程是否正在使用 `vfs` 存储驱动程序。使用 `docker info` 命令并查找 `Storage Driver`。

    ```console
    $ docker info

    Storage Driver: vfs
    ...
    ```

Docker 现在正在使用 `vfs` 存储驱动程序。Docker 已自动创建了 `/var/lib/docker/vfs/` 目录，其中包含运行中容器使用的所有层。

## `vfs` 存储驱动程序的工作原理

每个镜像层以及可写容器层在 Docker 主机上都表示为 `/var/lib/docker/` 内的子目录。联合挂载提供了所有层的统一视图。目录名称并不直接对应于层本身的 ID。

VFS 不支持写时复制 (COW)。每次创建一个新层时，它都是其父层的深拷贝。这些层都位于 `/var/lib/docker/vfs/dir/` 下。

### 示例：磁盘上的镜像和容器结构

以下 `docker pull` 命令显示了 Docker 主机下载一个包含五层的 Docker 镜像。

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
e0a742c2abfd: Pull complete
486cb8339a27: Pull complete
dc6f0d824617: Pull complete
4f7a5649a30e: Pull complete
672363445ad2: Pull complete
Digest: sha256:84c334414e2bfdcae99509a6add166bbb4fa4041dc3fa6af08046a66fed3005f
Status: Downloaded newer image for ubuntu:latest
```

拉取后，每一层都表示为 `/var/lib/docker/vfs/dir/` 的一个子目录。目录名称与 `docker pull` 命令中显示的镜像层 ID 不相关。要查看每一层在磁盘上占用的大小，可以使用 `du -sh` 命令，它会以人类可读的数值给出大小。

```console
$ ls -l /var/lib/docker/vfs/dir/

total 0
drwxr-xr-x.  2 root root  19 Aug  2 18:19 3262dfbe53dac3e1ab7dcc8ad5d8c4d586a11d2ac3c4234892e34bff7f6b821e
drwxr-xr-x. 21 root root 224 Aug  2 18:23 6af21814449345f55d88c403e66564faad965d6afa84b294ae6e740c9ded2561
drwxr-xr-x. 21 root root 224 Aug  2 18:23 6d3be4585ba32f9f5cbff0110e8d07aea5f5b9fbb1439677c27e7dfee263171c
drwxr-xr-x. 21 root root 224 Aug  2 18:23 9ecd2d88ca177413ab89f987e1507325285a7418fc76d0dcb4bc021447ba2bab
drwxr-xr-x. 21 root root 224 Aug  2 18:23 a292ac6341a65bf3a5da7b7c251e19de1294bd2ec32828de621d41c7ad31f895
drwxr-xr-x. 21 root root 224 Aug  2 18:23 e92be7a4a4e3ccbb7dd87695bca1a0ea373d4f673f455491b1342b33ed91446b
```

```console
$ du -sh /var/lib/docker/vfs/dir/*

4.0K	/var/lib/docker/vfs/dir/3262dfbe53dac3e1ab7dcc8ad5d8c4d586a11d2ac3c4234892e34bff7f6b821e
125M	/var/lib/docker/vfs/dir/6af21814449345f55d88c403e66564faad965d6afa84b294ae6e740c9ded2561
104M	/var/lib/docker/vfs/dir/6d3be4585ba32f9f5cbff0110e8d07aea5f5b9fbb1439677c27e7dfee263171c
125M	/var/lib/docker/vfs/dir/9ecd2d88ca177413ab89f987e1507325285a7418fc76d0dcb4bc021447ba2bab
104M	/var/lib/docker/vfs/dir/a292ac6341a65bf3a5da7b7c251e19de1294bd2ec32828de621d41c7ad31f895
104M	/var/lib/docker/vfs/dir/e92be7a4a4e3ccbb7dd87695bca1a0ea373d4f673f455491b1342b33ed91446b
```

上述输出显示三层各占用 104M，两层各占用 125M。这些目录彼此之间只有很小的差异，但它们都消耗相同数量的磁盘空间。这是使用 `vfs` 存储驱动程序的缺点之一。

## 相关信息

- [了解镜像、容器和存储驱动程序](index.md)
- [选择存储驱动程序](select-storage-driver.md)
