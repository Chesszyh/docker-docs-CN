---
linktitle: Quickstart
title: Docker 强化镜像快速入门
description: 按照快速入门指南探索、镜像同步和运行 Docker 强化镜像。
weight: 2
keywords: docker hardened images quickstart, mirror container image, run secure image
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

本指南向您展示如何从零开始运行 Docker 强化镜像（DHI），并使用一个实际示例。虽然这些步骤使用特定镜像作为示例，但它们可以应用于任何 DHI。

## 步骤 1：注册并订阅 DHI 以获取访问权限

要访问 Docker 强化镜像，您的组织必须[注册](https://www.docker.com/products/hardened-images/#getstarted)并订阅。

## 步骤 2：查找要使用的镜像

订阅后，Docker 强化镜像将显示在您组织在 Docker Hub 上的命名空间下。

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 在顶部导航栏中选择 **My Hub**。
3. 在左侧边栏中，选择具有 DHI 访问权限的组织。
4. 在左侧边栏中，选择 **DHI catalog**。

   ![Docker Hub 侧边栏显示 DHI 目录](./images/dhi-catalog.png)

5. 使用搜索栏或过滤器查找镜像（例如 `python`、`node`、`golang`）。在本指南中，我们以 Python 镜像为例。

    ![DHI 目录显示 Python 仓库](./images/dhi-python-search.png)

6. 选择 Python 仓库以查看其详细信息。

继续下一步以镜像同步该镜像。要深入了解如何探索镜像，请参阅[探索 Docker 强化镜像](./how-to/explore.md)。

## 步骤 3：镜像同步

要使用 Docker 强化镜像，您必须将其镜像同步到您的组织。只有组织所有者可以执行此操作。镜像同步会在您组织的命名空间中创建镜像的副本，允许团队成员拉取和使用它。

1. 在镜像仓库页面中，选择 **Mirror to repository**。

   ![Python 页面显示 Mirror to repository 按钮的图片](./images/dhi-mirror-button.png)

   > [!NOTE]
   >
   > 如果您没有看到 **Mirror to repository** 按钮，该仓库可能已经镜像同步到您的组织。在这种情况下，您可以选择 **View in repository** 查看镜像同步的镜像位置，或将其镜像同步到另一个仓库。

2. 按照屏幕上的说明选择名称。在本指南中，示例使用名称 `dhi-python`。请注意，名称必须以 `dhi-` 开头。

   ![镜像同步仓库页面](./images/dhi-mirror-screen.png)

3. 选择 **Create repository** 开始镜像同步过程。

所有标签完成镜像同步可能需要几分钟时间。镜像同步完成后，镜像仓库将出现在您组织的命名空间中。例如，在 [Docker Hub](https://hub.docker.com) 中，前往 **My Hub** > ***YOUR_ORG*** > **Repositories**，您应该会看到列出的 `dhi-python`。现在您可以像拉取任何其他镜像一样拉取它。

![仓库列表显示已镜像同步的仓库](./images/dhi-python-mirror.png)

继续下一步以拉取和运行镜像。要深入了解镜像同步，请参阅[镜像同步 Docker 强化镜像仓库](./how-to/mirror.md)。

## 步骤 4：拉取并运行镜像

将镜像镜像同步到您的组织后，您可以像拉取和运行任何其他 Docker 镜像一样拉取和运行它。请注意，Docker 强化镜像设计为精简且安全，因此它们可能不包含您在典型镜像中期望的所有工具或库。您可以在[采用 DHI 时的注意事项](./how-to/use.md#considerations-when-adopting-dhis)中查看典型差异。

以下示例演示您可以运行 Python 镜像并执行简单的 Python 命令，就像使用任何其他 Docker 镜像一样：

1. 拉取镜像同步的镜像。打开终端并运行以下命令，将 `<your-namespace>` 替换为您组织的命名空间：

   ```console
   $ docker pull <your-namespace>/dhi-python:3.13
   ```

2. 运行镜像以确认一切正常：

    ```console
    $ docker run --rm <your-namespace>/dhi-python:3.13 python -c "print('Hello from DHI')"
    ```

    这将从 `dhi-python:3.13` 镜像启动一个容器，并运行一个简单的 Python 脚本，打印 `Hello from DHI`。

要深入了解如何使用镜像，请参阅[使用 Docker 强化镜像](./how-to/use.md)。

## 后续步骤

您已经拉取并运行了您的第一个 Docker 强化镜像。以下是一些继续学习的方式：

- [将现有应用程序迁移到 DHIs](./how-to/migrate.md)：了解如何更新您的 Dockerfile 以使用 Docker 强化镜像作为基础镜像。

- [验证 DHIs](./how-to/verify.md)：使用 [Docker Scout](/scout/) 或 Cosign 等工具检查和验证签名证明，如 SBOM 和来源证明。

- [扫描 DHIs](./how-to/scan.md)：使用 Docker Scout 或其他扫描器分析镜像，以识别已知的 CVE。
