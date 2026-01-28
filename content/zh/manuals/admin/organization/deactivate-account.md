---
title: 停用组织
description: 了解如何停用 Docker 组织。
keywords: Docker Hub, 删除, 停用组织, 账户, 组织管理
weight: 42
aliases:
- /docker-hub/deactivate-account/
---

{{< summary-bar feature_name="通用管理" >}}

您可以随时停用账户。本节介绍了停用组织账户的前提条件和步骤。有关停用用户账户的信息，请参阅 [停用用户账户](../../accounts/deactivate-user-account.md)。

> [!WARNING]
>
> 停用账户后，所有使用您 Docker 账户或组织账户的 Docker 产品和服务都将无法访问。

## 前提条件

在停用组织之前，请完成以下操作：

- 下载任何您想保留的镜像和标签：
  `docker pull -a <image>:<tag>`。
- 如果您有活跃的 Docker 订阅，请将其 [降级为免费订阅](../../subscription/change.md)。
- 移除组织内的所有其他成员。
- 取消关联您的 [Github 和 Bitbucket 账户](../../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account)。
- 对于 Business 组织，请 [移除您的 SSO 连接](../../security/for-admins/single-sign-on/manage/#remove-an-organization)。

## 停用

完成上述所有步骤后，您可以停用组织。

> [!WARNING]
>
> 此操作不可撤销。请务必在停用组织之前收集好您需要的所有数据。

{{< tabs >}}
{{< tab name="管理控制台" >}}

1. 登录 [Docker Home](https://app.docker.com) 并选择您要停用的组织。
2. 选择 **Admin Console**（管理控制台），然后选择 **Deactivate**（停用）。如果此按钮为灰色，则必须先完成 [前提条件](#prerequisites)。
3. 输入组织名称以确认停用。
4. 选择 **Deactivate organization**（停用组织）。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您要停用的组织。
3. 在 **Settings**（设置）中，选择 **Deactivate org**（停用组织）。
4. 选择 **Deactivate organization**（停用组织）。

{{< /tab >}}
{{< /tabs >}}
