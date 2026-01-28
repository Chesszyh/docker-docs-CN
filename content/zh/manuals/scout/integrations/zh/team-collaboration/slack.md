---
title: 将 Docker Scout 与 Slack 集成
linkTitle: Slack
description: |
  将 Docker Scout 与 Slack 集成，在 Slack 频道中接收有关漏洞和策略合规性的实时更新
keywords: scout, team collaboration, slack, notifications, updates
---

您可以通过创建 Slack webhook 并将其添加到 Docker Scout Dashboard 来将 Docker Scout 与 Slack 集成。当发现新漏洞并且影响到您的一个或多个镜像时，Docker Scout 会通知您。

![Slack notification from Docker Scout](../../images/scout-slack-notification.png?border=true "Example Slack notification from Docker Scout")

## 工作原理

配置集成后，Docker Scout 会向与 webhook 关联的 Slack 频道发送有关您仓库的策略合规性和漏洞暴露变化的通知。

> [!NOTE]
>
> 通知仅针对每个仓库*最后推送*的镜像标签触发。"最后推送"是指最近推送到仓库并由 Docker Scout 分析的镜像标签。如果最后推送的镜像未受到新披露的 CVE 影响，则不会触发通知。

有关 Docker Scout 通知的更多信息，请参阅[通知设置](/manuals/scout/explore/dashboard.md#notification-settings)。

## 设置

要添加 Slack 集成：

1. 创建一个 webhook，请参阅 [Slack 文档](https://api.slack.com/messaging/webhooks)。
2. 前往 Docker Scout Dashboard 上的 [Slack 集成页面](https://scout.docker.com/settings/integrations/slack/)。
3. 在 **How to integrate** 部分，输入一个 **Configuration name**。Docker Scout 使用此标签作为集成的显示名称，因此您可能希望将默认名称更改为更有意义的名称。例如 `#channel-name`，或此配置所属团队的名称。
4. 将您刚刚创建的 webhook 粘贴到 **Slack webhook** 字段中。

   如果您想验证连接，请选择 **Test webhook** 按钮。Docker Scout 将向指定的 webhook 发送一条测试消息。

5. 选择是要为所有启用 Scout 的镜像仓库启用通知，还是输入要发送通知的仓库名称。
6. 准备好启用集成时，选择 **Create**。

创建 webhook 后，Docker Scout 开始向与 webhook 关联的 Slack 频道发送通知更新。

## 移除 Slack 集成

要移除 Slack 集成：

1. 前往 Docker Scout Dashboard 上的 [Slack 集成页面](https://scout.docker.com/settings/integrations/slack/)。
2. 选择要移除的集成的 **Remove** 图标。
3. 在确认对话框中再次选择 **Remove** 确认。
