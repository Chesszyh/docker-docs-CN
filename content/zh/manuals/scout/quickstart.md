---
title: Docker Scout 快速入门
linkTitle: 快速入门
weight: 20
keywords: scout, 供应链, 漏洞, 软件包, cves, 扫描, 分析
description: 了解如何开始使用 Docker Scout 分析镜像并修复漏洞
---

Docker Scout 分析镜像内容并生成其检测到的软件包和漏洞的详细报告。它可以为您提供如何修复镜像分析发现的问题的建议。

本指南将以一个包含漏洞的容器镜像为例，向您展示如何使用 Docker Scout 识别和修复漏洞、比较镜像版本随时间的变化，并与您的团队分享结果。

## 第 1 步：设置

[此示例项目](https://github.com/docker/scout-demo-service) 包含一个易受攻击的 Node.js 应用程序，您可以按照它进行操作。

1. 克隆其仓库：

   ```console
   $ git clone https://github.com/docker/scout-demo-service.git
   ```

2. 进入该目录：

   ```console
   $ cd scout-demo-service
   ```

3. 确保您已登录 Docker 帐户，可以通过运行 `docker login` 命令或通过 Docker Desktop 登录。

4. 构建镜像并将其推送到 `<ORG_NAME>/scout-demo:v1`，其中 `<ORG_NAME>` 是您推送到的 Docker Hub 命名空间。

   ```console
   $ docker build --push -t <ORG_NAME>/scout-demo:v1 .
   ```

## 第 2 步：启用 Docker Scout

Docker Scout 默认分析所有本地镜像。要分析远程仓库中的镜像，您需要先启用它。
您可以从 Docker Hub、Docker Scout 控制面板和 CLI 执行此操作。
[在概览指南中了解如何操作](/scout)。

1. 使用 `docker login` 命令登录您的 Docker 帐户，或使用 Docker Desktop 中的 **Sign in** 按钮。

2. 接下来，使用 `docker scout enroll` 命令将您的组织注册到 Docker Scout。

   ```console
   $ docker scout enroll <ORG_NAME>
   ```

3. 使用 `docker scout repo enable` 命令为您的镜像仓库启用 Docker Scout。

   ```console
   $ docker scout repo enable --org <ORG_NAME> <ORG_NAME>/scout-demo
   ```

## 第 3 步：分析镜像漏洞

构建后，使用 `docker scout` CLI 命令查看 Docker Scout 检测到的漏洞。

本指南的示例应用程序使用了一个包含漏洞的 Express 版本。
以下命令显示了在您刚刚构建的镜像中受影响 Express 的所有 CVE：

```console
$ docker scout cves --only-package express
```

Docker Scout 默认分析您最近构建的镜像，因此在这种情况下无需指定镜像名称。

在 [`CLI 参考文档`](/reference/cli/docker/scout/cves) 中了解有关 `docker scout cves` 命令的更多信息。

## 第 4 步：修复应用程序漏洞

在 Docker Scout 分析之后，发现了一个高危漏洞 CVE-2022-24999，这是由过时版本的 **express** 软件包引起的。

express 软件包的 4.17.3 版本修复了该漏洞。因此，将 `package.json` 文件更新为新版本：

   ```diff
      "dependencies": {
   -    "express": "4.17.1"
   +    "express": "4.17.3"
      }
   ```
   
使用新标签重新构建镜像并将其推送到您的 Docker Hub 仓库：

   ```console
   $ docker build --push -t <ORG_NAME>/scout-demo:v2 .
   ```

再次运行 `docker scout` 命令并确认高危 CVE-2022-24999 不再存在：

```console
$ docker scout cves --only-package express
    ✓ Provenance obtained from attestation
    ✓ Image stored for indexing
    ✓ Indexed 79 packages
    ✓ No vulnerable package detected


  ## Overview

                      │                  Analyzed Image                   
  ────────────────────┼───────────────────────────────────────────────────
    Target            │  mobywhale/scout-demo:v2                   
      digest          │  ef68417b2866                                     
      platform        │ linux/arm64                                       
      provenance      │ https://github.com/docker/scout-demo-service.git  
                      │  7c3a06793fc8f97961b4a40c73e0f7ed85501857         
      vulnerabilities │    0C     0H     0M     0L                        
      size            │ 19 MB                                             
      packages        │ 1                                                 


  ## Packages and Vulnerabilities

  No vulnerable packages detected

```

## 第 5 步：评估策略合规性

虽然根据特定软件包检查漏洞很有用，但这并不是改进供应链行为的最有效方法。

Docker Scout 还支持策略评估，这是一个用于检测和修复镜像中问题的更高级概念。
策略是一组可定制的规则，让组织能够跟踪镜像是否符合其供应链要求。

因为策略规则对于每个组织都是特定的，所以您必须指定要根据哪个组织的策略进行评估。
使用 `docker scout config` 命令配置您的 Docker 组织。

```console
$ docker scout config organization <ORG_NAME>
    ✓ Successfully set organization to <ORG_NAME>
```

现在您可以运行 `quickview` 命令来获取您刚刚构建的镜像的合规状态概览。
该镜像将根据默认策略配置进行评估。您将看到类似于以下内容的输出：

```console
$ docker scout quickview

...
Policy status  FAILED  (2/6 policies met, 2 missing data)

  Status │                  Policy                      │           Results
─────────┼──────────────────────────────────────────────┼──────────────────────────────
  ✓      │ No copyleft licenses                         │    0 packages
  !      │ Default non-root user                        │
  !      │ No fixable critical or high vulnerabilities  │    2C    16H     0M     0L
  ✓      │ No high-profile vulnerabilities              │    0C     0H     0M     0L
  ?      │ No outdated base images                      │    No data
  ?      │ Supply chain attestations                    │    No data
```

状态列中的感叹号表示违反了策略。问号表示没有足够的元数据来完成评估。复选标记表示符合合规要求。

## 第 6 步：提高合规性

`quickview` 命令的输出显示还有改进的空间。
由于镜像缺少来源（provenance）和 SBOM 证明（attestations），某些策略无法成功评估 (`No data`)。
该镜像在几项评估中也未能通过检查。

策略评估不仅仅是检查漏洞。以 `Default non-root user` 策略为例。
此策略通过确保镜像默认不设置为以 `root` 超级用户身份运行，来帮助提高运行时安全性。

要解决此策略冲突，请通过添加 `USER` 指令来编辑 Dockerfile，指定非 root 用户：

```diff
  CMD ["node","/app/app.js"]
  EXPOSE 3000
+ USER appuser
```

此外，为了获得更完整的策略评估结果，您的镜像应该附带 SBOM 和来源证明。
Docker Scout 使用来源证明来确定镜像的构建方式，从而提供更好的评估结果。

在构建带有证明的镜像之前，必须启用 [containerd 镜像存储](/manuals/desktop/features/containerd.md) (或使用 `docker-container` 驱动程序创建自定义构建器)。
传统的镜像存储不支持清单列表 (manifest lists)，而这正是将来源证明附加到镜像的方式。

打开 Docker Desktop 中的 **Settings**。在 **General** 部分下，确保勾选了 **Use containerd for pulling and storing images** 选项，然后选择 **Apply**。
请注意，更改镜像存储会暂时隐藏非活动镜像存储的镜像和容器，直到您切换回来。

启用 containerd 镜像存储后，使用新的 `v3` 标签重新构建镜像。这次，添加 `--provenance=true` 和 `--sbom=true` 标志。

```console
$ docker build --provenance=true --sbom=true --push -t <ORG_NAME>/scout-demo:v3 .
```

## 第 7 步：在控制面板中查看

推送更新后的带有证明的镜像后，是时候从不同的视角查看结果了：Docker Scout 控制面板。

1. 打开 [Docker Scout 控制面板](https://scout.docker.com/)。
2. 使用您的 Docker 帐户登录。
3. 在左侧导航栏中选择 **Images**。

镜像页面列出了您启用 Scout 的仓库。

选择您要查看的镜像行（行中除链接外的任意位置），以打开 **Image details** 侧边栏。

侧边栏显示了仓库最后推送标签的合规性概览。

> [!NOTE]
>
> 如果策略结果尚未出现，请尝试刷新页面。如果您是第一次使用 Docker Scout 控制面板，可能需要几分钟时间才会显示结果。

回到镜像列表，选择 **Most recent image** 列中提供的镜像版本。
然后，在页面右上角，选择 **Update base image** 按钮以检查策略。

此策略检查您使用的基础镜像是否是最新的。
由于示例镜像使用旧版本的 `alpine` 作为基础镜像，因此目前处于不合规状态。

关闭 **Recommended fixes for base image** 模态框。在策略列表中，选择策略名称旁边的 **View fixes** 按钮，以查看有关违规的详细信息以及有关如何解决该问题的建议。

在这种情况下，建议的操作是启用 [Docker Scout 的 GitHub 集成](./integrations/source-code-management/github.md)，这有助于自动保持基础镜像为最新版本。

> [!TIP]
>
> 您无法为本指南中使用的演示应用程序启用此集成。您可以随意将代码推送到您拥有的 GitHub 仓库，并在那里尝试集成！

## 总结

本快速入门指南仅触及了 Docker Scout 支持软件供应链管理的一些方式：

- 如何为您的仓库启用 Docker Scout
- 分析镜像漏洞
- 策略和合规性
- 修复漏洞并提高合规性

## 下一步是什么？

还有更多内容值得探索，从第三方集成到策略定制，以及实时运行时环境监控。

查看以下章节：

- [镜像分析](/manuals/scout/explore/analysis.md)
- [数据源](/scout/advisory-db-sources)
- [Docker Scout 控制面板](/scout/dashboard)
- [集成](./integrations/_index.md)
- [策略评估](./policy/_index.md)
