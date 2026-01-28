---
title: Services 顶层元素
description: 探索 services 顶层元素可以拥有的所有属性。
keywords: compose, compose specification, services, compose file reference
alias:
 - /compose/compose-file/05-services/
weight: 20
---

{{% include "compose/services.md" %}}

Compose 文件必须将 `services` 顶层元素声明为一个映射，其键是服务名称的字符串表示，其值是服务定义。服务定义包含应用于每个服务容器的配置。

每个服务还可以包含一个 `build` 部分，该部分定义了如何为服务创建 Docker 镜像。Compose 支持使用此服务定义构建 Docker 镜像。如果不使用，则忽略 `build` 部分，Compose 文件仍然被视为有效。构建支持是 Compose 规范的一个可选方面，并在 [Compose 构建规范](build.md) 文档中有详细描述。

每个服务都定义了运行其容器的运行时约束和要求。`deploy` 部分对这些约束进行分组，并允许平台调整部署策略，以最匹配容器的需求与可用资源。部署支持是 Compose 规范的一个可选方面，并在 [Compose 部署规范](deploy.md) 文档中有详细描述。如果未实现，则忽略 `deploy` 部分，Compose 文件仍然被视为有效。

## 示例

### 简单示例

以下示例演示了如何定义两个简单的服务，设置它们的镜像，映射端口，并使用 Docker Compose 配置基本的环境变量。

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: example
      POSTGRES_DB: exampledb
```

### 高级示例

在以下示例中，`proxy` 服务使用 Nginx 镜像，将本地 Nginx 配置文件挂载到容器中，暴露端口 `80` 并依赖于 `backend` 服务。

`backend` 服务从位于 `backend` 目录中的 Dockerfile 构建镜像，该 Dockerfile 设置为在 `builder` 阶段构建。

```yaml
services:
  proxy:
    image: nginx
    volumes:
      - type: bind
        source: ./proxy/nginx.conf
        target: /etc/nginx/conf.d/default.conf
        read_only: true
    ports:
      - 80:80
    depends_on:
      - backend

  backend:
    build:
      context: backend
      target: builder
```

要查看更多 Compose 文件示例，请浏览 [Awesome Compose 示例](https://github.com/docker/awesome-compose)。

## 属性

<!-- vale off(Docker.HeadingSentenceCase.yml) -->

### `annotations`

`annotations` 定义了容器的注解。`annotations` 可以使用数组或映射。

```yml
annotations:
  com.example.foo: bar
```

```yml
annotations:
  - com.example.foo=bar
```

### `attach`

{{< summary-bar feature_name="Compose attach" >}}

当 `attach` 被定义并设置为 `false` 时，Compose 不会收集服务日志，直到你显式请求。

默认服务配置为 `attach: true`。

### `build`

`build` 指定了从源代码创建容器镜像的构建配置，如 [Compose 构建规范](build.md) 中所定义。

### `blkio_config`

`blkio_config` 定义了一组配置选项，用于设置服务的块 I/O 限制。

```yml
services:
  foo:
    image: busybox
    blkio_config:
       weight: 300
       weight_device:
         - path: /dev/sda
           weight: 400
       device_read_bps:
         - path: /dev/sdb
           rate: '12mb'
       device_read_iops:
         - path: /dev/sdb
           rate: 120
       device_write_bps:
         - path: /dev/sdb
           rate: '1024k'
       device_write_iops:
         - path: /dev/sdb
           rate: 30
```

#### `device_read_bps`, `device_write_bps`

设置给定设备上读/写操作的每秒字节数限制。列表中的每一项必须有两个键：

- `path`：定义受影响设备的符号路径。
- `rate`：表示字节数的整数值或表示字节值的字符串。

#### `device_read_iops`, `device_write_iops`

设置给定设备上读/写操作的每秒操作数限制。列表中的每一项必须有两个键：

- `path`：定义受影响设备的符号路径。
- `rate`：表示每秒允许操作数的整数值。

#### `weight`

修改分配给服务的带宽相对于其他服务的比例。取值范围为 10 到 1000 的整数，默认值为 500。

#### `weight_device`

按设备微调带宽分配。列表中的每一项必须有两个键：

- `path`：定义受影响设备的符号路径。
- `weight`：10 到 1000 之间的整数值。

### `cpu_count`

`cpu_count` 定义服务容器可用的 CPU 数量。

### `cpu_percent`

`cpu_percent` 定义可用 CPU 的可用百分比。

### `cpu_shares`

`cpu_shares` 定义为一个整数值，表示服务容器相对于其他容器的 CPU 权重。

### `cpu_period`

`cpu_period` 配置当平台基于 Linux 内核时的 CPU CFS（完全公平调度器）周期。

### `cpu_quota`

`cpu_quota` 配置当平台基于 Linux 内核时的 CPU CFS（完全公平调度器）配额。

### `cpu_rt_runtime`

`cpu_rt_runtime` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒为单位的整数值，或者是 [duration（持续时间）](extension.md#specifying-durations)。

```yml
 cpu_rt_runtime: '400ms'
 cpu_rt_runtime: '95000'
```

### `cpu_rt_period`

`cpu_rt_period` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒为单位的整数值，或者是 [duration（持续时间）](extension.md#specifying-durations)。

```yml
 cpu_rt_period: '1400us'
 cpu_rt_period: '11000'
```

### `cpus`

`cpus` 定义分配给服务容器的（可能是虚拟的）CPU 数量。这是一个小数值。`0.000` 表示没有限制。

设置时，`cpus` 必须与 [部署规范](deploy.md#cpus) 中的 `cpus` 属性一致。

### `cpuset`

`cpuset` 定义允许执行的显式 CPU。可以是范围 `0-3` 或列表 `0,1`。

### `cap_add`

`cap_add` 指定额外的容器 [capabilities（能力）](https://man7.org/linux/man-pages/man7/capabilities.7.html) 为字符串。

```yaml
cap_add:
  - ALL
```

### `cap_drop`

`cap_drop` 指定要删除的容器 [capabilities（能力）](https://man7.org/linux/man-pages/man7/capabilities.7.html) 为字符串。

```yaml
cap_drop:
  - NET_ADMIN
  - SYS_ADMIN
```

### `cgroup`

{{< summary-bar feature_name="Compose cgroup" >}}

`cgroup` 指定要加入的 cgroup 命名空间。如果未设置，则由容器运行时决定选择使用哪个 cgroup 命名空间（如果支持）。

- `host`：在容器运行时 cgroup 命名空间中运行容器。
- `private`：在自己的私有 cgroup 命名空间中运行容器。

### `cgroup_parent`

`cgroup_parent` 指定容器的可选父 [cgroup](https://man7.org/linux/man-pages/man7/cgroups.7.html)。

```yaml
cgroup_parent: m-executor-abcd
```

### `command`

`command` 覆盖容器镜像声明的默认命令，例如 Dockerfile 的 `CMD`。

```yaml
command: bundle exec thin -p 3000
```

如果值为 `null`，则使用镜像中的默认命令。

如果值为 `[]`（空列表）或 `''`（空字符串），则忽略镜像声明的默认命令，换句话说，被覆盖为空。

> [!NOTE]
> 
> 与 Dockerfile 中的 `CMD` 指令不同，`command` 字段不会自动在镜像中定义的 [`SHELL`](/reference/dockerfile.md#shell-form) 指令的上下文中运行。如果你的 `command` 依赖于 shell 特定的功能，例如环境变量扩展，你需要显式地在 shell 中运行它。例如：
> 
> ```yaml
> command: /bin/sh -c 'echo "hello $$HOSTNAME"'
> ```

该值也可以是一个列表，类似于 [Dockerfile](/reference/dockerfile.md#exec-form) 使用的 [exec-form 语法](/reference/dockerfile.md#exec-form)。

### `configs`

`configs` 允许服务调整其行为，而无需重建 Docker 镜像。
只有通过 `configs` 属性显式授予访问权限时，服务才能访问配置。支持两种不同的语法变体。

如果 `config` 在平台上不存在或未在 Compose 文件的 [`configs` 顶层元素](configs.md) 中定义，Compose 将报告错误。

定义了两种配置语法：短语法和长语法。

你可以授予服务访问多个配置的权限，并且可以混合使用长语法和短语法。

#### 短语法

短语法变体仅指定配置名称。这授予容器对配置的访问权限，并将其作为文件挂载到服务容器的文件系统中。容器内挂载点的位置在 Linux 容器中默认为 `/<config_name>`，在 Windows 容器中默认为 `C:\<config_name>`。

以下示例使用短语法授予 `redis` 服务访问 `my_config` 和 `my_other_config` 配置的权限。`my_config` 的值设置为文件 `./my_config.txt` 的内容，而 `my_other_config` 定义为外部资源，这意味着它已经在平台中定义。如果外部配置不存在，部署将失败。

```yml
services:
  redis:
    image: redis:latest
    configs:
      - my_config
      - my_other_config
configs:
  my_config:
    file: ./my_config.txt
  my_other_config:
    external: true
```

#### 长语法

长语法提供了在服务的任务容器中如何创建配置的更细粒度的控制。

- `source`：平台中存在的配置名称。
- `target`：要挂载在服务的任务容器中的文件的路径和名称。如果未指定，默认为 `/<source>`。
- `uid` 和 `gid`：在服务的任务容器中拥有挂载的配置文件的数字 uid 或 gid。未指定时的默认值为 `USER`。
- `mode`：在服务的任务容器内挂载的文件的 [权限](https://wintelguy.com/permissions-calc.pl)，以八进制表示法。默认值为全局可读 (`0444`)。必须忽略可写位。可以设置可执行位。

以下示例将容器内的 `my_config` 名称设置为 `redis_config`，将模式设置为 `0440`（组可读），并将用户和组设置为 `103`。`redis` 服务没有访问 `my_other_config` 配置的权限。

```yml
services:
  redis:
    image: redis:latest
    configs:
      - source: my_config
        target: /redis_config
        uid: "103"
        gid: "103"
        mode: 0440
configs:
  my_config:
    external: true
  my_other_config:
    external: true
```

### `container_name`

`container_name` 是一个字符串，指定自定义容器名称，而不是默认生成的名称。

```yml
container_name: my-web-container
```

如果 Compose 文件指定了 `container_name`，Compose 不会将服务扩展到超过一个容器。尝试这样做会导致错误。

`container_name` 遵循 `[a-zA-Z0-9][a-zA-Z0-9_.-]+` 的正则表达式格式。

### `credential_spec`

`credential_spec` 配置托管服务帐户的凭证规范。

如果你的服务使用 Windows 容器，你可以为 `credential_spec` 使用 `file:` 和 `registry:` 协议。Compose 还支持用于自定义用例的其他协议。

`credential_spec` 必须采用 `file://<filename>` 或 `registry://<value-name>` 的格式。

```yml
credential_spec:
  file: my-credential-spec.json
```

当使用 `registry:` 时，凭证规范从守护进程主机的 Windows 注册表中读取。具有给定名称的注册表值必须位于：

    HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization\Containers\CredentialSpecs

以下示例从注册表中名为 `my-credential-spec` 的值加载凭证规范：

```yml
credential_spec:
  registry: my-credential-spec
```

#### gMSA 配置示例

为服务配置 gMSA 凭证规范时，你只需使用 `config` 指定凭证规范，如下例所示：

```yml
services:
  myservice:
    image: myimage:latest
    credential_spec:
      config: my_credential_spec

configs:
  my_credentials_spec:
    file: ./my-credential-spec.json
```

### `depends_on`

{{% include "compose/services-depends-on.md" %}}

#### 短语法

短语法变体仅指定依赖项的服务名称。服务依赖关系会导致以下行为：

- Compose 按依赖顺序创建服务。在以下示例中，`db` 和 `redis` 在 `web` 之前创建。

- Compose 按依赖顺序删除服务。在以下示例中，`web` 在 `db` 和 `redis` 之前删除。

简单示例：

```yml
services:
  web:
    build: .
    depends_on:
      - db
      - redis
  redis:
    image: redis
  db:
    image: postgres
```

Compose 保证在启动依赖服务之前已启动被依赖的服务。
Compose 等待依赖服务“就绪”后再启动被依赖的服务。

#### 长语法

长格式语法允许配置短格式无法表达的额外字段。

- `restart`：当设置为 `true` 时，Compose 在更新依赖服务后重启此服务。这适用于由 Compose 操作控制的显式重启，不包括容器死机后由容器运行时进行的自动重启。在 Docker Compose 版本 [2.17.0](/manuals/compose/releases/release-notes.md#2170) 中引入。

- `condition`：设置依赖被视为满足的条件
  - `service_started`：等同于前面描述的短语法
  - `service_healthy`：指定在启动被依赖的服务之前，依赖项预期处于“健康”状态（如 [`healthcheck`](#healthcheck) 所指示）。
  - `service_completed_successfully`：指定在启动被依赖的服务之前，依赖项预期成功运行完成。
- `required`：当设置为 `false` 时，如果依赖服务未启动或不可用，Compose 仅发出警告。如果未定义，`required` 的默认值为 `true`。在 Docker Compose 版本 [2.20.0](/manuals/compose/releases/release-notes.md#2200) 中引入。

服务依赖关系会导致以下行为：

- Compose 按依赖顺序创建服务。在以下示例中，`db` 和 `redis` 在 `web` 之前创建。

- Compose 等待标记为 `service_healthy` 的依赖项的健康检查通过。在以下示例中，`db` 在 `web` 创建之前预期为“健康”。

- Compose 按依赖顺序删除服务。在以下示例中，`web` 在 `db` 和 `redis` 之前删除。

```yml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres
```

Compose 保证在启动被依赖的服务之前启动依赖服务。
Compose 保证在启动被依赖的服务之前，标记为 `service_healthy` 的依赖服务是“健康”的。

### `deploy`

`deploy` 指定服务的部署和生命周期配置，如 [Compose 部署规范](deploy.md) 中所定义。

### `develop`

{{< summary-bar feature_name="Compose develop" >}}

`develop` 指定用于保持容器与源代码同步的开发配置，如 [开发部分](develop.md) 中所定义。

### `device_cgroup_rules`

`device_cgroup_rules` 定义此容器的设备 cgroup 规则列表。格式与 Linux 内核在 [Control Groups Device Whitelist Controller](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v1/devices.html) 中指定的格式相同。

```yml
device_cgroup_rules:
  - 'c 1:3 mr'
  - 'a 7:* rmw'
```

### `devices`

`devices` 以 `HOST_PATH:CONTAINER_PATH[:CGROUP_PERMISSIONS]` 的形式定义已创建容器的设备映射列表。

```yml
devices:
  - "/dev/ttyUSB0:/dev/ttyUSB0"
  - "/dev/sda:/dev/xvda:rwm"
```

`devices` 还可以依赖 [CDI](https://github.com/cncf-tags/container-device-interface) 语法让容器运行时选择设备：

```yml
devices:
  - "vendor1.com/device=gpu"
```

### `dns`

`dns` 定义要在容器网络接口配置上设置的自定义 DNS 服务器。它可以是单个值或列表。

```yml
dns: 8.8.8.8
```

```yml
dns:
  - 8.8.8.8
  - 9.9.9.9
```

### `dns_opt`

`dns_opt` 列出要传递给容器 DNS 解析器（Linux 上的 `/etc/resolv.conf` 文件）的自定义 DNS 选项。

```yml
dns_opt:
  - use-vc
  - no-tld-query
```

### `dns_search`

`dns_search` 定义要在容器网络接口配置上设置的自定义 DNS 搜索域。它可以是单个值或列表。

```yml
dns_search: example.com
```

```yml
dns_search:
  - dc1.example.com
  - dc2.example.com
```

### `domainname`

`domainname` 声明要用于服务容器的自定义域名。它必须是有效的 RFC 1123 主机名。

### `driver_opts`

{{< summary-bar feature_name="Compose driver opts" >}}

`driver_opts` 指定作为键值对的选项列表以传递给驱动程序。这些选项依赖于驱动程序。

```yml
services:
  app:
    networks:
      app_net:
        driver_opts:
          com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
```

有关更多信息，请参阅 [网络驱动程序文档](/manuals/engine/network/_index.md)。

### `entrypoint`

`entrypoint` 声明服务容器的默认入口点。
这会覆盖服务的 Dockerfile 中的 `ENTRYPOINT` 指令。

如果 `entrypoint` 不为 null，Compose 将忽略镜像中的任何默认命令，例如 Dockerfile 中的 `CMD` 指令。

另请参阅 [`command`](#command) 以设置或覆盖由 entrypoint 进程执行的默认命令。

在其短形式中，值可以定义为字符串：
```yml
entrypoint: /code/entrypoint.sh
```

或者，该值也可以是一个列表，方式类似于 [Dockerfile](https://docs.docker.com/reference/dockerfile/#cmd)：

```yml
entrypoint:
  - php
  - -d
  - zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so
  - -d
  - memory_limit=-1
  - vendor/bin/phpunit
```

如果值为 `null`，则使用镜像中的默认入口点。

如果值为 `[]`（空列表）或 `''`（空字符串），则忽略镜像声明的默认入口点，换句话说，被覆盖为空。

### `env_file`

{{% include "compose/services-env-file.md" %}}

```yml
env_file: .env
```

相对路径从 Compose 文件的父文件夹解析。由于绝对路径会阻止 Compose 文件可移植，因此当使用此类路径设置 `env_file` 时，Compose 会发出警告。

在 [`environment`](#environment) 部分声明的环境变量会覆盖这些值。即使这些值为空或未定义，这也是适用的。

`env_file` 也可以是一个列表。列表中的文件从上到下处理。对于在两个环境文件中指定的同一变量，列表中最后一个文件中的值有效。

```yml
env_file:
  - ./a.env
  - ./b.env
```

列表元素也可以声明为映射，从而允许你设置其他属性。

#### `required`

{{< summary-bar feature_name="Compose required" >}}

`required` 属性默认为 `true`。当 `required` 设置为 `false` 且 `.env` 文件丢失时，Compose 会静默忽略该条目。

```yml
env_file:
  - path: ./default.env
    required: true # default
  - path: ./override.env
    required: false
```

#### `format`

{{< summary-bar feature_name="Compose format" >}}

`format` 属性允许你为 `env_file` 使用替代文件格式。未设置时，`env_file` 将根据 [`Env_file` 格式](#env_file-format) 中概述的 Compose 规则进行解析。

`raw` 格式允许你使用带有 key=value 项目的 `env_file`，但 Compose 不会尝试解析该值以进行插值。这允许你按原样传递值，包括引号和 `$` 符号。

```yml
env_file:
  - path: ./default.env
    format: raw
```

#### `Env_file` 格式

`.env` 文件中的每一行必须采用 `VAR[=[VAL]]` 格式。适用以下语法规则：

- 以 `#` 开头的行作为注释处理并忽略。
- 空行被忽略。
- 未加引号和双引号 (`"`) 的值应用 [插值](interpolation.md)。
- 每一行代表一个键值对。值可以选加引号。
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
- 未加引号值的行内注释必须前面有一个空格。
  - `VAR=VAL # comment` -> `VAL`
  - `VAR=VAL# not a comment` -> `VAL# not a comment`
- 加引号值的行内注释必须跟在结束引号后面。
  - `VAR="VAL # not a comment"` -> `VAL # not a comment`
  - `VAR="VAL" # comment` -> `VAL`
- 单引号 (`'`) 值按字面意思使用。
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- 引号可以用 `\` 转义。
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- 双引号值中支持常见的 shell 转义序列，包括 `\n`、`\r`、`\t` 和 `\\`。
  - `VAR="some\tvalue"` -> `some  value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`

`VAL` 可以省略，在这种情况下，变量值是一个空字符串。
`=VAL` 可以省略，在这种情况下，变量未设置。

```bash
# Set Rails/Rack environment
RACK_ENV=development
VAR="quoted"
```

### `environment`

{{% include "compose/services-environment.md" %}}

环境变量可以通过单个键（没有值到等号）声明。在这种情况下，Compose 依赖于你来解析该值。如果值未解析，则该变量未设置并从服务容器环境中删除。

映射语法：

```yml
environment:
  RACK_ENV: development
  SHOW: "true"
  USER_INPUT:
```

数组语法：

```yml
environment:
  - RACK_ENV=development
  - SHOW=true
  - USER_INPUT
```

当同时为服务设置 `env_file` 和 `environment` 时，由 `environment` 设置的值具有优先权。

### `expose`

`expose` 定义 Compose 从容器暴露的（传入）端口或端口范围。这些端口必须可供链接的服务访问，并且不应发布到主机。只能指定内部容器端口。

语法是 `<portnum>/[<proto>]` 或 `<startport-endport>/[<proto>]` 用于端口范围。
当未显式设置时，使用 `tcp` 协议。

```yml
expose:
  - "3000"
  - "8000"
  - "8080-8085/tcp"
```

> [!NOTE]
> 
> 如果镜像的 Dockerfile 已经暴露了端口，即使你的 Compose 文件中未设置 `expose`，它对网络上的其他容器也是可见的。

### `extends`

`extends` 允许你在不同文件甚至完全不同的项目之间共享通用配置。使用 `extends`，你可以在一个地方定义一组通用的服务选项，并从任何地方引用它。你可以引用另一个 Compose 文件并选择你也想在自己的应用程序中使用的服务，并且能够根据自己的需要覆盖某些属性。

You可以在任何服务上将 `extends` 与其他配置键一起使用。`extends` 值必须是使用必需的 `service` 和可选的 `file` 键定义的映射。

```yaml
extends:
  file: common.yml
  service: webapp
```

- `service`：定义被引用为基础的服务名称，例如 `web` 或 `database`。
- `file`：定义该服务的 Compose 配置文件的位置。

#### 限制

当使用 `extends` 引用服务时，它可以声明对其他资源的依赖关系。这些依赖关系可以通过 `volumes`、`networks`、`configs`、`secrets`、`links`、`volumes_from` 或 `depends_on` 等属性显式定义。或者，依赖关系可以在 `ipc`、`pid` 或 `network_mode` 等命名空间声明中使用 `service:{name}` 语法引用另一个服务。

Compose 不会自动将这些引用的资源导入扩展模型。你有责任确保依赖于 extends 的模型中显式声明了所有必需的资源。

不支持带有 `extends` 的循环引用，当检测到时，Compose 会返回错误。

#### 查找引用的服务

`file` 值可以是：

- 不存在。
  这表示正在引用同一 Compose 文件中的另一个服务。
- 文件路径，可以是：
  - 相对路径。此路径被视为相对于主 Compose 文件位置的相对路径。
  - 绝对路径。

`service` 表示的服务必须存在于标识的被引用 Compose 文件中。
如果出现以下情况，Compose 将返回错误：

- 未找到 `service` 表示的服务。
- 未找到 `file` 表示的 Compose 文件。

#### 合并服务定义

两个服务定义（当前 Compose 文件中的主定义和由 `extends` 指定的被引用定义）按以下方式合并：

- 映射：主服务定义的映射中的键覆盖被引用服务定义的映射中的键。未覆盖的键按原样包含。
- 序列：项目组合成一个新的序列。保留元素的顺序，引用的项目在先，主项目在后。
- 标量：主服务定义中的键优先于被引用的键。

##### 映射

以下键应被视为映射：`annotations`、`build.args`、`build.labels`、`build.extra_hosts`、`deploy.labels`、`deploy.update_config`、`deploy.rollback_config`、`deploy.restart_policy`、`deploy.resources.limits`、`environment`、`healthcheck`、`labels`、`logging.options`、`sysctls`、`storage_opt`、`extra_hosts`、`ulimits`。

适用于 `healthcheck` 的一个例外是，除非被引用的映射也指定了 `disable: true`，否则主映射不能指定 `disable: true`。在这种情况下，Compose 返回错误。
例如，以下输入：

```yaml
services:
  common:
    image: busybox
    environment:
      TZ: utc
      PORT: 80
  cli:
    extends:
      service: common
    environment:
      PORT: 8080
```

为 `cli` 服务生成以下配置。如果使用数组语法，也会产生相同的输出。

```yaml
environment:
  PORT: 8080
  TZ: utc
image: busybox
```

`blkio_config.device_read_bps`、`blkio_config.device_read_iops`、`blkio_config.device_write_bps`、`blkio_config.device_write_iops`、`devices` 和 `volumes` 下的项目也被视为映射，其中键是容器内的目标路径。

例如，以下输入：

```yaml
services:
  common:
    image: busybox
    volumes:
      - common-volume:/var/lib/backup/data:rw
  cli:
    extends:
      service: common
    volumes:
      - cli-volume:/var/lib/backup/data:ro
```

为 `cli` 服务生成以下配置。请注意，挂载路径现在指向新的卷名称，并且应用了 `ro` 标志。

```yaml
image: busybox
volumes:
- cli-volume:/var/lib/backup/data:ro
```

如果被引用的服务定义包含 `extends` 映射，则其下的项目将简单地复制到新的合并定义中。然后再次启动合并过程，直到没有剩余的 `extends` 键。

例如，以下输入：

```yaml
services:
  base:
    image: busybox
    user: root
  common:
    image: busybox
    extends:
      service: base
  cli:
    extends:
      service: common
```

为 `cli` 服务生成以下配置。这里，`cli` 服务从 `common` 服务获取 `user` 键，而 `common` 服务又从 `base` 服务获取此键。

```yaml
image: busybox
user: root
```

##### 序列

以下键应被视为序列：`cap_add`、`cap_drop`、`configs`、`deploy.placement.constraints`、`deploy.placement.preferences`、`deploy.reservations.generic_resources`、`device_cgroup_rules`、`expose`、`external_links`、`ports`、`secrets`、`security_opt`。
删除合并产生的任何重复项，以便序列仅包含唯一元素。

例如，以下输入：

```yaml
services:
  common:
    image: busybox
    security_opt:
      - label=role:ROLE
  cli:
    extends:
      service: common
    security_opt:
      - label=user:USER
```

为 `cli` 服务生成以下配置。

```yaml
image: busybox
security_opt:
- label=role:ROLE
- label=user:USER
```

如果使用列表语法，以下键也应被视为序列：`dns`、`dns_search`、`env_file`、`tmpfs`。与前面提到的序列字段不同，不会删除合并产生的重复项。

##### 标量

服务定义中任何其他允许的键都应被视为标量。

### `external_links`

`external_links` 将服务容器链接到 Compose 应用程序之外管理的常见。
`external_links` 定义要使用平台查找机制检索的现有服务名称。
可以指定 `SERVICE:ALIAS` 形式的别名。

```yml
external_links:
  - redis
  - database:mysql
  - database:postgresql
```

### `extra_hosts`

`extra_hosts` 将主机名映射添加到容器网络接口配置（Linux 为 `/etc/hosts`）。

#### 短语法

短语法在列表中使用纯字符串。值必须以 `HOSTNAME=IP` 的形式为其他主机设置主机名和 IP 地址。

```yml
extra_hosts:
  - "somehost=162.242.195.82"
  - "otherhost=50.31.209.229"
  - "myhostv6=::1"
```

IPv6 地址可以用方括号括起来，例如：

```yml
extra_hosts:
  - "myhostv6=[::1]"
```

首选分隔符 `=`，但也支持 `:`。在 Docker Compose 版本 [2.24.1](/manuals/compose/releases/release-notes.md#2241) 中引入。例如：

```yml
extra_hosts:
  - "somehost:162.242.195.82"
  - "myhostv6:::1"
```

#### 长语法

或者，`extra_hosts` 可以设置为主机名和 IP 之间的映射

```yml
extra_hosts:
  somehost: "162.242.195.82"
  otherhost: "50.31.209.229"
  myhostv6: "::1"
```

Compose 在容器的网络配置中创建一个包含 IP 地址和主机名的匹配条目，这意味着对于 Linux，`/etc/hosts` 会获得额外的行：

```console
162.242.195.82  somehost
50.31.209.229   otherhost
::1             myhostv6
```

### `gpus`

{{< summary-bar feature_name="Compose gpus" >}}

`gpus` 指定要为容器使用分配的 GPU 设备。这等同于具有隐式 `gpu` 能力的 [设备请求](deploy.md#devices)。

```yaml
services:
  model:
    gpus: 
      - driver: 3dfx
        count: 2
```

`gpus` 也可以设置为字符串 `all`，以将所有可用的 GPU 设备分配给容器。

```yaml
services:
  model:
    gpus: all
```

### `group_add`

`group_add` 指定容器内的用户必须所属的其他组（按名称或编号）。

一个有用的例子是当多个容器（作为不同用户运行）都需要读取或写入共享卷上的同一文件时。该文件可以由所有容器共享的组拥有，并在 `group_add` 中指定。

```yml
services:
  myservice:
    image: alpine
    group_add:
      - mail
```

在创建的容器内运行 `id` 必须显示用户属于 `mail` 组，如果未声明 `group_add`，情况则不会如此。

### `healthcheck`

{{% include "compose/services-healthcheck.md" %}}

有关 `HEALTHCHECK` 的更多信息，请参阅 [Dockerfile 参考](/reference/dockerfile.md#healthcheck)。

```yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost"]
  interval: 1m30s
  timeout: 10s
  retries: 3
  start_period: 40s
  start_interval: 5s
```

`interval`、`timeout`、`start_period` 和 `start_interval` [指定为持续时间](extension.md#specifying-durations)。在 Docker Compose 版本 [2.20.2](/manuals/compose/releases/release-notes.md#2202) 中引入

`test` 定义 Compose 运行以检查容器健康的命令。它可以是字符串或列表。如果是列表，第一项必须是 `NONE`、`CMD` 或 `CMD-SHELL`。
如果是字符串，则等同于指定 `CMD-SHELL` 后跟该字符串。

```yml
# Hit the local web app
test: ["CMD", "curl", "-f", "http://localhost"]
```

使用 `CMD-SHELL` 使用容器的默认 shell（Linux 为 `/bin/sh`）运行配置为字符串的命令。以下两种形式是等效的：

```yml
test: ["CMD-SHELL", "curl -f http://localhost || exit 1"]
```

```yml
test: curl -f https://localhost || exit 1
```

`NONE` 禁用健康检查，主要用于禁用服务镜像设置的 Healthcheck Dockerfile 指令。或者，可以通过设置 `disable: true` 来禁用镜像设置的健康检查：

```yml
healthcheck:
  disable: true
```

### `hostname`

`hostname` 声明要用于服务容器的自定义主机名。它必须是有效的 RFC 1123 主机名。

### `image`

`image` 指定启动容器所使用的镜像。`image` 必须遵循开放容器规范 [可寻址镜像格式](https://github.com/opencontainers/org/blob/master/docs/docs/introduction/digests.md)，即 `[<registry>/][<project>/]<image>[:<tag>|@<digest>]`。

```yml
    image: redis
    image: redis:5
    image: redis@sha256:0ed5d5928d4737458944eb604cc8509e245c3e19d02ad83935398bc4b991aac7
    image: library/redis
    image: docker.io/library/redis
    image: my_private.registry:5000/redis
```

如果镜像在平台上不存在，Compose 会尝试根据 `pull_policy` 拉取它。
如果你也使用 [Compose 构建规范](build.md)，则还有用于控制拉取优先于从源构建镜像的替代选项，但拉取镜像是默认行为。

只要声明了 `build` 部分，就可以从 Compose 文件中省略 `image`。如果你不使用 Compose 构建规范，如果 Compose 文件中缺少 `image`，Compose 将无法工作。

### `init`

`init` 在容器内运行一个 init 进程 (PID 1)，该进程转发信号并回收进程。
将此选项设置为 `true` 以启用服务的此功能。

```yml
services:
  web:
    image: alpine:latest
    init: true
```

使用的 init 二进制文件是特定于平台的。

### `ipc`

`ipc` 配置服务容器设置的 IPC 隔离模式。

- `shareable`：为容器提供自己的私有 IPC 命名空间，并可能与其他容器共享。
- `service:{name}`：让容器加入另一个容器 (`shareable`) 的 IPC 命名空间。

```yml
    ipc: "shareable"
    ipc: "service:[service name]"
```

### `isolation`

`isolation` 指定容器的隔离技术。支持的值是特定于平台的。

### `labels`

`labels` 向容器添加元数据。你可以使用数组或映射。

建议你使用反向 DNS 表示法，以防止你的标签与其他软件使用的标签冲突。

```yml
labels:
  com.example.description: "Accounting webapp"
  com.example.department: "Finance"
  com.example.label-with-empty-value: ""
```

```yml
labels:
  - "com.example.description=Accounting webapp"
  - "com.example.department=Finance"
  - "com.example.label-with-empty-value"
```

Compose 使用规范标签创建容器：

- `com.docker.compose.project` 在 Compose 创建的所有资源上设置为用户项目名称
- `com.docker.compose.service` 在服务容器上设置为 Compose 文件中定义的服务名称

`com.docker.compose` 标签前缀是保留的。在 Compose 文件中指定带有此前缀的标签会导致运行时错误。

### `label_file`

{{< summary-bar feature_name="Compose label file" >}}

`label_file` 属性允许你从外部文件或文件列表加载服务标签。这提供了一种管理多个标签而不会使 Compose 文件混乱的便捷方法。

该文件使用键值格式，类似于 `env_file`。你可以将多个文件指定为列表。使用多个文件时，它们按在列表中出现的顺序进行处理。如果同一标签在多个文件中定义，则列表中最后一个文件中的值将覆盖前面的值。

```yaml
services:
  one:
    label_file: ./app.labels

  two:
    label_file:
      - ./app.labels
      - ./additional.labels
```

如果在 `label_file` 和 `labels` 属性中都定义了标签，则 [labels](#labels) 中的值优先。

### `links`

`links` 定义到另一个服务中的容器的网络链接。指定服务名称和链接别名 (`SERVICE:ALIAS`)，或仅指定服务名称。

```yml
web:
  links:
    - db
    - db:database
    - redis
```

链接服务的容器可以通过与别名相同的主机名访问，如果未指定别名，则通过服务名称访问。

不需要链接来启用服务通信。当未设置特定网络配置时，任何服务都可以在 `default` 网络上以该服务的名称访问任何其他服务。
如果服务指定了它们连接到的网络，`links` 不会覆盖网络配置。未连接到共享网络的服务无法相互通信。Compose 不会警告你配置不匹配。

链接还以与 [`depends_on`](#depends_on) 相同的方式表示服务之间的隐式依赖关系，因此它们确定服务启动的顺序。

### `logging`

`logging` 定义服务的日志记录配置。

```yml
logging:
  driver: syslog
  options:
    syslog-address: "tcp://192.168.0.42:123"
```

`driver` 名称指定服务容器的日志记录驱动程序。默认值和可用值是特定于平台的。驱动程序特定选项可以使用 `options` 设置为键值对。

### `mac_address`

> 适用于 Docker Compose 版本 2.24.0 及更高版本。

`mac_address` 设置服务容器的 Mac 地址。

> [!NOTE]
> 容器运行时可能会拒绝此值，例如 Docker Engine >= v25.0。在这种情况下，你应该改用 [networks.mac_address](#mac_address)。

### `mem_limit`

`mem_limit` 配置容器可以分配的内存限制，设置为表示 [字节值](extension.md#specifying-byte-values) 的字符串。

设置时，`mem_limit` 必须与 [部署规范](deploy.md#memory) 中的 `limits.memory` 属性一致。

### `mem_reservation`

`mem_reservation` 配置容器可以分配的内存预留，设置为表示 [字节值](extension.md#specifying-byte-values) 的字符串。

设置时，`mem_reservation` 必须与 [部署规范](deploy.md#memory) 中的 `reservations.memory` 属性一致。

### `mem_swappiness`

`mem_swappiness` 定义主机内核交换容器使用的匿名内存页的百分比，值在 0 到 100 之间。

- `0`：关闭匿名页面交换。
- `100`：将所有匿名页面设置为可交换。

默认值是特定于平台的。

### `memswap_limit`

`memswap_limit` 定义允许容器交换到磁盘的内存量。这是一个修饰属性，只有在同时也设置了 [`memory`](deploy.md#memory) 时才有意义。使用交换允许容器在耗尽所有可用内存时将多余的内存需求写入磁盘。对于频繁将内存交换到磁盘的应用程序，会有性能损失。

- 如果 `memswap_limit` 设置为正整数，则必须同时设置 `memory` 和 `memswap_limit`。`memswap_limit` 表示可以使用的内存和交换的总量，而 `memory` 控制非交换内存的使用量。因此，如果 `memory`="300m" 且 `memswap_limit`="1g"，则容器可以使用 300m 内存和 700m (1g - 300m) 交换。
- 如果 `memswap_limit` 设置为 0，则忽略该设置，并将该值视为未设置。
- 如果 `memswap_limit` 设置为与 `memory` 相同的值，并且 `memory` 设置为正整数，则容器无法访问交换。
- 如果 `memswap_limit` 未设置，并且设置了 `memory`，如果主机容器配置了交换内存，则容器可以使用与 `memory` 设置一样多的交换。例如，如果 `memory`="300m" 并且未设置 `memswap_limit`，则容器总共可以使用 600m 的内存和交换。
- 如果 `memswap_limit` 显式设置为 -1，则允许容器使用无限交换，最高可达主机系统上的可用量。

### models

{{< summary-bar feature_name="Compose models" >}}

`models` 定义服务在运行时应使用的 AI 模型。每个引用的模型必须在 [`models` 顶层元素](models.md) 下定义。

```yaml
services:
  short_syntax:
    image: app
    models:
      - my_model
  long_syntax:
    image: app
    models:
      my_model:
        endpoint_var: MODEL_URL
        model_var: MODEL
```

当服务链接到模型时，Docker Compose 会注入环境变量以将连接详细信息和模型标识符传递给容器。这允许应用程序在运行时动态定位并与模型通信，而无需硬编码值。

#### 长语法

长语法让你能够更好地控制环境变量名称。

- `endpoint_var` 设置保存模型运行器 URL 的环境变量的名称。
- `model_var` 设置保存模型标识符的环境变量的名称。

如果省略任何一个，Compose 会根据模型键使用以下规则自动生成环境变量名称：

 - 将模型键转换为大写
 - 将任何 '-' 字符替换为 '_'
 - 附加 `_URL` 用于端点变量

### `network_mode`

`network_mode` 设置服务容器的网络模式。

- `none`：关闭所有容器网络。
- `host`：让容器获得对主机网络接口的原始访问权限。
- `service:{name}`：通过引用服务名称让容器访问指定容器。
- `container:{name}`：通过引用容器 ID 让容器访问指定容器。

有关容器网络的更多信息，请参阅 [Docker Engine 文档](/manuals/engine/network/_index.md#container-networks)。

```yml
    network_mode: "host"
    network_mode: "none"
    network_mode: "service:[service name]"
```

设置后，不允许使用 [`networks`](#networks) 属性，Compose 将拒绝包含这两个属性的任何 Compose 文件。

### `networks`

{{% include "compose/services-networks.md" %}}

```yml
services:
  some-service:
    networks:
      - some-network
      - other-network
```
有关 `networks` 顶层元素的更多信息，请参阅 [网络](networks.md)。

### 隐式默认网络

如果 `networks` 为空或从 Compose 文件中缺失，Compose 会考虑该服务的隐式定义为连接到 `default` 网络：

```yml
services:
  some-service:
    image: foo
```
这个例子实际上等同于：

```yml
services:
  some-service:
    image: foo  
    networks:
      default: {}
```

如果你希望服务不连接到网络，必须设置 [`network_mode: none`](#network_mode)。

#### `aliases`

`aliases` 声明网络上服务的替代主机名。同一网络上的其他容器可以使用服务名称或别名连接到服务容器之一。

由于 `aliases` 是网络范围的，因此同一服务可以在不同网络上具有不同的别名。

> [!NOTE]
> 网络范围的别名可以由多个容器甚至多个服务共享。
> 如果是这样，则不保证名称解析到哪个容器。

```yml
services:
  some-service:
    networks:
      some-network:
        aliases:
          - alias1
          - alias3
      other-network:
        aliases:
          - alias2
```

在以下示例中，`frontend` 服务能够在 `back-tier` 网络上的主机名 `backend` 或 `database` 处访问 `backend` 服务。`monitoring` 服务能够在 `admin` 网络上的 `backend` 或 `mysql` 处访问同一个 `backend` 服务。

```yml
services:
  frontend:
    image: example/webapp
    networks:
      - front-tier
      - back-tier

  monitoring:
    image: example/monitoring
    networks:
      - admin

  backend:
    image: example/backend
    networks:
      back-tier:
        aliases:
          - database
      admin:
        aliases:
          - mysql

networks:
  front-tier: {}
  back-tier: {}
  admin: {}
```

### `interface_name`

{{< summary-bar feature_name="Compose interface-name" >}}

`interface_name` 允许你指定用于将服务连接到给定网络的网络接口名称。这确保了跨服务和网络的一致和可预测的接口命名。

```yaml
services:
  backend:
    image: alpine
    command: ip link show
    networks:
      back-tier:
        interface_name: eth0
```

运行示例 Compose 应用程序显示：

```console
backend-1  | 11: eth0@if64: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP 
```

#### `ipv4_address`, `ipv6_address`

加入网络时为服务容器指定静态 IP 地址。

[顶层 networks 部分](networks.md) 中的相应网络配置必须具有覆盖每个静态地址的子网配置的 `ipam` 属性。

```yml
services:
  frontend:
    image: example/webapp
    networks:
      front-tier:
        ipv4_address: 172.16.238.10
        ipv6_address: 2001:3984:3989::10

networks:
  front-tier:
    ipam:
      driver: default
      config:
        - subnet: "172.16.238.0/24"
        - subnet: "2001:3984:3989::/64"
```

#### `link_local_ips`

`link_local_ips` 指定本地链接 IP 列表。本地链接 IP 是属于众所周知的子网的特殊 IP，纯粹由操作员管理，通常取决于部署它们的架构。

示例：

```yml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net:
        link_local_ips:
          - 57.123.22.11
          - 57.123.22.13
networks:
  app_net:
    driver: bridge
```

#### `mac_address`

{{< summary-bar feature_name="Compose mac address" >}}

`mac_address` 设置服务容器在连接到此特定网络时使用的 Mac 地址。

#### `gw_priority`

{{< summary-bar feature_name="Compose gw priority" >}}

具有最高 `gw_priority` 的网络被选为服务容器的默认网关。
如果未指定，默认值为 0。

在以下示例中，`app_net_2` 将被选为默认网关。

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net_1:
      app_net_2:
        gw_priority: 1
      app_net_3:
networks:
  app_net_1:
  app_net_2:
  app_net_3:
```

#### `priority`

`priority` 指示 Compose 将服务容器连接到其网络的顺序。如果未指定，默认值为 0。

如果容器运行时接受服务级别的 `mac_address` 属性，则将其应用于具有最高 `priority` 的网络。在其他情况下，使用属性 `networks.mac_address`。

`priority` 不影响哪个网络被选为默认网关。请改用 [`gw_priority`](#gw_priority) 属性。

`priority` 不控制将网络连接添加到容器的顺序，它不能用于确定容器中的设备名称（`eth0` 等）。

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net_1:
        priority: 1000
      app_net_2:

      app_net_3:
        priority: 100
networks:
  app_net_1:
  app_net_2:
  app_net_3:
```

### `oom_kill_disable`

如果设置了 `oom_kill_disable`，Compose 会配置平台，以便在内存不足的情况下不会终止容器。

### `oom_score_adj`

`oom_score_adj` 调整平台在内存不足时终止容器的偏好。值必须在 -1000,1000 范围内。

### `pid`

`pid` 设置 Compose 创建的容器的 PID 模式。 
支持的值是特定于平台的。

### `pids_limit`

`pids_limit` 调整容器的 PID 限制。设置为 -1 表示无限制 PID。

```yml
pids_limit: 10
```

设置时，`pids_limit` 必须与 [部署规范](deploy.md#pids) 中的 `pids` 属性一致。

### `platform`

`platform` 定义服务容器运行的目标平台。它使用 `os[/arch[/variant]]` 语法。

`os`、`arch` 和 `variant` 的值必须符合 [OCI 镜像规范](https://github.com/opencontainers/image-spec/blob/v1.0.2/image-index.md) 使用的约定。

Compose 使用此属性来确定拉取哪个版本的镜像和/或在哪个平台上执行服务的构建。

```yml
platform: darwin
platform: windows/amd64
platform: linux/arm64/v8
```

### `ports`

{{% include "compose/services-ports.md" %}}

> [!NOTE]
> 
> 端口映射不得与 `network_mode: host` 一起使用。这样做会导致运行时错误，因为 `network_mode: host` 已经将容器端口直接暴露给主机网络，因此不需要端口映射。

#### 短语法

短语法是一个冒号分隔的字符串，用于设置主机 IP、主机端口和容器端口，形式如下：

`[HOST:]CONTAINER[/PROTOCOL]` 其中：

- `HOST` 是 `[IP:](port | range)`（可选）。如果未设置，则绑定到所有网络接口 (`0.0.0.0`)。
- `CONTAINER` 是 `port | range`。
- `PROTOCOL` 将端口限制为指定协议，`tcp` 或 `udp`（可选）。默认为 `tcp`。

端口可以是单个值或范围。`HOST` 和 `CONTAINER` 必须使用等效的范围。

你可以指定两个端口（`HOST:CONTAINER`），也可以仅指定容器端口。在后一种情况下，容器运行时会自动分配主机的任何未分配端口。

`HOST:CONTAINER` 应始终指定为（带引号的）字符串，以避免与 [YAML base-60 float](https://yaml.org/type/float.html) 冲突。

IPv6 地址可以用方括号括起来。

示例：

```yml
ports:
  - "3000"
  - "3000-3005"
  - "8000:8000"
  - "9090-9091:8080-8081"
  - "49100:22"
  - "8000-9000:80"
  - "127.0.0.1:8001:8001"
  - "127.0.0.1:5000-5010:5000-5010"  
  - "::1:6000:6000"   
  - "[::1]:6001:6001" 
  - "6060:6060/udp"    
```

> [!NOTE]
> 
> 如果容器引擎不支持主机 IP 映射，Compose 将拒绝 Compose 文件并忽略指定的主机 IP。

#### 长语法

长格式语法允许你配置短格式无法表达的额外字段。

- `target`：容器端口。
- `published`：公开暴露的端口。它定义为字符串，可以使用语法 `start-end` 设置为范围。这意味着实际端口被分配了设定范围内的剩余可用端口。
- `host_ip`：主机 IP 映射。如果未设置，则绑定到所有网络接口 (`0.0.0.0`)。
- `protocol`：端口协议（`tcp` 或 `udp`）。默认为 `tcp`。
- `app_protocol`：此端口使用的应用程序协议（TCP/IP 第 4 层/OSI 第 7 层）。这是可选的，可以用作提示，让 Compose 为其理解的协议提供更丰富的行为。在 Docker Compose 版本 [2.26.0](/manuals/compose/releases/release-notes.md#2260) 中引入。
- `mode`：指定如何在 Swarm 设置中发布端口。如果设置为 `host`，则在 Swarm 中的每个节点上发布端口。如果设置为 `ingress`，则允许在 Swarm 中的节点之间进行负载均衡。默认为 `ingress`。
- `name`：端口的人类可读名称，用于在服务中记录其用途。

```yml
ports:
  - name: web
    target: 80
    host_ip: 127.0.0.1
    published: "8080"
    protocol: tcp
    app_protocol: http
    mode: host

  - name: web-secured
    target: 443
    host_ip: 127.0.0.1
    published: "8083-9000"
    protocol: tcp
    app_protocol: https
    mode: host
```

### `post_start`

{{< summary-bar feature_name="Compose post start" >}}

`post_start` 定义了在容器启动后运行的一系列生命周期钩子。命令运行的确切时间无法保证。

- `command`：指定容器启动后运行的命令。此属性是必需的，你可以选择使用 shell 形式或 exec 形式。
- `user`：运行命令的用户。如果未设置，命令将以与主服务命令相同的用户运行。
- `privileged`：允许 `post_start` 命令以特权访问权限运行。
- `working_dir`：运行命令的工作目录。如果未设置，它将在与主服务命令相同的工作目录中运行。
- `environment`：专门为 `post_start` 命令设置环境变量。虽然命令继承了为服务主命令定义的环境变量，但此部分允许你添加新变量或覆盖现有变量。

```yml
services:
  test:
    post_start:
      - command: ./do_something_on_startup.sh
        user: root
        privileged: true
        environment:
          - FOO=BAR
```

有关更多信息，请参阅 [使用生命周期钩子](/manuals/compose/how-tos/lifecycle.md)。

### `pre_stop`

{{< summary-bar feature_name="Compose pre stop" >}}

`pre_stop` 定义了在容器停止之前运行的一系列生命周期钩子。如果容器自行停止或突然终止，这些钩子将不会运行。

配置等同于 [post_start](#post_start)。

### `privileged`

`privileged` 配置服务容器以提升的权限运行。支持和实际影响是特定于平台的。

### `profiles`

`profiles` 定义服务启用的一组命名配置文件。如果未分配，服务总是启动，但如果已分配，则只有在激活配置文件时才启动。

如果存在，`profiles` 遵循 `[a-zA-Z0-9][a-zA-Z0-9_.-]+` 的正则表达式格式。

```yml
services:
  frontend:
    image: frontend
    profiles: ["frontend"]

  phpmyadmin:
    image: phpmyadmin
    depends_on:
      - db
    profiles:
      - debug
```

### `provider`

{{< summary-bar feature_name="Compose provider services" >}}

`provider` 可用于定义 Compose 不会直接管理的服务。Compose 将服务生命周期委托给专用或第三方组件。

```yaml
  database:
    provider:
      type: awesomecloud
      options:
        type: mysql
        foo: bar  
  app:
    image: myapp 
    depends_on:
       - database
```

当 Compose 运行应用程序时，使用 `awesomecloud` 二进制文件来管理 `database` 服务设置。
依赖服务 `app` 接收以服务名称为前缀的附加环境变量，以便它可以访问资源。

为了说明，假设 `awesomecloud` 执行产生了变量 `URL` 和 `API_KEY`，`app` 服务使用环境变量 `DATABASE_URL` 和 `DATABASE_API_KEY` 运行。

当 Compose 停止应用程序时，使用 `awesomecloud` 二进制文件来管理 `database` 服务拆卸。

[这里](https://github.com/docker/compose/tree/main/docs/extension.md) 描述了 Compose 用于将服务生命周期委托给外部二进制文件的机制。

有关使用 `provider` 属性的更多信息，请参阅 [使用提供程序服务](/manuals/compose/how-tos/provider-services.md)。

### `type`

`type` 属性是必需的。它定义了 Compose 用于管理设置和拆卸生命周期事件的外部组件。

### `options`

`options` 特定于所选提供程序，并且不由 compose 规范验证。

### `pull_policy`

`pull_policy` 定义 Compose 在开始拉取镜像时做出的决策。可能的值有：

- `always`：Compose 总是从注册表中拉取镜像。
- `never`：Compose 不会从注册表中拉取镜像，而是依赖于平台缓存的镜像。
   如果没有缓存的镜像，则报告失败。
- `missing`：Compose 仅在平台缓存中不可用时才拉取镜像。
   如果你没有同时使用 [Compose 构建规范](build.md)，这是默认选项。
  为了向后兼容，`if_not_present` 被视为此值的别名。
- `build`：Compose 构建镜像。如果镜像已存在，Compose 会重建镜像。
- `daily`：如果上次拉取发生在 24 小时前，Compose 会检查注册表以获取镜像更新。
- `weekly`：如果上次拉取发生在 7 天前，Compose 会检查注册表以获取镜像更新。
- `every_<duration>`：如果上次拉取发生在 `<duration>` 之前，Compose 会检查注册表以获取镜像更新。持续时间可以用周 (`w`)、天 (`d`)、小时 (`h`)、分钟 (`m`)、秒 (`s`) 或这些的组合来表示。

```yaml
services:
  test:
    image: nginx
    pull_policy: every_12h
```

### `read_only`

`read_only` 配置服务容器以只读文件系统创建。

### `restart`

`restart` 定义平台在容器终止时应用的策略。

- `no`：默认重启策略。它在任何情况下都不会重启容器。
- `always`：该策略总是重启容器直到其被删除。
- `on-failure[:max-retries]`：如果退出代码指示错误，该策略会重启容器。
可选地，限制 Docker 守护进程尝试重启的次数。
- `unless-stopped`：该策略无论退出代码如何都会重启容器，但当服务停止或删除时停止重启。

```yml
    restart: "no"
    restart: always
    restart: on-failure
    restart: on-failure:3
    restart: unless-stopped
```

你可以在 Docker 运行参考页面的 [重启策略 (--restart)](/reference/cli/docker/container/run.md#restart) 部分找到有关重启策略的更多详细信息。

### `runtime`

`runtime` 指定用于服务容器的运行时。

例如，`runtime` 可以是 [OCI 运行时规范的实现](https://github.com/opencontainers/runtime-spec/blob/master/implementations.md) 的名称，例如 "runc"。

```yml
web:
  image: busybox:latest
  command: true
  runtime: runc
```

默认为 `runc`。要使用不同的运行时，请参阅 [替代运行时](/manuals/engine/daemon/alternative-runtimes.md)。

### `scale`

`scale` 指定为此服务部署的默认容器数量。
当两者都设置时，`scale` 必须与 [部署规范](deploy.md#replicas) 中的 `replicas` 属性一致。

### `secrets`

{{% include "compose/services-secrets.md" %}}

支持两种不同的语法变体；短语法和长语法。长语法和短语法的密钥可以在同一个 Compose 文件中使用。

如果密钥在平台上不存在或未在 Compose 文件的 [`secrets` 顶层部分](secrets.md) 中定义，Compose 将报告错误。

在顶层 `secrets` 中定义密钥不得暗示授予任何服务访问它的权限。
此类授予必须在服务规范中显式作为 [secrets](secrets.md) 服务元素。

#### 短语法

短语法变体仅指定密钥名称。这授予容器访问密钥的权限，并在容器内将其以只读方式挂载到 `/run/secrets/<secret_name>`。源名称和目标挂载点都设置为密钥名称。

以下示例使用短语法授予 `frontend` 服务访问 `server-certificate` 密钥的权限。`server-certificate` 的值设置为文件 `./server.cert` 的内容。

```yml
services:
  frontend:
    image: example/webapp
    secrets:
      - server-certificate
secrets:
  server-certificate:
    file: ./server.cert
```

#### 长语法

长语法提供了在服务容器中如何创建密钥的更细粒度的控制。

- `source`：平台中存在的密钥名称。
- `target`：要挂载在服务任务容器中 `/run/secrets/` 中的文件名，如果需要备用位置，则是文件的绝对路径。如果未指定，默认为 `source`。
- `uid` 和 `gid`：在服务任务容器中拥有 `/run/secrets/` 内文件的数字 uid 或 gid。默认值为 `USER`。
- `mode`：在服务任务容器中挂载到 `/run/secrets/` 的文件的 [权限](https://wintelguy.com/permissions-calc.pl)，以八进制表示法。
  默认值为全局可读权限 (模式 `0444`)。
  如果设置，必须忽略可写位。可以设置可执行位。

请注意，当密钥的源是 [`file`](secrets.md) 时，Docker Compose 未实现对 `uid`、`gid` 和 `mode` 属性的支持。这是因为底层使用的绑定挂载不允许 uid 重映射。

以下示例将容器内的 `server-certificate` 密钥文件名称设置为 `server.cert`，将模式设置为 `0440`（组可读），并将用户和组设置为 `103`。`server-certificate` 的值设置为文件 `./server.cert` 的内容。

```yml
services:
  frontend:
    image: example/webapp
    secrets:
      - source: server-certificate
        target: server.cert
        uid: "103"
        gid: "103"
        mode: 0o440
secrets:
  server-certificate:
    file: ./server.cert
```

### `security_opt`

`security_opt` 覆盖每个容器的默认标签方案。

```yml
security_opt:
  - label=user:USER
  - label=role:ROLE
```

有关你可以覆盖的更多默认标签方案，请参阅 [安全配置](/reference/cli/docker/container/run.md#security-opt)。

### `shm_size`

`shm_size` 配置服务容器允许的共享内存（Linux 上的 `/dev/shm` 分区）的大小。
它指定为 [字节值](extension.md#specifying-byte-values)。

### `stdin_open`

`stdin_open` 配置服务容器以分配的 stdin 运行。这与使用 `-i` 标志运行容器相同。有关更多信息，请参阅 [保持 stdin 打开](/reference/cli/docker/container/run.md#interactive)。

支持的值是 `true` 或 `false`。

### `stop_grace_period`

`stop_grace_period` 指定 Compose 在尝试停止容器时，如果容器不处理 SIGTERM（或使用 [`stop_signal`](#stop_signal) 指定的任何停止信号），必须等待多长时间才能发送 SIGKILL。它指定为 [持续时间](extension.md#specifying-durations)。

```yml
    stop_grace_period: 1s
    stop_grace_period: 1m30s
```

默认值为 10 秒，在发送 SIGKILL 之前让容器退出。

### `stop_signal`

`stop_signal` 定义 Compose 用于停止服务容器的信号。
如果未设置，容器由 Compose 发送 `SIGTERM` 停止。

```yml
stop_signal: SIGUSR1
```

### `storage_opt`

`storage_opt` 定义服务的存储驱动程序选项。

```yml
storage_opt:
  size: '1G'
```

### `sysctls`

`sysctls` 定义在容器中设置的内核参数。`sysctls` 可以使用数组或映射。

```yml
sysctls:
  net.core.somaxconn: 1024
  net.ipv4.tcp_syncookies: 0
```

```yml
sysctls:
  - net.core.somaxconn=1024
  - net.ipv4.tcp_syncookies=0
```

你只能使用在内核中命名空间的 sysctls。Docker 不支持在容器内更改同时修改主机系统的 sysctls。
有关支持的 sysctls 的概述，请参阅 [在运行时配置命名空间内核参数 (sysctls)](/reference/cli/docker/container/run.md#sysctl)。

### `tmpfs`

`tmpfs` 在容器内挂载临时文件系统。它可以是单个值或列表。

```yml
tmpfs:
 - <path>
 - <path>:<options>
```

- `path`：容器内挂载 tmpfs 的路径。
- `options`：tmpfs 挂载的逗号分隔选项列表。

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

`tty` 配置服务容器以 TTY 运行。这与使用 `-t` 或 `--tty` 标志运行容器相同。有关更多信息，请参阅 [分配伪 TTY](/reference/cli/docker/container/run.md#tty)。

支持的值是 `true` 或 `false`。

### `ulimits`

`ulimits` 覆盖容器的默认 `ulimits`。它指定为单个限制的整数或软/硬限制的映射。

```yml
ulimits:
  nproc: 65535
  nofile:
    soft: 20000
    hard: 40000
```

### `use_api_socket`

当设置 `use_api_socket` 时，容器能够通过 API 套接字与底层容器引擎交互。
你的凭证挂载在容器内，因此容器充当与容器引擎相关的命令的纯代表。
通常，容器运行的命令可以 `pull` 和 `push` 到你的注册表。

### `user`

`user` 覆盖用于运行容器进程的用户。默认值由镜像设置，例如 Dockerfile `USER`。如果未设置，则为 `root`。

### `userns_mode`

`userns_mode` 设置服务的用户命名空间。支持的值是特定于平台的，并且可能取决于平台配置。

```yml
userns_mode: "host"
```

### `uts`

{{< summary-bar feature_name="Compose uts" >}}

`uts` 配置为服务容器设置的 UTS 命名空间模式。当未指定时，由运行时决定分配 UTS 命名空间（如果支持）。可用值有：

- `'host'`：导致容器使用与主机相同的 UTS 命名空间。

```yml
    uts: "host"
```

### `volumes`

{{% include "compose/services-volumes.md" %}}

以下示例显示了 `backend` 服务正在使用的命名卷 (`db-data`)，以及为单个服务定义的绑定挂载。

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

有关 `volumes` 顶层元素的更多信息，请参阅 [卷](volumes.md)。

#### 短语法

短语法使用带有冒号分隔值的单个字符串来指定卷挂载 (`VOLUME:CONTAINER_PATH`) 或访问模式 (`VOLUME:CONTAINER_PATH:ACCESS_MODE`)。

- `VOLUME`：可以是托管容器的平台上的主机路径（绑定挂载）或卷名称。
- `CONTAINER_PATH`：卷挂载在容器中的路径。
- `ACCESS_MODE`：逗号分隔 `,` 的选项列表：
  - `rw`：读写访问。如果未指定，这是默认值。
  - `ro`：只读访问。
  - `z`：SELinux 选项，指示绑定挂载主机内容在多个容器之间共享。
  - `Z`：SELinux 选项，指示绑定挂载主机内容是私有的，不与其他容器共享。

> [!NOTE]
> SELinux 重新标记绑定挂载选项在没有 SELinux 的平台上被忽略。

> [!NOTE]
> 
> 对于绑定挂载，如果主机上的源路径不存在，短语法会在该路径创建目录。这是为了与 `docker-compose` 旧版向后兼容。
> 可以通过使用长语法并将 `create_host_path` 设置为 `false` 来防止这种情况。

#### 长语法

长格式语法允许你配置短格式无法表达的额外字段。

- `type`：挂载类型。`volume`、`bind`、`tmpfs`、`image`、`npipe` 或 `cluster` 之一。
- `source`：挂载的源，绑定挂载的主机路径，镜像挂载的 Docker 镜像引用，或 [顶层 `volumes` 键](volumes.md) 中定义的卷名称。不适用于 tmpfs 挂载。
- `target`：卷挂载在容器中的路径。
- `read_only`：将卷设置为只读的标志。
- `bind`：用于配置其他绑定选项：
  - `propagation`：用于绑定的传播模式。
  - `create_host_path`：如果主机上源路径不存在，则在该路径创建目录。默认为 `true`。
  - `selinux`：SELinux 重新标记选项 `z`（共享）或 `Z`（私有）
- `volume`：配置其他卷选项：
  - `nocopy`：创建卷时禁用从容器复制数据的标志。
  - `subpath`：挂载在卷内部的路径，而不是卷根目录。
- `tmpfs`：配置其他 tmpfs 选项：
  - `size`：tmpfs 挂载的大小，以字节为单位（数字或字节单位）。
  - `mode`：tmpfs 挂载的文件模式，作为八进制数字的 Unix 权限位。在 Docker Compose 版本 [2.14.0](/manuals/compose/releases/release-notes.md#2260) 中引入。
- `image`：配置其他镜像选项：
  - `subpath`：挂载在源镜像内部的路径，而不是镜像根目录。在 [Docker Compose 版本 2.35.0](/manuals/compose/releases/release-notes.md#2350) 中可用
- `consistency`：挂载的一致性要求。可用值是特定于平台的。

> [!TIP]
> 
> 处理大型存储库或 monorepo，或者处理不再随代码库扩展的虚拟文件系统？
> Compose 现在利用 [同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 并自动为绑定挂载创建文件共享。
> 确保你已使用付费订阅登录 Docker，并在 Docker Desktop 设置中启用了 **Access experimental features** 和 **Manage Synchronized file shares with Compose**。

### `volumes_from`

`volumes_from` 挂载来自另一个服务或容器的所有卷。你可以选择性地指定只读访问 `ro` 或读写 `rw`。如果未指定访问级别，则使用读写访问。

你还可以通过使用 `container:` 前缀挂载非 Compose 管理的容器的卷。

```yml
volumes_from:
  - service_name
  - service_name:ro
  - container:container_name
  - container:container_name:rw
```

### `working_dir`

`working_dir` 覆盖由镜像指定的容器工作目录，例如 Dockerfile `WORKDIR`。


```yaml
```