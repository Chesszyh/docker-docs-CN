---
title: GenAI 视频转录和聊天
linkTitle: 视频转录和聊天
description: 探索使用 Docker、OpenAI 和 Pinecone 的生成式 AI 视频分析应用程序。
keywords: python, generative ai, genai, llm, whisper, pinecone, openai, whisper
summary: |
  了解如何使用 Docker 构建和部署生成式 AI 视频分析和转录机器人。
tags: [ai]
aliases:
  - /guides/use-case/genai-video-bot/
params:
  time: 20 minutes
---

## 概览

本指南介绍了一个使用与 [GenAI Stack](https://www.docker.com/blog/introducing-a-new-genai-stack/) 相关的一组技术进行视频转录和分析的项目。

该项目展示了以下技术：

- [Docker 和 Docker Compose](#docker-and-docker-compose)
- [OpenAI](#openai-api)
- [Whisper](#whisper)
- [Embeddings](#embeddings)
- [Chat completions](#chat-completions)
- [Pinecone](#pinecone)
- [检索增强生成](#retrieval-augmented-generation)

> **致谢**
>
> 本指南是社区贡献。Docker 感谢 [David Cardozo](https://www.davidcardozo.com/) 对本指南的贡献。

## 先决条件

- 您拥有一个 [OpenAI API 密钥](https://platform.openai.com/api-keys)。

  > [!NOTE]
  >
  > OpenAI 是第三方托管服务，可能会 [收费](https://openai.com/pricing)。

- 您拥有一个 [Pinecone API 密钥](https://app.pinecone.io/)。
- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 您拥有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

## 关于应用程序

该应用程序是一个聊天机器人，可以回答视频中的问题。此外，它还提供视频中的时间戳，这可以帮助您找到用于回答问题的来源。

## 获取并运行应用程序

1. 克隆示例应用程序的存储库。在终端中，运行以下命令。

   ```console
   $ git clone https://github.com/Davidnet/docker-genai.git
   ```

   该项目包含以下目录和文件：

   ```text
   ├── docker-genai/
   │ ├── docker-bot/
   │ ├── yt-whisper/
   │ ├── .env.example
   │ ├── .gitignore
   │ ├── LICENSE
   │ ├── README.md
   │ └── docker-compose.yaml
   ```

2. 指定您的 API 密钥。在 `docker-genai` 目录中，创建一个名为 `.env` 的文本文件并在其中指定您的 API 密钥。以下是您可以作为示例参考的 `.env.example` 文件的内容。

   ```text
   #----------------------------------------------------------------------------
   # OpenAI
   #----------------------------------------------------------------------------
   OPENAI_TOKEN=your-api-key # Replace your-api-key with your personal API key

   #----------------------------------------------------------------------------
   # Pinecone
   #----------------------------------------------------------------------------
   PINECONE_TOKEN=your-api-key # Replace your-api-key with your personal API key
   ```

3. 构建并运行应用程序。在终端中，切换到您的 `docker-genai` 目录并运行以下命令。

   ```console
   $ docker compose up --build
   ```

   Docker Compose 根据 `docker-compose.yaml` 文件中定义的服务构建并运行应用程序。当应用程序运行时，您将在终端中看到 2 个服务的日志。

   在日志中，您将看到服务暴露在端口 `8503` 和 `8504` 上。
   这两个服务是互补的。

   `yt-whisper` 服务在端口 `8503` 上运行。此服务将您想要归档到知识数据库中的视频提供给 Pinecone 数据库。下一节将探讨此服务。

## 使用 yt-whisper 服务

yt-whisper 服务是一个 YouTube 视频处理服务，它使用 OpenAI Whisper 模型生成视频的转录并将它们存储在 Pinecone 数据库中。以下步骤展示了如何使用该服务。

1. 打开浏览器并在 [http://localhost:8503](http://localhost:8503) 访问 yt-whisper 服务。
2. 应用程序出现后，在 **Youtube URL** 字段中指定 Youtube 视频 URL 并选择 **Submit**。以下示例使用 [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU)。

   ![在 yt-whisper 服务中提交视频](images/yt-whisper.webp)

   yt-whisper 服务下载视频的音频，使用 Whisper 将其转录为 WebVTT (`*.vtt`) 格式（您可以下载），然后使用 text-embedding-3-small 模型创建嵌入，最后将这些嵌入上传到 Pinecone 数据库中。

   处理视频后，Web 应用程序中会出现一个视频列表，通知您哪些视频已在 Pinecone 中建立了索引。它还提供了一个下载转录的按钮。

   ![yt-whisper 服务中处理后的视频](images/yt-whisper-2.webp)

   您现在可以访问端口 `8504` 上的 dockerbot 服务并询问有关视频的问题。

## 使用 dockerbot 服务

dockerbot 服务是一个问答服务，它利用 Pinecone 数据库和 AI 模型来提供响应。以下步骤展示了如何使用该服务。

> [!NOTE]
>
> 在使用 dockerbot 服务之前，您必须通过 [yt-whisper 服务](#using-the-yt-whisper-service) 处理至少一个视频。

1. 打开浏览器并在 [http://localhost:8504](http://localhost:8504) 访问该服务。

2. 在 **What do you want to know about your videos?** 文本框中，向 Dockerbot 询问有关 yt-whisper 服务处理过的视频的问题。以下示例询问问题：“What is a sugar cookie?”。
   该问题的答案存在于上一个示例中处理的视频中，
   [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU)。

   ![向 Dockerbot 提问](images/bot.webp)

   在此示例中，Dockerbot 回答了问题并提供了带有时间戳的视频链接，其中可能包含有关答案的更多信息。

   dockerbot 服务获取问题，使用 text-embedding-3-small 模型将其转换为嵌入，查询 Pinecone 数据库以查找类似的嵌入，然后将该上下文传递给 gpt-4-turbo-preview 以生成答案。

3. 选择第一个链接以查看它提供的信息。基于上一个示例，选择
   [https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s](https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s)。

   在示例链接中，您可以看到该视频部分完美地回答了问题“What is a sugar cookie?”。

## 探索应用程序架构

下图显示了应用程序的高级服务架构，其中包括：

- yt-whisper：由 Docker Compose 运行的本地服务，与远程 OpenAI 和 Pinecone 服务交互。
- dockerbot：由 Docker Compose 运行的本地服务，与远程 OpenAI 和 Pinecone 服务交互。
- OpenAI：远程第三方服务。
- Pinecone：远程第三方服务。

![应用程序架构图](images/architecture.webp)

## 探索使用的技术及其作用

### Docker 和 Docker Compose

该应用程序使用 Docker 在容器中运行应用程序，为其运行提供一致且隔离的环境。这意味着无论底层系统有何差异，应用程序都将在其 Docker 容器内按预期运行。要了解有关 Docker 的更多信息，请参阅 [入门概述](/get-started/introduction/_index.md)。

Docker Compose 是一个用于定义和运行多容器应用程序的工具。Compose 使通过单个命令 `docker compose up` 运行此应用程序变得容易。有关更多详细信息，请参阅 [Compose 概述](/manuals/compose/_index.md)。

### OpenAI API

OpenAI API 提供了一种 LLM 服务，该服务以其尖端的 AI 和机器学习技术而闻名。在此应用程序中，OpenAI 的技术用于从音频生成转录（使用 Whisper 模型）并为文本数据创建嵌入，以及生成对用户查询的响应（使用 GPT 和聊天完成）。有关更多详细信息，请参阅 [openai.com](https://openai.com/product)。

### Whisper

Whisper 是由 OpenAI 开发的自动语音识别系统，旨在将口语转录为文本。在此应用程序中，Whisper 用于将 YouTube 视频中的音频转录为文本，从而实现对视频内容的进一步处理和分析。有关更多详细信息，请参阅 [介绍 Whisper](https://openai.com/research/whisper)。

### Embeddings

Embeddings（嵌入）是文本或其他数据类型的数值表示，它们以机器学习算法可以处理的方式捕捉其含义。在此应用程序中，嵌入用于将视频转录转换为向量格式，可以查询和分析该格式以了解其与用户输入的相关性，从而促进应用程序中的高效搜索和响应生成。有关更多详细信息，请参阅 OpenAI 的 [Embeddings](https://platform.openai.com/docs/guides/embeddings) 文档。

![Embedding 图](images/embeddings.webp)

### Chat completions

聊天完成（Chat completion）在此应用程序中通过 OpenAI 的 API 使用，指的是根据给定的上下文或提示生成对话响应。在应用程序中，它用于通过处理和集成来自视频转录和其他输入的信息来为用户查询提供智能的、具有上下文意识的答案，从而增强聊天机器人的交互能力。有关更多详细信息，请参阅 OpenAI 的 [Chat Completions API](https://platform.openai.com/docs/guides/text-generation) 文档。

### Pinecone

Pinecone 是一个针对相似性搜索进行了优化的向量数据库服务，用于构建和部署大规模向量搜索应用程序。在此应用程序中，Pinecone 用于存储和检索视频转录的嵌入，从而基于用户查询在应用程序内实现高效且相关的搜索功能。有关更多详细信息，请参阅 [pincone.io](https://www.pinecone.io/)。

### 检索增强生成

检索增强生成 (Retrieval-Augmented Generation, RAG) 是一种将信息检索与语言模型相结合的技术，用于根据检索到的文档或数据生成响应。在 RAG 中，系统检索相关信息（在本例中，通过来自视频转录的嵌入），然后使用语言模型根据这些检索到的数据生成响应。有关更多详细信息，请参阅 OpenAI 的食谱 [使用 Pinecone 进行检索增强生成问答](https://cookbook.openai.com/examples/vector_databases/pinecone/gen_qa)。

## 后续步骤

探索如何使用生成式 AI [创建 PDF 机器人应用程序](/guides/genai-pdf-bot/_index.md)，或在 [GenAI Stack](https://github.com/docker/genai-stack) 存储库中查看更多 GenAI 示例。
