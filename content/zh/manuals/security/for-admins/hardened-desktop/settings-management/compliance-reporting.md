---
description: 了解如何使用 Desktop 设置报告仪表板
keywords: 设置管理, Settings Management, docker desktop, hardened desktop, reporting, compliance, 合规性
title: Desktop 设置报告
linkTitle: Desktop 设置报告
weight: 30
params:
  sidebar:
    badge:
      color: violet
      text: EA
---

{{< summary-bar feature_name="合规性报告" >}}

Desktop 设置报告是 Desktop 设置管理的一项功能，用于跟踪并报告用户对其分配的设置策略的合规情况。这让管理员能够跟踪设置的应用情况，并监控需要采取哪些行动来使用户合规。

本指南提供了访问 Desktop 设置报告、查看合规状态以及解决非合规用户问题的步骤。

## 访问 Desktop 设置报告

> [!IMPORTANT]
>
> Desktop 设置报告目前处于早期访问阶段（Early Access），并正在逐步推广。您可能尚未在管理控制台（Admin Console）中看到此设置。

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
2. 选择 **Admin Console（管理控制台）**，然后选择 **Desktop settings reporting（Desktop 设置报告）**。

这将打开 Desktop 设置报告页面。在此页面中，您可以：

- 使用 **Search（搜索）** 字段通过用户名或电子邮件地址进行搜索
- 按策略过滤
- 隐藏或取消隐藏合规用户
- 查看用户的合规状态以及分配给该用户的策略
- 下载用户合规信息的 CSV 文件

## 查看合规状态

> [!WARNING]
>
> 使用 Docker Desktop 4.40 之前版本的用户可能会显示为非合规，因为旧版本无法报告合规性。为确保合规状态准确，用户必须更新到 Docker Desktop 4.40 及更高版本。

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
2. 选择 **Admin Console（管理控制台）**，然后选择 **Desktop settings reporting（Desktop 设置报告）**。
3. （可选）勾选 **Hide compliant users（隐藏合规用户）** 复选框以同时显示合规和非合规用户。
4. 使用 **Search（搜索）** 字段搜索用户名或电子邮件地址。
5. 将鼠标悬停在用户的合规状态指示器上，即可快速查看其状态。
6. 选择一个用户名以查看有关其合规状态的更多详情，以及解决非合规用户的步骤。

## 理解合规状态

Docker 根据以下各项评估合规状态：

- 合规状态（Compliance status）：用户是否已获取并应用了最新的设置。这是报告页面上显示的主要标签。
- 域名状态（Domain status）：用户的电子邮件是否与已验证的域名匹配。
- 设置状态（Settings status）：是否对用户应用了设置策略。

这些状态的组合决定了您需要采取的操作。

### 合规状态参考

此参考解释了报告仪表板如何根据用户域名和设置数据确定每种状态。管理控制台根据以下规则显示优先级最高的适用状态。

**合规状态 (Compliance status)**

| 合规状态 | 含义 |
|-------------------|---------------|
| Uncontrolled domain (未受控域名) | 用户的电子邮件域名未验证。 |
| No policy assigned (未分配策略) | 用户未分配任何策略。 |
| Non-compliant (不合规) | 用户已获取正确的策略，但尚未应用。 |
| Outdated (已过时) | 用户获取的是旧版本的策略。 |
| Compliant (合规) | 用户已获取并应用了最新分配的策略。 |

**域名状态 (Domain status)**

这反映了根据组织的域名设置如何评估用户的电子邮件域名。

| 域名状态 | 含义 |
|---------------|---------------|
| Verified (已验证) | 用户的电子邮件域名已验证。 |
| Guest user (访客用户) | 用户的电子邮件域名未验证。 |
| Domainless (无域名) | 您的组织没有已验证的域名，且用户的域名未知。 |

**设置状态 (Settings status)**

这显示了用户是否被分配了设置策略以及如何分配的。

| 设置状态 | 含义 |
|-----------------|---------------|
| Global policy (全局策略) | 用户被分配了组织的默认策略。 |
| User policy (用户策略) | 用户被分配了特定的自定义策略。 |
| No policy assigned (未分配策略) | 用户未分配任何策略。 |

## 解决合规状态问题

要解决合规状态问题，您必须在 Desktop 设置报告页面上选择用户名来查看用户的合规状态详情。这些详情包括以下信息：

- **Compliance status（合规状态）**：指示用户是否合规其应用的设置
- **Domain status（域名状态）**：指示用户的电子邮件地址是否与已验证的域名相关联
- **Settings status（设置状态）**：指示用户是否应用了设置
- **Resolution steps（解决步骤）**：如果用户不合规，此部分提供有关如何解决用户合规状态的信息

### 合规 (Compliant)

当用户合规时，Desktop 设置报告仪表板上的用户名旁边会出现 **Compliant（合规）** 图标。选择一个合规用户以打开其合规状态详情。合规用户具有以下状态详情：

- **Compliance status（合规状态）**：Compliant（合规）
- **Domain status（域名状态）**：Verified（已验证）
- **Settings status（设置状态）**：Global policy（全局策略）或 User policy（用户策略）
- **User is compliant（用户合规）** 指示器

合规用户不需要采取任何解决步骤。

### 不合规 (Non-compliant)

当用户不合规时，Desktop 设置报告仪表板上的用户名旁边会出现 **Non-compliant（不合规）** 或 **Unknown（未知）** 图标。必须解决非合规用户的合规状态：

1. 从 Desktop 设置报告仪表板中选择一个用户名。
2. 在合规状态详情页面上，按照提供的解决步骤来解决合规状态。
3. 刷新页面以确保解决步骤已生效并解决了合规状态。
