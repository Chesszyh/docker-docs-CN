---
description: 了解如何管理 Docker Hub 仓库中的镜像
keywords: Docker Hub, Hub, images, content
title: 镜像管理
linkTitle: 镜像
weight: 60
---

Docker Hub 提供了强大的功能来管理和组织您的仓库内容，确保您的镜像和制品可访问、版本可控且易于共享。本节涵盖关键的镜像管理任务，包括标签管理、推送镜像、在仓库之间转移镜像以及支持的软件制品。


- [标签](./tags.md)：标签帮助您在单个仓库中对镜像的不同迭代进行版本控制和组织。本主题解释了标签的概念，并提供了如何在 Docker Hub 中创建、查看和删除标签的指导。
- [镜像管理](./manage.md)：管理您的镜像和镜像索引以优化仓库存储。
- [软件制品](./oci-artifacts.md)：Docker Hub 支持 OCI（Open Container Initiative，开放容器倡议）制品，允许您存储、管理和分发标准 Docker 镜像之外的一系列内容，包括 Helm charts、漏洞报告等。本节提供了 OCI 制品的概述以及将其推送到 Docker Hub 的一些示例。
- [推送镜像到 Hub](./push.md)：Docker Hub 使您能够将本地镜像推送到其中，使其可供您的团队或 Docker 社区使用。了解如何配置您的镜像并使用 `docker push` 命令将其上传到 Docker Hub。
- [在仓库之间移动镜像](./move.md)：在不同仓库之间组织内容可以帮助简化协作和资源管理。本主题详细介绍了如何将镜像从一个 Docker Hub 仓库移动到另一个仓库，无论是用于个人整合还是与组织共享镜像。
