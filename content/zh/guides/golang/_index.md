---
title: Go 语言特定指南
linkTitle: Go
description: 使用 Docker 容器化 Go 应用程序
keywords: docker, getting started, go, golang, language, dockerfile
summary: |
  本指南教你如何使用 Docker 容器化 Go 应用程序。
toc_min: 1
toc_max: 2
aliases:
  - /language/golang/
  - /guides/language/golang/
languages: [go]
params:
  time: 30 minutes
---

本指南将向你展示如何使用 Docker 创建、测试和部署容器化的 Go 应用程序。

> **致谢**
>
> Docker 感谢 [Oliver Frolovs](https://www.linkedin.com/in/ofr/) 对本指南的贡献。

## 你将学到什么？

在本指南中，你将学习如何：

- 创建一个 `Dockerfile`，其中包含构建用 Go 编写的程序的容器镜像的指令。
- 在本地 Docker 实例中将镜像作为容器运行并管理容器的生命周期。
- 使用多阶段构建来有效地构建小镜像，同时保持 Dockerfile 易于阅读和维护。
- 使用 Docker Compose 在开发环境中编排多个相关容器的运行。
- 使用 [GitHub Actions](https://docs.github.com/en/actions) 为你的应用程序配置 CI/CD 管道
- 部署你的容器化 Go 应用程序。

## 先决条件

假设你对 Go 及其工具链有一些基本的了解。这不是 Go 教程。如果你是这门语言的新手，[Go 网站](https://golang.org/) 是一个很好的探索之地，所以 _go_（双关语）去看看吧！

你还必须了解一些基本的 [Docker 概念](/get-started/docker-concepts/the-basics/what-is-a-container.md)，并且至少对 [Dockerfile 格式](/manuals/build/concepts/dockerfile.md) 有一些模糊的熟悉。

你的 Docker 设置必须启用 BuildKit。对于 [Docker Desktop](/manuals/desktop/_index.md) 上的所有用户，BuildKit 默认处于启用状态。
如果你已经安装了 Docker Desktop，则无需手动启用 BuildKit。如果你在 Linux 上运行 Docker，请查看 BuildKit [入门](/manuals/build/buildkit/_index.md#getting-started) 页面。

还需要对命令行有一些熟悉。

## 接下来是什么？

本指南的目的是为你提供足够的示例和说明，以便你容器化自己的 Go 应用程序并将其部署到云中。

从构建你的第一个 Go 镜像开始。
