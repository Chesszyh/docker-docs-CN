---
description: 了解 Docker Hub 的拉取使用量和限制。
keywords: Docker Hub, pulls, usage, limit
title: Docker Hub 拉取使用量和限制
linkTitle: 拉取
weight: 10
aliases:
  - /docker-hub/usage/storage/
  - /docker-hub/usage/repositories/
---

未认证用户和 Docker Personal 用户在 Docker Hub 上有 6 小时拉取速率限制。相比之下，Docker Pro、Team 和 Business 用户享有无限拉取速率。

以下拉取使用量和限制根据您的订阅适用，受合理使用条款约束：

| 用户类型 | 每 6 小时拉取速率限制 |
|--------------------------|-----------------------------------------|
| Business（已认证） | 无限制 |
| Team（已认证） | 无限制 |
| Pro（已认证） | 无限制 |
| Personal（已认证） | 200 |
| 未认证用户 | 每个 IPv4 地址或 IPv6 /64 子网 100 次 |

## 拉取定义

拉取定义如下：

 - Docker 拉取包括版本检查和作为拉取结果发生的任何下载。根据客户端，`docker pull` 可以通过执行版本检查来验证镜像或标签的存在而不下载它。
 - 版本检查不计入使用定价。
 - 对普通镜像的拉取为[单个清单](https://github.com/opencontainers/image-spec/blob/main/manifest.md)计为一次拉取。
 - 对多架构镜像的拉取将为每个不同的架构计为一次拉取。

## 拉取归属

来自已认证用户的拉取可以归属于个人或[组织命名空间](/manuals/admin/faqs/general-faqs.md#whats-an-organization-name-or-namespace)。

归属基于以下规则：

- 私有拉取：私有仓库的拉取归属于仓库的命名空间所有者。
- 公共拉取：从公共仓库拉取镜像时，归属根据域名关联和组织成员身份确定。
- 已验证的域名所有权：从与已验证域名关联的账户拉取镜像时，归属设置为该[域名](/manuals/security/faqs/single-sign-on/domain-faqs.md)的所有者。
- 单一组织成员身份：
   - 如果已验证域名的所有者是公司，且用户只属于该[公司](../../admin/faqs/company-faqs.md#what-features-are-supported-at-the-company-level)内的一个组织，则拉取归属于该特定组织。
   - 如果用户只属于一个组织，则拉取归属于该特定组织。
- 多个组织成员身份：如果用户属于公司下的多个组织，则拉取归属于用户的个人命名空间。


### 认证

为确保正确归属您的拉取，您必须使用 Docker Hub 进行认证。以下部分提供有关如何登录 Docker Hub 以认证您的拉取的信息。

#### Docker Desktop

如果您使用的是 Docker Desktop，您可以从 Docker Desktop 菜单登录 Docker Hub。

从 Docker Desktop 菜单选择 **Sign in / Create Docker ID**（登录/创建 Docker ID），然后按照屏幕上的说明完成登录过程。

#### Docker Engine

如果您使用的是独立版本的 Docker Engine，请从终端运行 `docker login` 命令以使用 Docker Hub 进行认证。有关如何使用该命令的信息，请参阅 [docker login](/reference/cli/docker/login.md)。

#### Docker Swarm

如果您运行的是 Docker Swarm，必须使用 `--with-registry-auth` 标志以使用 Docker Hub 进行认证。有关更多信息，请参阅[创建服务](/reference/cli/docker/service/create.md#with-registry-auth)。如果您使用 Docker Compose 文件部署应用程序栈，请参阅 [docker stack deploy](/reference/cli/docker/stack/deploy.md)。

#### GitHub Actions

如果您使用 GitHub Actions 构建和推送 Docker 镜像到 Docker Hub，请参阅 [login action](https://github.com/docker/login-action#dockerhub)。如果您使用其他 Action，必须以类似方式添加您的用户名和访问令牌进行认证。

#### Kubernetes

如果您运行的是 Kubernetes，请按照[从私有注册表拉取镜像](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)中的说明获取认证信息。

#### 第三方平台

如果您使用任何第三方平台，请按照您的提供商关于使用注册表认证的说明操作。

> [!NOTE]
>
> 通过第三方平台拉取镜像时，平台可能使用相同的 IPv4 地址或 IPv6 /64 子网为多个用户拉取镜像。即使您已认证，归属于单个 IPv4 地址或 IPv6 /64 子网的拉取也可能导致[滥用速率限制](./_index.md#abuse-rate-limit)。

- [Artifactory](https://www.jfrog.com/confluence/display/JFROG/Advanced+Settings#AdvancedSettings-RemoteCredentials)
- [AWS CodeBuild](https://aws.amazon.com/blogs/devops/how-to-use-docker-images-from-a-private-registry-in-aws-codebuild-for-your-build-environment/)
- [AWS ECS/Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html)
- [Azure Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml#sep-docreg)
- [Chipper CI](https://docs.chipperci.com/builds/docker/#rate-limit-auth)
- [CircleCI](https://circleci.com/docs/2.0/private-images/)
- [Codefresh](https://codefresh.io/docs/docs/docker-registries/external-docker-registries/docker-hub/)
- [Drone.io](https://docs.drone.io/pipeline/docker/syntax/images/#pulling-private-images)
- [GitLab](https://docs.gitlab.com/ee/user/packages/container_registry/#authenticate-with-the-container-registry)
- [LayerCI](https://layerci.com/docs/advanced-workflows#logging-in-to-docker)
- [TeamCity](https://www.jetbrains.com/help/teamcity/integrating-teamcity-with-docker.html#Conforming+with+Docker+download+rate+limits)

## 查看每月拉取量和包含的使用量

您可以在 Docker Hub 的[使用量页面](https://hub.docker.com/usage/pulls)查看您的每月拉取量。

在该页面上，您还可以向您的电子邮件发送报告，其中包含一个逗号分隔文件，包含以下详细信息。

| CSV 列 | 定义 | 使用指南 |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `datehour` | 导致数据传输的拉取的日期和小时（`yyyy/mm/dd/hh`）。 | 这有助于识别峰值使用时间和模式。 |
| `user_name` | 拉取镜像的用户的 Docker ID | 这使组织所有者可以跟踪每个用户的数据消耗并有效管理资源。 |
| `repository` | 被拉取的镜像的仓库名称。 | 这使您可以识别哪些仓库被最频繁访问并消耗最多的数据传输。 |
| `access_token_name` | 用于 Docker CLI 认证的访问令牌名称。`generated` 令牌是当用户登录时由 Docker 客户端自动生成的。 | 个人访问令牌通常用于认证自动化工具（Docker Desktop、CI/CD 工具等）。这对于识别哪个自动化系统发出了拉取很有用。 |
| `ips` | 用于拉取镜像的 IP 地址。此字段是聚合的，因此可能出现多个 IP 地址，代表在同一日期和小时内用于拉取镜像的所有 IP。 | 这有助于您了解数据传输的来源，这对于诊断和识别自动化或手动拉取的模式很有用。 |
| `repository_privacy` | 被拉取的镜像仓库的隐私状态。可以是 `public` 或 `private`。 | 这区分了公共和私有仓库，以识别拉取影响哪个数据传输阈值。 |
| `tag` | 镜像的标签。仅当拉取包含标签时，标签才可用。 | 这有助于识别镜像。标签通常用于识别镜像的特定版本或变体。 |
| `digest` | 镜像的唯一镜像摘要。 | 这有助于识别镜像。 |
| `version_checks` | 每个镜像仓库在该日期和小时累计的版本检查次数。根据客户端，拉取可以进行版本检查以验证镜像或标签的存在而不下载它。 | 这有助于识别版本检查的频率，您可以用来分析使用趋势和潜在的意外行为。 |
| `pulls` | 每个镜像仓库在该日期和小时累计的拉取次数。 | 这有助于识别仓库拉取的频率，您可以用来分析使用趋势和潜在的意外行为。 |

## 查看拉取速率和限制

拉取速率限制按 6 小时计算。对于付费订阅的用户或自动化系统没有拉取速率限制。使用 Docker Hub 的未认证用户和 Docker Personal 用户将受到镜像拉取速率限制。

当您发出拉取请求且超过限制时，在请求清单时，Docker Hub 返回 `429` 响应代码，消息体如下：

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

此错误消息出现在 Docker CLI 或 Docker Engine 日志中。

要查看您当前的拉取速率和限制：

> [!NOTE]
>
> 要检查您的限制，您需要安装 `curl`、`grep` 和 `jq`。

1. 获取令牌。

   - 如果您匿名拉取，要匿名获取令牌：

      ```console
      $ TOKEN=$(curl "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
      ```

   - 如果您已认证，要使用用户账户获取令牌，请在以下命令中插入您的用户名和密码：

      ```console
      $ TOKEN=$(curl --user 'username:password' "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
      ```

2. 获取包含您限制的标头。这些标头在 GET 和 HEAD 请求上都会返回。使用 GET 模拟真实拉取并计入限制。使用 HEAD 则不会。


   ```console
   $ curl --head -H "Authorization: Bearer $TOKEN" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest
   ```

3. 检查标头。您应该会看到以下标头。

   ```text
   ratelimit-limit: 100;w=21600
   ratelimit-remaining: 20;w=21600
   docker-ratelimit-source: 192.0.2.1
   ```

   在上面的示例中，拉取限制是每 21600 秒（6 小时）100 次拉取，还剩余 20 次拉取。

   如果您没有看到任何 `ratelimit` 标头，可能是因为该镜像或您的 IP 与发布商、提供商或开源组织合作而不受限制。也可能意味着您拉取时使用的用户属于付费 Docker 订阅。如果您没有看到这些标头，拉取该镜像不会计入拉取速率限制。
