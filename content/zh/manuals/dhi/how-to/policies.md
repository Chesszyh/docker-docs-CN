---
title: 通过策略强制使用 Docker Hardened Image
linktitle: 强制镜像使用
description: 了解如何将镜像策略与 Docker Scout 配合用于 Docker Hardened Images。
weight: 50
keywords: docker scout policies, enforce image compliance, container security policy, image provenance, vulnerability policy check
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

镜像 Docker Hardened Image（DHI）仓库会自动启用 [Docker Scout](/scout/)，让您无需额外设置即可开始为镜像强制执行安全和合规策略。使用 Docker Scout 策略，您可以定义和应用规则，确保仅在您的环境中使用经过批准的安全镜像（如基于 DHI 的镜像）。

通过 Docker Scout 内置的策略评估功能，您可以实时监控镜像合规性，将检查集成到 CI/CD 工作流中，并维护镜像安全和来源的一致标准。

## 查看现有策略

要查看应用于镜像 DHI 仓库的当前策略：

1. 在 [Docker Hub](https://hub.docker.com) 中前往镜像的 DHI 仓库。
2. 选择 **View on Scout**。

   这将打开 [Docker Scout 仪表板](https://scout.docker.com)，您可以在其中查看当前活动的策略以及您的镜像是否符合策略标准。

Docker Scout 会在推送新镜像时自动评估策略合规性。每个策略都包含合规结果和指向受影响镜像及层的链接。

## 为基于 DHI 的镜像创建策略

为确保使用 Docker Hardened Images 构建的镜像保持安全，您可以为自己的仓库创建符合您要求的 Docker Scout 策略。这些策略有助于强制执行安全标准，例如防止高危漏洞、要求使用最新的基础镜像或验证关键元数据的存在。

策略在镜像推送到仓库时进行评估，使您能够跟踪合规性、获得偏差通知，并将策略检查集成到 CI/CD 流水线中。

### 示例：为基于 DHI 的镜像创建策略

此示例展示了如何创建一个策略，要求组织中的所有镜像使用 Docker Hardened Images 作为其基础镜像。这确保了您的应用构建在安全、最小化且生产就绪的镜像上。

#### 步骤 1：在 Dockerfile 中使用 DHI 基础镜像

创建一个使用 Docker Hardened Image 镜像仓库作为基础的 Dockerfile。例如：

```dockerfile
# Dockerfile
FROM ORG_NAME/dhi-python:3.13-alpine3.21

ENTRYPOINT ["python", "-c", "print('Hello from a DHI-based image')"]
```

#### 步骤 2：构建并推送镜像

打开终端并导航到包含 Dockerfile 的目录。然后，构建并将镜像推送到您的 Docker Hub 仓库：

```console
$ docker build \
  --push \
  -t YOUR_ORG/my-dhi-app:v1 .
```

#### 步骤 3：启用 Docker Scout

要为您的组织和仓库启用 Docker Scout，请在终端中运行以下命令：

```console
$ docker login
$ docker scout enroll YOUR_ORG
$ docker scout repo enable --org YOUR_ORG YOUR_ORG/my-dhi-app
```

#### 步骤 4：创建策略

1. 前往 [Docker Scout 仪表板](https://scout.docker.com)。
2. 选择您的组织并导航到 **Policies**。
3. 选择 **Add policy**。
4. 为 **Approved Base Images Policy** 选择 **Configure**。
5. 为策略指定一个合规的名称，例如 **Approved DHI Base Images**。
6. 在 **Approved base image sources** 中，删除默认项。
7. 在 **Approved base image sources** 中，添加批准的基础镜像源。对于此示例，使用通配符（`*`）允许所有镜像的 DHI 仓库，`docker.io/ORG_NAME/dhi-*`。将 `ORG_NAME` 替换为您的组织名称。
8. 选择 **Save policy**。

#### 步骤 4：评估策略合规性

1. 前往 [Docker Scout 仪表板](https://scout.docker.com)。
2. 选择您的组织并导航到 **Images**。
3. 找到您的镜像 `YOUR_ORG/my-dhi-app:v1`，并选择 **Compliance** 列中的链接。

这将显示您镜像的策略合规结果，包括它是否满足 **Approved DHI Base Images** 策略的要求。

您现在可以[在 CI 中评估策略合规性](/scout/policy/ci/)。
