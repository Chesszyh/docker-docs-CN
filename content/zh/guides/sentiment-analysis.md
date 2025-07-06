---
title: 构建情感分析应用
linkTitle: 情感分析
keywords: nlp, 自然语言处理, 情感分析, python, nltk
description: 了解如何使用 Python、NLTK 和 Docker 构建和运行情感分析应用程序。
summary: |
  本指南演示了如何使用 Docker 容器化情感分析模型。
tags: [ai]
languages: [python]
aliases:
  - /guides/use-case/nlp/sentiment-analysis/
params:
  time: 20 分钟
---

## 概述

在本指南中，您将学习如何构建和运行情感分析应用程序。
您将使用 Python 和自然语言工具包 (NLTK) 构建应用程序，然后使用 Docker 设置环境并运行应用程序。

该应用程序使用 NLTK 的
SentimentIntensityAnalyzer 分析用户输入文本的情感，并输出情感是积极的、
消极的还是中性的。

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 会定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 您有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 获取示例应用程序

1. 打开终端，并使用
   以下命令克隆示例应用程序的存储库。

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. 验证您已克隆存储库。

   您应该在 `Docker-NLP` 目录中看到以下文件。

   ```text
   01_sentiment_analysis.py
   02_name_entity_recognition.py
   03_text_classification.py
   04_text_summarization.py
   05_language_translation.py
   entrypoint.sh
   requirements.txt
   Dockerfile
   README.md
   ```

## 探索应用程序代码

情感分析应用程序的源代码位于 `Docker-NLP/01_sentiment_analysis.py` 文件中。在文本或代码编辑器中打开 `01_sentiment_analysis.py` 以在以下步骤中探索其内容。

1. 导入所需的库。

   ```python
   import nltk
   from nltk.sentiment import SentimentIntensityAnalyzer
   import ssl
   ```

   - `nltk`：这是用于在 Python 中处理
     人类语言数据的自然语言工具包库。
   - `SentimentIntensityAnalyzer`：这是 NLTK 中用于
     确定一段文本情感的特定工具。
   - `ssl`：此模块提供对用于安全 Web 连接的传输层安全性（加密）
     功能的访问。

2. 处理 SSL 证书验证。

   ```python
   try:
       _create_unverified_https_context = ssl._create_unverified_context
   except AttributeError:
       pass
   else:
       ssl._create_default_https_context = _create_unverified_https_context
   ```

   此块是针对某些环境的解决方法，在这些环境中，由于 SSL 证书验证问题，通过 NLTK 下载数据可能会失败。它告诉 Python 忽略 HTTPS 请求的 SSL 证书验证。

3. 下载 NLTK 资源。

   ```python
   nltk.download('vader_lexicon')
   nltk.download('punkt')
   ```

   - `vader_lexicon`：这是 `SentimentIntensityAnalyzer`
     用于情感分析的词典。
   - `punkt`：NLTK 使用它来对句子进行分词。`SentimentIntensityAnalyzer`
     需要它才能正常工作。

4. 创建一个情感分析函数。

   ```python
   def perform_semantic_analysis(text):
       sid = SentimentIntensityAnalyzer()
       sentiment_score = sid.polarity_scores(text)

       if sentiment_score['compound'] >= 0.05:
           return "Positive"
       elif sentiment_score['compound'] <= -0.05:
           return "Negative"
       else:
           return "Neutral"
   ```

   - `SentimentIntensityAnalyzer()` 创建一个
     分析器的实例。
   - `polarity_scores(text)` 为输入文本生成一个情感分数。

   该函数根据
   复合分数返回**积极**、**消极**或**中性**。

5. 创建主循环。

   ```python
   if __name__ == "__main__":
       while True:
           input_text = input("Enter the text for semantic analysis (type 'exit' to end): ")

           if input_text.lower() == 'exit':
               print("Exiting...")
               break

           result = perform_semantic_analysis(input_text)
           print(f"Sentiment: {result}")
   ```

   脚本的这一部分运行一个无限循环以接受用户输入进行
   分析。如果用户键入 `exit`，程序将终止。否则，它会
   打印出所提供文本的情感。

6. 创建 `requirements.txt`。

   示例应用程序已包含
   `requirements.txt` 文件，以指定
   应用程序导入的必要包。在代码或文本编辑器中打开 `requirements.txt` 以
   探索其内容。

   ```text
   # 01 sentiment_analysis
   nltk==3.6.5

   ...
   ```

   情感分析应用程序只需要 `nltk` 包。

## 探索应用程序环境

您将使用 Docker 在容器中运行应用程序。Docker 允许您
将应用程序容器化，为其运行提供一致且隔离的环境
。这意味着无论底层系统差异如何，应用程序都将在其
Docker 容器内按预期运行。

要在容器中运行应用程序，需要一个 Dockerfile。Dockerfile 是
一个文本文档，其中包含您将在命令行中调用以组装镜像的所有命令
。镜像是具有创建
Docker 容器说明的只读模板。

示例应用程序已包含一个 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释了 `Dockerfile` 的每个部分。有关更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令为构建奠定了基础。`python:3.8-slim` 是
   Python 3.8 镜像的轻量级版本，针对大小和速度进行了优化。
   使用此精简镜像可以减小 Docker 镜像的整体大小，从而
   加快下载速度并减少安全漏洞的攻击面。这
   对于您可能不需要完整标准 Python 镜像的基于 Python 的应用程序特别有用
   。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 设置 Docker 镜像中的当前工作目录。通过
   将其设置为 `/app`，您可以确保
   Dockerfile 中的所有后续命令
   （如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于
   组织您的 Docker 镜像，因为所有与应用程序相关的文件都包含在
   一个特定的目录中。

3. 将需求文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从
   您的本地计算机传输到 Docker 镜像中。此文件列出了
   应用程序所需的所有 Python
   依赖项。将其复制到容器中
   可让下一个命令 (`RUN pip install`) 在镜像环境内安装这些依赖项
   。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）来安装
   `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用
   缓存，这通过不存储
   不必要的缓存数据来减小 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤特定于需要 spaCy 库的 NLP 应用程序。它下载 `en_core_web_sm` 模型，这是一个用于 spaCy 的小型英语语言模型。虽然此应用程序不需要它，但为了与可能使用此 Dockerfile 的其他 NLP 应用程序兼容而包含它。

6. 将应用程序代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将您的 Python 脚本和 `entrypoint.sh` 脚本复制到
   镜像的 `/app` 目录中。这至关重要，因为容器需要
   这些脚本来运行应用程序。`entrypoint.sh` 脚本
   尤其重要，因为它规定了应用程序在
   容器内如何启动。

7. 设置 `entrypoint.sh` 脚本的权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 的文件权限，使其
   可执行。此步骤对于确保 Docker 容器可以
   运行此脚本以启动应用程序是必要的。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令将容器配置为运行 `entrypoint.sh`
   作为其默认可执行文件。这意味着当容器启动时，它
   会自动执行该脚本。

   您可以通过在代码或文本
   编辑器中打开 `entrypoint.sh` 脚本来探索它。由于示例包含多个应用程序，因此该脚本可让您
   指定在容器启动时运行哪个应用程序。

## 运行应用程序

要使用 Docker 运行应用程序：

1. 构建镜像。

   在终端中，在 `Dockerfile` 所在的目录内运行以下命令。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是该命令的分解：

   - `docker build`：这是用于从
     Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是
     位于指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志
     代表标记。它为镜像分配一个名称，在本例中为
     `basic-nlp`。标签是以后引用镜像的便捷方式，
     尤其是在将它们推送到注册表或运行容器时。
   - `.`：这是命令的最后一部分，指定了构建上下文。
     句点 (`.`) 表示当前目录。Docker 将在
     此目录中查找 Dockerfile。
     构建上下文（在本例中为当前目录）将发送到 Docker 守护程序以启用构建。它包括
     指定目录中的所有文件和子目录。

   Docker 在构建镜像时会向您的控制台输出几个日志。您将
   看到它下载并安装依赖项。根据您的网络
   连接，这可能需要几分钟时间。Docker 确实有一个缓存
   功能，因此后续构建可以更快。完成后，控制台将
   返回到提示符。

   有关更多详细信息，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 01_sentiment_analysis.py
   ```

   以下是该命令的分解：

   - `docker run`：这是用于从
     Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：即使未附加，也保持标准输入 (STDIN) 打开
       。它让容器保持在前台运行
       并具有交互性。
     - `-t` 或 `--tty`：这会分配一个伪 TTY，本质上是模拟一个
       终端，如命令提示符或 shell。它让您
       可以与容器内的应用程序进行交互。
   - `basic-nlp`：这指定了用于
     创建容器的 Docker 镜像的名称。在这种情况下，它是您使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像
     。
   - `01_sentiment_analysis.py`：这是您要在
     Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在
     容器启动时运行它。

   有关更多详细信息，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   > 
   > 对于 Windows 用户，您在运行容器时可能会遇到错误。验证
   > `entrypoint.sh` 中的行尾是 `LF` (`\n`) 而不是 `CRLF` (`\r\n`)，
   > 然后重新构建镜像。有关更多详细信息，请参阅[避免意外的语法错误，在容器中使用 Unix 样式的行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers)。

   容器启动后，您将在控制台中看到以下内容。

   ```console
   Enter the text for semantic analysis (type 'exit' to end):
   ```

3. 测试应用程序。

   输入评论以获取情感分析。

   ```console
   Enter the text for semantic analysis (type 'exit' to end): I love containers!
   Sentiment: Positive
   Enter the text for semantic analysis (type 'exit' to end): I'm still learning about containers.
   Sentiment: Neutral
   ```

## 总结

在本指南中，您学习了如何构建和运行情感分析
应用程序。您学习了如何使用 Python 和 NLTK 构建应用程序，
然后使用 Docker 设置环境并运行应用程序。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [自然语言工具包](https://www.nltk.org/)
- [Python 文档](https://docs.python.org/3/)

## 后续步骤

探索更多[自然语言处理指南](./_index.md)。
