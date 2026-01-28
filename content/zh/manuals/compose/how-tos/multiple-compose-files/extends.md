---
description: 了解如何使用 Docker Compose 的 extends 属性在文件和项目之间重用服务配置。
keywords: fig, composition, compose, docker, orchestration, documentation, docs, compose file modularization
title: 扩展你的 Compose 文件
linkTitle: Extend
weight: 20
aliases:
- /compose/extends/
- /compose/multiple-compose-files/extends/
---

Docker Compose 的 [`extends` 属性](/reference/compose-file/services.md#extends)
允许你在不同文件甚至完全不同的项目之间共享通用配置。

如果你有多个服务重用一组通用配置选项，扩展服务非常有用。使用 `extends`，你可以在一个地方定义一组通用的
服务选项，并从任何地方引用它。你可以引用
另一个 Compose 文件并选择你也想在自己的应用程序中使用的服务，并能够根据自己的需要覆盖某些属性。

> [!IMPORTANT]
>
> 当你使用多个 Compose 文件时，必须确保所有文件中的路径
都是相对于基础 Compose 文件（即主项目文件夹中的 Compose 文件）的。这是必需的，因为扩展文件
不需要是有效的 Compose 文件。扩展文件可以包含小的配置片段。
跟踪服务的哪个片段相对于哪个路径是
困难且令人困惑的，因此为了使路径更容易理解，所有路径必须
相对于基础文件定义。

## `extends` 属性的工作原理

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

如果 `common-services.yml`
如下所示：

```yaml
services:
  webapp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - "/data"
```
你得到的结果与直接在 `web` 下定义相同的 `build`、`ports` 和 `volumes` 配置值编写 `compose.yaml` 完全相同。

要在从另一个文件扩展服务时将 `webapp` 服务包含在最终项目中，你需要在当前 Compose 文件中显式包含这两个服务。例如（这仅用于说明目的）：

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

或者，你可以使用 [include](include.md)。

### 在同一文件中扩展服务

如果你在同一个 Compose 文件中定义服务并从另一个服务扩展，原始服务和扩展的服务都将成为最终配置的一部分。例如：

```yaml
services:
  web:
    build: alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### 在同一文件中以及从另一个文件扩展服务

你可以进一步在 `compose.yaml` 中本地定义或重新定义配置：

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

## 附加示例

当你有多个具有通用配置的服务时，扩展单个服务非常有用。下面的示例是一个包含两个
服务的 Compose 应用程序，一个 web 应用程序和一个队列工作器。两个服务使用相同的
代码库并共享许多配置选项。

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

`compose.yaml` 定义了使用通用
配置的具体服务：

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

`volumes_from` 和 `depends_on` 永远不会在使用
`extends` 的服务之间共享。这些例外的存在是为了避免隐式依赖；你总是
在本地定义 `volumes_from`。这确保在读取当前文件时服务之间的依赖关系是清晰可见的。在本地定义这些也
确保对引用文件的更改不会破坏任何东西。

如果你只需要共享单个服务并且你熟悉
你要扩展的文件，`extends` 非常有用，这样你可以调整
配置。但是，当你想重用
别人的不熟悉的配置并且你不了解其自身
依赖项时，这不是一个可接受的解决方案。

## 相对路径

当使用带有指向另一个文件夹的 `file` 属性的 `extends` 时，被扩展服务声明的相对路径
会被转换，以便在被扩展服务使用时仍然指向
相同的文件。以下示例说明了这一点：

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

生成的服务引用 `commons` 目录中的原始 `container.env` 文件。这可以通过 `docker compose config` 确认，
它会检查实际模型：
```yaml
services:
  webapp:
    image: example
    env_file:
      - ../commons/container.env
```

## 参考信息

- [`extends`](/reference/compose-file/services.md#extends)
