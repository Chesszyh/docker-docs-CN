---
description: Docker Compose 如何在容器之间设置网络
keywords: documentation, docs, docker, compose, orchestration, containers, networking
title: Compose 中的网络
linkTitle: 网络
weight: 70
aliases:
- /compose/networking/
---

{{% include "compose-eol.md" %}}

默认情况下，Compose 为您的应用程序设置一个单独的[网络](/reference/cli/docker/network/create.md)。服务的每个容器都会加入默认网络，并且可以被该网络上的其他容器访问，同时也可以通过服务名称被发现。

> [!NOTE]
>
> 您的应用程序网络的名称基于"项目名称"，
> 而项目名称基于其所在目录的名称。您可以使用
> [`--project-name` 标志](/reference/cli/docker/compose.md)
> 或 [`COMPOSE_PROJECT_NAME` 环境变量](environment-variables/envvars.md#compose_project_name)来覆盖项目名称。

例如，假设您的应用程序位于名为 `myapp` 的目录中，您的 `compose.yaml` 如下所示：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres
    ports:
      - "8001:5432"
```

当您运行 `docker compose up` 时，会发生以下情况：

1.  创建一个名为 `myapp_default` 的网络。
2.  使用 `web` 的配置创建一个容器。它以 `web` 的名称加入网络 `myapp_default`。
3.  使用 `db` 的配置创建一个容器。它以 `db` 的名称加入网络 `myapp_default`。

现在每个容器都可以查找服务名称 `web` 或 `db` 并获取相应容器的 IP 地址。例如，`web` 的应用程序代码可以连接到 URL `postgres://db:5432` 并开始使用 Postgres 数据库。

重要的是要注意 `HOST_PORT` 和 `CONTAINER_PORT` 之间的区别。在上面的示例中，对于 `db`，`HOST_PORT` 是 `8001`，容器端口是 `5432`（postgres 默认端口）。网络化的服务到服务通信使用 `CONTAINER_PORT`。当定义了 `HOST_PORT` 时，该服务也可以在 swarm 外部访问。

在 `web` 容器内，您连接到 `db` 的连接字符串看起来像 `postgres://db:5432`，而从主机机器，连接字符串看起来像 `postgres://{DOCKER_IP}:8001`，例如如果您的容器在本地运行，则为 `postgres://localhost:8001`。

## 更新网络上的容器

如果您对服务进行配置更改并运行 `docker compose up` 来更新它，旧容器会被删除，新容器会以不同的 IP 地址但相同的名称加入网络。正在运行的容器可以查找该名称并连接到新地址，但旧地址将停止工作。

如果任何容器与旧容器有打开的连接，这些连接将被关闭。容器有责任检测此情况，再次查找名称并重新连接。

> [!TIP]
>
> 尽可能通过名称而不是 IP 引用容器。否则您需要不断更新使用的 IP 地址。

## 链接容器

链接允许您定义额外的别名，通过这些别名可以从另一个服务访问某个服务。它们不是启用服务通信所必需的。默认情况下，任何服务都可以通过该服务的名称访问任何其他服务。在以下示例中，`db` 可以从 `web` 通过主机名 `db` 和 `database` 访问：

```yaml
services:

  web:
    build: .
    links:
      - "db:database"
  db:
    image: postgres
```

有关更多信息，请参阅 [links 参考](/reference/compose-file/services.md#links)。

## 多主机网络

当在启用了 [Swarm 模式](/manuals/engine/swarm/_index.md)的 Docker Engine 上部署 Compose 应用程序时，您可以使用内置的 `overlay` 驱动程序来启用多主机通信。

Overlay 网络始终创建为 `attachable`。您可以选择将 [`attachable`](/reference/compose-file/networks.md#attachable) 属性设置为 `false`。

请参阅 [Swarm 模式部分](/manuals/engine/swarm/_index.md)了解如何设置 Swarm 集群，以及[多主机网络入门](/manuals/engine/network/tutorials/overlay.md)了解多主机 overlay 网络。

## 指定自定义网络

您可以使用顶级 `networks` 键指定自己的网络，而不仅仅使用默认的应用程序网络。这允许您创建更复杂的拓扑结构并指定[自定义网络驱动程序](/engine/extend/plugins_network/)和选项。您还可以使用它将服务连接到非 Compose 管理的外部创建的网络。

每个服务都可以使用服务级别的 `networks` 键指定要连接的网络，这是一个引用顶级 `networks` 键下条目的名称列表。

以下示例显示了一个定义两个自定义网络的 Compose 文件。`proxy` 服务与 `db` 服务是隔离的，因为它们没有共同的网络。只有 `app` 可以与两者通信。

```yaml
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

可以通过为每个附加的网络设置 [ipv4_address 和/或 ipv6_address](/reference/compose-file/services.md#ipv4_address-ipv6_address) 来配置静态 IP 地址的网络。

网络还可以指定[自定义名称](/reference/compose-file/networks.md#name)：

```yaml
services:
  # ...
networks:
  frontend:
    name: custom_frontend
    driver: custom-driver-1
```

## 配置默认网络

您可以通过在 `networks` 下定义一个名为 `default` 的条目来更改应用程序范围的默认网络设置，而不是或除了指定自己的网络之外：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres

networks:
  default:
    # 使用自定义驱动程序
    driver: custom-driver-1
```

## 使用现有网络

如果您已经在 Compose 外部使用 `docker network create` 命令手动创建了桥接网络，您可以通过将网络标记为 `external` 来将您的 Compose 服务连接到它。

如果您希望容器加入预先存在的网络，请使用 [`external` 选项](/reference/compose-file/networks.md#external)
```yaml
services:
  # ...
networks:
  network1:
    name: my-pre-existing-network
    external: true
```

Compose 不会尝试创建名为 `[projectname]_default` 的网络，而是查找名为 `my-pre-existing-network` 的网络并将您的应用程序容器连接到它。

## 更多参考信息

有关可用网络配置选项的完整详细信息，请参阅以下参考：

- [顶级 `networks` 元素](/reference/compose-file/networks.md)
- [服务级别 `networks` 属性](/reference/compose-file/services.md#networks)
