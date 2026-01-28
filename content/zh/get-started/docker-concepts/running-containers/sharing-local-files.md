---
title: 与容器共享本地文件
weight: 4
keywords: concepts, images, container, docker desktop
description: 本概念页面将教您了解 Docker 中可用的各种存储选项及其常见用法。
aliases:
 - /guides/docker-concepts/running-containers/sharing-local-files/
---

{{< youtube-embed 2dAzsVg3Dek >}}


## 概念解释

每个容器都拥有运行所需的一切，无需依赖主机上任何预先安装的依赖项。由于容器是隔离运行的，它们对主机和其他容器的影响最小。这种隔离有一个主要好处：容器最大限度地减少与主机系统和其他容器的冲突。然而，这种隔离也意味着容器默认情况下无法直接访问主机上的数据。

考虑这样一个场景：您有一个 Web 应用程序容器，需要访问存储在主机系统文件中的配置设置。此文件可能包含敏感数据，如数据库凭据或 API 密钥。将此类敏感信息直接存储在容器镜像中会带来安全风险，尤其是在镜像共享期间。为了解决这一挑战，Docker 提供了存储选项，弥合了容器隔离与主机数据之间的差距。

Docker 提供两种主要的存储选项，用于持久化数据和在主机与容器之间共享文件：卷（volume）和绑定挂载（bind mount）。

### 卷与绑定挂载

如果您想确保容器内生成或修改的数据即使在容器停止运行后仍然持久化，您应该选择卷。请参阅[持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/)了解更多关于卷及其使用场景的信息。

如果您有想要直接与容器共享的主机系统上的特定文件或目录，如配置文件或开发代码，那么您应该使用绑定挂载。这就像在主机和容器之间打开一个直接的门户进行共享。绑定挂载非常适合开发环境，在这些环境中，主机和容器之间的实时文件访问和共享至关重要。

### 在主机和容器之间共享文件

`docker run` 命令中使用的 `-v`（或 `--volume`）和 `--mount` 标志都允许您在本地机器（主机）和 Docker 容器之间共享文件或目录。但是，它们的行为和用法有一些关键区别。

`-v` 标志更简单，更方便用于基本的卷或绑定挂载操作。如果在使用 `-v` 或 `--volume` 时主机位置不存在，将自动创建一个目录。

假设您是一名从事项目的开发人员。您的开发机器上有一个源代码目录，您的代码就在那里。当您编译或构建代码时，生成的工件（编译后的代码、可执行文件、镜像等）保存在源目录内的单独子目录中。在以下示例中，此子目录是 `/HOST/PATH`。现在您希望这些构建工件可以在运行应用程序的 Docker 容器中访问。此外，您希望每当重新构建代码时，容器自动访问最新的构建工件。

以下是使用 `docker run` 启动容器并使用绑定挂载将其映射到容器文件位置的方法。

```console
$ docker run -v /HOST/PATH:/CONTAINER/PATH -it nginx
```

`--mount` 标志提供更高级的功能和更精细的控制，适合复杂的挂载场景或生产部署。如果您使用 `--mount` 绑定挂载一个在 Docker 主机上尚不存在的文件或目录，`docker run` 命令不会自动为您创建它，而是生成一个错误。

```console
$ docker run --mount type=bind,source=/HOST/PATH,target=/CONTAINER/PATH,readonly nginx
```

> [!NOTE]
>
> Docker 建议使用 `--mount` 语法而不是 `-v`。它提供对挂载过程更好的控制，并避免因缺少目录而产生的潜在问题。

### Docker 访问主机文件的文件权限

使用绑定挂载时，确保 Docker 具有访问主机目录的必要权限至关重要。要授予读/写访问权限，您可以在容器创建期间与 `-v` 或 `--mount` 标志一起使用 `:ro` 标志（只读）或 `:rw`（读写）。
例如，以下命令授予读写访问权限。

```console
$ docker run -v HOST-DIRECTORY:/CONTAINER-DIRECTORY:rw nginx
```

只读绑定挂载允许容器访问主机上挂载的文件进行读取，但不能更改或删除文件。使用读写绑定挂载，容器可以修改或删除挂载的文件，这些更改或删除也将反映在主机系统上。只读绑定挂载确保主机上的文件不会被容器意外修改或删除。

> **同步文件共享**
>
> 随着代码库变得越来越大，传统的文件共享方法（如绑定挂载）可能变得低效或缓慢，尤其是在需要频繁访问文件的开发环境中。[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md)通过利用同步的文件系统缓存来提高绑定挂载性能。此优化确保主机和虚拟机（VM）之间的文件访问快速高效。

## 动手实践

在本动手指南中，您将练习如何创建和使用绑定挂载在主机和容器之间共享文件。

### 运行容器

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 使用以下命令通过 [httpd](https://hub.docker.com/_/httpd) 镜像启动容器：

   ```console
   $ docker run -d -p 8080:80 --name my_site httpd:2.4
   ```

   这将在后台启动 `httpd` 服务，并将网页发布到主机的端口 `8080`。

3. 打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 或使用 curl 命令验证是否正常工作。

    ```console
    $ curl localhost:8080
    ```


### 使用绑定挂载

使用绑定挂载，您可以将主机计算机上的配置文件映射到容器内的特定位置。在此示例中，您将看到如何使用绑定挂载更改网页的外观：

1. 使用 Docker Desktop 仪表板删除现有容器：

   ![Docker Desktop 仪表板的截图，显示如何删除 httpd 容器](images/delete-httpd-container.webp?border=true)


2. 在主机系统上创建一个名为 `public_html` 的新目录。

    ```console
    $ mkdir public_html
    ```

3. 进入新创建的 `public_html` 目录，创建一个名为 `index.html` 的文件，内容如下。这是一个基本的 HTML 文档，创建一个简单的网页，用一只友好的鲸鱼欢迎您。

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title> My Website with a Whale & Docker!</title>
    </head>
    <body>
    <h1>Whalecome!!</h1>
    <p>Look! There's a friendly whale greeting you!</p>
    <pre id="docker-art">
       ##         .
      ## ## ##        ==
     ## ## ## ## ##    ===
     /"""""""""""""""""\___/ ===
   {                       /  ===-
   \______ O           __/
    \    \         __/
     \____\_______/

    Hello from Docker!
    </pre>
    </body>
    </html>
    ```

4. 是时候运行容器了。`--mount` 和 `-v` 示例产生相同的结果。除非您在运行第一个后删除 `my_site` 容器，否则不能同时运行两者。

   {{< tabs >}}
   {{< tab name="`-v`" >}}

   ```console
   $ docker run -d --name my_site -p 8080:80 -v .:/usr/local/apache2/htdocs/ httpd:2.4
   ```

   {{< /tab >}}
   {{< tab name="`--mount`" >}}

   ```console
   $ docker run -d --name my_site -p 8080:80 --mount type=bind,source=./,target=/usr/local/apache2/htdocs/ httpd:2.4
   ```

   {{< /tab >}}
   {{< /tabs >}}


   > [!TIP]
   > 在 Windows PowerShell 中使用 `-v` 或 `--mount` 标志时，您需要提供目录的绝对路径，而不仅仅是 `./`。这是因为 PowerShell 处理相对路径的方式与 bash（通常在 Mac 和 Linux 环境中使用）不同。



   现在一切都已启动并运行，您应该能够通过 [http://localhost:8080](http://localhost:8080) 访问网站，并找到一个用友好的鲸鱼欢迎您的新网页。


### 在 Docker Desktop 仪表板上访问文件

1. 您可以通过选择容器的 **Files** 选项卡，然后在 `/usr/local/apache2/htdocs/` 目录中选择一个文件来查看容器内挂载的文件。然后，选择 **Open file editor**。


   ![Docker Desktop 仪表板的截图，显示容器内挂载的文件](images/mounted-files.webp?border=true)

2. 删除主机上的文件并验证容器中的文件也已删除。您会发现文件不再存在于 Docker Desktop 仪表板的 **Files** 下。


   ![Docker Desktop 仪表板的截图，显示容器内已删除的文件](images/deleted-files.webp?border=true)


3. 在主机系统上重新创建 HTML 文件，并查看文件重新出现在 Docker Desktop 仪表板的 **Containers** 下的 **Files** 选项卡中。此时，您也将能够访问该网站。



### 停止您的容器

容器将继续运行，直到您停止它。

1. 在 Docker Desktop 仪表板中进入 **Containers** 视图。

2. 找到您要停止的容器。

3. 选择 Actions 列中的 **Delete** 操作。

![Docker Desktop 仪表板的截图，显示如何删除容器](images/delete-the-container.webp?border=true)


## 其他资源

以下资源将帮助您了解更多关于绑定挂载的信息：

* [在 Docker 中管理数据](/storage/)
* [卷](/storage/volumes/)
* [绑定挂载](/storage/bind-mounts/)
* [运行容器](/reference/run/)
* [存储错误故障排除](/storage/troubleshooting_volume_errors/)
* [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/)

## 后续步骤

现在您已经学习了与容器共享本地文件，是时候学习多容器应用程序了。

{{< button text="多容器应用程序" url="Multi-container applications" >}}
