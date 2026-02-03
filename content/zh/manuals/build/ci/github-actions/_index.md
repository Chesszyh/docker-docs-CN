---
title: Docker Build GitHub Actions
linkTitle: GitHub Actions
description: Docker 维护了一套用于构建 Docker 镜像的官方 GitHub Actions。
keywords: ci, github actions, gha, build, 构建, 入门, 教程
aliases:
  - /ci-cd/github-actions/
  - /build/ci/github-actions/examples/
---

GitHub Actions 是一款流行的 CI/CD 平台，用于自动化您的构建、测试和部署流水线。Docker 提供了一套官方 GitHub Actions 供您在工作流中使用。这些官方 Actions 是可复用且易于使用的组件，用于构建、注解和推送镜像。

以下是可用的 GitHub Actions：

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)：使用 BuildKit 构建并推送 Docker 镜像。
- [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)：支持使用 [Bake](../../bake/_index.md) 进行高级构建。
- [Docker Login](https://github.com/marketplace/actions/docker-login)：登录到 Docker 注册表。
- [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)：创建并引导一个 BuildKit 构建器。
- [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action)：从 Git 引用和 GitHub 事件中提取元数据，以生成标签、标签 (labels) 和注解 (annotations)。
- [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose)：安装并设置 [Compose](../../../compose)。
- [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker)：安装 Docker CE。
- [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu)：安装 [QEMU](https://github.com/qemu/qemu) 静态二进制文件，用于多平台构建。
- [Docker Scout](https://github.com/docker/scout-action)：分析 Docker 镜像的安全漏洞。

使用 Docker 的 Actions 既提供了易用的界面，又保留了自定义构建参数的灵活性。

## 示例

如果您正在寻找关于如何使用 Docker GitHub Actions 的示例，请参考以下章节：

{{% sectionlinks %}}

## GitHub Actions 入门

[使用 Docker 入门 GitHub Actions](/guides/gha.md) 指南将引导您完成设置并使用 Docker GitHub Actions 构建 Docker 镜像并推送到 Docker Hub 的过程。