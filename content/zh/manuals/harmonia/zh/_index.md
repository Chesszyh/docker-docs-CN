---
title: Project Harmonia
description: 了解如何使用 Project Harmonia 在云端运行您的应用程序
keywords: run, cloud, docker desktop, resources
sitemap: false
params:
  sidebar:
    group: Products
aliases:
- /run-cloud/
---

{{% restricted title="私有预览" %}}
Project Harmonia 目前处于私有预览（Private preview）阶段。
{{% /restricted %}}

Project Harmonia 将云的强大能力带入您的本地开发工作流程。您现在可以在云端运行应用程序，同时继续使用现有的工具和工作流程，而无需担心本地资源限制。Project Harmonia 还允许您分享基于云的应用程序预览，以获取实时反馈。

## 设置

要开始使用 Project Harmonia，您需要：

- 拥有一个属于 Docker 组织的 Docker 账户
- 发送邮件至 `run.cloud@docker.com` 以获取入门帮助

## 快速入门

您可以通过 Docker Desktop Dashboard 或 CLI 使用 Project Harmonia。

本指南将向您介绍创建、管理和共享云引擎（cloud engine）的基本命令和步骤。

### 第一步：创建云引擎

{{< tabs group="method" >}}
{{< tab name="Docker Desktop">}}

1. 在 Docker Desktop Dashboard 中，导航到 **Project Harmonia** 标签页。
2. 在右上角，选择 **Create Cloud Engine**。
3. 填写创建表单：
   - 输入 `cloudengine` 作为名称
   - 选择要关联云引擎的组织
   - 选择引擎大小和架构

   请注意，**Switch Docker Context to use remote engine** 默认是选中的。一旦云引擎创建完成，这将自动切换到您的新云引擎。
4. 选择 **Create**。

要验证创建是否成功，请检查 Docker Desktop Dashboard 左上角的上下文切换器；它应该显示 `cloudengine`。现在您可以开始使用它了。

{{< /tab >}}
{{< tab name="CLI">}}

运行以下命令：

```console
$ docker harmonia engine create cloudengine --type "standard-amd64"  --use
```

这将创建一个名为 `cloudengine` 的引擎，并且：
- 通过 `--use` 标志立即切换到新的云引擎。
- 通过 `--type` 标志将引擎大小设置为 standard，并将引擎的 CPU 架构设置为 amd64。

Project Harmonia 支持以下 `--type` 值：
- `standard-arm64`
- `standard-amd64`（默认）
- `large-arm64`
- `large-amd64`
- `aiml-amd64`

Standard 大小的引擎具有 2 个 CPU 核心和 4GB RAM，large 和 AI/ML 引擎具有 4 个 CPU 核心和 8GB RAM。

要验证您正在使用新创建的云引擎，请运行：

```console
$ docker context inspect
```

您应该看到以下内容：

```text
[
    {
        "Name": "cloudengine2",
...
```

{{< /tab >}}
{{< /tabs >}}

### 第二步：使用新创建的云引擎运行和删除容器

1.  在云引擎中运行一个 Nginx 容器：
    ```console
    $ docker run -d --name cloudnginx -p 8080:80 nginx
    ```
    这会将容器的端口 `80` 映射到主机的端口 `8080`。如果主机上的端口 `8080` 已被占用，您可以指定其他端口。
2.  查看 Nginx 欢迎页面。导航到 [`http://localhost:8080/`](http://localhost:8080/)。
3.  验证正在运行的容器：
    -   在 Docker Desktop Dashboard 的 **Containers** 标签页中，您应该能看到您的 Nginx 容器列出。
    -   或者，通过终端列出云引擎中所有正在运行的容器：
        ```console
        $ docker ps
        ```
4.  停止容器：
    ```console
    $ docker kill cloudnginx
    ```

使用云引擎运行容器与在本地运行一样简单直接。

### 第三步：创建并切换到新的云引擎

{{< tabs group="method" >}}
{{< tab name="Docker Desktop">}}

1. 创建一个新的云引擎：
   - 输入 `cloudengine2` 作为名称
   - 选择要关联云引擎的组织
   - 选择 **Standard** 引擎大小和 **AMD-64** 架构
   在 **Project Harmonia** 视图中，您现在应该能看到 `cloudengine` 和 `cloudengine2`。
2. 在引擎之间切换，也称为您的 Docker 上下文（contexts）。使用 Docker Desktop Dashboard 左上角的上下文切换器在云引擎之间切换，或从本地引擎（`desktop-linux`）切换到云引擎。

{{< /tab >}}
{{< tab name="CLI">}}

1. 创建一个新的云引擎。运行：
   ```console
   $ docker harmonia engine create cloudengine2
   ```
   Docker 会自动切换到您的新云引擎。
2. 在引擎之间切换，也称为您的 Docker 上下文（contexts）。切换到您的第一个云引擎：
   ```console
   $ docker context use cloudengine
   ```
   或者切换回您的本地引擎：
   ```console
   $ docker context use desktop-linux
   ```

{{< /tab >}}
{{< /tabs >}}

### 第四步：为云引擎使用文件同步

Project Harmonia 利用[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md)来实现本地到远程的文件共享和端口映射。

{{< tabs group="method" >}}
{{< tab name="Docker Desktop">}}

1. 克隆 [Awesome Compose](https://github.com/docker/awesome-compose) 仓库。
2. 在 Docker Desktop Dashboard 中，导航到 **Project Harmonia** 视图。
3. 对于 `cloudengine` 云引擎，选择 **Actions** 菜单，然后选择 **Manage file syncs**。
4. 选择 **Create file sync**。
5. 导航到 `awesome-compose/react-express-mysql` 文件夹并选择 **Open**。
6. 在终端中，导航到 `awesome-compose/react-express-mysql` 目录。
7. 使用以下命令在云引擎中运行项目：
   ```console
   $ docker compose up -d
   ```
8. 通过访问 [`http://localhost:3000`](http://localhost:3000/) 测试应用程序。
   您应该能看到主页。此页面的代码位于 `react-express-mysql/frontend/src/App.js`。
9. 在 IDE 或文本编辑器中，打开 `App.js` 文件，修改一些文本并保存。观察代码在浏览器中实时重新加载。

{{< /tab >}}
{{< tab name="CLI">}}

1. 克隆 [Awesome Compose](https://github.com/docker/awesome-compose) 仓库。
2. 在终端中，切换到 `awesome-compose/react-express-mysql` 目录。
3. 为 `cloudengine` 创建文件同步：
   ```console
   $ docker harmonia file-sync create --engine cloudengine $PWD
4. 使用以下命令在云引擎中运行项目：
   ```console
   $ docker compose up -d
   ```
5. 通过访问 [`http://localhost:3000`](http://localhost:3000/) 测试应用程序。
   您应该能看到主页。此页面的代码位于 `react-express-mysql/frontend/src/App.js`。
6. 在 IDE 或文本编辑器中，打开 `App.js` 文件，修改一些文本并保存。观察代码在浏览器中实时重新加载。

{{< /tab >}}
{{< /tabs >}}

### 第五步：共享容器端口

{{< tabs group="method" >}}
{{< tab name="Docker Desktop">}}

1.  确保您的 Docker 上下文设置为 `cloudengine`。
2.  在 Docker Desktop Dashboard 中，导航到 **Containers** 视图。
3.  如有必要，展开应用程序列表以显示其所有容器。
4.  在正在运行的容器的 **Ports** 列中，选择 `3000:3000` 旁边的 **lock** 图标。
    这将创建一个可公开访问的 URL，您可以与团队成员共享。
5.  选择 **copy** 图标来复制此 URL。

要查看您的 Docker 上下文的所有共享端口，请选择 Docker Desktop Dashboard 右下角的 **Shared ports** 图标。

{{< /tab >}}
{{< tab name="CLI">}}

要共享容器端口，请确保您的 Docker 上下文设置为 `cloudengine`，然后运行：
``` console
$ docker harmonia engine share create cloudengine 3000
```
这将返回一个可公开访问的 URL，用于您托管在端口 `3000` 上的 React 应用，您可以与团队成员共享。

要查看所有共享端口的列表，请运行：

```console
$ docker harmonia engine share list
```

{{< /tab >}}
{{< /tabs >}}

### 第六步：清理

{{< tabs group="method" >}}
{{< tab name="Docker Desktop">}}

要停止正在运行的项目：

```console
$ docker compose down
```

要删除文件同步会话：
1. 在 **Project Harmonia** 视图中导航到您的云引擎。
2. 选择 **Actions** 菜单，然后选择 **Manage file syncs**。
3. 选择文件同步上的 **drop-down** 图标。
4. 选择 **Delete**。

要删除云引擎，请导航到 **Project Harmonia** 视图，然后选择 **delete** 图标。

{{< /tab >}}
{{< tab name="CLI">}}

要停止正在运行的项目：

```console
$ docker compose down
```

要删除文件同步会话，请运行：

```console
$ docker harmonia file-sync delete --engine cloudengine $PWD
```

要删除云引擎，请运行：

```console
$ docker harmonia engine delete <name-of-engine>
```

{{< /tab >}}
{{< /tabs >}}

## 故障排除

运行 `docker harmonia doctor` 以打印有用的故障排除信息。

## 已知问题

- KinD 无法在 Project Harmonia 上运行，因为它有一些硬编码的假设以确保其在特权容器中运行。K3d 是一个很好的替代方案。
- 容器无法通过 DNS `host.docker.internal` 访问主机。
- 文件绑定（非目录绑定）目前是静态的，这意味着更改在容器重启之前不会生效。这也影响 Compose 的 configs 和 secrets 指令。
- 绑定_挂载_，例如 `docker run` 命令中的 `-v /localpath:/incontainer`，需要创建文件同步。
- 为包含大量文件的目录创建[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md)可能需要额外的时间来同步，然后才能在容器中使用。
- 绑定_卷_，例如使用 `docker volume create --driver local --opt type=none --opt o=bind --opt device=/some/host/path myvolname` 或通过等效的 compose 方式创建的卷，不受支持。
- 不支持 UDP 端口转发。
- 依赖 `sync` 模式下 `watch` 的 Docker Compose 项目无法与 `tar` 同步器一起工作。请将其配置为使用 `docker cp`，通过在环境中设置 `COMPOSE_EXPERIMENTAL_WATCH_TAR=0` 来禁用 tar 同步。
- 一些允许访问底层主机的 Docker Engine 功能，如 `--pid=host`、`--network=host` 和 `--ipc=host`，目前已被禁用。
