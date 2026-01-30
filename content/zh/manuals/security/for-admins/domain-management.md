---
description: 了解如何在管理控制台管理域名和用户
keywords: domain management, security, identify users, manage users, 域名管理, 安全, 识别用户, 管理用户
title: 域名管理
weight: 55
---

{{< summary-bar feature_name="Domain management" >}}

域名管理允许您添加和验证域名，并为用户启用自动预置 (auto-provisioning)。当用户使用与经验证域名匹配的电子邮件地址登录时，自动预置功能会将该用户添加到您的组织中。

这简化了用户管理，确保了安全性设置的一致性，并降低了未受管用户在缺乏可见性或控制的情况下访问 Docker 的风险。

## 添加域名

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司 (Company)，请选择该公司并在公司级别为组织配置域名。
2. 选择 **Admin Console** (管理控制台)，然后选择 **Domain management** (域名管理)。
3. 选择 **Add a domain** (添加域名)。
4. 输入您的域名并选择 **Add domain**。
5. 在弹出的模态框中，复制 **TXT Record Value** (TXT 记录值) 以验证您的域名。

## 验证域名

验证域名可确认您拥有该域名。要进行验证，请使用 Docker 提供的数值向您的域名系统 (DNS) 主机添加一条 TXT 记录。此数值可证明所有权并指示您的 DNS 发布该记录。

DNS 更改生效可能需要长达 72 小时。一旦识别到更改，Docker 会自动检查该记录并确认所有权。

请按照您的 DNS 提供商的文档添加 **TXT Record Value**。如果您的提供商未在列表中，请参考其他提供商的步骤。

> [!TIP]
>
> 记录名称字段决定了 TXT 记录添加到域名的位置 (根域名或子域名)。通常，请参考以下关于添加记录名称的提示：
>
> - 对于 `example.com` 这样的根域名，使用 `@` 或保持记录名称为空，具体取决于您的提供商。
> - 不要输入 `docker`、`docker-verification`、`www` 或您的域名等值。这些值可能会指向错误的位置。
>
> 请查阅您的 DNS 提供商文档以核实记录名称的要求。

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 要向 AWS 添加 TXT 记录，请参阅 [使用 Amazon Route 53 控制台创建记录](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html)。
2. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台](https://app.docker.com/admin) 的 **Domain management** 页面，并选择您域名旁边的 **Verify** (验证)。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 要向 Google Cloud DNS 添加 TXT 记录，请参阅 [使用 TXT 记录验证您的域名](https://cloud.google.com/identity/docs/verify-domain-txt)。
2. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台](https://app.docker.com/admin) 的 **Domain management** 页面，并选择您域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 要向 GoDaddy 添加 TXT 记录，请参阅 [添加 TXT 记录](https://www.godaddy.com/help/add-a-txt-record-19232)。
2. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台](https://app.docker.com/admin) 的 **Domain management** 页面，并选择您域名旁边的 **Verify**。

{{< /tab >}}
{{< tab name="其他提供商" >}}

1. 登录您的域名主机。
2. 向您的 DNS 设置添加一条 TXT 记录并保存该记录。
3. TXT 记录验证可能需要 72 小时。等待 TXT 记录验证后，返回 [管理控制台](https://app.docker.com/admin) 的 **Domain management** 页面，并选择您域名旁边的 **Verify**。

{{< /tab >}}
{{< /tabs >}}

## 删除域名

删除域名会移除分配的 TXT 记录值。删除域名的步骤：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
2. 选择 **Admin Console**，然后选择 **Domain management**。
3. 对于您想要删除的域名，选择 **Actions** (操作) 菜单，然后选择 **Delete domain** (删除域名)。
4. 在弹出的模态框中选择 **Delete domain** 进行确认。

## 自动预置 (Auto-provisioning)

在启用自动预置之前，您必须先添加并验证域名。这确认了您的组织拥有该域名。一旦域名验证通过，Docker 就可以自动将匹配的用户与您的组织关联起来。自动预置不需要 SSO 连接。

> [!IMPORTANT]
>
> 对于属于 SSO 连接的域名，即时配置 (Just-in-Time, JIT) 会覆盖自动预置来将用户添加到组织。

### 工作原理

当为经验证的域名启用自动预置后，用户下次使用与经验证域名关联的电子邮件地址登录 Docker 时，他们将被自动添加到您的组织中。自动预置不会为新用户创建帐户，而是将现有的未关联用户添加到您的组织中。用户在登录或用户体验上 *不会* 感到任何变化。

当新用户被自动预置时，公司和组织所有者将收到一封电子邮件，通知他们有新用户已加入其组织。如果您需要为组织添加更多席位以容纳新用户，请参阅 [管理席位](/manuals/subscription/manage-seats.md)。

### 启用自动预置

自动预置是针对每个域名启用的。启用自动预置的步骤：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
2. 选择 **Admin Console**，然后选择 **Domain management**。
3. 选择您想要启用自动预置的域名旁边的 **Actions 菜单**。
4. 选择 **Enable auto-provisioning** (启用自动预置)。
5. (可选) 如果是在公司级别启用自动预置，请为该域名的用户选择一个组织。
6. 选择 **Enable** (启用) 进行确认。

**Auto-provisioning** 列将更新为 **Enabled** (已启用)。

### 禁用自动预置

要禁用自动预置：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
2. 选择 **Admin Console**，然后选择 **Domain management**。
3. 选择您域名旁边的 **Actions 菜单**。
4. 选择 **Disable auto-provisioning** (禁用自动预置)。
5. 选择 **Disable** (禁用)。
