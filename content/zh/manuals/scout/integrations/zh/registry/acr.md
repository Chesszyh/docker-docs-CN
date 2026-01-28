---
description: 将 Azure Container Registry 与 Docker Scout 集成
keywords: docker scout, acr, azure, integration, image analysis, security, cves
title: 将 Docker Scout 与 Azure Container Registry 集成
linkTitle: Azure Container Registry
---

将 Docker Scout 与 Azure Container Registry（ACR）集成后，您可以查看托管在 ACR 仓库中的镜像洞察。将 Docker Scout 与 ACR 集成并为仓库激活 Docker Scout 后，将镜像推送到仓库会自动触发镜像分析。您可以使用 Docker Scout Dashboard 或 `docker scout` CLI 命令查看镜像洞察。

## 工作原理

为了帮助您将 Azure Container Registry 与 Docker Scout 集成，您可以使用自定义的 Azure Resource Manager（ARM）模板，该模板会自动在 Azure 中为您创建必要的基础设施：

- 用于镜像推送和删除事件的 EventGrid Topic 和 Subscription。
- 仓库的只读授权令牌，用于列出仓库和摄取镜像。

在 Azure 中创建资源后，您可以为集成的 ACR 实例中的镜像仓库启用集成。启用仓库后，推送新镜像会自动触发镜像分析。分析结果会显示在 Docker Scout Dashboard 中。

如果您在已包含镜像的仓库上启用集成，Docker Scout 会自动拉取并分析最新的镜像版本。

### ARM 模板

下表描述了配置资源。

> [!NOTE]
>
> 创建这些资源会在 Azure 账户上产生少量的经常性费用。表中的 **Cost** 列代表了资源的估计月度成本，假设集成的 ACR 仓库每天推送 100 个镜像。
>
> 出站流量（Egress）成本因使用情况而异，但大约为每 GB $0.1，前 100 GB 免费。

| Azure                   | Resource                                                                                   | Cost                                              |
| ----------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| Event Grid system topic | Subscribe to Azure Container Registry events (image push and image delete)                 | Free                                              |
| Event subscription      | Send Event Grid events to Scout via a Webhook subscription                                 | $0.60 for every 1M messages. First 100k for free. |
| Registry Token          | Read-only token used for Scout to list the repositories, and pull images from the registry | Free                                              |

以下 JSON 文档展示了 Docker Scout 用于创建 Azure 资源的 ARM 模板。

{{< accordion title="JSON template" >}}

{{< acr-template.inline >}}
{{ with resources.GetRemote "https://prod-scout-integration-templates.s3.amazonaws.com/latest/acr_token_template.json" }}
{{ $data := .Content | transform.Unmarshal }}

```json
{{ transform.Remarshal "json" $data }}
```

{{ end }}
{{< /acr-template.inline >}}

{{< /accordion >}}

## 集成仓库

1. 前往 Docker Scout Dashboard 上的 [ACR 集成页面](https://scout.docker.com/settings/integrations/azure/)。
2. 在 **How to integrate** 部分，输入您要集成的仓库的 **Registry hostname**。
3. 选择 **Next**。
4. 选择 **Deploy to Azure** 以在 Azure 中打开模板部署向导。

   如果您尚未登录 Azure 账户，可能会提示您登录。

5. 在模板向导中，配置您的部署：

   - **Resource group**：输入与容器仓库相同的资源组。Docker Scout 资源必须部署到与仓库相同的资源组中。

   - **Registry name**：该字段会预填充仓库主机名的子域名。

6. 选择 **Review + create**，然后选择 **Create** 以部署模板。

7. 等待部署完成。
8. 在 **Deployment details** 部分，点击新创建的 **Container registry token** 类型的资源。为此令牌生成新密码。

    或者，使用 Azure 中的搜索功能导航到您要集成的 **Container registry** 资源，并为创建的访问令牌生成新密码。

9. 复制生成的密码并返回 Docker Scout Dashboard 完成集成。

10. 将生成的密码粘贴到 **Registry token** 字段中。
11. 选择 **Enable integration**。

选择 **Enable integration** 后，Docker Scout 会执行连接测试以验证集成。如果验证成功，您将被重定向到 Azure 仓库摘要页面，该页面显示当前组织的所有 Azure 集成。

接下来，在[仓库设置](https://scout.docker.com/settings/repos/)中为您要分析的仓库激活 Docker Scout。

激活仓库后，您推送的镜像将由 Docker Scout 分析。分析结果会显示在 Docker Scout Dashboard 中。如果您的仓库已包含镜像，Docker Scout 会自动拉取并分析最新的镜像版本。

## 移除集成

> [!IMPORTANT]
>
> 在 Docker Scout Dashboard 中移除集成不会自动删除在 Azure 中创建的资源。

要移除 ACR 集成：

1. 前往 Docker Scout Dashboard 上的 [ACR 集成页面](https://scout.docker.com/settings/integrations/azure/)。
2. 找到您要移除的 ACR 集成，然后选择 **Remove** 按钮。
3. 在打开的对话框中，选择 **Remove** 确认。
4. 在 Docker Scout Dashboard 中移除集成后，还需要删除与该集成相关的 Azure 资源：

   - 容器仓库的 `docker-scout-readonly-token` 令牌。
   - `docker-scout-repository` Event Grid System Topic。
