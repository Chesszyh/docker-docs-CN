---
description: 使用绑定挂载 (bind mounts)
title: 绑定挂载 (Bind mounts)
weight: 20
keywords: storage, persistence, data persistence, mounts, bind mounts, 存储, 持久化, 挂载, 绑定挂载
alias:
  - /engine/admin/volumes/bind-mounts/
  - /storage/bind-mounts/
---


当您使用绑定挂载 (bind mount) 时，主机的网络上的文件或目录会被挂载到容器中。相比之下，当您使用卷 (volume) 时，会在主机上的 Docker 存储目录中创建一个新目录，并由 Docker 管理该目录的内容。

## 何时使用绑定挂载

绑定挂载适用于以下类型的用例：

- 在 Docker 主机上的开发环境与容器之间共享源代码或构建制品。

- 当您想在容器中创建或生成文件，并将文件持久化到主机的文件系统中时。

- 将配置文件从主机共享到容器。这就是 Docker 默认向容器提供 DNS 解析的方式，通过将主机的 `/etc/resolv.conf` 挂载到每个容器中。

绑定挂载也可用于构建：您可以将主机上的源代码绑定挂载到构建容器中，以对项目进行测试、lint 或编译。

## 在现有数据上进行绑定挂载

如果您将文件或目录绑定挂载到容器中已存在文件或目录的目录中，则预先存在的文件会被该挂载遮蔽。这类似于如果您在 Linux 主机上将文件保存到 `/mnt` 中，然后将 USB 驱动器挂载到 `/mnt` 中。在卸载 USB 驱动器之前，`/mnt` 的内容将被 USB 驱动器的内容遮蔽。

对于容器，没有直接的方法来移除挂载以再次显示被遮蔽的文件。最好的选择是在没有该挂载的情况下重新创建容器。

## 注意事项和限制

- 默认情况下，绑定挂载对主机上的文件具有写权限。

  使用绑定挂载的一个副作用是，您可以通过在容器中运行的进程更改主机文件系统，包括创建、修改或删除重要的系统文件或目录。这种能力可能会产生安全影响。例如，它可能会影响主机系统上的非 Docker 进程。

  您可以使用 `readonly` 或 `ro` 选项来防止容器写入挂载。

- 绑定挂载是创建到 Docker 守护进程主机的，而不是客户端。

  如果您使用的是远程 Docker 守护进程，则无法在容器中创建绑定挂载来访问客户端机器上的文件。

  对于 Docker Desktop，守护进程运行在 Linux 虚拟机内部，而不是直接在原生主机上。Docker Desktop 具有内置机制，可以透明地处理绑定挂载，允许您与虚拟机中运行的容器共享原生主机的文件系统路径。

- 带有绑定挂载的容器与主机紧密耦合。

  绑定挂载依赖于主机文件系统具有可用的特定目录结构。这种依赖性意味着，如果带有绑定挂载的容器在没有相同目录结构的不同主机上运行，可能会失败。

## 语法

要创建绑定挂载，您可以使用 `--mount` 或 `--volume` 标志。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>
$ docker run --volume <host-path>:<container-path>
```

通常，首选 `--mount`。主要区别在于 `--mount` 标志更加明确，并支持所有可用选项。

如果您使用 `--volume` 来绑定挂载 Docker 主机上尚不存在的文件或目录，Docker 会自动为您在主机上创建该目录。它始终被创建为一个目录。

如果主机上不存在指定的挂载路径，`--mount` 不会自动创建目录。相反，它会产生一个错误：

```console
$ docker run --mount type=bind,src=/dev/noexist,dst=/mnt/foo alpine
docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.
```

### --mount 的选项

`--mount` 标志由多个键值对组成，由逗号分隔，每个键值对由一个 `<key>=<value>` 元组组成。键的顺序并不重要。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>[,<key>=<value>...]
```

`--mount type=bind` 的有效选项包括：

| 选项                           | 描述                                                                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------|
| `source`, `src`                | 主机上文件或目录的位置。这可以是绝对路径或相对路径。                    |
| `destination`, `dst`, `target` | 文件或目录在容器中挂载的路径。必须是绝对路径。                     |
| `readonly`, `ro`               | 如果存在，则导致绑定挂载以 [只读方式挂载到容器中](#use-a-read-only-bind-mount)。 |
| `bind-propagation`             | 如果存在，则更改 [挂载传播 (bind propagation)](#configure-bind-propagation)。                                        |

```console {title="示例"}
$ docker run --mount type=bind,src=.,dst=/project,ro,bind-propagation=rshared
```

### --volume 的选项

`--volume` 或 `-v` 标志由三个字段组成，由冒号 (`:`) 分隔。字段必须按正确的顺序排列。

```console
$ docker run -v <host-path>:<container-path>[:opts]
```

第一个字段是主机上要绑定挂载到容器的路径。第二个字段是文件或目录在容器中挂载的路径。

第三个字段是可选的，是一个由逗号分隔的选项列表。带有绑定挂载的 `--volume` 的有效选项包括：

| 选项                 | 描述                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------|
| `readonly`, `ro`     | 如果存在，则导致绑定挂载以 [只读方式挂载到容器中](#use-a-read-only-bind-mount)。    |
| `z`, `Z`             | 配置 SELinux 标签。参见 [配置 SELinux 标签](#configure-the-selinux-label)                       |
| `rprivate` (默认)    | 为此挂载将挂载传播设置为 `rprivate`。参见 [配置挂载传播](#configure-bind-propagation)。 |
| `private`            | 为此挂载将挂载传播设置为 `private`。参见 [配置挂载传播](#configure-bind-propagation)。  |
| `rshared`            | 为此挂载将挂载传播设置为 `rshared`。参见 [配置挂载传播](#configure-bind-propagation)。  |
| `shared`             | 为此挂载将挂载传播设置为 `shared`。参见 [配置挂载传播](#configure-bind-propagation)。   |
| `rslave`             | 为此挂载将挂载传播设置为 `rslave`。参见 [配置挂载传播](#configure-bind-propagation)。   |
| `slave`              | 为此挂载将挂载传播设置为 `slave`。参见 [配置挂载传播](#configure-bind-propagation)。    |

```console {title="示例"}
$ docker run -v .:/project:ro,rshared
```

## 使用绑定挂载启动容器

考虑这样一个案例：您有一个目录 `source`，当您构建源代码时，制品会保存到另一个目录 `source/target/` 中。您希望这些制品在容器的 `/app/` 处可用，并且您希望每次在开发主机上构建源代码时，容器都能访问到新的构建结果。使用以下命令将 `target/` 目录绑定挂载到容器的 `/app/` 处。在 `source` 目录内运行该命令。在 Linux 或 macOS 主机上，`$(pwd)` 子命令会扩展为当前工作目录。如果您使用的是 Windows，请参阅 [Windows 上的路径转换](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)。

以下 `--mount` 和 `-v` 示例产生相同的结果。除非您在运行第一个之后删除 `devtest` 容器，否则不能同时运行它们。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect devtest` 验证绑定挂载是否已正确创建。查找 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "",
        "RW": true,
        "Propagation": "rprivate"
    }
],
```

这显示了该挂载是一个 `bind` 挂载，显示了正确的源和目的地，显示了挂载是读写的，并且传播设置为 `rprivate`。

停止并移除容器：

```console
$ docker container rm -fv devtest
```

### 挂载到容器上的非空目录

如果您将目录绑定挂载到容器上的非空目录中，则该目录现有的内容会被绑定挂载遮蔽。这可能是有益的，例如当您想要在不构建新镜像的情况下测试应用程序的新版本时。然而，这也可能会让人感到意外，且此行为与 [卷 (volumes)](volumes.md) 的行为不同。

这个示例设计得比较极端，但它会将容器的 `/usr/` 目录内容替换为主机上的 `/tmp/` 目录。在大多数情况下，这将导致容器无法运行。

`--mount` 和 `-v` 示例具有相同的最终结果。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name broken-container \
  --mount type=bind,source=/tmp,target=/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name broken-container \
  -v /tmp:/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

{{< /tab >}}
{{< /tabs >}}

容器已创建但无法启动。将其移除：

```console
$ docker container rm broken-container
```

## 使用只读绑定挂载

对于某些开发应用程序，容器需要写入绑定挂载，以便将更改传播回 Docker 主机。在其他时候，容器只需要读取权限。

这个示例修改了前一个示例，但通过在容器内的挂载点之后将 `ro` 添加到 (默认情况下为空的) 选项列表中，将目录挂载为只读绑定挂载。如果存在多个选项，请用逗号分隔。

`--mount` 和 `-v` 示例具有相同的结果。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app,readonly \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:ro \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect devtest` 验证绑定挂载是否已正确创建。查找 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "ro",
        "RW": false,
        "Propagation": "rprivate"
    }
],
```

停止并移除容器：

```console
$ docker container rm -fv devtest
```

## 递归挂载

当您绑定挂载一个本身包含挂载的路径时，这些子挂载默认也会包含在绑定挂载中。此行为是可配置的，可以使用 `--mount` 的 `bind-recursive` 选项。此选项仅在 `--mount` 标志中受支持，而在 `-v` 或 `--volume` 中不受支持。

如果绑定挂载是只读的，Docker Engine 会尽力尝试也将子挂载设置为只读。这被称为递归只读挂载。递归只读挂载需要 Linux 内核版本 5.12 或更高。如果您运行的是较旧的内核版本，子挂载默认会自动挂载为读写。在低于 5.12 的内核版本上尝试使用 `bind-recursive=readonly` 选项将子挂载设置为只读，会导致错误。

`bind-recursive` 选项支持的值有：

| 值                  | 描述                                                                                                       |
| :------------------ | :---------------------------------------------------------------------------------------------------------------- |
| `enabled` (默认)    | 如果内核为 v5.12 或更高，只读挂载将以递归方式设置为只读。否则，子挂载为读写。 |
| `disabled`          | 子挂载被忽略 (不包含在绑定挂载中)。                                                           |
| `writable`          | 子挂载为读写。                                                                                         |
| `readonly`          | 子挂载为只读。需要内核 v5.12 或更高。                                                          |

## 配置挂载传播 (Bind propagation)

对于绑定挂载和卷，挂载传播默认为 `rprivate`。它仅对绑定挂载可配置，且仅在 Linux 主机上。挂载传播是一个高级主题，许多用户永远不需要配置它。

挂载传播是指在给定绑定挂载内创建的挂载是否可以传播到该挂载的副本。考虑一个挂载点 `/mnt`，它也挂载在 `/tmp` 上。传播设置控制 `/tmp/a` 上的挂载是否也可以在 `/mnt/a` 上可用。每个传播设置都有一个递归对应项。在递归的情况下，考虑 `/tmp/a` 也挂载为 `/foo`。传播设置控制 `/mnt/a` 和/或 `/tmp/a` 是否存在。

> [!NOTE]
> 挂载传播在 Docker Desktop 上不起作用。

| 传播设置            | 描述                                                                                                                                                                                                         |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `shared`            | 原始挂载的子挂载会暴露给副本挂载，副本挂载的子挂载也会传播到原始挂载。                                                                         |
| `slave`             | 类似于共享挂载，但仅在一个方向上。如果原始挂载暴露了一个子挂载，副本挂载可以看到它。但是，如果副本挂载暴露了一个子挂载，原始挂载无法看到它。 |
| `private`           | 挂载是私有的。其内部的子挂载不会暴露给副本挂载，副本挂载的子挂载也不会暴露给原始挂载。                                                               |
| `rshared`           | 与 shared 相同，但传播也扩展到嵌套在任何原始挂载点或副本挂载点内的挂载点，并从这些挂载点传播出来。                                                                            |
| `rslave`            | 与 slave 相同，但传播也扩展到嵌套在任何原始挂载点或副本挂载点内的挂载点，并从这些挂载点传播出来。                                                                             |
| `rprivate`          | 默认值。与 private 相同，意味着原始挂载点或副本挂载点内任何位置的挂载点都不会在任何方向上传播。                                                                  |

在为挂载点设置挂载传播之前，主机文件系统需要已经支持挂载传播。

有关挂载传播的更多信息，请参阅 [共享子树的 Linux 内核文档](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)。

以下示例将 `target/` 目录两次挂载到容器中，第二次挂载同时设置了 `ro` 选项和 `rslave` 挂载传播选项。

`--mount` 和 `-v` 示例具有相同的结果。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  --mount type=bind,source="$(pwd)"/target,target=/app2,readonly,bind-propagation=rslave \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  -v "$(pwd)"/target:/app2:ro,rslave \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

现在如果您创建 `/app/foo/`，`/app2/foo/` 也会存在。

## 配置 SELinux 标签

如果您使用 SELinux，可以添加 `z` 或 `Z` 选项来修改被挂载到容器中的主机文件或目录的 SELinux 标签。这会影响主机机器本身的文件或目录，并可能产生超出 Docker 范围的后果。

- `z` 选项表示绑定挂载内容在多个容器之间共享。
- `Z` 选项表示绑定挂载内容是私有的且不共享。

使用这些选项时要格外小心。使用 `Z` 选项绑定挂载 `/home` 或 `/usr` 等系统目录会使您的主机机器无法操作，您可能需要手动重新标记主机文件。

> [!IMPORTANT]
>
> 在将绑定挂载与服务配合使用时，SELinux 标签 (`:Z` 和 `:z`) 以及 `:ro` 会被忽略。详情请参见 [moby/moby #32579](https://github.com/moby/moby/issues/32579)。

此示例设置 `z` 选项以指定多个容器可以共享绑定挂载的内容：

无法使用 `--mount` 标志修改 SELinux 标签。

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:z \
  nginx:latest
```

## 在 Docker Compose 中使用绑定挂载

带有一个绑定挂载的单个 Docker Compose 服务如下所示：

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - type: bind
        source: ./static
        target: /opt/app/static
volumes:
  myapp:
```

有关在 Compose 中使用 `bind` 类型卷的更多信息，请参阅 [关于卷的 Compose 参考](/reference/compose-file/services.md#volumes) 和 [关于卷配置的 Compose 参考](/reference/compose-file/services.md#volumes)。

## 后续步骤

- 了解 [卷 (volumes)](./volumes.md)。
- 了解 [tmpfs 挂载 (tmpfs mounts)](./tmpfs.md)。
- 了解 [存储驱动程序 (storage drivers)](/engine/storage/drivers/)。
