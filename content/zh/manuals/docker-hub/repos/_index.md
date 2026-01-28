---
description: 了解如何在 Docker Hub 上管理仓库
keywords: Docker Hub, Hub, repositories
title: 仓库
weight: 20
aliases:
- /engine/tutorials/dockerrepos/
- /docker-hub/repos/configure/
---

Docker Hub 仓库（repository）是容器镜像的集合，使您能够公开或私密地存储、管理和共享 Docker 镜像。每个仓库都是一个专用空间，您可以在其中存储与特定应用程序、微服务或项目相关的镜像。仓库中的内容按标签组织，标签代表同一应用程序的不同版本，允许用户在需要时拉取正确的版本。

在本节中，了解如何：

- [创建](./create.md)仓库。
- 管理仓库，包括如何管理：

   - [仓库信息](./manage/information.md)：添加描述、概述和类别，帮助用户了解仓库的用途和使用方法。清晰的仓库信息有助于提高可发现性和可用性。

   - [访问控制](./manage/access.md)：通过灵活的选项控制谁可以访问您的仓库。将仓库设为公开或私有，添加协作者，对于组织，还可以管理角色和团队以维护安全性和控制。

   - [镜像](./manage/hub-images/_index.md)：仓库支持多种内容类型，包括 OCI 制品，并允许通过标记进行版本控制。推送新镜像并管理跨仓库的现有内容以获得灵活性。

   - [镜像安全洞察](./manage/vulnerability-scanning.md)：利用持续的 Docker Scout 分析和静态漏洞扫描来检测、理解和解决容器镜像中的安全问题。

   - [Webhooks](./manage/webhooks.md)：通过设置 webhooks 自动响应仓库事件（如镜像推送或更新），这可以触发外部系统中的通知或操作，简化工作流程。

   - [自动构建](./manage/builds/_index.md)：与 GitHub 或 Bitbucket 集成以实现自动构建。每次代码更改都会触发镜像重建，支持持续集成和交付。

   - [可信内容](./manage/trusted-content/_index.md)：为 Docker 官方镜像做贡献，或管理 Verified Publisher 和 Sponsored Open Source 计划中的仓库，包括设置徽标、访问分析和启用漏洞扫描等任务。

- [归档](./archive.md)过时或不再支持的仓库。
- [删除](./delete.md)仓库。
- [管理个人设置](./settings.md)：对于您的账户，您可以设置仓库的个人设置，包括默认仓库隐私和自动构建通知。
