---
description: Compose 预定义环境变量
keywords: fig, composition, compose, docker, 编排, cli, 参考, compose 环境配置, docker 环境变量
title: 在 Docker Compose 中配置预定义的环境变量
linkTitle: 预定义环境变量
weight: 30
---

Docker Compose 包含多个预定义的环境变量。它还继承了常用的 Docker CLI 环境变量，如 `DOCKER_HOST` 和 `DOCKER_CONTEXT`。详情请参阅 [Docker CLI 环境变量参考](/reference/cli/docker/#environment-variables)。

本页解释了如何设置或更改以下预定义环境变量：

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

| 方法 | 描述 |
| ----------- | -------------------------------------------- |
| [`.env` 文件](/manuals/compose/how-tos/environment-variables/variable-interpolation.md) | 位于工作目录中。 |
| [Shell](variable-interpolation.md#substitute-from-the-shell)       | 在宿主机操作系统的 shell 中定义。 |
| CLI         | 在运行时通过 `--env` 或 `-e` 标志传递。 |

在更改或设置任何环境变量时，请注意 [环境变量优先级](envvars-precedence.md)。

## 配置详情

### 项目和文件配置

#### COMPOSE\_PROJECT\_NAME

设置项目名称。在启动时，此值会与服务名称一起作为前缀添加到容器名称中。

例如，如果您的项目名称是 `myapp` 且包含两个服务 `db` 和 `web` ，则 Compose 会分别启动名为 `myapp-db-1` 和 `myapp-web-1` 的容器。

Compose 可以通过不同方式设置项目名称。每种方法的优先级顺序（从高到低）如下：

1. `-p` 命令行标志 
2. `COMPOSE_PROJECT_NAME`
3. 配置文件中的顶级 `name:` 变量（或者在使用 `-f` 指定的一系列配置文件中的最后一个 `name:`）
4. 包含配置文件的项目目录的 `basename`（或者包含使用 `-f` 指定的第一个配置文件的目录的 `basename`）
5. 如果未指定配置文件，则为当前目录的 `basename`

项目名称只能包含小写字母、十进制数字、横杠和下划线，并且必须以小写字母或十进制数字开头。如果项目目录或当前目录的 `basename` 违反了此约束，您必须使用其他机制之一。

另请参阅 [命令行选项概览](/reference/cli/docker/compose/_index.md#command-options-overview-and-help) 和 [使用 `-p` 指定项目名称](/reference/cli/docker/compose/_index.md#use--p-to-specify-a-project-name)。

#### COMPOSE\_FILE

指定 Compose 文件的路径。支持指定多个 Compose 文件。

- 默认行为：如果未提供，Compose 会在当前目录中查找名为 `compose.yaml` 的文件；如果未找到，则递归搜索每个父目录，直到找到同名文件。
- 当指定多个 Compose 文件时，默认的路径分隔符为：
   - Mac 和 Linux：`:`（冒号）
   - Windows：`;`（分号）
   例如：

      ```console
      COMPOSE_FILE=compose.yaml:compose.prod.yaml
      ```  
   路径分隔符也可以使用 [`COMPOSE_PATH_SEPARATOR`](#compose_path_separator) 自定义。  

另请参阅 [命令行选项概览](/reference/cli/docker/compose/_index.md#command-options-overview-and-help) 和 [使用 `-f` 指定一个或多个 Compose 文件的名称和路径](/reference/cli/docker/compose/_index.md#use--f-to-specify-the-name-and-path-of-one-or-more-compose-files)。

#### COMPOSE\_PROFILES

指定在运行 `docker compose up` 时要启用的一个或多个配置文件 (profiles)。

具有匹配配置文件的服务以及未定义任何配置文件的服务将被启动。

例如，在设置 `COMPOSE_PROFILES=frontend` 的情况下调用 `docker compose up` 会选择带有 `frontend` 配置文件的服务以及任何未指定配置文件的服务。

如果指定多个配置文件，请使用逗号作为分隔符。

以下示例启用了所有匹配 `frontend` 和 `debug` 配置文件的服务以及不带配置文件的服务。 

```console
COMPOSE_PROFILES=frontend,debug
```

另请参阅 [在 Compose 中使用配置文件](../profiles.md) 和 [`--profile` 命令行选项](/reference/cli/docker/compose/_index.md#use-profiles-to-enable-optional-services)。

#### COMPOSE\_PATH\_SEPARATOR

为 `COMPOSE_FILE` 中列出的项目指定不同的路径分隔符。

- 默认值：
    - 在 macOS 和 Linux 上为 `:`
    - 在 Windows 上为 `;`

#### COMPOSE\_ENV\_FILES

指定如果不使用 `--env-file` 时，Compose 应使用的环境文件。

使用多个环境文件时，请使用逗号作为分隔符。例如： 

```console
COMPOSE_ENV_FILES=.env.envfile1, .env.envfile2
```

如果未设置 `COMPOSE_ENV_FILES` 且您未在 CLI 中提供 `--env-file`，则 Docker Compose 使用默认行为，即在项目目录中查找 `.env` 文件。

### 环境处理和容器生命周期

#### COMPOSE\_CONVERT\_WINDOWS\_PATHS

启用后，Compose 会在卷定义中执行从 Windows 风格到 Unix 风格的路径转换。

- 支持的值： 
    - `true` 或 `1`：启用
    - `false` 或 `0`：禁用
- 默认值：`0`

#### COMPOSE\_IGNORE\_ORPHANS

启用后，Compose 不会尝试检测项目的孤立（orphaned）容器。

- 支持的值： 
   - `true` 或 `1`：启用
   - `false` 或 `0`：禁用
- 默认值：`0`

#### COMPOSE\_REMOVE\_ORPHANS

启用后，Compose 在更新服务或栈时会自动移除孤立容器。孤立容器是指由之前的配置创建但当前 `compose.yaml` 文件中已不再定义的容器。

- 支持的值：
   - `true` 或 `1`：启用自动移除孤立容器
   - `false` 或 `0`：禁用自动移除。此时 Compose 会显示关于孤立容器的警告。
- 默认值：`0`

#### COMPOSE\_PARALLEL\_LIMIT

指定并发引擎调用的最大并行级别。

### 输出 (Output)

#### COMPOSE\_ANSI

指定何时打印 ANSI 控制字符。 

- 支持的值：
   - `auto`：Compose 检测是否可以使用 TTY 模式。否则使用纯文本模式。
   - `never`：使用纯文本模式
   - `always` 或 `0`：使用 TTY 模式
- 默认值：`auto`

#### COMPOSE\_STATUS\_STDOUT

启用后，Compose 会将其内部状态和进度消息写入 `stdout` 而不是 `stderr`。默认值为 false，以便清晰地分隔 Compose 消息与容器日志的输出流。

- 支持的值：
   - `true` 或 `1`：启用
   - `false` 或 `0`：禁用
- 默认值：`0`

#### COMPOSE\_PROGRESS

{{< summary-bar feature_name="Compose 进度" >}}

如果未使用 `--progress`，则定义进度输出的类型。 

支持的值包括 `auto`、`tty`、`plain`、`json` 和 `quiet`。默认值为 `auto`。 

### 用户体验

#### COMPOSE\_MENU

{{< summary-bar feature_name="Compose 菜单" >}}

启用后，Compose 会显示一个导航菜单，您可以选择在 Docker Desktop 中打开 Compose 栈、开启 [`watch` 模式](../file-watch.md) 或使用 [Docker Debug](/reference/cli/docker/debug.md)。

- 支持的值：
   - `true` 或 `1`：启用
   - `false` 或 `0`：禁用
- 默认值：如果您是通过 Docker Desktop 获取的 Docker Compose，则默认值为 `1`；否则默认值为 `0`。

#### COMPOSE\_EXPERIMENTAL

{{< summary-bar feature_name="Compose 实验性功能" >}}

这是一个选择性退出的变量。当关闭时，它将停用实验性功能。

- 支持的值：
   - `true` 或 `1`：启用
   - `false` 或 `0`：禁用
- 默认值：`1`

## Compose V2 不支持的变量

以下环境变量在 Compose V2 中无效。有关更多信息，请参阅 [迁移到 Compose V2](/manuals/compose/releases/migrate.md)。

- `COMPOSE_API_VERSION`
    默认情况下，API 版本是与服务器协商确定的。请使用 `DOCKER_API_VERSION`。参阅 [Docker CLI 环境变量参考](/reference/cli/docker/#environment-variables) 页面。
- `COMPOSE_HTTP_TIMEOUT`
- `COMPOSE_TLS_VERSION`
- `COMPOSE_FORCE_WINDOWS_HOST`
- `COMPOSE_INTERACTIVE_NO_CLI`
- `COMPOSE_DOCKER_CLI_BUILD`
    使用 `DOCKER_BUILDKIT` 在 BuildKit 和传统构建器之间进行选择。如果 `DOCKER_BUILDKIT=0`，则 `docker compose build` 使用传统构建器构建镜像。
