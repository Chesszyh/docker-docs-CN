---
title: 构建证明
keywords: build, attestations, sbom, provenance, metadata
description: |
  介绍 Docker Build 中的 SBOM 和来源证明，
  它们是什么以及为什么存在
weight: 50
---

{{< youtube-embed qOzcycbTs4o >}}

[构建证明](/manuals/build/metadata/attestations/_index.md)（Build attestations）为您提供有关镜像构建方式及其包含内容的详细信息。这些证明由 BuildKit 在构建时生成，作为元数据附加到最终镜像，使您可以检查镜像以查看其来源、创建者和内容。这些信息可帮助您就镜像的安全性及其对供应链的影响做出明智的决策。

Docker Scout 使用这些证明来评估镜像的安全性和供应链状态，并为问题提供修复建议。如果检测到问题（例如缺失或过时的证明），Docker Scout 可以指导您如何添加或更新它们，确保合规性并提高对镜像安全状态的可见性。

有两种关键类型的证明：

- **SBOM（软件物料清单）**：列出镜像中的软件组件。
- **来源证明（Provenance）**：详细说明镜像的构建方式。

您可以通过使用 `docker buildx build` 命令配合 `--provenance` 和 `--sbom` 标志来创建证明。证明附加到镜像索引，使您无需拉取整个镜像即可检查它们。Docker Scout 利用这些元数据为您提供更精确的建议和对镜像安全性的更好控制。

<div id="scout-lp-survey-anchor"></div>
