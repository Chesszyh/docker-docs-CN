---
title: Compose 如何工作
weight: 10
description: 了解 Docker Compose 如何工作，从应用程序模型到 Compose 文件和 CLI，同时跟随一个详细的示例。
keywords: docker compose, compose.yaml, docker compose model, compose cli, multi-container application, compose example
aliases:
- /compose/compose-file/02-model/
- /compose/compose-yaml-file/
- /compose/compose-application-model/
---

使用 Docker Compose，您可以使用 YAML 配置文件（称为 [Compose 文件](#compose-文件)）来配置应用程序的服务，然后使用 [Compose CLI](#cli) 从您的配置中创建和启动所有服务。

Compose 文件，或 `compose.yaml` 文件，遵循 [Compose Specification（Compose 规范）](/reference/compose-file/_index.md)提供的规则来定义多容器应用程序。这是正式 [Compose Specification](https://github.com/compose-spec/compose-spec) 的 Docker Compose 实现。

{{< accordion title="Compose 应用程序模型" >}}

应用程序的计算组件被定义为[服务（services）](/reference/compose-file/services.md)。服务是一个抽象概念，通过一次或多次运行相同的容器镜像和配置在平台上实现。

服务之间通过[网络（networks）](/reference/compose-file/networks.md)相互通信。在 Compose Specification 中，网络是一种平台能力抽象，用于在连接在一起的服务中的容器之间建立 IP 路由。

服务将持久数据存储和共享到[卷（volumes）](/reference/compose-file/volumes.md)中。Specification 将此类持久数据描述为具有全局选项的高级文件系统挂载。

某些服务需要依赖于运行时或平台的配置数据。为此，Specification 定义了专门的 [configs（配置）](/reference/compose-file/configs.md)概念。从容器内部来看，configs 的行为类似于卷——它们作为文件被挂载。然而，configs 在平台级别的定义是不同的。

[secret（密钥）](/reference/compose-file/secrets.md)是配置数据的一种特殊类型，用于不应在没有安全考虑的情况下暴露的敏感数据。Secrets 作为文件挂载到容器中提供给服务，但提供敏感数据的平台特定资源足够特殊，值得在 Compose Specification 中有一个独特的概念和定义。

> [!NOTE]
>
> 对于卷、configs 和 secrets，您可以在顶层有一个简单的声明，然后在服务级别添加更多平台特定的信息。

项目是应用程序规范在平台上的单独部署。项目名称通过顶级 [`name`](/reference/compose-file/version-and-name.md) 属性设置，用于将资源组合在一起并将它们与其他应用程序或使用不同参数的同一 Compose 指定应用程序的其他安装隔离。如果您在平台上创建资源，必须用项目名称作为资源名称的前缀，并设置标签 `com.docker.compose.project`。

Compose 提供了一种方式让您设置自定义项目名称并覆盖此名称，以便同一个 `compose.yaml` 文件可以在同一基础设施上部署两次，而无需更改，只需传递不同的名称。

{{< /accordion >}}

## Compose 文件

Compose 文件的默认路径是放置在工作目录中的 `compose.yaml`（首选）或 `compose.yml`。Compose 还支持 `docker-compose.yaml` 和 `docker-compose.yml` 以向后兼容早期版本。如果两个文件都存在，Compose 优先使用规范的 `compose.yaml`。

您可以使用[片段（fragments）](/reference/compose-file/fragments.md)和[扩展（extensions）](/reference/compose-file/extension.md)来保持 Compose 文件高效且易于维护。

多个 Compose 文件可以[合并](/reference/compose-file/merge.md)在一起以定义应用程序模型。YAML 文件的组合是通过根据您设置的 Compose 文件顺序追加或覆盖 YAML 元素来实现的。简单属性和映射会被最高顺序的 Compose 文件覆盖，列表通过追加来合并。当被合并的补充文件托管在其他文件夹中时，相对路径基于第一个 Compose 文件的父文件夹解析。由于某些 Compose 文件元素既可以表示为单个字符串也可以表示为复杂对象，合并应用于展开形式。有关更多信息，请参阅[使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

如果您想重用其他 Compose 文件，或将应用程序模型的部分分解到单独的 Compose 文件中，您也可以使用 [`include`](/reference/compose-file/include.md)。如果您的 Compose 应用程序依赖于由不同团队管理的另一个应用程序，或需要与他人共享，这将非常有用。

## CLI

Docker CLI 让您可以通过 `docker compose` 命令及其子命令与 Docker Compose 应用程序交互。如果您使用的是 Docker Desktop，Docker Compose CLI 默认包含在内。

使用 CLI，您可以管理 `compose.yaml` 文件中定义的多容器应用程序的生命周期。CLI 命令使您能够轻松地启动、停止和配置应用程序。

### 关键命令

要启动 `compose.yaml` 文件中定义的所有服务：

```console
$ docker compose up
```

要停止和移除正在运行的服务：

```console
$ docker compose down
```

如果您想监控正在运行的容器的输出并调试问题，可以查看日志：

```console
$ docker compose logs
```

要列出所有服务及其当前状态：

```console
$ docker compose ps
```

有关所有 Compose CLI 命令的完整列表，请参阅[参考文档](/reference/cli/docker/compose/_index.md)。

## 示例说明

以下示例说明了上述 Compose 概念。该示例是非规范性的。

考虑一个分为前端 Web 应用程序和后端服务的应用程序。

前端在运行时配置了一个由基础设施管理的 HTTP 配置文件，提供外部域名，以及一个由平台安全密钥存储注入的 HTTPS 服务器证书。

后端将数据存储在持久卷中。

两个服务在隔离的后端网络上相互通信，同时前端还连接到前端网络并暴露端口 443 供外部使用。

![Compose 应用程序示例](../images/compose-application.webp)

示例应用程序由以下部分组成：

- 两个服务，由 Docker 镜像支持：`webapp` 和 `database`
- 一个密钥（HTTPS 证书），注入到前端
- 一个配置（HTTP），注入到前端
- 一个持久卷，附加到后端
- 两个网络

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate

  backend:
    image: example/database
    volumes:
      - db-data:/etc/data
    networks:
      - back-tier

volumes:
  db-data:
    driver: flocker
    driver_opts:
      size: "10GiB"

configs:
  httpd-config:
    external: true

secrets:
  server-certificate:
    external: true

networks:
  # The presence of these objects is sufficient to define them
  front-tier: {}
  back-tier: {}
```

`docker compose up` 命令启动 `frontend` 和 `backend` 服务，创建必要的网络和卷，并将配置和密钥注入到前端服务中。

`docker compose ps` 提供服务当前状态的快照，使您可以轻松查看哪些容器正在运行、它们的状态以及它们使用的端口：

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## 下一步

- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
- [探索一些 Compose 示例应用程序](/manuals/compose/support-and-feedback/samples-for-compose.md)
- [熟悉 Compose Specification](/reference/compose-file/_index.md)
