---
title: 容器化生成式 AI 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: python, generative ai, genai, llm, neo4j, ollama, containerize, initialize, langchain, openai
description: 了解如何容器化生成式 AI (GenAI) 应用程序。
aliases:
  - /guides/use-case/genai-pdf-bot/containerize/
---

## 先决条件

> [!NOTE]
>
> GenAI 应用程序通常可以从 GPU 加速中受益。目前 Docker Desktop 仅在 [使用 WSL2 后端的 Windows](/manuals/desktop/features/gpu.md#using-nvidia-gpus-with-wsl2) 上支持 GPU 加速。Linux 用户也可以使用 [Docker Engine](/manuals/engine/install/_index.md) 的原生安装来访问 GPU 加速。

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)，或者如果您是 Linux 用户并计划使用 GPU 加速，则已安装 [Docker Engine](/manuals/engine/install/_index.md)。Docker 定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 您有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

## 概览

本节将带您完成使用 Docker Desktop 容器化生成式 AI (GenAI) 应用程序的过程。

> [!NOTE]
>
> 您可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用程序中查看更多容器化 GenAI 应用程序的示例。

## 获取示例应用程序

本指南中使用的示例应用程序是 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用程序中 PDF 阅读器应用程序的修改版本。该应用程序是一个全栈 Python 应用程序，允许您针对 PDF 文件提问。

该应用程序使用 [LangChain](https://www.langchain.com/) 进行编排，使用 [Streamlit](https://streamlit.io/) 作为 UI，使用 [Ollama](https://ollama.ai/) 运行 LLM，并使用 [Neo4j](https://neo4j.com/) 存储向量。

克隆示例应用程序。打开终端，切换到您想要工作的目录，然后运行以下命令来克隆存储库：

```console
$ git clone https://github.com/craig-osterhout/docker-genai-sample
```

现在您的 `docker-genai-sample` 目录中应该有以下文件。

```text
├── docker-genai-sample/
│ ├── .gitignore
│ ├── app.py
│ ├── chains.py
│ ├── env.example
│ ├── requirements.txt
│ ├── util.py
│ ├── LICENSE
│ └── README.md
```

## 初始化 Docker 资产

现在您拥有一个应用程序，您可以使用 `docker init` 来创建必要的 Docker 资产以容器化您的应用程序。在 `docker-genai-sample` 目录内，运行 `docker init` 命令。`docker init` 提供了一些默认配置，但您需要回答几个关于您的应用程序的问题。例如，此应用程序使用 Streamlit 运行。请参考以下 `docker init` 示例并为您的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Python
? What version of Python do you want to use? 3.11.4
? What port do you want your app to listen on? 8000
? What is the command to run your app? streamlit run app.py --server.address=0.0.0.0 --server.port=8000
```

现在您的 `docker-genai-sample` 目录中应该有以下内容。

```text
├── docker-genai-sample/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── app.py
│ ├── chains.py
│ ├── compose.yaml
│ ├── env.example
│ ├── requirements.txt
│ ├── util.py
│ ├── Dockerfile
│ ├── LICENSE
│ ├── README.Docker.md
│ └── README.md
```

要了解有关 `docker init` 添加的文件的更多信息，请参阅以下内容：

- [Dockerfile](../../../reference/dockerfile.md)
- [.dockerignore](../../../reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `docker-genai-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

Docker 构建并运行您的应用程序。根据您的网络连接，下载所有依赖项可能需要几分钟时间。当应用程序运行时，您将在终端中看到类似以下的消息。

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8000
server-1  |
```

打开浏览器并在 [http://localhost:8000](http://localhost:8000) 查看应用程序。您应该看到一个简单的 Streamlit 应用程序。该应用程序可能需要几分钟才能下载嵌入模型。下载进行时，右上角会显示 **Running**。

应用程序需要 Neo4j 数据库服务和 LLM 服务才能运行。如果您可以访问在 Docker 外部运行的服务，请指定连接信息并进行尝试。如果您没有运行这些服务，请继续阅读本指南，了解如何使用 Docker 运行部分或全部这些服务。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 总结

在本节中，您学习了如何使用 Docker 容器化并运行您的 GenAI 应用程序。

相关信息：

- [docker init CLI 参考](../../../reference/cli/docker/init.md)

## 后续步骤

在下一节中，您将学习如何使用 Docker 在本地运行您的应用程序、数据库和 LLM 服务。
