---
description: 使用 prune 命令删除未使用的资源来释放磁盘空间
keywords: pruning, prune, images, volumes, containers, networks, disk, administration,
  garbage collection
title: 清理未使用的 Docker 对象
aliases:
- /engine/admin/pruning/
- /config/pruning/
---

Docker 对清理未使用的对象（通常称为"垃圾回收"）采取保守的方法，
例如镜像、容器、卷和网络。这些对象通常不会被删除，除非你明确要求
Docker 这样做。这可能导致 Docker 使用额外的磁盘空间。对于每种类型的
对象，Docker 提供了一个 `prune` 命令。此外，你可以使用 `docker
system prune` 一次性清理多种类型的对象。本主题展示
如何使用这些 `prune` 命令。

## 清理镜像

`docker image prune` 命令允许你清理未使用的镜像。默认情况下，
`docker image prune` 只清理_悬空_镜像。悬空镜像
是指没有标签且没有被任何容器引用的镜像。要删除
悬空镜像：

```console
$ docker image prune

WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
```

要删除所有未被现有容器使用的镜像，使用 `-a`
标志：

```console
$ docker image prune -a

WARNING! This will remove all images without at least one container associated to them.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示你确认是否继续。要跳过提示，使用 `-f` 或
`--force` 标志。

你可以使用 `--filter` 标志和过滤表达式来限制清理哪些镜像。例如，只考虑创建时间超过 24
小时的镜像：

```console
$ docker image prune -a --filter "until=24h"
```

还有其他可用的过滤表达式。请参阅
[`docker image prune` 参考](/reference/cli/docker/image/prune.md)
了解更多示例。

## 清理容器

当你停止一个容器时，它不会自动删除，除非你启动它时
使用了 `--rm` 标志。要查看 Docker 主机上的所有容器，包括
已停止的容器，使用 `docker ps -a`。你可能会惊讶于存在多少容器，
特别是在开发系统上！已停止容器的可写层
仍然占用磁盘空间。要清理这些，你可以使用 `docker container
prune` 命令。

```console
$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示你确认是否继续。要跳过提示，使用 `-f` 或
`--force` 标志。

默认情况下，所有已停止的容器都会被删除。你可以使用
`--filter` 标志限制范围。例如，以下命令只删除
停止时间超过 24 小时的容器：

```console
$ docker container prune --filter "until=24h"
```

还有其他可用的过滤表达式。请参阅
[`docker container prune` 参考](/reference/cli/docker/container/prune.md)
了解更多示例。

## 清理卷

卷可以被一个或多个容器使用，并占用 Docker
主机上的空间。卷永远不会自动删除，因为这样做可能会销毁
数据。

```console
$ docker volume prune

WARNING! This will remove all volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示你确认是否继续。要跳过提示，使用 `-f` 或
`--force` 标志。

默认情况下，所有未使用的卷都会被删除。你可以使用
`--filter` 标志限制范围。例如，以下命令只删除
没有标记 `keep` 标签的卷：

```console
$ docker volume prune --filter "label!=keep"
```

还有其他可用的过滤表达式。请参阅
[`docker volume prune` 参考](/reference/cli/docker/volume/prune.md)
了解更多示例。

## 清理网络

Docker 网络不会占用太多磁盘空间，但它们会创建 `iptables`
规则、桥接网络设备和路由表条目。要清理这些东西，
你可以使用 `docker network prune` 来清理没有被
任何容器使用的网络。

```console
$ docker network prune

WARNING! This will remove all networks not used by at least one container.
Are you sure you want to continue? [y/N] y
```

默认情况下，会提示你确认是否继续。要跳过提示，使用 `-f` 或
`--force` 标志。

默认情况下，所有未使用的网络都会被删除。你可以使用
`--filter` 标志限制范围。例如，以下命令只删除
创建时间超过 24 小时的网络：

```console
$ docker network prune --filter "until=24h"
```

还有其他可用的过滤表达式。请参阅
[`docker network prune` 参考](/reference/cli/docker/network/prune.md)
了解更多示例。

## 清理所有内容

`docker system prune` 命令是一个快捷方式，可以清理镜像、容器
和网络。默认情况下不会清理卷，你必须为 `docker system prune` 指定
`--volumes` 标志才能清理卷。

```console
$ docker system prune

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - unused build cache

Are you sure you want to continue? [y/N] y
```

要同时清理卷，添加 `--volumes` 标志：

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

默认情况下，会提示你确认是否继续。要跳过提示，使用 `-f` 或
`--force` 标志。

默认情况下，所有未使用的容器、网络和镜像都会被删除。你可以
使用 `--filter` 标志限制范围。例如，以下命令
删除创建时间超过 24 小时的项目：

```console
$ docker system prune --filter "until=24h"
```

还有其他可用的过滤表达式。请参阅
[`docker system prune` 参考](/reference/cli/docker/system/prune.md)
了解更多示例。
