---
title: 构建语言翻译应用
linkTitle: 语言翻译
keywords: nlp, natural language processing, text summarization, python, language translation, googletrans
description: 学习如何使用 Python、Googletrans 和 Docker 构建和运行语言翻译应用程序。
summary: |
  本指南演示如何使用 Docker 部署用于 NLP 任务的语言翻译模型。
tags: [ai]
languages: [python]
aliases:
  - /guides/use-case/nlp/language-translation/
params:
  time: 20 minutes
---

## 概述

本指南将引导您构建和运行语言翻译应用程序。您将使用 Python 和 Googletrans 构建应用程序，然后使用 Docker 设置环境并运行应用程序。

该应用程序演示了 Googletrans 库在语言翻译中的简单但实用的用法，展示了基本的 Python 和 Docker 概念。Googletrans 是一个免费且无限制的 Python 库，实现了 Google 翻译 API。它使用 Google 翻译 Ajax API 来调用诸如检测和翻译等方法。

## 前提条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 您有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 获取示例应用程序

1. 打开终端，使用以下命令克隆示例应用程序的仓库。

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. 验证您已克隆仓库。

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

应用程序的源代码位于 `Docker-NLP/05_language_translation.py` 文件中。在文本或代码编辑器中打开 `05_language_translation.py` 以在以下步骤中探索其内容。

1. 导入所需的库。

   ```python
   from googletrans import Translator
   ```

   此行从 `googletrans` 导入 `Translator` 类。Googletrans 是一个 Python 库，提供 Google 翻译 AJAX API 的接口。

2. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   这个 Python 惯用法确保以下代码块仅在此脚本是主程序时运行。它提供了灵活性，允许脚本既可以作为独立程序运行，也可以作为导入的模块运行。

3. 创建用于持续输入的无限循环。

   ```python
      while True:
         input_text = input("Enter the text for translation (type 'exit' to end): ")

         if input_text.lower() == 'exit':
            print("Exiting...")
            break
   ```

   这里建立了一个无限循环，持续提示您输入文本，确保交互性。当您输入 `exit` 时，循环中断，允许您有效地控制应用程序流程。

4. 创建 Translator 实例。

   ```python
         translator = Translator()
   ```

   这创建了 Translator 类的实例，用于执行翻译。

5. 翻译文本。

   ```python
         translated_text = translator.translate(input_text, dest='fr').text
   ```

   这里使用用户输入调用 `translator.translate` 方法。`dest='fr'` 参数指定翻译的目标语言是法语。`.text` 属性获取翻译后的字符串。有关可用语言代码的更多详细信息，请参阅 [Googletrans 文档](https://py-googletrans.readthedocs.io/en/latest/)。

6. 打印原始文本和翻译后的文本。

   ```python
         print(f"Original Text: {input_text}")
         print(f"Translated Text: {translated_text}")
   ```

   这两行打印用户输入的原始文本和翻译后的文本。

7. 创建 `requirements.txt`。示例应用程序已包含 `requirements.txt` 文件，用于指定应用程序导入的必要模块。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

   ```text
   ...

   # 05 language_translation
   googletrans==4.0.0-rc1
   ```

   语言翻译应用程序只需要 `googletrans`。

## 探索应用程序环境

您将使用 Docker 在容器中运行应用程序。Docker 允许您容器化应用程序，为运行它提供一致且隔离的环境。这意味着无论底层系统差异如何，应用程序都将在其 Docker 容器中按预期运行。

要在容器中运行应用程序，需要一个 Dockerfile。Dockerfile 是一个文本文档，包含您在命令行上调用以组装镜像的所有命令。镜像是一个只读模板，包含创建 Docker 容器的说明。

示例应用程序已包含 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释了 `Dockerfile` 的每个部分。有关更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令为构建奠定基础。`python:3.8-slim` 是 Python 3.8 镜像的轻量级版本，针对大小和速度进行了优化。使用这个精简镜像可以减少 Docker 镜像的整体大小，从而加快下载速度并减少安全漏洞的攻击面。这对于基于 Python 的应用程序特别有用，因为您可能不需要完整的标准 Python 镜像。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 设置 Docker 镜像中的当前工作目录。通过将其设置为 `/app`，您可以确保 Dockerfile 中的所有后续命令（如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于组织您的 Docker 镜像，因为所有与应用程序相关的文件都包含在特定目录中。

3. 将 requirements 文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从本地机器传输到 Docker 镜像中。此文件列出了应用程序所需的所有 Python 依赖项。将其复制到容器中允许下一个命令（`RUN pip install`）在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减小 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤特定于需要 spaCy 库的 NLP 应用程序。它下载 `en_core_web_sm` 模型，这是一个用于 spaCy 的小型英语语言模型。虽然此应用程序不需要它，但它被包含在内是为了与可能使用此 Dockerfile 的其他 NLP 应用程序兼容。

6. 将应用程序代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将您的 Python 脚本和 `entrypoint.sh` 脚本复制到镜像的 `/app` 目录中。这是至关重要的，因为容器需要这些脚本来运行应用程序。`entrypoint.sh` 脚本特别重要，因为它决定了应用程序如何在容器内启动。

7. 为 `entrypoint.sh` 脚本设置权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 的文件权限，使其可执行。此步骤是必要的，以确保 Docker 容器可以运行此脚本来启动应用程序。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令将容器配置为将 `entrypoint.sh` 作为其默认可执行文件运行。这意味着当容器启动时，它会自动执行该脚本。

   您可以通过在代码或文本编辑器中打开 `entrypoint.sh` 脚本来探索它。由于示例包含多个应用程序，该脚本允许您在容器启动时指定要运行的应用程序。

## 运行应用程序

要使用 Docker 运行应用程序：

1. 构建镜像。

   在终端中，在 `Dockerfile` 所在目录内运行以下命令。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是命令的分解：

   - `docker build`：这是用于从 Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志代表标签。它为镜像分配一个名称，在本例中为 `basic-nlp`。标签是稍后引用镜像的便捷方式，特别是在将它们推送到注册表或运行容器时。
   - `.`：这是命令的最后部分，指定构建上下文。句点（`.`）表示当前目录。Docker 将在此目录中查找 Dockerfile。构建上下文（在本例中为当前目录）被发送到 Docker 守护进程以启用构建。它包括指定目录中的所有文件和子目录。

   有关更多详细信息，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向控制台输出多个日志。您会看到它下载并安装依赖项。根据您的网络连接，这可能需要几分钟。Docker 确实有缓存功能，因此后续构建可以更快。完成后控制台将返回到提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 05_language_translation.py
   ```

   以下是命令的分解：

   - `docker run`：这是用于从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：即使未附加也保持标准输入（STDIN）打开。它允许容器在前台继续运行并保持交互。
     - `-t` 或 `--tty`：这分配一个伪 TTY，本质上是模拟一个终端，如命令提示符或 shell。这是让您与容器内应用程序交互的关键。
   - `basic-nlp`：这指定用于创建容器的 Docker 镜像的名称。在本例中，它是您使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `05_language_translation.py`：这是您要在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   有关更多详细信息，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   >
   > 对于 Windows 用户，运行容器时可能会遇到错误。验证 `entrypoint.sh` 中的行尾是 `LF`（`\n`）而不是 `CRLF`（`\r\n`），然后重新构建镜像。有关更多详细信息，请参阅[避免意外的语法错误，为容器中的文件使用 Unix 风格的行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers)。

   容器启动后，您将在控制台中看到以下内容。

   ```console
   Enter the text for translation (type 'exit' to end):
   ```

3. 测试应用程序。

   输入一些文本以获取文本摘要。

   ```console
   Enter the text for translation (type 'exit' to end): Hello, how are you doing?
   Original Text: Hello, how are you doing?
   Translated Text: Bonjour comment allez-vous?
   ```

## 总结

在本指南中，您学习了如何构建和运行语言翻译应用程序。您学习了如何使用 Python 和 Googletrans 构建应用程序，然后使用 Docker 设置环境并运行应用程序。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Googletrans](https://github.com/ssut/py-googletrans)
- [Python 文档](https://docs.python.org/3/)

## 后续步骤

探索更多[自然语言处理指南](./_index.md)。
