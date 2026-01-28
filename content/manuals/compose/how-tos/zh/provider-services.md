---
title: 使用提供者服务
description: 了解如何在 Docker Compose 中使用提供者服务将外部功能集成到您的应用程序中
keywords: compose, docker compose, provider, services, platform capabilities, integration, model runner, ai
weight: 112
params:
  sidebar:
    badge:
      color: green
      text: New
---

{{< summary-bar feature_name="Compose provider services" >}}

Docker Compose 支持提供者服务（provider services），允许与生命周期由第三方组件而非 Compose 本身管理的服务进行集成。此功能使您能够定义和使用平台特定的服务，而无需手动设置或直接进行生命周期管理。

## 什么是提供者服务？

提供者服务是 Compose 中一种特殊类型的服务，代表平台能力而非容器。它们允许您声明应用程序所需的特定平台功能的依赖关系。

当您在 Compose 文件中定义提供者服务时，Compose 会与平台协作来配置和设置所请求的能力，使其可供您的应用程序服务使用。

## 使用提供者服务

要在 Compose 文件中使用提供者服务，您需要：

1. 使用 `provider` 属性定义服务
2. 指定要使用的提供者 `type`
3. 配置任何提供者特定的选项
4. 从您的应用程序服务声明对提供者服务的依赖

这是一个基本示例：

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

请注意 `database` 服务中专用的 `provider` 属性。此属性指定该服务由提供者管理，并允许您定义特定于该提供者类型的选项。

`app` 服务中的 `depends_on` 属性指定它依赖于 `database` 服务。这意味着 `database` 服务将在 `app` 服务之前启动，允许将提供者信息注入到 `app` 服务中。

## 工作原理

在 `docker compose up` 命令执行期间，Compose 识别依赖提供者的服务并与它们协作来配置所请求的能力。然后提供者用关于如何访问已配置资源的信息填充 Compose 模型。

此信息通过环境变量传递给声明对提供者服务有依赖的服务。这些变量的命名约定是：

```env
<<PROVIDER_SERVICE_NAME>>_<<VARIABLE_NAME>>
```

例如，如果您的提供者服务名为 `database`，您的应用程序服务可能会收到如下环境变量：

- `DATABASE_URL` 包含访问已配置资源的 URL
- `DATABASE_TOKEN` 包含身份验证令牌
- 其他提供者特定的变量

然后您的应用程序可以使用这些环境变量与已配置的资源进行交互。

## 提供者类型

提供者服务中的 `type` 字段引用以下之一的名称：

1. Docker CLI 插件（例如 `docker-model`）
2. 用户 PATH 中可用的二进制文件

当 Compose 遇到提供者服务时，它会查找具有指定名称的插件或二进制文件来处理所请求能力的配置。

例如，如果您指定 `type: model`，Compose 将查找名为 `docker-model` 的 Docker CLI 插件或 PATH 中名为 `model` 的二进制文件。

```yaml
services:
  ai-runner:
    provider:
      type: model  # 查找 docker-model 插件或 model 二进制文件
      options:
        model: ai/example-model
```

插件或二进制文件负责：

1. 解释提供者服务中提供的选项
2. 配置所请求的能力
3. 返回关于如何访问已配置资源的信息

然后此信息作为环境变量传递给依赖的服务。

> [!TIP]
>
> 如果您在 Compose 中使用 AI 模型，请改用 [`models` 顶级元素](/manuals/ai/compose/models-and-compose.md)。

## 使用提供者服务的好处

在 Compose 应用程序中使用提供者服务提供了几个好处：

1. 简化配置：您不需要手动配置和管理平台能力
2. 声明式方法：您可以在一个地方声明应用程序的所有依赖项
3. 一致的工作流程：您使用相同的 Compose 命令来管理整个应用程序，包括平台能力

## 创建您自己的提供者

如果您想创建自己的提供者来使用自定义能力扩展 Compose，您可以实现一个注册提供者类型的 Compose 插件。

有关如何创建和实现自己的提供者的详细信息，请参阅 [Compose 扩展文档](https://github.com/docker/compose/blob/main/docs/extension.md)。本指南解释了允许您向 Compose 添加新提供者类型的扩展机制。

## 参考

- [Docker Model Runner 文档](/manuals/ai/model-runner.md)
- [Compose 扩展文档](https://github.com/docker/compose/blob/main/docs/extension.md)
