---
title: Docker container 驱动
description: Docker container 驱动在容器镜像中运行 BuildKit。
keywords: build, buildx, driver, builder, docker-container
aliases:
  - /build/buildx/drivers/docker-container/
  - /build/building/drivers/docker-container/
  - /build/drivers/docker-container/
---

Docker container 驱动允许在专用的 Docker 容器中创建一个可管理和可定制的 BuildKit 环境。

与默认的 Docker 驱动相比，使用 Docker container 驱动有几个优势。例如：

- 指定要使用的自定义 BuildKit 版本。
- 构建多架构镜像，参见 [QEMU](#qemu)
- [缓存导入和导出](/manuals/build/cache/backends/_index.md)的高级选项

## 概要

运行以下命令来创建一个名为 `container` 的新构建器，该构建器使用 Docker container 驱动：

```console
$ docker buildx create \
  --name container \
  --driver=docker-container \
  --driver-opt=[key=value,...]
container
```

下表描述了可以传递给 `--driver-opt` 的特定于驱动的可用选项：

| 参数             | 类型    | 默认值           | 描述                                                                                                                            |
| ---------------- | ------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `image`          | String  |                  | 设置用于容器的 BuildKit 镜像。                                                                                                  |
| `memory`         | String  |                  | 设置容器可使用的内存量。                                                                                                        |
| `memory-swap`    | String  |                  | 设置容器的内存交换限制。                                                                                                        |
| `cpu-quota`      | String  |                  | 对容器施加 CPU CFS 配额。                                                                                                       |
| `cpu-period`     | String  |                  | 设置容器的 CPU CFS 调度周期。                                                                                                   |
| `cpu-shares`     | String  |                  | 配置容器的 CPU 份额（相对权重）。                                                                                               |
| `cpuset-cpus`    | String  |                  | 限制容器可使用的 CPU 核心集。                                                                                                   |
| `cpuset-mems`    | String  |                  | 限制容器可使用的 CPU 内存节点集。                                                                                               |
| `default-load`   | Boolean | `false`          | 自动将镜像加载到 Docker Engine 镜像存储。                                                                                       |
| `network`        | String  |                  | 设置容器的网络模式。                                                                                                            |
| `cgroup-parent`  | String  | `/docker/buildx` | 如果 Docker 使用 "cgroupfs" 驱动，则设置容器的 cgroup 父级。                                                                    |
| `restart-policy` | String  | `unless-stopped` | 设置容器的[重启策略](/manuals/engine/containers/start-containers-automatically.md#use-a-restart-policy)。                       |
| `env.<key>`      | String  |                  | 在容器中将环境变量 `key` 设置为指定的 `value`。                                                                                 |

在配置容器的资源限制之前，请阅读关于[为容器配置运行时资源约束](/engine/containers/resource_constraints/)的内容。

## 使用方法

当您运行构建时，Buildx 会拉取指定的 `image`（默认为 [`moby/buildkit`](https://hub.docker.com/r/moby/buildkit)）。当容器启动后，Buildx 会将构建提交到容器化的构建服务器。

```console
$ docker buildx build -t <image> --builder=container .
WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1
#1 pulling image moby/buildkit:buildx-stable-1 1.9s done
#1 creating container buildx_buildkit_container0
#1 creating container buildx_buildkit_container0 0.5s done
#1 DONE 2.4s
...
```

## 缓存持久化

`docker-container` 驱动支持缓存持久化，因为它将所有 BuildKit 状态和相关缓存存储到专用的 Docker 卷中。

要在使用 `docker buildx rm` 和 `docker buildx create` 重新创建驱动后仍保留 `docker-container` 驱动的缓存，您可以在销毁构建器时使用 `--keep-state` 标志：

例如，创建一个名为 `container` 的构建器，然后在保留状态的情况下删除它：

```console
# setup a builder
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT              STATUS   BUILDKIT PLATFORMS
container *     docker-container
  container0    desktop-linux                running  v0.10.5  linux/amd64
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# remove the builder while persisting state
$ docker buildx rm --keep-state container
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# the newly created driver with the same name will have all the state of the previous one!
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
```

## QEMU

`docker-container` 驱动支持使用 [QEMU](https://www.qemu.org/)（用户模式）来构建非原生平台的镜像。使用 `--platform` 标志指定您要构建的目标架构。

例如，为 `amd64` 和 `arm64` 构建 Linux 镜像：

```console
$ docker buildx build \
  --builder=container \
  --platform=linux/amd64,linux/arm64 \
  -t <registry>/<image> \
  --push .
```

> [!NOTE]
>
> 使用 QEMU 进行模拟可能比原生构建慢得多，尤其是对于计算密集型任务，如编译和压缩/解压缩。

## 自定义网络

您可以自定义构建器容器使用的网络。如果您需要在构建中使用特定网络，这会很有用。

例如，让我们[创建一个网络](/reference/cli/docker/network/create.md)，名为 `foonet`：

```console
$ docker network create foonet
```

现在创建一个将使用此网络的 [`docker-container` 构建器](/reference/cli/docker/buildx/create.md)：

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "network=foonet"
```

启动并[检查 `mybuilder`](/reference/cli/docker/buildx/inspect.md)：

```console
$ docker buildx inspect --bootstrap
```

[检查构建器容器](/reference/cli/docker/inspect.md)并查看正在使用的网络：

```console
$ docker inspect buildx_buildkit_mybuilder0 --format={{.NetworkSettings.Networks}}
map[foonet:0xc00018c0c0]
```

## 延伸阅读

有关 Docker container 驱动的更多信息，请参阅 [buildx 参考文档](/reference/cli/docker/buildx/create.md#driver)。
