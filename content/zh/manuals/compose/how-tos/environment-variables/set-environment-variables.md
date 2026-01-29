---
title: 在容器环境中设置环境变量
linkTitle: 设置环境变量
weight: 10
description: 了解如何使用 Compose 设置、使用和管理环境变量
keywords: compose, 编排, 环境, 环境变量, 容器环境变量
aliases:
- /compose/env/
- /compose/link-env-deprecated/
- /compose/environment-variables/set-environment-variables/
---

容器的环境变量在服务配置中明确指定之前不会被设置。在 Compose 中，有两种方法可以通过 Compose 文件在容器中设置环境变量。 

>[!TIP]
>
> 不要使用环境变量向容器传递敏感信息（如密码）。请改用 [机密 (Secrets)](../use-secrets.md)。


## 使用 `environment` 属性

您可以在 `compose.yaml` 中通过 [`environment` 属性](/reference/compose-file/services.md#environment) 直接在容器环境中设置环境变量。

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

请参阅 [`environment` 属性](/reference/compose-file/services.md#environment) 获取更多使用示例。 

### 补充信息 

- 您可以选择不设置具体的值，从而直接将 shell 中的环境变量传递给容器。其工作方式与 `docker run -e VARIABLE ...` 相同：
  ```yaml
  web:
    environment:
      - DEBUG
  ```
容器中 `DEBUG` 变量的值将取自运行 Compose 的 shell 中同名变量的值。请注意，在这种情况下，如果 shell 环境中未设置 `DEBUG` 变量，则不会发出警告。 

- 您还可以利用 [插值](variable-interpolation.md#插值语法)。在以下示例中，结果与上述类似，但如果 shell 环境中或项目目录下的 `.env` 文件中未设置 `DEBUG` 变量，Compose 会给您一个警告。

  ```yaml
  web:
    environment:
      - DEBUG=${DEBUG}
  ```

## 使用 `env_file` 属性

容器的环境也可以使用 [`.env` 文件](variable-interpolation.md#env-file) 配合 [`env_file` 属性](/reference/compose-file/services.md#env_file) 来设置。

```yaml
services:
  webapp:
    env_file: "webapp.env"
```

使用 `.env` 文件可以让您在普通的 `docker run --env-file ...` 命令中重复使用同一个文件，或者在多个服务之间共享同一个 `.env` 文件，而无需重复编写冗长的 `environment` YAML 块。

这还可以帮助您将环境变量与主配置文件分开，提供一种更具条理且更安全的方式来管理敏感信息，因为您无需将 `.env` 文件放在项目根目录中。

[`env_file` 属性](/reference/compose-file/services.md#env_file) 还允许您在 Compose 应用程序中使用多个 `.env` 文件。  

在 `env_file` 属性中指定的 `.env` 文件路径是相对于 `compose.yaml` 文件所在位置的。

> [!IMPORTANT]
>
> `.env` 文件中的插值（Interpolation）是 Docker Compose CLI 的一项功能。
>
> 运行 `docker run --env-file ...` 时不支持此功能。

### 补充信息 

- 如果指定了多个文件，它们将按顺序评估，并且可以覆盖之前文件中设置的值。
- 自 Docker Compose 2.24.0 版本起，您可以使用 `required` 字段将 `env_file` 属性定义的 `.env` 文件设置为可选。当 `required` 设置为 `false` 且 `.env` 文件缺失时，Compose 会静默忽略该条目。
  ```yaml
  env_file:
    - path: ./default.env
      required: true # 默认值
    - path: ./override.env
      required: false
  ``` 
- 自 Docker Compose 2.30.0 版本起，您可以使用 `format` 属性为 `env_file` 指定备选文件格式。有关更多信息，请参阅 [`format`](/reference/compose-file/services.md#format)。
- `.env` 文件中的值可以通过使用 [`docker compose run -e`](#使用-docker-compose-run---env-设置环境变量) 从命令行覆盖。 

## 使用 `docker compose run --env` 设置环境变量

与 `docker run --env` 类似，您可以使用 `docker compose run --env` 或其简写形式 `docker compose run -e` 临时设置环境变量：

```console
$ docker compose run -e DEBUG=1 web python console.py
```

### 补充信息 

- 您也可以通过不赋予变量值，从而从 shell 或环境文件中传递该变量：

  ```console
  $ docker compose run -e DEBUG web python console.py
  ```

容器中 `DEBUG` 变量的值将取自运行 Compose 的 shell 中或环境文件中的同名变量值。

## 更多资源

- [理解环境变量优先级](envvars-precedence.md)。
- [设置或更改预定义环境变量](envvars.md)
- [探索最佳实践](best-practices.md)
- [理解插值 (Interpolation)](variable-interpolation.md)
