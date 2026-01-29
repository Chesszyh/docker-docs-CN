---
description: 了解如何使用 Docker Compose 的 extends 属性在不同文件和项目之间重用服务配置。
keywords: fig, composition, compose, docker, 编排, 文档, docs, compose 文件模块化
title: 扩展您的 Compose 文件
linkTitle: 扩展 (Extend)
weight: 20
---

Docker Compose 的 [`extends` 属性](/reference/compose-file/services.md#extends) 允许您在不同文件甚至完全不同的项目之间共享通用配置。

如果您有多个服务需要重用一组通用的配置选项，那么扩展服务将非常有用。通过 `extends`，您可以在一个地方定义一组通用的服务选项，并在任何地方引用它。您可以引用另一个 Compose 文件，选择您也想在自己的应用程序中使用的服务，并能够根据自己的需求覆盖某些属性。

> [!IMPORTANT]
>
> 当您使用多个 Compose 文件时，必须确保文件中的所有路径都相对于基础 Compose 文件（即主项目文件夹中的 Compose 文件）。这是必要的，因为被继承的文件不一定是完整的有效 Compose 文件。被继承的文件可以包含配置的小片段。跟踪服务的哪个片段相对于哪个路径是困难且容易混淆的，因此为了使路径易于理解，所有路径都必须相对于基础文件定义。 

## `extends` 属性的工作原理

### 从另一个文件扩展服务

以前面的示例为例：

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
```

这指示 Compose 仅重用 `common-services.yml` 文件中定义的 `webapp` 服务的属性。`webapp` 服务本身并不是最终项目的一部分。

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
您得到的结果与直接在 `web` 下编写具有相同 `build`、`ports` 和 `volumes` 配置值的 `compose.yaml` 完全相同。

在从另一个文件扩展服务时，如果您也想将 `webapp` 服务包含在最终项目中，则需要在当前的 Compose 文件中显式包含这两个服务。例如（这仅用于说明目的）：

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

或者，您也可以使用 [include](include.md)。 

### 在同一个文件内扩展服务 

如果您在同一个 Compose 文件中定义服务，并让一个服务扩展另一个服务，那么原始服务和扩展后的服务都将是您最终配置的一部分。例如：

```yaml 
services:
  web:
    build: alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### 同时在同一个文件内和从另一个文件扩展服务

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

## 补充示例

当您有多个具有通用配置的服务时，扩展单个服务非常有用。下面的示例是一个具有两个服务的 Compose 应用：一个 Web 应用程序和一个队列 worker。这两个服务使用相同的代码库并共享许多配置选项。

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

## 例外情况和局限性

`volumes_from` 和 `depends_on` 绝不会在使用了 `extends` 的服务之间共享。这些例外情况的存在是为了避免隐式依赖；您始终要在本地定义 `volumes_from`。这确保了在阅读当前文件时，服务之间的依赖关系清晰可见。在本地定义这些内容还能确保对引用文件的更改不会破坏任何东西。

如果您只需要共享单个服务，并且熟悉要扩展的文件，以便调整配置，那么 `extends` 将非常有用。但如果您想重用他人不熟悉的配置，且不知道其自身的依赖关系，这并不是一个可以接受的解决方案。

## 相对路径

当使用带有指向另一个文件夹的 `file` 属性的 `extends` 时，被扩展服务声明的相对路径会被转换，以便在被扩展服务使用时仍指向同一个文件。以下示例说明了这一点：

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

生成的服务引用了 `commons` 目录中原始的 `container.env` 文件。可以通过 `docker compose config` 查看实际模型来确认这一点：
```yaml
services:
  webapp:
    image: example
    env_file: 
      - ../commons/container.env
```

## 参考信息

- [`extends`](/reference/compose-file/services.md#extends)
