---
title: 在 Docker Compose 应用中定义 AI 模型
linkTitle: 在 Compose 中使用 AI 模型
description: 了解如何使用 models 顶级元素在 Docker Compose 应用中定义和使用 AI 模型
keywords: compose, docker compose, models, ai, machine learning, cloud providers, specification
alias:
  - /compose/how-tos/model-runner/
  - /ai/compose/model-runner/
weight: 10
params:
  sidebar:
    badge:
      color: green
      text: New
---

{{< summary-bar feature_name="Compose models" >}}

Compose 允许您将 AI 模型定义为应用程序的核心组件，因此您可以与服务一起声明模型依赖项，并在任何支持 Compose 规范的平台上运行该应用程序。

## 前提条件

- Docker Compose v2.38 或更高版本
- 支持 Compose 模型的平台，例如 Docker Model Runner (DMR) 或兼容的云提供商。
  如果您使用的是 DMR，请参阅 [要求](/manuals/ai/model-runner/_index.md#要求)。

## 什么是 Compose 模型？

Compose `models` 是在应用程序中定义 AI 模型依赖项的标准化方式。通过在 Compose 文件中使用 [`models` 顶级元素](/reference/compose-file/models.md)，您可以：

- 声明您的应用程序需要哪些 AI 模型
- 指定模型配置和要求
- 使您的应用程序可以在不同平台之间移植
- 让平台处理模型的供应和生命周期管理

## 基本模型定义

要在 Compose 应用程序中定义模型，请使用 `models` 顶级元素：

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
```

此示例定义了：
- 一个名为 `chat-app` 的服务，它使用一个名为 `llm` 的模型
- `llm` 的模型定义，它引用了 `ai/smollm2` 模型镜像

## 模型配置选项

模型支持各种配置选项：

```yaml
models:
  llm:
    model: ai/smollm2
    context_size: 1024
    runtime_flags:
      - "--a-flag"
      - "--another-flag=42"
```

常见的配置选项包括：
- `model`（必填）：模型的 OCI 构件标识符。这是 Compose 通过模型运行器拉取并运行的内容。
- `context_size`：定义模型的最大 token 上下文大小。
  
   > [!NOTE]
   > 每个模型都有其自己的最大上下文大小。增加上下文长度时，请考虑您的硬件限制。通常，请尽量根据您的特定需求将上下文大小保持在尽可能小的范围内。
  
- `runtime_flags`：在模型启动时传递给推理引擎的原始命令行标志列表。
   例如，如果您使用 llama.cpp，您可以传递任何 [可用参数](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)。
- 通过扩展属性 `x-*` 可能还提供特定于平台的选项

## 服务模型绑定

服务可以通过两种方式引用模型：短语法和长语法。

### 短语法

短语法是将模型绑定到服务的最简单方式：

```yaml
services:
  app:
    image: my-app
    models:
      - llm
      - embedding-model

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

使用短语法，平台会自动根据模型名称生成环境变量：
- `LLM_URL` - 访问 llm 模型的 URL
- `LLM_MODEL` - llm 模型的标识符
- `EMBEDDING_MODEL_URL` - 访问 embedding-model 的 URL
- `EMBEDDING_MODEL_MODEL` - embedding-model 的标识符

### 长语法

长语法允许您自定义环境变量名称：

```yaml
services:
  app:
    image: my-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME
      embedding-model:
        endpoint_var: EMBEDDING_URL
        model_var: EMBEDDING_NAME

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

使用此配置，您的服务将接收：
- 用于 LLM 模型的 `AI_MODEL_URL` 和 `AI_MODEL_NAME`
- 用于 embedding 模型的 `EMBEDDING_URL` 和 `EMBEDDING_NAME`

## 平台移植性

使用 Compose 模型的主要优势之一是可以在支持 Compose 规范的不同平台之间移植。

### Docker Model Runner

当 [启用 Docker Model Runner](/manuals/ai/model-runner/_index.md) 时：

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME

models:
  llm:
    model: ai/smollm2
    context_size: 4096
    runtime_flags:
      - "--no-prefill-assistant"
```

Docker Model Runner 将：
- 在本地拉取并运行指定的模型
- 提供用于访问模型的端点 URL
- 向服务中注入环境变量

#### 使用提供者服务的替代配置

> [!TIP]
>
> 此方法已弃用。请改为使用 [`models` 顶级元素](#基本模型定义)。

您还可以使用 `provider` 服务类型，它允许您声明应用程序所需的平台功能。 
对于 AI 模型，您可以使用 `model` 类型来声明模型依赖项。

定义模型提供者：

```yaml
services:
  chat:
    image: my-chat-app
    depends_on:
      - ai_runner

  ai_runner:
    provider:
      type: model
      options:
        model: ai/smollm2
        context-size: 1024
        runtime-flags: "--no-prefill-assistant"
```


### 云提供商

相同的 Compose 文件可以在支持 Compose 模型的云提供商上运行：

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
    # 云特定配置
    x-cloud-options:
      - "cloud.instance-type=gpu-small"
      - "cloud.region=us-west-2"
```

云提供商可能会：
- 使用托管 AI 服务，而不是在本地运行模型
- 应用云特定的优化和扩展
- 提供额外的监控和日志记录功能
- 自动处理模型版本控制和更新

## 参考

- [`models` 顶级元素](/reference/compose-file/models.md)
- [`models` 属性](/reference/compose-file/services.md#models)
- [Docker Model Runner 文档](/manuals/ai/model-runner.md)
- [Compose Model Runner 文档](/manuals/ai/compose/models-and-compose.md)
