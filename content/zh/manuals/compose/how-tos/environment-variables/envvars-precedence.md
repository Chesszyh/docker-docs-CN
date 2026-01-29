---
title: Docker Compose 中的环境变量优先级
linkTitle: 环境变量优先级
description: 场景概览，演示了 Compose 中环境变量是如何解析的
keywords: compose, 环境, env 文件
weight: 20
aliases:
- /compose/envvars-precedence/
- /compose/environment-variables/envvars-precedence/
---

当同一个环境变量在多个来源中被设置时，Docker Compose 会遵循一套优先级规则来确定该变量在容器环境中的最终值。

本页解释了当环境变量在多个位置定义时，Docker Compose 如何确定其最终值。

优先级顺序（从高到低）如下：
1. 在 CLI 中使用 [`docker compose run -e`](set-environment-variables.md#set-environment-variables-with-docker-compose-run---env) 设置的值。
2. 使用 `environment` 或 `env_file` 属性设置，但其值是从 [shell](variable-interpolation.md#substitute-from-the-shell) 或环境文件（默认 [`.env` 文件](variable-interpolation.md#env-file)，或 CLI 中的 [`--env-file` 参数](variable-interpolation.md#substitute-with---env-file)）中插值得到的。
3. 仅在 Compose 文件中使用 [`environment` 属性](set-environment-variables.md#use-the-environment-attribute) 设置的值。
4. 在 Compose 文件中使用 [`env_file` 属性](set-environment-variables.md#use-the-env_file-attribute) 设置的值。
5. 在容器镜像的 [ENV 指令](/reference/dockerfile.md#env) 中设置的值。只有当 Docker Compose 中没有 `environment`、`env_file` 或 `run --env` 条目时，`Dockerfile` 中的 `ARG` 或 `ENV` 设置才会生效。

## 简单示例

在以下示例中，同一个环境变量在 `.env` 文件和 Compose 文件的 `environment` 属性中被赋予了不同的值：

```console
$ cat ./webapp.env
NODE_ENV=test

$ cat compose.yaml
services:
  webapp:
    image: 'webapp'
    env_file:
     - ./webapp.env
    environment:
     - NODE_ENV=production
```

使用 `environment` 属性定义的环境变量具有更高优先级。

```console
$ docker compose run webapp env | grep NODE_ENV
NODE_ENV=production
```

## 进阶示例 

下表以 `VALUE`（一个定义镜像版本的环境变量）为例进行说明。

### 表格说明

每一列代表一个可以设置或替换 `VALUE` 值的上下文。

“宿主机操作系统环境”和“.env 文件”列仅用于说明目的。实际上，它们本身并不会在容器中产生变量，而是需要配合 `environment` 或 `env_file` 属性使用。

每一行代表 `VALUE` 被设置或替换的上下文组合。**结果**列表示每种场景下 `VALUE` 的最终值。

|  # |  `docker compose run`  |  `environment` 属性  |  `env_file` 属性  |  镜像 `ENV` |  `宿主机` 环境  |  `.env` 文件      |   结果  |
|:--:|:----------------:|:-------------------------------:|:----------------------:|:------------:|:-----------------------:|:-----------------:|:----------:|
|  1 |   -              |   -                             |   -                    |   -          |  `VALUE=1.4`            |  `VALUE=1.3`      | -               |
|  2 |   -              |   -                             |  `VALUE=1.6`           |  `VALUE=1.5` |  `VALUE=1.4`            |   -               |**`VALUE=1.6`**  |
|  3 |   -              |  `VALUE=1.7`                    |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |   -               |**`VALUE=1.7`**  |
|  4 |   -              |   -                             |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.5`**  |
|  5 |`--env VALUE=1.8` |   -                             |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |
|  6 |`--env VALUE`     |   -                             |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
|  7 |`--env VALUE`     |   -                             |   -                    |  `VALUE=1.5` |   -                     |  `VALUE=1.3`      |**`VALUE=1.3`**  |
|  8 |   -              |   -                             |   `VALUE`              |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
|  9 |   -              |   -                             |   `VALUE`              |  `VALUE=1.5` |   -                     |  `VALUE=1.3`      |**`VALUE=1.3`**  |
| 10 |   -              |  `VALUE`                        |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
| 11 |   -              |  `VALUE`                        |   -                    |  `VALUE=1.5` |  -                      |  `VALUE=1.3`      |**`VALUE=1.3`**  |
| 12 |`--env VALUE`     |  `VALUE=1.7`                    |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
| 13 |`--env VALUE=1.8` |  `VALUE=1.7`                    |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |
| 14 |`--env VALUE=1.8` |   -                             |  `VALUE=1.6`           |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |
| 15 |`--env VALUE=1.8` |  `VALUE=1.7`                    |  `VALUE=1.6`           |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |

### 理解优先级结果

结果 1：本地环境具有优先级，但 Compose 文件未设置为在容器内复制此变量，因此没有设置该变量。

结果 2：Compose 文件中的 `env_file` 属性为 `VALUE` 定义了显式值，因此容器环境据此进行设置。

结果 3：Compose 文件中的 `environment` 属性为 `VALUE` 定义了显式值，因此容器环境据此进行设置。

结果 4：镜像的 `ENV` 指令声明了变量 `VALUE`，由于 Compose 文件未设置为覆盖此值，因此该变量由镜像定义。

结果 5：`docker compose run` 命令设置了具有显式值的 `--env` 标志，并覆盖了镜像设置的值。 

结果 6：`docker compose run` 命令设置了 `--env` 标志以复制环境中的值。宿主机操作系统的数值具有优先级，并被复制到容器环境中。

结果 7：`docker compose run` 命令设置了 `--env` 标志以复制环境中的值。选择了来自 `.env` 文件中的值来定义容器环境。

结果 8：Compose 文件中的 `env_file` 属性被设置为从本地环境复制 `VALUE`。宿主机操作系统的数值具有优先级，并被复制到容器环境中。

结果 9：Compose 文件中的 `env_file` 属性被设置为从本地环境复制 `VALUE`。选择了来自 `.env` 文件中的值来定义容器环境。

结果 10：Compose 文件中的 `environment` 属性被设置为从本地环境复制 `VALUE`。宿主机操作系统的数值具有优先级，并被复制到容器环境中。

结果 11：Compose 文件中的 `environment` 属性被设置为从本地环境复制 `VALUE`。选择了来自 `.env` 文件中的值来定义容器环境。

结果 12：`--env` 标志的优先级高于 `environment` 和 `env_file` 属性，并被设置为从本地环境复制 `VALUE`。宿主机操作系统的数值具有优先级，并被复制到容器环境中。

结果 13 到 15：`--env` 标志的优先级高于 `environment` 和 `env_file` 属性，因此由它设置该数值。 

## 下一步

- [在 Compose 中设置环境变量](set-environment-variables.md)
- [在 Compose 文件中使用变量插值](variable-interpolation.md)
