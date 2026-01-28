---
title: 停用组织
description: 了解如何停用 Docker 组织。
keywords: Docker Hub, delete, deactivate organization, account, organization management
weight: 42
aliases:
- /docker-hub/deactivate-account/
---

{{< summary-bar feature_name="General admin" >}}

您可以随时停用帐户。本节介绍停用组织帐户的前提条件和步骤。有关停用用户帐户的信息，请参阅[停用用户帐户](../../accounts/deactivate-user-account.md)。

> [!WARNING]
>
> 停用帐户后，所有使用您的 Docker 帐户或组织帐户的 Docker 产品和服务都将无法访问。

## 前提条件

在停用组织之前，请完成以下操作：

- 下载您想要保留的任何镜像和标签：
  `docker pull -a <image>:<tag>`。
- 如果您有活跃的 Docker 订阅，请[将其降级为免费订阅](../../subscription/change.md)。
- 移除组织内的所有其他成员。
- 取消关联您的 [Github 和 Bitbucket 帐户](../../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account)。
- 对于 Business 组织，[移除您的 SSO 连接](../../security/for-admins/single-sign-on/manage/#remove-an-organization)。

## 停用

完成所有上述步骤后，您可以停用您的组织。

> [!WARNING]
>
> 此操作无法撤销。请确保在停用组织之前已从组织中收集了所有需要的数据。

{{< tabs >}}
{{< tab name="Admin Console" >}}

1. 登录 [Docker Home](https://app.docker.com) 并选择您要停用的组织。
1. 选择 **Admin Console**，然后选择 **Deactivate**。如果此按钮显示为灰色，您必须完成[前提条件](#前提条件)。
1. 输入组织名称以确认停用。
1. 选择 **Deactivate organization**。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您要停用的组织。
1. 在 **Settings** 中，选择 **Deactivate org**。
1. 选择 **Deactivate organization**。

{{< /tab >}}
{{< /tabs >}}
