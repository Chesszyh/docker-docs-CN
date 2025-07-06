---
title: 构建文本识别应用程序
linkTitle: 文本分类
keywords: nlp, 自然语言处理, 情感分析, python, nltk, scikit-learn, 文本分类
description: 了解如何使用 Python、NLTK、scikit-learn 和 Docker 构建和运行文本识别应用程序。
summary: |
  本指南详细介绍了如何使用 Docker 对文本分类模型进行容器化。
tags: [ai]
languages: [python]
aliases:
  - /guides/use-case/nlp/text-classification/
params:
  time: 20 分钟
---

## 概述

在本指南中，你将学习如何创建和运行文本识别应用程序。你将使用 Python、scikit-learn 和自然语言工具包 (NLTK) 构建该应用程序。然后，你将使用 Docker 设置环境并运行该应用程序。

该应用程序使用 NLTK 的 SentimentIntensityAnalyzer 分析用户输入文本的情感。它允许用户输入文本，然后处理该文本以确定其情感，将其分类为积极或消极。此外，它还根据预定义的数据集显示其情感分析模型的准确性和详细的分类报告。

## 先决条件

- 你已经安装了最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 会定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 你有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 获取示例应用程序

1. 打开终端，并使用以下命令克隆示例应用程序的存储库。

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. 验证你是否已克隆该存储库。

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

文本分类应用程序的源代码位于 `Docker-NLP/03_text_classification.py` 文件中。在文本或代码编辑器中打开 `03_text_classification.py` 以在以下步骤中探索其内容。

1. 导入所需的库。

   ```python
   import nltk
   from nltk.sentiment import SentimentIntensityAnalyzer
   from sklearn.metrics import accuracy_score, classification_report
   from sklearn.model_selection import train_test_split
   import ssl
   ```

   - `nltk`：一个流行的用于自然语言处理 (NLP) 的 Python 库。
   - `SentimentIntensityAnalyzer`：`nltk` 中用于情感分析的组件。
   - `accuracy_score`、`classification_report`：来自 scikit-learn 的用于评估模型的函数。
   - `train_test_split`：来自 scikit-learn 的用于将数据集拆分为训练集和测试集的函数。
   - `ssl`：用于处理在为 `nltk` 下载数据时可能发生的 SSL 证书问题。

2. 处理 SSL 证书验证。

   ```python
   try:
       _create_unverified_https_context = ssl._create_unverified_context
   except AttributeError:
       pass
   else:
       ssl._create_default_https_context = _create_unverified_https_context
   ```

   此代码块是针对某些环境中通过 NLTK 下载数据可能因 SSL 证书验证问题而失败的变通方法。它告诉 Python 忽略 HTTPS 请求的 SSL 证书验证。

3. 下载 NLTK 资源。

   ```python
   nltk.download('vader_lexicon')
   ```

   `vader_lexicon` 是 `SentimentIntensityAnalyzer` 用于情感分析的词典。

4. 定义用于测试的文本和相应的标签。

   ```python
   texts = [...]
   labels = [0, 1, 2, 0, 1, 2]
   ```

   本节定义了一个小的数据集，其中包含文本及其相应的标签（0 表示积极，1 表示消极，2 表示垃圾邮件）。

5. 拆分测试数据。

   ```python
   X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
   ```

   此部分将数据集拆分为训练集和测试集，其中 20% 的数据作为测试集。由于此应用程序使用预训练模型，因此它不会训练模型。

6. 设置情感分析。

   ```python
   sia = SentimentIntensityAnalyzer()
   ```

   此代码初始化 `SentimentIntensityAnalyzer` 以分析文本的情感。

7. 为测试数据生成预测和分类。

   ```python
   vader_predictions = [sia.polarity_scores(text)["compound"] for text in X_test]
   threshold = 0.2
   vader_classifications = [0 if score > threshold else 1 for score in vader_predictions]
   ```

   此部分为测试集中的每个文本生成情感分数，并根据阈值将其分类为积极或消极。

8. 评估模型。

   ```python
   accuracy = accuracy_score(y_test, vader_classifications)
   report_vader = classification_report(y_test, vader_classifications, zero_division='warn')
   ```

   此部分计算预测的准确性和分类报告。

9. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   这个 Python 惯用法确保以下代码块仅在此脚本是主程序时运行。它提供了灵活性，允许脚本既可以作为独立程序运行，也可以作为导入的模块运行。

10. 创建一个无限循环以进行连续输入。

    ```python
       while True:
        input_text = input("Enter the text for classification (type 'exit' to end): ")

          if input_text.lower() == 'exit':
             print("Exiting...")
             break
    ```

    这个 while 循环无限期运行，直到被明确中断。它允许用户连续输入文本进行实体识别，直到他们决定退出。

11. 分析文本。

    ```python
            input_text_score = sia.polarity_scores(input_text)["compound"]
            input_text_classification = 0 if input_text_score > threshold else 1
    ```

12. 打印 VADER 分类报告和情感分析。

    ```python
            print(f"Accuracy: {accuracy:.2f}")
            print("\nVADER Classification Report:")
            print(report_vader)

            print(f"\nTest Text (Positive): '{input_text}'")
            print(f"Predicted Sentiment: {'Positive' if input_text_classification == 0 else 'Negative'}")
    ```

13. 创建 `requirements.txt`。示例应用程序已包含 `requirements.txt` 文件，以指定应用程序导入的必要包。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

    ```text
    # 01 sentiment_analysis
    nltk==3.6.5

    ...

    # 03 text_classification
    scikit-learn==1.3.2

    ...
    ```

    文本分类应用程序需要 `nltk` 和 `scikit-learn` 模块。

## 探索应用程序环境

你将使用 Docker 在容器中运行该应用程序。Docker 允许你对应用程序进行容器化，从而为运行它提供一个一致且隔离的环境。这意味着无论底层系统有何差异，该应用程序都将在其 Docker 容器中按预期运行。

要在容器中运行该应用程序，需要一个 Dockerfile。Dockerfile 是一个文本文档，其中包含你在命令行上为组装镜像而调用的所有命令。镜像是具有创建 Docker 容器的说明的只读模板。

示例应用程序已包含一个 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释了 `Dockerfile` 的每个部分。有关更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令为构建奠定了基础。`python:3.8-slim` 是 Python 3.8 镜像的轻量级版本，针对大小和速度进行了优化。使用此精简镜像可以减小 Docker 镜像的整体大小，从而加快下载速度并减少安全漏洞的表面积。这对于基于 Python 的应用程序尤其有用，因为你可能不需要完整的标准 Python 镜像。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 设置 Docker 镜像中的当前工作目录。通过将其设置为 `/app`，你可以确保 Dockerfile 中的所有后续命令（如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于组织你的 Docker 镜像，因为所有与应用程序相关的文件都包含在一个特定的目录中。

3. 将需求文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从你的本地计算机传输到 Docker 镜像中。此文件列出了应用程序所需的所有 Python 依赖项。将其复制到容器中可以让下一个命令 (`RUN pip install`) 在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）来安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减小 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤特定于需要 spaCy 库的 NLP 应用程序。它下载 `en_core_web_sm` 模型，这是一个用于 spaCy 的小型英语语言模型。虽然此应用程序不需要它，但为了与可能使用此 Dockerfile 的其他 NLP 应用程序兼容，它被包含在内。

6. 将应用程序代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将你的 Python 脚本和 `entrypoint.sh` 脚本复制到镜像的 `/app` 目录中。这至关重要，因为容器需要这些脚本来运行应用程序。`entrypoint.sh` 脚本尤其重要，因为它规定了应用程序在容器内如何启动。

7. 为 `entrypoint.sh` 脚本设置权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 的文件权限，使其可执行。此步骤是必要的，以确保 Docker 容器可以运行此脚本来启动应用程序。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令将容器配置为运行 `entrypoint.sh` 作为其默认可执行文件。这意味着当容器启动时，它会自动执行该脚本。

   你可以通过在代码或文本编辑器中打开 `entrypoint.sh` 脚本来探索它。由于示例包含多个应用程序，因此该脚本允许你在容器启动时指定要运行的应用程序。

## 运行应用程序

要使用 Docker 运行该应用程序：

1. 构建镜像。

   在终端中，在 `Dockerfile` 所在的目录中运行以下命令。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是该命令的分解：

   - `docker build`：这是用于从 Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是位于指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志代表标记。它为镜像分配一个名称，在本例中为 `basic-nlp`。标记是以后引用镜像的便捷方式，尤其是在将它们推送到注册表或运行容器时。
   - `.`：这是命令的最后一部分，指定了构建上下文。句点 (`.`) 表示当前目录。Docker 将在此目录中查找 Dockerfile。构建上下文（在本例中为当前目录）将发送到 Docker 守护进程以启用构建。它包括指定目录中的所有文件和子目录。

   有关更多详细信息，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向你的控制台输出多个日志。你会看到它下载并安装依赖项。根据你的网络连接情况，这可能需要几分钟时间。Docker 确实具有缓存功能，因此后续构建可以更快。完成后，控制台将返回到提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 03_text_classification.py
   ```

   以下是该命令的分解：

   - `docker run`：这是用于从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：即使未附加，此选项也会保持标准输入 (STDIN) 打开。它允许容器在前台保持运行并具有交互性。
     - `-t` 或 `--tty`：此选项分配一个伪 TTY，实质上是模拟一个终端，如命令提示符或 shell。它允许你与容器内的应用程序进行交互。
   - `basic-nlp`：这指定了用于创建容器的 Docker 镜像的名称。在本例中，它是你使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `03_text_classification.py`：这是你想要在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   有关更多详细信息，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   > 
   > 对于 Windows 用户，运行容器时可能会出现错误。请验证 `entrypoint.sh` 中的行尾是 `LF` (`\n`) 而不是 `CRLF` (`\r\n`)，然后重新构建镜像。有关更多详细信息，请参阅[避免意外的语法错误，为容器中的文件使用 Unix 式的行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line-endings-for-files-in-containers)。

   容器启动后，你将在控制台中看到以下内容。

   ```console
   Enter the text for classification (type 'exit' to end):
   ```

3. 测试应用程序。

   输入一些文本以获取文本分类。

   ```console
   Enter the text for classification (type 'exit' to end): I love containers!
   Accuracy: 1.00

   VADER Classification Report:
                 precision    recall  f1-score   support

              0       1.00      1.00      1.00         1
              1       1.00      1.00      1.00         1

       accuracy                           1.00         2
      macro avg       1.00      1.00      1.00         2
   weighted avg       1.00      1.00      1.00         2

   Test Text (Positive): 'I love containers!'
   Predicted Sentiment: Positive
   ```

## 总结

在本指南中，你学习了如何构建和运行文本分类应用程序。你学习了如何使用 Python、scikit-learn 和 NLTK 构建该应用程序。然后，你学习了如何使用 Docker 设置环境并运行该应用程序。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [自然语言工具包](https://www.nltk.org/)
- [Python 文档](https://docs.python.org/3/)
- [scikit-learn](https://scikit-learn.org/)

## 下一步

探索更多[自然语言处理指南](./_index.md)。
