--- 
title: 在 Compose 文件中通过插值设置、使用和管理变量
linkTitle: 插值 (Interpolation)
description: 了解如何通过插值在 Compose 文件中设置、使用和管理变量
keywords: compose, 编排, 环境, 变量, 插值
weight: 40
---

Compose 文件可以使用变量来提供更大的灵活性。如果您想快速切换镜像标签以测试多个版本，或者想根据本地环境调整卷（volume）源，您无需每次都编辑 Compose 文件，只需设置变量，在运行时将值插入到 Compose 文件中即可。

插值也可以用于在运行时将值插入到 Compose 文件中，随后这些值可用于将变量传递到容器环境中。

以下是一个简单的示例： 

```console
$ cat .env
TAG=v1.5
$ cat compose.yaml
services:
  web:
    image: "webapp:${TAG}"
```

当您运行 `docker compose up` 时，Compose 文件中定义的 `web` 服务会将镜像 [插值](variable-interpolation.md) 为 `.env` 文件中设置的 `webapp:v1.5`。您可以使用 [config 命令](/reference/cli/docker/compose/config.md) 来验证这一点，它会将解析后的应用程序配置打印到终端：

```console
$ docker compose config
services:
  web:
    image: 'webapp:v1.5'
```

## 插值语法

插值适用于未加引号和双引号的值。支持大括号形式 (`${VAR}`) 和无大括号形式 (`$VAR`) 的表达式。

对于大括号表达式，支持以下格式：
- 直接替换
  - `${VAR}` -> `VAR` 的值
- 默认值
  - `${VAR:-default}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则为 `default`
  - `${VAR-default}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则为 `default`
- 必需值
  - `${VAR:?error}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则报错退出
  - `${VAR?error}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则报错退出
- 替代值
  - `${VAR:+replacement}` -> 如果 `VAR` 已设置且非空，则为 `replacement`，否则为空
  - `${VAR+replacement}` -> 如果 `VAR` 已设置，则为 `replacement`，否则为空

有关更多信息，请参阅 Compose 规范中的 [插值 (Interpolation)](/reference/compose-file/interpolation.md)。 

## 通过插值设置变量的方式

Docker Compose 可以从多个来源将变量插值到您的 Compose 文件中。 

请注意，当同一个变量由多个来源声明时，适用优先级规则：

1. 来自 shell 环境的变量
2. 如果未设置 `--env-file`，则为本地工作目录 (`PWD`) 下 `.env` 文件中设置的变量
3. 来自由 `--env-file` 指定的文件或项目目录下的 `.env` 文件中的变量

您可以通过运行 `docker compose config --environment` 来查看 Compose 用于插值模型的变量和值。

### `.env` 文件

Docker Compose 中的 `.env` 文件是一个文本文件，用于定义运行 `docker compose up` 时可供插值的变量。此文件通常包含变量的键值对，它允许您在一个地方集中管理配置。如果您有多个变量需要存储，`.env` 文件非常有用。

`.env` 文件是设置变量的默认方法。`.env` 文件应放在项目目录的根目录下，紧邻 `compose.yaml` 文件。有关环境文件格式的更多信息，请参阅 [环境文件语法](#env-文件语法)。

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

#### 补充信息 

- 如果您在 `.env` 文件中定义了变量，可以使用 [`environment` 属性](/reference/compose-file/services.md#environment) 在 `compose.yaml` 中直接引用它。例如，如果您的 `.env` 文件包含环境变量 `DEBUG=1` 且您的 `compose.yaml` 文件如下所示：
   ```yaml
    services:
      webapp:
        image: my-webapp-image
        environment:
          - DEBUG=${DEBUG}
   ```
   Docker Compose 会将 `${DEBUG}` 替换为来自 `.env` 文件中的值。

   > [!IMPORTANT] 
   > 
   > 当使用 `.env` 文件中的变量作为容器环境中的环境变量时，请注意 [环境变量优先级](envvars-precedence.md)。

- 您可以将 `.env` 文件放在项目根目录以外的位置，然后使用 [CLI 中的 `--env-file` 选项](#使用-env-file-进行替换)，以便 Compose 可以找到它。

- 如果使用 [`--env-file` 替换](#使用-env-file-进行替换)，您的 `.env` 文件可以被另一个 `.env` 文件覆盖。

> [!IMPORTANT] 
> 
> 从 `.env` 文件进行替换是 Docker Compose CLI 的一项功能。
> 
> 运行 `docker stack deploy` 时，Swarm 不支持此功能。

#### `.env` 文件语法

以下语法规则适用于环境文件：

- 以 `#` 开头的行被视为注释并被忽略。
- 空行被忽略。
- 未加引号和双引号 (`"`) 的值会应用插值。
- 每行代表一个键值对。值可以选加引号。
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
- 未加引号值的行内注释必须前置空格。
  - `VAR=VAL # 注释` -> `VAL`
  - `VAR=VAL# 不是注释` -> `VAL# 不是注释`
- 加引号值的行内注释必须跟在闭合引号之后。
  - `VAR="VAL # 不是注释"` -> `VAL # 不是注释`
  - `VAR="VAL" # 注释` -> `VAL`
- 单引号 (`'`) 的值按原样使用。
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- 引号可以使用 `\` 进行转义。
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- 双引号值支持常见的 shell 转义序列，包括 `\n`、`\r`、`\t` 和 `\\`。 
  - `VAR="some\tvalue"` -> `some  value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`
- 单引号值可以跨越多行。示例：

   ```yaml
   KEY='SOME
   VALUE'
   ```

   如果您运行 `docker compose config` ，您会看到：
  
   ```yaml
   environment:
     KEY: |-
       SOME
       VALUE
   ```

### 使用 `--env-file` 进行替换

您可以在 `.env` 文件中为多个环境变量设置默认值，然后将该文件作为参数传递给 CLI。

这种方法的优点是您可以将文件存储在任何位置并适当命名。该文件路径是相对于执行 Docker Compose 命令的当前工作目录的。通过使用 `--env-file` 选项来传递文件路径：

```console
$ docker compose --env-file ./config/.env.dev up
```

#### 补充信息 

- 如果您想临时覆盖 `compose.yaml` 文件中已经引用的 `.env` 文件，此方法非常有用。例如，您可能拥有针对生产环境 (`.env.prod`) 和测试环境 (`.env.test`) 的不同 `.env` 文件。在以下示例中，有两个环境文件 `.env` 和 `.env.dev`。它们都为 `TAG` 设置了不同的值。
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
  当作为 `--env-file` 参数传递的文件路径无效时，Compose 会返回错误：
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

### 本地 `.env` 文件与 <项目目录> `.env` 文件的对比

`.env` 文件也可用于声明用于控制 Compose 行为和要加载文件的 [预定义环境变量](envvars.md)。 

在不带显式 `--env-file` 标志的情况下执行时，Compose 会在您的工作目录 ([PWD](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-PWD)) 中搜索 `.env` 文件，并加载用于自身配置和插值的值。如果此文件中的值定义了 `COMPOSE_FILE` 预定义变量，导致项目目录被设置为另一个文件夹，那么 Compose 会加载第二个 `.env` 文件（如果存在）。这第二个 `.env` 文件的优先级较低。 

这种机制使得可以使用一组自定义变量作为覆盖来调用现有的 Compose 项目，而无需通过命令行传递环境变量。 

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

### 从 shell 进行替换

You can use environment variables that already exist on the host or in the shell where you execute the `docker compose` command. This allows you to dynamically inject values into your Docker Compose configuration at runtime.
For example, suppose your shell contains `POSTGRES_VERSION=9.3` and you provide the following configuration:

```yaml
db:
  image: "postgres:${POSTGRES_VERSION}"
```

When you run `docker compose up` with this configuration, Compose looks for the `POSTGRES_VERSION` environment variable in your shell and substitutes its value. In this example, Compose resolves the image to `postgres:9.3` before running the configuration.

If an environment variable is not set, Compose substitutes an empty string. In the preceding example, if `POSTGRES_VERSION` is not set, the value of the image option becomes `postgres:`.

> [!NOTE] 
> 
> `postgres:` is not a valid image reference. Docker expects either a reference without a tag (e.g., `postgres`, which defaults to the `latest` tag) or a reference with a tag (e.g., `postgres:15`).
```