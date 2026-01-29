---
description: 了解 Docker Compose 如何在容器之间设置网络
keywords: 文档, docs, docker, compose, 编排, 容器, 网络
title: Compose 中的网络
linkTitle: 网络 (Networking)
weight: 70
aliases:
- /compose/networking/
---

{{% include "compose-eol.md" %}}

默认情况下，Compose 会为您的应用程序设置一个单一的 [网络](/reference/cli/docker/network/create.md)。服务的每个容器都会加入该默认网络，并且既可以被该网络上的其他容器访问，也可以通过服务名称被发现。

> [!NOTE]
>
> 您的应用程序网络名称是基于“项目名称”生成的，而项目名称通常基于其所在目录的名称。您可以使用 [`--project-name` 标志](/reference/cli/docker/compose.md) 或 [`COMPOSE_PROJECT_NAME` 环境变量](environment-variables/envvars.md#compose_project_name) 来覆盖项目名称。

例如，假设您的应用程序位于名为 `myapp` 的目录中，且您的 `compose.yaml` 如下所示：

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
2.  使用 `web` 的配置创建一个容器。它以 `web` 为名加入 `myapp_default` 网络。
3.  使用 `db` 的配置创建一个容器。它以 `db` 为名加入 `myapp_default` 网络。

现在，每个容器都可以查找服务名称 `web` 或 `db` 并获取相应的容器 IP 地址。例如，`web` 的应用程序代码可以连接到 URL `postgres://db:5432` 并开始使用 Postgres 数据库。

注意 `HOST_PORT`（宿主机端口）和 `CONTAINER_PORT`（容器端口）之间的区别非常重要。在上面的示例中，对于 `db`，`HOST_PORT` 是 `8001` ，容器端口是 `5432`（Postgres 默认端口）。网络化的服务间通信使用的是 `CONTAINER_PORT`。当定义了 `HOST_PORT` 时，该服务也可以从外部访问。

在 `web` 容器内部，您到 `db` 的连接字符串看起来像 `postgres://db:5432`；而从宿主机来看，连接字符串看起来像 `postgres://{DOCKER_IP}:8001`，例如如果您的容器在本地运行，则是 `postgres://localhost:8001`。

## 更新网络上的容器

如果您对某个服务进行了配置更改并运行 `docker compose up` 来更新它，旧容器会被移除，新容器会以不同的 IP 地址但相同的名称加入网络。运行中的容器可以查找该名称并连接到新地址，但旧地址将失效。

如果有任何容器开启了到旧容器的连接，这些连接将被关闭。容器有责任检测到这种情况，重新查找名称并重新连接。

> [!TIP]
>
> 只要可能，请通过名称而不是 IP 引用容器。否则，您将需要不断更新所使用的 IP 地址。

## 链接容器

链接（Links）允许您定义额外的别名，通过这些别名，一个服务可以从另一个服务访问。它们不是实现服务间通信所必需的。默认情况下，任何服务都可以通过其他服务的名称访问它们。在以下示例中，`db` 可以通过主机名 `db` 和 `database` 从 `web` 访问：

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

在 [启用了 Swarm 模式](/manuals/engine/swarm/_index.md) 的 Docker Engine 上部署 Compose 应用程序时，您可以利用内置的 `overlay` 驱动程序来实现多主机通信。

Overlay 网络始终被创建为 `attachable`（可附加的）。您可以选择将 [`attachable`](/reference/compose-file/networks.md#attachable) 属性设置为 `false`。

请查阅 [Swarm 模式章节](/manuals/engine/swarm/_index.md) 了解如何设置 Swarm 集群，以及 [多主机网络入门](/manuals/engine/network/tutorials/overlay.md) 了解多主机 overlay 网络。

## 指定自定义网络

除了使用默认的应用程序网络外，您还可以通过顶级 `networks` 键指定自己的网络。这允许您创建更复杂的拓扑，并指定 [自定义网络驱动程序](/engine/extend/plugins_network/) 和选项。您还可以使用它将服务连接到并非由 Compose 管理的外部创建的网络。

每个服务都可以通过服务级别的 `networks` 键指定要连接的网络，这是一个引用顶级 `networks` 键下条目的名称列表。

以下示例展示了一个定义了两个自定义网络的 Compose 文件。`proxy` 服务与 `db` 服务相互隔离，因为它们没有共同的网络。只有 `app` 可以与两者通信。

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

可以通过为每个附加网络设置 [ipv4_address 和/或 ipv6_address](/reference/compose-file/services.md#ipv4_address-ipv6_address) 来为网络配置静态 IP 地址。

网络也可以被赋予 [自定义名称](/reference/compose-file/networks.md#name)：

```yaml
services:
  # ...
networks:
  frontend:
    name: custom_frontend
    driver: custom-driver-1
```

## 配置默认网络

除了（或同时）指定您自己的网络外，您还可以通过在 `networks` 下定义一个名为 `default` 的条目来更改全应用默认网络的设置：

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

如果您在 Compose 之外使用 `docker network create` 命令手动创建了一个 bridge 网络，可以通过将该网络标记为 `external`（外部）来将您的 Compose 服务连接到它。

如果您想让容器加入一个预先存在的网络，请使用 [`external` 选项](/reference/compose-file/networks.md#external)：
```yaml
services:
  # ...
networks:
  network1:
    name: my-pre-existing-network
    external: true
```

Compose 不再尝试创建名为 `[projectname]_default` 的网络，而是寻找名为 `my-pre-existing-network` 的网络并将您的应用容器连接到它。

## 更多参考信息 

有关可用网络配置选项的完整详情，请参阅以下参考资料：

- [顶级 `networks` 元素](/reference/compose-file/networks.md)
- [服务级 `networks` 属性](/reference/compose-file/services.md#networks)
