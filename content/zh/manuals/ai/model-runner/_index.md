--- 
title: Docker Model Runner
params:
  sidebar:
    badge:
      color: blue
      text: Beta
    group: AI
weight: 20
description: 了解如何使用 Docker Model Runner 管理和运行 AI 模型。
keywords: Docker, ai, model runner, docker desktop, docker engine, llm
alias:
  - /desktop/features/model-runner/
  - /model-runner/
---

{{< summary-bar feature_name="Docker Model Runner" >}}

Docker Model Runner 让使用 Docker 管理、运行和部署 AI 模型变得轻而易举。Docker Model Runner 专为开发人员设计，简化了直接从 Docker Hub 或任何符合 OCI 标准的镜像库拉取、运行和提供大语言模型 (LLM) 及其他 AI 模型服务的过程。

通过与 Docker Desktop 和 Docker Engine 的无缝集成，您可以经由兼容 OpenAI 的 API 提供模型服务，将 GGUF 文件打包为 OCI 构件（Artifacts），并从命令行和图形界面与模型进行交互。

无论您是在构建生成式 AI 应用程序、试验机器学习工作流，还是将 AI 集成到软件开发生命周期中， Docker Model Runner 都为您在本地使用 AI 模型提供了一种一致、安全且高效的方式。

## 主要功能

- [从 Docker Hub 拉取和推送模型](https://hub.docker.com/u/ai)
- 在兼容 OpenAI 的 API 上提供模型服务，以便轻松与现有应用集成
- 将 GGUF 文件打包为 OCI 构件并发布到任何容器镜像库
- 直接从命令行或 Docker Desktop GUI 运行并与 AI 模型交互
- 管理本地模型并显示日志

## 要求 

Docker Model Runner 支持以下平台：

{{< tabs >}}
{{< tab name="Windows">

Windows(amd64):
-  NVIDIA GPU 
-  NVIDIA 驱动程序 576.57+

Windows(arm64):
- OpenCL for Adreno
- Qualcomm Adreno GPU（6xx 系列及更高版本）
    
  > [!NOTE]
  > 在 6xx 系列上，某些 llama.cpp 功能可能无法完全支持。

{{< /tab >}}
{{< tab name="MacOS">

- Apple Silicon

{{< /tab >}}
{{< tab name="Linux">

仅限 Docker Engine：

- Linux CPU 和 Linux NVIDIA
- NVIDIA 驱动程序 575.57.08+

{{< /tab >}}
{{</tabs >}}


## 工作原理

模型在第一次使用时从 Docker Hub 拉取并存储在本地。它们仅在发出请求的运行时才加载到内存中，并在不使用时卸载以优化资源。由于模型可能很大，初始拉取可能需要一些时间，但在此之后，它们将被缓存在本地以实现更快的访问。您可以使用 [兼容 OpenAI 的 API](#可用哪些-api-端点) 与模型进行交互。

> [!TIP]
>
> 正在使用 Testcontainers 或 Docker Compose？
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/) 
> 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/)，以及 
> [Docker Compose](/manuals/ai/compose/models-and-compose.md) 现在都支持 Docker Model Runner。

## 启用 Docker Model Runner

### 在 Docker Desktop 中启用 DMR

1. 在设置视图中，导航至 **Beta features**（Beta 功能）选项卡。
2. 勾选 **Enable Docker Model Runner**（启用 Docker Model Runner）设置。
3. 如果您在运行具有受支持 NVIDIA GPU 的 Windows 上，您还应该看到并能勾选 **Enable GPU-backed inference**（启用 GPU 加速推理）设置。
4. 可选：如果您想启用 TCP 支持，请选择 **Enable host-side TCP support**（启用主机端 TCP 支持）
   1. 在 **Port**（端口）字段中，输入您选择的端口。
   2. 如果您正通过本地前端 Web 应用与 Model Runner 交互，在 **CORS Allows Origins**（CORS 允许源）中选择 Model Runner 应接受请求的源。源是您的 Web 应用运行的 URL，例如 `http://localhost:3131`。

您现在可以在 CLI 中使用 `docker model` 命令，并在 Docker Desktop 仪表板的 **Models**（模型）选项卡中查看本地模型并与之交互。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，此设置位于 **Features in development**（开发中的功能）页面上的 **Experimental features**（实验性功能）选项卡下。

### 在 Docker Engine 中启用 DMR

1. 确保您已安装 [Docker Engine](/engine/install/)。
2. DMR 以软件包形式提供。要安装它，请运行：

   {{< tabs >}}
   {{< tab name="Ubuntu/Debian">

   ```console
   $ sudo apt-get update
   $ sudo apt-get install docker-model-plugin
   ```

   {{< /tab >}}
   {{< tab name="RPM-base distributions">

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

1. 可选：要启用 TCP 支持，请使用 `DMR_RUNNER_PORT` 环境变量设置端口。
1. 可选：如果您启用了 TCP 支持，可以使用 `DMR_ORIGINS` 环境变量配置 CORS 允许源。可能的值包括：
   - `*`：允许所有源
   - 以逗号分隔的允许源列表
   - 未指定时，拒绝所有源。

## 拉取模型

模型会缓存在本地。

> [!NOTE]
>
> 使用 Docker CLI 时，您也可以直接从 [HuggingFace](https://huggingface.co/) 拉取模型。

{{< tabs group="release" >}}
{{< tab name="通过 Docker Desktop">

1. 选择 **Models**（模型）并选择 **Docker Hub** 选项卡。
2. 找到您选择的模型，然后选择 **Pull**（拉取）。

![Docker Hub 视图截图](./images/dmr-catalog.png)

{{< /tab >}}
{{< tab name="通过 Docker CLI">

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
{{< tab name="通过 Docker Desktop">

1. 选择 **Models**（模型）并选择 **Local**（本地）选项卡
2. 点击播放按钮。交互式聊天屏幕将打开。

![本地视图截图](./images/dmr-run.png)

{{< /tab >}}
{{< tab name="通过 Docker CLI" >}}

使用 [`docker model run` 命令](/reference/cli/docker/model/run/)。

{{< /tab >}}
{{< /tabs >}}

## 故障排除

要排除潜在问题，请显示日志：

{{< tabs group="release" >}}
{{< tab name="通过 Docker Desktop">

选择 **Models**（模型）并选择 **Logs**（日志）选项卡。

![模型视图截图](./images/dmr-logs.png)

{{< /tab >}}
{{< tab name="通过 Docker CLI">

使用 [`docker model logs` 命令](/reference/cli/docker/model/logs/)。

{{< /tab >}}
{{< /tabs >}}

## 发布模型

> [!NOTE]
>
> 这适用于任何支持 OCI 构件的容器镜像库，而不仅仅是 Docker Hub。

您可以使用新名称标记现有模型，并将其发布在不同的命名空间和存储库下：

```console
# 使用新名称标记拉取的模型
$ docker model tag ai/smollm2 myorg/smollm2

# 将其推送到 Docker Hub
$ docker model push myorg/smollm2
```

有关更多详情，请参阅 [`docker model tag`](/reference/cli/docker/model/tag) 和 [`docker model push`](/reference/cli/docker/model/push) 命令文档。

您也可以直接将 GGUF 格式的模型文件打包为 OCI 构件，并发布到 Docker Hub。

```console
# 下载 GGUF 格式的模型文件，例如从 HuggingFace 下载
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# 将其打包为 OCI 构件并推送到 Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

有关更多详情，请参阅 [`docker model package`](/reference/cli/docker/model/package/) 命令文档。

## 示例：将 Docker Model Runner 集成到您的软件开发生命周期中

您现在可以开始构建由 Docker Model Runner 驱动的生成式 AI 应用程序。

如果您想尝试现有的 GenAI 应用程序，请按照以下说明操作。

1. 设置示例应用。克隆并运行以下仓库：

   ```console
   $ git clone https://github.com/docker/hello-genai.git
   ```

2. 在终端中，进入 `hello-genai` 目录。

3. 运行 `run.sh` 以拉取选定的模型并运行应用：

4. 在浏览器中打开仓库 [README](https://github.com/docker/hello-genai) 中指定的地址。

您将看到 GenAI 应用的界面，在其中可以开始输入您的提示词。

您现在可以与由本地模型驱动的 GenAI 应用进行交互。尝试输入一些提示词，注意响应速度是多么快——这一切都在您的机器上通过 Docker 运行。

## 常见问题 (FAQ)

### 有哪些可用模型？

所有可用模型都托管在 [Docker Hub 的公共命名空间 `ai`](https://hub.docker.com/u/ai) 中。

### 有哪些可用 CLI 命令？

请参阅 [参考文档](/reference/cli/docker/model/)。

### 可用哪些 API 端点？

功能启用后，可在以下基础 URL 下使用新的 API 端点：

{{< tabs >}}
{{< tab name="Docker Desktop">

- 从容器内部：`http://model-runner.docker.internal/`
- 从宿主机进程：`http://localhost:12434/`（假设已在默认端口 12434 启用了 TCP 主机访问）。

{{< /tab >}}
{{< tab name="Docker Engine">

- 从容器内部：`http://172.17.0.1:12434/`（其中 `172.17.0.1` 代表宿主机网关地址）
- 从宿主机进程：`http://localhost:12434/`

> [!NOTE]
> 对于 Compose 项目中的容器，`172.17.0.1` 接口默认可能不可用。在这种情况下，请在您的 Compose 服务 YAML 中添加 `extra_hosts` 指令：
> 
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
> 然后您就可以通过 http://model-runner.docker.internal:12434/ 访问 Docker Model Runner API。

{{< /tab >}}
{{</tabs >}}

Docker 模型管理端点：

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

要通过 Unix 套接字（`/var/run/docker.sock`）调用这些端点，请在其路径前加上 `/exp/vDD4.40` 前缀。

> [!NOTE]
> 您可以从路径中省略 `llama.cpp`。例如：`POST /engines/v1/chat/completions`。

### 如何通过 OpenAI API 进行交互？

#### 从容器内部

要在另一个容器中使用 `curl` 调用 `chat/completions` OpenAI 端点：

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

#### 通过 TCP 从宿主机交互

要通过 TCP 从宿主机调用 `chat/completions` OpenAI 端点：

1. 通过 Docker Desktop GUI 或 [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 启用主机端 TCP 支持。
   例如：`docker desktop enable model-runner --tcp <port>`。

   如果您在 Windows 上运行，还需要启用 GPU 加速推理。
   请参阅 [在 Docker Desktop 中启用 DMR](#在-docker-desktop-中启用-dmr)。

2. 使用 `localhost` 和正确的端口按照前一节记录的方式进行交互。

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

#### 通过 Unix 套接字从宿主机交互

要通过 Docker 套接字从宿主机使用 `curl` 调用 `chat/completions` OpenAI 端点：

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

如果您运行 Docker Model Runner 命令并看到：

```text
docker: 'model' is not a docker command
```

这意味着 Docker 找不到该插件，因为它不在预期的 CLI 插件目录中。

要修复此问题，请创建一个符号链接，以便 Docker 可以检测到它：

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

链接完成后，重新运行该命令。

### 运行超大模型没有保护措施

目前， Docker Model Runner 不包含防止您启动超过系统可用资源的模型的保护措施。尝试运行对于宿主机来说太大的模型可能会导致严重的性能下降，或者可能使系统暂时无法使用。在没有足够 GPU 显存或系统内存的情况下运行 LLM 时，此问题尤为常见。

### Model CLI 中缺乏一致的 Digest 支持

Docker Model CLI 目前缺乏对通过镜像 Digest 指定模型的一致支持。作为临时的变通方法，您应该通过名称而不是 Digest 来引用模型。

## 分享反馈

感谢您试用 Docker Model Runner。请通过 **Enable Docker Model Runner** 设置旁边的 **Give feedback**（提供反馈）链接分享您的反馈或报告您发现的任何 Bug。
