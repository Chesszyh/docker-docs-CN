---
description:
  Docker Scout 可以与运行时环境集成，为您提供有关软件供应链的实时洞察。
keywords: supply chain, security, streams, environments, workloads, deployments
title: 将 Docker Scout 与环境集成
---

您可以将 Docker Scout 与运行时环境集成，获取正在运行的工作负载的洞察。这使您能够实时查看已部署制品的安全状态。

Docker Scout 允许您定义多个环境，并将镜像分配到不同的环境。这为您提供了软件供应链的完整概览，让您可以查看和比较环境之间的差异，例如 staging（预发布）和 production（生产）环境。

如何定义和命名环境由您决定。您可以使用对您有意义的模式，以匹配您交付应用程序的方式。

## 分配到环境

每个环境包含对多个镜像的引用。这些引用代表当前在该特定环境中运行的容器。

例如，假设您在生产环境中运行 `myorg/webapp:3.1`，您可以将该标签分配到 `production` 环境。您可能在 staging 环境中运行同一镜像的不同版本，在这种情况下，您可以将该镜像版本分配到 `staging` 环境。

要向 Docker Scout 添加环境，您可以：

- 使用 `docker scout env <environment> <image>` CLI 命令手动将镜像记录到环境
- 启用运行时集成以自动检测环境中的镜像

Docker Scout 支持以下运行时集成：

- [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout#record-an-image-deployed-to-an-environment)
- [CLI 客户端](./cli.md)
- [Sysdig 集成](./sysdig.md)

> [!NOTE]
>
> 只有组织所有者才能创建新环境和设置集成。此外，Docker Scout 仅在镜像[已被分析](/manuals/scout/explore/analysis.md)后才会将其分配到环境，分析可以手动进行或通过[仓库集成](/manuals/scout/integrations/_index.md#container-registries)进行。

## 列出环境

要查看组织的所有可用环境，可以使用 `docker scout env` 命令。

```console
$ docker scout env
```

默认情况下，这会打印您个人 Docker 组织的所有环境。要列出您所属的其他组织的环境，请使用 `--org` 标志。

```console
$ docker scout env --org <org>
```

您可以使用 `docker scout config` 命令更改默认组织。这会更改所有 `docker scout` 命令的默认组织，而不仅仅是 `env`。

```console
$ docker scout config organization <org>
```

## 环境之间的比较

将镜像分配到环境后，您可以与环境进行比较以及在环境之间进行比较。这对于诸如 GitHub 拉取请求之类的场景很有用，可以将 PR 中代码构建的镜像与 staging 或 production 中的相应镜像进行比较。

您也可以使用 [`docker scout compare`](/reference/cli/docker/scout/compare.md) CLI 命令的 `--to-env` 标志与流进行比较：

```console
$ docker scout compare --to-env production myorg/webapp:latest
```

## 查看环境的镜像

要查看某个环境的镜像：

1. 前往 Docker Scout Dashboard 中的[镜像页面](https://scout.docker.com/)。
2. 打开 **Environments** 下拉菜单。
3. 选择您要查看的环境。

列表显示已分配到所选环境的所有镜像。如果您在一个环境中部署了同一镜像的多个版本，所有版本的镜像都会出现在列表中。

或者，您可以使用 `docker scout env` 命令从终端查看镜像。

```console
$ docker scout env production
docker/scout-demo-service:main@sha256:ef08dca54c4f371e7ea090914f503982e890ec81d22fd29aa3b012351a44e1bc
```

### 镜像标签不匹配

当您在 **Images** 标签页上选择了某个环境时，列表中的标签代表用于部署镜像的标签。标签是可变的，这意味着您可以更改标签所指向的镜像摘要。如果 Docker Scout 检测到某个标签指向了过时的摘要，镜像名称旁边会显示一个警告图标。
