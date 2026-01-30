---
description: Docker Scout 控制面板有助于查看和共享镜像分析结果。
keywords: scout, 扫描, 分析, 漏洞, Hub, 供应链, 安全, 报告, 控制面板
title: 控制面板
aliases:
- /scout/reports/
- /scout/web-app/
- /scout/dashboard/
---

[Docker Scout 控制面板](https://scout.docker.com/) 可帮助您与团队共享组织中镜像的分析结果。开发人员现在可以查看其在 Docker Hub 中所有镜像的安全状态概览，并触手可及地获得修复建议。它有助于安全、合规和运营等角色的团队成员了解他们需要关注哪些漏洞和问题。

## 概览

![Docker Scout 控制面板概览截图](../images/dashboard-overview.webp?border=true)

**Overview** (概览) 选项卡提供了所选组织中仓库的摘要。

在此页面的顶部，您可以选择要查看的 **Environment** (环境)。默认情况下，显示最近推送的镜像。要了解有关环境的更多信息，请参阅 [环境监控](/manuals/scout/integrations/environment/_index.md)。

**Policy** (策略) 框显示您当前针对每项策略的合规性评级，以及所选环境的趋势指示。趋势描述了最新镜像与先前版本相比的策略增量。有关策略的更多信息，请参阅 [策略评估](/manuals/scout/policy/_index.md)。

漏洞图表显示了所选环境中镜像的漏洞总数随时间的变化情况。您可以使用下拉菜单配置图表的时间范围。

使用网站顶部的标题菜单访问 Docker Scout 控制面板的不同主要部分：

- **Policies**: 显示组织的策略合规情况，见 [策略](#policies)
- **Images**: 列出组织中所有启用了 Docker Scout 的仓库，见 [镜像](#images)
- **Base images**: 列出组织中仓库使用的所有基础镜像
- **Packages**: 列出组织中跨仓库的所有软件包
- **Vulnerabilities**: 列出组织镜像中的所有 CVE，见 [漏洞](#vulnerabilities)
- **Integrations**: 创建和管理第三方集成，见 [集成](#integrations)
- **Settings**: 管理仓库设置，见 [设置](#settings)

## 策略

**Policies** (策略) 视图显示了所选组织和环境中所有镜像的策略合规情况细目。您可以使用 **Image** 下拉菜单查看特定环境的策略细目。

有关策略的更多信息，请参阅 [策略评估](/manuals/scout/policy/_index.md)。

## 镜像

**Images** (镜像) 视图显示所选环境中启用 Scout 的仓库中的所有镜像。您可以通过选择不同的环境或使用文本过滤器按仓库名称过滤列表。

![镜像视图截图](../images/dashboard-images.webp)

对于每个仓库，列表显示以下详细信息：

- 仓库名称 (不带标签或摘要的镜像引用)
- 所选环境中镜像的最新标签
- 最新标签的操作系统和架构
- 最新标签的漏洞状态
- 最新标签的策略状态

选择仓库链接将带您进入该仓库中已分析的所有镜像列表。在此处，您可以查看特定镜像的完整分析结果，并比较标签以查看软件包和漏洞的差异。

选择镜像链接将带您进入所选标签或摘要的详情视图。此视图包含两个选项卡，详细说明了镜像的组成和策略合规情况：

- **Policy status** 显示所选镜像的策略评估结果。此处还有指向策略冲突详情的链接。

  有关策略的更多信息，请参阅 [策略评估](/manuals/scout/policy/_index.md)。

- **Image layers** 显示镜像分析结果的细目。您可以完整查看镜像包含的漏洞，并了解它们是如何进入镜像的。

## 漏洞

**Vulnerabilities** (漏洞) 视图显示组织中镜像的所有漏洞列表。此列表包含有关 CVE 的详细信息，例如严重性和通用漏洞评分系统 (CVSS) 评分，以及是否有可用的修复版本。此处显示的 CVSS 评分是所有可用 [源](/manuals/scout/deep-dive/advisory-db-sources.md) 中的最高分。

选择此页面上的链接将打开漏洞详情页面。此页面是公开可见的，显示有关 CVE 的详细信息。您可以与其他人员分享特定 CVE 描述的链接，即使他们不是您 Docker 组织的成员或未登录 Docker Scout。

如果您已登录，此页面上的 **My images** 选项卡会列出受该 CVE 影响的所有镜像。

## 集成

**Integrations** (集成) 页面允许您创建和管理 Docker Scout 集成，例如环境集成和注册表集成。有关如何开始使用集成的更多信息，请参阅 [将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

## 设置

Docker Scout 控制面板中的设置菜单包含：

- [**Repository settings**](#repository-settings) (仓库设置)，用于启用和禁用仓库
- [**Notifications**](#notification-settings) (通知)，用于管理您的 Docker Scout 通知首选项。

### 仓库设置

当您为仓库启用 Docker Scout 时，Docker Scout 会在您推送至该仓库时自动分析新标签。要启用 Amazon ECR、Azure ACR 或其他第三方注册表中的仓库，您首先需要集成它们。参见 [容器注册表集成](/manuals/scout/integrations/_index.md#container-registries)

### 通知设置

[通知设置](https://scout.docker.com/settings/notifications) 页面是您可以更改接收来自 Docker Scout 通知首选项的地方。通知设置是个人化的，更改通知设置仅影响您的个人帐户，而不会影响整个组织。

Docker Scout 中通知的目的是提高对影响您的上游更改的意识。当安全公告中披露新的漏洞且该漏洞影响您的一个或多个镜像时，Docker Scout 会通知您。您不会因为推送新镜像而收到有关漏洞暴露或策略合规性更改的通知。

> [!NOTE]
>
> 仅针对每个仓库 *最后推送* 的镜像标签触发通知。“最后推送”是指最近推送到注册表并由 Docker Scout 分析的镜像标签。如果最后推送的镜像不受新披露的 CVE 影响，则不会触发通知。

可用的通知设置有：

- **Repository scope** (仓库范围)

  在此处，您可以选择是要启用所有仓库的通知，还是仅启用特定仓库的通知。这些设置适用于当前选定的组织，并且可以为您作为成员的每个组织进行更改。

  - **All repositories**: 选择此选项可接收您有权访问的所有仓库的通知。
  - **Specific repositories**: 选择此选项可接收特定仓库的通知。然后，您可以输入要接收通知的仓库名称。

- **Delivery preferences** (递送首选项)

  这些设置控制您接收来自 Docker Scout 通知的方式。它们适用于您作为成员的所有组织。

  - **Notification pop-ups**: 选中此复选框可在 Docker Scout 控制面板中接收通知弹出消息。
  - **OS notifications**: 选中此复选框可从浏览器接收操作系统级别的通知 (如果您在浏览器选项卡中打开了 Docker Scout 控制面板)。
  
  要启用操作系统通知，Docker Scout 需要权限才能使用浏览器 API 发送通知。

在此页面中，您还可以转到团队协作集成的设置，例如 [Slack](/manuals/scout/integrations/team-collaboration/slack.md) 集成。

您也可以在 Docker Desktop 中通过转到 **Settings** > **Notifications** 来配置您的通知设置。
