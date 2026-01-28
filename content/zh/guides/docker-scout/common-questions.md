---
title: 常见挑战和问题
description: 探索与 Docker Scout 相关的常见挑战和问题。
---

<!-- vale Docker.HeadingLength = NO -->

### Docker Scout 与其他安全工具有何不同？

与第三方安全工具相比，Docker Scout 采用更全面的容器安全方法。第三方安全工具即使提供修复指导，也往往在软件供应链中的应用程序安全态势方面范围有限，建议的修复方案也常常不够完善。这些工具要么在运行时监控方面存在局限性，要么完全没有运行时保护功能。即使它们提供运行时监控，在关键策略的遵循方面也很有限。第三方安全工具对 Docker 特定构建的策略评估范围也有限。Docker Scout 专注于整个软件供应链，提供可操作的指导，并通过强大的策略执行提供全面的运行时保护，不仅仅是识别容器中的漏洞，还帮助您从底层构建安全的应用程序。

### 我可以将 Docker Scout 与 Docker Hub 以外的外部仓库一起使用吗？

您可以将 Scout 与 Docker Hub 以外的仓库一起使用。将 Docker Scout 与第三方容器仓库集成后，Docker Scout 可以对这些仓库运行镜像分析，这样即使镜像不是托管在 Docker Hub 上，您也可以了解这些镜像的组成。

以下容器仓库集成可用：

- Artifactory
- Amazon Elastic Container Registry
- Azure Container Registry

在[将 Docker Scout 与第三方仓库集成](/scout/integrations/#container-registries)中了解有关配置 Scout 与您的仓库的更多信息。

### Docker Scout CLI 是否默认包含在 Docker Desktop 中？

是的，Docker Scout CLI 插件预装在 Docker Desktop 中。

### 是否可以在没有 Docker Desktop 的 Linux 系统上运行 `docker scout` 命令？

如果您运行的是不带 Docker Desktop 的 Docker Engine，Docker Scout 不会预装，但您可以[将其作为独立二进制文件安装](/scout/install/)。

### Docker Scout 如何使用 SBOM？

SBOM（软件物料清单）是构成软件组件的成分列表。[Docker Scout 使用 SBOM](/scout/concepts/sbom/) 来确定 Docker 镜像中使用的组件。当您分析镜像时，Docker Scout 将使用附加到镜像的 SBOM（作为证明），或者通过分析镜像内容即时生成 SBOM。

SBOM 与安全公告数据库进行交叉引用，以确定镜像中的任何组件是否存在已知漏洞。

<div id="scout-lp-survey-anchor"></div>
