---
title: 管理漏洞例外
description: |
  例外允许您提供有关漏洞如何影响您的制品的额外上下文和文档，并提供抑制不适用漏洞的能力
keywords: scout, cves, 抑制, vex, 例外
---

在容器镜像中发现的漏洞有时需要额外的上下文。仅仅因为镜像包含一个有漏洞的软件包，并不意味着该漏洞是可利用的。Docker Scout 中的 **Exceptions** (例外) 允许您承认已接受的风险或解决镜像分析中的误报。

通过排除不适用的漏洞，您可以让自己和镜像的下游消费者更容易理解漏洞在镜像上下文中的安全含义。

在 Docker Scout 中，例外会自动计入结果中。如果镜像包含一个将 CVE 标记为不适用的例外，那么该 CVE 将被排除在分析结果之外。

## 创建例外

要为镜像创建例外，您可以：

- 在 Docker Scout 控制面板或 Docker Desktop 的 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 中创建例外。
- 创建一个 [VEX](/manuals/scout/how-tos/create-exceptions-vex.md) 文档并将其附加到镜像上。

创建例外的推荐方法是使用 Docker Scout 控制面板或 Docker Desktop。GUI 为创建例外提供了一个用户友好的界面。它还允许您一次性为多个镜像或整个组织创建例外。

## 查看例外

要查看镜像的例外情况，您需要拥有适当的权限。

- [使用 GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外对您 Docker 组织的成员可见。未经身份验证的用户或不是您组织成员的用户无法看到这些例外。
- [使用 VEX 文档](/manuals/scout/how-tos/create-exceptions-vex.md) 创建的例外对任何可以拉取镜像的人都可见，因为 VEX 文档存储在镜像清单或镜像文件系统中。

### 在 Docker Scout 控制面板或 Docker Desktop 中查看例外

Docker Scout 控制面板中漏洞页面的 [**Exceptions** 选项卡](https://scout.docker.com/reports/vulnerabilities/exceptions) 列出了您组织中所有镜像的所有例外情况。在此处，您可以查看有关每个例外的更多详细信息，包括被抑制的 CVE、例外适用的镜像、例外类型及其创建方式等。

对于使用 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外，选择操作菜单可以编辑或删除该例外。

要查看特定镜像标签的所有例外：

{{< tabs >}}
{{< tab name="Docker Scout Dashboard" >}}

1. 转到 [Images 页面](https://scout.docker.com/reports/images)。
2. 选择您要检查的标签。
3. 打开 **Exceptions** 选项卡。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 中打开 **Images** 视图。
2. 打开 **Hub** 选项卡。
3. 选择您要检查的标签。
4. 打开 **Exceptions** 选项卡。

{{< /tab >}}
{{< /tabs >}}

### 在 CLI 中查看例外

{{< summary-bar feature_name="Docker Scout exceptions" >}}

当您运行 `docker scout cves <image>` 时，漏洞例外会在 CLI 中突出显示。如果某个 CVE 被例外抑制，CVE ID 旁边会出现一个 `SUPPRESSED` 标签。还会显示有关该例外的详细信息。

![CLI 输出中的 SUPPRESSED 标签](/scout/images/suppressed-cve-cli.png)

> [!IMPORTANT]
> 为了在 CLI 中查看例外，您必须将 CLI 配置为使用您创建例外时使用的同一个 Docker 组织。
>
> 要为 CLI 配置组织，请运行：
>
> ```console
> $ docker scout configure organization <organization>
> ```
>
> 将 `<organization>` 替换为您 Docker 组织的名称。
>
> 您还可以通过使用 `--org` 标志在每个命令的基础上设置组织：
>
> ```console
> $ docker scout cves --org <organization> <image>
> ```

要从输出中排除被抑制的 CVE，请使用 `--ignore-suppressed` 标志：

```console
$ docker scout cves --ignore-suppressed <image>
```
