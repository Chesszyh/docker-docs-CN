---
description: 通过使用 prune 命令移除未使用的资源来释放磁盘空间
keywords: pruning, prune, images, volumes, containers, networks, disk, administration, garbage collection, 清理, 镜像, 容器, 卷, 网络, 垃圾回收
title: 清理未使用的 Docker 对象
aliases:
- /engine/admin/pruning/
- /config/pruning/
---

Docker 在清理未使用的对象 (通常称为“垃圾回收”) (如镜像、容器、卷和网络) 时采取保守策略。除非您显式要求 Docker 执行此操作，否则通常不会移除这些对象。这可能会导致 Docker 占用额外的磁盘空间。对于每种类型的对象，Docker 都提供了一个 `prune` 命令。此外，您可以使用 `docker system prune` 一次性清理多种类型的对象。本主题展示如何使用这些 `prune` 命令。

## 清理镜像 (Prune images)

`docker image prune` 命令允许您清理未使用的镜像。默认情况下，`docker image prune` 仅清理 *悬空 (dangling)* 镜像。悬空镜像是指未打标签且未被任何容器引用的镜像。要移除悬空镜像：

```console
$ docker image prune

WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
```

要移除现有容器未使用的所有镜像，请使用 `-a` 标志：

```console
$ docker image prune -a

WARNING! This will remove all images without at least one container associated to them.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示您是否继续。要跳过提示，请使用 `-f` 或 `--force` 标志。

您可以使用带有 `--filter` 标志的过滤表达式来限制要清理的镜像。例如，仅考虑 24 小时前创建的镜像：

```console
$ docker image prune -a --filter "until=24h"
```

还提供其他过滤表达式。参见 [`docker image prune` 参考](/reference/cli/docker/image/prune.md) 以获取更多示例。

## 清理容器 (Prune containers)

当您停止容器时，除非您使用 `--rm` 标志启动它，否则它不会被自动移除。要查看 Docker 主机上的所有容器 (包括已停止的容器)，请使用 `docker ps -a`。您可能会惊讶于存在这么多容器，尤其是在开发系统中！已停止容器的可写层仍然占用磁盘空间。要清理这些内容，可以使用 `docker container prune` 命令。

```console
$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示您是否继续。要跳过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有停止的容器都将被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令仅移除超过 24 小时的已停止容器：

```console
$ docker container prune --filter "until=24h"
```

还提供其他过滤表达式。参见 [`docker container prune` 参考](/reference/cli/docker/container/prune.md) 以获取更多示例。

## 清理卷 (Prune volumes)

卷可以被一个或多个容器使用，并占用 Docker 主机上的空间。卷永远不会被自动移除，因为这样做可能会破坏数据。

```console
$ docker volume prune

WARNING! This will remove all volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示您是否继续。要跳过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有未使用的卷都将被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令仅移除未标记有 `keep` 标签的卷：

```console
$ docker volume prune --filter "label!=keep"
```

还提供其他过滤表达式。参见 [`docker volume prune` 参考](/reference/cli/docker/volume/prune.md) 以获取更多示例。

## 清理网络 (Prune networks)

Docker 网络不占用太多磁盘空间，但它们确实会创建 `iptables` 规则、网桥设备和路由表条目。要清理这些内容，可以使用 `docker network prune` 来清理任何容器都未使用的网络。

```console
$ docker network prune

WARNING! This will remove all networks not used by at least one container.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示您是否继续。要跳过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有未使用的网络都将被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令仅移除超过 24 小时的网络：

```console
$ docker network prune --filter "until=24h"
```

还提供其他过滤表达式。参见 [`docker network prune` 参考](/reference/cli/docker/network/prune.md) 以获取更多示例。

## 清理所有内容 (Prune everything)

`docker system prune` 命令是一个快捷方式，可以清理镜像、容器和网络。默认情况下不会清理卷，您必须为 `docker system prune` 指定 `--volumes` 标志才能清理卷。

```console
$ docker system prune

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - unused build cache

Are you sure you want to continue? [y/N] y
```

要同时清理卷，请添加 `--volumes` 标志：

```console
$ docker system prune --volumes

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all volumes not used by at least one container
        - all dangling images
        - all build cache

Are you sure you want to continue? [y/N] y
```

默认情况下，会提示您是否继续。要跳过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有未使用的容器、网络和镜像都将被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令移除超过 24 小时的项：

```console
$ docker system prune --filter "until=24h"
```

还提供其他过滤表达式。参见 [`docker system prune` 参考](/reference/cli/docker/system/prune.md) 以获取更多示例。
