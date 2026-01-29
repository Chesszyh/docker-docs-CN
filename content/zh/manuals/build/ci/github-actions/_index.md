---
title: Docker 构建 GitHub Actions
linkTitle: GitHub Actions
description: Docker 维护了一组用于构建 Docker 镜像的官方 GitHub Actions。
keywords: ci, github actions, gha, 构建, 简介, 教程
---

GitHub Actions 是一个流行的 CI/CD 平台，用于自动化您的构建、测试和部署流水线。Docker 提供了一组官方的 GitHub Actions 供您在工作流中使用。这些官方 actions 是可重用的、易于使用的组件，用于构建、标注和推送镜像。

提供以下 GitHub Actions：

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)：使用 BuildKit 构建并推送 Docker 镜像。
- [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)：支持使用 [Bake](../../bake/_index.md) 进行高级构建。
- [Docker Login](https://github.com/marketplace/actions/docker-login)：登录到 Docker 镜像库。
- [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)：创建并启动 BuildKit 构建器。
- [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action)：从 Git 引用和 GitHub 事件中提取元数据，以生成标签（tags）、标签（labels）和注解（annotations）。
- [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose)：安装并设置 [Compose](../../../compose)。
- [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker)：安装 Docker CE。
- [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu)：安装 [QEMU](https://github.com/qemu/qemu) 静态二进制文件，用于多平台构建。
- [Docker Scout](https://github.com/docker/scout-action)：分析 Docker 镜像的安全漏洞。

使用 Docker 的 actions 提供了易于使用的接口，同时仍然允许灵活地自定义构建参数。

## 示例

如果您正在寻找有关如何使用 Docker GitHub Actions 的示例，请参阅以下部分：

{{% sectionlinks %}}

## GitHub Actions 入门

[GitHub Actions 与 Docker 入门](/guides/gha.md) 指南将引导您完成设置和使用 Docker GitHub Actions 构建 Docker 镜像并将其推送到 Docker Hub 的过程。
