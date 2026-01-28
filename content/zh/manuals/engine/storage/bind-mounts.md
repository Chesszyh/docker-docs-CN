---
description: Using bind mounts
title: 绑定挂载
weight: 20
keywords: storage, persistence, data persistence, mounts, bind mounts
aliases:
  - /engine/admin/volumes/bind-mounts/
  - /storage/bind-mounts/
---

当你使用绑定挂载（bind mount）时，主机上的文件或目录会从主机挂载到容器中。相比之下，当你使用卷时，会在 Docker 主机的存储目录中创建一个新目录，由 Docker 管理该目录的内容。

## 何时使用绑定挂载

绑定挂载适用于以下类型的用例：

- 在 Docker 主机上的开发环境和容器之间共享源代码或构建产物。

- 当你希望在容器中创建或生成文件，并将文件持久化到主机文件系统时。

- 将配置文件从主机共享到容器。这就是 Docker 默认为容器提供 DNS 解析的方式，通过将主机的 `/etc/resolv.conf` 挂载到每个容器中。

绑定挂载也可用于构建：你可以将源代码从主机绑定挂载到构建容器中，以测试、lint 或编译项目。

## 在现有数据上进行绑定挂载

如果你将文件或目录绑定挂载到容器中已存在文件或目录的目录，则预先存在的文件会被挂载遮盖。这类似于在 Linux 主机上将文件保存到 `/mnt`，然后将 USB 驱动器挂载到 `/mnt`。`/mnt` 的内容会被 USB 驱动器的内容遮盖，直到 USB 驱动器被卸载。

对于容器，没有直接的方法来移除挂载以显示被遮盖的文件。最好的选择是重新创建不带该挂载的容器。

## 注意事项和约束

- 默认情况下，绑定挂载对主机上的文件具有写入权限。

  使用绑定挂载的一个副作用是，你可以通过在容器中运行的进程来更改主机文件系统，包括创建、修改或删除重要的系统文件或目录。这种能力可能会带来安全隐患。例如，它可能会影响主机系统上的非 Docker 进程。

  你可以使用 `readonly` 或 `ro` 选项来阻止容器写入挂载。

- 绑定挂载是在 Docker 守护进程主机上创建的，而不是客户端。

  如果你使用的是远程 Docker 守护进程，则无法创建绑定挂载来访问容器中客户端机器上的文件。

  对于 Docker Desktop，守护进程在 Linux 虚拟机内运行，而不是直接在本机主机上运行。Docker Desktop 具有内置机制，可以透明地处理绑定挂载，允许你将本机主机文件系统路径与在虚拟机中运行的容器共享。

- 使用绑定挂载的容器与主机紧密绑定。

  绑定挂载依赖于主机具有特定的目录结构可用。这种依赖性意味着如果在没有相同目录结构的其他主机上运行，使用绑定挂载的容器可能会失败。

## 语法

要创建绑定挂载，你可以使用 `--mount` 或 `--volume` 标志。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>
$ docker run --volume <host-path>:<container-path>
```

通常，推荐使用 `--mount`。主要区别在于 `--mount` 标志更加明确，并支持所有可用选项。

如果你使用 `--volume` 绑定挂载一个在 Docker 主机上尚不存在的文件或目录，Docker 会自动在主机上为你创建该目录。它始终被创建为目录。

如果指定的挂载路径在主机上不存在，`--mount` 不会自动创建目录。相反，它会产生错误：

```console
$ docker run --mount type=bind,src=/dev/noexist,dst=/mnt/foo alpine
docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.
```

### --mount 的选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由一个 `<key>=<value>` 元组组成。键的顺序不重要。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>[,<key>=<value>...]
```

`--mount type=bind` 的有效选项包括：

| 选项                           | 描述                                                                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `source`, `src`                | 主机上文件或目录的位置。可以是绝对路径或相对路径。                    |
| `destination`, `dst`, `target` | 文件或目录在容器中挂载的路径。必须是绝对路径。                     |
| `readonly`, `ro`               | 如果存在，会将绑定挂载以[只读方式挂载到容器中](#use-a-read-only-bind-mount)。 |
| `bind-propagation`             | 如果存在，更改[绑定传播](#configure-bind-propagation)。                                        |

```console {title="Example"}
$ docker run --mount type=bind,src=.,dst=/project,ro,bind-propagation=rshared
```

### --volume 的选项

`--volume` 或 `-v` 标志由三个字段组成，用冒号字符 (`:`) 分隔。这些字段必须按正确顺序排列。

```console
$ docker run -v <host-path>:<container-path>[:opts]
```

第一个字段是要绑定挂载到容器中的主机路径。第二个字段是文件或目录在容器中挂载的路径。

第三个字段是可选的，是一个逗号分隔的选项列表。绑定挂载的 `--volume` 有效选项包括：

| 选项                 | 描述                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `readonly`, `ro`     | 如果存在，会将绑定挂载以[只读方式挂载到容器中](#use-a-read-only-bind-mount)。    |
| `z`, `Z`             | 配置 SELinux 标签。参见[配置 SELinux 标签](#configure-the-selinux-label)                       |
| `rprivate`（默认）   | 为此挂载设置绑定传播为 `rprivate`。参见[配置绑定传播](#configure-bind-propagation)。 |
| `private`            | 为此挂载设置绑定传播为 `private`。参见[配置绑定传播](#configure-bind-propagation)。  |
| `rshared`            | 为此挂载设置绑定传播为 `rshared`。参见[配置绑定传播](#configure-bind-propagation)。  |
| `shared`             | 为此挂载设置绑定传播为 `shared`。参见[配置绑定传播](#configure-bind-propagation)。   |
| `rslave`             | 为此挂载设置绑定传播为 `rslave`。参见[配置绑定传播](#configure-bind-propagation)。   |
| `slave`              | 为此挂载设置绑定传播为 `slave`。参见[配置绑定传播](#configure-bind-propagation)。    |

```console {title="Example"}
$ docker run -v .:/project:ro,rshared
```

## 使用绑定挂载启动容器

假设你有一个 `source` 目录，当你构建源代码时，产物保存到另一个目录 `source/target/`。你希望产物在容器的 `/app/` 位置可用，并且每次在开发主机上构建源代码时，容器都能访问新的构建。使用以下命令将 `target/` 目录绑定挂载到容器的 `/app/`。从 `source` 目录内运行该命令。`$(pwd)` 子命令在 Linux 或 macOS 主机上展开为当前工作目录。
如果你在 Windows 上，另请参阅 [Windows 上的路径转换](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)。

以下 `--mount` 和 `-v` 示例产生相同的结果。除非在运行第一个示例后删除 `devtest` 容器，否则无法同时运行它们。

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

使用 `docker inspect devtest` 验证绑定挂载是否正确创建。查看 `Mounts` 部分：

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

这显示挂载是一个 `bind` 挂载，显示了正确的源和目标，显示挂载是可读写的，并且传播设置为 `rprivate`。

停止并删除容器：

```console
$ docker container rm -fv devtest
```

### 挂载到容器中的非空目录

如果你将目录绑定挂载到容器中的非空目录，该目录的现有内容会被绑定挂载遮盖。这可能是有益的，例如当你想测试应用程序的新版本而无需构建新镜像时。然而，这也可能令人意外，这种行为与[卷](volumes.md)的行为不同。

这个示例比较极端，但它用主机上的 `/tmp/` 目录替换了容器的 `/usr/` 目录的内容。在大多数情况下，这会导致容器无法运行。

`--mount` 和 `-v` 示例有相同的最终结果。

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

容器被创建但无法启动。删除它：

```console
$ docker container rm broken-container
```

## 使用只读绑定挂载

对于某些开发应用程序，容器需要写入绑定挂载，以便将更改传播回 Docker 主机。在其他时候，容器只需要读取访问权限。

此示例修改了之前的示例，通过在容器内的挂载点后面添加 `ro` 到（默认为空的）选项列表中，将目录挂载为只读绑定挂载。当存在多个选项时，用逗号分隔它们。

`--mount` 和 `-v` 示例有相同的结果。

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

使用 `docker inspect devtest` 验证绑定挂载是否正确创建。查看 `Mounts` 部分：

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

停止并删除容器：

```console
$ docker container rm -fv devtest
```

## 递归挂载

当你绑定挂载一个本身包含挂载的路径时，默认情况下这些子挂载也会包含在绑定挂载中。此行为是可配置的，使用 `--mount` 的 `bind-recursive` 选项。此选项仅支持 `--mount` 标志，不支持 `-v` 或 `--volume`。

如果绑定挂载是只读的，Docker 引擎会尽力尝试使子挂载也变为只读。这称为递归只读挂载。递归只读挂载需要 Linux 内核版本 5.12 或更高版本。如果你运行的是较旧的内核版本，默认情况下子挂载会自动以可读写方式挂载。在 5.12 之前的内核版本上尝试使用 `bind-recursive=readonly` 选项将子挂载设置为只读会导致错误。

`bind-recursive` 选项支持的值有：

| 值                  | 描述                                                                                                       |
| :------------------ | :---------------------------------------------------------------------------------------------------------------- |
| `enabled`（默认）   | 如果内核版本为 v5.12 或更高，只读挂载会递归设置为只读。否则，子挂载为可读写。 |
| `disabled`          | 忽略子挂载（不包含在绑定挂载中）。                                                           |
| `writable`          | 子挂载为可读写。                                                                                         |
| `readonly`          | 子挂载为只读。需要内核 v5.12 或更高版本。                                                          |

## 配置绑定传播

绑定传播（bind propagation）对于绑定挂载和卷默认都是 `rprivate`。它仅对绑定挂载可配置，并且仅在 Linux 主机上可配置。绑定传播是一个高级主题，许多用户永远不需要配置它。

绑定传播是指在给定绑定挂载内创建的挂载是否可以传播到该挂载的副本。考虑一个挂载点 `/mnt`，它也被挂载在 `/tmp` 上。传播设置控制 `/tmp/a` 上的挂载是否也在 `/mnt/a` 上可用。每个传播设置都有一个递归对应项。在递归的情况下，假设 `/tmp/a` 也被挂载为 `/foo`。传播设置控制 `/mnt/a` 和/或 `/tmp/a` 是否存在。

> [!NOTE]
> 挂载传播不适用于 Docker Desktop。

| 传播设置    | 描述                                                                                                                                                                                                         |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `shared`            | 原始挂载的子挂载会暴露给副本挂载，副本挂载的子挂载也会传播到原始挂载。                                                                         |
| `slave`             | 类似于共享挂载，但只是单向的。如果原始挂载暴露了一个子挂载，副本挂载可以看到它。然而，如果副本挂载暴露了一个子挂载，原始挂载看不到它。 |
| `private`           | 挂载是私有的。其中的子挂载不会暴露给副本挂载，副本挂载的子挂载也不会暴露给原始挂载。                                                               |
| `rshared`           | 与 shared 相同，但传播也扩展到和来自嵌套在任何原始或副本挂载点内的挂载点。                                                                            |
| `rslave`            | 与 slave 相同，但传播也扩展到和来自嵌套在任何原始或副本挂载点内的挂载点。                                                                             |
| `rprivate`          | 默认值。与 private 相同，意味着原始或副本挂载点内任何位置的挂载点都不会在任一方向传播。                                                                  |

在挂载点上设置绑定传播之前，主机文件系统需要已经支持绑定传播。

有关绑定传播的更多信息，请参阅[Linux 内核共享子树文档](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)。

以下示例将 `target/` 目录挂载到容器中两次，第二次挂载同时设置了 `ro` 选项和 `rslave` 绑定传播选项。

`--mount` 和 `-v` 示例有相同的结果。

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

现在如果你创建 `/app/foo/`，`/app2/foo/` 也会存在。

## 配置 SELinux 标签

如果你使用 SELinux，可以添加 `z` 或 `Z` 选项来修改被挂载到容器中的主机文件或目录的 SELinux 标签。这会影响主机上的文件或目录本身，并可能产生超出 Docker 范围的后果。

- `z` 选项表示绑定挂载内容在多个容器之间共享。
- `Z` 选项表示绑定挂载内容是私有的且不共享。

使用这些选项时要格外小心。使用 `Z` 选项绑定挂载系统目录（如 `/home` 或 `/usr`）会使你的主机无法操作，你可能需要手动重新标记主机文件。

> [!IMPORTANT]
>
> 当在服务中使用绑定挂载时，SELinux 标签（`:Z` 和 `:z`）以及 `:ro` 会被忽略。详情请参见 [moby/moby #32579](https://github.com/moby/moby/issues/32579)。

此示例设置 `z` 选项以指定多个容器可以共享绑定挂载的内容：

使用 `--mount` 标志无法修改 SELinux 标签。

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:z \
  nginx:latest
```

## 使用 Docker Compose 进行绑定挂载

使用绑定挂载的单个 Docker Compose 服务如下所示：

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

有关在 Compose 中使用 `bind` 类型卷的更多信息，请参阅 [Compose 卷参考](/reference/compose-file/services.md#volumes)和 [Compose 卷配置参考](/reference/compose-file/services.md#volumes)。

## 后续步骤

- 了解[卷](./volumes.md)。
- 了解 [tmpfs 挂载](./tmpfs.md)。
- 了解[存储驱动程序](/engine/storage/drivers/)。
