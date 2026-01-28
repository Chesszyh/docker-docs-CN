---
title: 将 Docker Scout 与 GitHub 集成
linkTitle: GitHub
description: 通过 GitHub 应用集成 Docker Scout，直接在您的仓库中获取修复建议
keywords: scout, github, integration, image analysis, supply chain, remediation, source code
---

{{< summary-bar feature_name="Docker Scout GitHub" >}}

Docker Scout 的 GitHub 应用集成授予 Docker Scout 访问您在 GitHub 上的源代码仓库的权限。这种对镜像创建过程的增强可见性意味着 Docker Scout 可以为您提供自动化的、有针对性的修复建议。

## 工作原理

当您启用 GitHub 集成后，Docker Scout 可以在镜像分析结果和源代码之间建立直接关联。

在分析您的镜像时，Docker Scout 会检查 [provenance attestations](/manuals/build/metadata/attestations/slsa-provenance.md) 以检测镜像源代码仓库的位置。如果找到源代码位置，并且您已启用 GitHub 应用，Docker Scout 会解析用于创建镜像的 Dockerfile。

解析 Dockerfile 可以揭示用于构建镜像的基础镜像标签。通过了解使用的基础镜像标签，Docker Scout 可以检测该标签是否已过时，即它已被更改为指向不同的镜像摘要。例如，假设您使用 `alpine:3.18` 作为基础镜像，在稍后的某个时间点，镜像维护者发布了 `3.18` 版本的补丁版本，其中包含安全修复。您一直使用的 `alpine:3.18` 标签变得过时了；您使用的 `alpine:3.18` 不再是最新的。

当这种情况发生时，Docker Scout 会检测到差异并通过[基础镜像最新策略](/manuals/scout/policy/_index.md#up-to-date-base-images-policy)将其呈现出来。当启用 GitHub 集成后，您还会获得关于如何更新基础镜像的自动建议。有关 Docker Scout 如何帮助您自动改善供应链行为和安全状况的更多信息，请参阅[修复](../../policy/remediation.md)。

## 设置

要将 Docker Scout 与您的 GitHub 组织集成：

1. 前往 Docker Scout Dashboard 上的 [GitHub 集成](https://scout.docker.com/settings/integrations/github/)页面。
2. 选择 **Integrate GitHub app** 按钮以打开 GitHub。
3. 选择您要集成的组织。
4. 选择是要集成 GitHub 组织中的所有仓库还是手动选择仓库。
5. 选择 **Install & Authorize** 将 Docker Scout 应用添加到组织。

   这会将您重定向回 Docker Scout Dashboard，其中列出了您活跃的 GitHub 集成。

GitHub 集成现已激活。
