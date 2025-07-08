---
description: Compose 预定义环境变量
keywords: fig, composition, compose, docker, orchestration, cli, reference, compose environment configuration, docker env variables, 编排, 命令行, 参考, 环境配置, 环境变量
title: 在 Docker Compose 中配置预定义环境变量
linkTitle: 预定义环境变量
weight: 30
aliases:
- /compose/reference/envvars/
- /compose/environment-variables/envvars/
---

Docker Compose 包括几个预定义的环境变量。它还继承了常见的 Docker CLI 环境变量，例如 `DOCKER_HOST` 和 `DOCKER_CONTEXT`。有关详细信息，请参阅 [Docker CLI 环境变量参考](/reference/cli/docker/#environment-variables)。

本页介绍如何设置或更改以下预定义的环境变量：

- `COMPOSE_PROJECT_NAME`
- `COMPOSE_FILE`
- `COMPOSE_PROFILES`
- `COMPOSE_CONVERT_WINDOWS_PATHS`
- `COMPOSE_PATH_SEPARATOR`
- `COMPOSE_IGNORE_ORPHANS`
- `COMPOSE_REMOVE_ORPHANS`
- `COMPOSE_PARALLEL_LIMIT`
- `COMPOSE_ANSI`
- `COMPOSE_STATUS_STDOUT`
- `COMPOSE_ENV_FILES`
- `COMPOSE_MENU`
- `COMPOSE_EXPERIMENTAL`
- `COMPOSE_PROGRESS`

## 覆盖方法

| 方法      | 描述                                  |
| ----------- | -------------------------------------------- |
| [`.env` 文件](/manuals/compose/how-tos/environment-variables/variable-interpolation.md) | 位于工作目录中。            |
| [Shell](variable-interpolation.md#substitute-from-the-shell)       | 在主机操作系统 shell 中定义。  |
| CLI         | 在运行时使用 `--env` 或 `-e` 标志传递。 |

更改或设置任何环境变量时，请注意[环境变量优先级](envvars-precedence.md)。

## 配置详细信息

### 项目和文件配置

#### COMPOSE\_PROJECT\_NAME

设置项目名称。此值在启动时与服务名称一起作为容器名称的前缀。

例如，如果您的项目名称是 `myapp`，并且它包括两个服务 `db` 和 `web`，那么 Compose 会分别启动名为 `myapp-db-1` 和 `myapp-web-1` 的容器。

Compose 可以通过不同的方式设置项目名称。每种方法的优先级（从高到低）如下：

1. `-p` 命令行标志
2. `COMPOSE_PROJECT_NAME`
3. 配置文件中的顶级 `name:` 变量（或使用 `-f` 指定的一系列配置文件中的最后一个 `name:`）
4. 包含配置文件的项目目录的 `basename`（或包含使用 `-f` 指定的第一个配置文件的项目目录）
5. 如果未指定配置文件，则为当前目录的 `basename`

项目名称只能包含小写字母、十进制数字、破折号和下划线，并且必须以小写字母或十进制数字开��。如果项目目录或当前目录的 `basename` 违反此约束，则必须使用其他机制之一。

另请参阅[命令行选项概述](/reference/cli/docker/compose/_index.md#command-options-overview-and-help)和[使用 `-p` 指定项目名称](/reference/cli/docker/compose/_index.md#use--p-to-specify-a-project-name)。

#### COMPOSE\_FILE

指定 Compose 文件的路径。支持指定多个 Compose 文件。

- 默认行为：如果未提供，Compose 会在当前目录中查找名为 `compose.yaml` 的文件，如果未找到，则 Compose 会递归搜索每个父目录，直到找到该名称的文件。
- 指定多个 Compose 文件时，路径分隔符默认为：
   - Mac 和 Linux：`:`（冒号）
   - Windows：`;`（分号）
   例如：

      ```console
      COMPOSE_FILE=compose.yaml:compose.prod.yaml
      ```  
   路径分隔符也可以使用 [`COMPOSE_PATH_SEPARATOR`](#compose_path_separator) 进行自定义。

另请参阅[命令行选项概述](/reference/cli/docker/compose/_index.md#command-options-overview-and-help)和[使用 `-f` 指定一个或多个 Compose 文件的名称和路径](/reference/cli/docker/compose/_index.md#use--f-to-specify-the-name-and-path-of-one-or-more-compose-files)。

#### COMPOSE\_PROFILES

指定在运行 `docker compose up` 时要启用的一个或多个配置文件。

具有匹配配置文件的服务以及未定义配置文件的任何服务都将启动。

例如，使用 `COMPOSE_PROFILES=frontend` 调用 `docker compose up` 会选择具有 `frontend` 配置文件的服务以及未指定配置文件的任何服务。

如果指定多个配置文件，请使用逗号作为分隔符。

以下示例启用所有匹配 `frontend` 和 `debug` 配置文件的服务以及没有配置文件的服务。

```console
COMPOSE_PROFILES=frontend,debug
```

另请参阅[将配置文件与 Compose 一起使用](../profiles.md)和 [`--profile` 命令行选项](/reference/cli/docker/compose/_index.md#use-profiles-to-enable-optional-services)。

#### COMPOSE\_PATH\_SEPARATOR

为 `COMPOSE_FILE` 中列出的项目指定不同的路径分隔符。

- 默认为：
    - 在 macOS 和 Linux 上为 `:`
    - 在 Windows 上为 `;`

#### COMPOSE\_ENV\_FILES

指定如果未使用 `--env-file`，Compose 应使用哪些环境文件。

使用多个环境文件时，请使用逗号作为分隔符。例如：

```console
COMPOSE_ENV_FILES=.env.envfile1, .env.envfile2
```

如果未设置 `COMPOSE_ENV_FILES`，并且您未在 CLI 中提供 `--env-file`，则 Docker Compose 将使用默认行为，即在项目目录中查找 `.env` 文件。

### 环境处理和容器生命周期

#### COMPOSE\_CONVERT\_WINDOWS\_PATHS

启用后，Compose 会在卷定义中执行从 Windows 样式到 Unix 样式的路径转换。

- 支持的值：
    - `true` 或 `1`，启用
    - `false` 或 `0`，禁用
- 默认为：`0`

#### COMPOSE\_IGNORE\_ORPHANS

启用后，Compose 不会尝试检测项目的孤立容器。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：`0`

#### COMPOSE\_REMOVE\_ORPHANS

启用后，Compose 会在更新服务或堆栈时自动删除孤立容器。孤立容器是由先前配置创建但不再在当前 `compose.yaml` 文件中定义的容器。

- 支持的值：
   - `true` 或 `1`，启用自动删除孤立容器
   - `false` 或 `0`，禁用自动删除。Compose 会显示有关孤立容器的警告。
- 默认为：`0`

#### COMPOSE\_PARALLEL\_LIMIT

指定并发引擎调用的最大并行度。

### 输出

#### COMPOSE\_ANSI

指定何时打印 ANSI 控制字符。

- 支持的值：
   - `auto`，Compose 检测是否可以使用 TTY 模式。否则，使用纯文本模式
   - `never`，使用纯文本模式
   - `always` 或 `0`，使用 TTY 模式
- 默认为：`auto`

#### COMPOSE\_STATUS\_STDOUT

启用后，Compose 会将其内部状态和进度消息写入 `stdout` 而不是 `stderr`。
默认值为 false，以明确区分 Compose 消息和容器日志的输出流。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：`0`

#### COMPOSE\_PROGRESS

{{< summary-bar feature_name="Compose progress" >}}

定义进度输出的类型（如果未使用 `--progress`）。

支持的值为 `auto`、`tty`、`plain`、`json` 和 `quiet`。
默认为 `auto`。

### 用户体验

#### COMPOSE\_MENU

{{< summary-bar feature_name="Compose menu" >}}

启用后，Compose 会显示一个导航菜单，您可以在其中选择在 Docker Desktop 中打开 Compose 堆栈、打开 [`watch` 模式](../file-watch.md)或使用 [Docker Debug](/reference/cli/docker/debug.md)。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：如果您通过 Docker Desktop 获取 Docker Compose，则为 `1`，否则默认为 `0`

#### COMPOSE\_EXPERIMENTAL

{{< summary-bar feature_name="Compose experimental" >}}

这是一个选择退出的变量。关闭时，它会停用实验性功能。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：`1`

## Compose V2 中不支持

以下环境变量在 Compose V2 中无效。
有关更多信息，请参阅[迁移到 Compose V2](/manuals/compose/releases/migrate.md)。

- `COMPOSE_API_VERSION`
    默认情况下，API 版本与服务器协商。使用 `DOCKER_API_VERSION`。
    请参阅 [Docker CLI 环境变量参考](/reference/cli/docker/#environment-variables)页面。
- `COMPOSE_HTTP_TIMEOUT`
- `COMPOSE_TLS_VERSION`
- `COMPOSE_FORCE_WINDOWS_HOST`
- `COMPOSE_INTERACTIVE_NO_CLI`
- `COMPOSE_DOCKER_CLI_BUILD`
    使用 `DOCKER_BUILDKIT` 在 BuildKit 和经典构建器之间进行选择。如果 `DOCKER_BUILDKIT=0`，则 `docker compose build` 使用经典构建器来构建镜像。
