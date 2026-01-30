---
description: 使用 tmpfs 挂载 (tmpfs mounts)
title: tmpfs 挂载 (tmpfs mounts)
weight: 30
keywords: storage, persistence, data persistence, tmpfs, 存储, 持久化, 挂载
---

[卷 (volumes)](volumes.md) 和 [绑定挂载 (bind mounts)](bind-mounts.md) 允许您在主机和容器之间共享文件，以便在容器停止后也能持久化数据。

如果您在 Linux 上运行 Docker，您还有第三个选择：tmpfs 挂载。当您创建一个带有 tmpfs 挂载的容器时，容器可以在容器的可写层之外创建文件。

与卷和绑定挂载相反，tmpfs 挂载是临时的，仅持久化在主机的内存中。当容器停止时，tmpfs 挂载会被移除，写入其中的文件将不会被持久化。

tmpfs 挂载最适合用于您不希望数据持久化到主机或容器内部的情况。这可能是出于安全原因，或者是在应用程序需要写入大量非持久状态数据时为了保护容器的性能。

> [!IMPORTANT]
> Docker 中的 tmpfs 挂载直接映射到 Linux 内核中的 [tmpfs](https://en.wikipedia.org/wiki/Tmpfs)。因此，临时数据可能会被写入交换文件 (swap file)，从而持久化到文件系统中。

## 在现有数据上挂载

如果您将 tmpfs 挂载到一个容器中已存在文件或目录的目录中，则预先存在的文件会被该挂载遮蔽。这类似于如果您在 Linux 主机上将文件保存到 `/mnt` 中，然后将 USB 驱动器挂载到 `/mnt` 中。在卸载 USB 驱动器之前，`/mnt` 的内容将被 USB 驱动器的内容遮蔽。

对于容器，没有直接的方法来移除挂载以再次显示被遮蔽的文件。最好的选择是在没有该挂载的情况下重新创建容器。

## tmpfs 挂载的限制

- 与卷和绑定挂载不同，您不能在容器之间共享 tmpfs 挂载。
- 此功能仅在 Linux 上运行 Docker 时可用。
- 在 tmpfs 上设置权限可能会导致它们在 [容器重启后重置](https://github.com/docker/for-linux/issues/138)。在某些情况下，[设置 uid/gid](https://github.com/docker/compose/issues/3425#issuecomment-423091370) 可以作为一种变通方法。

## 语法

要使用 `docker run` 命令挂载 tmpfs，您可以使用 `--mount` 或 `--tmpfs` 标志。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>
$ docker run --tmpfs <mount-path>
```

通常，首选 `--mount`。主要区别在于 `--mount` 标志更加明确。另一方面，`--tmpfs` 较简洁，并为您提供了更多灵活性，因为它允许您设置更多挂载选项。

`--tmpfs` 标志不能用于 swarm 服务。您必须使用 `--mount`。

### --tmpfs 的选项

`--tmpfs` 标志由两个字段组成，由冒号 (`:`) 分隔。

```console
$ docker run --tmpfs <mount-path>[:opts]
```

第一个字段是要挂载到 tmpfs 的容器路径。第二个字段是可选的，允许您设置挂载选项。`--tmpfs` 的有效挂载选项包括：

| 选项         | 描述                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `ro`         | 创建只读 tmpfs 挂载。                                                            |
| `rw`         | 创建读写 tmpfs 挂载 (默认行为)。                                        |
| `nosuid`     | 防止在执行期间遵守 `setuid` 和 `setgid` 位。                    |
| `suid`       | 允许在执行期间遵守 `setuid` 和 `setgid` 位 (默认行为)。        |
| `nodev`      | 可以创建设备文件，但不可用 (访问会导致错误)。            |
| `dev`        | 可以创建设备文件，并且完全可用。                                       |
| `exec`       | 允许在挂载的文件系统中执行可执行二进制文件。                     |
| `noexec`     | 不允许在挂载的文件系统中执行可执行二进制文件。             |
| `sync`       | 对文件系统的所有 I/O 都是同步进行的。                                           |
| `async`      | 对文件系统的所有 I/O 都是异步进行的 (默认行为)。                       |
| `dirsync`    | 文件系统内的目录更新是同步进行的。                            |
| `atime`      | 每次访问文件时更新文件访问时间。                                    |
| `noatime`    | 访问文件时不更新文件访问时间。                                |   |
| `diratime`   | 每次访问目录时更新目录访问时间。                         |
| `nodiratime` | 访问目录时不更新目录访问时间。                      |
| `size`       | 指定 tmpfs 挂载的大小，例如 `size=64m`。                             |
| `mode`       | 指定 tmpfs 挂载的文件模式 (权限) (例如 `mode=1777`)。       |
| `uid`        | 指定 tmpfs 挂载所有者的用户 ID (例如 `uid=1000`)。           |
| `gid`        | 指定 tmpfs 挂载所有者的组 ID (例如 `gid=1000`)。          |
| `nr_inodes`  | 指定 tmpfs 挂载的最大索引节点 (inode) 数 (例如 `nr_inodes=400k`)。 |
| `nr_blocks`  | 指定 tmpfs 挂载的最大块数 (例如 `nr_blocks=1024`)。 |

```console {title="示例"}
$ docker run --tmpfs /data:noexec,size=1024,mode=1777
```

并非 Linux mount 命令中可用的所有 tmpfs 挂载功能在 `--tmpfs` 标志中都受支持。如果您需要高级 tmpfs 选项或功能，您可能需要使用特权容器或在 Docker 外部配置挂载。

> [!CAUTION]
> 使用 `--privileged` 运行容器会授予提升的权限，并将主机系统暴露在安全风险中。仅在绝对必要且受信任的环境中使用此选项。

```console
$ docker run --privileged -it debian sh
/# mount -t tmpfs -o <options> tmpfs /data
```

### --mount 的选项

`--mount` 标志由多个键值对组成，由逗号分隔，每个键值对由一个 `<key>=<value>` 元组组成。键的顺序并不重要。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>[,<key>=<value>...]
```

`--mount type=tmpfs` 的有效选项包括：

| 选项                           | 描述                                                                                                            |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `destination`, `dst`, `target` | 要挂载到 tmpfs 的容器路径。                                                                                  |
| `tmpfs-size`                   | tmpfs 挂载的大小 (以字节为单位)。如果未设置，tmpfs 卷的默认最大大小为主机总内存的 50%。 |
| `tmpfs-mode`                   | tmpfs 的文件模式 (八进制)。例如 `700` 或 `0770`。默认为 `1777` 或所有人可写。                  |

```console {title="示例"}
$ docker run --mount type=tmpfs,dst=/app,tmpfs-size=21474836480,tmpfs-mode=1770
```

## 在容器中使用 tmpfs 挂载

要在容器中使用 `tmpfs` 挂载，使用 `--tmpfs` 标志，或者使用带有 `type=tmpfs` 和 `destination` 选项的 `--mount` 标志。`tmpfs` 挂载没有 `source`。以下示例在 Nginx 容器中的 `/app` 处创建一个 `tmpfs` 挂载。第一个示例使用 `--mount` 标志，第二个示例使用 `--tmpfs` 标志。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name tmptest \
  --mount type=tmpfs,destination=/app \
  nginx:latest
```

通过查看 `docker inspect` 输出的 `Mounts` 部分，验证该挂载是否为 `tmpfs` 挂载：

```console
$ docker inspect tmptest --format '{{ json .Mounts }}'
[{"Type":"tmpfs","Source":"","Destination":"/app","Mode":"","RW":true,"Propagation":""}]
```

{{< /tab >}}
{{< tab name="`--tmpfs`" >}}

```console
$ docker run -d \
  -it \
  --name tmptest \
  --tmpfs /app \
  nginx:latest
```

通过查看 `docker inspect` 输出的 `Mounts` 部分，验证该挂载是否为 `tmpfs` 挂载：

```console
$ docker inspect tmptest --format '{{ json .Mounts }}'
{" /app":""}
```

{{< /tab >}}
{{< /tabs >}}

停止并移除容器：

```console
$ docker stop tmptest
$ docker rm tmptest
```

## 后续步骤

- 了解 [卷 (volumes)](volumes.md)
- 了解 [绑定挂载 (bind mounts)](bind-mounts.md)
- 了解 [存储驱动程序 (storage drivers)](/engine/storage/drivers/)

