---
title: 使用容器进行 RAG 开发
linkTitle: 开发你的应用
weight: 10
keywords: python, local, development, generative ai, genai, llm, rag, ollama
description: 了解如何在本地开发你的生成式 RAG 应用程序。
aliases:
  - /guides/use-case/rag-ollama/develop/
---

## 先决条件

完成 [容器化 RAG 应用程序](containerize.md)。

## 概述

在本节中，你将学习如何设置开发环境以访问你的生成式 RAG 应用程序所需的所有服务。这包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用程序中查看更多容器化 GenAI 应用程序的示例。

## 添加本地数据库

你可以使用容器来设置本地服务，例如数据库。在本节中，你将在 `docker-compose.yaml` 文件中探索数据库服务。

要运行数据库服务：

1. 在克隆的存储库目录中，在 IDE 或文本编辑器中打开 `docker-compose.yaml` 文件。

2. 在 `docker-compose.yaml` 文件中，你将看到以下内容：

   ```yaml
   services:
     qdrant:
       image: qdrant/qdrant
       container_name: qdrant
       ports:
         - "6333:6333"
       volumes:
         - qdrant_data:/qdrant/storage
   ```

   > [!NOTE]
   > 要了解有关 Qdrant 的更多信息，请参阅 [Qdrant 官方 Docker 镜像](https://hub.docker.com/r/qdrant/qdrant)。

3. 启动应用程序。在 `winy` 目录内，在终端中运行以下命令。

   ```console
   $ docker compose up --build
   ```

4. 访问应用程序。打开浏览器并在 [http://localhost:8501](http://localhost:8501) 查看应用程序。你应该会看到一个简单的 Streamlit 应用程序。

5. 停止应用程序。在终端中，按 `ctrl`+`c` 停止应用程序。

## 添加本地或远程 LLM 服务

示例应用程序支持 [Ollama](https://ollama.ai/)。本指南为以下场景提供说明：

- 在容器中运行 Ollama
- 在容器外运行 Ollama

虽然所有平台都可以使用上述任何场景，但性能和 GPU 支持可能会有所不同。你可以使用以下指南来帮助你选择合适的选项：

- 如果你在 Linux 上使用 Docker Engine 的本机安装，或在 Windows 10/11 上使用 Docker Desktop，并且拥有支持 CUDA 的 GPU，且系统至少有 8 GB 内存，请在容器中运行 Ollama。
- 如果在 Linux 机器上运行 Docker Desktop，请在容器外运行 Ollama。

为你的 LLM 服务选择以下选项之一。

{{< tabs >}}
{{< tab name="在容器中运行 Ollama" >}}

当在容器中运行 Ollama 时，你应该拥有一个支持 CUDA 的 GPU。虽然你可以在没有支持 GPU 的情况下在容器中运行 Ollama，但性能可能无法接受。只有 Linux 和 Windows 11 支持对容器的 GPU 访问。

要在容器中运行 Ollama 并提供 GPU 访问：

1. 安装先决条件。
   - 对于 Linux 上的 Docker Engine，安装 [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)。
   - 对于 Windows 10/11 上的 Docker Desktop，安装最新的 [NVIDIA 驱动程序](https://www.nvidia.com/Download/index.aspx) 并确保你使用的是 [WSL2 后端](/manuals/desktop/features/wsl/_index.md#turn-on-docker-desktop-wsl-2)。
2. `docker-compose.yaml` 文件已经包含必要的说明。在你自己的应用程序中，你需要将 Ollama 服务添加到你的 `docker-compose.yaml` 中。以下是更新后的 `docker-compose.yaml`：

   ```yaml
   ollama:
     image: ollama/ollama
     container_name: ollama
     ports:
       - "8000:8000"
     deploy:
       resources:
         reservations:
           devices:
             - driver: nvidia
               count: 1
               capabilities: [gpu]
   ```

   > [!NOTE]
   > 有关 Compose 说明的更多详细信息，请参阅 [使用 Docker Compose 开启 GPU 访问](/manuals/compose/how-tos/gpu-support.md)。

3. 一旦 Ollama 容器启动并运行，就可以使用以下命令使用 `tools` 文件夹中的 `download_model.sh`：

   ```console
   . ./download_model.sh <model-name>
   ```

拉取 Ollama 模型可能需要几分钟。

{{< /tab >}}
{{< tab name="在容器外运行 Ollama" >}}

要在容器外运行 Ollama：

1. 在你的主机上 [安装](https://github.com/jmorganca/ollama) 并运行 Ollama。
2. 使用以下命令将模型拉取到 Ollama。

   ```console
   $ ollama pull llama2
   ```

3. 从 `docker-compose.yaml` 中移除 `ollama` 服务，并正确更新 `winy` 服务中的连接变量：

   ```diff
   - OLLAMA=http://ollama:11434
   + OLLAMA=<your-url>
   ```

{{< /tab >}}
{{< /tabs >}}

## 运行你的 RAG 应用程序

此时，你的 Compose 文件中拥有以下服务：

- 你的主 RAG 应用程序的服务器服务
- 用于在 Qdrant 数据库中存储向量的数据库服务
- （可选）运行 LLM 服务的 Ollama 服务

一旦应用程序运行，打开浏览器并在 [http://localhost:8501](http://localhost:8501) 访问应用程序。

根据你的系统和你选择的 LLM 服务，回答可能需要几分钟。

## 总结

在本节中，你学习了如何设置开发环境以提供访问你的 GenAI 应用程序所需的所有服务。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [GenAI Stack 演示应用程序](https://github.com/docker/genai-stack)

## 下一步

在 [GenAI Stack 演示应用程序](https://github.com/docker/genai-stack) 中查看更多 GenAI 应用程序的示例。
