---
title: 沟通与信息收集
description: 从关键利益相关者那里收集公司需求，并与开发人员沟通。
weight: 10
---

## 第一步：与开发人员和 IT 团队沟通

### Docker 用户沟通

您的公司内可能已经有 Docker Desktop 用户，此过程中的某些步骤可能会影响他们与平台的交互方式。强烈建议您尽早与用户沟通，告知他们作为订阅入门的一部分，他们将升级到受支持的 Docker Desktop 版本。

此外，请传达以下信息：设置将被审查以优化生产力，用户需要使用其企业电子邮件登录公司的 Docker 组织，以充分利用订阅权益。

### MDM 团队沟通

设备管理解决方案（如 Intune 和 Jamf）通常用于企业范围内的软件分发，通常由专门的 MDM 团队管理。建议您尽早与该团队接洽，了解他们的要求以及部署变更的前置时间。

本指南中的几个关键设置步骤需要使用 JSON 文件、注册表项或 .plist 文件，这些文件需要分发到开发人员机器。最佳实践是使用 MDM 工具来部署这些配置文件并确保其完整性。

## 第二步：确定 Docker 组织

一些公司可能创建了多个 [Docker 组织](/manuals/admin/organization/_index.md)。这些组织可能是为特定目的创建的，或者可能已不再需要。如果您怀疑公司有多个 Docker 组织，建议您调查您的团队，看看他们是否有自己的组织。您还可以联系 Docker 客户成功代表，获取其用户电子邮件与您的域名匹配的组织列表。

## 第三步：收集需求

通过[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)，Docker 提供了许多可以预设的配置参数。Docker 组织所有者、开发负责人和信息安全代表应审查这些设置，以建立公司的基准配置，包括安全功能和 Docker Desktop 用户的[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。此外，他们应该决定是否利用其他 Docker 产品，例如订阅中包含的 [Docker Scout](/manuals/scout/_index.md)。

要查看可以预设的参数，请参阅[配置设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md#step-two-configure-the-settings-you-want-to-lock-in)。

## 可选的第四步：与 Docker 实施团队会面

Docker 实施团队可以帮助您逐步完成组织设置、配置 SSO、强制登录和配置 Docker。您可以通过发送电子邮件至 successteam@docker.com 安排会议。
