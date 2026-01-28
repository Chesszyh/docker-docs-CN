---
title: 活动日志
weight: 50
description: 了解活动日志。
keywords: team, organization, activity, log, audit, activities
aliases:
- /docker-hub/audit-log/
---

{{< summary-bar feature_name="Activity logs" >}}

活动日志（Activity logs）按时间顺序显示在组织和仓库级别发生的活动列表。它为所有者提供了关于所有成员活动的报告。

通过活动日志，所有者可以查看和跟踪：
 - 进行了哪些更改
 - 更改的日期
 - 谁发起了更改

例如，活动日志会显示仓库创建或删除的日期、创建仓库的成员、仓库名称以及隐私设置的更改时间等活动。

如果仓库属于订阅了 Docker Business 或 Team 订阅的组织，所有者还可以查看其仓库的活动日志。

## 管理活动日志

{{< tabs >}}
{{< tab name="Admin Console" >}}

{{% admin-org-audit-log product="admin" %}}

{{< /tab >}}
{{< tab name="Docker Hub" >}}

{{% include "hub-org-management.md" %}}

{{% admin-org-audit-log product="hub" %}}

{{< /tab >}}
{{< /tabs >}}

## 事件定义

请参阅以下章节了解事件列表及其描述：

### 组织事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Team Created | 与创建团队相关的活动 |
| Team Updated | 与修改团队相关的活动 |
| Team Deleted | 与删除团队相关的活动 |
| Team Member Added | 添加到您团队的成员详情 |
| Team Member Removed | 从您团队移除的成员详情 |
| Team Member Invited | 邀请到您团队的成员详情 |
| Organization Member Added | 添加到您组织的成员详情 |
| Organization Member Removed | 从您组织移除的成员详情 |
| Member Role Changed | 组织中成员角色更改的详情 |
| Organization Created | 与创建新组织相关的活动 |
| Organization Settings Updated | 与更新的组织设置相关的详情 |
| Registry Access Management enabled | 与启用注册表访问管理相关的活动 |
| Registry Access Management disabled | 与禁用注册表访问管理相关的活动 |
| Registry Access Management registry added | 与添加注册表相关的活动 |
| Registry Access Management registry removed | 与移除注册表相关的活动 |
| Registry Access Management registry updated | 与更新的注册表相关的详情 |
| Single Sign-On domain added | 添加到您组织的单点登录域名详情 |
| Single Sign-On domain removed | 从您组织移除的单点登录域名详情 |
| Single Sign-On domain verified | 为您组织验证的单点登录域名详情 |
| Access token created | 在组织中创建的访问令牌 |
| Access token updated | 在组织中更新的访问令牌 |
| Access token deleted | 在组织中删除的访问令牌 |
| Policy created | 添加设置策略的详情 |
| Policy updated | 更新设置策略的详情 |
| Policy deleted | 删除设置策略的详情 |
| Policy transferred | 将设置策略转移给其他所有者的详情 |
| Create SSO Connection | 创建新组织/公司 SSO 连接的详情 |
| Update SSO Connection | 更新现有组织/公司 SSO 连接的详情 |
| Delete SSO Connection | 删除现有组织/公司 SSO 连接的详情 |
| Enforce SSO | 在现有组织/公司 SSO 连接上切换强制执行的详情 |
| Enforce SCIM | 在现有组织/公司 SSO 连接上切换 SCIM 的详情 |
| Refresh SCIM Token | 在现有组织/公司 SSO 连接上刷新 SCIM 令牌的详情 |
| Change SSO Connection Type | 在现有组织/公司 SSO 连接上更改连接类型的详情 |
| Toggle JIT provisioning | 在现有组织/公司 SSO 连接上切换 JIT 的详情 |

### 仓库事件

> [!NOTE]
>
> 包含用户操作的事件描述可以指 Docker 用户名、个人访问令牌（PAT）或组织访问令牌（OAT）。例如，如果用户向仓库推送标签，事件将包含描述：`<user-access-token>` 向仓库推送了标签。

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Repository Created | 与创建新仓库相关的活动 |
| Repository Deleted | 与删除仓库相关的活动 |
| Repository Updated | 与更新仓库描述、完整描述或状态相关的活动 |
| Privacy Changed | 与更新的隐私策略相关的详情 |
| Tag Pushed | 与推送的标签相关的活动 |
| Tag Deleted | 与删除的标签相关的活动 |
| Categories Updated | 与设置或更新仓库分类相关的活动 |

### 账单事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Plan Upgraded | 当您组织的账单计划升级到更高层级计划时发生。|
| Plan Downgraded | 当您组织的账单计划降级到较低层级计划时发生。 |
| Seat Added | 当向您组织的账单计划添加席位时发生。 |
| Seat Removed | 当从您组织的账单计划移除席位时发生。 |
| Billing Cycle Changed | 当您组织的收费周期发生变化时发生。|
| Plan Downgrade Canceled | 当您组织的计划降级计划被取消时发生。|
| Seat Removal Canceled | 当组织账单计划的席位移除计划被取消时发生。 |
| Plan Upgrade Requested | 当您组织中的用户请求计划升级时发生。 |
| Plan Downgrade Requested | 当您组织中的用户请求计划降级时发生。 |
| Seat Addition Requested | 当您组织中的用户请求增加席位数量时发生。 |
| Seat Removal Requested | 当您组织中的用户请求减少席位数量时发生。 |
| Billing Cycle Change Requested | 当您组织中的用户请求更改账单周期时发生。 |
| Plan Downgrade Cancellation Requested | 当您组织中的用户请求取消计划降级计划时发生。 |
| Seat Removal Cancellation Requested | 当您组织中的用户请求取消计划席位移除时发生。 |
