---
title: 在 Compose 中使用配置文件 (Profiles)
linkTitle: 使用服务配置文件
weight: 20
description: 了解如何使用 Docker Compose 的配置文件 (profiles)
keywords: cli, compose, profile, 配置文件参考
aliases:
- /compose/profiles/
---

{{% include "compose/profiles.md" %}}

## 为服务分配配置文件

服务通过 [`profiles` 属性](/reference/compose-file/services.md#profiles) 与配置文件关联，该属性接受一个配置文件名称数组：

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

在这里，服务 `frontend` 和 `phpmyadmin` 分别被分配给配置文件 `frontend` 和 `debug`，因此只有当启用各自的配置文件时，它们才会被启动。

不带 `profiles` 属性的服务始终处于启用状态。在这种情况下，运行 `docker compose up` 将仅启动 `backend` 和 `db`。

有效的配置文件名称遵循正则表达式格式 `[a-zA-Z0-9][a-zA-Z0-9_.-]+`。

> [!TIP]
>
> 应用程序的核心服务不应被分配 `profiles`，这样它们就始终处于启用状态并自动启动。

## 启动特定的配置文件

要启动特定的配置文件，请提供 `--profile` [命令行选项](/reference/cli/docker/compose.md) 或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug up
```
```console
$ COMPOSE_PROFILES=debug docker compose up
```

这两个命令都会在启用 `debug` 配置文件的情况下启动服务。在之前的 `compose.yaml` 文件中，这将启动服务 `db`、`backend` 和 `phpmyadmin`。

### 启动多个配置文件

您也可以启用多个配置文件，例如通过 `docker compose --profile frontend --profile debug up`，配置文件 `frontend` 和 `debug` 将被启用。

可以通过传递多个 `--profile` 标志或为 `COMPOSE_PROFILES` 环境变量提供逗号分隔的列表来指定多个配置文件：

```console
$ docker compose --profile frontend --profile debug up
```

```console
$ COMPOSE_PROFILES=frontend,debug docker compose up
```

如果您想同时启用所有配置文件，可以运行 `docker compose --profile "*"`。

## 自动启动配置文件和依赖解析

当您在命令行中显式指定一个分配了一个或多个配置文件的服务时，您无需手动启用该配置文件，因为无论其配置文件是否激活，Compose 都会运行该服务。这对于运行一次性服务或调试工具非常有用。

仅启动目标服务（以及任何通过 `depends_on` 声明的依赖项）。共享相同配置文件的其他服务将不会被启动，除非：
- 它们也被显式指定，或者
- 显式使用 `--profile` 或 `COMPOSE_PROFILES` 启用了该配置文件。

当在命令行中显式指定一个分配了 `profiles` 的服务时，其配置文件会自动启动，因此您无需手动启动它们。这可用于一次性服务和调试工具。以下是一个配置示例：

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
# 仅启动 backend 和 db（不涉及配置文件）
$ docker compose up -d

# 运行 db-migrations 服务，无需手动启用 'tools' 配置文件
$ docker compose run db-migrations
```

在此示例中，`db-migrations` 虽然被分配到了 tools 配置文件中，但它仍然会运行，因为它是被显式指定的。`db` 服务也会自动启动，因为它列在 `depends_on` 中。

如果目标服务具有同样受配置文件限制的依赖项，您必须确保这些依赖项： 
 - 位于相同的配置文件中
 - 单独启动
 - 未分配给任何配置文件，从而始终处于启用状态

## 停止具有特定配置文件的应用程序和服务

与启动特定配置文件一样，您可以使用 `--profile` [命令行选项](/reference/cli/docker/compose.md#use--p-to-specify-a-project-name) 或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug down
```
```console
$ COMPOSE_PROFILES=debug docker compose down
```

这两个命令都会停止并移除具有 `debug` 配置文件的服务以及不带配置文件的服务。在以下 `compose.yaml` 文件中，这将停止服务 `db`、`backend` 和 `phpmyadmin`。

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
或 
```console 
$ docker compose stop phpmyadmin
```

> [!NOTE]
>
> 运行 `docker compose down` 将仅停止 `backend` 和 `db`。

## 参考信息

[`profiles`](/reference/compose-file/services.md#profiles)
