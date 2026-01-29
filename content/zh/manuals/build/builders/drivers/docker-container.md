--driver-opt=[key=value,...]
container

下表描述了您可以传递给 `--driver-opt` 的可用驱动程序特定选项：

| 参数 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `image`          | 字符串  |                  | 设置容器使用的 BuildKit 镜像。                                                                      |
| `memory`         | 字符串  |                  | 设置容器可以使用的内存量。                                                                       |
| `memory-swap`    | 字符串  |                  | 设置容器的内存交换限制。                                                                          |
| `cpu-quota`      | 字符串  |                  | 对容器施加 CPU CFS 配额。                                                                              |
| `cpu-period`     | 字符串  |                  | 设置容器的 CPU CFS 调度周期。                                                                   |
| `cpu-shares`     | 字符串  |                  | 配置容器的 CPU 权重（相对权重）。                                                              |
| `cpuset-cpus`    | 字符串  |                  | 限制容器可以使用的 CPU 核心集。                                                                     |
| `cpuset-mems`    | 字符串  |                  | 限制容器可以使用的 CPU 内存节点集。                                                              |
| `default-load`   | 布尔值 | `false`          | 自动将镜像加载到 Docker Engine 镜像库。                                                            |
| `network`        | 字符串  |                  | 设置容器的网络模式。                                                                               |
| `cgroup-parent`  | 字符串  | `/docker/buildx` | 如果 Docker 使用 "cgroupfs" 驱动程序，则设置容器的 cgroup 父级。                                      |
| `restart-policy` | 字符串  | `unless-stopped` | 设置容器的 [重启策略](/manuals/engine/containers/start-containers-automatically.md#使用重启策略)。      |
| `env.<key>`      | 字符串  |                  | 在容器中将环境变量 `key` 设置为指定的 `value`。                                         |

在配置容器的资源限制之前，请阅读有关 [配置容器的运行时资源约束](/engine/containers/resource_constraints/) 的内容。

## 用法

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

`docker-container` 驱动程序支持缓存持久化，因为它将所有的 BuildKit 状态和相关缓存存储在一个专用的 Docker 卷中。

为了持久化 `docker-container` 驱动程序的缓存，即使在使用 `docker buildx rm` 和 `docker buildx create` 重新创建驱动程序之后，您也可以在销毁构建器时使用 `--keep-state` 标志：

例如，创建一个名为 `container` 的构建器，然后在保留状态的情况下将其移除：

```console
# 设置一个构建器
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT              STATUS   BUILDKIT PLATFORMS
container *     docker-container
  container0    desktop-linux                running  v0.10.5  linux/amd64
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# 在保留状态的情况下移除构建器
$ docker buildx rm --keep-state container
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# 使用相同名称新创建的驱动程序将拥有之前驱动程序的所有状态！
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
```

## QEMU

`docker-container` 驱动程序支持使用 [QEMU](https://www.qemu.org/)（用户模式）来构建非原生平台。使用 `--platform` 标志指定您想要构建的架构。

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
> 使用 QEMU 进行模拟可能比原生构建慢得多，特别是对于编译以及压缩或解压缩等计算密集型任务。

## 自定义网络

您可以自定义构建器容器使用的网络。如果您需要为构建使用特定网络，这将非常有用。

例如，让我们 [创建一个名为 `foonet` 的网络](/reference/cli/docker/network/create.md)：

```console
$ docker network create foonet
```

现在创建一个使用此网络的 [`docker-container` 构建器](/reference/cli/docker/buildx/create.md)：

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "network=foonet"
```

启动并 [检查 `mybuilder`](/reference/cli/docker/buildx/inspect.md)：

```console
$ docker buildx inspect --bootstrap
```

[检查构建器容器](/reference/cli/docker/inspect.md) 并查看正在使用哪个网络：

```console
$ docker inspect buildx_buildkit_mybuilder0 --format={{.NetworkSettings.Networks}}
map[foonet:0xc00018c0c0]
```

## 延伸阅读

有关 Docker 容器驱动程序的更多信息，请参阅 [buildx 参考](/reference/cli/docker/buildx/create.md#driver)。
