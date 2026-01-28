---
title: 将 Docker Scout 与 Sysdig 集成
linkTitle: Sysdig
description: 使用 Sysdig 将您的运行时环境与 Docker Scout 集成
keywords: scout, sysdig, integration, image analysis, environments, supply chain
---

{{% include "scout-early-access.md" %}}

Sysdig 集成使 Docker Scout 能够自动检测您正在运行的工作负载所使用的镜像。激活此集成可让您实时了解安全状况，并能够将构建与生产环境中运行的内容进行比较。

## 工作原理

Sysdig Agent 捕获容器工作负载的镜像。Docker Scout 与 Sysdig API 集成以发现集群中的镜像。此集成使用 Sysdig 的 Risk Spotlight 功能。更多信息请参阅 [Risk Spotlight Integrations（Sysdig 文档）](https://docs.sysdig.com/en/docs/sysdig-secure/integrations-for-sysdig-secure/risk-spotlight-integrations/)。

> [!TIP]
>
> Sysdig 为 Docker 用户提供免费试用以体验新的 Docker Scout 集成。
>
> {{< button url=`https://sysdig.com/free-trial-for-docker-customers/` text="Sign up" >}}

每个 Sysdig 集成映射到一个环境。当您启用 Sysdig 集成时，您需要为该集群指定环境名称，例如 `production` 或 `staging`。Docker Scout 将集群中的镜像分配到相应的环境。这使您可以使用环境过滤器查看某个环境的漏洞状态和策略合规性。

只有被 Docker Scout 分析过的镜像才能分配到环境。Sysdig 运行时集成本身不会触发镜像分析。要自动分析镜像，请启用[仓库集成](../_index.md#container-registries)。

镜像分析不一定需要在运行时集成之前进行，但环境分配只有在 Docker Scout 分析镜像后才会生效。

## 前提条件

- 在您要集成的集群中安装 Sysdig Agent，请参阅 [Install Sysdig Agent（Sysdig 文档）](https://docs.sysdig.com/en/docs/installation/sysdig-monitor/install-sysdig-agent/)。
- 在 Sysdig 中为 Risk Spotlight Integrations 启用 profiling，请参阅 [Profiling（Sysdig 文档）](https://docs.sysdig.com/en/docs/sysdig-secure/policies/profiling/#enablement)。
- 您必须是组织所有者才能在 Docker Scout Dashboard 中启用集成。

## 集成环境

1. 前往 Docker Scout Dashboard 上的 [Sysdig 集成页面](https://scout.docker.com/settings/integrations/sysdig/)。
2. 在 **How to integrate** 部分，为此集成输入一个配置名称。Docker Scout 使用此标签作为集成的显示名称。

3. 选择 **Next**。

4. 输入 Risk Spotlight API 令牌并在下拉列表中选择区域。

   Risk Spotlight API 令牌是 Docker Scout 与 Sysdig 集成所需的 Sysdig 令牌。有关如何生成 Risk Spotlight 令牌的更多说明，请参阅 [Risk Spotlight Integrations（Sysdig 文档）](https://docs.sysdig.com/en/docs/sysdig-secure/integrations-for-sysdig-secure/risk-spotlight-integrations/docker-scout/#generate-a-token-for-the-integration)。

   区域对应于部署 Sysdig Agent 时设置的 `global.sysdig.region` 配置参数。

5. 选择 **Next**。

   选择 **Next** 后，Docker Scout 会连接到 Sysdig 并检索您 Sysdig 账户的集群名称。集群名称对应于部署 Sysdig Agent 时设置的 `global.clusterConfig.name` 配置参数。

   如果 Docker Scout 使用提供的令牌无法连接到 Sysdig，将显示错误。如果出现错误，您将无法继续集成。请返回并验证配置详情是否正确。

6. 在下拉列表中选择集群名称。

7. 选择 **Next**。

8. 为此集群分配一个环境名称。

    您可以重用现有环境或创建新环境。

9. 选择 **Enable integration**。

启用集成后，Docker Scout 会自动检测集群中运行的镜像，并将这些镜像分配到与集群关联的环境。有关环境的更多信息，请参阅[环境监控](./_index.md)。

> [!NOTE]
>
> Docker Scout 只检测已被分析的镜像。要触发镜像分析，请启用[仓库集成](../_index.md#container-registries)并将镜像推送到您的仓库。
>
> 如果您为此集成创建了新环境，该环境将在至少有一个镜像被分析后出现在 Docker Scout 中。

要集成更多集群，请前往 [Sysdig 集成页面](https://scout.docker.com/settings/integrations/sysdig/)并选择 **Add** 按钮。
