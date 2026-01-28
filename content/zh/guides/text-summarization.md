---
title: 构建文本摘要应用
linkTitle: 文本摘要
keywords: nlp, natural language processing, text summarization, python, bert extractive summarizer
description: 了解如何使用 Python、Bert Extractive Summarizer 和 Docker 构建和运行文本摘要应用程序。
summary: |
  本指南展示了如何使用 Docker 容器化文本摘要模型。
tags: [ai]
languages: [python]
alias:
  - /guides/use-case/nlp/text-summarization/
params:
  time: 20 minutes
---

## 概览

在本指南中，你将学习如何构建和运行文本摘要应用程序。你将使用 Python 和 Bert Extractive Summarizer 构建应用程序，然后使用 Docker 设置环境并运行应用程序。

示例文本摘要应用程序使用 Bert Extractive Summarizer。此工具利用 HuggingFace Pytorch transformers 库来运行提取式摘要。其工作原理是首先嵌入句子，然后运行聚类算法，找到最接近聚类质心的句子。

## 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 你有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 获取示例应用程序

1. 打开终端，使用以下命令克隆示例应用程序的存储库。

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. 验证你是否已克隆存储库。

   你应该在 `Docker-NLP` 目录中看到以下文件。

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

文本摘要应用程序的源代码位于 `Docker-NLP/04_text_summarization.py` 文件中。在文本或代码编辑器中打开 `04_text_summarization.py`，按照以下步骤探索其内容。

1. 导入所需的库。

   ```python
   from summarizer import Summarizer
   ```

   这行代码从 `summarizer` 包中导入 `Summarizer` 类，这对于你的文本摘要应用程序至关重要。summarizer 模块实现了 Bert Extractive Summarizer，利用了在 NLP（自然语言处理）领域著名的 HuggingFace Pytorch transformers 库。该库提供对预训练模型（如 BERT）的访问，这些模型彻底改变了包括文本摘要在内的语言理解任务。

   BERT 模型，即来自 Transformers 的双向编码器表示，擅长理解语言中的上下文，使用一种称为“注意力”的机制来确定句子中单词的重要性。对于摘要，该模型嵌入句子，然后使用聚类算法识别关键句子，即那些最接近这些聚类质心的句子，从而有效地捕捉文本的主要思想。

2. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   这个 Python 习语确保只有当此脚本作为主程序运行时才会运行以下代码块。它提供了灵活性，允许脚本既可以作为独立程序运行，也可以作为模块导入。

3. 创建无限循环以进行连续输入。

   ```python
      while True:
         input_text = input("Enter the text for summarization (type 'exit' to end): ")

         if input_text.lower() == 'exit':
            print("Exiting...")
            break
   ```

   一个无限循环不断提示你输入文本，确保交互性。当输入 `exit` 时，循环中断，让你有效地控制应用程序流程。

4. 创建 Summarizer 实例。

   ```python
         bert_model = Summarizer()
   ```

   在这里，你创建一个名为 `bert_model` 的 Summarizer 类实例。此实例现在准备好使用 BERT 模型执行摘要任务，将嵌入句子和聚类的复杂过程简化为可访问的接口。

5. 生成并打印摘要。

   ```python
   summary = bert_model(input_text)
   print(summary)
   ```

   你的输入文本由 bert_model 实例处理，然后返回摘要版本。这演示了 Python 高级库在用最少的代码实现复杂操作方面的强大功能。

6. 创建 `requirements.txt`。示例应用程序已包含 `requirements.txt` 文件，用于指定应用程序导入的必要模块。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

   ```text
   ...

   # 04 text_summarization
   bert-extractive-summarizer==0.10.1

   ...

   torch==2.1.2
   ```

   文本摘要应用程序需要 `bert-extractive-summarizer` 和 `torch` 模块。summarizer 模块生成输入文本的摘要。这需要 PyTorch，因为用于生成摘要的底层 BERT 模型是在 PyTorch 中实现的。

## 探索应用程序环境

你将使用 Docker 在容器中运行应用程序。Docker 允许你容器化应用程序，为其运行提供一致且隔离的环境。这意味着无论底层系统有何差异，应用程序都将在其 Docker 容器内按预期运行。

要在容器中运行应用程序，需要一个 Dockerfile。Dockerfile 是一个文本文档，其中包含你在命令行上调用以组装镜像的所有命令。镜像是用于创建 Docker 容器的只读模板，其中包含指令。

示例应用程序已包含一个 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释了 `Dockerfile` 的每个部分。有关更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令为构建奠定基础。`python:3.8-slim` 是 Python 3.8 镜像的轻量级版本，针对大小和速度进行了优化。使用此 slim 镜像可以减小 Docker 镜像的整体大小，从而加快下载速度并减少安全漏洞的攻击面。这对于可能不需要完整标准 Python 镜像的基于 Python 的应用程序特别有用。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 设置 Docker 镜像内当前的工作目录。通过将其设置为 `/app`，你可以确保 Dockerfile 中的所有后续命令（如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于组织你的 Docker 镜像，因为所有与应用程序相关的文件都包含在特定目录中。

3. 将需求文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从你的本地机器传输到 Docker 镜像中。此文件列出了应用程序所需的所有 Python 依赖项。将其复制到容器中可以让下一个命令 (`RUN pip install`) 在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）来安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减小 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤特定于需要 spaCy 库的 NLP 应用程序。它下载 `en_core_web_sm` 模型，这是一个用于 spaCy 的小型英语语言模型。虽然此应用程序不需要，但包含它是为了与可能使用此 Dockerfile 的其他 NLP 应用程序兼容。

6. 将应用程序代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将你的 Python 脚本和 `entrypoint.sh` 脚本复制到镜像的 `/app` 目录中。这至关重要，因为容器需要这些脚本来运行应用程序。`entrypoint.sh` 脚本特别重要，因为它规定了应用程序如何在容器内启动。

7. 设置 `entrypoint.sh` 脚本的权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 的文件权限，使其可执行。此步骤对于确保 Docker 容器可以运行此脚本以启动应用程序是必要的。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令配置容器以将 `entrypoint.sh` 作为其默认可执行文件运行。这意味着当容器启动时，它会自动执行该脚本。

   你可以通过在代码或文本编辑器中打开 `entrypoint.sh` 脚本来探索它。由于该示例包含多个应用程序，因此该脚本允许你指定容器启动时运行哪个应用程序。

## 运行应用程序

要使用 Docker 运行应用程序：

1. 构建镜像。

   在终端中，在 `Dockerfile` 所在的目录内运行以下命令。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是命令的细分：

   - `docker build`：这是用于从 Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志代表 tag（标记）。它为镜像分配一个名称，在本例中为 `basic-nlp`。标记是稍后引用镜像的一种便捷方式，尤其是在将镜像推送到注册表或运行容器时。
   - `.`：这是命令的最后一部分，指定构建上下文。句点 (`.`) 表示当前目录。Docker 将在此目录中查找 Dockerfile。构建上下文（在本例中为当前目录）被发送到 Docker 守护进程以启用构建。它包括指定目录中的所有文件和子目录。

   有关更多详细信息，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/).

   Docker 在构建镜像时会向控制台输出多个日志。你会看到它下载并安装依赖项。根据你的网络连接，这可能需要几分钟。Docker 具有缓存功能，因此后续构建可能会更快。完成后，控制台将返回提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 04_text_summarization.py
   ```

   以下是命令的细分：

   - `docker run`：这是用于从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：即使未附加，这也保持标准输入 (STDIN) 打开。它允许容器在前台保持运行并具有交互性。
     - `-t` or `--tty`：这分配一个伪 TTY，本质上是模拟终端，如命令提示符或 shell。它是让你与容器内的应用程序进行交互的原因。
   - `basic-nlp`：这指定用于创建容器的 Docker 镜像的名称。在这种情况下，它是你使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `04_text_summarization.py`：这是你要在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   有关更多详细信息，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/).

   > [!NOTE]
   > 
   > 对于 Windows 用户，运行容器时可能会遇到错误。验证 `entrypoint.sh` 中的行尾是 `LF` (`\n`) 而不是 `CRLF` (`\r\n`)，然后重建镜像。有关更多详细信息，请参阅 [避免意外的语法错误，对容器中的文件使用 Unix 风格的行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers)。

   容器启动后，你将在控制台中看到以下内容。

   ```console
   Enter the text for summarization (type 'exit' to end):
   ```

3. 测试应用程序。

   输入一些文本以获取文本摘要。

   ```console
   Enter the text for summarization (type 'exit' to end): Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making. AI technologies can be classified into two main types: narrow or weak AI, which is designed for a particular task, and general or strong AI, which possesses the ability to understand, learn, and apply knowledge across various domains. One of the most popular approaches in AI is machine learning, where algorithms are trained on large datasets to recognize patterns and make predictions.

   Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making.
   ```

## 总结

在本指南中，你学习了如何构建和运行文本摘要应用程序。你学习了如何使用 Python 和 Bert Extractive Summarizer 构建应用程序，然后使用 Docker 设置环境并运行应用程序。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Bert Extractive Summarizer](https://github.com/dmmiller612/bert-extractive-summarizer)
- [PyTorch](https://pytorch.org/)
- [Python 文档](https://docs.python.org/3/)

## 后续步骤

探索更多 [自然语言处理指南](./_index.md)。
