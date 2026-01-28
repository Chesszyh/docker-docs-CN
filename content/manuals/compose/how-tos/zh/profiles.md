---
title: 在 Compose 中使用配置文件
linkTitle: 使用服务配置文件
weight: 20
description: 如何在 Docker Compose 中使用配置文件
keywords: cli, compose, profile, profiles reference
aliases:
- /compose/profiles/
---

{{% include "compose/profiles.md" %}}

## 为服务分配配置文件

服务通过 [`profiles` 属性](/reference/compose-file/services.md#profiles)与配置文件关联，该属性接受配置文件名称数组：

```yaml
services:
  frontend:
    image: frontend
    profiles: [frontend]

  phpmyadmin:
    image: phpmyadmin
    depends_on: [db]
    profiles: [debug]

  backend:
    image: backend

  db:
    image: mysql
```

这里服务 `frontend` 和 `phpmyadmin` 分别被分配到配置文件 `frontend` 和 `debug`，因此只有在它们各自的配置文件被启用时才会启动。

没有 `profiles` 属性的服务始终被启用。在这种情况下，运行 `docker compose up` 只会启动 `backend` 和 `db`。

有效的配置文件名称遵循正则表达式格式 `[a-zA-Z0-9][a-zA-Z0-9_.-]+`。

> [!TIP]
>
> 应用程序的核心服务不应分配 `profiles`，
> 这样它们始终被启用并自动启动。

## 启动特定配置文件

要启动特定配置文件，请提供 `--profile` [命令行选项](/reference/cli/docker/compose.md)或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug up
```
```console
$ COMPOSE_PROFILES=debug docker compose up
```

这两个命令都会启动启用了 `debug` 配置文件的服务。在前面的 `compose.yaml` 文件中，这会启动服务 `db`、`backend` 和 `phpmyadmin`。

### 启动多个配置文件

您还可以启用多个配置文件，例如使用 `docker compose --profile frontend --profile debug up` 将启用配置文件 `frontend` 和 `debug`。

可以通过传递多个 `--profile` 标志或为 `COMPOSE_PROFILES` 环境变量指定逗号分隔的列表来指定多个配置文件：

```console
$ docker compose --profile frontend --profile debug up
```

```console
$ COMPOSE_PROFILES=frontend,debug docker compose up
```

如果您想同时启用所有配置文件，可以运行 `docker compose --profile "*"`。

## 配置文件自动启动和依赖解析

当您在命令行上明确指定分配了一个或多个配置文件的服务时，您不需要手动启用配置文件，因为 Compose 无论其配置文件是否被激活都会运行该服务。这对于运行一次性服务或调试工具很有用。

只有目标服务（及其通过 `depends_on` 声明的任何依赖项）会被启动。共享相同配置文件的其他服务不会被启动，除非：
- 它们也被明确指定，或者
- 使用 `--profile` 或 `COMPOSE_PROFILES` 明确启用了配置文件。

当在命令行上明确指定分配了 `profiles` 的服务时，其配置文件会自动启动，因此您不需要手动启动它们。这可用于一次性服务和调试工具。作为示例，请考虑以下配置：

```yaml
services:
  backend:
    image: backend

  db:
    image: mysql

  db-migrations:
    image: backend
    command: myapp migrate
    depends_on:
      - db
    profiles:
      - tools
```

```sh
# 只启动 backend 和 db（不涉及配置文件）
$ docker compose up -d

# 运行 db-migrations 服务而不手动启用 'tools' 配置文件
$ docker compose run db-migrations
```

在此示例中，`db-migrations` 运行，即使它被分配到 tools 配置文件，因为它被明确指定。`db` 服务也会自动启动，因为它在 `depends_on` 中列出。

如果目标服务的依赖项也受配置文件限制，您必须确保这些依赖项：
 - 在同一配置文件中
 - 单独启动
 - 未分配到任何配置文件，因此始终启用

## 使用特定配置文件停止应用程序和服务

与启动特定配置文件一样，您可以使用 `--profile` [命令行选项](/reference/cli/docker/compose.md#use--p-to-specify-a-project-name)或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug down
```
```console
$ COMPOSE_PROFILES=debug docker compose down
```

这两个命令都会停止并删除具有 `debug` 配置文件的服务以及没有配置文件的服务。在以下 `compose.yaml` 文件中，这会停止服务 `db`、`backend` 和 `phpmyadmin`。

```yaml
services:
  frontend:
    image: frontend
    profiles: [frontend]

  phpmyadmin:
    image: phpmyadmin
    depends_on: [db]
    profiles: [debug]

  backend:
    image: backend

  db:
    image: mysql
```

如果您只想停止 `phpmyadmin` 服务，可以运行

```console
$ docker compose down phpmyadmin
```
或者
```console
$ docker compose stop phpmyadmin
```

> [!NOTE]
>
> 运行 `docker compose down` 只会停止 `backend` 和 `db`。

## 参考信息

[`profiles`](/reference/compose-file/services.md#profiles)
