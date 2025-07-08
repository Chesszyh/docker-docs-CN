---
title: Docker Compose 中的环境变量优先级
linkTitle: 环境变量优先级
description: 说明 Compose 中如何解析环境变量的场景概述
keywords: compose, environment, env file, 环境, 环境变量文件
weight: 20
aliases:
- /compose/envvars-precedence/
- /compose/environment-variables/envvars-precedence/
---

当在多个源中设置相同的环境变量时，Docker Compose 会遵循优先级规则来确定容器环境中该变量的值。

本页介绍当在多个位置定义环境变量时，Docker Compose 如何确定该环境变量的最终值。

优先级顺序（从高到低）如下：
1. 在 CLI 中使用 [`docker compose run -e`](set-environment-variables.md#set-environment-variables-with-docker-compose-run---env) 设置。
2. 使用 `environment` 或 `env_file` 属性设置，但其值从您的 [shell](variable-interpolation.md#substitute-from-the-shell) 或环境文件（您的默认 [`.env` 文件](variable-interpolation.md#env-file) 或 CLI 中的 [`--env-file` 参数](variable-interpolation.md#substitute-with---env-file)）中插值。
3. 仅在 Compose 文件中使用 [`environment` 属性](set-environment-variables.md#use-the-environment-attribute)设置。
4. 在 Compose 文件中使用 [`env_file` 属性](set-environment-variables.md#use-the-env_file-attribute)。
5. 在容器镜像的 [ENV 指令](/reference/dockerfile.md#env)中设置。
   `Dockerfile` 中的任何 `ARG` 或 `ENV` 设置仅在没有 `environment`、`env_file` 或 `run --env` 的 Docker Compose 条目时才会评估。

## 简单示例

在以下示例中，在 `.env` 文件中和在 Compose 文件中使用 `environment` 属性为同一个环境变量设置了不同的值：

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

使用 `environment` 属性定义的环境变量优先。

```console
$ docker compose run webapp env | grep NODE_ENV
NODE_ENV=production
```

## 高级示例

下表以 `VALUE`（一个定义镜像版本的环境变量）为例。

### 表格如何工作

每列代表一个您可以设置值或替换 `VALUE` 值的上下文。

`Host OS environment` 和 `.env` 文件列仅用于说明目的。实际上，它们本身不会在容器中产生变量，而是与 `environment` 或 `env_file` 属性结合使用。

每行代表设置、替换或同时设置和替换 `VALUE` 的上下文组合。**结果**列表示每种情况下 `VALUE` 的最终值。

|  # |  `docker compose run`  |  `environment` 属性  |  `env_file` 属性  |  镜像 `ENV` |  `Host OS` 环境  |  `.env` 文件      |   结果  |
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

结果 1：本地环境优先，但 Compose 文件未设置为在容器内复制此变量，因此未设置此类变量。

结果 2：Compose 文件中的 `env_file` 属性为 `VALUE` 定义了一个显式值，因此容器环境会相应地设置。

结果 3：Compose 文件中的 `environment` 属性为 `VALUE` 定义了一个显式值，因此容器环境会相应地设置。

结果 4：镜像的 `ENV` 指令声明了变量 `VALUE`，并且由于 Compose 文件未设置为覆盖此值，因此此变量由镜像定义。

结果 5：`docker compose run` 命令设置了 `--env` 标志并带有显式值，并覆盖了镜像设置的值。

结果 6：`docker compose run` 命令设置了 `--env` 标志以从环境中复制值。主机操作系统值优先，并复制到容器的环境中。

结果 7：`docker compose run` 命令设置了 `--env` 标志以从环境中复制值。选择 `.env` 文件中的值来定义容器的环境。

结果 8：Compose 文件中的 `env_file` 属性设置为从本地环境复制 `VALUE`。主机操作系统值优先，并复制到容器的环境中。

结果 9：Compose 文件中的 `env_file` 属性设置为从本地环境复制 `VALUE`。选择 `.env` 文件中的值来定义容器的环境。

结果 10：Compose 文件中的 `environment` 属性设置为从本地环境复制 `VALUE`。主机操作系统值优先，并复制到容器的环境中。

结果 11：Compose 文件中的 `environment` 属性设置为从本地环境复制 `VALUE`。选择 `.env` 文件中的值来定义容器的环境。

结果 12：`--env` 标志的优先级高于 `environment` 和 `env_file` 属性，并设置为从本地环境复制 `VALUE`。主机操作系统值优先，并复制到容器的环境中。

结果 13 到 15：`--env` 标志的优先级高于 `environment` 和 `env_file` 属性，因此设置了该值。

## 后续步骤

- [在 Compose 中设置环境变量](set-environment-variables.md)
- [在 Compose 文件中使用变量插值](variable-interpolation.md)
