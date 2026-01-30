---
title: 使用 GUI 创建例外
description: 使用 Docker Scout 控制面板或 Docker Desktop 为镜像中的漏洞创建例外。
keywords: Docker, Docker Scout, Docker Desktop, 漏洞, 例外, 创建, GUI
---

Docker Scout 控制面板和 Docker Desktop 为针对容器镜像中发现的漏洞创建 [例外](/manuals/scout/explore/exceptions.md) 提供了一个用户友好的界面。例外允许您承认已接受的风险或解决镜像分析中的误报。

## 前提条件

要在 Docker Scout 控制面板或 Docker Desktop 中创建例外，您需要一个在拥有该镜像的 Docker 组织中具有 **Editor** (编辑器) 或 **Owner** (所有者) 权限的 Docker 帐户。

## 步骤

使用 Docker Scout 控制面板或 Docker Desktop 为镜像中的漏洞创建例外：

{{< tabs >}}
{{< tab name="Docker Scout Dashboard" >}}

1. 转到 [Images 页面](https://scout.docker.com/reports/images)。
2. 选择包含您要为其创建例外的漏洞的镜像标签。
3. 打开 **Image layers** (镜像层) 选项卡。
4. 选择包含您要为其创建例外的漏洞的层。
5. 在 **Vulnerabilities** (漏洞) 选项卡中，找到您要为其创建例外的漏洞。漏洞按软件包分组。找到包含该漏洞的软件包，然后展开该软件包。
6. 选择漏洞旁边的 **Create exception** (创建例外) 按钮。

{{% create_panel.inline %}}
选择 **Create exception** 按钮将打开 **Create exception** 侧面板。在此面板中，您可以提供例外的详细信息：

- **Exception type** (例外类型)：例外的类型。目前唯一支持的类型有：

  - **Accepted risk** (已接受的风险)：由于安全风险极小、修复成本高、依赖上游修复等原因，不处理该漏洞。
  - **False positive** (误报)：由于您的特定用例、配置或因为已实施了阻止利用的措施，该漏洞不存在安全风险。

    如果选择 **False positive**，则必须提供该漏洞为何是误报的理由。

- **Additional details** (附加详情)：您想要提供的有关例外的任何其他信息。

- **Scope** (范围)：例外的范围。范围可以是：

  - **Image** (镜像)：例外适用于所选镜像。
  - **All images in repository** (仓库中的所有镜像)：例外适用于该仓库中的所有镜像。
  - **Specific repository** (特定仓库)：例外适用于指定仓库中的所有镜像。
  - **All images in my organization** (我组织中的所有镜像)：例外适用于您组织中的所有镜像。

- **Package scope** (软件包范围)：例外的范围。软件包范围可以是：

  - **Selected package** (选定软件包)：例外仅适用于选定的软件包。
  - **Any packages** (任何软件包)：例外适用于所有受此 CVE 影响的软件包。

填写完详细信息后，选择 **Create** 按钮以创建例外。

现在例外已创建，并已计入所选镜像的分析结果中。该例外也列在 Docker Scout 控制面板 [Vulnerabilities 页面](https://scout.docker.com/reports/vulnerabilities/exceptions) 的 **Exceptions** 选项卡上。

{{% /create_panel.inline %}}

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 中打开 **Images** 视图。
2. 打开 **Hub** 选项卡。
3. 选择包含您要为其创建例外的漏洞的镜像标签。
4. 选择包含您要为其创建例外的漏洞的层。
5. 在 **Vulnerabilities** 选项卡中，找到您要为其创建例外的漏洞。
6. 选择漏洞旁边的 **Create exception** 按钮。

{{% create_panel.inline / %}}

{{< /tab >}}
{{< /tabs >}}
