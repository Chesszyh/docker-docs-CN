--- 
description: 了解如何创建、管理和使用卷 (volumes) 代替绑定挂载 (bind mounts) 来持久化 Docker 生成和使用的数据。
title: 卷 (Volumes)
weight: 10
keywords:
  docker compose volumes, docker volumes, docker compose volume, docker volume mount, docker mount volume, docker volume create, docker volume location, 卷, 卷挂载, 创建卷
---

卷 (Volumes) 是容器的持久化数据存储，由 Docker 创建和管理。您可以使用 `docker volume create` 命令显式创建卷，或者 Docker 可以在创建容器或服务期间创建卷。

当您创建卷时，它存储在 Docker 主机上的一个目录中。当您将卷挂载到容器时，挂载到容器中的正是这个目录。这类似于绑定挂载的工作方式，不同之处在于卷由 Docker 管理，并与主机的核心功能隔离。

## 何时使用卷

卷是持久化 Docker 容器生成和使用的数据的首选机制。虽然 [绑定挂载 (bind mounts)](bind-mounts.md) 依赖于主机的目录结构和操作系统，但卷完全由 Docker 管理。在以下用例中，卷是一个很好的选择：

- 卷比绑定挂载更容易备份或迁移。
- 您可以使用 Docker CLI 命令或 Docker API 来管理卷。
- 卷在 Linux 和 Windows 容器上均可工作。
- 卷可以更安全地在多个容器之间共享。
- 新卷可以由容器或构建预先填充其内容。
- 当您的应用程序需要高性能 I/O 时。

如果您需要从主机访问文件，卷不是一个好的选择，因为卷完全由 Docker 管理。如果您需要同时从容器和主机访问文件或目录，请使用 [绑定挂载 (bind mounts)](bind-mounts.md)。

卷通常比直接将数据写入容器更好，因为卷不会增加使用它的容器的大小。使用卷也更快；写入容器的可写层需要一个 [存储驱动程序 (storage driver)](/manuals/engine/storage/drivers/_index.md) 来管理文件系统。存储驱动程序使用 Linux 内核提供联合文件系统。与使用直接写入主机文件系统的卷相比，这种额外的抽象降低了性能。

如果您的容器生成非持久化的状态数据，请考虑使用 [tmpfs 挂载](tmpfs.md)，以避免将数据永久存储在任何地方，并通过避免写入容器的可写层来提高容器的性能。

卷使用 `rprivate` (递归私有) 挂载传播，并且卷的挂载传播不可配置。

## 卷的生命周期

卷的内容存在于给定容器的生命周期之外。当容器被销毁时，可写层也随之销毁。使用卷可以确保即使使用它的容器被移除，数据也会被持久化。

一个给定的卷可以同时挂载到多个容器中。当没有运行中的容器使用卷时，该卷对 Docker 仍然可用，并且不会自动移除。您可以使用 `docker volume prune` 移除未使用的卷。

## 在现有数据上挂载卷

如果您将 *非空卷* 挂载到容器中已存在文件或目录的目录中，则预先存在的文件会被该挂载遮蔽。这类似于如果您在 Linux 主机上将文件保存到 `/mnt` 中，然后将 USB 驱动器挂载到 `/mnt` 中。在卸载 USB 驱动器之前，`/mnt` 的内容将被 USB 驱动器的内容遮蔽。

对于容器，没有直接的方法来移除挂载以再次显示被遮蔽的文件。最好的选择是在没有该挂载的情况下重新创建容器。

如果您将 *空卷* 挂载到容器中已存在文件或目录的目录中，则默认情况下，这些文件或目录会被传播 (复制) 到卷中。同样，如果您启动一个容器并指定一个尚不存在的卷，系统会为您创建一个空卷。这是预先填充另一个容器所需数据的良好方式。

要防止 Docker 将容器中预先存在的文件复制到空卷中，请使用 `volume-nocopy` 选项，参见 [--mount 的选项](#options-for---mount)。

## 具名卷和匿名卷

卷可以是具名的或匿名的。匿名卷被分配一个随机名称，保证在给定的 Docker 主机内是唯一的。就像具名卷一样，匿名卷即使在移除使用它们的容器后也会持久存在，除非您在创建容器时使用了 `--rm` 标志，在这种情况下，与容器关联的匿名卷将被销毁。参见 [移除匿名卷](volumes.md#remove-anonymous-volumes)。

如果您连续创建多个均使用匿名卷的容器，每个容器都会创建自己的卷。匿名卷不会在容器之间自动重用或共享。要在两个或更多容器之间共享匿名卷，您必须使用随机卷 ID 来挂载该匿名卷。

## 语法

要使用 `docker run` 命令挂载卷，您可以使用 `--mount` 或 `--volume` 标志。

```console
$ docker run --mount type=volume,src=<volume-name>,dst=<mount-path>
$ docker run --volume <volume-name>:<mount-path>
```

通常，首选 `--mount`。主要区别在于 `--mount` 标志更加明确，并支持所有可用选项。

如果您想执行以下操作，则必须使用 `--mount`：

- 指定 [卷驱动程序选项](#use-a-volume-driver)
- 挂载 [卷子目录](#mount-a-volume-subdirectory)
- 将卷挂载到 Swarm 服务中

### --mount 的选项

`--mount` 标志由多个键值对组成，由逗号分隔，每个键值对由一个 `<key>=<value>` 元组组成。键的顺序并不重要。

```console
$ docker run --mount type=volume[,src=<volume-name>],dst=<mount-path>[,<key>=<value>...]
```

`--mount type=volume` 的有效选项包括：

| 选项                           | 描述                                                                                                                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `source`, `src`                | 挂载的源。对于具名卷，这是卷的名称。对于匿名卷，省略此字段。                                                                                                       |
| `destination`, `dst`, `target` | 文件或目录在容器中挂载的路径。                                                                                                                                                               |
| `volume-subpath`               | 卷中要挂载到容器的子目录路径。在将卷挂载到容器之前，子目录必须已存在于卷中。参见 [挂载卷子目录](#mount-a-volume-subdirectory)。 |
| `readonly`, `ro`               | 如果存在，则导致卷以 [只读方式挂载到容器中](#use-a-read-only-volume)。                                                                                                                         |
| `volume-nocopy`                | 如果存在，当卷为空时，目的地的数据不会被复制到卷中。默认情况下，如果目标目的地已有内容，挂载空卷时内容会被复制到卷中。                                              |
| `volume-opt`                   | 可以指定多次，采用由选项名称及其值组成的键值对。                                                                                                                            |

```console {title="示例"}
$ docker run --mount type=volume,src=myvolume,dst=/data,ro,volume-subpath=/foo
```

### --volume 的选项

`--volume` 或 `-v` 标志由三个字段组成，由冒号 (`:`) 分隔。字段必须按正确的顺序排列。

```console
$ docker run -v [<volume-name>:]<mount-path>[:opts]
```

对于具名卷，第一个字段是卷的名称，在给定的主机上是唯一的。对于匿名卷，第一个字段被省略。第二个字段是文件或目录在容器中挂载的路径。

第三个字段是可选的，是一个由逗号分隔的选项列表。带有数据卷的 `--volume` 有效选项包括：

| 选项             | 描述                                                                                                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `readonly`, `ro` | 如果存在，则导致卷以 [只读方式挂载到容器中](#use-a-read-only-volume)。                                                                            |
| `volume-nocopy`  | 如果存在，当卷为空时，目的地的数据不会被复制到卷中。默认情况下，如果目标目的地已有内容，挂载空卷时内容会被复制到卷中。 |

```console {title="示例"}
$ docker run -v myvolume:/data:ro
```

## 创建和管理卷

与绑定挂载不同，您可以在任何容器的作用域之外创建和管理卷。

创建卷：

```console
$ docker volume create my-vol
```

列出卷：

```console
$ docker volume ls

local               my-vol
```

检查卷：

```console
$ docker volume inspect my-vol
[
    {
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
        "Name": "my-vol",
        "Options": {},
        "Scope": "local"
    }
]
```

移除卷：

```console
$ docker volume rm my-vol
```

## 使用卷启动容器

如果您使用尚不存在的卷启动容器，Docker 会为您创建该卷。以下示例将卷 `myvol2` 挂载到容器中的 `/app/`。

以下 `-v` 和 `--mount` 示例产生相同的结果。除非您在运行第一个之后删除 `devtest` 容器和 `myvol2` 卷，否则不能同时运行它们。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  --name devtest \
  --mount source=myvol2,target=/app \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  --name devtest \
  -v myvol2:/app \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect devtest` 验证 Docker 是否创建了卷并已正确挂载。查找 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "volume",
        "Name": "myvol2",
        "Source": "/var/lib/docker/volumes/myvol2/_data",
        "Destination": "/app",
        "Driver": "local",
        "Mode": "",
        "RW": true,
        "Propagation": ""
    }
],
```

这显示了该挂载是一个卷，显示了正确的源和目的地，并且挂载是读写的。

停止容器并移除卷。注意移除卷是一个单独的步骤。

```console
$ docker container stop devtest

$ docker container rm devtest

$ docker volume rm myvol2
```

## 在 Docker Compose 中使用卷

以下示例显示了带有一个卷的单个 Docker Compose 服务：

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - myapp:/home/node/app
volumes:
  myapp:
```

第一次运行 `docker compose up` 会创建一个卷。以后运行该命令时，Docker 会重用同一个卷。

您可以直接在 Compose 之外使用 `docker volume create` 创建卷，然后在 `compose.yaml` 中引用它，如下所示：

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - myapp:/home/node/app
volumes:
  myapp:
    external: true
```

有关在 Compose 中使用卷的更多信息，请参阅 Compose 规范中的 [卷 (Volumes)](/reference/compose-file/volumes.md) 部分。

### 启动带有卷的服务

当您启动服务并定义卷时，每个服务容器都使用自己的本地卷。如果您使用 `local` 卷驱动程序，任何容器都无法共享此数据。但是，某些卷驱动程序确实支持共享存储。

以下示例启动了一个具有四个副本的 `nginx` 服务，每个副本都使用一个名为 `myvol2` 的本地卷。

```console
$ docker service create -d \
  --replicas=4 \
  --name devtest-service \
  --mount source=myvol2,target=/app \
  nginx:latest
```

使用 `docker service ps devtest-service` 验证服务是否正在运行：

```console
$ docker service ps devtest-service

ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
4d7oz1j85wwn        devtest-service.1   nginx:latest        moby                Running             Running 14 seconds ago
```

您可以移除该服务以停止正在运行的任务：

```console
$ docker service rm devtest-service
```

移除服务不会移除服务创建的任何卷。移除卷是一个单独的步骤。

### 使用容器填充卷

如果您启动一个创建新卷的容器，并且容器在要挂载的目录 (如 `/app/`) 中已有文件或目录，Docker 会将该目录的内容复制到卷中。然后容器挂载并使用该卷，使用该卷的其他容器也可以访问预先填充的内容。

为了展示这一点，以下示例启动一个 `nginx` 容器，并使用容器 `/usr/share/nginx/html` 目录的内容填充新卷 `nginx-vol`。这是 Nginx 存储其默认 HTML 内容的地方。

`--mount` 和 `-v` 示例具有相同的最终结果。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  --mount source=nginx-vol,destination=/usr/share/nginx/html \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  -v nginx-vol:/usr/share/nginx/html \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

运行这两个示例中的任何一个后，运行以下命令来清理容器和卷。注意移除卷是一个单独的步骤。

```console
$ docker container stop nginxtest

$ docker container rm nginxtest

$ docker volume rm nginx-vol
```

## 使用只读卷

对于某些开发应用程序，容器需要写入绑定挂载，以便将更改传播回 Docker 主机。在其他时候，容器仅需要对数据的读取权限。多个容器可以挂载同一个卷。您可以同时将单个卷为某些容器挂载为 `read-write` (读写)，而为其他容器挂载为 `read-only` (只读)。

以下示例修改了前一个示例。它通过在容器内的挂载点之后将 `ro` 添加到 (默认情况下为空的) 选项列表中，将目录挂载为只读卷。如果存在多个选项，可以用逗号分隔它们。

`--mount` 和 `-v` 示例具有相同的结果。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  --mount source=nginx-vol,destination=/usr/share/nginx/html,readonly \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  -v nginx-vol:/usr/share/nginx/html:ro \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect nginxtest` 验证 Docker 是否已正确创建只读挂载。查找 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "volume",
        "Name": "nginx-vol",
        "Source": "/var/lib/docker/volumes/nginx-vol/_data",
        "Destination": "/usr/share/nginx/html",
        "Driver": "local",
        "Mode": "",
        "RW": false,
        "Propagation": ""
    }
],
```

停止并移除容器，然后移除卷。移除卷是一个单独的步骤。

```console
$ docker container stop nginxtest

$ docker container rm nginxtest

$ docker volume rm nginx-vol
```

## 挂载卷子目录

将卷挂载到容器时，您可以使用 `--mount` 标志的 `volume-subpath` 参数指定要使用的卷子目录。您指定的子目录必须在尝试将其挂载到容器之前已存在于卷中；如果它不存在，挂载将失败。

如果您只想与容器共享卷的特定部分，指定 `volume-subpath` 非常有用。例如，假设您有多个正在运行的容器，并且您希望将每个容器的日志存储在一个共享卷中。您可以为共享卷中的每个容器创建一个子目录，然后将该子目录挂载到容器。

以下示例创建一个 `logs` 卷并在该卷中启动子目录 `app1` 和 `app2`。然后启动两个容器，并将 `logs` 卷的一个子目录挂载到每个容器。此示例假设容器中的进程将其日志写入 `/var/log/app1` 和 `/var/log/app2`。

```console
$ docker volume create logs
$ docker run --rm \
  --mount src=logs,dst=/logs \
  alpine mkdir -p /logs/app1 /logs/app2
$ docker run -d \
  --name=app1 \
  --mount src=logs,dst=/var/log/app1,volume-subpath=app1 \
  app1:latest
$ docker run -d \
  --name=app2 \
  --mount src=logs,dst=/var/log/app2,volume-subpath=app2 \
  app2:latest
```

通过此设置，容器将其日志写入 `logs` 卷的单独子目录中。容器无法访问另一个容器的日志。

## 在机器之间共享数据

在构建容错应用程序时，您可能需要配置同一服务的多个副本来访问相同的文件。

![共享存储](images/volumes-shared-storage.webp)

在开发应用程序时，有几种方法可以实现这一点。一种是在您的应用程序中添加逻辑，将文件存储在 Amazon S3 等云对象存储系统上。另一种是使用支持将文件写入外部存储系统 (如 NFS 或 Amazon S3) 的驱动程序来创建卷。

卷驱动程序允许您将底层存储系统从应用程序逻辑中抽象出来。例如，如果您的服务使用具有 NFS 驱动程序的卷，您可以更新服务以使用不同的驱动程序 (例如在云中存储数据)，而无需更改应用程序逻辑。

## 使用卷驱动程序

当您使用 `docker volume create` 创建卷时，或者启动一个使用尚未创建的卷的容器时，您可以指定一个卷驱动程序。以下示例使用 `rclone/docker-volume-rclone` 卷驱动程序，首先在创建独立卷时使用，然后在启动一个创建新卷的容器时使用。

> [!NOTE]
> 
> 如果您的卷驱动程序接受以逗号分隔的列表作为选项，则必须转义来自外部 CSV 解析器的值。要转义 `volume-opt`，请用双引号 (`"`) 将其包围，并用单引号 (`'`) 将整个挂载参数包围。
> 
> 例如，`local` 驱动程序在 `o` 参数中接受挂载选项作为逗号分隔的列表。此示例展示了转义列表的正确方法。
> 
> ```console
> $ docker service create \
>  --mount 'type=volume,src=<VOLUME-NAME>,dst=<CONTAINER-PATH>,volume-driver=local,volume-opt=type=nfs,volume-opt=device=<nfs-server>:<nfs-path>,"volume-opt=o=addr=<nfs-address>,vers=4,soft,timeo=180,bg,tcp,rw"'
>  --name myservice \
>  <IMAGE>
> ```

### 初始设置

以下示例假设您有两个节点，第一个节点是 Docker 主机，可以通过 SSH 连接到第二个节点。

在 Docker 主机上，安装 `rclone/docker-volume-rclone` 插件：

```console
$ docker plugin install --grant-all-permissions rclone/docker-volume-rclone --aliases rclone
```

### 使用卷驱动程序创建卷

此示例将主机 `1.2.3.4` 上的 `/remote` 目录挂载到名为 `rclonevolume` 的卷中。每个卷驱动程序可能有零个或多个可配置选项，您可以使用 `-o` 标志指定其中每一个。

```console
$ docker volume create \
  -d rclone \
  --name rclonevolume \
  -o type=sftp \
  -o path=remote \
  -o sftp-host=1.2.3.4 \
  -o sftp-user=user \
  -o "sftp-password=$(cat file_containing_password_for_remote_host)"
```

该卷现在可以挂载到容器中。

### 启动使用卷驱动程序创建卷的容器

> [!NOTE]
> 
> 如果卷驱动程序要求您传递任何选项，则必须使用 `--mount` 标志挂载卷，而不能使用 `-v`。

```console
$ docker run -d \
  --name rclone-container \
  --mount type=volume,volume-driver=rclone,src=rclonevolume,target=/app,volume-opt=type=sftp,volume-opt=path=remote, volume-opt=sftp-host=1.2.3.4,volume-opt=sftp-user=user,volume-opt=-o "sftp-password=$(cat file_containing_password_for_remote_host)" \
  nginx:latest
```

### 创建一个创建 NFS 卷的服务

以下示例显示了如何在创建服务时创建 NFS 卷。它使用 `10.0.0.10` 作为 NFS 服务器，将 NFS 服务器上的 `/var/docker-nfs` 作为导出目录。请注意，指定的卷驱动程序是 `local`。

#### NFSv3

```console
$ docker service create -d \
  --name nfs-service \
  --mount 'type=volume,source=nfsvolume,target=/app,volume-driver=local,volume-opt=type=nfs,volume-opt=device=:/var/docker-nfs,volume-opt=o=addr=10.0.0.10' \
  nginx:latest
```

#### NFSv4

```console
$ docker service create -d \
    --name nfs-service \
    --mount 'type=volume,source=nfsvolume,target=/app,volume-driver=local,volume-opt=type=nfs,volume-opt=device=:/var/docker-nfs,"volume-opt=o=addr=10.0.0.10,rw,nfsvers=4,async"' \
    nginx:latest
```

### 创建 CIFS/Samba 卷

您可以直接在 Docker 中挂载 Samba 共享，而无需在主机上配置挂载点。

```console
$ docker volume create \
	--driver local \
	--opt type=cifs \
	--opt device=//uxxxxx.your-server.de/backup \
	--opt o=addr=uxxxxx.your-server.de,username=uxxxxxxx,password=*****,file_mode=0777,dir_mode=0777 \
	--name cif-volume
```

如果您指定主机名而不是 IP，则需要 `addr` 选项。这允许 Docker 执行主机名查找。

### 块存储设备 (Block storage devices)

您可以将块存储设备 (如外部驱动器或驱动器分区) 挂载到容器。以下示例展示了如何创建和使用文件作为块存储设备，以及如何将块设备挂载为容器卷。

> [!IMPORTANT]
> 
> 以下步骤仅为示例。这里阐述的解决方案不建议作为通用实践。除非您对自己正在做的事情充满信心，否则请勿尝试此方法。

#### 挂载块设备的工作原理

在底层，使用 `local` 存储驱动程序的 `--mount` 标志会调用 Linux 的 `mount` 系统调用，并原封不动地转发您传递给它的选项。Docker 不在 Linux 内核支持的原生挂载功能之上实现任何额外功能。

如果您熟悉 [Linux `mount` 命令](https://man7.org/linux/man-pages/man8/mount.8.html)，您可以将 `--mount` 选项视为按以下方式转发给 `mount` 命令：

```console
$ mount -t <mount.volume-opt.type> <mount.volume-opt.device> <mount.dst> -o <mount.volume-opts.o>
```

为了进一步解释，请考虑以下 `mount` 命令示例。此命令将 `/dev/loop5` 设备挂载到系统上的路径 `/external-drive`。

```console
$ mount -t ext4 /dev/loop5 /external-drive
```

从被运行的容器的角度来看，以下 `docker run` 命令实现了类似的结果。使用此 `--mount` 选项运行容器会建立挂载，就像您执行了前一个示例中的 `mount` 命令一样。

```console
$ docker run \
  --mount='type=volume,dst=/external-drive,volume-driver=local,volume-opt=device=/dev/loop5,volume-opt=type=ext4'
```

您不能直接在容器内部运行 `mount` 命令，因为容器无法访问 `/dev/loop5` 设备。这就是为什么 `docker run` 命令使用 `--mount` 选项的原因。

#### 示例：在容器中挂载块设备

以下步骤创建一个 `ext4` 文件系统并将其挂载到容器中。您的系统对文件系统的支持取决于您使用的 Linux 内核版本。

1. 创建一个文件并为其分配一些空间：

   ```console
   $ fallocate -l 1G disk.raw
   ```

2. 在 `disk.raw` 文件上构建文件系统：

   ```console
   $ mkfs.ext4 disk.raw
   ```

3. 创建一个回环设备 (loop device)：

   ```console
   $ losetup -f --show disk.raw
   /dev/loop5
   ```

   > [!NOTE]
   > 
   > `losetup` 创建一个临时的回环设备，该设备在系统重启后被移除，或者可以使用 `losetup -d` 手动移除。

4. 运行一个将回环设备挂载为卷的容器：

   ```console
   $ docker run -it --rm \
     --mount='type=volume,dst=/external-drive,volume-driver=local,volume-opt=device=/dev/loop5,volume-opt=type=ext4' \
     ubuntu bash
   ```

   当容器启动时，路径 `/external-drive` 将主机文件系统中的 `disk.raw` 文件作为块设备挂载。

5. 完成操作后，且设备已从容器卸载，请脱离回环设备以将其从主机系统中移除：

   ```console
   $ losetup -d /dev/loop5
   ```

## 备份、恢复或迁移数据卷

卷对于备份、恢复和迁移非常有用。使用 `--volumes-from` 标志创建一个挂载该卷的新容器。

### 备份卷

例如，创建一个名为 `dbstore` 的新容器：

```console
$ docker run -v /dbdata --name dbstore ubuntu /bin/bash
```

在下一个命令中：

- 启动一个新容器并挂载 `dbstore` 容器中的卷
- 将本地主机目录挂载为 `/backup`
- 传递一个命令，将 `dbdata` 卷的内容打包成 `/backup` 目录下的 `backup.tar` 文件。

```console
$ docker run --rm --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```

当命令执行完成且容器停止时，它就创建了 `dbdata` 卷的备份。

### 从备份中恢复卷

使用刚刚创建的备份，您可以将其恢复到同一个容器，或者恢复到您在别处创建的另一个容器。

例如，创建一个名为 `dbstore2` 的新容器：

```console
$ docker run -v /dbdata --name dbstore2 ubuntu /bin/bash
```

然后，在主机的网络容器的数据卷中解压备份文件：

```console
$ docker run --rm --volumes-from dbstore2 -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"
```

您可以使用这些技术使用您偏好的工具来自动执行备份、迁移和恢复测试。

## 移除卷

Docker 数据卷在您删除容器后仍然存在。有两种类型的卷需要考虑：

- 具名卷具有来自容器外部的特定源，例如 `awesome:/bar`。
- 匿名卷没有特定的源。因此，当容器被删除时，您可以指示 Docker Engine 守护进程将其移除。

### 移除匿名卷

要自动移除匿名卷，请使用 `--rm` 选项。例如，此命令创建一个匿名的 `/foo` 卷。当您移除容器时，Docker Engine 会移除 `/foo` 卷，但不会移除 `awesome` 卷。

```console
$ docker run --rm -v /foo -v awesome:/bar busybox top
```

> [!NOTE]
> 
> 如果另一个容器使用 `--volumes-from` 绑定了这些卷，则卷定义会被 *复制*，且匿名卷在第一个容器被移除后也会保留。

### 移除所有卷

要移除所有未使用的卷并释放空间：

```console
$ docker volume prune
```

## 后续步骤

- 了解 [绑定挂载 (bind mounts)](bind-mounts.md)。
- 了解 [tmpfs 挂载 (tmpfs mounts)](tmpfs.md)。
- 了解 [存储驱动程序 (storage drivers)](/engine/storage/drivers/)。
- 了解 [第三方卷驱动程序插件](/engine/extend/legacy_plugins/)
