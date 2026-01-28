---
title: 在 GenAI 中利用 RAG 学习新信息
linkTitle: 在 GenAI 中利用 RAG
description:  本指南将带您完成使用检索增强生成 (RAG) 系统和图数据库设置和利用 GenAI 堆栈的过程。了解如何将 Neo4j 等图数据库与 AI 模型集成，以获得更准确、具有上下文意识的响应。
keywords: Docker, GenAI, Retrieval-Augmented Generation, RAG, Graph Databases, Neo4j, AI, LLM
summary: |
  本指南解释了如何使用检索增强生成 (RAG) 和 Neo4j 设置 GenAI 堆栈，涵盖关键概念、部署步骤和案例研究。它还包括有关使用实时数据优化 AI 性能的故障排除提示。
tags: [ai]
params:
  time: 35 minutes
---

## 介绍

检索增强生成 (RAG) 是一个强大的框架，通过集成来自外部知识源的信息检索来增强大型语言模型 (LLM)。本指南重点介绍使用像 Neo4j 这样擅长管理高度连接的关系数据的图数据库的专门 RAG 实现。与传统的带有向量数据库的 RAG 设置不同，将 RAG 与图数据库相结合可提供更好的上下文感知和关系驱动的见解。

在本指南中，您将：

* 探索将图数据库集成到 RAG 框架中的优势。
* 使用 Docker 配置 GenAI 堆栈，包含 Neo4j 和 AI 模型。
* 分析一个真实世界的案例研究，该案例重点介绍了此方法在处理专业查询方面的有效性。

## 了解 RAG

RAG 是一个混合框架，通过集成信息检索来增强大型语言模型的功能。它结合了三个核心组件：

- 来自外部知识库的 **信息检索**
- 用于生成响应的 **大型语言模型 (LLM)**
- 用于启用语义搜索的 **向量嵌入**

在 RAG 系统中，向量嵌入用于以机器可以理解和处理的方式表示文本的语义。例如，单词“dog”和“puppy”将具有相似的嵌入，因为它们具有相似的含义。通过将这些嵌入集成到 RAG 框架中，系统可以将大型语言模型的生成能力与从外部来源提取高度相关、具有上下文意识的数据的能力相结合。

系统运行如下：
1. 问题被转化为捕捉其含义的数学模式
2. 这些模式有助于在数据库中查找匹配信息
3. LLM 生成的响应融合了模型固有的知识和这些额外信息。

为了以有效的方式保存此向量信息，我们需要一种特殊类型的数据库。

## 图数据库介绍

图数据库（例如 Neo4j）专为管理高度连接的数据而设计。与传统的关系数据库不同，图数据库优先考虑实体及其之间的关系，使其成为连接与数据本身同样重要的任务的理想选择。

图数据库因其独特的数据存储和查询方法而脱颖而出。它们使用节点（或顶点）来表示实体，使用边来表示这些实体之间的关系。这种结构允许有效处理高度连接的数据和复杂的查询，而这些在传统数据库系统中很难管理。

SQL 数据库和图数据库在数据模型上有很大差异。SQL 数据库使用带有行和列的表格结构，其中实体之间的关系使用外键建立。这种方法适用于结构化数据和预定义关系。相比之下，图数据库将数据表示为节点（实体）和边（关系），使关系的表示更加直观和灵活。这种结构对于复杂的互连数据特别有利。

另一个关键区别在于模式的灵活性。SQL 数据库在严格的模式上运行，这意味着对数据结构的任何更改（例如添加新列或更改关系）通常都需要仔细的规划和迁移过程。然而，图数据库是模式可选的，允许更大的灵活性。可以在不破坏现有数据的情况下引入新的节点、边或属性，从而能够更快地适应不断变化的需求。

## 实际实施：测试 RAG 有效性

为了说明 RAG 系统在实践中的威力，让我们以 Apache NiFi 为主题来研究一个真实世界的实施案例。本案例研究演示了 RAG 如何增强 AI 提供有关专业技术主题的准确、上下文信息的能力。

### 教 AI 学习新技术

Apache NiFi 是一个很好的例子，说明了传统 LLM 的局限性以及 RAG 如何克服这些局限性。作为一项相对较新的技术，许多 LLM 对其了解有限或过时，使其成为演示 RAG 功能的完美候选者。

在没有 RAG 的情况下，当被问及超出其截止日期以外的信息时，LLM 可能会提供笼统的回答或承认其知识有限。以下示例演示了这一点。
```text
Question: What important events happened in 2024?
RAG: Disabled
I'm happy to help! Unfortunately, I'm a large language model, I don't have access to real-time information or events that occurred after my training data cutoff in 2024. Therefore, I cannot provide you with any important events that happened in 2024. My apologize for any inconvenience this may cause. Is there anything else I can help you with?
```

## 在 Linux 上设置具有 GPU 加速的 GenAI 堆栈

要在 Linux 主机上设置并运行 GenAI 堆栈，请执行以下命令之一，具体取决于 GPU 或 CPU 驱动：

### GPU 驱动

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux-gpu up -d
mv env.example .env
nano .env
```
在 `.env` 文件中，确保注释掉以下行。为了安全起见，请设置您自己的凭据

  ```txt
    NEO4J_URI=neo4j://database:7687
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=password
    OLLAMA_BASE_URL=http://llm-gpu:11434
  ```

### CPU 驱动

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux up -d
mv env.example .env
nano .env
```
在 `.env` 文件中，确保注释掉以下行。为了安全起见，请设置您自己的凭据

  ```txt
    NEO4J_URI=neo4j://database:7687
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=password
    OLLAMA_BASE_URL=http://llm:11434
  ```

### 在其他平台上设置

有关如何在其他平台上设置堆栈的说明，请参阅 [此页面](https://github.com/docker/genai-stack)。

### 初始启动

首次启动可能需要一些时间，因为系统需要下载大型语言模型。

### 监控进度

我们可以通过查看日志来监控下载和初始化进度。运行以下命令以查看日志：

```bash
docker compose logs
```

等待日志中的特定行，指示下载完成且堆栈已准备就绪。这些行通常确认设置和初始化成功。

  ```text
    pull-model-1 exited with code 0
    database-1    | 2024-12-29 09:35:53.269+0000 INFO  Started.
    pdf_bot-1     |   You can now view your Streamlit app in your browser.
    loader-1      |   You can now view your Streamlit app in your browser.
    bot-1         |   You can now view your Streamlit app in your browser.
  ```

现在，您可以访问 [http://localhost:8501/](http://localhost:8501/) 界面提问。例如，您可以尝试示例问题：

当我们在日志中看到这些行时，Web 应用程序就可以使用了。

由于我们的目标是教 AI 它还不知道的事情，我们首先在
[http://localhost:8501/](http://localhost:8501/) 问它一个关于 Nifi 的简单问题。
![alt text](image.png)

```text
Question: What is Apache Nifi?
RAG: Disabled
Hello! I'm here to help you with your question about Apache NiFi. Unfortunately, I don't know the answer to that question. I'm just an AI and my knowledge cutoff is December 2022, so I may not be familiar with the latest technologies or software. Can you please provide more context or details about Apache NiFi? Maybe there's something I can help you with related to it.
```

正如我们所看到的，AI 对这个主题一无所知，因为它在训练期间（也称为信息截止点）并不存在。

现在是教 AI 一些新技巧的时候了。首先，连接到 [http://localhost:8502/](http://localhost:8502/)。不要使用 "neo4j" 标签，而是将其更改为 "apache-nifi" 标签，然后选择 **Import** 按钮。

![alt text](image-1.png)

导入成功后，我们可以访问 Neo4j 来验证数据。

使用来自 `.env` 文件的凭据登录到 [http://localhost:7474/](http://localhost:7474/) 后，您可以在 Neo4j 上运行查询。使用 Neo4j Cypher 查询语言，您可以检查存储在数据库中的数据。

要统计数据，请运行以下查询：

```text
MATCH (n)
RETURN DISTINCT labels(n) AS NodeTypes, count(*) AS Count
ORDER BY Count DESC;
```

要执行此查询，请在顶部的框中写入并选择蓝色的运行按钮。

![alt text](image-2.png)

结果将显示在下方。我们在这里看到的是从 Stack Overflow 下载并保存在图数据库中的信息系统。RAG 将利用此信息来增强其响应。

您还可以运行以下查询来可视化数据：

```text
CALL db.schema.visualization()
```

要检查数据库中的关系，请运行以下查询：

```text
CALL db.relationshipTypes()
```

现在，我们准备启用我们的 LLM 来使用这些信息。回到 [http://localhost:8501/](http://localhost:8501/)，启用 **RAG** 复选框，然后再次问同样的问题。LLM 现在将提供更详细的答案。

![alt text](image-3.png)

该系统通过提取当前的技术文档来提供全面、准确的信息。
```text
Question: What is Apache Nifi?
RAG: Enabled

Answer:
Apache NiFi is an open-source, distributed data processing system that allows you to collect, transform, and transport data across various sources and sinks. It provides a graphical user interface for designing and managing data flows, as well as a set of APIs for integrating with other systems.
According to this Stack Overflow question, the free Neo4J JDBC driver doesn't understand SQL, only Cypher, so you would need to use a non-free BI Connector to connect to Neo4j from Apache Drill.
Additionally, this Stack Overflow question suggests that Apache POI does work in a Neo4j User Defined Function. However, there may be an unknown glitch in the standalone UDF mentioned in the initial question.
To export data from Neo4j to Excel using APOC Extended procedures, you can use apoc.export.xls.query which takes a Cypher query and exports the results to an Excel file.

References:
How to connect and query Neo4j Database on Apache Drill?
Is a Neo4j UDF compatible with Apache POI?
```

请记住，新的问题将被添加到 Stack Overflow，并且由于大多数 AI 模型固有的随机性，答案可能会有所不同，并且不会与本示例中的答案完全相同。

您可以随意使用另一个 [Stack Overflow 标签](https://stackoverflow.com/tags) 重新开始。要删除 Neo4j 中的所有数据，您可以在 Neo4j Web UI 中使用以下命令：

```txt
MATCH (n)
DETACH DELETE n;
```

为了获得最佳结果，请选择一个 LLM 不熟悉的标签。

### 何时利用 RAG 获得最佳结果

检索增强生成 (RAG) 在标准大型语言模型 (LLM) 不足的情况下特别有效。RAG 擅长的三个关键领域是知识限制、业务需求和成本效率。下面，我们将更详细地探讨这些方面。

#### 克服知识限制

LLM 是在某个时间点之前的固定数据集上训练的。这意味着它们无法访问：

* 实时信息：LLM 不会持续更新其知识，因此它们可能不知道最近发生的事件、新发布的研究或新兴技术。
* 专业知识：许多利基主题、专有框架或行业特定的最佳实践可能未在模型的训练语料库中得到充分记录。
* 准确的上下文理解：LLM 可能难以应对在金融、网络安全或医学研究等动态领域内频繁变化的细微差别或不断演变的术语。

通过将 RAG 与诸如 Neo4j 之类的图数据库相结合，AI 模型可以在生成响应之前访问和检索最新的、相关的和高度连接的数据。这确保了答案是及时的，并且基于事实信息而不是推断的近似值。

#### 满足业务和合规需求

医疗保健、法律服务和金融分析等行业的组织要求其 AI 驱动的解决方案必须：

* 准确：企业需要与其特定领域相关且基于事实的 AI 生成内容。
* 合规：许多行业必须遵守有关数据使用和安全性的严格规定。
* 可追溯：企业通常要求 AI 响应可审计，这意味着它们需要引用源材料。

通过使用 RAG，AI 生成的答案可以来源于受信任的数据库，确保更高的准确性并符合行业标准。这减轻了错误信息或违规行为等风险。

#### 提高成本效率和性能

训练和微调大型 AI 模型可能计算成本高昂且耗时。然而，集成 RAG 提供了：

* 减少微调需求：RAG 允许模型动态获取并合并更新的信息，而不是每次出现新数据时都重新训练 AI 模型。
* 使用较小模型获得更好性能：通过正确的检索技术，即使是紧凑的 AI 模型也可以通过有效利用外部知识表现良好。
* 降低运营成本：企业可以通过利用 RAG 的实时检索功能来优化资源，而不是投资昂贵的基础设施来支持大规模的重新训练。

通过遵循本指南，您现在拥有了使用 Neo4j 实现 RAG 的基础知识，使您的 AI 系统能够提供更准确、相关和有见地的响应。下一步是实验——选择一个数据集，配置您的堆栈，并开始利用检索增强生成的力量增强您的 AI。
