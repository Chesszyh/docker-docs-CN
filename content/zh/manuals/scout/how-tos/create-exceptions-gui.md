---
title: 使用 GUI 创建例外
description: 使用 Docker Scout Dashboard 或 Docker Desktop 为镜像中的漏洞创建例外。
keywords: Docker, Docker Scout, Docker Desktop, vulnerability, exception, create, GUI
---

Docker Scout Dashboard 和 Docker Desktop 提供了用户友好的界面，用于为容器镜像中发现的漏洞创建[例外](/manuals/scout/explore/exceptions.md)。例外允许您确认已接受的风险或处理镜像分析中的误报。

## 前提条件

要在 Docker Scout Dashboard 或 Docker Desktop 中创建例外，您需要一个对拥有该镜像的 Docker 组织具有 **Editor**（编辑者）或 **Owner**（所有者）权限的 Docker 帐户。

## 步骤

使用 Docker Scout Dashboard 或 Docker Desktop 为镜像中的漏洞创建例外：

{{< tabs >}}
{{< tab name="Docker Scout Dashboard" >}}

1. 前往[镜像页面](https://scout.docker.com/reports/images)。
2. 选择包含您要创建例外的漏洞的镜像标签。
3. 打开 **Image layers**（镜像层）标签页。
4. 选择包含您要创建例外的漏洞的层。
5. 在 **Vulnerabilities**（漏洞）标签页中，找到您要创建例外的漏洞。漏洞按软件包分组。找到包含您要创建例外的漏洞的软件包，然后展开该软件包。
6. 选择漏洞旁边的 **Create exception**（创建例外）按钮。

{{% create_panel.inline %}}
选择 **Create exception** 按钮会打开 **Create exception** 侧边面板。在此面板中，您可以提供例外的详细信息：

- **Exception type**（例外类型）：例外的类型。目前仅支持以下类型：

  - **Accepted risk**（已接受的风险）：由于安全风险较低、修复成本较高、依赖上游修复或类似原因，不处理该漏洞。
  - **False positive**（误报）：在您的特定用例、配置中，或由于已采取的阻止利用措施，该漏洞不构成安全风险。

    如果您选择 **False positive**，您必须提供该漏洞为何是误报的理由：

- **Additional details**（附加详情）：您想要提供的关于该例外的任何附加信息。

- **Scope**（范围）：例外的范围。范围可以是：

  - **Image**（镜像）：例外适用于所选镜像。
  - **All images in repository**（仓库中的所有镜像）：例外适用于该仓库中的所有镜像。
  - **Specific repository**（特定仓库）：例外适用于指定仓库中的所有镜像。
  - **All images in my organization**（我的组织中的所有镜像）：例外适用于您组织中的所有镜像。

- **Package scope**（软件包范围）：例外的软件包范围。软件包范围可以是：

  - **Selected package**（选定的软件包）：例外适用于选定的软件包。
  - **Any packages**（任何软件包）：例外适用于所有受此 CVE 影响的软件包。

填写完详细信息后，选择 **Create**（创建）按钮来创建例外。

例外现已创建，并会被纳入您所选镜像的分析结果中。该例外还会列在 Docker Scout Dashboard 中[漏洞页面](https://scout.docker.com/reports/vulnerabilities/exceptions)的 **Exceptions**（例外）标签页中。

{{% /create_panel.inline %}}

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 中打开 **Images**（镜像）视图。
2. 打开 **Hub** 标签页。
3. 选择包含您要创建例外的漏洞的镜像标签。
4. 选择包含您要创建例外的漏洞的层。
5. 在 **Vulnerabilities**（漏洞）标签页中，找到您要创建例外的漏洞。
6. 选择漏洞旁边的 **Create exception**（创建例外）按钮。

{{% create_panel.inline / %}}

{{< /tab >}}
{{< /tabs >}}
