---
description: 了解如何使用桌面设置报告仪表板
keywords: Settings Management, docker desktop, hardened desktop, reporting, compliance
title: 桌面设置报告
linkTitle: 桌面设置报告
weight: 30
params:
  sidebar:
    badge:
      color: violet
      text: EA
---

{{< summary-bar feature_name="Compliance reporting" >}}

桌面设置报告（Desktop settings reporting）是桌面设置管理的一项功能，用于
跟踪和报告用户对分配给他们的设置策略的合规情况。这使管理员能够跟踪设置的应用情况，
并监控需要采取哪些措施来使用户合规。

本指南提供了访问桌面设置报告、查看合规状态以及解决不合规用户的步骤。

## 访问桌面设置报告

> [!IMPORTANT]
>
> 桌面设置报告处于早期访问（Early Access）阶段，正在逐步推出。
> 您可能暂时在 Admin Console 中看不到此设置。

1. 登录 [Docker Home](https://app.docker.com) 并选择
您的组织。
1. 选择 **Admin Console**，然后选择 **Desktop settings reporting**。

这将打开桌面设置报告页面。在此页面，您可以：

- 使用 **Search** 字段按用户名或电子邮件地址搜索
- 按策略筛选
- 隐藏或取消隐藏合规用户
- 查看用户的合规状态以及分配给用户的策略
- 下载用户合规信息的 CSV 文件

## 查看合规状态

> [!WARNING]
>
> 使用 Docker Desktop 4.40 之前版本的用户可能显示为不合规，
> 因为较旧版本无法报告合规性。为确保准确的
> 合规状态，用户必须更新到 Docker Desktop 4.40 及更高版本。

1. 登录 [Docker Home](https://app.docker.com) 并选择
您的组织。
1. 选择 **Admin Console**，然后选择 **Desktop settings reporting**。
1. 可选。选择 **Hide compliant users** 复选框以同时显示合规
和不合规用户。
1. 使用 **Search** 字段按用户名或电子邮件地址搜索。
1. 将鼠标悬停在用户的合规状态指示器上以快速查看其状态。
1. 选择用户名以查看有关其合规状态的更多详细信息，以及
解决不合规用户的步骤。

## 理解合规状态

Docker 根据以下内容评估合规状态：

- 合规状态：用户是否已获取并应用了最新设置。这是报告页面上显示的主要标签。
- 域状态：用户的电子邮件是否匹配已验证的域。
- 设置状态：是否已向用户应用设置策略。

这些状态的组合决定了您需要采取的措施。

### 合规状态参考

此参考解释了报告仪表板中如何根据用户域和设置数据确定每种状态。Admin Console 根据以下规则显示
最高优先级的适用状态。

**合规状态**

| 合规状态 | 含义 |
|-------------------|---------------|
| Uncontrolled domain | 用户的电子邮件域未经验证。 |
| No policy assigned | 用户没有分配任何策略。 |
| Non-compliant | 用户获取了正确的策略，但尚未应用。 |
| Outdated | 用户获取的是策略的旧版本。 |
| Compliant | 用户已获取并应用了最新分配的策略。 |

**域状态**

这反映了根据组织的域设置如何评估用户的电子邮件域。

| 域状态 | 含义 |
|---------------|---------------|
| Verified | 用户的电子邮件域已验证。 |
| Guest user | 用户的电子邮件域未经验证。 |
| Domainless | 您的组织没有已验证的域，用户的域未知。 |

**设置状态**

这显示用户是否以及如何被分配设置策略。

| 设置状态 | 含义 |
|-----------------|---------------|
| Global policy | 用户被分配了您组织的默认策略。 |
| User policy | 用户被分配了特定的自定义策略。 |
| No policy assigned | 用户未被分配任何策略。 |

## 解决合规状态

要解决合规状态，您必须通过从桌面设置报告页面选择用户名来查看用户的合规状态详情。
这些详情包括以下信息：

- **Compliance status**：指示用户是否符合应用于他们的设置
- **Domain status**：指示用户的电子邮件地址是否与已验证的域关联
- **Settings status**：指示用户是否已应用设置
- **Resolution steps**：如果用户不合规，这将提供有关如何解决用户合规状态的信息

### 合规

当用户合规时，桌面设置报告仪表板上其名称旁边会显示 **Compliant** 图标。选择合规用户以打开其
合规状态详情。合规用户具有以下状态详情：

- **Compliance status**：Compliant
- **Domain status**：Verified
- **Settings status**：Global policy 或 user policy
- **User is compliant** 指示器

合规用户无需解决步骤。

### 不合规

当用户不合规时，桌面设置报告仪表板上其名称旁边会显示 **Non-compliant** 或 **Unknown** 图标。不合规
用户必须解决其合规状态：

1. 从桌面设置报告仪表板选择用户名。
1. 在合规状态详情页面，按照提供的解决步骤
解决合规状态。
1. 刷新页面以确保解决步骤已解决合规
状态。
