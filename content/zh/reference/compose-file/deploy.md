---
title: Compose 部署规范
description: 了解 Compose 部署规范
keywords: compose, compose 规范, compose 文件参考, compose 部署规范
aliases: 
 - /compose/compose-file/deploy/
weight: 140
---

{{% include "compose/deploy.md" %}}

## 属性

### `endpoint_mode`

`endpoint_mode` 指定了外部客户端连接到服务的服务发现方法。Compose 部署规范定义了两个规范值：

* `endpoint_mode: vip`：为服务分配一个虚拟 IP (VIP)，作为客户端在网络上访问服务的前端。
  平台在客户端和运行服务的节点之间路由请求，客户端无需了解有多少节点参与服务或它们的 IP 地址或端口。

* `endpoint_mode: dnsrr`：平台为服务设置 DNS 条目，以便对服务名称的 DNS 查询返回 IP 地址列表 (DNS 轮询)，
  客户端直接连接到其中一个。

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "8080:80"
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
```

### `labels`

`labels` 指定服务的元数据。这些标签仅设置在服务上，而不设置在服务的任何容器上。
这假设平台具有一些可以匹配 Compose 应用程序模型的“服务”原生概念。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      labels:
        com.example.description: "此标签将出现在 Web 服务上"
```

### `mode`

`mode` 定义了用于运行服务或作业的复制模型。选项包括：

- `global`：确保每个物理节点上持续运行一个任务，直到停止。
- `replicated`：在节点之间持续运行指定数量的任务，直到停止（默认）。
- `replicated-job`：执行定义数量的任务，直到完成状态（以代码 0 退出）。
   - 总任务数由 `replicas` 确定。
   - 并发性可以使用 `max-concurrent` 选项限制（仅限 CLI）。
- `global-job`：每个物理节点执行一个任务，并具有完成状态（以代码 0 退出）。
   - 随着新节点的添加自动运行。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      mode: global

  batch-job:
    image: example/processor
    deploy:
      mode: replicated-job
      replicas: 5

  maintenance:
    image: example/updater
    deploy:
      mode: global-job
```

> [!NOTE] 
> - 作业模式（`replicated-job` 和 `global-job`）专为完成并以代码 0 退出的任务而设计。
> - 已完成的任务将保留，直到明确删除。
> - 诸如 `max-concurrent` 等用于控制并发的选项仅通过 CLI 支持，在 Compose 中不可用。

有关作业选项和行为的更多详细信息，请参阅 [Docker CLI 文档](/reference/cli/docker/service/create.md#running-as-a-job)

### `placement`

`placement` 指定了平台选择物理节点以运行服务容器的约束和偏好。

#### `constraints`

`constraints` 定义了平台节点必须满足的运行服务容器的必需属性。有关更多示例，请参阅 [CLI 参考文档](/reference/cli/docker/service/create.md#constraint)。

```yml
deploy:
  placement:
    constraints:
      - disktype=ssd
```

#### `preferences`

`preferences` 定义了一种策略（目前 `spread` 是唯一支持的策略），用于将任务均匀地分布在数据中心节点标签的值上。有关更多示例，请参阅 [CLI 参考文档](/reference/cli/docker/service/create.md#placement-pref)

```yml
deploy:
  placement:
    preferences:
      - spread: node.labels.zone
```

### `replicas`

如果服务是 `replicated`（这是默认值），`replicas` 指定了在任何给定时间应运行的容器数量。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      mode: replicated
      replicas: 6
```

### `resources`

`resources` 配置了容器在平台上运行的物理资源约束。这些约束可以配置为：

- `limits`：平台必须阻止容器分配更多资源。
- `reservations`：平台必须保证容器至少可以分配配置的数量。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 50M
          pids: 1
        reservations:
          cpus: '0.25'
          memory: 20M
```

#### `cpus`

`cpus` 配置了容器可以使用的可用 CPU 资源（以核心数表示）的限制或预留。

#### `memory`

`memory` 配置了容器可以分配的内存量的限制或预留，设置为表示[字节值](extension.md#specifying-byte-values)的字符串。

#### `pids`

`pids` 调整容器的 PIDs 限制，设置为整数。

#### `devices`

`devices` 配置了容器可以使用的设备的预留。它包含一个预留列表，每个预留都设置为一个包含以下参数的对象：`capabilities`、`driver`、`count`、`device_ids` 和 `options`。

设备使用功能列表进行预留，使 `capabilities` 成为唯一必需的字段。设备必须满足所有请求的功能才能成功预留。

##### `capabilities`

`capabilities` 设置为字符串列表，表示通用和驱动程序特定的功能。
目前识别以下通用功能：

- `gpu`：图形加速器
- `tpu`：AI 加速器

为避免名称冲突，驱动程序特定的功能必须以驱动程序名称为前缀。
例如，预留 NVIDIA CUDA 启用的加速器可能如下所示：

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["nvidia-compute"]
```

##### `driver`

可以使用 `driver` 字段请求预留设备的不同驱动程序。该值指定为字符串。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["nvidia-compute"]
          driver: nvidia
```

##### `count`

如果 `count` 设置为 `all` 或未指定，Compose 将预留所有满足请求功能的设备。否则，Compose 将至少预留指定数量的设备。该值指定为整数。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["tpu"]
          count: 2
```

`count` 和 `device_ids` 字段是互斥的。如果同时指定两者，Compose 将返回错误。

##### `device_ids`

如果设置了 `device_ids`，Compose 将预留具有指定 ID 的设备，前提是它们满足请求的功能。该值指定为字符串列表。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["gpu"]
          device_ids: ["GPU-f123d1c9-26bb-df9b-1c23-4a731f61d8c7"]
```

`count` 和 `device_ids` 字段是互斥的。如果同时指定两者，Compose 将返回错误。

##### `options`

驱动程序特定选项可以使用 `options` 设置为键值对。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["gpu"]
          driver: gpuvendor
          options:
            virtualization: false
```

### `restart_policy`

`restart_policy` 配置容器退出时是否以及如何重新启动。如果未设置 `restart_policy`，Compose 将考虑服务配置设置的 `restart` 字段。

- `condition`。设置为：
  - `none`，无论退出状态如何，容器都不会自动重新启动。
  - `on-failure`，如果容器因错误而退出（表现为非零退出代码），则重新启动容器。
  - `any`（默认），无论退出状态如何，容器都会重新启动。
- `delay`：每次重新启动尝试之间等待的时间，指定为[持续时间](extension.md#specifying-durations)。默认值为 0，表示可以立即进行重新启动尝试。
- `max_attempts`：放弃之前允许的最大失败重新启动尝试次数。（默认：无限重试。）
只有当容器未在 `window` 定义的时间内成功重新启动时，失败尝试才会计入 `max_attempts`。
例如，如果 `max_attempts` 设置为 `2`，并且容器在第一次尝试时未能在窗口内成功重新启动，Compose 将继续重试，直到发生两次此类失败尝试，即使这意味着尝试超过两次。
- `window`：重新启动后等待的时间，以确定其是否成功，指定为[持续时间](extension.md#specifying-durations)（默认：结果在重新启动后立即评估）。

```yml
deploy:
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
    window: 120s
```

### `rollback_config`

`rollback_config` 配置了服务在更新失败时应如何回滚。

- `parallelism`：每次回滚的容器数量。如果设置为 0，则所有容器同时回滚。
- `delay`：每个容器组回滚之间等待的时间（默认 0s）。
- `failure_action`：如果回滚失败，该怎么做。`continue` 或 `pause` 之一（默认 `pause`）
- `monitor`：每次任务更新后监视失败的持续时间 `(ns|us|ms|s|m|h)`（默认 0s）。
- `max_failure_ratio`：回滚期间可容忍的失败率（默认 0）。
- `order`：回滚期间的操作顺序。`stop-first`（旧任务在启动新任务之前停止）或 `start-first`（新任务首先启动，并且正在运行的任务短暂重叠）之一（默认 `stop-first`）。

### `update_config`

`update_config` 配置了服务应如何更新。对于配置滚动更新很有用。

- `parallelism`：每次更新的容器数量。
- `delay`：更新一组容器之间等待的时间。
- `failure_action`：如果更新失败，该怎么做。`continue`、`rollback` 或 `pause` 之一（默认：`pause`）。
- `monitor`：每次任务更新后监视失败的持续时间 `(ns|us|ms|s|m|h)`（默认 0s）。
- `max_failure_ratio`：更新期间可容忍的失败率。
- `order`：更新期间的操作顺序。`stop-first`（旧任务在启动新任务之前停止）或 `start-first`（新任务首先启动，并且正在运行的任务短暂重叠）之一（默认 `stop-first`）。

```yml
deploy:
  update_config:
    parallelism: 2
    delay: 10s
    order: stop-first
```
