---
description: 深入了解 Docker 平台，包括其用途、采用的架构及其底层技术。
keywords: docker 是什么, docker 守护进程, 为什么要使用 docker, docker 架构, docker 的用途, docker 客户端, docker 是做什么用的, 为什么选择 docker, docker 的用途, docker 容器是做什么用的, docker 容器是用来做什么的
title: Docker 是什么？
weight: 20
aliases:
 - /introduction/understanding-docker/
 - /engine/userguide/basics/
 - /engine/introduction/understanding-docker/
 - /engine/understanding-docker/
 - /engine/docker-overview/
 - /get-started/overview/
 - /guides/docker-overview/
---

Docker 是一个用于开发、发布和运行应用程序的开放平台。
Docker 使您能够将应用程序与基础设施分离，从而
快速交付软件。借助 Docker，您可以像管理应用程序一样管理基础设施
。通过利用 Docker 的
代码发布、测试和部署方法，您可以
显着减少编写代码和在生产环境中运行代码之间的延迟。

## Docker 平台

Docker 提供了在称为容器的松散隔离环境中打包和运行���用程序的能力
。隔离和安全性使您可以在给定主机上同时运行许多
容器。容器是轻量级的，包含
运行应用程序所需的一切，因此您无需依赖主机上安装的内容
。您可以在工作时共享容器，
并确保与您共享的每个人都获得以
相同方式工作的相同容器。

Docker 提供工具和平台来管理容器的生命周期：

* 使用容器开发您的应用程序及其支持组件。
* 容器成为分发和测试您的应用程序的单元。
* 准备就绪后，将您的应用程序部署到生产环境中，
  作为容器或编排服务。无论您的
  生产环境是本地数据中心、云提供商还是两者的混合体，其工作方式都相同
  。

## 我可以用 Docker 做什么？

### 快速、一致地交付您的应用程序

Docker 通过允许开发人员在
使用提供您的应用程序
和服务的本地容器的标准化环境中使用本地容器来简化开发生命周期。容器非常适合持续集成和持续
交付 (CI/CD) 工作流程。

请考虑以下示例场景：

- 您的开发人员在本地编写代码，并使用 Docker 容器与同事
  共享他们的工作。
- 他们使用 Docker 将其应用程序推送到测试环境中，并运行
  自动化和手动测试。
- 当开发人员发现错误时，他们可以在开发环境中修复它们
  ，然后将其重新部署到测试环境中进行测试和验证。
- 测试完成后，将修复程序提供给客户就像
  将更新后的映像推送到生产环境一样简单。

### 响应式部署和扩展

Docker 基于容器的平台允许高度可移植的工作负载。Docker
容器可以在开发人员的本地笔记本电脑、数据中心的物理机或虚拟机
、云提供商或混合环境中运行。

Docker 的可移植性和轻量级特性还使其易于动态
管理工作负载，根据
业务需求近乎实时地扩展或拆除应用程序和服务。

### 在相同的硬件上运行更多的工作负载

Docker 轻巧快速。它为基于虚拟机监控程序的虚拟机提供了一种可行、经济高效的替代方案
，因此您可以使用更多的服务器
容量来实现您的业务目标。Docker 非常适合高密度
环境以及需要用
更少资源完成更多工作的中小型部署。

## Docker 架构

Docker 使用客户端-服务器架构。Docker 客户端与
Docker 守护进程通信，后者负责构建、运行和
分发 Docker 容器的繁重工作。Docker 客户端和守护进程可以
在同一系统上运行，或者您可以将 Docker 客户端连接到远程 Docker
守护进程。Docker 客户端和守护进程使用 REST API、UNIX
套接字或网络接口进行通信。另一个 Docker 客户端是 Docker Compose，
它允许您使用由一组容器组成的应用程序。

![Docker 架构图](images/docker-architecture.webp)

### Docker 守护进程

Docker 守护进程 (`dockerd`) 侦听 Docker API 请求并管理 Docker
对象，例如映像、容器、网络和卷。守护进程还可以
与其他守护进程通信以管理 Docker 服务。

### Docker 客户端

Docker 客户端 (`docker`) 是许多 Docker 用户与
Docker 交互的主要方式。当您使用诸如 `docker run` 之类的命令时，客户端会将这些
命令发送到 `dockerd`，后者会执行它们。`docker` 命令使用
Docker API。Docker 客户端可以与多个守护进程通信。

### Docker Desktop

Docker Desktop 是一款易于安装的应用程序，适用于您的 Mac、Windows 或 Linux 环境，使您能够构建和共享容器化应用程序和微服务。Docker Desktop 包括 Docker 守护进程 (`dockerd`)、Docker 客户端 (`docker`)、Docker Compose、Docker Content Trust、Kubernetes 和 Credential Helper。有关更多信息，请参阅 [Docker Desktop](/manuals/desktop/_index.md)。

### Docker 注册表

Docker 注册表存储 Docker 映像。Docker Hub 是一个任何人都可以使用的公共
注册表，Docker 默认在
Docker Hub 上查找映像。您甚��可以运行自己的私有注册表。

当您使用 `docker pull` 或 `docker run` 命令时，Docker 会从您配置的注册表中提取所需的映像。当您使用 `docker push` 命令时，Docker 会将
您的映像推送到您配置的注册表中。

### Docker 对象

当您使用 Docker 时，您正在创建和使用映像、容器、网络、
卷、插件和其他对象。本节简要概述了其中一些
对象。

#### 映像

映像是一个只读模板，其中包含有关创建 Docker
容器的说明。通常，一个映像基于另一个映像，并进行了一些额外的
自定义。例如，您可以构建一个基于 `ubuntu`
映像的映像，但安装 Apache Web 服务器和您的应用程序，以及
使您的应用程序运行所需的配置详细信息。

您可以创建自己的映像，也可以只使用其他人
创建并发布在注册表中的映像。要构建自己的映像，您需要创建一个具有
简单语法的 Dockerfile，用于定义创建映像和运行它所需的步骤
。Dockerfile 中的每条指令都会在映像中创建一个层。当您
更改 Dockerfile 并重新构建映像时，只有那些已
更改的层才会被重新构建。与其他虚拟化技术相比，这是使映像如此轻量、小巧
和快速的部分原因。

#### 容器

容器是映像的可运行实例。您可以使用 Docker API 或 CLI 创建、启动、停止、
移动或删除容器。您可以将容器连接到一个或多个网络，为其附加存储
，甚至可以根据其当前状态创建新映像。

默认情况下，容器与其他容器和
其主机相对隔离。您可以控制容器的网络、存储
或其他底层子系统与其他容器或主机
的隔离程度。

容器由其映像以及您在创建或启动它时
提供给它的任何配置选项定义。当容器被移除时，其状态的任何未
存储在持久存储中的更改都会消失。

##### `docker run` 命令示例

以下命令运行一个 `ubuntu` 容器，以交互方式附加到您的
本地命令行会话，并运行 `/bin/bash`。

```console
$ docker run -i -t ubuntu /bin/bash
```

当您运行此命令时，会发生以下情况（假设您使用的是
默认注册表配置）：

1.  如果您本地没有 `ubuntu` 映像，Docker 会从您
    配置的注册表中提取它，就像您手动运行 `docker pull ubuntu` 一样。

2.  Docker 创建一个新容器，就像您手动运行 `docker container create`
    命令一样。

3.  Docker 为容器分配一个读写文件系统，作为其最终
    层。这允许正在运行的容器在其本地文件系统中创建或修改文件和
    目录。

4.  Docker 创���一个网络接口以将容器连接到默认
    网络，因为您没有指定任何网络选项。这包括
    为容器分配 IP 地址。默认情况下，容器可以
    使用主机的网络连接连接到外部网络。

5.  Docker 启动容器并执行 `/bin/bash`。因为容器
    正在以交互方式运行并附加到您的终端（由于 `-i` 和 `-t`
    标志），您可以使用键盘提供输入，而 Docker 会将输出记录到
    您的终端。

6.  当您运行 `exit` 终止 `/bin/bash` 命令时，容器
    会停止但不会被移除。您可以再次启动它或将其移除。

## 底层技术

Docker 是用 [Go 编程语言](https://golang.org/) 编写的，并利用
Linux 内核的几个特性来提供其功能。
Docker 使用一种称为 `namespaces` 的技术来提供称为
容器的隔离工作区。当您运行容器时，Docker 会为该容器创建一组
命名空间。

这些命名空间提供了一层隔离。容器的每个方面都在
一个单独的命名空间中运行，其访问权限仅限于该命名空间。

## 后续步骤

- [安装 Docker](/get-started/get-docker.md)
- [开始使用 Docker](/get-started/introduction/_index.md)