---
title: 使用提供者服务 (Provider services)
description: 了解如何在 Docker Compose 中使用提供者服务，将外部功能集成到您的应用程序中
keywords: compose, docker compose, 提供者, 服务, 平台功能, 集成, 模型运行器, ai
weight: 112
params:
  sidebar:
    badge:
      color: green
      text: 新增
---

{{< summary-bar feature_name="Compose 提供者服务" >}}

Docker Compose 支持提供者服务（provider services），允许与那些生命周期由第三方组件（而非 Compose 自身）管理的服务进行集成。此功能使您能够定义并利用特定于平台的服务，而无需进行手动设置或直接进行生命周期管理。

## 什么是提供者服务？

提供者服务是 Compose 中的一种特殊服务类型，代表平台功能而非容器。它们允许您声明应用程序所需的特定平台特性的依赖关系。

当您在 Compose 文件中定义提供者服务时，Compose 会与平台协作来供应和配置所请求的功能，并使其对您的应用程序服务可用。

## 使用提供者服务

要在 Compose 文件中使用提供者服务，您需要：

1. 定义一个带有 `provider` 属性的服务
2. 指定您想要使用的提供者类型（`type`）
3. 配置任何特定于提供者的选项
4. 声明您的应用程序服务对该提供者服务的依赖关系

以下是一个基本示例：

```yaml
services:
  database:
    provider:
      type: awesomecloud
      options:
        type: mysql
        foo: bar  
  app:
    image: myapp 
    depends_on:
       - database
```

注意 `database` 服务中专门的 `provider` 属性。此属性指定该服务由提供者管理，并允许您定义特定于该提供者类型的选项。

`app` 服务中的 `depends_on` 属性指定它依赖于 `database` 服务。这意味着 `database` 服务将在 `app` 服务之前启动，从而允许将提供者信息注入到 `app` 服务中。

## 工作原理

在执行 `docker compose up` 命令期间，Compose 会识别依赖于提供者的服务，并与它们协作以供应请求的功能。然后，提供者会向 Compose 模型填充有关如何访问所供应资源的信息。

此信息通常通过环境变量传递给声明了对提供者服务依赖的服务。这些变量的命名约定为：

```env
<<PROVIDER_SERVICE_NAME>>_<<VARIABLE_NAME>>
```

例如，如果您的提供者服务命名为 `database` ，您的应用程序服务可能会收到如下环境变量：

- `DATABASE_URL` ：访问所供应资源的 URL
- `DATABASE_TOKEN` ：身份验证令牌
- 其他特定于提供者的变量

您的应用程序可以使用这些环境变量与所供应的资源进行交互。

## 提供者类型

提供者服务中的 `type` 字段引用以下内容之一的名称：

1. 一个 Docker CLI 插件（例如 `docker-model`）
2. 一个在用户 PATH 中可用的二进制文件

当 Compose 遇到提供者服务时，它会寻找具有指定名称的插件或二进制文件，以处理所请求功能的供应。

例如，如果您指定 `type: model`，Compose 将在 PATH 中寻找名为 `docker-model` 的 Docker CLI 插件或名为 `model` 的二进制文件。

```yaml
services:
  ai-runner:
    provider:
      type: model  # 寻找 docker-model 插件或 model 二进制文件
      options:
        model: ai/example-model
```

该插件或二进制文件负责：

1. 解释提供者服务中提供的选项
2. 供应请求的功能
3. 返回有关如何访问所供应资源的信息

然后，这些信息将以环境变量的形式传递给依赖它的服务。

> [!TIP]
>
> 如果您在 Compose 中使用 AI 模型，请改用 [`models` 顶级元素](/manuals/ai/compose/models-and-compose.md)。

## 使用提供者服务的好处

在您的 Compose 应用程序中使用提供者服务具有以下几个好处：

1. 简化配置：您无需手动配置和管理平台功能
2. 声明式方法：您可以在一个地方声明应用程序的所有依赖关系
3. 一致的工作流：您使用相同的 Compose 命令来管理整个应用程序，包括平台功能

## 创建您自己的提供者

如果您想创建自己的提供者，通过自定义功能扩展 Compose，您可以实现一个注册提供者类型的 Compose 插件。

有关如何创建和实现您自己的提供者的详细信息，请参阅 [Compose 扩展文档](https://github.com/docker/compose/blob/main/docs/extension.md)。此指南解释了允许您向 Compose 添加新提供者类型的扩展机制。

## 参考

- [Docker Model Runner 文档](/manuals/ai/model-runner.md)
- [Compose 扩展文档](https://github.com/docker/compose/blob/main/docs/extension.md)
