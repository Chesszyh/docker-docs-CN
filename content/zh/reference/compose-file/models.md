---
title: models 顶级元素
description: 了解 models 顶级元素
keywords: compose, compose specification, models, compose file reference
weight: 120
---

{{< summary-bar feature_name="Compose models" >}}

顶级 `models` 部分声明 Compose 应用程序使用的 AI 模型。这些模型通常作为 OCI 工件拉取，由模型运行器运行，并作为服务容器可以使用的 API 公开。

只有当服务通过 `services` 顶级元素内的 [`models` 属性](services.md#models) 显式授权时，服务才能访问模型。

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

在此基本示例中：

 - app 服务使用 `ai_model`。
 - `ai_model` 定义为由模型运行器拉取和提供服务的 OCI 工件（`ai/model`）。
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

在此高级设置中：

 - 服务 app 使用长语法引用 `my_model`。
 - Compose 将模型运行器的 URL 作为环境变量 `MODEL_URL` 注入。

## 属性

- `model`（必需）：模型的 OCI 工件标识符。这是 Compose 通过模型运行器拉取和运行的内容。
- `context_size`：定义模型的最大令牌上下文大小。
- `runtime_flags`：启动模型时传递给推理引擎的原始命令行标志列表。
