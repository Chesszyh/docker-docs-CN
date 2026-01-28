---
description: 了解 Docker 赞助开源计划及其运作方式
title: Docker 赞助开源计划
keywords: docker hub, hub, insights, analytics, open source, Docker sponsored, program
aliases:
  - /docker-hub/dsos-program/
  - /trusted-content/dsos-program/
---

[Docker 赞助开源镜像](https://hub.docker.com/search?q=&image_filter=open_source) 由通过该计划获得 Docker 赞助的开源项目发布和维护。

属于此计划的镜像在 Docker Hub 上有一个特殊徽章，使用户更容易识别 Docker 已验证为受信任、安全且活跃的开源项目。

![Docker-Sponsored Open Source badge](../../../images/sponsored-badge-iso.png)

Docker 赞助开源 (DSOS) 计划为非商业性开源开发者提供多项功能和福利。

该计划向符合条件的项目授予以下特权：

- 仓库徽标
- 认证的 Docker 赞助开源徽章
- 洞察与分析
- 访问 [Docker Scout](#docker-scout) 进行软件供应链管理
- 为开发者移除速率限制
- 在 Docker Hub 上提高可发现性

这些福利有效期为一年，如果项目仍然满足计划要求，发布者可以每年续订。计划成员和所有从项目命名空间拉取公共镜像的用户都可以获得无限制的拉取和无限制的出口流量。

### 仓库徽标

DSOS 组织可以为 Docker Hub 上的单个仓库上传自定义图像。这允许您在每个仓库的基础上覆盖默认的组织级徽标。

只有对仓库具有管理权限（所有者或具有管理员权限的团队成员）的用户才能更改仓库徽标。

#### 图像要求

- 徽标图像支持的文件类型为 JPEG 和 PNG。
- 允许的最小图像尺寸（像素）为 120×120。
- 允许的最大图像尺寸（像素）为 1000×1000。
- 允许的最大图像文件大小为 5MB。

#### 设置仓库徽标

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 转到您想要更改徽标的仓库页面。
3. 选择上传徽标按钮，由覆盖在当前仓库徽标上的相机图标表示
   ({{< inline-image src="../../../images/upload_logo_sm.png" alt="camera icon" >}})。
4. 在打开的对话框中，选择您要上传的 PNG 图像以将其设置为仓库的徽标。

#### 移除徽标

选择 **Clear** 按钮 ({{< inline-image src="../../../images/clear_logo_sm.png"
alt="clear button" >}}) 以移除徽标。

移除徽标会使仓库默认使用组织徽标（如果已设置），否则使用以下默认徽标。

![Default logo which is a 3D grey cube](../../../images/default_logo_sm.png)

### 认证的 Docker 赞助开源徽章

Docker 验证开发者可以信任 Docker Hub 上带有此徽章的镜像，将其视为活跃的开源项目。

![Fluent org with a Docker-Sponsored Open Source badge](../../../images/sponsored-badge.png)

### 洞察与分析

[洞察与分析](/docker-hub/publish/insights-analytics) 服务提供社区如何使用 Docker 镜像的使用指标，让您深入了解用户行为。

使用指标显示按标签或按摘要的镜像拉取次数，以及按地理位置、云提供商、客户端等的细分。

您可以选择要查看分析数据的时间跨度。您还可以以摘要或原始格式导出数据。

### Docker Scout

DSOS 项目最多可以免费在 100 个仓库上启用 Docker Scout。Docker Scout 提供自动镜像分析、改进供应链管理的策略评估、与 CI 平台和源代码管理等第三方系统的集成等功能。

您可以在每个仓库的基础上启用 Docker Scout。有关如何使用此产品的信息，请参阅 [Docker Scout 文档](/scout/)。

### 谁有资格参加 Docker 赞助开源计划？

要符合该计划的资格，发布者必须在公共仓库中共享项目命名空间，符合 [开源倡议定义](https://opensource.org/docs/osd)，并且处于活跃开发状态且没有商业化途径。

前往 [Docker 赞助开源计划](https://www.docker.com/community/open-source/application/) 申请页面了解更多信息。
