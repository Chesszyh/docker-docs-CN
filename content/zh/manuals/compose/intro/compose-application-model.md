---
title: Compose 工作原理
weight: 10
description: 了解 Docker Compose 的工作原理，从应用程序模型到 Compose 文件和 CLI，并辅以详细示例。
keywords: docker compose, compose.yaml, docker compose 模型, compose cli, 多容器应用程序, compose 示例 
---

通过 Docker Compose，您可以使用一个 YAML 配置文件（即 [Compose 文件](#compose-文件)）来配置应用程序的服务，然后使用 [Compose CLI](#cli) 根据该配置创建并启动所有服务。 

Compose 文件（即 `compose.yaml` 文件）遵循 [Compose 规范](/reference/compose-file/_index.md)中关于如何定义多容器应用程序的规则。这是正式 [Compose 规范](https://github.com/compose-spec/compose-spec) 的 Docker Compose 实现。 

{{< accordion title="Compose 应用程序模型" >}}

应用程序的计算组件被定义为 [服务 (services)](/reference/compose-file/services.md)。服务是一个抽象概念，通过在平台上运行同一个容器镜像和配置一次或多次来实现。

服务之间通过 [网络 (networks)](/reference/compose-file/networks.md) 进行通信。在 Compose 规范中，网络是一种平台能力抽象，用于在连接在一起的服务容器之间建立 IP 路由。

服务将持久化数据存储到 [卷 (volumes)](/reference/compose-file/volumes.md) 中并进行共享。规范将这种持久化数据描述为具有全局选项的高级文件系统挂载。

某些服务需要依赖于运行时或平台的配置数据。为此，规范定义了一个专门的 [configs](/reference/compose-file/configs.md) 概念。在容器内部，配置的行为类似于卷——它们被挂载为文件。然而，配置在平台层级的定义有所不同。

[机密 (secret)](/reference/compose-file/secrets.md) 是配置数据的一种特殊形式，用于处理不应在没有安全考虑的情况下暴露的敏感数据。机密以挂载到容器内的文件形式提供给服务，但由于提供敏感数据的平台特定资源非常特殊，因此在 Compose 规范中值得拥有独立的概念和定义。

> [!NOTE]
>
> 对于卷、配置和机密，您可以在顶级进行简单的声明，然后在服务层级添加更多特定于平台的信息。

一个项目（project）是应用程序规范在平台上的单次部署。项目名称通过顶级 [`name`](/reference/compose-file/version-and-name.md) 属性设置，用于将资源组合在一起，并将其与其他应用程序或具有不同参数的同一 Compose 规范应用程序的其他安装隔离。如果您在平台上创建资源，必须为资源名称加上项目前缀，并设置标签 `com.docker.compose.project`。

Compose 允许您设置自定义项目名称并覆盖此名称，这样同一个 `compose.yaml` 文件只需传递一个不同的名称，即可在同一基础设施上部署两次而无需更改。

{{< /accordion >}} 

## Compose 文件

Compose 文件的默认路径是位于工作目录中的 `compose.yaml`（首选）或 `compose.yml`。为了向后兼容早期版本，Compose 还支持 `docker-compose.yaml` 和 `docker-compose.yml`。如果两个文件都存在，Compose 会优先选择规范的 `compose.yaml`。

您可以使用 [片段 (fragments)](/reference/compose-file/fragments.md) 和 [扩展 (extensions)](/reference/compose-file/extension.md) 来保持 Compose 文件的效率和易维护性。

可以将多个 Compose 文件 [合并](/reference/compose-file/merge.md) 在一起以定义应用程序模型。YAML 文件的组合是通过根据您设置的 Compose 文件顺序追加或覆盖 YAML 元素来实现的。简单属性和映射会被优先级最高的 Compose 文件覆盖，列表则通过追加进行合并。每当合并位于其他文件夹中的补充文件时，相对路径将基于第一个 Compose 文件的父文件夹进行解析。由于某些 Compose 文件元素既可以表示为单个字符串也可以表示为复杂对象，因此合并适用于展开后的形式。有关更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

如果您想重用其他 Compose 文件，或者将应用程序模型的部分内容提取到单独的 Compose 文件中，还可以使用 [`include`](/reference/compose-file/include.md)。如果您的 Compose 应用程序依赖于另一个由不同团队管理的应用程序，或者需要与他人共享，这会非常有用。

## CLI

Docker CLI 允许您通过 `docker compose` 命令及其子命令与 Docker Compose 应用程序进行交互。如果您使用的是 Docker Desktop，默认已包含 Docker Compose CLI。

使用 CLI，您可以管理在 `compose.yaml` 文件中定义的多容器应用程序的生命周期。CLI 命令使您能够毫不费力地启动、停止和配置应用程序。

### 核心命令 

启动 `compose.yaml` 文件中定义的所有服务：

```console
$ docker compose up
```

停止并移除运行中的服务：

```console
$ docker compose down 
```

如果您想监控运行中容器的输出并调试问题，可以使用以下命令查看日志： 

```console
$ docker compose logs
```

列出所有服务及其当前状态：

```console
$ docker compose ps
```

有关所有 Compose CLI 命令的完整列表，请参阅 [参考文档](/reference/cli/docker/compose/_index.md)。

## 演示示例

以下示例说明了上述 Compose 概念。此示例仅供参考。

假设一个应用程序被分为前端 Web 应用程序和后端服务。

前端在运行时使用由基础设施管理的 HTTP 配置文件进行配置，提供一个外部域名，并由平台的安全机密存储注入 HTTPS 服务器证书。

后端将数据存储在持久卷中。

两个服务在隔离的后端网络 (back-tier network) 上相互通信，同时前端也连接到前端网络 (front-tier network) 并暴露 443 端口供外部使用。

![Compose 应用程序示例](../images/compose-application.webp)

示例应用程序由以下部分组成：

- 两个由 Docker 镜像支持的服务：`webapp` 和 `database`
- 一个注入到前端的机密 (HTTPS 证书)
- 一个注入到前端的配置 (HTTP)
- 一个挂载到后端的持久卷
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
  # 只要这些对象存在就足以定义它们
  front-tier: {}
  back-tier: {}
```

`docker compose up` 命令会启动 `frontend` 和 `backend` 服务，创建必要的网络和卷，并将配置和机密注入到前端服务中。

`docker compose ps` 提供了服务当前状态的快照，可以轻松查看哪些容器正在运行、它们的状态以及它们正在使用的端口：

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## 下一步 

- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
- [探索一些示例应用程序](/manuals/compose/support-and-feedback/samples-for-compose.md)
- [熟悉 Compose 规范](/reference/compose-file/_index.md)
