---
title: 使用插值在 Compose 文件中设置、使用和管理变量
linkTitle: 插值
description: 如何使用插值在您的 Compose 文件中设置、使用和管理变量
keywords: compose, orchestration, environment, variables, interpolation, 编排, 环境, 变量, 插值
weight: 40
aliases:
- /compose/env-file/
- /compose/environment-variables/env-file/
- /compose/environment-variables/variable-interpolation/
---

Compose 文件可以使用变量来提供更大的灵活性。如果您想在镜像标签之间快速切换以测试多个版本，或者想根据您的本地环境调整卷源，您无需每次都编辑 Compose 文件，只需设置变量即可在运行时将值插入到您的 Compose 文件中。

插值还可用于在运行时将值插入到您的 Compose 文件中，然后用于将变量传递到容器的环境中。

下面是一个简单的示例：

```console
$ cat .env
TAG=v1.5
$ cat compose.yaml
services:
  web:
    image: "webapp:${TAG}"
```

当您运行 `docker compose up` 时，在 Compose 文件中定义的 `web` 服��会[插值](variable-interpolation.md)到在 `.env` 文件中设置的镜像 `webapp:v1.5` 中。您可以使用 [config 命令](/reference/cli/docker/compose/config.md)来验证这一点，该命令会将您解析的应用程序配置打印到终端：

```console
$ docker compose config
services:
  web:
    image: 'webapp:v1.5'
```

## 插值语法

插值适用于未加引号和双引号的值。
支持带括号 (`${VAR}`) 和不带括号 (`$VAR`) 的表达式。

对于带括号的表达式，支持以下格式：
- 直接替换
  - `${VAR}` -> `VAR` 的值
- 默认值
  - `${VAR:-default}` -> 如果设置了 `VAR` 且非空，则为 `VAR` 的值，否则为 `default`
  - `${VAR-default}` -> 如果设置了 `VAR`，则为 `VAR` 的值，否则为 `default`
- 必需值
  - `${VAR:?error}` -> 如果设置了 `VAR` 且非空，则为 `VAR` 的值，否则退出并显示错误
  - `${VAR?error}` -> 如果设置了 `VAR`，则为 `VAR` 的值，否则退出并显示错误
- 替代值
  - `${VAR:+replacement}` -> 如果设置了 `VAR` 且非空，则为 `replacement`，否则为空
  - `${VAR+replacement}` -> 如果设置了 `VAR`，则为 `replacement`，否则为空

有关更多信息，请参阅 Compose 规范中的[插值](/reference/compose-file/interpolation.md)。

## 使用插值设置变量的方法

Docker Compose 可以从多个来源将变量插值到您的 Compose 文件中。

请注意，当多个来源声明同一个变量时，将应用优先级：

1. 来自您的 shell 环境的变量
2. 如果未设置 `--env-file`，则由本地工作目录 (`PWD`) 中的 `.env` 文件设置的变量
3. 由 `--env-file` 设置的文件或项目目录中的 `.env` 文件中的变量

您可以通过运行 `docker compose config --environment` 来检查 Compose 用于插值 Compose 模型的变量和值。

### `.env` 文件

Docker Compose 中的 `.env` 文件是一个文本文件，用于定义在运行 `docker compose up` 时应可用于插值的变量。此文件通常包含变量的键值对，并允许您在一个地方集中和管理配置。如果您需要存储多个变量，`.env` 文件非常有用。

`.env` 文件是设置变量的默认方法。`.env` 文件应放置在项目目录的根目录下，与您的 `compose.yaml` 文件相邻。有关格式化环境文件的更多信息，请参阅[环境文件语法](#env-file-syntax)。

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

- 如果您在 `.env` 文件中定义了一个变量，您可以使用 [`environment` 属性](/reference/compose-file/services.md#environment)直接在您的 `compose.yaml` 中引用它。例如，如果您的 `.env` 文件包含环境变量 `DEBUG=1`，并且您的 `compose.yaml` 文件如下所示：
   ```yaml
    services:
      webapp:
        image: my-webapp-image
        environment:
          - DEBUG=${DEBUG}
   ```
   Docker Compose 会将 `${DEBUG}` 替换为 `.env` 文件中的值。

   > [!IMPORTANT]
   >
   > 在 `.env` 文件中使用变量作为容器环境中的环境变量时，请注意[环境变量优先级](envvars-precedence.md)。

- 您可以将 `.env` 文件放置在项目目录根目录以外的位置，然后使用 CLI 中的 [`--env-file` 选项](#substitute-with---env-file)，以便 Compose 可以导航到它。

- 如果您的 `.env` 文件被另一个 `.env` 文件[用 `--env-file` 替换](#substitute-with---env-file)，则它可能会被覆盖。

> [!IMPORTANT]
>
> 从 `.env` 文件进行替换是 Docker Compose CLI 的一项功能。
>
> 在运行 `docker stack deploy` 时，Swarm 不支持此功能。

#### `.env` 文件语法

以下语法规则适用于环境文件：

- 以 `#` 开头的行被视为空白并被忽略。
- 空行将被忽略。
- 未加引号和双引号 (`"`) 的值将应用插值。
- 每行代表一个键值对。值可以选择性地加引号。
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
- 未加引号值的内联注释必须以空格开头。
  - `VAR=VAL # comment` -> `VAL`
  - `VAR=VAL# not a comment` -> `VAL# not a comment`
- 带引号值的内联注释必须跟在右引号后面。
  - `VAR="VAL # not a comment"` -> `VAL # not a comment`
  - `VAR="VAL" # comment` -> `VAL`
- 单引号 (`'`) 的值按字面意思使用。
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- 引号可以用 `\` 转义。
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- 双引号值中支持常见的 shell 转义序列，包括 `\n`、`\r`、`\t` 和 `\\`。
  - `VAR="some\tvalue"` -> `some  value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`
- 单引号值可以跨越多行。示例：

   ```yaml
   KEY='SOME
   VALUE'
   ```

   如果您随后运行 `docker compose config`，您将看到：
  
   ```yaml
   environment:
     KEY: |-
       SOME
       VALUE
   ```

### 使用 `--env-file` 替换

您可以在 `.env` 文件中为多个环境变量设置默认值，然后将该文件作为参数在 CLI 中传递。

此方法的优点是您可以将文件存储在任何地方并适当地命名它，例如，此文件路径相对于执行 Docker Compose 命令的当前工作目录。传递文件路径是使用 `--env-file` 选项完成的：

```console
$ docker compose --env-file ./config/.env.dev up
```

#### 附加信息

- 如果您想临时覆盖已在 `compose.yaml` 文件中引用的 `.env` 文件，此方法非常有用。例如，您可能对生产 (`.env.prod`) 和测试 (`.env.test`) 有不同的 `.env` 文件。
  在以下示例中，有两个环境文件 `.env` 和 `.env.dev`。两者都为 `TAG` 设置了不同的值。
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
  当将无效的文件路径作为 `--env-file` 参数传递时，Compose 会返回错误：
  ```console
  $ docker compose --env-file ./doesnotexist/.env.dev  config
  ERROR: Couldn't find env file: /home/user/./doesnotexist/.env.dev
  ```
- 您可以使用多个 `--env-file` 选项来指定多个环境文件，Docker Compose 会按顺序读取它们。后面的文件可以覆盖前面文件中的变量。
  ```console
  $ docker compose --env-file .env --env-file .env.override up
  ```
- 您可以在启动容器时从命令行覆盖特定的环境变量。
  ```console
  $ docker compose --env-file .env.dev up -e DATABASE_URL=mysql://new_user:new_password@new_db:3306/new_database
  ```

### 本地 `.env` 文件与 &lt;项目目录&gt; `.env` 文件

`.env` 文件还可用于声明用于控制 Compose 行为和要加载的文件的[预定义环境变量](envvars.md)。

当在没有显式 `--env-file` 标志的情况下执行时，Compose 会在您的工作目录 ([PWD](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-PWD)) 中搜索 `.env` 文件并加载值
用于自配置和插值。如果此文件中的值定义了 `COMPOSE_FILE` 预定义变量，这会导致项目目录设置为另一个文件夹，
Compose 将加载第二个 `.env` 文件（如果存在）。第二个 `.env` 文件的优先级较���。

此机制使得可以使用一组自定义变量作为覆盖来调用现有的 Compose 项目，而无需通过命令行传递环境变量。

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

您可以使用主机或执行 `docker compose` 命令的 shell 环境中的现有环境变量。这使您可以在运行时将值动态注入到您的 Docker Compose 配置中。
例如，假设 shell 包含 `POSTGRES_VERSION=9.3` 并且您提供了以下配置：

```yaml
db:
  image: "postgres:${POSTGRES_VERSION}"
```

当您使用此配置运行 `docker compose up` 时，Compose 会在 shell 中查找 `POSTGRES_VERSION` 环境变量并替换其值。对于此示例，Compose 在运行配置之前将镜像解析为 `postgres:9.3`。

如果未设置环境变量，Compose 会用空字符串替换。在前面的示例中，如果未设置 `POSTGRES_VERSION`，则镜像选项的值为 `postgres:`。

> [!NOTE]
>
> `postgres:` 不是有效的镜像引用。Docker 期望要么是没有标签的引用，比如 `postgres`，它默认为最新镜像，要么是带有标签的引用，比如 `postgres:15`。
