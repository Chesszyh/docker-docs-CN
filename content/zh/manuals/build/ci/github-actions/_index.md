---
title: Docker Build GitHub Actions
linkTitle: GitHub Actions
description: Docker 维护了一套用于构建 Docker 镜像的官方 GitHub Actions。
keywords: ci, github actions, gha,  build, introduction, tutorial
aliases:
  - /ci-cd/github-actions/
  - /build/ci/github-actions/examples/
---

GitHub Actions 是一个流行的 CI/CD 平台，用于自动化您的构建、测试和部署流水线。Docker 提供了一套官方的 GitHub Actions 供您在工作流中使用。这些官方 Actions 是可重用的、易于使用的组件，用于构建、注释和推送镜像。

可用的 GitHub Actions 如下：

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)：使用 BuildKit 构建和推送 Docker 镜像。
- [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)：支持使用 [Bake](../../bake/_index.md) 进行高级构建。
- [Docker Login](https://github.com/marketplace/actions/docker-login)：登录到 Docker 镜像仓库。
- [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)：创建并启动一个 BuildKit 构建器。
- [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action)：从 Git 引用和 GitHub 事件中提取元数据，以生成标签、标注和注释。
- [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose)：安装和设置 [Compose](../../../compose)。
- [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker)：安装 Docker CE。
- [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu)：安装 [QEMU](https://github.com/qemu/qemu) 静态二进制文件，用于多平台构建。
- [Docker Scout](https://github.com/docker/scout-action)：分析 Docker 镜像的安全漏洞。

使用 Docker 的 Actions 提供了易于使用的界面，同时仍允许灵活地自定义构建参数。

## 示例

如果您正在寻找如何使用 Docker GitHub Actions 的示例，请参阅以下部分：

{{% sectionlinks %}}

## 开始使用 GitHub Actions

[Introduction to GitHub Actions with Docker](/guides/gha.md) 指南将引导您完成设置和使用 Docker GitHub Actions 来构建 Docker 镜像并将镜像推送到 Docker Hub 的过程。
