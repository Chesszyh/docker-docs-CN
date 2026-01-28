---
title: 在容器环境中设置环境变量
linkTitle: 设置环境变量
weight: 10
description: 如何使用 Compose 设置、使用和管理环境变量
keywords: compose, orchestration, environment, environment variables, container environment variables
aliases:
- /compose/env/
- /compose/link-env-deprecated/
- /compose/environment-variables/set-environment-variables/
---

除非在服务配置中有明确的条目，否则容器的环境不会被设置。使用 Compose，你可以通过 Compose 文件以两种方式在容器中设置环境变量。

>[!TIP]
>
> 不要使用环境变量将敏感信息（如密码）传递到容器中。请改用 [secrets](../use-secrets.md)。


## 使用 `environment` 属性

你可以使用 `compose.yaml` 中的
[`environment` 属性](/reference/compose-file/services.md#environment)直接在容器环境中设置环境变量。

它支持列表和映射两种语法：

```yaml
services:
  webapp:
    environment:
      DEBUG: "true"
```
等同于
```yaml
services:
  webapp:
    environment:
      - DEBUG=true
```

有关如何使用它的更多示例，请参阅 [`environment` 属性](/reference/compose-file/services.md#environment)。

### 附加信息

- 你可以选择不设置值，直接将环境变量从 shell 传递到容器。它的工作方式与 `docker run -e VARIABLE ...` 相同：
  ```yaml
  web:
    environment:
      - DEBUG
  ```
容器中 `DEBUG` 变量的值取自运行 Compose 的 shell 中同名变量的值。注意，如果 shell 环境中的 `DEBUG` 变量未设置，则不会发出警告。

- 你还可以利用[插值](variable-interpolation.md#interpolation-syntax)。在以下示例中，结果与上面类似，但如果 shell 环境或项目目录中的 `.env` 文件中未设置 `DEBUG` 变量，Compose 会给你一个警告。

  ```yaml
  web:
    environment:
      - DEBUG=${DEBUG}
  ```

## 使用 `env_file` 属性

容器的环境也可以使用 [`.env` 文件](variable-interpolation.md#env-file)配合 [`env_file` 属性](/reference/compose-file/services.md#env_file)来设置。

```yaml
services:
  webapp:
    env_file: "webapp.env"
```

使用 `.env` 文件可以让你使用同一个文件用于普通的 `docker run --env-file ...` 命令，或在多个服务之间共享同一个 `.env` 文件，而无需重复冗长的 `environment` YAML 块。

它还可以帮助你将环境变量与主配置文件分开，提供更有组织和安全的方式来管理敏感信息，因为你不需要将 `.env` 文件放在项目目录的根目录中。

[`env_file` 属性](/reference/compose-file/services.md#env_file)还允许你在 Compose 应用程序中使用多个 `.env` 文件。

在 `env_file` 属性中指定的 `.env` 文件路径是相对于 `compose.yaml` 文件位置的。

> [!IMPORTANT]
>
> `.env` 文件中的插值是 Docker Compose CLI 功能。
>
> 运行 `docker run --env-file ...` 时不支持此功能。

### 附加信息

- 如果指定了多个文件，它们会按顺序计算，后面的文件可以覆盖前面文件中设置的值。
- 从 Docker Compose 2.24.0 版本开始，你可以使用 `required` 字段将 `env_file` 属性定义的 `.env` 文件设置为可选。当 `required` 设置为 `false` 且 `.env` 文件缺失时，Compose 会静默忽略该条目。
  ```yaml
  env_file:
    - path: ./default.env
      required: true # 默认值
    - path: ./override.env
      required: false
  ```
- 从 Docker Compose 2.30.0 版本开始，你可以使用 `format` 属性为 `env_file` 使用替代文件格式。有关更多信息，请参阅 [`format`](/reference/compose-file/services.md#format)。
- `.env` 文件中的值可以通过使用 [`docker compose run -e`](#set-environment-variables-with-docker-compose-run---env) 从命令行覆盖。

## 使用 `docker compose run --env` 设置环境变量

类似于 `docker run --env`，你可以使用 `docker compose run --env` 或其简写形式 `docker compose run -e` 临时设置环境变量：

```console
$ docker compose run -e DEBUG=1 web python console.py
```

### 附加信息

- 你也可以通过不给变量赋值来从 shell 或环境文件传递变量：

  ```console
  $ docker compose run -e DEBUG web python console.py
  ```

容器中 `DEBUG` 变量的值取自运行 Compose 的 shell 中同名变量的值或环境文件中的值。

## 更多资源

- [了解环境变量优先级](envvars-precedence.md)。
- [设置或更改预定义环境变量](envvars.md)
- [探索最佳实践](best-practices.md)
- [了解插值](variable-interpolation.md)
