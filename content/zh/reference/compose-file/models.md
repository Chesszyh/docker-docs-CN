---
title: 模型
description: 了解模型顶级元素
keywords: compose, compose 规范, 模型, compose 文件参考
weight: 120
---

{{< summary-bar feature_name="Compose 模型" >}}

顶级 `models` 部分声明了 Compose 应用程序使用的 AI 模型。这些模型通常作为 OCI 工件拉取，由模型运行器运行，并作为服务容器可以使用的 API 公开。

服务只有在 `services` 顶级元素中的 [`models` 属性](services.md#models) 明确授予时才能访问模型。

## 示例

### 示例 1

```yaml
services:
  app:
    image: app
    models:
      - ai_model


models:
  ai_model:
    model: ai/model
```

在这个基本示例中：

 - app 服务使用 `ai_model`。
 - `ai_model` 被定义为一个 OCI 工件 (`ai/model`)，由模型运行器拉取和提供。
 - Docker Compose 将连接信息（例如 `AI_MODEL_URL`）注入到容器中。

### 示例 2

```yaml
services:
  app:
    image: app
    models:
      my_model:
        endpoint_var: MODEL_URL

models:
  my_model:
    model: ai/model
    context_size: 1024
    runtime_flags: 
      - "--a-flag"
      - "--another-flag=42"
```

在这个高级设置中：

 - 服务应用程序使用长语法引用 `my_model`。
 - Compose 将模型运行器的 URL 作为环境变量 `MODEL_URL` 注入。

## 属性

- `model`（必需）：模型的 OCI 工件标识符。这是 Compose 通过模型运行器拉取和运行的内容。
- `context_size`：定义模型的最大令牌上下文大小。
- `runtime_flags`：模型启动时传递给推理引擎的原始命令行标志列表。
