---
title: 与容器共享本地文件
weight: 4
keywords: concepts, images, container, docker desktop, 概念, 镜像, 容器
description: 此概念页面将向您介绍 Docker 中可用的各种存储选项及其常见用法。
aliases: 
 - /guides/docker-concepts/running-containers/sharing-local-files/
---

{{< youtube-embed 2dAzsVg3Dek >}}


## 解释

每个容器都拥有其运行所需的一切，不依赖于主机上任何预装的依赖项。由于容器是隔离运行的，它们对主机和其他容器的影响极小。这种隔离有一个主要好处：容器最大程度地减少了与主机系统和其他容器的冲突。然而，这种隔离也意味着容器默认情况下无法直接访问主机机器上的数据。

考虑这样一个场景：您有一个 Web 应用程序容器，需要访问存储在主机系统文件中的配置设置。此文件可能包含敏感数据，如数据库凭据或 API 密钥。直接将此类敏感信息存储在容器镜像中会带来安全风险，尤其是在镜像共享期间。为了应对这一挑战，Docker 提供了存储选项，弥补了容器隔离与主机机器数据之间的鸿沟。

Docker 提供了两种主要的存储选项，用于持久化数据以及在主机机器与容器之间共享文件：卷 (Volumes) 和绑定挂载 (Bind mounts)。

### 卷与绑定挂载

如果您想确保容器内部生成或修改的数据即使在容器停止运行后也能持久存在，您可以选择卷。请参阅[持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/)以了解更多关于卷及其用例的信息。

如果您希望将主机系统上的特定文件或目录直接共享给容器（例如配置文件或开发代码），那么您可以使用绑定挂载。这就像是在主机和容器之间打开了一个直接共享的门户。绑定挂载非常适合实时文件访问以及主机与容器之间共享至关重要的开发环境。

### 在主机和容器之间共享文件

在 `docker run` 命令中使用的 `-v`（或 `--volume`）和 `--mount` 标志都允许您在本地机器（主机）和 Docker 容器之间共享文件或目录。然而，它们在行为和用法上存在一些关键差异。

对于基本的卷或绑定挂载操作，`-v` 标志更简单、更方便。如果在使用 `-v` 或 `--volume` 时主机位置不存在，则会自动创建一个目录。

想象一下您是一名正在开发项目的开发人员。您的开发机器上有一个源代码目录，代码就存放在那里。当您编译或构建代码时，生成的构件（编译后的代码、可执行文件、镜像等）会保存在源代码目录下的一个单独子目录中。在以下示例中，此子目录为 `/HOST/PATH`。现在您希望这些构建构件在运行应用程序的 Docker 容器中可访问。此外，您希望容器在您每次重新构建代码时都能自动访问最新的构建构件。

以下是使用 `docker run` 通过绑定挂载启动容器并将其映射到容器文件位置的方法。

```console
$ docker run -v /HOST/PATH:/CONTAINER/PATH -it nginx
```

`--mount` 标志提供了更高级的功能和更细粒度的控制，使其适用于复杂的挂载场景或生产部署。如果您使用 `--mount` 绑定挂载一个在 Docker 主机上尚不存在的文件或目录，`docker run` 命令不会自动为您创建它，而是会生成一个错误。

```console
$ docker run --mount type=bind,source=/HOST/PATH,target=/CONTAINER/PATH,readonly nginx
```

> [!NOTE]
>
> Docker 建议使用 `--mount` 语法而不是 `-v`。它对挂载过程提供了更好的控制，并避免了由于目录缺失可能导致的问题。

### Docker 访问主机文件的文件权限

使用绑定挂载时，确保 Docker 具有访问主机目录的必要权限至关重要。要授予读/写访问权限，可以在容器创建期间在 `-v` 或 `--mount` 标志中使用 `:ro`（只读）或 `:rw`（读写）标志。
例如，以下命令授予读写访问权限。

```console
$ docker run -v HOST-DIRECTORY:/CONTAINER-DIRECTORY:rw nginx
```

只读绑定挂载允许容器访问主机上挂载的文件进行读取，但不能更改或删除这些文件。通过读写绑定挂载，容器可以修改或删除挂载的文件，并且这些更改或删除也将反映在主机系统上。只读绑定挂载可确保主机上的文件不会被容器意外修改或删除。

> **同步文件共享 (Synchronized File Share)**
>
> 随着代码库变得越来越大，传统的绑定挂载等文件共享方法可能会变得低效或缓慢，尤其是在需要频繁访问文件的开发环境中。[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md)通过利用同步的文件系统缓存来提高绑定挂载的性能。这种优化确保了主机与虚拟机 (VM) 之间的文件访问快速且高效。

## 试一试

在本实践指南中，您将练习如何创建和使用绑定挂载在主机和容器之间共享文件。

### 运行容器

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 使用以下命令启动一个使用 [httpd](https://hub.docker.com/_/httpd) 镜像的容器：

   ```console
   $ docker run -d -p 8080:80 --name my_site httpd:2.4
   ```

   这将在后台启动 `httpd` 服务，并将网页发布到主机的 `8080` 端口。

3. 打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 或使用 curl 命令验证它是否正常工作。

    ```console
    $ curl localhost:8080
    ```


### 使用绑定挂载

使用绑定挂载，您可以将主机电脑上的配置文件映射到容器内的特定位置。在这个例子中，您将看到如何通过使用绑定挂载来改变网页的外观：

1. 使用 Docker Desktop Dashboard 删除现有容器：

   ![Docker Desktop Dashboard 截图，显示如何删除 httpd 容器](images/delete-httpd-container.webp?border=true)


2. 在您的主机系统上创建一个名为 `public_html` 的新目录。

    ```console
    $ mkdir public_html
    ```

3. 进入新创建的目录 `public_html` 并创建一个名为 `index.html` 的文件，内容如下。这是一个基础的 HTML 文档，它创建了一个简单的网页，用一只友好的鲸鱼欢迎您。

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

4. 现在是运行容器的时候了。`--mount` 和 `-v` 示例产生相同的结果。除非您在运行第一个容器后移除 `my_site` 容器，否则您无法同时运行它们。

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
   > 在 Windows PowerShell 中使用 `-v` 或 `--mount` 标志时，您需要提供目录的绝对路径，而不仅仅是 `./`。这是因为 PowerShell 处理相对路径的方式与 bash（常用于 Mac 和 Linux 环境）不同。



   现在一切都启动并运行了，您应该能够通过 [http://localhost:8080](http://localhost:8080) 访问该站点，并看到一个新的网页，用一只友好的鲸鱼欢迎您。


### 在 Docker Desktop Dashboard 上访问文件

1. 您可以通过选择容器的 **Files**（文件）选项卡，然后选择 `/usr/local/apache2/htdocs/` 目录中的文件来查看容器内挂载的文件。然后，选择 **Open file editor**（打开文件编辑器）。


   ![Docker Desktop Dashboard 截图，显示容器内挂载的文件](images/mounted-files.webp?border=true)

2. 删除主机上的文件，并验证容器中的文件是否也被删除。您会发现 Docker Desktop Dashboard 的 **Files** 下不再存在该文件。


   ![Docker Desktop Dashboard 截图，显示容器内已删除的文件](images/deleted-files.webp?border=true)


3. 在主机系统上重新创建该 HTML 文件，并观察该文件重新出现在 Docker Desktop Dashboard 的 **Containers** 下的 **Files** 选项卡中。到目前为止，您也将能够访问该网站。



### 停止您的容器

容器将继续运行，直到您将其停止。

1. 转到 Docker Desktop Dashboard 中的 **Containers**（容器）视图。

2. 找到您想要停止的容器。

3. 选择 Actions（操作）列中的 **Delete**（删除）操作。

![Docker Desktop Dashboard 截图，显示如何删除容器](images/delete-the-container.webp?border=true)


## 其他资源

以下资源将帮助您了解有关绑定挂载的更多信息：

* [在 Docker 中管理数据](/storage/)
* [卷 (Volumes)](/storage/volumes/)
* [绑定挂载 (Bind mounts)](/storage/bind-mounts/)
* [运行容器](/reference/run/)
* [排查存储错误](/storage/troubleshooting_volume_errors/)
* [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/)

## 下一步

现在您已经了解了与容器共享本地文件，是时候了解多容器应用程序了。

{{< button text="多容器应用程序" url="Multi-container applications" >}}
