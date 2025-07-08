---
description: 了解如何为生产环境配置、部署和更新 Docker Compose 应用程序。
keywords: compose, orchestration, containers, production, production docker compose configuration, 编排, 容器, 生产环境, 配置
title: 在生产环境中使用 Compose
weight: 100
aliases:
- /compose/production/
---

当您在开发中使用 Compose 定义您的应用程序时，您可以使用此定义在不同的环境（如 CI、预发和生产）中运行您的应用程序。

部署应用程序最简单的方法是在单个服务器上运行它，类似于您运行开发环境的方式。如果您想扩展您的应用程序，您可以在 Swarm 集群上运行 Compose 应用程序。

### 为生产环境修改您的 Compose 文件

您可能需要对您的应用程序配置进行更改，以使其为生产环境做好准备。这些更改可能包括：

- 删除应用程序代码的任何卷绑定，以便代码保留在容器内，并且不能从外部更改
- 绑定到主机上的不同端口
- 以不同方式设置环境变量，例如减少日志记录的详细程度，或指定外部��务（如电子邮件服务器）的设置
- 指定重启策略，如 [`restart: always`](/reference/compose-file/services.md#restart) 以避免停机
- 添加额外的服务，如日志聚合器

因此，请考虑定义一个额外的 Compose 文件，例如 `compose.production.yaml`，其中包含特定于生产环境的配置详细信息。此配置文件只需要包含您要对原始 Compose 文件进行的更改。然后，将额外的 Compose 文件应用于原始 `compose.yaml` 以创建新配置。

一旦您有了第二个配置文件，您就可以将它与 `-f` 选项一起使用：

```console
$ docker compose -f compose.yaml -f compose.production.yaml up -d
```

有关更完整的示例和其他选项，请参阅[使用多个 compose 文件](multiple-compose-files/_index.md)。

### 部署更改

当您对应用程序代码进行更改时，请记住重新构建您的镜像并重新创建您的应用程序容器。要重新部署名为 `web` 的服务，请使用：

```console
$ docker compose build web
$ docker compose up --no-deps -d web
```

第一个命令重新构建 `web` 的镜像，然后停止、销毁并仅重新创建 `web` 服务。`--no-deps` 标志可防止 Compose 同时重新创建 `web` 所依赖的任何服务。

### 在单个服务器上运行 Compose

您可以通过适当设置 `DOCKER_HOST`���`DOCKER_TLS_VERIFY` 和 `DOCKER_CERT_PATH` 环境变量，使用 Compose 将应用程序部署到远程 Docker 主机。有关更多信息，请参阅[预定义环境变量](environment-variables/envvars.md)。

设置好环境变量后，所有常规的 `docker compose` 命令都无需进一步配置即可工作。

## 后续步骤

- [使用多个 Compose 文件](multiple-compose-files/_index.md)
