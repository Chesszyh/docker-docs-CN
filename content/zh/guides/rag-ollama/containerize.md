---
title: 容器化 RAG 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: python, generative ai, genai, llm, ollama, containerize, initialize, qdrant
description: 了解如何容器化 RAG 应用程序。
aliases:
  - /guides/use-case/rag-ollama/containerize/
---

## 概述

本节将带你了解如何使用 Docker 容器化 RAG 应用程序。

> [!NOTE]
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用程序中查看更多容器化 GenAI 应用程序的示例。

## 获取示例应用程序

本指南中使用的示例应用程序是一个 RAG 应用程序的示例，由三个主要组件组成，它们是每个 RAG 应用程序的构建块。一个托管在某处的大型语言模型（LLM），在本例中，它托管在一个容器中并通过 [Ollama](https://ollama.ai/) 提供服务。一个向量数据库 [Qdrant](https://qdrant.tech/)，用于存储本地数据的嵌入（embeddings）。以及一个使用 [Streamlit](https://streamlit.io/) 的 Web 应用程序，为用户提供最佳的用户体验。

克隆示例应用程序。打开终端，将目录切换到你想工作的目录，然后运行以下命令来克隆存储库：

```console
$ git clone https://github.com/mfranzon/winy.git
```

你应该在 `winy` 目录中拥有以下文件。

```text
├── winy/
│ ├── .gitignore
│ ├── app/
│ │ ├── main.py
│ │ ├── Dockerfile
| | └── requirements.txt
│ ├── tools/
│ │ ├── create_db.py
│ │ ├── create_embeddings.py
│ │ ├── requirements.txt
│ │ ├── test.py
| | └── download_model.sh
│ ├── docker-compose.yaml
│ ├── wine_database.db
│ ├── LICENSE
│ └── README.md
```

## 容器化你的应用程序：基础知识

容器化应用程序涉及将其与依赖项一起打包到容器中，这确保了不同环境之间的一致性。以下是容器化像 Winy 这样的应用程序所需的内容：

1. Dockerfile：一个包含如何为你的应用程序构建 Docker 镜像的指令的 Dockerfile。它指定了基础镜像、依赖项、配置文件以及运行应用程序的命令。

2. Docker Compose 文件：Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。Compose 文件允许你在一个文件中配置应用程序的服务、网络和卷。

## 运行应用程序

在 `winy` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

Docker 构建并运行你的应用程序。根据你的网络连接情况，下载所有依赖项可能需要几分钟时间。当应用程序运行时，你将在终端中看到类似以下的消息。

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8501
server-1  |
```

打开浏览器并在 [http://localhost:8501](http://localhost:8501) 查看应用程序。你应该会看到一个简单的 Streamlit 应用程序。

该应用程序需要 Qdrant 数据库服务和 LLM 服务才能正常工作。如果你可以访问在 Docker 之外运行的服务，请在 `docker-compose.yaml` 中指定连接信息。

```yaml
winy:
  build:
    context: ./app
    dockerfile: Dockerfile
  environment:
    - QDRANT_CLIENT=http://qdrant:6333 # Specifies the url for the qdrant database
    - OLLAMA=http://ollama:11434 # Specifies the url for the ollama service
  container_name: winy
  ports:
    - "8501:8501"
  depends_on:
    - qdrant
    - ollama
```

如果你没有运行这些服务，请继续阅读本指南，了解如何使用 Docker 运行部分或全部这些服务。
请记住，`ollama` 服务是空的；它没有任何模型。因此，在开始使用 RAG 应用程序之前，你需要拉取一个模型。所有说明都在下一页。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 总结

在本节中，你学习了如何使用 Docker 容器化并运行你的 RAG 应用程序。

## 下一步

在下一节中，你将学习如何使用 Docker 在完全本地的环境中，使用你首选的 LLM 模型正确配置应用程序。
