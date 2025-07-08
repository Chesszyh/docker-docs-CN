  - net.core.somaxconn=1024
  - net.ipv4.tcp_syncookies=0
```

您只能使用内核中命名空间的 sysctls。Docker 不支持更改容器内同时修改主机系统的 sysctls。
有关支持的 sysctls 的概述，请参阅 [在运行时配置命名空间内核参数 (sysctls)](/reference/cli/docker/container/run.md#sysctl)。

### `tmpfs`

`tmpfs` 在容器内部挂载一个临时文件系统。它可以是单个值或列表。

```yml
tmpfs:
 - <path>
 - <path>:<options>
```

- `path`：容器内部挂载 tmpfs 的路径。
- `options`：tmpfs 挂载选项的逗号分隔列表。

可用选项：

- `mode`：设置文件系统权限。
- `uid`：设置拥有挂载 tmpfs 的用户 ID。
- `gid`：设置拥有挂载 tmpfs 的组 ID。

```yml
services:
  app:
    tmpfs:
      - /data:mode=755,uid=1009,gid=1009
      - /run
```

### `tty`

`tty` 配置服务的容器以 TTY 运行。这与使用 `-t` 或 `--tty` 标志运行容器相同。有关更多信息，请参阅 [分配伪 TTY](/reference/cli/docker/container/run.md#tty)。

支持的值为 `true` 或 `false`。

### `ulimits`

`ulimits` 覆盖容器的默认 `ulimits`。它可以指定为单个限制的整数，也可以指定为软/硬限制的映射。

```yml
ulimits:
  nproc: 65535
  nofile:
    soft: 20000
    hard: 40000
```

### `use_api_socket`

当设置 `use_api_socket` 时，容器能够通过 API 套接字与底层容器引擎交互。
您的凭据将挂载到容器内部，因此容器充当与容器引擎相关的命令的纯委托。
通常，容器运行的命令可以 `pull` 和 `push` 到您的注册表。

### `user`

`user` 覆盖用于运行容器进程的用户。默认值由镜像设置，例如 Dockerfile `USER`。如果未设置，则为 `root`。

### `userns_mode`

`userns_mode` 设置服务的用户命名空间。支持的值是平台特定的，并且可能取决于平台配置。

```yml
userns_mode: "host"
```

### `uts`

{{< summary-bar feature_name="Compose uts" >}}

`uts` 配置服务容器的 UTS 命名空间模式。如果未指定，则由运行时决定分配 UTS 命名空间（如果支持）。可用值为：

- `'host'`：导致容器使用与主机相同的 UTS 命名空间。

```yml
    uts: "host"
```

### `volumes`

{{% include "compose/services-volumes.md" %}}

以下示例显示了 `backend` 服务使用的命名卷 (`db-data`)，以及为单个服务定义的绑定挂载。

```yml
services:
  backend:
    image: example/backend
    volumes:
      - type: volume
        source: db-data
        target: /data
        volume:
          nocopy: true
          subpath: sub
      - type: bind
        source: /var/run/postgres/postgres.sock
        target: /var/run/postgres/postgres.sock

volumes:
  db-data:
```

有关 `volumes` 顶级元素的更多信息，请参阅 [卷](volumes.md)。

#### 短语法

短语法使用单个字符串，其中包含冒号分隔的值，以指定卷挂载 (`VOLUME:CONTAINER_PATH`) 或访问模式 (`VOLUME:CONTAINER_PATH:ACCESS_MODE`)。

- `VOLUME`：可以是托管容器的平台上的主机路径（绑定挂载）或卷名称。
- `CONTAINER_PATH`：卷在容器中挂载的路径。
- `ACCESS_MODE`：逗号分隔的选项列表：
  - `rw`：读写访问。如果未指定，则为默认值。
  - `ro`：只读访问。
  - `z`：SELinux 选项，表示绑定挂载主机内容在多个容器之间共享。
  - `Z`：SELinux 选项，表示绑定挂载主机内容是私有的，不与其他容器共享。

> [!NOTE]
>
> SELinux 重新标记绑定挂载选项在没有 SELinux 的平台上将被忽略。

> [!NOTE]
> 相对主机路径仅受部署到本地容器运行时的 Compose 支持。
> 这是因为相对路径是从 Compose 文件的父目录解析的，这仅适用于本地情况。当 Compose 部署到非本地
> 平台时，它会拒绝使用相对主机路径的 Compose 文件并报错。为了避免与命名卷的歧义，相对路径应始终以 `.` 或 `..` 开头。

> [!NOTE]
>
> 对于绑定挂载，如果主机上不存在源路径，短语法会在主机上创建该目录。这是为了与 `docker-compose` 旧版兼容。
> 可以通过使用长语法并将 `create_host_path` 设置为 `false` 来防止这种情况。

#### 长语法

长语法允许您配置短语法无法表达的附加字段。

- `type`：挂载类型。可以是 `volume`、`bind`、`tmpfs`、`image`、`npipe` 或 `cluster`
- `source`：挂载源，绑定挂载的主机路径，镜像挂载的 Docker 镜像引用，或在
  [顶级 `volumes` 键](volumes.md) 中定义的卷名称。不适用于 tmpfs 挂载。
- `target`：卷在容器中挂载的路径。
- `read_only`：将卷设置为只读的标志。
- `bind`：用于配置附加绑定选项：
  - `propagation`：用于绑定的传播模式。
  - `create_host_path`：如果主机上不存在源路径，则创建该目录。默认为 `true`。
  - `selinux`：SELinux 重新标记选项 `z`（共享）或 `Z`（私有）
- `volume`：配置附加卷选项：
  - `nocopy`：创建卷时禁用从容器复制数据的标志。
  - `subpath`：卷内要挂载的路径，而不是卷根目录。
- `tmpfs`：配置附加 tmpfs 选项：
  - `size`：tmpfs 挂载的大小（以字节为单位，可以是数字或字节单位）。
  - `mode`：tmpfs 挂载的文件模式，作为 Unix 权限位（八进制数）。在 Docker Compose 2.14.0 及更高版本中引入。
- `image`：配置附加镜像选项：
  - `subpath`：源镜像内要挂载的路径，而不是镜像根目录。在 [Docker Compose 2.35.0](https://docs.docker.com/compose/release-notes/#2350) 中可用。
- `consistency`：挂载的一致性要求。可用值是平台特定的。

> [!TIP]
>
> 正在处理大型仓库或 monorepos，或者文件系统不再与您的代码库一起扩展？
> Compose 现在利用 [同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 并自动为绑定挂载创建文件共享。
> 确保您已使用付费订阅登录 Docker，并在 Docker Desktop 的设置中启用了**访问实验性功能**和**使用 Compose 管理同步文件共享**。

### `volumes_from`

`volumes_from` 挂载来自另一个服务或容器的所有卷。您可以选择指定
只读访问 `ro` 或读写 `rw`。如果未指定访问级别，则使用读写访问。

您还可以通过使用 `container:` 前缀从不由 Compose 管理的容器挂载卷。

```yaml
volumes_from:
  - service_name
  - service_name:ro
  - container:container_name
  - container:container_name:rw
```

### `working_dir`

`working_dir` 覆盖容器的工作目录，该目录由镜像指定，例如 Dockerfile 的 `WORKDIR`。
