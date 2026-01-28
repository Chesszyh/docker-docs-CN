---
title: 使用插值在 Compose 文件中设置、使用和管理变量
linkTitle: 插值
description: 如何在 Compose 文件中使用插值设置、使用和管理变量
keywords: compose, orchestration, environment, variables, interpolation
weight: 40
aliases:
- /compose/env-file/
- /compose/environment-variables/env-file/
- /compose/environment-variables/variable-interpolation/
---

Compose 文件可以使用变量来提供更大的灵活性。如果你想快速切换镜像标签以测试多个版本，或者想根据本地环境调整卷源，你不需要每次都编辑 Compose 文件，只需设置变量，在运行时将值插入到 Compose 文件中。

插值还可用于在运行时将值插入到 Compose 文件中，然后用于将变量传递到容器的环境中。

下面是一个简单的示例：

```console
$ cat .env
TAG=v1.5
$ cat compose.yaml
services:
  web:
    image: "webapp:${TAG}"
```

当你运行 `docker compose up` 时，Compose 文件中定义的 `web` 服务会[插值](variable-interpolation.md)镜像 `webapp:v1.5`，该值是在 `.env` 文件中设置的。你可以使用
[config 命令](/reference/cli/docker/compose/config.md)验证这一点，该命令会将解析后的应用程序配置打印到终端：

```console
$ docker compose config
services:
  web:
    image: 'webapp:v1.5'
```

## 插值语法

插值适用于未加引号和双引号的值。
支持带花括号（`${VAR}`）和不带花括号（`$VAR`）两种表达式。

对于带花括号的表达式，支持以下格式：
- 直接替换
  - `${VAR}` -> `VAR` 的值
- 默认值
  - `${VAR:-default}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则为 `default`
  - `${VAR-default}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则为 `default`
- 必需值
  - `${VAR:?error}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则以错误退出
  - `${VAR?error}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则以错误退出
- 替代值
  - `${VAR:+replacement}` -> 如果 `VAR` 已设置且非空，则为 `replacement`，否则为空
  - `${VAR+replacement}` -> 如果 `VAR` 已设置，则为 `replacement`，否则为空

有关更多信息，请参阅 Compose 规范中的[插值](/reference/compose-file/interpolation.md)。

## 使用插值设置变量的方法

Docker Compose 可以从多个来源将变量插值到 Compose 文件中。

请注意，当同一变量由多个来源声明时，会应用优先级：

1. 来自 shell 环境的变量
2. 如果未设置 `--env-file`，则为本地工作目录（`PWD`）中 `.env` 文件设置的变量
3. 由 `--env-file` 设置的文件或项目目录中的 `.env` 文件中的变量

你可以通过运行 `docker compose config --environment` 检查 Compose 用于插值 Compose 模型的变量和值。

### `.env` 文件

Docker Compose 中的 `.env` 文件是一个文本文件，用于定义在运行 `docker compose up` 时应可用于插值的变量。此文件通常包含变量的键值对，它允许你在一个地方集中和管理配置。如果你有多个需要存储的变量，`.env` 文件非常有用。

`.env` 文件是设置变量的默认方法。`.env` 文件应放在 `compose.yaml` 文件旁边的项目根目录中。有关环境文件格式的更多信息，请参阅[环境文件语法](#env-file-syntax)。

基本示例：

```console
$ cat .env
## 根据 DEV_MODE 定义 COMPOSE_DEBUG，默认为 false
COMPOSE_DEBUG=${DEV_MODE:-false}

$ cat compose.yaml
  services:
    webapp:
      image: my-webapp-image
      environment:
        - DEBUG=${COMPOSE_DEBUG}

$ DEV_MODE=true docker compose config
services:
  webapp:
    environment:
      DEBUG: "true"
```

#### 附加信息

- 如果你在 `.env` 文件中定义了一个变量，你可以在 `compose.yaml` 中使用 [`environment` 属性](/reference/compose-file/services.md#environment)直接引用它。例如，如果你的 `.env` 文件包含环境变量 `DEBUG=1`，而你的 `compose.yaml` 文件如下所示：
   ```yaml
    services:
      webapp:
        image: my-webapp-image
        environment:
          - DEBUG=${DEBUG}
   ```
   Docker Compose 会将 `${DEBUG}` 替换为 `.env` 文件中的值

   > [!IMPORTANT]
   >
   > 当使用 `.env` 文件中的变量作为容器环境中的环境变量时，请注意[环境变量优先级](envvars-precedence.md)。

- 你可以将 `.env` 文件放在项目根目录以外的位置，然后在 CLI 中使用 [`--env-file` 选项](#substitute-with---env-file)让 Compose 找到它。

- 你的 `.env` 文件可以被另一个 `.env` 文件覆盖，如果它[使用 `--env-file` 替换](#substitute-with---env-file)。

> [!IMPORTANT]
>
> 从 `.env` 文件替换是 Docker Compose CLI 功能。
>
> 运行 `docker stack deploy` 时 Swarm 不支持此功能。

#### `.env` 文件语法

以下语法规则适用于环境文件：

- 以 `#` 开头的行被处理为注释并被忽略。
- 空白行被忽略。
- 未加引号和双引号（`"`）的值会应用插值。
- 每行表示一个键值对。值可以选择性地加引号。
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
- 未加引号值的行内注释必须以空格开头。
  - `VAR=VAL # comment` -> `VAL`
  - `VAR=VAL# not a comment` -> `VAL# not a comment`
- 加引号值的行内注释必须在结束引号之后。
  - `VAR="VAL # not a comment"` -> `VAL # not a comment`
  - `VAR="VAL" # comment` -> `VAL`
- 单引号（`'`）的值按字面意思使用。
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- 引号可以用 `\` 转义。
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- 双引号值中支持常见的 shell 转义序列，包括 `\n`、`\r`、`\t` 和 `\\`。
  - `VAR="some\tvalue"` -> `some  value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`
- 单引号值可以跨多行。示例：

   ```yaml
   KEY='SOME
   VALUE'
   ```

   如果你随后运行 `docker compose config`，你会看到：

   ```yaml
   environment:
     KEY: |-
       SOME
       VALUE
   ```

### 使用 `--env-file` 替换

你可以在 `.env` 文件中为多个环境变量设置默认值，然后在 CLI 中将该文件作为参数传递。

此方法的优点是你可以将文件存储在任何位置并适当命名，例如，
此文件路径相对于执行 Docker Compose 命令的当前工作目录。使用 `--env-file` 选项传递文件路径：

```console
$ docker compose --env-file ./config/.env.dev up
```

#### 附加信息

- 如果你想临时覆盖 `compose.yaml` 文件中已引用的 `.env` 文件，此方法很有用。例如，你可能有不同的 `.env` 文件用于生产（`.env.prod`）和测试（`.env.test`）。
  在以下示例中，有两个环境文件，`.env` 和 `.env.dev`。两者为 `TAG` 设置了不同的值。
  ```console
  $ cat .env
  TAG=v1.5
  $ cat ./config/.env.dev
  TAG=v1.6
  $ cat compose.yaml
  services:
    web:
      image: "webapp:${TAG}"
  ```
  如果命令行中未使用 `--env-file`，则默认加载 `.env` 文件：
  ```console
  $ docker compose config
  services:
    web:
      image: 'webapp:v1.5'
  ```
  传递 `--env-file` 参数会覆盖默认文件路径：
  ```console
  $ docker compose --env-file ./config/.env.dev config
  services:
    web:
      image: 'webapp:v1.6'
  ```
  当传递无效的文件路径作为 `--env-file` 参数时，Compose 返回错误：
  ```console
  $ docker compose --env-file ./doesnotexist/.env.dev  config
  ERROR: Couldn't find env file: /home/user/./doesnotexist/.env.dev
  ```
- 你可以使用多个 `--env-file` 选项指定多个环境文件，Docker Compose 按顺序读取它们。后面的文件可以覆盖前面文件中的变量。
  ```console
  $ docker compose --env-file .env --env-file .env.override up
  ```
- 你可以在启动容器时从命令行覆盖特定的环境变量。
  ```console
  $ docker compose --env-file .env.dev up -e DATABASE_URL=mysql://new_user:new_password@new_db:3306/new_database
  ```

### 本地 `.env` 文件与 &lt;project directory&gt; `.env` 文件

`.env` 文件也可用于声明[预定义环境变量](envvars.md)，用于控制 Compose 行为和要加载的文件。

当没有明确的 `--env-file` 标志执行时，Compose 在你的工作目录（[PWD](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-PWD)）中搜索 `.env` 文件并加载值，
用于自身配置和插值。如果此文件中的值定义了 `COMPOSE_FILE` 预定义变量，导致项目目录设置为另一个文件夹，
Compose 将加载第二个 `.env` 文件（如果存在）。这个第二个 `.env` 文件具有较低的优先级。

此机制使得可以使用自定义变量集作为覆盖来调用现有的 Compose 项目，而无需通过命令行传递环境变量。

```console
$ cat .env
COMPOSE_FILE=../compose.yaml
POSTGRES_VERSION=9.3

$ cat ../compose.yaml
services:
  db:
    image: "postgres:${POSTGRES_VERSION}"
$ cat ../.env
POSTGRES_VERSION=9.2

$ docker compose config
services:
  db:
    image: "postgres:9.3"
```

### 从 shell 替换

你可以使用主机上的现有环境变量或执行 `docker compose` 命令的 shell 环境中的变量。这允许你在运行时动态地将值注入到 Docker Compose 配置中。
例如，假设 shell 包含 `POSTGRES_VERSION=9.3`，并且你提供以下配置：

```yaml
db:
  image: "postgres:${POSTGRES_VERSION}"
```

当你使用此配置运行 `docker compose up` 时，Compose 在 shell 中查找 `POSTGRES_VERSION` 环境变量并替换其值。在此示例中，Compose 在运行配置之前将镜像解析为 `postgres:9.3`。

如果未设置环境变量，Compose 使用空字符串替换。在前面的示例中，如果未设置 `POSTGRES_VERSION`，则镜像选项的值为 `postgres:`。

> [!NOTE]
>
> `postgres:` 不是有效的镜像引用。Docker 期望要么是不带标签的引用（如 `postgres`，默认为最新镜像），要么是带标签的引用（如 `postgres:15`）。


