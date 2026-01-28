---
title: 理解镜像层
keywords: concepts, build, images, container, docker desktop
description: 这个概念页面将教您有关容器镜像层的知识。
summary: |
  您是否想过镜像是如何工作的？本指南将帮助您理解镜像层 - 容器镜像的基本构建块。您将全面了解如何创建、堆叠和利用层来确保高效和优化的容器。
weight: 1
aliases: 
 - /guides/docker-concepts/building-images/understanding-image-layers/
---

{{< youtube-embed wJwqtAkmtQA >}}

## 说明

正如您在[什么是镜像？](../the-basics/what-is-an-image.md) 中了解到的，容器镜像由层组成。每一层一旦创建，就是不可变的。但这实际上意味着什么？这些层又是如何用于创建容器可以使用的文件系统的呢？

### 镜像层

镜像中的每一层都包含一组文件系统更改 - 添加、删除或修改。让我们看一个理论上的镜像：

1. 第一层添加了基本命令和包管理器，例如 apt。
2. 第二层安装了 Python 运行时和用于依赖项管理的 pip。
3. 第三层复制了应用程序特定的 requirements.txt 文件。
4. 第四层安装了该应用程序特定的依赖项。
5. 第五层复制了应用程序的实际源代码。

这个例子可能看起来像这样：

![显示镜像层概念的流程图屏幕截图](images/container_image_layers.webp?border=true)

这样做是有益的，因为它允许层在镜像之间重用。例如，假设您想创建另一个 Python 应用程序。由于分层，您可以利用相同的 Python 基础。这将使构建更快，并减少分发镜像所需的存储和带宽量。镜像分层可能类似于以下内容：

![显示镜像分层优势的流程图屏幕截图](images/container_image_layer_reuse.webp?border=true)

层允许您通过重用他人的基础层来扩展镜像，从而允许您仅添加应用程序需要的数据。

### 堆叠层

分层是通过内容寻址存储和联合文件系统实现的。虽然这会涉及到技术细节，但其工作原理如下：

1. 下载每一层后，它会被解压到主机文件系统上自己的目录中。
2. 当您从镜像运行容器时，会创建一个联合文件系统，其中层彼此堆叠，创建一个新的统一视图。
3. 当容器启动时，其根目录使用 `chroot` 设置为此统一目录的位置。

创建联合文件系统时，除了镜像层之外，还会专门为正在运行的容器创建一个目录。这允许容器在保持原始镜像层不变的情况下更改文件系统。这使您能够从同一个底层镜像运行多个容器。

## 试一试

在这个动手指南中，您将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令手动创建新的镜像层。请注意，您很少会以这种方式创建镜像，因为通常您会 [使用 Dockerfile](./writing-a-dockerfile.md)。但是，这使您更容易理解一切是如何工作的。

### 创建基础镜像

在第一步中，您将创建自己的基础镜像，然后在接下来的步骤中使用它。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 在终端中，运行以下命令以启动新容器：

    ```console
    $ docker run --name=base-container -ti ubuntu
    ```

    一旦镜像下载完成并且容器启动，您应该会看到一个新的 shell 提示符。这是在您的容器内运行的。它看起来类似于以下内容（容器 ID 会有所不同）：

    ```console
    root@d8c5ca119fcd:/#
    ```

3. 在容器内，运行以下命令以安装 Node.js：

    ```console
    $ apt update && apt install -y nodejs
    ```

    运行此命令时，它会在容器内下载并安装 Node。在联合文件系统的上下文中，这些文件系统更改发生在此容器唯一的目录中。

4. 通过运行以下命令验证 Node 是否已安装：

    ```console
    $ node -e 'console.log("Hello world!")'
    ```

    然后您应该会在控制台中看到 "Hello world!"。

5. 现在您已经安装了 Node，准备将您所做的更改保存为新的镜像层，您可以从中启动新容器或构建新镜像。为此，您将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令。在一个新终端中运行以下命令：

    ```console
    $ docker container commit -m "Add node" base-container node-base
    ```

6. 使用 `docker image history` 命令查看镜像的层：

    ```console
    $ docker image history node-base
    ```

    您将看到类似以下的输出：

    ```console
    IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
    d5c1fca2cdc4   10 seconds ago   /bin/bash                                       126MB     Add node
    2b7cc08dcdbb   5 weeks ago      /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>      5 weeks ago      /bin/sh -c #(nop) ADD file:07cdbabf782942af0…   69.2MB
    <missing>      5 weeks ago      /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago      /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago      /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
    <missing>      5 weeks ago      /bin/sh -c #(nop)  ARG RELEASE                  0B
    ```

    请注意顶行上的 "Add node" 注释。此层包含您刚刚进行的 Node.js 安装。

7. 要证明您的镜像已安装 Node，您可以使用此新镜像启动一个新容器：

    ```console
    $ docker run node-base node -e "console.log('Hello again')"
    ```

    这样，您应该在终端中得到 "Hello again" 输出，表明 Node 已安装并正在工作。

8. 现在您已完成基础镜像的创建，可以删除该容器：

    ```console
    $ docker rm -f base-container
    ```

> **基础镜像定义**
>
> 基础镜像 (Base Image) 是构建其他镜像的基础。可以使用任何镜像作为基础镜像。但是，有些镜像是特意作为构建块创建的，为应用程序提供基础或起点。
>
> 在这个例子中，您可能不会部署这个 `node-base` 镜像，因为它实际上还没有做任何事情。但它是您可以用于其他构建的基础。

### 构建应用程序镜像

现在您有了一个基础镜像，您可以扩展该镜像以构建其他镜像。

1. 使用新创建的 node-base 镜像启动一个新容器：

    ```console
    $ docker run --name=app-container -ti node-base
    ```

2. 在此容器内，运行以下命令以创建一个 Node 程序：

    ```console
    $ echo 'console.log("Hello from an app")' > app.js
    ```

    要运行此 Node 程序，您可以使用以下命令并在屏幕上查看打印的消息：

    ```console
    $ node app.js
    ```

3. 在另一个终端中，运行以下命令将此容器的更改保存为新镜像：

    ```console
    $ docker container commit -c "CMD node app.js" -m "Add app" app-container sample-app
    ```

    此命令不仅创建了一个名为 `sample-app` 的新镜像，还向镜像添加了额外的配置以设置启动容器时的默认命令。在这种情况下，您将其设置为自动运行 `node app.js`。

4. 在容器外部的终端中，运行以下命令以查看更新后的层：

    ```console
    $ docker image history sample-app
    ```

    然后您将看到类似于以下的输出。请注意，顶层注释为 "Add app"，下一层为 "Add node"：

    ```console
    IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
    c1502e2ec875   About a minute ago   /bin/bash                                       33B       Add app
    5310da79c50a   4 minutes ago        /bin/bash                                       126MB     Add node
    2b7cc08dcdbb   5 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>      5 weeks ago          /bin/sh -c #(nop) ADD file:07cdbabf782942af0…   69.2MB
    <missing>      5 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago          /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
    <missing>      5 weeks ago          /bin/sh -c #(nop)  ARG RELEASE                  0B
    ```

5. 最后，使用全新的镜像启动一个新容器。由于您指定了默认命令，因此可以使用以下命令：

    ```console
    $ docker run sample-app
    ```

    您应该会看到您的问候语出现在终端中，来自您的 Node 程序。

6. 现在您已完成容器的操作，可以使用以下命令删除它们：

    ```console
    $ docker rm -f app-container
    ```

## 其他资源

如果您想深入了解所学内容，请查看以下资源：

* [`docker image history`](/reference/cli/docker/image/history/)
* [`docker container commit`](/reference/cli/docker/container/commit/)

## 下一步

正如前面暗示的那样，大多数镜像构建不使用 `docker container commit`。相反，您将使用 Dockerfile 为您自动执行这些步骤。

{{< button text="编写 Dockerfile" url="writing-a-dockerfile" >}}
