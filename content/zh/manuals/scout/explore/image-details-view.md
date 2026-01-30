---
title: 镜像详情视图
keywords: scout, 供应链, 漏洞, 软件包, cves, 镜像, 标签, 扫描, 分析
description: Docker Scout 镜像详情视图分析镜像以显示其层次结构、层、软件包和漏洞
aliases:
  - /scout/image-details-view
---

镜像详情视图显示了 Docker Scout 分析的细目。您可以从 Docker Scout 控制面板、Docker Desktop 的 **Images** 视图以及 Docker Hub 上的镜像标签页面访问该视图。镜像详情显示了镜像层次结构 (基础镜像)、镜像层、软件包和漏洞的细目。

![Docker Desktop 中的镜像详情视图](../images/dd-image-view.png)

Docker Desktop 首先在本地分析镜像，并在此生成软件物料清单 (SBOM)。Docker Desktop、Docker Hub、Docker Scout 控制面板和 CLI 都使用此 SBOM 中的 [软件包 URL (PURL) 链接](https://github.com/package-url/purl-spec) 在 [Docker Scout 的咨询数据库](/manuals/scout/deep-dive/advisory-db-sources.md) 中查询匹配的通用漏洞披露 (CVE)。

## 镜像层次结构

您检查的镜像可能在 **Image hierarchy** (镜像层次结构) 下有一个或多个基础镜像。这意味着镜像的作者在构建镜像时使用了其他镜像作为起点。通常，这些基础镜像要么是 Debian、Ubuntu 和 Alpine 等操作系统镜像，要么是 PHP、Python 和 Java 等编程语言镜像。

选择链中的每个镜像可以让您查看哪些层源自每个基础镜像。选择 **ALL** 行会选择所有层和基础镜像。

一个或多个基础镜像可能有可用更新，其中可能包含修复镜像漏洞的更新安全补丁。任何有可用更新的基础镜像都会在 **Image hierarchy** 的右侧注明。

## 层

Docker 镜像由层组成。镜像层从上到下列出，最早的层在顶部，最近的层在底部。通常，列表顶部的层源自基础镜像，而底部的层是由镜像作者添加的，通常使用 Dockerfile 中的命令。在 **Image hierarchy** 下选择基础镜像会突出显示源自基础镜像的层。

选择单个或多个层会过滤右侧的软件包和漏洞，以显示所选层添加的内容。

## 漏洞

**Vulnerabilities** (漏洞) 选项卡显示镜像中检测到的漏洞和利用列表。该列表按软件包分组，并按严重性排序。

您可以通过展开列表项找到有关漏洞或利用的更多信息，包括是否有可用的修复程序。

## 修复建议

当您在 Docker Desktop 或 Docker Hub 中检查镜像时，Docker Scout 可以提供提高该镜像安全性的建议。

### Docker Desktop 中的建议

要在 Docker Desktop 中查看镜像的安全建议：

1. 转到 Docker Desktop 中的 **Images** 视图。
2. 选择要查看建议的镜像标签。
3. 在靠近顶部的位置，选择 **Recommended fixes** 下拉按钮。

下拉菜单允许您选择是要查看当前镜像的建议，还是查看用于构建它的任何基础镜像的建议：

- [**Recommendations for this image**](#recommendations-for-current-image) (此镜像的建议) 为您正在检查的当前镜像提供建议。
- [**Recommendations for base image**](#recommendations-for-base-image) (基础镜像的建议) 为用于构建该镜像的基础镜像提供建议。

如果您查看的镜像没有关联的基础镜像，下拉菜单仅显示查看当前镜像建议的选项。

### Docker Hub 中的建议

要在 Docker Hub 中查看镜像的安全建议：

1. 转到已激活 Docker Scout 镜像分析的镜像仓库页面。
2. 打开 **Tags** 选项卡。
3. 选择要查看建议的镜像标签。
4. 选择 **View recommended base image fixes** 按钮。

   这将打开一个窗口，为您提供如何通过使用更好的基础镜像来提高镜像安全性的建议。有关更多详细信息，请参阅 [基础镜像建议](#recommendations-for-base-image)。

### 当前镜像的建议

当前镜像的建议视图可帮助您确定您使用的镜像版本是否已过时。如果您使用的标签引用的是旧摘要，该视图将显示建议通过拉取最新版本来更新标签。

选择 **Pull new image** 按钮以获取更新版本。勾选复选框可在拉取最新版本后删除旧版本。

### 基础镜像建议

基础镜像建议视图包含两个选项卡，用于在不同类型的建议之间切换：

- **Refresh base image** (刷新基础镜像)
- **Change base image** (更换基础镜像)

只有当您是所检查镜像的作者时，这些基础镜像建议才具有可操作性。这是因为更换镜像的基础镜像需要您更新 Dockerfile 并重新构建镜像。

#### 刷新基础镜像

此选项卡显示选定的基础镜像标签是否为最新的可用版本，或者是否已过时。

如果用于构建当前镜像的基础镜像标签不是最新的，则窗口中会显示这两个版本之间的差异。差异信息包括：

- 推荐 (更新) 版本的标签名称和别名
- 当前基础镜像版本的存在时间
- 最新可用版本的存在时间
- 影响每个版本的 CVE 数量

在窗口底部，您还会收到可以运行的命令片段，以便使用最新版本重新构建镜像。

#### 更换基础镜像

此选项卡显示了您可以使用的不同备选标签，并概述了每个标签版本的优缺点。选择基础镜像会显示该标签的推荐选项。

例如，如果您检查的镜像使用旧版本的 `debian` 作为基础镜像，它会显示推荐使用的更新且更安全的 `debian` 版本。通过提供多个备选方案供您选择，您可以亲自了解这些选项之间的比较，并决定使用哪一个。

![基础镜像建议](../images/change-base-image.png)

选择一个推荐标签以查看建议的更多详细信息。它会显示该标签的优点和潜在缺点、推荐原因以及如何更新 Dockerfile 以使用此版本。
