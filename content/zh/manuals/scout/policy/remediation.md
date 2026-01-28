---
title: Docker Scout 修复
description: 了解 Docker Scout 如何使用修复功能帮助您自动改善软件质量
keywords: scout, supply chain, security, remediation, automation
---

{{< summary-bar feature_name="Remediation with Docker Scout" >}}

Docker Scout 通过基于策略评估结果提供建议来帮助您修复供应链或安全问题。建议是您可以采取的操作，可以改善策略合规性，或向镜像添加元数据，使 Docker Scout 能够提供更好的评估结果和建议。

Docker Scout 为以下策略类型的默认策略提供修复建议：

- [Up-to-Date Base Images 修复](#up-to-date-base-images-remediation)
- [Supply Chain Attestations 修复](#supply-chain-attestations-remediation)

<!-- TODO(dvdksn): verify the following -->
> [!NOTE]
> 自定义策略不支持引导式修复。

对于违反策略的镜像，建议侧重于解决合规问题和修复违规。对于 Docker Scout 无法确定合规性的镜像，建议会向您展示如何满足先决条件，以确保 Docker Scout 能够成功评估策略。

## 查看建议

建议出现在 Docker Scout 仪表板的策略详情页面上。要进入此页面：

1. 前往 Docker Scout 仪表板中的[策略页面](https://scout.docker.com/reports/policy)。
2. 在列表中选择一个策略。

策略详情页面根据策略状态将评估结果分为两个不同的标签页：

- Violations（违规）
- Compliance unknown（合规性未知）

**Violations** 标签页列出不符合所选策略的镜像。**Compliance unknown** 标签页列出 Docker Scout 无法确定其合规状态的镜像。当合规性未知时，Docker Scout 需要有关镜像的更多信息。

要查看镜像的建议操作，请将鼠标悬停在列表中的某个镜像上，以显示 **View fixes** 按钮。

![策略违规的修复](../images/remediation.png)

选择 **View fixes** 按钮以打开包含镜像建议操作的修复侧边栏。

如果有多个建议可用，主要建议显示为 **Recommended fix**。其他建议列为 **Quick fixes**。快速修复通常是提供临时解决方案的操作。

侧边栏还可能包含与可用建议相关的一个或多个帮助部分。

## Up-to-Date Base Images 修复

**Up-to-Date Base Images** 策略检查您使用的基础镜像是否是最新的。修复侧边栏中显示的建议操作取决于 Docker Scout 拥有的关于您镜像的信息量。可用信息越多，建议就越好。

以下场景概述了根据镜像可用信息的不同建议。

### 无来源证明

为了让 Docker Scout 能够评估此策略，您必须向镜像添加[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。如果您的镜像没有来源证明，合规性将无法确定。

<!--
  TODO(dvdksn): no support for the following, yet

  When provenance attestations are unavailable, Docker Scout provides generic,
  best-effort recommendations in the remediation side panel. These
  recommendations estimate your base using information from image analysis
  results. The base image version is unknown, but you can manually select the
  version you use in the remediation side panel. This lets Docker Scout evaluate
  whether the base image detected in the image analysis is up-to-date with the
  version you selected.

  https://github.com/docker/docs/pull/18961#discussion_r1447186845
-->

### 有来源证明

添加来源证明后，Docker Scout 可以正确检测您正在使用的基础镜像版本。证明中找到的版本会与相应标签的当前版本进行交叉引用，以确定它是否是最新的。

如果存在策略违规，建议的操作会显示如何将基础镜像版本更新到最新版本，同时将基础镜像版本固定到特定摘要。有关更多信息，请参阅[固定基础镜像版本](/manuals/build/building/best-practices.md#pin-base-image-versions)。

### 启用 GitHub 集成

如果您在 GitHub 上托管镜像的源代码，可以启用 [GitHub 集成](../integrations/source-code-management/github.md)。此集成使 Docker Scout 能够提供更有用的修复建议，并让您可以直接从 Docker Scout 仪表板启动违规修复。

启用 GitHub 集成后，您可以使用修复侧边栏在镜像的 GitHub 仓库上发起拉取请求。拉取请求会自动将 Dockerfile 中的基础镜像版本更新到最新版本。

这种自动修复会将您的基础镜像固定到特定摘要，同时帮助您在新版本可用时保持更新。将基础镜像固定到摘要对于可重复性很重要，并有助于避免不需要的更改进入您的供应链。

有关基础镜像固定的更多信息，请参阅[固定基础镜像版本](/manuals/build/building/best-practices.md#pin-base-image-versions)。

<!--
  TODO(dvdksn): no support for the following, yet

  Enabling the GitHub integration also allows Docker Scout to visualize the
  remediation workflow in the Docker Scout Dashboard. Each step, from the pull
  request being raised to the image being deployed to an environment, is
  displayed in the remediation sidebar when inspecting the image.

  https://github.com/docker/docs/pull/18961#discussion_r1447189475
-->

## Supply Chain Attestations 修复

默认的 **Supply Chain Attestations** 策略要求镜像具有完整的来源证明和 SBOM 证明。如果您的镜像缺少证明，或者证明不包含足够的信息，则违反策略。

修复侧边栏中的建议可帮助指导您需要采取哪些操作来解决问题。例如，如果您的镜像有来源证明，但证明不包含足够的信息，建议您使用 [`mode=max`](/manuals/build/metadata/attestations/slsa-provenance.md#max) 来源重新构建镜像。
