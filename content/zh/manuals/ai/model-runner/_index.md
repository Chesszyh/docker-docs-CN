---
title: Docker 模型运行器
params:
  sidebar:
    badge:
      color: blue
      text: Beta
    group: AI
weight: 20
description: 了解如何使用 Docker 模型运行器管理和运行 AI 模型。
keywords: Docker, ai, 模型运行器, docker desktop, docker engine, llm
aliases:
  - /desktop/features/model-runner/
  - /model-runner/
---

{{< summary-bar feature_name="Docker 模型运行器" >}}

Docker 模型运行器使使用 Docker 管理、运行和部署 AI 模型变得容易。Docker 模型运行器专为开发人员设计，简化了直接从 Docker Hub 或任何 OCI 兼容注册表拉取、运行和提供大型语言模型 (LLM) 和其他 AI 模型的过程。

通过与 Docker Desktop 和 Docker Engine 的无缝集成，您可以通过 OpenAI 兼容的 API 提供模型，将 GGUF 文件打包为 OCI 工件，并从命令行和图形界面与模型交互。

无论您是构建生成式 AI 应用程序、试验机器学习工作流程，还是将 AI 集成到您的软件开发生命周期中，Docker 模型运行器都提供了一种一致、安全和高效的方式来在本地使用 AI 模型。

## 主要功能

- [从 Docker Hub 拉取和推送模型](https://hub.docker.com/u/ai)
- 在 OpenAI 兼容的 API 上提供模型，以便与现有应用程序轻松集成
- 将 GGUF 文件打包为 OCI 工件并发布到任何容器注册表
- 直接从命令行或 Docker Desktop GUI 运行和交互 AI 模型
- 管理本地模型并显示日志

## 要求

Docker 模型运行器支持以下平台：

{{< tabs >}}
{{< tab name="Windows">}}

Windows(amd64):
- NVIDIA GPU
- NVIDIA 驱动程序 576.57+

Windows(arm64):
- Adreno 的 OpenCL
- Qualcomm Adreno GPU（6xx 系列及更高版本）
    
  > [!NOTE]
  > 某些 llama.cpp 功能可能无法在 6xx 系列上完全支持。

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

模型在首次使用时从 Docker Hub 拉取并存储在本地。它们仅在运行时收到请求时才加载到内存中，并在不使用时卸载以优化资源。由于模型可能很大，初始拉取可能需要一些时间——但之后，它们会缓存在本地以加快访问速度。您可以使用 [OpenAI 兼容的 API](#what-api-endpoints-are-available) 与模型交互。

> [!TIP]
>
> 使用 Testcontainers 或 Docker Compose？
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/)
> 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/)，以及
> [Docker Compose](/manuals/ai/compose/models-and-compose.md) 现在支持 Docker 模型运行器。

## 启用 Docker 模型运行器

### 在 Docker Desktop 中启用 DMR

1. 在设置视图中，导航到**Beta 功能**选项卡。
1. 勾选**启用 Docker 模型运行器**设置。
1. 如果您在支持 NVIDIA GPU 的 Windows 上运行，您还应该看到并能够勾选**启用 GPU 支持的推理**设置。
1. 可选：如果您想启用 TCP 支持，请选择**启用主机端 TCP 支持**
   1. 在**端口**字段中，键入您选择的端口。
   1. 如果您正在从本地前端 Web 应用程序与模型运行器交互，
      在**CORS 允许来源**中，选择模型运行器应接受请求的来源。
      来源是您的 Web 应用程序运行的 URL，例如 `http://localhost:3131`。

您现在可以在 CLI 中使用 `docker model` 命令，并在 Docker Desktop 仪表板的**模型**选项卡中查看和与您的本地模型交互。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，此设置位于**开发中功能**页面上的**实验性功能**选项卡下。

### 在 Docker Engine 中启用 DMR

1. 确保您已安装 [Docker Engine](/engine/install/)。
1. DMR 可作为软件包使用。要安装它，请运行：

   {{< tabs >}}
   {{< tab name="Ubuntu/Debian">}}

   ```console
   $ sudo apt-get update
   $ sudo apt-get install docker-model-plugin
   ```

   {{< /tab >}}
   {{< tab name="基于 RPM 的发行版">}}

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
1. 可选：如果您启用了 TCP 支持，您可以使用 `DMR_ORIGINS` 环境变量配置 CORS 允许的来源。可能的值是：
   - `*`：允许所有来源
   - 逗号分隔的允许来源列表
   - 未指定时，所有来源都被拒绝。

## 拉取模型

模型缓存在本地。

> [!NOTE]
>
> 使用 Docker CLI 时，您还可以直接从 [HuggingFace](https://huggingface.co/) 拉取模型。

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

1. 选择**模型**并选择**Docker Hub**选项卡。
1. 找到您选择的模型并选择**拉取**。

![Docker Hub 视图的屏幕截图](./images/dmr-catalog.png)

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

1. 选择**模型**并选择**本地**选项卡
1. 单击播放按钮。交互式聊天屏幕打开。

![本地视图的屏幕截图](./images/dmr-run.png)

{{< /tab >}}
{{< tab name="从 Docker CLI" >}}

使用 [`docker model run` 命令](/reference/cli/docker/model/run/)。

{{< /tab >}}
{{< /tabs >}}

## 故障排除

要排除潜在问题，请显示日志：

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

选择**模型**并选择**日志**选项卡。

![模型视图的屏幕截图](./images/dmr-logs.png)

{{< /tab >}}
{{< tab name="从 Docker CLI">}}

使用 [`docker model logs` 命令](/reference/cli/docker/model/logs/)。

{{< /tab >}}
{{< /tabs >}}

## 发布模型

> [!NOTE]
>
> 这适用于任何支持 OCI 工件的容器注册表，而不仅仅是 Docker Hub。

您可以为现有模型标记新名称，并将其发布到不同的命名空间和存储库下：

```console
# 为拉取的模型标记新名称
$ docker model tag ai/smollm2 myorg/smollm2

# 将其推送到 Docker Hub
$ docker model push myorg/smollm2
```

有关更多详细信息，请参阅 [`docker model tag`](/reference/cli/docker/model/tag) 和 [`docker model push`](/reference/cli/docker/model/push) 命令文档。

您还可以直接将 GGUF 格式的模型文件打包为 OCI 工件并将其发布到 Docker Hub。

```console
# 下载 GGUF 格式的模型文件，例如从 HuggingFace
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# 将其打包为 OCI 工件并推送到 Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

有关更多详细信息，请参阅 [`docker model package`](/reference/cli/docker/model/package/) 命令文档。

## 示例：将 Docker 模型运行器集成到您的软件开发生命周期中

您现在可以开始构建由 Docker 模型运行器提供支持的生成式 AI 应用程序。

如果您想尝试现有的 GenAI 应用程序，请按照以下说明操作。

1. 设置示例应用程序。克隆并运行以下存储库：

   ```console
   $ git clone https://github.com/docker/hello-genai.git
   ```

2. 在您的终端中，导航到 `hello-genai` 目录。

3. 运行 `run.sh` 以拉取所选模型并运行应用程序：

4. 在浏览器中打开您的应用程序，地址在存储库 [README](https://github.com/docker/docker/hello-genai) 中指定。

您将看到 GenAI 应用程序的界面，您可以在其中开始输入提示。

您现在可以与您自己的 GenAI 应用程序交互，该应用程序由本地模型提供支持。尝试一些提示，并注意响应速度有多快——所有这些都在您的机器上使用 Docker 运行。

## 常见问题解答

### 有哪些模型可用？

所有可用模型都托管在 [Docker Hub 的 `ai` 公共命名空间](https://hub.docker.com/u/ai)中。

### 有哪些 CLI 命令可用？

请参阅[参考文档](/reference/cli/docker/model/)。

### 有哪些 API 端点可用？

启用该功能后，以下基本 URL 下将提供新的 API 端点：

{{< tabs >}}
{{< tab name="Docker Desktop">}}

- 从容器：`http://model-runner.docker.internal/`
- 从主机进程：`http://localhost:12434/`，假设在默认端口 (12434) 上启用了 TCP 主机访问。

{{< /tab >}}
{{< tab name="Docker Engine">}}

- 从容器：`http://172.17.0.1:12434/`（其中 `172.17.0.1` 表示主机网关地址）
- 从主机进程：`http://localhost:12434/`

> [!NOTE]
> 默认情况下，`172.17.0.1` 接口可能不适用于 Compose 项目中的容器。
> 在这种情况下，请在 Compose 服务 YAML 中添加 `extra_hosts` 指令：
> 
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
> 然后您可以通过 http://model-runner.docker.internal:12434/ 访问 Docker 模型运行器 API

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

要通过 Unix 套接字 (`/var/run/docker.sock`) 调用这些端点，请在其路径前加上
`/exp/vDD4.40`。

> [!NOTE]
> 您可以省略路径中的 `llama.cpp`。例如：`POST /engines/v1/chat/completions`。

### 如何通过 OpenAI API 进行交互？

#### 从容器内部

要从另一个容器内部使用 `curl` 调用 `chat/completions` OpenAI 端点：

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
                "content": "请写 500 字关于罗马帝国的衰落。"
            }
        ]
    }'

```

#### 从主机使用 TCP

要从主机通过 TCP 调用 `chat/completions` OpenAI 端点：

1. 从 Docker Desktop GUI 或通过 [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 启用主机端 TCP 支持。
   例如：`docker desktop enable model-runner --tcp <port>`。

   如果您在 Windows 上运行，也请启用 GPU 支持的推理。
   请参阅[启用 Docker 模型运行器](#enable-dmr-in-docker-desktop)。

2. 按照上一节中的说明使用 `localhost` 和正确的端口进行交互。

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
                "content": "请写 500 字关于罗马帝国的衰落。"
            }
        ]
    }'
```

#### 从主机使用 Unix 套接字

要通过 Docker 套接字从主机使用 `curl` 调用 `chat/completions` OpenAI 端点：

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
                "content": "请写 500 字关于罗马帝国的衰落。"
            }
        ]
    }'
```

## 已知问题

### `docker model` 未被识别

如果您运行 Docker 模型运行器命令并看到：

```text
docker: 'model' 不是 docker 命令
```

这意味着 Docker 找不到插件，因为它不在预期的 CLI 插件目录中。

要解决此问题，请创建符号链接，以便 Docker 可以检测到它：

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

链接后，重新运行命令。

### 没有运行超大模型的保护措施

目前，Docker 模型运行器不包含防止您启动超出系统可用资源的模型。
尝试运行对于主机机器来说过大的模型可能会导致严重的
速度下降或可能导致系统暂时无法使用。此问题在没有足够 GPU 内存或系统
RAM 的情况下运行 LLM 时尤其常见。

### 模型 CLI 中没有一致的摘要支持

Docker 模型 CLI 目前缺乏对通过镜像摘要指定模型的一致支持。作为临时解决方案，您应该通过名称而不是摘要来引用模型。

## 分享反馈

感谢您试用 Docker 模型运行器。通过**启用 Docker 模型运行器**设置旁边的**提供反馈**链接提供反馈或报告您可能发现的任何错误。