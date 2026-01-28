---
title: Docker Model Runner
params:
  sidebar:
    badge:
      color: blue
      text: Beta
    group: AI
weight: 20
description: 学习如何使用 Docker Model Runner 管理和运行 AI 模型。
keywords: Docker, ai, model runner, docker desktop, docker engine, llm
aliases:
  - /desktop/features/model-runner/
  - /model-runner/
---

{{< summary-bar feature_name="Docker Model Runner" >}}

Docker Model Runner 使使用 Docker 管理、运行和部署 AI 模型变得轻松。Docker Model Runner 专为开发者设计，简化了从 Docker Hub 或任何符合 OCI 标准的注册表直接拉取、运行和服务大型语言模型（LLM）和其他 AI 模型的过程。

通过与 Docker Desktop 和 Docker Engine 的无缝集成，你可以通过 OpenAI 兼容的 API 服务模型，将 GGUF 文件打包为 OCI 制品，并从命令行和图形界面与模型交互。

无论你是构建生成式 AI 应用程序、试验机器学习工作流程，还是将 AI 集成到软件开发生命周期中，Docker Model Runner 都提供了一种一致、安全且高效的方式来在本地使用 AI 模型。

## 主要功能

- [从 Docker Hub 拉取和推送模型](https://hub.docker.com/u/ai)
- 通过 OpenAI 兼容的 API 服务模型，便于与现有应用程序集成
- 将 GGUF 文件打包为 OCI 制品并发布到任何容器注册表
- 直接从命令行或 Docker Desktop GUI 运行和与 AI 模型交互
- 管理本地模型并显示日志

## 要求

Docker Model Runner 在以下平台上受支持：

{{< tabs >}}
{{< tab name="Windows">}}

Windows(amd64)：
-  NVIDIA GPU
-  NVIDIA 驱动程序 576.57+

Windows(arm64)：
- OpenCL for Adreno
- Qualcomm Adreno GPU（6xx 系列及更高版本）

  > [!NOTE]
  > 某些 llama.cpp 功能可能在 6xx 系列上不完全支持。

{{< /tab >}}
{{< tab name="MacOS">}}

- Apple Silicon

{{< /tab >}}
{{< tab name="Linux">}}

仅限 Docker Engine：

- Linux CPU 和 Linux NVIDIA
- NVIDIA 驱动程序 575.57.08+

{{< /tab >}}
{{</tabs >}}


## 工作原理

模型在首次使用时从 Docker Hub 拉取并存储在本地。它们仅在运行时发出请求时加载到内存中，不使用时卸载以优化资源。由于模型可能很大，初次拉取可能需要一些时间——但之后，它们会被缓存在本地以便更快访问。你可以使用 [OpenAI 兼容的 API](#有哪些可用的-api-端点) 与模型交互。

> [!TIP]
>
> 使用 Testcontainers 或 Docker Compose？
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/)
> 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/)，以及
> [Docker Compose](/manuals/ai/compose/models-and-compose.md) 现在支持 Docker Model Runner。

## 启用 Docker Model Runner

### 在 Docker Desktop 中启用 DMR

1. 在设置视图中，导航到 **Beta features** 选项卡。
1. 勾选 **Enable Docker Model Runner** 设置。
1. 如果你在 Windows 上使用支持的 NVIDIA GPU 运行，你还应该能够看到并勾选 **Enable GPU-backed inference** 设置。
1. 可选：如果你想启用 TCP 支持，选择 **Enable host-side TCP support**
   1. 在 **Port** 字段中，输入你选择的端口。
   1. 如果你正在从本地前端 Web 应用程序与 Model Runner 交互，在 **CORS Allows Origins** 中，选择 Model Runner 应该接受请求的来源。来源是你的 Web 应用程序运行的 URL，例如 `http://localhost:3131`。

你现在可以在 CLI 中使用 `docker model` 命令，并在 Docker Desktop Dashboard 的 **Models** 选项卡中查看和与本地模型交互。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，此设置位于 **Features in development** 页面的 **Experimental features** 选项卡下。

### 在 Docker Engine 中启用 DMR

1. 确保你已安装 [Docker Engine](/engine/install/)。
1. DMR 作为软件包提供。要安装它，运行：

   {{< tabs >}}
   {{< tab name="Ubuntu/Debian">}}

   ```console
   $ sudo apt-get update
   $ sudo apt-get install docker-model-plugin
   ```

   {{< /tab >}}
   {{< tab name="RPM-base distributions">}}

   ```console
   $ sudo dnf update
   $ sudo dnf install docker-model-plugin
   ```

   {{< /tab >}}
   {{< /tabs >}}

1. 测试安装：

   ```console
   $ docker model version
   $ docker model run ai/smollm2
   ```

1. 可选：要启用 TCP 支持，使用 `DMR_RUNNER_PORT` 环境变量设置端口。
1. 可选：如果你启用了 TCP 支持，可以使用 `DMR_ORIGINS` 环境变量配置 CORS 允许的来源。可能的值为：
   - `*`：允许所有来源
   - 允许来源的逗号分隔列表
   - 未指定时，拒绝所有来源。

## 拉取模型

模型缓存在本地。

> [!NOTE]
>
> 使用 Docker CLI 时，你也可以直接从 [HuggingFace](https://huggingface.co/) 拉取模型。

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

1. 选择 **Models** 并选择 **Docker Hub** 选项卡。
1. 找到你选择的模型并选择 **Pull**。

![Docker Hub 视图截图](./images/dmr-catalog.png)

{{< /tab >}}
{{< tab name="从 Docker CLI">}}

使用 [`docker model pull` 命令](/reference/cli/docker/model/pull/)。例如：

```bash {title="从 Docker Hub 拉取"}
docker model pull ai/smollm2:360M-Q4_K_M
```

```bash {title="从 HuggingFace 拉取"}
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

{{< /tab >}}
{{< /tabs >}}

## 运行模型

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

1. 选择 **Models** 并选择 **Local** 选项卡
1. 点击播放按钮。交互式聊天屏幕打开。

![Local 视图截图](./images/dmr-run.png)

{{< /tab >}}
{{< tab name="从 Docker CLI" >}}

使用 [`docker model run` 命令](/reference/cli/docker/model/run/)。

{{< /tab >}}
{{< /tabs >}}

## 故障排除

要排查潜在问题，请显示日志：

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

选择 **Models** 并选择 **Logs** 选项卡。

![Models 视图截图](./images/dmr-logs.png)

{{< /tab >}}
{{< tab name="从 Docker CLI">}}

使用 [`docker model logs` 命令](/reference/cli/docker/model/logs/)。

{{< /tab >}}
{{< /tabs >}}

## 发布模型

> [!NOTE]
>
> 这适用于任何支持 OCI 制品的容器注册表，不仅仅是 Docker Hub。

你可以使用新名称标记现有模型并在不同的命名空间和仓库下发布它们：

```console
# Tag a pulled model under a new name
$ docker model tag ai/smollm2 myorg/smollm2

# Push it to Docker Hub
$ docker model push myorg/smollm2
```

有关更多详细信息，请参阅 [`docker model tag`](/reference/cli/docker/model/tag) 和 [`docker model push`](/reference/cli/docker/model/push) 命令文档。

你也可以直接将 GGUF 格式的模型文件打包为 OCI 制品并发布到 Docker Hub。

```console
# Download a model file in GGUF format, e.g. from HuggingFace
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# Package it as OCI Artifact and push it to Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

有关更多详细信息，请参阅 [`docker model package`](/reference/cli/docker/model/package/) 命令文档。

## 示例：将 Docker Model Runner 集成到软件开发生命周期中

你现在可以开始构建由 Docker Model Runner 提供支持的生成式 AI 应用程序。

如果你想尝试现有的 GenAI 应用程序，请按照以下说明操作。

1. 设置示例应用程序。克隆并运行以下仓库：

   ```console
   $ git clone https://github.com/docker/hello-genai.git
   ```

2. 在终端中，导航到 `hello-genai` 目录。

3. 运行 `run.sh` 拉取所选模型并运行应用程序：

4. 在仓库 [README](https://github.com/docker/hello-genai) 中指定的地址在浏览器中打开你的应用程序。

你将看到 GenAI 应用程序的界面，可以在其中开始输入提示词。

你现在可以与由本地模型提供支持的自己的 GenAI 应用程序交互。尝试一些提示词，注意响应有多快——全部在你的机器上使用 Docker 运行。

## 常见问题

### 有哪些可用的模型？

所有可用的模型都托管在 [`ai` 的公共 Docker Hub 命名空间](https://hub.docker.com/u/ai)中。

### 有哪些可用的 CLI 命令？

请参阅[参考文档](/reference/cli/docker/model/)。

### 有哪些可用的 API 端点？

启用该功能后，新的 API 端点在以下基础 URL 下可用：

{{< tabs >}}
{{< tab name="Docker Desktop">}}

- 从容器内：`http://model-runner.docker.internal/`
- 从主机进程：`http://localhost:12434/`，假设在默认端口（12434）上启用了 TCP 主机访问。

{{< /tab >}}
{{< tab name="Docker Engine">}}

- 从容器内：`http://172.17.0.1:12434/`（其中 `172.17.0.1` 代表主机网关地址）
- 从主机进程：`http://localhost:12434/`

> [!NOTE]
> `172.17.0.1` 接口可能默认对 Compose 项目内的容器不可用。
> 在这种情况下，在 Compose 服务 YAML 中添加 `extra_hosts` 指令：
>
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
> 然后你可以在 http://model-runner.docker.internal:12434/ 访问 Docker Model Runner API

{{< /tab >}}
{{</tabs >}}

Docker Model 管理端点：

```text
POST /models/create
GET /models
GET /models/{namespace}/{name}
DELETE /models/{namespace}/{name}
```

OpenAI 端点：

```text
GET /engines/llama.cpp/v1/models
GET /engines/llama.cpp/v1/models/{namespace}/{name}
POST /engines/llama.cpp/v1/chat/completions
POST /engines/llama.cpp/v1/completions
POST /engines/llama.cpp/v1/embeddings
```

要通过 Unix 套接字（`/var/run/docker.sock`）调用这些端点，在其路径前加上 `/exp/vDD4.40`。

> [!NOTE]
> 你可以从路径中省略 `llama.cpp`。例如：`POST /engines/v1/chat/completions`。

### 如何通过 OpenAI API 交互？

#### 从容器内

要使用 `curl` 从另一个容器内调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl http://model-runner.docker.internal/engines/llama.cpp/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'

```

#### 使用 TCP 从主机

要通过 TCP 从主机调用 `chat/completions` OpenAI 端点：

1. 从 Docker Desktop GUI 启用主机端 TCP 支持，或通过 [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md)。
   例如：`docker desktop enable model-runner --tcp <port>`。

   如果你在 Windows 上运行，还要启用 GPU 支持的推理。
   请参阅[启用 Docker Model Runner](#在-docker-desktop-中启用-dmr)。

2. 如上一节所述，使用 `localhost` 和正确的端口与其交互。

```bash
#!/bin/sh

	curl http://localhost:12434/engines/llama.cpp/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

#### 使用 Unix 套接字从主机

要使用 `curl` 通过 Docker 套接字从主机调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl --unix-socket $HOME/.docker/run/docker.sock \
    localhost/exp/vDD4.40/engines/llama.cpp/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

## 已知问题

### `docker model` 未被识别

如果你运行 Docker Model Runner 命令并看到：

```text
docker: 'model' is not a docker command
```

这意味着 Docker 找不到插件，因为它不在预期的 CLI 插件目录中。

要修复此问题，创建一个符号链接以便 Docker 可以检测到它：

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

链接后，重新运行命令。

### 运行超大模型没有保护措施

目前，Docker Model Runner 不包含防止你启动超出系统可用资源的模型的保护措施。尝试运行对于主机机器来说太大的模型可能会导致严重的速度变慢或使系统暂时无法使用。当在没有足够 GPU 内存或系统 RAM 的情况下运行 LLM 时，此问题尤其常见。

### Model CLI 中不一致的摘要支持

Docker Model CLI 目前缺乏对按镜像摘要指定模型的一致支持。作为临时解决方法，你应该按名称而不是摘要引用模型。

## 分享反馈

感谢你试用 Docker Model Runner。通过 **Enable Docker Model Runner** 设置旁边的 **Give feedback** 链接提供反馈或报告你可能发现的任何错误。
