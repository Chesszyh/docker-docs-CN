--- 
title: 构建文本识别应用
linkTitle: 文本分类
keywords: nlp, natural language processing, sentiment analysis, python, nltk, scikit-learn, text classification
description: 了解如何使用 Python、NLTK、scikit-learn 和 Docker 构建和运行文本识别应用程序。
summary: |
  本指南详细介绍了如何使用 Docker 容器化文本分类模型。
tags: [ai]
languages: [python]
alias:
  - /guides/use-case/nlp/text-classification/
params:
  time: 20 minutes
---

## 概览

在本指南中，你将学习如何创建并运行一个文本识别应用程序。你将使用 Python 以及 scikit-learn 和自然语言工具包 (NLTK) 来构建该应用程序。然后，你将使用 Docker 设置环境并运行该应用程序。

该应用程序使用 NLTK 的 SentimentIntensityAnalyzer 分析用户输入文本的情感。它允许用户输入文本，然后对文本进行处理以确定其情感，将其分类为积极或消极。此外，它还会根据预定义的数据集显示其情感分析模型的准确性和详细的分类报告。

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

文本分类应用程序的源代码位于 `Docker-NLP/03_text_classification.py` 文件中。在文本或代码编辑器中打开 `03_text_classification.py`，按照以下步骤探索其内容。

1. 导入所需的库。

   ```python
   import nltk
   from nltk.sentiment import SentimentIntensityAnalyzer
   from sklearn.metrics import accuracy_score, classification_report
   from sklearn.model_selection import train_test_split
   import ssl
   ```

   - `nltk`：一个流行的用于自然语言处理 (NLP) 的 Python 库。
   - `SentimentIntensityAnalyzer`：`nltk` 的一个组件，用于情感分析。
   - `accuracy_score`, `classification_report`：来自 scikit-learn 的函数，用于评估模型。
   - `train_test_split`：来自 scikit-learn 的函数，用于将数据集拆分为训练集和测试集。
   - `ssl`：用于处理下载 `nltk` 数据时可能出现的 SSL 证书问题。

2. 处理 SSL 证书验证。

   ```python
   try:
       _create_unverified_https_context = ssl._create_unverified_https_context
   except AttributeError:
       pass
   else:
       ssl._create_default_https_context = _create_unverified_https_context
   ```

   此代码块是针对某些环境的解决方法，在这些环境中，通过 NLTK 下载数据可能会因 SSL 证书验证问题而失败。它告诉 Python 在 HTTPS 请求中忽略 SSL 证书验证。

3. 下载 NLTK 资源。

   ```python
   nltk.download('vader_lexicon')
   ```

   `vader_lexicon` 是 `SentimentIntensityAnalyzer` 用于情感分析的词典。

4. 定义测试文本和相应的标签。

   ```python
   texts = [...] 
   labels = [0, 1, 2, 0, 1, 2]
   ```

   本节定义了一个包含文本及其相应标签的小型数据集（0 代表积极，1 代表消极，2 代表垃圾邮件）。

5. 拆分测试数据。

   ```python
   X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
   ```

   这部分将数据集拆分为训练集和测试集，其中 20% 的数据作为测试集。由于此应用程序使用预训练模型，因此它不会训练模型。

6. 设置情感分析。

   ```python
   sia = SentimentIntensityAnalyzer()
   ```

   此代码初始化 `SentimentIntensityAnalyzer` 以分析文本的情感。

7. 生成测试数据的预测和分类。

   ```python
   vader_predictions = [sia.polarity_scores(text)("compound") for text in X_test]
   threshold = 0.2
   vader_classifications = [0 if score > threshold else 1 for score in vader_predictions]
   ```

   这部分为测试集中的每个文本生成情感分数，并根据阈值将其分类为积极或消极。

8. 评估模型。

   ```python
   accuracy = accuracy_score(y_test, vader_classifications)
   report_vader = classification_report(y_test, vader_classifications, zero_division='warn')
   ```

   这部分计算预测的准确率和分类报告。

9. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   这个 Python 习语确保只有当此脚本作为主程序运行时才会运行以下代码块。它提供了灵活性，允许脚本既可以作为独立程序运行，也可以作为模块导入。

10. 创建无限循环以进行连续输入。

    ```python
       while True:
        input_text = input("Enter the text for classification (type 'exit' to end): ")

          if input_text.lower() == 'exit':
             print("Exiting...")
             break
    ```

    这个 while 循环无限期运行，直到被显式中断。它允许用户连续输入文本进行实体识别，直到他们决定退出。

11. 分析文本。

    ```python
            input_text_score = sia.polarity_scores(input_text)("compound")
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

13. 创建 `requirements.txt`。示例应用程序已包含 `requirements.txt` 文件，用于指定应用程序导入的必要包。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

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

   有关更多详细信息，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向控制台输出多个日志。你会看到它下载并安装依赖项。根据你的网络连接，这可能需要几分钟。Docker 具有缓存功能，因此后续构建可能会更快。完成后，控制台将返回提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 03_text_classification.py
   ```

   以下是命令的细分：

   - `docker run`：这是用于从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：即使未附加，这也保持标准输入 (STDIN) 打开。它允许容器在前台保持运行并具有交互性。
     - `-t` or `--tty`：这分配一个伪 TTY，本质上是模拟终端，如命令提示符或 shell。它是让你与容器内的应用程序进行交互的原因。
   - `basic-nlp`：这指定用于创建容器的 Docker 镜像的名称。在这种情况下，它是你使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `03_text_classification.py`：这是你要在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   有关更多详细信息，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   > 
   > 对于 Windows 用户，运行容器时可能会遇到错误。验证 `entrypoint.sh` 中的行尾是 `LF` (`\n`) 而不是 `CRLF` (`\r\n`)，然后重建镜像。有关更多详细信息，请参阅 [避免意外的语法错误，对容器中的文件使用 Unix 风格的行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers)。

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

在本指南中，你学习了如何构建和运行文本分类应用程序。你学习了如何使用 Python 以及 scikit-learn 和 NLTK 构建应用程序。然后，你学习了如何使用 Docker 设置环境并运行应用程序。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Natural Language Toolkit](https://www.nltk.org/)
- [Python 文档](https://docs.python.org/3/)
- [scikit-learn](https://scikit-learn.org/)

## 后续步骤

探索更多 [自然语言处理指南](./_index.md)。
