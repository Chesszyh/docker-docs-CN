---
title: 镜像 Docker Hardened Image 仓库
linktitle: 镜像镜像
description: 了解如何将镜像镜像到您组织的命名空间，并可选择推送到另一个私有镜像仓库。
weight: 20
keywords: mirror docker image, private container registry, docker hub automation, webhook image sync, secure image distribution
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

在使用 Docker Hardened Image（DHI）之前，您必须将其仓库镜像到您的组织。只有组织所有者可以执行此操作。镜像完成后，镜像将在您组织的命名空间中可用，有访问权限的用户可以开始拉取和使用它。

镜像的仓库会自动保持最新。Docker 会继续从上游 DHI 目录同步新标签和镜像更新，因此您始终可以访问最新的安全版本。

## 前提条件

- 要管理镜像，您必须是[组织所有者](/admin/)。
- 您的组织必须已[注册](https://www.docker.com/products/hardened-images/#getstarted)使用 Docker Hardened Images。

## 镜像镜像仓库

要镜像 Docker Hardened Image 仓库：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择有权访问 DHI 的组织。
4. 选择 **DHI catalog**。
5. 选择一个 DHI 仓库以查看其详情。
6. 选择 **Mirror to repository** 并按照屏幕上的说明操作。


所有标签完成镜像可能需要几分钟时间。镜像完成后，**Mirror to repository** 按钮会变为 **View in repository**。选择 **View in repository** 会打开一个下拉列表，显示镜像已被镜像到的仓库。从这个下拉菜单中，您可以：

 - 选择现有的镜像仓库以查看其详情
 - 再次选择 **Mirror to repository** 将镜像镜像到其他仓库

镜像仓库后，该仓库会出现在您组织的仓库列表中，名称为您指定的名称，前缀为 `dhi-`。它将继续接收更新的镜像。

![Repository list with mirrored repository showing](../images/dhi-python-mirror.png)

> [!IMPORTANT]
>
> 镜像仓库的可见性必须保持私有。将其可见性更改为公开将停止镜像更新。

镜像完成后，镜像仓库的工作方式与 Docker Hub 上的任何其他私有仓库相同。有权访问该仓库的团队成员现在可以拉取和使用镜像。要了解如何管理访问、查看标签或配置设置，请参阅[仓库](/manuals/docker-hub/repos.md)。

### 用于同步和告警的 Webhook 集成

要使外部镜像仓库或系统与您镜像的 Docker Hardened Images 保持同步，并在更新发生时接收通知，您可以在 Docker Hub 上的镜像仓库上配置 [webhook](/docker-hub/repos/manage/webhooks/)。每当推送或更新新的镜像标签时，webhook 都会向您定义的 URL 发送 `POST` 请求。

例如，您可以配置一个 webhook，在每次镜像新标签时调用 CI/CD 系统的 `https://ci.example.com/hooks/dhi-sync`。此 webhook 触发的自动化可以从 Docker Hub 拉取更新的镜像，并将其推送到内部镜像仓库，如 Amazon ECR、Google Artifact Registry 或 GitHub Container Registry。

其他常见的 webhook 用例包括：

- 触发验证或漏洞扫描工作流
- 签名或提升镜像
- 向下游系统发送通知

#### 示例 webhook 负载

当 webhook 被触发时，Docker Hub 会发送如下 JSON 负载：

```json
{
  "callback_url": "https://registry.hub.docker.com/u/exampleorg/dhi-python/hook/abc123/",
  "push_data": {
    "pushed_at": 1712345678,
    "pusher": "trustedbuilder",
    "tag": "3.13-alpine3.21"
  },
  "repository": {
    "name": "dhi-python",
    "namespace": "exampleorg",
    "repo_name": "exampleorg/dhi-python",
    "repo_url": "https://hub.docker.com/r/exampleorg/dhi-python",
    "is_private": true,
    "status": "Active",
    ...
  }
}
```

## 停止镜像镜像仓库

只有组织所有者可以停止镜像仓库。停止镜像后，仓库会保留，但不会再接收更新。您仍然可以拉取最后镜像的镜像，但仓库不会从原始仓库接收新标签或更新。

 要停止镜像镜像仓库：

1. 前往您组织命名空间中的镜像仓库。
2. 选择 **Stop mirroring**。

停止镜像仓库后，您可以选择另一个 DHI 仓库进行镜像。

## 从 Docker Hub 镜像到另一个镜像仓库

将 Docker Hardened Image 仓库镜像到您组织在 Docker Hub 上的命名空间后，您可以选择将其镜像到另一个容器镜像仓库，如 Amazon ECR、Google Artifact Registry、GitHub Container Registry 或私有 Harbor 实例。

您可以使用任何标准工作流，包括：

- [Docker CLI](/reference/cli/docker/_index.md)
- [Docker Hub Registry API](/reference/api/registry/latest/)
- 第三方镜像仓库工具或 CI/CD 自动化

以下示例展示了如何使用 Docker CLI 拉取镜像的 DHI 并推送到另一个镜像仓库：

```console
# Authenticate to Docker Hub (if not already signed in)
$ docker login

# Pull the image from your organization's namespace on Docker Hub
$ docker pull <your-namespace>/dhi-<image>:<tag>

# Tag the image for your destination registry
$ docker tag <your-namespace>/dhi-<image>:<tag> registry.example.com/my-project/<image>:<tag>

# Push the image to the destination registry
# You will need to authenticate to the third-party registry before pushing
$ docker push registry.example.com/my-project/<image>:<tag>
```

> [!IMPORTANT]
>
> 为了继续接收镜像更新并保留对 Docker Hardened Images 的访问权限，请确保推送到其他镜像仓库的任何副本保持私有。

### 镜像时包含证明

Docker Hardened Images 已签名并包含相关证明，这些证明提供构建来源和漏洞扫描结果等元数据。这些证明存储为 OCI 制品，使用 Docker CLI 镜像镜像时默认不包含。

要在将 DHI 复制到另一个镜像仓库时保留完整的安全上下文，您必须显式包含证明。一个工具是 `regctl`，它支持复制镜像及其关联的制品。

有关如何使用 `regctl` 复制镜像及其关联制品的更多详情，请参阅 [regclient 文档](https://regclient.org/cli/regctl/image/copy/)。

## 接下来

镜像镜像仓库后，您可以开始[使用镜像](./use.md)。
