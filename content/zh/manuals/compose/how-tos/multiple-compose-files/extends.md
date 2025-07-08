---
description: 了解如何使用 Docker Compose 的 extends 属性在文件和项目之间重用服务配置。
keywords: fig, composition, compose, docker, orchestration, documentation, docs, compose file modularization, 组合, 编排, 文档, 模块化
title: 扩展您的 Compose 文件
linkTitle: 扩展
weight: 20
aliases:
- /compose/extends/
- /compose/multiple-compose-files/extends/
---

Docker Compose 的 [`extends` 属性](/reference/compose-file/services.md#extends)
可让您在不同文件甚至完全不同的项目之间共享通用配置。

如果您有多个服务重用一组通用的配置选项，那么扩展服务非常有用。使用 `extends`，您可以在一个地方定义一组通用的服务选项，并从任何地方引用它。您可以引用另一个 Compose 文件并选择一个您也想在自己的应用程序中使用的服务，并能够根据自己的需要覆盖某些属性。

> [!IMPORTANT]
>
> 当您使用多个 Compose 文件时，您必须确保文件中的所有路径都是相对于基础 Compose 文件（即主项目文件夹中的 Compose 文件）的。这是必需的，因为扩展文件不必是有效的 Compose 文件。扩展文件可以包含小的配置片段。跟���服务的哪个片段相对于哪个路径是困难和混乱的，因此为了使路径更易于理解，所有路径都必须相对于基础文件进行定义。

## `extends` 属性如何工作

### 从另一个文件扩展服务

以下面的例子为例：

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
```

这指示 Compose 仅重用 `common-services.yml` 文件中定义的 `webapp` 服务的属性。`webapp` 服务本身不是最终项目的一部分。

如果 `common-services.yml` 如下所示：

```yaml
services:
  webapp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - "/data"
```
您将得到与直接在 `web` 下定义相同的 `build`、`ports` 和 `volumes` 配置值的 `compose.yaml` 完全相同的结果。

要从另一个文件扩展服务时将服务 `webapp` 包含在最终项目中，您需要在当前的 Compose 文件中明确包含这两个服务。例如（这仅用于说明目的）：

```yaml
services:
  web:
    build: alpine
    command: echo
    extends:
      file: common-services.yml
      service: webapp
  webapp:
    extends:
      file: common-services.yml
      service: webapp
```

或者，您可以使用 [include](include.md)。

### 在同一文件中扩展服务

如果您在同一个 Compose 文���中定义服务并从另一个服务扩展一个服务，则原始服务和扩展服务都将成为最终配置的一部分。例如：

```yaml 
services:
  web:
    build: alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### 在同一文件中和从另一个文件中扩展服务

您可以更进一步，在 `compose.yaml` 中本地定义或重新定义配置：

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
    environment:
      - DEBUG=1
    cpu_shares: 5

  important_web:
    extends: web
    cpu_shares: 10
```

## 其他示例

当您有多个具有通用配置的服务时，扩展单个服务非常有用。下面的示例是一个包含两个服务的 Compose 应用程序，一个 Web 应用程序和一个队列工作程序。这两个服务都使用相同的代码库并共享许多配置选项。

`common.yaml` 文件定义了通用配置：

```yaml
services:
  app:
    build: .
    environment:
      CONFIG_FILE_PATH: /code/config
      API_KEY: xxxyyy
    cpu_shares: 5
```

`compose.yaml` 定义了使用通用配置的具体服务：

```yaml
services:
  webapp:
    extends:
      file: common.yaml
      service: app
    command: /code/run_web_app
    ports:
      - 8080:8080
    depends_on:
      - queue
      - db

  queue_worker:
    extends:
      file: common.yaml
      service: app
    command: /code/run_worker
    depends_on:
      - queue
```

## 例外和限制

`volumes_from` 和 `depends_on` 从不使用 `extends` 在服务之间共享。存在这些例外是为了避免隐式依赖；您始终在本地定义 `volumes_from`。这可确保在读取当前文件时服务之间的依赖关系清晰可见。在本地定义这些还可以确保对引���文件的更改不会破坏任何内容。

如果您只需要共享单个服务并且您熟悉要扩展的文件，那么 `extends` 非常有用，因此您可以调整配置。但是，当您想重用别人不熟悉的配置并且您不了解其自身的依赖关系时，这不是一个可接受的解决方案。

## 相对路径

当使用带有指向另一个文件夹的 `file` 属性的 `extends` 时，被扩展服务声明的相对路径将被转换，以便在被扩展服务使用时它们仍然指向同一个文件。下面的示例说明了这一点：

基础 Compose 文件：
```yaml
services:
  webapp:
    image: example
    extends:
      file: ../commons/compose.yaml
      service: base
```

`commons/compose.yaml` 文件：
```yaml
services:
  base:
    env_file: ./container.env
```

生成的服务引用 `commons` 目录中的原始 `container.env` 文��。这可以通过 `docker compose config` 来确认，它会检查实际模型：
```yaml
services:
  webapp:
    image: example
    env_file: 
      - ../commons/container.env
```

## 参考信息

- [`extends`](/reference/compose-file/services.md#extends)
