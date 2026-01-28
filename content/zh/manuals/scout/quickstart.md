---
title: Docker Scout 快速入门
linkTitle: 快速入门
weight: 20
keywords: scout, supply chain, vulnerabilities, packages, cves, scan, analysis, analyze
description: 学习如何开始使用 Docker Scout 分析镜像并修复漏洞
---

Docker Scout 分析镜像内容并生成详细的软件包和检测到的漏洞报告。
它可以为您提供如何修复镜像分析发现的问题的建议。

本指南以一个存在漏洞的容器镜像为例，向您展示如何使用 Docker
Scout 识别和修复漏洞、比较不同时间的镜像版本，以及与团队分享结果。

## 步骤 1：设置

[这个示例项目](https://github.com/docker/scout-demo-service)包含
一个存在漏洞的 Node.js 应用程序，您可以用它来跟随操作。

1. 克隆其仓库：

   ```console
   $ git clone https://github.com/docker/scout-demo-service.git
   ```

2. 进入目录：

   ```console
   $ cd scout-demo-service
   ```

3. 确保您已登录到 Docker 账户，
   可以通过运行 `docker login` 命令或在 Docker Desktop 中点击登录。

4. 构建镜像并推送到 `<ORG_NAME>/scout-demo:v1`，
   其中 `<ORG_NAME>` 是您推送到的 Docker Hub 命名空间。

   ```console
   $ docker build --push -t <ORG_NAME>/scout-demo:v1 .
   ```

## 步骤 2：启用 Docker Scout

Docker Scout 默认分析所有本地镜像。要分析远程仓库中的镜像，您需要先启用它。
您可以从 Docker Hub、Docker Scout 仪表板和 CLI 中执行此操作。
[在概述指南中了解如何操作](/scout)。

1. 使用 `docker login` 命令或 Docker Desktop 中的**登录**按钮登录您的 Docker 账户。

2. 接下来，使用 `docker scout enroll` 命令为您的组织注册 Docker Scout。

   ```console
   $ docker scout enroll <ORG_NAME>
   ```

3. 使用 `docker scout repo enable` 命令为您的镜像仓库启用 Docker Scout。

   ```console
   $ docker scout repo enable --org <ORG_NAME> <ORG_NAME>/scout-demo
   ```

## 步骤 3：分析镜像漏洞

构建后，使用 `docker scout` CLI 命令查看 Docker Scout 检测到的漏洞。

本指南的示例应用程序使用了存在漏洞的 Express 版本。
以下命令显示了您刚构建的镜像中影响 Express 的所有 CVE：

```console
$ docker scout cves --only-package express
```

Docker Scout 默认分析您最近构建的镜像，
因此在这种情况下无需指定镜像名称。

在 [`CLI 参考文档`](/reference/cli/docker/scout/cves)中了解更多关于 `docker scout cves` 命令的信息。

## 步骤 4：修复应用程序漏洞

经过 Docker Scout 分析后，发现了一个高危漏洞 CVE-2022-24999，由过时版本的 **express** 软件包引起。

express 软件包的 4.17.3 版本修复了该漏洞。因此，更新 `package.json` 文件到新版本：

   ```diff
      "dependencies": {
   -    "express": "4.17.1"
   +    "express": "4.17.3"
      }
   ```

使用新标签重新构建镜像并推送到您的 Docker Hub 仓库：

   ```console
   $ docker build --push -t <ORG_NAME>/scout-demo:v2 .
   ```

再次运行 `docker scout` 命令并验证高危漏洞 CVE-2022-24999 不再存在：

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

## 步骤 5：评估策略合规性

虽然根据特定软件包检查漏洞可能很有用，
但这并不是改善供应链行为的最有效方式。

Docker Scout 还支持策略评估，
这是一个用于检测和修复镜像问题的更高级别概念。
策略是一组可自定义的规则，让组织跟踪镜像是否符合其供应链要求。

因为策略规则特定于每个组织，
您必须指定要评估的组织的策略。
使用 `docker scout config` 命令配置您的 Docker 组织。

```console
$ docker scout config organization <ORG_NAME>
    ✓ Successfully set organization to <ORG_NAME>
```

现在您可以运行 `quickview` 命令来获取
您刚构建的镜像的合规状态概览。
镜像将根据默认策略配置进行评估。您将看到类似以下的输出：

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

状态列中的感叹号表示策略违规。
问号表示没有足够的元数据来完成评估。
勾号表示合规。

## 步骤 6：改善合规性

`quickview` 命令的输出显示还有改进空间。
一些策略无法成功评估（`No data`），
因为镜像缺少来源（provenance）和 SBOM 证明。
镜像在一些评估项上也未通过检查。

策略评估不仅仅是检查漏洞。
以 `Default non-root user` 策略为例。
该策略通过确保镜像默认不以 `root` 超级用户运行来帮助提高运行时安全性。

要解决此策略违规，编辑 Dockerfile 添加 `USER`
指令，指定非 root 用户：

```diff
  CMD ["node","/app/app.js"]
  EXPOSE 3000
+ USER appuser
```

此外，为了获得更完整的策略评估结果，
您的镜像应该附加 SBOM 和来源证明。
Docker Scout 使用来源证明来确定镜像是如何构建的，
以便提供更好的评估结果。

在构建带有证明的镜像之前，
您必须启用 [containerd 镜像存储](/manuals/desktop/features/containerd.md)
（或使用 `docker-container` 驱动创建自定义构建器）。
传统镜像存储不支持清单列表，
而来源证明正是通过清单列表附加到镜像的。

在 Docker Desktop 中打开**设置**。在**常规**部分，确保
**使用 containerd 拉取和存储镜像**选项已勾选，然后选择**应用**。
请注意，更改镜像存储会暂时隐藏非活动镜像存储的镜像和容器，
直到您切换回来。

启用 containerd 镜像存储后，使用新的 `v3` 标签重新构建镜像。
这次，添加 `--provenance=true` 和 `--sbom=true` 标志。

```console
$ docker build --provenance=true --sbom=true --push -t <ORG_NAME>/scout-demo:v3 .
```

## 步骤 7：在仪表板中查看

推送带有证明的更新镜像后，是时候通过不同的视角查看结果了：Docker Scout 仪表板。

1. 打开 [Docker Scout 仪表板](https://scout.docker.com/)。
2. 使用您的 Docker 账户登录。
3. 在左侧导航中选择**镜像**。

镜像页面列出了您启用了 Scout 的仓库。

在行中的任意位置（链接除外）选择您要查看的镜像行，打开**镜像详情**侧边栏。

侧边栏显示仓库最后推送标签的合规概览。

> [!NOTE]
>
> 如果策略结果尚未出现，请尝试刷新页面。
> 如果这是您第一次使用 Docker Scout 仪表板，
> 结果可能需要几分钟才能出现。

返回镜像列表并选择镜像版本，可在**最新镜像**列中找到。
然后，在页面右上角，选择**更新基础镜像**按钮来检查策略。

此策略检查您使用的基础镜像是否是最新的。
它当前处于不合规状态，
因为示例镜像使用了旧版本的 `alpine` 作为基础镜像。

关闭**基础镜像的推荐修复**模态框。在策略列表中，选择策略名称旁边的**查看修复**按钮，了解有关违规的详细信息以及如何解决的建议。

在这种情况下，建议的操作是启用
[Docker Scout 的 GitHub 集成](./integrations/source-code-management/github.md)，
它有助于自动保持基础镜像的更新。

> [!TIP]
>
> 您无法为本指南中使用的演示应用启用此集成。
> 您可以随意将代码推送到您拥有的 GitHub 仓库，
> 并在那里尝试该集成！

## 总结

本快速入门指南初步介绍了 Docker Scout
支持软件供应链管理的一些方式：

- 如何为您的仓库启用 Docker Scout
- 分析镜像漏洞
- 策略和合规性
- 修复漏洞和改善合规性

## 下一步

还有很多内容可以探索，从第三方集成、
策略自定义到实时运行时环境监控。

查看以下章节：

- [镜像分析](/manuals/scout/explore/analysis.md)
- [数据来源](/scout/advisory-db-sources)
- [Docker Scout 仪表板](/scout/dashboard)
- [集成](./integrations/_index.md)
- [策略评估](./policy/_index.md)
