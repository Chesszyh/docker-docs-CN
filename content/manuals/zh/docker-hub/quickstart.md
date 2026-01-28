---
description: 了解如何开始使用 Docker Hub
keywords: Docker Hub, push image, pull image, repositories
title: Docker Hub 快速入门
linkTitle: 快速入门
weight: 10
---

Docker Hub 提供了大量预构建的镜像和资源库，可以加速开发工作流程并减少设置时间。您可以基于 Docker Hub 中的预构建镜像进行构建，然后使用仓库与您的团队或数百万其他开发人员共享和分发您自己的镜像。

本指南向您展示如何查找和运行预构建镜像。然后引导您创建自定义镜像并通过 Docker Hub 共享它。

## 前提条件

- [下载并安装 Docker](../../get-started/get-docker.md)
- [创建 Docker 账户](https://app.docker.com/signup)

## 步骤 1：在 Docker Hub 的镜像库中查找镜像

您可以在 Docker Hub 本身、Docker Desktop 仪表板或使用 CLI 来搜索内容。

要在 Docker Hub 上搜索或浏览内容：

{{< tabs >}}
{{< tab name="Docker Hub" >}}

1. 导航到 [Docker Hub 探索页面](https://hub.docker.com/explore)。

   在 **Explore**（探索）页面上，您可以按目录或类别浏览，或使用搜索快速查找内容。

2. 在 **Categories**（类别）下，选择 **Web servers**（Web 服务器）。

   显示结果后，您可以使用页面左侧的过滤器进一步筛选结果。

3. 在过滤器中，选择 **Docker Official Image**（Docker 官方镜像）。

   按可信内容（Trusted Content）过滤可确保您只看到由 Docker 和经过验证的发布合作伙伴精心策划的高质量、安全镜像。

4. 在结果中，选择 **nginx** 镜像。

   选择镜像会打开镜像页面，您可以在其中了解更多关于如何使用该镜像的信息。在页面上，您还会找到用于拉取镜像的 `docker pull` 命令。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 打开 Docker Desktop 仪表板。
2. 选择 **Docker Hub** 视图。

   在 **Docker Hub** 视图中，您可以按目录或类别浏览，或使用搜索快速查找内容。

3. 保持搜索框为空，然后选择 **Search**（搜索）。

   搜索结果会显示出来，搜索框旁边还会出现额外的过滤器。

4. 选择搜索过滤器图标，然后选择 **Docker Official Image** 和 **Web Servers**。
5. 在结果中，选择 **nginx** 镜像。

{{< /tab >}}
{{< tab name="CLI" >}}

1. 打开终端窗口。

   > [!TIP]
   >
   > Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 **>_ Terminal** 打开它。

2. 在终端中，运行以下命令。

   ```console
   $ docker search --filter is-official=true nginx
   ```

   与 Docker Hub 和 Docker Desktop 界面不同，您无法使用 `docker search` 命令按类别浏览。有关该命令的更多详细信息，请参阅 [docker search](/reference/cli/docker/search/)。

{{< /tab >}}
{{< /tabs >}}

现在您已经找到了镜像，是时候将其拉取并在您的设备上运行了。

## 步骤 2：从 Docker Hub 拉取并运行镜像

您可以使用 CLI 或 Docker Desktop 仪表板从 Docker Hub 运行镜像。

{{< tabs >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 仪表板中，在 **Docker Hub** 视图中选择 **nginx** 镜像。有关更多详细信息，请参阅[步骤 1：在 Docker Hub 的镜像库中查找镜像](#步骤-1在-docker-hub-的镜像库中查找镜像)。

2. 在 **nginx** 界面上，选择 **Run**（运行）。

   如果镜像不存在于您的设备上，它会自动从 Docker Hub 拉取。拉取镜像可能需要几秒到几分钟，具体取决于您的连接速度。镜像拉取完成后，Docker Desktop 中会出现一个窗口，您可以指定运行选项。

3. 在 **Host port**（主机端口）选项中，指定 `8080`。
4. 选择 **Run**（运行）。

   容器启动后会显示容器日志。

5. 选择 **8080:80** 链接打开服务器，或在 Web 浏览器中访问 [http://localhost:8080](http://localhost:8080)。

6. 在 Docker Desktop 仪表板中，选择 **Stop**（停止）按钮停止容器。


{{< /tab >}}
{{< tab name="CLI" >}}

1. 打开终端窗口。

   > [!TIP]
   >
   > Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 **>_ Terminal** 打开它。

2. 在终端中，运行以下命令来拉取并运行 Nginx 镜像。

   ```console
   $ docker run -p 8080:80 --rm nginx
   ```

   `docker run` 命令会自动拉取并运行镜像，无需先运行 `docker pull`。要了解更多关于该命令及其选项的信息，请参阅 [`docker run` CLI 参考](../../reference/cli/docker/container/run.md)。运行命令后，您应该会看到类似以下的输出。

   ```console {collapse=true}
   Unable to find image 'nginx:latest' locally
   latest: Pulling from library/nginx
   a480a496ba95: Pull complete
   f3ace1b8ce45: Pull complete
   11d6fdd0e8a7: Pull complete
   f1091da6fd5c: Pull complete
   40eea07b53d8: Pull complete
   6476794e50f4: Pull complete
   70850b3ec6b2: Pull complete
   Digest: sha256:28402db69fec7c17e179ea87882667f1e054391138f77ffaf0c3eb388efc3ffb
   Status: Downloaded newer image for nginx:latest
   /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
   /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
   /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
   10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
   10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
   /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
   /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
   /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
   /docker-entrypoint.sh: Configuration complete; ready for start up
   2024/11/07 21:43:41 [notice] 1#1: using the "epoll" event method
   2024/11/07 21:43:41 [notice] 1#1: nginx/1.27.2
   2024/11/07 21:43:41 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
   2024/11/07 21:43:41 [notice] 1#1: OS: Linux 6.10.11-linuxkit
   2024/11/07 21:43:41 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
   2024/11/07 21:43:41 [notice] 1#1: start worker processes
   2024/11/07 21:43:41 [notice] 1#1: start worker process 29
   ...
   ```

3. 访问 [http://localhost:8080](http://localhost:8080) 查看默认的 Nginx 页面并验证容器正在运行。

4. 在终端中，按 <kdb>Ctrl+C</kbd> 停止容器。

{{< /tab >}}
{{< /tabs >}}

您现在已经运行了一个 Web 服务器，无需任何设置或配置。Docker Hub 提供即时访问预构建的、即用型容器镜像，让您可以快速拉取和运行应用程序，而无需手动安装或配置软件。借助 Docker Hub 庞大的镜像库，您可以轻松地试验和部署应用程序，提高生产力，轻松尝试新工具、设置开发环境或基于现有软件进行构建。

您还可以扩展 Docker Hub 中的镜像，让您可以快速构建和自定义自己的镜像以满足特定需求。


## 步骤 3：构建并推送镜像到 Docker Hub

1. 创建一个 [Dockerfile](/reference/dockerfile.md) 来指定您的应用程序：

   ```dockerfile
   FROM nginx
   RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/nginx/html/index.html
   ```

   这个 Dockerfile 扩展了来自 Docker Hub 的 Nginx 镜像，创建了一个简单的网站。只需几行代码，您就可以使用 Docker 轻松设置、自定义和共享静态网站。

2. 运行以下命令来构建您的镜像。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker build -t <YOUR-USERNAME>/nginx-custom .
   ```

   此命令构建您的镜像并为其打标签，以便 Docker 知道要将其推送到 Docker Hub 中的哪个仓库。要了解更多关于该命令及其选项的信息，请参阅 [`docker build` CLI 参考](../../reference/cli/docker/buildx/build.md)。运行命令后，您应该会看到类似以下的输出。

   ```console {collapse=true}
   [+] Building 0.6s (6/6) FINISHED                      docker:desktop-linux
    => [internal] load build definition from Dockerfile                  0.0s
    => => transferring dockerfile: 128B                                  0.0s
    => [internal] load metadata for docker.io/library/nginx:latest       0.0s
    => [internal] load .dockerignore                                     0.0s
    => => transferring context: 2B                                       0.0s
    => [1/2] FROM docker.io/library/nginx:latest                         0.1s
    => [2/2] RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/  0.2s
    => exporting to image                                                0.1s
    => => exporting layers                                               0.0s
    => => writing image sha256:f85ab68f4987847713e87a95c39009a5c9f4ad78  0.0s
    => => naming to docker.io/mobyismyname/nginx-custom                  0.0s
   ```

3. 运行以下命令来测试您的镜像。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker run -p 8080:80 --rm <YOUR-USERNAME>/nginx-custom
   ```

4. 访问 [http://localhost:8080](http://localhost:8080) 查看页面。您应该会看到 `Hello world from Docker!`。

5. 在终端中，按 CTRL+C 停止容器。

6. 登录 Docker Desktop。在将镜像推送到 Docker Hub 之前，您必须先登录。

7. 运行以下命令将您的镜像推送到 Docker Hub。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker push <YOUR-USERNAME>/nginx-custom
   ```

    > [!NOTE]
    >
    > 您必须通过 Docker Desktop 或命令行登录 Docker Hub，并且必须按照上述步骤正确命名您的镜像。

   该命令将镜像推送到 Docker Hub，如果仓库不存在，则会自动创建。要了解更多关于该命令的信息，请参阅 [`docker push` CLI 参考](../../reference/cli/docker/image/push.md)。运行命令后，您应该会看到类似以下的输出。

   ```console {collapse=true}
   Using default tag: latest
   The push refers to repository [docker.io/mobyismyname/nginx-custom]
   d0e011850342: Pushed
   e4e9e9ad93c2: Mounted from library/nginx
   6ac729401225: Mounted from library/nginx
   8ce189049cb5: Mounted from library/nginx
   296af1bd2844: Mounted from library/nginx
   63d7ce983cd5: Mounted from library/nginx
   b33db0c3c3a8: Mounted from library/nginx
   98b5f35ea9d3: Mounted from library/nginx
   latest: digest: sha256:7f5223ae866e725a7f86b856c30edd3b86f60d76694df81d90b08918d8de1e3f size: 1985
   ```

  现在您已经创建了仓库并推送了镜像，是时候查看您的仓库并探索其选项了。

## 步骤 4：在 Docker Hub 上查看您的仓库并探索选项

您可以在 Docker Hub 或 Docker Desktop 界面中查看您的 Docker Hub 仓库。

{{< tabs >}}
{{< tab name="Docker Hub" >}}

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。

   登录后，您应该在 **Repositories**（仓库）页面。如果不在，请前往 [**Repositories**](https://hub.docker.com/repositories/) 页面。

2. 找到 **nginx-custom** 仓库并选择该行。

   选择仓库后，您应该会看到仓库的更多详细信息和选项。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 登录 Docker Desktop。
2. 选择 **Images**（镜像）视图。
3. 选择 **Hub repositories**（Hub 仓库）选项卡。

   您的 Docker Hub 仓库列表会出现。

4. 找到 **nginx-custom** 仓库，将鼠标悬停在该行上，然后选择 **View in Hub**（在 Hub 中查看）。

   Docker Hub 会打开，您可以查看有关镜像的更多详细信息。

{{< /tab >}}
{{< /tabs >}}

您现在已经验证了您的仓库存在于 Docker Hub 上，并发现了更多选项。查看后续步骤以了解更多关于这些选项的信息。

## 后续步骤

添加[仓库信息](./repos/manage/information.md)以帮助用户查找和使用您的镜像。
