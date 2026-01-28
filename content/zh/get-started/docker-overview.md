---
description: 深入了解 Docker 平台的概述，包括其用途、架构及底层技术。
keywords: what is a docker, docker daemon, why use docker, docker architecture, what
  to use docker for, docker client, what is docker for, why docker, uses for docker,
  what is docker container used for, what are docker containers used for
title: 什么是 Docker？
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

Docker 是一个用于开发、交付和运行应用程序的开放平台。Docker 使您能够将应用程序与基础设施分离，从而实现软件的快速交付。借助 Docker，您可以像管理应用程序一样管理基础设施。通过利用 Docker 的代码交付、测试和部署方法论，您可以显著缩短从编写代码到在生产环境中运行代码之间的延迟。

## Docker 平台

Docker 提供了在称为容器（container）的松散隔离环境中打包和运行应用程序的能力。这种隔离性和安全性使您能够在给定主机上同时运行多个容器。容器是轻量级的，包含运行应用程序所需的一切，因此您无需依赖主机上已安装的内容。您可以在工作时共享容器，并确保与您共享的每个人都获得以相同方式工作的相同容器。

Docker 提供工具和平台来管理容器的生命周期：

* 使用容器开发您的应用程序及其支持组件。
* 容器成为分发和测试应用程序的单元。
* 当准备就绪时，将您的应用程序作为容器或编排服务部署到生产环境中。无论您的生产环境是本地数据中心、云提供商还是两者的混合，这都以相同的方式工作。

## Docker 的用途

### 快速、一致地交付应用程序

Docker 通过允许开发人员使用提供应用程序和服务的本地容器在标准化环境中工作，简化了开发生命周期。容器非常适合持续集成和持续交付（CI/CD）工作流程。

考虑以下示例场景：

- 您的开发人员在本地编写代码，并使用 Docker 容器与同事共享他们的工作。
- 他们使用 Docker 将应用程序推送到测试环境，并运行自动化和手动测试。
- 当开发人员发现错误时，他们可以在开发环境中修复它们，并重新部署到测试环境进行测试和验证。
- 测试完成后，向客户推送修复程序就像将更新的镜像推送到生产环境一样简单。

### 响应式部署和扩展

Docker 基于容器的平台支持高度可移植的工作负载。Docker 容器可以在开发人员的本地笔记本电脑上、数据中心的物理机或虚拟机上、云提供商上或混合环境中运行。

Docker 的可移植性和轻量级特性也使得动态管理工作负载变得容易，可以根据业务需求近乎实时地扩展或缩减应用程序和服务。

### 在相同硬件上运行更多工作负载

Docker 是轻量级且快速的。它为基于虚拟机管理程序的虚拟机提供了一个可行的、具有成本效益的替代方案，因此您可以利用更多的服务器容量来实现业务目标。Docker 非常适合高密度环境以及需要用更少资源完成更多工作的中小型部署。

## Docker 架构

Docker 使用客户端-服务器架构。Docker 客户端与 Docker 守护进程（daemon）通信，后者负责构建、运行和分发 Docker 容器的繁重工作。Docker 客户端和守护进程可以在同一系统上运行，您也可以将 Docker 客户端连接到远程 Docker 守护进程。Docker 客户端和守护进程使用 REST API 通过 UNIX 套接字或网络接口进行通信。另一个 Docker 客户端是 Docker Compose，它允许您处理由一组容器组成的应用程序。

![Docker 架构图](images/docker-architecture.webp)

### Docker 守护进程

Docker 守护进程（`dockerd`）监听 Docker API 请求，并管理 Docker 对象，如镜像、容器、网络和卷。守护进程还可以与其他守护进程通信以管理 Docker 服务。

### Docker 客户端

Docker 客户端（`docker`）是许多 Docker 用户与 Docker 交互的主要方式。当您使用诸如 `docker run` 之类的命令时，客户端会将这些命令发送到 `dockerd`，由其执行。`docker` 命令使用 Docker API。Docker 客户端可以与多个守护进程通信。

### Docker Desktop

Docker Desktop 是一个易于安装的应用程序，适用于 Mac、Windows 或 Linux 环境，使您能够构建和共享容器化应用程序和微服务。Docker Desktop 包括 Docker 守护进程（`dockerd`）、Docker 客户端（`docker`）、Docker Compose、Docker Content Trust、Kubernetes 和 Credential Helper。更多信息，请参阅 [Docker Desktop](/manuals/desktop/_index.md)。

### Docker 镜像仓库

Docker 镜像仓库（registry）存储 Docker 镜像。Docker Hub 是一个任何人都可以使用的公共镜像仓库，Docker 默认在 Docker Hub 上查找镜像。您甚至可以运行自己的私有镜像仓库。

当您使用 `docker pull` 或 `docker run` 命令时，Docker 会从您配置的镜像仓库中拉取所需的镜像。当您使用 `docker push` 命令时，Docker 会将您的镜像推送到您配置的镜像仓库。

### Docker 对象

使用 Docker 时，您会创建和使用镜像、容器、网络、卷、插件和其他对象。本节简要概述其中一些对象。

#### 镜像

镜像（image）是一个只读模板，包含创建 Docker 容器的指令。通常，一个镜像基于另一个镜像，并进行一些额外的自定义。例如，您可以构建一个基于 `ubuntu` 镜像的镜像，但安装 Apache Web 服务器和您的应用程序，以及使应用程序运行所需的配置详细信息。

您可以创建自己的镜像，也可以只使用他人创建并发布在镜像仓库中的镜像。要构建自己的镜像，您需要创建一个 Dockerfile，使用简单的语法定义创建和运行镜像所需的步骤。Dockerfile 中的每条指令都会在镜像中创建一个层。当您更改 Dockerfile 并重新构建镜像时，只有那些已更改的层会被重新构建。这是使镜像与其他虚拟化技术相比如此轻量、小巧和快速的原因之一。

#### 容器

容器（container）是镜像的可运行实例。您可以使用 Docker API 或 CLI 创建、启动、停止、移动或删除容器。您可以将容器连接到一个或多个网络，为其附加存储，甚至可以基于其当前状态创建新镜像。

默认情况下，容器与其他容器及其主机相对隔离。您可以控制容器的网络、存储或其他底层子系统与其他容器或主机的隔离程度。

容器由其镜像以及您在创建或启动时提供的任何配置选项定义。当容器被移除时，其状态中未存储在持久存储中的任何更改都会消失。

##### `docker run` 命令示例

以下命令运行一个 `ubuntu` 容器，以交互方式附加到您的本地命令行会话，并运行 `/bin/bash`。

```console
$ docker run -i -t ubuntu /bin/bash
```

当您运行此命令时，会发生以下情况（假设您使用的是默认镜像仓库配置）：

1.  如果您本地没有 `ubuntu` 镜像，Docker 会从您配置的镜像仓库中拉取它，就像您手动运行 `docker pull ubuntu` 一样。

2.  Docker 创建一个新容器，就像您手动运行 `docker container create` 命令一样。

3.  Docker 为容器分配一个读写文件系统，作为其最终层。这允许正在运行的容器在其本地文件系统中创建或修改文件和目录。

4.  Docker 创建一个网络接口将容器连接到默认网络，因为您没有指定任何网络选项。这包括为容器分配 IP 地址。默认情况下，容器可以使用主机的网络连接连接到外部网络。

5.  Docker 启动容器并执行 `/bin/bash`。因为容器以交互方式运行并附加到您的终端（由于 `-i` 和 `-t` 标志），您可以使用键盘提供输入，同时 Docker 将输出记录到您的终端。

6.  当您运行 `exit` 终止 `/bin/bash` 命令时，容器会停止但不会被删除。您可以再次启动它或删除它。

## 底层技术

Docker 使用 [Go 编程语言](https://golang.org/)编写，并利用 Linux 内核的多项功能来提供其功能。Docker 使用一种称为 `namespaces`（命名空间）的技术来提供称为容器的隔离工作区。当您运行容器时，Docker 会为该容器创建一组命名空间。

这些命名空间提供了一层隔离。容器的每个方面都在单独的命名空间中运行，其访问权限仅限于该命名空间。

## 后续步骤

- [安装 Docker](/get-started/get-docker.md)
- [Docker 快速入门](/get-started/introduction/_index.md)
