---
description: 使用 Kafka 和 Docker 开发事件驱动应用程序
keywords: kafka, container-supported development
title: 使用 Kafka 和 Docker 开发事件驱动应用程序
linktitle: 使用 Kafka 的事件驱动应用
summary: |
  本指南介绍如何在 Docker 容器中运行 Apache Kafka。
tags: [distributed-systems]
languages: [js]
aliases:
  - /guides/use-case/kafka/
params:
  time: 20 minutes
---

随着微服务的兴起，事件驱动架构变得越来越流行。[Apache Kafka](https://kafka.apache.org/) 是一个分布式事件流平台，通常是这些架构的核心。不幸的是，为开发设置和部署自己的 Kafka 实例通常很棘手。幸运的是，Docker 和容器使这变得更加容易。

在本指南中，您将学习如何：

1. 使用 Docker 启动 Kafka 集群
2. 将非容器化应用连接到集群
3. 将容器化应用连接到集群
4. 部署 Kafka-UI 以帮助故障排除和调试

## 前提条件

按照本操作指南需要以下前提条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager) 和 [yarn](https://yarnpkg.com/)
- Kafka 和 Docker 的基础知识

## 启动 Kafka

从 [Kafka 3.3](https://www.confluent.io/blog/apache-kafka-3-3-0-new-features-and-updates/) 开始，由于 KRaft（Kafka Raft）不再需要 Zookeeper，Kafka 的部署大大简化。使用 KRaft，为本地开发设置 Kafka 实例变得更加容易。从 [Kafka 3.8](https://www.confluent.io/blog/introducing-apache-kafka-3-8/) 发布开始，现在可以使用新的 [kafka-native](https://hub.docker.com/r/apache/kafka-native) Docker 镜像，它提供了显著更快的启动速度和更低的内存占用。

> [!TIP]
>
> 本指南将使用 apache/kafka 镜像，因为它包含许多用于管理和使用 Kafka 的有用脚本。但是，您可能希望使用 apache/kafka-native 镜像，因为它启动更快且需要更少的资源。

### 启动 Kafka

通过以下步骤启动基本的 Kafka 集群。此示例将启动一个集群，将端口 9092 暴露到主机，以便本机运行的应用程序可以连接到它。

1. 通过运行以下命令启动 Kafka 容器：

   ```console
   $ docker run -d --name=kafka -p 9092:9092 apache/kafka
   ```

2. 镜像拉取完成后，一两秒钟内您就会有一个运行中的 Kafka 实例。

3. apache/kafka 镜像在 `/opt/kafka/bin` 目录中附带了几个有用的脚本。运行以下命令验证集群是否正在运行并获取其集群 ID：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server :9092
   ```

   这样做会产生类似以下的输出：

   ```plaintext
   Cluster ID: 5L6g3nShT-eMCtK--X86sw
   ```

4. 通过运行以下命令创建示例主题并生产（或发布）一些消息：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
   ```

   运行后，您可以每行输入一条消息。例如，输入几条消息，每行一条。一些示例可能是：

   ```plaintext
   First message
   ```

   和

   ```plaintext
   Second message
   ```

   按 `enter` 发送最后一条消息，完成后按 ctrl+c。消息将被发布到 Kafka。

5. 通过消费消息确认消息已发布到集群：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server :9092 --topic demo --from-beginning
   ```

   然后您应该在输出中看到您的消息：

   ```plaintext
   First message
   Second message
   ```

   如果您愿意，可以打开另一个终端并发布更多消息，然后看到它们出现在消费者中。

   完成后，按 ctrl+c 停止消费消息。

您现在有了一个本地运行的 Kafka 集群，并验证了可以连接到它。

## 从非容器化应用连接到 Kafka

现在您已经展示了可以从命令行连接到 Kafka 实例，是时候从应用程序连接到集群了。在此示例中，您将使用一个使用 [KafkaJS](https://github.com/tulios/kafkajs) 库的简单 Node 项目。

由于集群在本地运行并在端口 9092 上暴露，应用程序可以通过 localhost:9092 连接到集群（因为它现在是本机运行而不是在容器中运行）。连接后，此示例应用程序将记录它从 `demo` 主题消费的消息。此外，当它在开发模式下运行时，如果找不到主题，它还会创建该主题。

1. 如果您没有从上一步运行 Kafka 集群，请运行以下命令启动 Kafka 实例：

   ```console
   $ docker run -d --name=kafka -p 9092:9092 apache/kafka
   ```

2. 在本地克隆 [GitHub 仓库](https://github.com/dockersamples/kafka-development-node)。

   ```console
   $ git clone https://github.com/dockersamples/kafka-development-node.git
   ```

3. 导航到项目中。

   ```console
   cd kafka-development-node/app
   ```

4. 使用 yarn 安装依赖项。

   ```console
   $ yarn install
   ```

5. 使用 `yarn dev` 启动应用程序。这将把 `NODE_ENV` 环境变量设置为 `development` 并使用 `nodemon` 监视文件更改。

   ```console
   $ yarn dev
   ```

6. 应用程序现在正在运行，它将把接收到的消息记录到控制台。在新终端中，使用以下命令发布几条消息：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
   ```

   然后向集群发送消息：

   ```plaintext
   Test message
   ```

   记住完成后按 `ctrl+c` 停止生产消息。

## 从容器和本机应用程序连接到 Kafka

现在您有了一个通过其暴露端口连接到 Kafka 的应用程序，是时候探索从另一个容器连接到 Kafka 需要哪些更改了。为此，您现在将从容器中运行应用程序而不是本机运行。

但在此之前，重要的是要了解 Kafka 监听器的工作原理以及这些监听器如何帮助客户端连接。

### 理解 Kafka 监听器

当客户端连接到 Kafka 集群时，它实际上连接到一个 "broker"。虽然 broker 有许多角色，但其中之一是支持客户端的负载均衡。当客户端连接时，broker 返回一组连接 URL，客户端随后应使用这些 URL 进行消息的生产或消费。这些连接 URL 是如何配置的？

每个 Kafka 实例都有一组监听器和公告监听器。"监听器" 是 Kafka 绑定的内容，"公告监听器" 配置客户端应如何连接到集群。客户端接收的连接 URL 基于客户端连接到的监听器。

### 定义监听器

为了帮助理解这一点，让我们看看如何配置 Kafka 以支持两种连接机会：

1. 主机连接（通过主机映射端口进入的连接）- 这些需要使用 localhost 连接
2. Docker 连接（来自 Docker 网络内部的连接）- 这些不能使用 localhost 连接，而是使用 Kafka 服务的网络别名（或 DNS 地址）

由于客户端需要两种不同的连接方法，因此需要两个不同的监听器 - `HOST` 和 `DOCKER`。`HOST` 监听器将告诉客户端使用 localhost:9092 连接，而 `DOCKER` 监听器将通知客户端使用 `kafka:9093` 连接。注意这意味着 Kafka 同时在端口 9092 和 9093 上监听。但是，只有主机监听器需要暴露给主机。

![显示 DOCKER 和 HOST 监听器以及它们如何暴露给主机和 Docker 网络的图表](./images/kafka-1.webp)

为了设置这一点，Kafka 的 `compose.yaml` 需要一些额外的配置。一旦您开始覆盖一些默认值，您还需要指定一些其他选项才能使 KRaft 模式工作。

```yaml
services:
  kafka:
    image: apache/kafka-native
    ports:
      - "9092:9092"
    environment:
      # 为 docker 和主机通信配置监听器
      KAFKA_LISTENERS: CONTROLLER://localhost:9091,HOST://0.0.0.0:9092,DOCKER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9092,DOCKER://kafka:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,DOCKER:PLAINTEXT,HOST:PLAINTEXT

      # KRaft 模式所需的设置
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9091

      # 用于 broker 间通信的监听器
      KAFKA_INTER_BROKER_LISTENER_NAME: DOCKER

      # 单节点集群所需
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

使用以下步骤尝试一下。

1. 如果您从上一步运行着 Node 应用程序，请在终端中按 `ctrl+c` 停止它。

2. 如果您从上一部分运行着 Kafka 集群，请使用以下命令停止该容器：

   ```console
   $ docker rm -f kafka
   ```

3. 通过在克隆项目目录的根目录运行以下命令启动 Compose 堆栈：

   ```console
   $ docker compose up
   ```

   片刻之后，应用程序将启动并运行。

4. 堆栈中还有另一个可用于发布消息的服务。通过访问 [http://localhost:3000](http://localhost:3000) 打开它。当您输入消息并提交表单时，您应该会看到应用程序接收消息的日志消息。

   这有助于演示容器化方法如何轻松添加额外的服务来帮助测试和排查应用程序。

## 添加集群可视化

一旦您开始在开发环境中使用容器，您就会意识到添加专注于帮助开发的额外服务（如可视化工具和其他支持服务）的便利性。由于您正在运行 Kafka，可视化 Kafka 集群中发生的事情可能会很有帮助。为此，您可以运行 [Kafbat UI Web 应用程序](https://github.com/kafbat/kafka-ui)。

要将其添加到您自己的项目中（它已经在演示应用程序中），您只需将以下配置添加到 Compose 文件：

```yaml
services:
  kafka-ui:
    image: kafbat/kafka-ui:main
    ports:
      - 8080:8080
    environment:
      DYNAMIC_CONFIG_ENABLED: "true"
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9093
    depends_on:
      - kafka
```

然后，一旦 Compose 堆栈启动，您可以在浏览器中打开 [http://localhost:8080](http://localhost:8080) 并导航以查看有关集群的其他详细信息、检查消费者、发布测试消息等。

## 使用 Kafka 进行测试

如果您有兴趣了解如何轻松地将 Kafka 集成到集成测试中，请查看[使用 Testcontainers 测试 Spring Boot Kafka 监听器指南](https://testcontainers.com/guides/testing-spring-boot-kafka-listener-using-testcontainers/)。本指南将教您如何使用 Testcontainers 管理测试中 Kafka 容器的生命周期。

## 结论

通过使用 Docker，您可以简化使用 Kafka 开发和测试事件驱动应用程序的过程。容器简化了设置和部署开发所需的各种服务的过程。一旦它们在 Compose 中定义，团队中的每个人都可以受益于这种易用性。

如果您之前错过了，所有示例应用程序代码都可以在 dockersamples/kafka-development-node 中找到。
