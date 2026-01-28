---
title: Docker 研讨会之后的下一步
weight: 100
linkTitle: "第九部分：下一步"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop, 入门, 设置, 概览, 快速入门, 简介, 概念, 容器
description: 确保您对接下来可以使用应用程序做什么有更多想法
aliases:
 - /get-started/11_what_next/
 - /guides/workshop/10_what_next/
---

虽然您已经完成了研讨会，但关于容器还有很多东西需要学习。

以下是接下来要关注的其他几个领域。

## 容器编排

在生产环境中运行容器很困难。您不想登录机器并简单地运行 `docker run` 或 `docker compose up`。为什么不呢？好吧，如果容器挂了怎么办？如何在多台机器上进行扩展？容器编排解决了这个问题。Kubernetes、Swarm、Nomad 和 ECS 等工具都有助于解决这个问题，尽管方式略有不同。

一般的想法是，您有接收预期状态的管理器。此状态可能是“我想运行我的 Web 应用程序的两个实例并公开端口 80”。然后，管理器查看集群中的所有机器并将工作委派给工作节点。管理器监视更改（例如容器退出），然后努力使实际状态反映预期状态。

## 云原生计算基金会项目

CNCF 是各种开源项目的供应商中立之家，包括 Kubernetes、Prometheus、Envoy、Linkerd、NATS 等。您可以查看[此处的毕业和孵化项目](https://www.cncf.io/projects/)以及整个 [CNCF Landscape](https://landscape.cncf.io/)。有很多项目可以帮助解决有关监控、日志记录、安全性、镜像注册表、消息传递等方面的问题。

## 入门视频研讨会

Docker 建议观看 DockerCon 2022 的视频研讨会。观看整个视频或使用以下链接打开视频的特定部分。

* [Docker 概览和安装](https://youtu.be/gAGEar5HQoU)
* [拉取、运行和探索容器](https://youtu.be/gAGEar5HQoU?t=1400)
* [构建容器镜像](https://youtu.be/gAGEar5HQoU?t=3185)
* [容器化应用程序](https://youtu.be/gAGEar5HQoU?t=4683)
* [连接数据库并设置绑定挂载](https://youtu.be/gAGEar5HQoU?t=6305)
* [将容器部署到云端](https://youtu.be/gAGEar5HQoU?t=8280)

<iframe src="https://www.youtube-nocookie.com/embed/gAGEar5HQoU" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 从头开始创建容器

如果您想了解容器是如何从头开始构建的，来自 Aqua Security 的 Liz Rice 做了一个精彩的演讲，其中她用 Go 从头开始创建了一个容器。虽然这次演讲没有深入探讨网络、使用镜像作为文件系统以及其他高级主题，但它深入探讨了事情是如何工作的。

<iframe src="https://www.youtube-nocookie.com/embed/8fi7uSYlOdc" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>