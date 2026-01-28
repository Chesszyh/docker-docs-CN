---
description: 将 Amazon Elastic Container Registry 与 Docker Scout 集成
keywords: docker scout, ecr, integration, image analysis, security, cves
title: 将 Docker Scout 与 Amazon ECR 集成
linkTitle: Amazon ECR
---

将 Docker Scout 与 Amazon Elastic Container Registry（ECR）集成后，您可以查看托管在 ECR 仓库中的镜像洞察。将 Docker Scout 与 ECR 集成并为仓库激活 Docker Scout 后，将镜像推送到仓库会自动触发镜像分析。您可以使用 Docker Scout Dashboard 或 `docker scout` CLI 命令查看镜像洞察。

## 工作原理

为了帮助您将 Docker Scout 与 ECR 集成，您可以使用 CloudFormation 堆栈模板，该模板会创建和配置将 Docker Scout 与您的 ECR 仓库集成所需的 AWS 资源。有关 AWS 资源的更多详情，请参阅 [CloudFormation 堆栈模板](#cloudformation-堆栈模板)。

下图展示了 Docker Scout ECR 集成的工作原理。

![How the ECR integration works](../../images/Scout-ECR.png)

集成后，Docker Scout 会自动拉取并分析您推送到 ECR 仓库的镜像。镜像的元数据存储在 Docker Scout 平台上，但 Docker Scout 不存储容器镜像本身。有关 Docker Scout 如何处理镜像数据的更多信息，请参阅[数据处理](/manuals/scout/deep-dive/data-handling.md)。

### CloudFormation 堆栈模板

下表描述了配置资源。

> [!NOTE]
>
> 创建这些资源会在 AWS 账户上产生少量的经常性费用。表中的 **Cost** 列代表了资源的估计月度成本，假设集成的 ECR 仓库每天推送 100 个镜像。
>
> 此外，当 Docker Scout 从 ECR 拉取镜像时还会产生出站流量费用。出站流量成本大约为每 GB $0.09。

| Resource type                 | Resource name                 | Description                                                                                | Cost  |
| ----------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------ | ----- |
| `AWS::SNSTopic::Topic`        | `SNSTopic`                    | SNS topic for notifying Docker Scout when the AWS resources have been created.             | Free  |
| `AWS::SNS::TopicPolicy`       | `TopicPolicy`                 | Defines the topic for the initial setup notification.                                      | Free  |
| `AWS::SecretsManager::Secret` | `ScoutAPICredentials`         | Stores the credentials used by EventBridge to fire events to Scout.                        | $0.42 |
| `AWS::Events::ApiDestination` | `ApiDestination`              | Sets up the EventBridge connection to Docker Scout for sending ECR push and delete events. | $0.01 |
| `AWS::Events::Connection`     | `Connection`                  | EventBridge connection credentials to Scout.                                               | Free  |
| `AWS::Events::Rule`           | `DockerScoutEcrRule`          | Defines the rule to send ECR pushes and deletes to Scout.                                  | Free  |
| `AWS::Events::Rule`           | `DockerScoutRepoDeletedRule`  | Defines the rule to send ECR repository deletes to Scout.                                  | Free  |
| `AWS::IAM::Role`              | `InvokeApiRole`               | Internal role to grant the event access to `ApiDestination`.                               | Free  |
| `AWS::IAM::Role`              | `AssumeRoleEcrAccess`         | This role has access to `ScoutAPICredentials` for setting up the Docker Scout integration. | Free  |

## 集成您的第一个仓库

在您的 AWS 账户中创建 CloudFormation 堆栈以启用 Docker Scout 集成。

前提条件：

- 您必须有权访问具有创建资源权限的 AWS 账户。
- 您必须是 Docker 组织的所有者。

创建堆栈：

1. 前往 Docker Scout Dashboard 上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 选择 **Create on AWS** 按钮。

   这会在新的浏览器标签页中打开 AWS CloudFormation 控制台的 **Create stack** 向导。如果您尚未登录 AWS，将先重定向到登录页面。

   如果按钮显示为灰色，表示您在 Docker 组织中缺少必要的权限。

3. 按照 **Create stack** 向导中的步骤直到完成。选择您要集成的 AWS 区域。通过创建资源完成该过程。

   向导中的字段已由 CloudFormation 模板预填充，因此您无需编辑任何字段。

4. 当资源创建完成后（AWS 控制台中的 CloudFormation 状态显示 `CREATE_COMPLETE`），返回 Docker Scout Dashboard 中的 ECR 集成页面。

   **Integrated registries** 列表显示您刚刚集成的 ECR 仓库的账户 ID 和区域。如果成功，集成状态为 **Connected**。

ECR 集成现已激活。要让 Docker Scout 开始分析仓库中的镜像，您需要在[仓库设置](https://scout.docker.com/settings/repos/)中为每个仓库激活它。

激活仓库后，您推送的镜像将由 Docker Scout 分析。分析结果会显示在 Docker Scout Dashboard 中。如果您的仓库已包含镜像，Docker Scout 会自动拉取并分析最新的镜像版本。

## 集成其他仓库

要添加其他仓库：

1. 前往 Docker Scout Dashboard 上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 选择列表顶部的 **Add** 按钮。
3. 完成创建 AWS 资源的步骤。
4. 当资源创建完成后，返回 Docker Scout Dashboard 中的 ECR 集成页面。

   **Integrated registries** 列表显示您刚刚集成的 ECR 仓库的账户 ID 和区域。如果成功，集成状态为 **Connected**。

接下来，在[仓库设置](https://scout.docker.com/settings/repos/)中为您要分析的仓库激活 Docker Scout。

## 移除集成

要移除集成的 ECR 仓库，您必须是 Docker 组织的所有者。

1. 前往 Docker Scout Dashboard 上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 在集成仓库列表中找到您要移除的仓库，并选择 **Actions** 列中的移除图标。

   如果移除图标被禁用，表示您在 Docker 组织中缺少必要的权限。

3. 在打开的对话框中，选择 **Remove** 确认。

> [!IMPORTANT]
>
> 从 Docker Scout Dashboard 移除集成不会删除您 AWS 账户中的资源。
>
> 在 Docker Scout 中移除集成后，请前往 AWS 控制台删除您要移除的集成对应的 **DockerScoutECRIntegration** CloudFormation 堆栈。

## 故障排除

### 无法集成仓库

在 Docker Scout Dashboard 的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)上检查集成的 **Status**。

- 如果状态长时间显示为 **Pending**，表示 AWS 端的集成尚未完成。选择 **Pending** 链接打开 CloudFormation 向导，并完成所有步骤。

- **Error** 状态表示后端出现问题。您可以尝试[移除集成](#移除集成)然后重新创建。

### ECR 镜像未显示在 Dashboard 中

如果您的 ECR 镜像的镜像分析结果未显示在 Docker Scout Dashboard 中：

- 确保您已为仓库激活 Docker Scout。在[仓库设置](https://scout.docker.com/settings/repos/)中查看和管理已激活的仓库。

- 确保您仓库的 AWS 账户 ID 和区域已列在 ECR 集成页面上。

  账户 ID 和区域包含在仓库主机名中：`<aws_account_id>.dkr.ecr.<region>.amazonaws.com/<image>`
