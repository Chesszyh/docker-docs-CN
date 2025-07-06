---
title: Docker 研讨会之后该做什么
weight: 100
linkTitle: "第九部分：下一步"
keywords: '入门, 设置, 定向, 快速入门, 介绍, 概念, 容器, docker desktop'
description: 确保你对接下来可以用你的应用程序做什么有更多的想法
aliases:
 - /get-started/11_what_next/
 - /guides/workshop/10_what_next/
---

虽然你已经完成了研讨会，但关于容器还有很多东西需要学习。

以下是接下来可以关注的其他几个领域。

## 容器编排

在生产环境中运行容器是很困难的。你不想登录到一台机器上，然后简单地运行 `docker run` 或 `docker compose up`。为什么不呢？嗯，如果容器死掉了怎么办？你如何在多台机器上进行扩展？容器编排解决了这个问题。像 Kubernetes、Swarm、Nomad 和 ECS 这样的工具都以略有不同的方式帮助解决了这个问题。

总体的想法是，你有一些管理者，他们接收预期的状态。这个状态可能是“我想要运行我的 Web 应用程序的两个实例并暴露 80 端口”。然后，管理者会查看集群中的所有机器，并将工作委托给工作节点。管理者会监视变化（例如容器退出），然后努力使实际状���反映预期状态。

## 云原生计算基金会项目

CNCF 是各种开源项目的中立之家，包括 Kubernetes、Prometheus、Envoy、Linkerd、NATS 等。你可以在[这里查看已毕业和正在孵化的项目](https://www.cncf.io/projects/)，并在[这里查看整个 CNCF 全景图](https://landscape.cncf.io/)。有很多项目可以帮助解决监控、日志记录、安全性、镜像仓库、消息传递等方面的问题。

## 入门视频研讨会

Docker 建议观看 DockerCon 2022 的视频研讨会。观看整个视频或使用以下链接在特定部分打开视频。

* [Docker 概述和安装](https://youtu.be/gAGEar5HQoU)
* [拉取、运行和探索容器](https://youtu.be/gAGEar5HQoU?t=1400)
* [构建容器镜像](https://youtu.be/gAGEar5HQoU?t=3185)
* [容器化应用程序](https://youtu.be/gAGEar5HQoU?t=4683)
* [连接数据库并设置绑定挂载](https://youtu.be/gAGEar5HQoU?t=6305)
* [将容器部署到云端](https://youtu.be/gAGEar5HQoU?t=8280)

<iframe src="https://www.youtube-nocookie.com/embed/gAGEar5HQoU" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 从头开始创建容器

如果你想了解容器是如何��头开始构建的，Aqua Security 的 Liz Rice 有一个很棒的演讲，她在其中用 Go 从头开始创建了一个容器。虽然演讲没有涉及网络、使用镜像作为文件系统以及其他高级主题，但它深入探讨了事情是如何运作的。

<iframe src="https://www.youtube-nocookie.com/embed/8fi7uSYlOdc" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
