---
title: 探索 Docker Hardened Images
linktitle: 探索镜像
description: 了解如何在 Docker Hub 上的 DHI 目录中查找和评估镜像仓库、变体、元数据和证明。
keywords: explore docker images, image variants, docker hub catalog, container image metadata, signed attestations
weight: 10
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

Docker Hardened Images（DHI）是一组精选的安全、生产就绪的容器镜像，专为企业使用而设计。本页说明如何探索可用的 DHI 仓库、查看镜像元数据、检查变体详情，以及了解提供的安全证明。使用此信息来评估和选择适合您应用的镜像变体，然后再将它们镜像到您的组织。

## 访问 Docker Hardened Images

Docker Hardened Images 需要订阅。[注册](https://www.docker.com/products/hardened-images/#getstarted)以访问 Docker Hardened Images。

## 探索 Docker Hardened Images

要探索 Docker Hardened Images（DHI）：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择有权访问 DHI 的组织。
4. 选择 **DHI catalog**。

在 DHI 页面上，您可以浏览镜像、搜索镜像或按类别筛选镜像。

## 查看仓库详情

要查看仓库详情：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择有权访问 DHI 的组织。
4. 选择 **DHI catalog**。
5. 在 DHI 目录列表中选择一个仓库。

仓库详情页面提供以下内容：

 - 概述：镜像的简要说明。
 - 指南：关于如何使用镜像和迁移现有应用的多个指南。
 - 标签：选择此选项以[查看镜像变体](#查看镜像变体)。
 - 安全摘要：选择标签名称以查看快速安全摘要，包括软件包数量、已知漏洞总数和 Scout 健康评分。
 - 最近推送的标签：最近更新的镜像变体列表及其最后更新时间。
 - 镜像到仓库：选择此选项将镜像镜像到您组织的仓库以便使用。只有组织所有者可以镜像仓库。
 - 在仓库中查看：仓库被镜像后，您可以选择此选项查看仓库已被镜像到的位置，或将其镜像到另一个仓库。

## 查看镜像变体

标签用于标识镜像变体。镜像变体是同一应用或框架针对不同用例定制的不同构建版本。

要探索镜像变体：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择有权访问 DHI 的组织。
4. 选择 **DHI catalog**。
5. 在 DHI 目录列表中选择一个仓库。
6. 选择 **Tags**。

**Tags** 页面提供以下信息：

- 标签：所有可用标签的列表，也称为镜像变体。
- 合规性：列出相关的合规认证。例如，`FIPS`。
- 发行版：变体所基于的发行版。例如，`debian 12` 或 `alpine 3.21`。
- 包管理器：变体中可用的包管理器。例如，`apt`、`apk` 或 `-`（无包管理器）。
- Shell：变体中可用的 shell。例如，`bash`、`busybox` 或 `-`（无 shell）。
- 用户：容器运行时使用的用户。例如，`root`、`nonroot (65532)` 或 `node (1000)`。
- 最后推送：镜像变体最后推送的天数。
- 漏洞：根据严重性统计的变体漏洞数量。
- 健康：变体的 Scout 健康评分。选择评分图标以获取更多详情。

> [!NOTE]
>
> 与 Docker Hub 上的大多数镜像不同，Docker Hardened Images 不使用 `latest` 标签。每个镜像变体都使用完整的语义版本标签发布（例如，`3.13`、`3.13-dev`）并保持最新。如果您需要固定到特定的镜像发布版本以实现可重复性，可以通过其[摘要](../core-concepts/digests.md)引用镜像。

## 查看镜像变体详情

要探索镜像变体的详情：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择有权访问 DHI 的组织。
4. 选择 **DHI catalog**。
5. 在 DHI 目录列表中选择一个仓库。
6. 选择 **Tags**。
7. 在表格中选择镜像变体的标签。

镜像变体详情页面提供以下信息：

- 软件包：镜像变体中包含的所有软件包列表。此部分包括每个软件包的详细信息，包括名称、版本、发行版和许可信息。
- 规格：镜像变体的规格包括以下关键详情：
   - 源代码和构建信息：镜像从此处找到的 Dockerfile 和 Git 提交构建。
   - 构建参数
   - Entrypoint
   - CMD
   - 用户
   - 工作目录
   - 环境变量
   - 标签
   - 平台
- 漏洞：漏洞部分提供镜像变体的已知 CVE 列表，包括：
   - CVE
   - 严重性
   - 软件包
   - 修复版本
   - 最后检测时间
   - 状态
   - 已抑制的 CVE
- 证明：变体包含全面的安全证明，用于验证镜像的构建过程、内容和安全状态。这些证明已签名，可以使用 cosign 进行验证。有关可用证明的列表，请参阅[证明](../core-concepts/attestations.md)。

## 接下来

找到所需的镜像后，您可以[将镜像镜像到您的组织](./mirror.md)。如果镜像已被镜像，则可以开始[使用镜像](./use.md)。
