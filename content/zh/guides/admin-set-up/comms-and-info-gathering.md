---
title: 沟通和信息收集
description: 从关键利益相关者那里收集公司的需求，并与你的开发人员进行沟通。
weight: 10
---

## 第一步：与你的开发人员和 IT 团队沟通

### Docker 用户沟通

你的公司内部可能已经有 Docker Desktop 用户，此过程中的某些步骤可能会影响他们与平台的交互方式。强烈建议尽早与用户沟通，告知他们作为订阅入门的一部分，他们将被升级到受支持的 Docker Desktop 版本。

此外，还要告知他们将审查设置以优化生产力，并且用户需要使用其企业电子邮件登录公司的 Docker 组织，以充分利用订阅权益。

### MDM 团队沟通

设备管理解决方案（例如 Intune 和 Jamf）通常用于在企业范围内分发软件，通常由专门的 MDM 团队管理。建议你在此过程的早期与该团队联系，以了解他们的要求和部署更改的准备时间。

本指南中的几个关键设置步骤需要使用 JSON 文件、注册表项或 .plist 文件，这些文件需要分发到开发人员计算机。最佳实��是使用 MDM 工具来部署这些配置文件并确保其完整性得到保留。

## 第二步：识别 Docker 组织

一些公司可能创建了多个 [Docker 组织](/manuals/admin/organization/_index.md)。这些组织可能是为特定目的而创建的，或者可能不再需要。如果你怀疑你的公司有多个 Docker 组织，建议你调查你的团队，看看他们是否有自己的组织。你还可以联系你的 Docker 客户成功代表，以获取其电子邮件与你的域名匹配的用户的组织列表。

## 第三步：收集需求

通过[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)，Docker 提供了许多可以预设的配置参数。Docker 组织所有者、开发负责人和信息安全代表应审查这些设置，以建立公司的基线配置，包括安全功能和为 Docker Desktop 用户[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。此外，他们还应决定是否利用其他 Docker 产品，例如订阅中包含的 [Docker Scout](/manuals/scout/_index.md)。

要查看可以预设的参数，请参阅[配置设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md#step-two-configure-the-settings-you-want-to-lock-in)。

## 可选的第四步：与 Docker 实施团队会面

Docker ��施团队可以帮助你逐步完成组织设置、配置 SSO、强制登录和配置 Docker。你可以通过发送电子邮件至 successteam@docker.com 来安排会议。
