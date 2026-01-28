---
title: 将 Docker Scout 与 SonarQube 集成
linkTitle: SonarQube
description: 使用项目中定义的 SonarQube 质量门对镜像进行评估
keywords: scout, supply chain, integration, code quality
---

SonarQube 集成使 Docker Scout 能够通过策略评估（Policy Evaluation）呈现 SonarQube 质量门检查结果，这体现在新的 [SonarQube 质量门策略](/manuals/scout/policy/_index.md#sonarqube-quality-gates-policy)中。

## 工作原理

此集成使用 [SonarQube webhooks](https://docs.sonarsource.com/sonarqube/latest/project-administration/webhooks/) 在 SonarQube 项目分析完成时通知 Docker Scout。当 webhook 被调用时，Docker Scout 会接收分析结果并将其存储在数据库中。

当您将新镜像推送到仓库时，Docker Scout 会评估与该镜像对应的 SonarQube 分析记录结果。Docker Scout 使用镜像上的 Git 来源元数据（来自 provenance attestations 或 OCI 注解）将镜像仓库与 SonarQube 分析结果关联起来。

> [!NOTE]
>
> Docker Scout 无法访问历史 SonarQube 分析记录。只有在启用集成后记录的分析结果才能被 Docker Scout 使用。

自托管的 SonarQube 实例和 SonarCloud 均受支持。

## 前提条件

要将 Docker Scout 与 SonarQube 集成，请确保：

- 您的镜像仓库已[与 Docker Scout 集成](../_index.md#container-registries)。
- 您的镜像构建时包含 [provenance attestations](/manuals/build/metadata/attestations/slsa-provenance.md) 或 `org.opencontainers.image.revision` 注解，其中包含 Git 仓库信息。

## 启用 SonarQube 集成

1. 前往 Docker Scout Dashboard 上的 [SonarQube 集成页面](https://scout.docker.com/settings/integrations/sonarqube/)。
2. 在 **How to integrate** 部分，为此集成输入一个配置名称。Docker Scout 使用此标签作为集成的显示名称以及 webhook 的名称。
3. 选择 **Next**。
4. 输入您的 SonarQube 实例的配置详情。Docker Scout 使用这些信息创建 SonarQube webhook。

   在 SonarQube 中，[生成一个新的 **User token**](https://docs.sonarsource.com/sonarqube/latest/user-guide/user-account/generating-and-using-tokens/#generating-a-token)。该令牌需要对指定项目具有 'Administer' 权限，或具有全局 'Administer' 权限。

   输入令牌、您的 SonarQube URL 以及您的 SonarQube 组织 ID。如果您使用的是 SonarCloud，则 SonarQube 组织是必填项。

5. 选择 **Enable configuration**。

   Docker Scout 会执行连接测试以验证所提供的详情是否正确，以及令牌是否具有必要的权限。

6. 连接测试成功后，您将被重定向到 SonarQube 集成概览页面，该页面列出了您所有的 SonarQube 集成及其状态。

从集成概览页面，您可以直接访问 **SonarQube Quality Gates Policy**。此策略最初不会有任何结果。要开始看到此策略的评估结果，请触发项目的新 SonarQube 分析并将相应的镜像推送到仓库。更多信息请参阅[策略描述](../../policy/_index.md#sonarqube-quality-gates)。
