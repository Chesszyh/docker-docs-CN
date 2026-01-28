---
description: Using tmpfs mounts
title: tmpfs 挂载
weight: 30
keywords: storage, persistence, data persistence, tmpfs
aliases:
  - /engine/admin/volumes/tmpfs/
  - /storage/tmpfs/
---

[卷](volumes.md)和[绑定挂载](bind-mounts.md)允许你在主机和容器之间共享文件，以便即使在容器停止后也能持久化数据。

如果你在 Linux 上运行 Docker，你还有第三个选择：tmpfs 挂载。当你使用 tmpfs 挂载创建容器时，容器可以在容器可写层之外创建文件。

与卷和绑定挂载相反，tmpfs 挂载是临时的，只持久化在主机内存中。当容器停止时，tmpfs 挂载会被移除，写入其中的文件不会被持久化。

tmpfs 挂载最适合用于你不希望数据在主机上或容器内持久化的情况。这可能是出于安全原因，或者是为了在应用程序需要写入大量非持久性状态数据时保护容器的性能。

> [!IMPORTANT]
> Docker 中的 tmpfs 挂载直接映射到 Linux 内核中的 [tmpfs](https://en.wikipedia.org/wiki/Tmpfs)。因此，临时数据可能会被写入交换文件，从而持久化到文件系统中。

## 在现有数据上挂载

如果你在容器中已存在文件或目录的目录中创建 tmpfs 挂载，则预先存在的文件会被挂载遮盖。这类似于在 Linux 主机上将文件保存到 `/mnt`，然后将 USB 驱动器挂载到 `/mnt`。`/mnt` 的内容会被 USB 驱动器的内容遮盖，直到 USB 驱动器被卸载。

对于容器，没有直接的方法来移除挂载以显示被遮盖的文件。最好的选择是重新创建不带该挂载的容器。

## tmpfs 挂载的限制

- 与卷和绑定挂载不同，你不能在容器之间共享 tmpfs 挂载。
- 此功能仅在 Linux 上运行 Docker 时可用。
- 在 tmpfs 上设置权限可能会导致它们在[容器重启后重置](https://github.com/docker/for-linux/issues/138)。在某些情况下，[设置 uid/gid](https://github.com/docker/compose/issues/3425#issuecomment-423091370) 可以作为解决方法。

## 语法

要使用 `docker run` 命令挂载 tmpfs，你可以使用 `--mount` 或 `--tmpfs` 标志。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>
$ docker run --tmpfs <mount-path>
```

通常，推荐使用 `--mount`。主要区别在于 `--mount` 标志更加明确。另一方面，`--tmpfs` 更简洁，并且允许你设置更多挂载选项，因此更加灵活。

`--tmpfs` 标志不能与 swarm 服务一起使用。你必须使用 `--mount`。

### --tmpfs 的选项

`--tmpfs` 标志由两个字段组成，用冒号字符 (`:`) 分隔。

```console
$ docker run --tmpfs <mount-path>[:opts]
```

第一个字段是要挂载到 tmpfs 的容器路径。第二个字段是可选的，允许你设置挂载选项。`--tmpfs` 的有效挂载选项包括：

| 选项         | 描述                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `ro`         | 创建只读 tmpfs 挂载。                                                            |
| `rw`         | 创建可读写 tmpfs 挂载（默认行为）。                                        |
| `nosuid`     | 阻止在执行期间使用 `setuid` 和 `setgid` 位。                    |
| `suid`       | 允许在执行期间使用 `setuid` 和 `setgid` 位（默认行为）。        |
| `nodev`      | 设备文件可以创建但没有功能（访问会导致错误）。            |
| `dev`        | 设备文件可以创建并且完全可用。                                       |
| `exec`       | 允许在挂载的文件系统中执行可执行二进制文件。                     |
| `noexec`     | 不允许在挂载的文件系统中执行可执行二进制文件。             |
| `sync`       | 文件系统的所有 I/O 都是同步进行的。                                           |
| `async`      | 文件系统的所有 I/O 都是异步进行的（默认行为）。                       |
| `dirsync`    | 文件系统内的目录更新是同步进行的。                            |
| `atime`      | 每次访问文件时更新文件访问时间。                                    |
| `noatime`    | 访问文件时不更新文件访问时间。                                |
| `diratime`   | 每次访问目录时更新目录访问时间。                         |
| `nodiratime` | 访问目录时不更新目录访问时间。                      |
| `size`       | 指定 tmpfs 挂载的大小，例如 `size=64m`。                             |
| `mode`       | 指定 tmpfs 挂载的文件模式（权限）（例如 `mode=1777`）。       |
| `uid`        | 指定 tmpfs 挂载所有者的用户 ID（例如 `uid=1000`）。           |
| `gid`        | 指定 tmpfs 挂载所有者的组 ID（例如 `gid=1000`）。          |
| `nr_inodes`  | 指定 tmpfs 挂载的最大 inode 数（例如 `nr_inodes=400k`）。 |
| `nr_blocks`  | 指定 tmpfs 挂载的最大块数（例如 `nr_blocks=1024`）。 |

```console {title="Example"}
$ docker run --tmpfs /data:noexec,size=1024,mode=1777
```

并非 Linux mount 命令中所有可用的 tmpfs 挂载功能都支持 `--tmpfs` 标志。如果你需要高级 tmpfs 选项或功能，可能需要使用特权容器或在 Docker 之外配置挂载。

> [!CAUTION]
> 使用 `--privileged` 运行容器会授予提升的权限，可能会将主机系统暴露于安全风险。仅在绝对必要时且在受信任的环境中使用此选项。

```console
$ docker run --privileged -it debian sh
/# mount -t tmpfs -o <options> tmpfs /data
```

### --mount 的选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由一个 `<key>=<value>` 元组组成。键的顺序不重要。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>[,<key>=<value>...]
```

`--mount type=tmpfs` 的有效选项包括：

| 选项                           | 描述                                                                                                            |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `destination`, `dst`, `target` | 要挂载到 tmpfs 的容器路径。                                                                                  |
| `tmpfs-size`                   | tmpfs 挂载的大小（以字节为单位）。如果未设置，tmpfs 卷的默认最大大小为主机总 RAM 的 50%。 |
| `tmpfs-mode`                   | tmpfs 的八进制文件模式。例如 `700` 或 `0770`。默认为 `1777` 或全局可写。                  |

```console {title="Example"}
$ docker run --mount type=tmpfs,dst=/app,tmpfs-size=21474836480,tmpfs-mode=1770
```

## 在容器中使用 tmpfs 挂载

要在容器中使用 `tmpfs` 挂载，使用 `--tmpfs` 标志，或使用带有 `type=tmpfs` 和 `destination` 选项的 `--mount` 标志。`tmpfs` 挂载没有 `source`。以下示例在 Nginx 容器中的 `/app` 创建一个 `tmpfs` 挂载。第一个示例使用 `--mount` 标志，第二个使用 `--tmpfs` 标志。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name tmptest \
  --mount type=tmpfs,destination=/app \
  nginx:latest
```

通过查看 `docker inspect` 输出的 `Mounts` 部分来验证挂载是 `tmpfs` 挂载：

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

通过查看 `docker inspect` 输出的 `Mounts` 部分来验证挂载是 `tmpfs` 挂载：

```console
$ docker inspect tmptest --format '{{ json .Mounts }}'
{"/app":""}
```

{{< /tab >}}
{{< /tabs >}}

停止并删除容器：

```console
$ docker stop tmptest
$ docker rm tmptest
```

## 后续步骤

- 了解[卷](volumes.md)
- 了解[绑定挂载](bind-mounts.md)
- 了解[存储驱动程序](/engine/storage/drivers/)
