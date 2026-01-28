---
description: 了解 Docker 认证发布者计划及其运作方式
title: Docker 认证发布者计划
aliases:
- /docker-hub/publish/publish/
- /docker-hub/publish/customer_faq/
- /docker-hub/publish/publisher_faq/
- /docker-hub/publish/certify-images/
- /docker-hub/publish/certify-plugins-logging/
- /docker-hub/publish/trustchain/
- /docker-hub/publish/byol/
- /docker-hub/publish/publisher-center-migration/
- /docker-hub/publish/
- /docker-hub/publish/repository-logos/
- /docker-hub/dvp-program/
- /trusted-content/dvp-program/
---

[Docker 认证发布者计划](https://hub.docker.com/search?q=&image_filter=store) 提供由 Docker 验证的商业发布者提供的高质量镜像。

这些镜像帮助开发团队构建安全的软件供应链，在流程早期最大限度地减少对恶意内容的暴露，从而在后期节省时间和金钱。

属于此计划的镜像在 Docker Hub 上有一个特殊徽章，使用户更容易识别 Docker 已验证为高质量商业发布者的项目。

![Docker-Sponsored Open Source badge](../../../images/verified-publisher-badge-iso.png)

Docker 认证发布者计划 (DVP) 为 Docker Hub 发布者提供多项功能和福利。该计划根据参与层级授予以下特权：

- 仓库徽标
- 认证发布者徽章
- Docker Hub 搜索优先排名
- 洞察与分析
- 漏洞分析
- 额外的 Docker Business 席位
- 为开发者移除速率限制
- 联合营销机会

### 仓库徽标

DVP 组织可以为 Docker Hub 上的单个仓库上传自定义图像。这允许您在每个仓库的基础上覆盖默认的组织级徽标。

只有对仓库具有管理权限（所有者或具有管理员权限的团队成员）的用户才能更改仓库徽标。

#### 图像要求

- 徽标图像支持的文件类型为 JPEG 和 PNG。
- 允许的最小图像尺寸（像素）为 120×120。
- 允许的最大图像尺寸（像素）为 1000×1000。
- 允许的最大图像文件大小为 5MB。

#### 设置仓库徽标

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 转到您想要更改徽标的仓库页面。
3. 选择上传徽标按钮，由覆盖在当前仓库徽标上的相机图标 ({{< inline-image
   src="../../../images/upload_logo_sm.png" alt="camera icon" >}}) 表示。
4. 在打开的对话框中，选择您要上传的 PNG 图像以将其设置为仓库的徽标。

#### 移除徽标

选择 **Clear** 按钮 ({{< inline-image src="../../../images/clear_logo_sm.png"
alt="clear button" >}}) 以移除徽标。

移除徽标会使仓库默认使用组织徽标（如果已设置），否则使用以下默认徽标。

![Default logo which is a 3D grey cube](../../../images/default_logo_sm.png)

### 认证发布者徽章

属于此计划的镜像在 Docker Hub 上有一个徽章，使开发者更容易识别 Docker 已验证为高质量发布者且内容可信赖的项目。

![Docker, Inc. org with a verified publisher badge](../../../images/verified-publisher-badge.png)

### 洞察与分析

[洞察与分析](./insights-analytics.md) 服务提供社区如何使用 Docker 镜像的使用指标，让您深入了解用户行为。

使用指标显示按标签或按摘要的镜像拉取次数，以及按地理位置、云提供商、客户端等的细分。

您可以选择要查看分析数据的时间跨度。您还可以以摘要或原始格式导出数据。

### 漏洞分析

[Docker Scout](/scout/) 为发布到 Docker Hub 的 DVP 镜像提供自动漏洞分析。扫描镜像可确保发布的内容是安全的，并向开发者证明他们可以信任该镜像。

您可以在每个仓库的基础上启用分析。有关使用此功能的更多信息，请参阅 [基本漏洞扫描](/docker-hub/repos/manage/vulnerability-scanning/)。

### 谁有资格成为认证发布者？

任何在 Docker Hub 上分发软件的独立软件供应商都可以加入认证发布者计划。前往 [Docker 认证发布者计划](https://www.docker.com/partners/programs) 页面了解更多信息。
