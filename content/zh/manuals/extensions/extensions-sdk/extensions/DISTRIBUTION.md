---
title: 打包和发布您的扩展
description: Docker 扩展分发
keywords: Docker, extensions, sdk, distribution
aliases:
 - /desktop/extensions-sdk/extensions/DISTRIBUTION/
weight: 30
---

本页包含有关如何打包和分发扩展的额外信息。

## 打包您的扩展

Docker 扩展被打包为 Docker 镜像。整个扩展运行时，包括 UI、后端服务（主机或虚拟机）以及任何必要的二进制文件，都必须包含在扩展镜像中。
每个扩展镜像必须在其文件系统根目录下包含一个 `metadata.json` 文件，用于定义[扩展的内容](../architecture/metadata.md)。

Docker 镜像必须具有多个[镜像标签](labels.md)，提供有关扩展的信息。请参阅如何使用[扩展标签](labels.md)来提供扩展概述信息。

要打包和发布扩展，您必须构建 Docker 镜像（`docker build`），并将镜像推送到 [Docker Hub](https://hub.docker.com/)（`docker push`），使用特定的标签来管理扩展版本。

## 发布您的扩展

Docker 镜像标签必须遵循 semver（语义化版本）约定，以便获取扩展的最新版本，并了解是否有可用的更新。请访问 [semver.org](https://semver.org/) 了解更多关于语义化版本控制的信息。

扩展镜像必须是多架构镜像，以便用户可以在 ARM/AMD 硬件上安装扩展。这些多架构镜像可以包含 ARM/AMD 特定的二进制文件。Mac 用户将根据其架构自动使用正确的镜像。
在主机上安装二进制文件的扩展还必须在同一扩展镜像中提供 Windows 二进制文件。请参阅如何为您的扩展[构建多架构镜像](multi-arch.md)。

您可以在代码仓库上实现扩展而不受任何限制。Docker 不需要访问代码仓库即可使用扩展。此外，您可以管理扩展的新版本发布，而不依赖于 Docker Desktop 的版本发布。

## 新版本和更新

您可以通过将带有新标签的新镜像推送到 Docker Hub 来发布 Docker 扩展的新版本。

推送到与扩展对应的镜像仓库的任何新镜像都定义了该扩展的新版本。镜像标签用于标识版本号。扩展版本必须遵循 semver 以便于理解和比较版本。

Docker Desktop 扫描 Marketplace 中发布的扩展列表以查找新版本，并在用户可以升级特定扩展时向用户发送通知。目前，不属于 Marketplace 的扩展没有自动更新通知。

用户可以下载并安装任何扩展的较新版本，而无需更新 Docker Desktop 本身。

## 扩展 API 依赖

扩展必须指定其依赖的扩展 API 版本。Docker Desktop 检查扩展所需的版本，并且仅建议安装与当前安装的 Docker Desktop 版本兼容的扩展。用户可能需要更新 Docker Desktop 才能安装最新可用的扩展。

扩展镜像标签必须指定扩展依赖的 API 版本。这允许 Docker Desktop 检查较新版本的扩展镜像，而无需预先下载完整的扩展镜像。

## 扩展和扩展 SDK 的许可证

[Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) 采用 Apache 2.0 许可证，可免费使用。

对于每个扩展应如何获得许可没有限制，这由您在创建新扩展时决定。
