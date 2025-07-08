---
title: 网络顶级元素
description: 探索网络顶级元素可以拥有的所有属性。
keywords: compose, compose 规范, 网络, compose 文件参考
aliases:
 - /compose/compose-file/06-networks/
weight: 30
---

{{% include "compose/networks.md" %}}

要在多个服务之间使用网络，您必须通过 `services` 顶级元素中的 [networks](services.md) 属性明确授予每个服务访问权限。`networks` 顶级元素具有提供更精细控制的附加语法。

## 示例

### 基本示例

在以下示例中，在运行时，将创建网络 `front-tier` 和 `back-tier`，并且 `frontend` 服务将连接到 `front-tier` 和 `back-tier` 网络。

```yml
services:
  frontend:
    image: example/webapp
    networks:
      - front-tier
      - back-tier

networks:
  front-tier:
  back-tier:
```

### 高级示例

```yml
services:
  proxy:
    build: ./proxy
    networks:
      - frontend
  app:
    build: ./app
    networks:
      - frontend
      - backend
  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
    # 指定驱动程序选项
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
  backend:
    # 使用自定义驱动程序
    driver: custom-driver
```

高级示例展示了一个定义了两个自定义网络的 Compose 文件。`proxy` 服务与 `db` 服务隔离，因为它们没有共享网络。只有 `app` 可以与两者通信。

## 默认网络

当 Compose 文件未声明显式网络时，Compose 会使用隐式 `default` 网络。没有显式 [`networks`](services.md#networks) 声明的服务将由 Compose 连接到此 `default` 网络：


```yml
services:
  some-service:
    image: foo
```
此示例实际上等同于：

```yml
services:
  some-service:
    image: foo
    networks:
      default: {}  
networks:
  default: {}      
```

You can customize the `default` network with an explicit declaration:

```yml
networks:
  default: 
    name: a_network # Use a custom name
    driver_opts:    # pass options to driver for network creation
      com.docker.network.bridge.host_binding_ipv4: 127.0.0.1
```

有关选项，请参阅 [Docker Engine 文档](https://docs.docker.com/engine/network/drivers/bridge/#options)。

## 属性

### `driver`

`driver` 指定此网络应使用的驱动程序。如果驱动程序在平台上不可用，Compose 将返回错误。

```yml
networks:
  db-data:
    driver: bridge
```

有关驱动程序和可用选项的更多信息，请参阅 [网络驱动程序](/manuals/engine/network/drivers/_index.md)。

### `driver_opts`

`driver_opts` 指定要传递给驱动程序的选项列表，以键值对的形式。这些选项是驱动程序相关的。

```yml
networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
```

有关更多信息，请查阅 [网络驱动程序文档](/manuals/engine/network/_index.md)。

### `attachable`

如果 `attachable` 设置为 `true`，则独立容器除了服务之外，还应该能够连接到此网络。
如果独立容器连接到网络，它可以与服务和也连接到网络的其他独立容器通信。

```yml
networks:
  mynet1:
    driver: overlay
    attachable: true
```

### `enable_ipv4`

{{< summary-bar feature_name="Compose 启用 ipv4" >}}

`enable_ipv4` 可用于禁用 IPv4 地址分配。

```yml
  networks:
    ip6net:
      enable_ipv4: false
      enable_ipv6: true
```

### `enable_ipv6`

`enable_ipv6` 启用 IPv6 地址分配。

```yml
  networks:
    ip6net:
      enable_ipv6: true
```

### `external`

如果设置为 `true`：
 - `external` 指定此网络的生命周期在应用程序之外维护。
Compose 不会尝试创建这些网络，如果网络不存在，则会返回错误。
 - 除名称之外的所有其他属性都无关紧要。如果 Compose 检测到任何其他属性，它会拒绝 Compose 文件为无效。

在以下示例中，`proxy` 是通往外部世界的网关。Compose 不会尝试创建网络，而是查询平台以获取名为 `outside` 的现有网络，并将 `proxy` 服务的容器连接到该网络。

```yml
services:
  proxy:
    image: example/proxy
    networks:
      - outside
      - default
  app:
    image: example/app
    networks:
      - default

networks:
  outside:
    external: true
```

### `ipam`

`ipam` 指定自定义 IPAM 配置。这是一个具有多个属性的对象，每个属性都是可选的：

- `driver`：自定义 IPAM 驱动程序，而不是默认驱动程序。
- `config`：包含零个或多个配置元素的列表，每个元素包含：
  - `subnet`：表示网络段的 CIDR 格式子网
  - `ip_range`：用于分配容器 IP 的 IP 范围
  - `gateway`：主子网的 IPv4 或 IPv6 网关
  - `aux_addresses`：网络驱动程序使用的辅助 IPv4 或 IPv6 地址，作为从主机名到 IP 的映射
- `options`：驱动程序特定的选项，作为键值映射。

```yml
networks:
  mynet1:
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          ip_range: 172.28.5.0/24
          gateway: 172.28.5.254
          aux_addresses:
            host1: 172.28.1.5
            host2: 172.28.1.6
            host3: 172.28.1.7
      options:
        foo: bar
        baz: "0"
```

### `internal`

默认情况下，Compose 为网络提供外部连接。`internal` 设置为 `true` 时，允许您创建外部隔离的网络。

### `labels`

使用 `labels` 向容器添加元数据。您可以使用数组或字典。

建议您使用反向 DNS 表示法，以防止标签与由其他软件使用的标签冲突。

```yml
networks:
  mynet1:
    labels:
      com.example.description: "金融交易网络"
      com.example.department: "财务"
      com.example.label-with-empty-value: ""
```

```yml
networks:
  mynet1:
    labels:
      - "com.example.description=金融交易网络"
      - "com.example.department=财务"
      - "com.example.label-with-empty-value"
```

Compose 设置 `com.docker.compose.project` 和 `com.docker.compose.network` 标签。

### `name`

`name` 为网络设置自定义名称。`name` 字段可用于引用包含特殊字符的网络。
名称按原样使用，并且不与项目名称进行范围限定。

```yml
networks:
  network1:
    name: my-app-net
```

它还可以与 `external` 属性结合使用，以定义 Compose 应该检索的平台网络，通常通过使用参数，以便 Compose 文件不需要硬编码运行时特定值：

```yml
networks:
  network1:
    external: true
    name: "${NETWORK_ID}"
```

## 附加资源

有关更多示例，请参阅 [Compose 中的网络](/manuals/compose/how-tos/networking.md)。
