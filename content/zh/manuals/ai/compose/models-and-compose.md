---
title: 在 Docker Compose 应用程序中定义 AI 模型
linkTitle: 在 Compose 中使用 AI 模型
description: 学习如何使用 models 顶级元素在 Docker Compose 应用程序中定义和使用 AI 模型
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

Compose 允许你将 AI 模型定义为应用程序的核心组件，这样你可以在服务旁边声明模型依赖，并在任何支持 Compose 规范的平台上运行应用程序。

## 前置条件

- Docker Compose v2.38 或更高版本
- 支持 Compose 模型的平台，例如 Docker Model Runner（DMR，Docker 模型运行器）或兼容的云提供商。
  如果你使用 DMR，请参阅[要求](/manuals/ai/model-runner/_index.md#requirements)。

## 什么是 Compose 模型？

Compose `models` 是一种在应用程序中定义 AI 模型依赖的标准化方式。通过在 Compose 文件中使用 [`models` 顶级元素](/reference/compose-file/models.md)，你可以：

- 声明应用程序需要哪些 AI 模型
- 指定模型配置和要求
- 使应用程序在不同平台之间具有可移植性
- 让平台处理模型的配置和生命周期管理

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
- 一个名为 `chat-app` 的服务，使用名为 `llm` 的模型
- `llm` 的模型定义，引用 `ai/smollm2` 模型镜像

## 模型配置选项

模型支持多种配置选项：

```yaml
models:
  llm:
    model: ai/smollm2
    context_size: 1024
    runtime_flags:
      - "--a-flag"
      - "--another-flag=42"
```

常用配置选项包括：
- `model`（必需）：模型的 OCI 制品标识符。这是 Compose 通过模型运行器拉取和运行的内容。
- `context_size`：定义模型的最大令牌上下文大小。

   > [!NOTE]
   > 每个模型都有自己的最大上下文大小。在增加上下文长度时，
   > 请考虑你的硬件限制。一般来说，尽量保持上下文大小
   > 在满足特定需求的前提下尽可能小。

- `runtime_flags`：传递给推理引擎的原始命令行标志列表，在模型启动时使用。
   例如，如果你使用 llama.cpp，你可以传递任何[可用参数](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)。
- 平台特定选项也可以通过扩展属性 `x-*` 使用

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

使用短语法时，平台会根据模型名称自动生成环境变量：
- `LLM_URL` - 访问 llm 模型的 URL
- `LLM_MODEL` - llm 模型的模型标识符
- `EMBEDDING_MODEL_URL` - 访问 embedding-model 的 URL
- `EMBEDDING_MODEL_MODEL` - embedding-model 的模型标识符

### 长语法

长语法允许你自定义环境变量名称：

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

使用此配置，你的服务将收到：
- `AI_MODEL_URL` 和 `AI_MODEL_NAME` 用于 LLM 模型
- `EMBEDDING_URL` 和 `EMBEDDING_NAME` 用于嵌入模型

## 平台可移植性

使用 Compose 模型的一个关键优势是可以在支持 Compose 规范的不同平台之间移植。

### Docker Model Runner

当 [Docker Model Runner 启用](/manuals/ai/model-runner/_index.md)时：

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
- 提供访问模型的端点 URL
- 将环境变量注入到服务中

#### 使用 provider 服务的替代配置

> [!TIP]
>
> 此方法已弃用。请改用 [`models` 顶级元素](#基本模型定义)。

你也可以使用 `provider` 服务类型，它允许你声明应用程序所需的平台能力。
对于 AI 模型，你可以使用 `model` 类型来声明模型依赖。

要定义模型提供者：

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

同一个 Compose 文件可以在支持 Compose 模型的云提供商上运行：

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
- 使用托管 AI 服务而不是在本地运行模型
- 应用云特定的优化和扩展
- 提供额外的监控和日志功能
- 自动处理模型版本控制和更新

## 参考

- [`models` 顶级元素](/reference/compose-file/models.md)
- [`models` 属性](/reference/compose-file/services.md#models)
- [Docker Model Runner 文档](/manuals/ai/model-runner.md)
- [Compose Model Runner 文档](/manuals/ai/compose/models-and-compose.md)
