---
description: 使用 JupyterLab 和 Docker 运行、开发和共享数据科学项目
keywords: getting started, jupyter, notebook, python, jupyterlab, data science
title: 使用 JupyterLab 进行数据科学
toc_max: 2
summary: |
  使用 Docker 运行 Jupyter notebooks。
tags: [data-science]
languages: [python]
aliases:
  - /guides/use-case/jupyter/
params:
  time: 20 minutes
---

Docker 和 JupyterLab 是两个强大的工具，可以增强您的数据科学工作流程。在本指南中，您将学习如何将它们结合使用来创建和运行可重现的数据科学环境。本指南基于[使用 JupyterLab 和 Docker 增强 AI/ML 开发](https://www.docker.com/blog/supercharging-ai-ml-development-with-jupyterlab-and-docker/)。

在本指南中，您将学习如何：

- 在本地机器上运行带有 JupyterLab 的个人 Jupyter 服务器
- 自定义您的 JupyterLab 环境
- 与其他数据科学家共享您的 JupyterLab notebook 和环境

## 什么是 JupyterLab？

[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) 是一个围绕计算笔记本文档概念构建的开源应用程序。它支持代码共享和执行、数据处理、可视化，并提供一系列用于创建图形的交互功能。

## 为什么要一起使用 Docker 和 JupyterLab？

通过结合 Docker 和 JupyterLab，您可以受益于两种工具的优势，例如：

- 容器化确保所有部署中 JupyterLab 环境的一致性，消除兼容性问题。
- 容器化的 JupyterLab 通过消除手动环境设置的需要，简化了共享和协作。
- 容器为 JupyterLab 提供可扩展性，支持工作负载分配和使用 Kubernetes 等平台进行高效的资源管理。

## 前提条件

要按照本指南操作，您必须安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。

## 运行和访问 JupyterLab 容器

在终端中，运行以下命令来运行 JupyterLab 容器。

```console
$ docker run --rm -p 8889:8888 quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

以下是命令中值得注意的部分：

- `-p 8889:8888`：将主机的 8889 端口映射到容器的 8888 端口。
- `start-notebook.py --NotebookApp.token='my-token'`：设置访问令牌而不是使用随机令牌。

有关更多详细信息，请参阅 [Jupyter 服务器选项](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#jupyter-server-options)和 [docker run CLI 参考](/reference/cli/docker/container/run/)。

如果这是您第一次运行该镜像，Docker 将下载并运行它。下载镜像所需的时间取决于您的网络连接。

镜像下载并运行后，您可以访问容器。要访问容器，请在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

要停止容器，请在终端中按 `ctrl`+`c`。

要访问系统上现有的 notebook，您可以使用[绑定挂载](/storage/bind-mounts/)。打开终端并切换到现有 notebook 所在的目录。然后，根据您的操作系统运行以下命令。

{{< tabs >}}
{{< tab name="Mac / Linux" >}}

```console
$ docker run --rm -p 8889:8888 -v "$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< tab name="Windows (Command Prompt)" >}}

```console
$ docker run --rm -p 8889:8888 -v "%cd%":/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< tab name="Windows (PowerShell)" >}}

```console
$ docker run --rm -p 8889:8888 -v "$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< tab name="Windows (Git Bash)" >}}

```console
$ docker run --rm -p 8889:8888 -v "/$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< /tabs >}}

`-v` 选项告诉 Docker 将当前工作目录挂载到容器内的 `/home/jovyan/work`。默认情况下，Jupyter 镜像的根目录是 `/home/jovyan`，您只能在容器中访问或保存 notebook 到该目录。

现在您可以访问 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token) 并打开绑定挂载目录中包含的 notebook。

要停止容器，请在终端中按 `ctrl`+`c`。

Docker 还有卷（volumes），这是持久化 Docker 容器生成和使用的数据的首选机制。虽然绑定挂载依赖于主机的目录结构和操作系统，但卷完全由 Docker 管理。

## 保存和访问 notebooks

当您删除容器时，该容器中的所有数据都会被删除。要在容器外保存 notebooks，您可以使用[卷](/engine/storage/volumes/)。

### 使用卷运行 JupyterLab 容器

要使用卷启动容器，请打开终端并运行以下命令

```console
$ docker run --rm -p 8889:8888 -v jupyter-data:/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

`-v` 选项告诉 Docker 创建一个名为 `jupyter-data` 的卷并将其挂载到容器中的 `/home/jovyan/work`。

要访问容器，请在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。
Notebooks 现在可以保存到卷中，即使容器被删除也可以访问。

### 将 notebook 保存到卷

对于此示例，您将使用 scikit-learn 的 [Iris 数据集](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html)示例。

1. 打开 Web 浏览器并在 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token) 访问您的 JupyterLab 容器。

2. 在 **Launcher** 中，在 **Notebook** 下，选择 **Python 3**。

3. 在 notebook 中，指定以下内容以安装必要的包。

   ```console
   !pip install matplotlib scikit-learn
   ```

4. 选择播放按钮运行代码。

5. 在 notebook 中，指定以下代码。

   ```python
   from sklearn import datasets

   iris = datasets.load_iris()
   import matplotlib.pyplot as plt

   _, ax = plt.subplots()
   scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
   ax.set(xlabel=iris.feature_names[0], ylabel=iris.feature_names[1])
   _ = ax.legend(
      scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes"
   )
   ```

6. 选择播放按钮运行代码。您应该会看到 Iris 数据集的散点图。

7. 在顶部菜单中，选择 **File**，然后选择 **Save Notebook**。

8. 在 `work` 目录中指定一个名称以将 notebook 保存到卷中。例如，`work/mynotebook.ipynb`。

9. 选择 **Rename** 保存 notebook。

notebook 现在保存在卷中。

在终端中，按 `ctrl`+ `c` 停止容器。

现在，每当您使用该卷运行 Jupyter 容器时，您都可以访问保存的 notebook。

当您运行新容器并再次运行数据绘图代码时，它需要运行 `!pip install matplotlib scikit-learn` 并下载包。您可以通过创建自己的已安装包的镜像来避免每次运行新容器时重新安装包。

## 自定义您的 JupyterLab 环境

您可以使用 Docker 创建自己的 JupyterLab 环境并将其构建到镜像中。通过构建自己的镜像，您可以使用所需的包和工具自定义 JupyterLab 环境，并确保在不同部署中保持一致和可重现。构建自己的镜像还可以更轻松地与他人共享 JupyterLab 环境，或将其用作进一步开发的基础。

### 在 Dockerfile 中定义您的环境

在之前[将 notebook 保存到卷](#将-notebook-保存到卷)的 Iris 数据集示例中，每次运行新容器时都必须安装依赖项 `matplotlib` 和 `scikit-learn`。虽然该小示例中的依赖项下载和安装很快，但随着依赖项列表的增长，这可能会成为问题。可能还有其他您始终希望在环境中使用的工具、包或文件。

在这种情况下，您可以将依赖项作为镜像中环境的一部分安装。然后，每次运行容器时，依赖项将始终被安装。

您可以在 Dockerfile 中定义环境。Dockerfile 是一个文本文件，指示 Docker 如何创建 JupyterLab 环境的镜像。镜像包含运行 JupyterLab 时您想要和需要的所有内容，例如文件、包和工具。

在您选择的目录中，创建一个名为 `Dockerfile` 的新文本文件。在 IDE 或文本编辑器中打开 `Dockerfile`，然后添加以下内容。

```dockerfile
# syntax=docker/dockerfile:1

FROM quay.io/jupyter/base-notebook
RUN pip install --no-cache-dir matplotlib scikit-learn
```

此 Dockerfile 使用 `quay.io/jupyter/base-notebook` 镜像作为基础，然后运行 `pip` 安装依赖项。有关 Dockerfile 中指令的更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

在继续之前，保存对 `Dockerfile` 的更改。

### 将环境构建到镜像中

有了定义环境的 `Dockerfile` 后，您可以使用 `docker build` 使用您的 `Dockerfile` 构建镜像。

打开终端，切换到 `Dockerfile` 所在的目录，然后运行以下命令。

```console
$ docker build -t my-jupyter-image .
```

该命令从您的 `Dockerfile` 和上下文构建 Docker 镜像。`-t` 选项指定镜像的名称和标签，在本例中为 `my-jupyter-image`。`.` 表示当前目录是上下文，这意味着该目录中的文件可以在镜像创建过程中使用。

您可以通过在 Docker Desktop 中查看 `Images` 视图，或在终端中运行 `docker image ls` 命令来验证镜像是否已构建。您应该看到一个名为 `my-jupyter-image` 的镜像。

## 将镜像作为容器运行

要将镜像作为容器运行，请使用 `docker run` 命令。在 `docker run` 命令中，您将指定自己的镜像名称。

```console
$ docker run --rm -p 8889:8888 my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

要访问容器，请在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

您现在可以使用这些包而无需在 notebook 中安装它们。

1. 在 **Launcher** 中，在 **Notebook** 下，选择 **Python 3**。

2. 在 notebook 中，指定以下代码。

   ```python
   from sklearn import datasets

   iris = datasets.load_iris()
   import matplotlib.pyplot as plt

   _, ax = plt.subplots()
   scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
   ax.set(xlabel=iris.feature_names[0], ylabel=iris.feature_names[1])
   _ = ax.legend(
      scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes"
   )
   ```

3. 选择播放按钮运行代码。您应该会看到 Iris 数据集的散点图。

在终端中，按 `ctrl`+ `c` 停止容器。

## 使用 Compose 运行容器

Docker Compose 是一个用于定义和运行多容器应用程序的工具。在这种情况下，应用程序不是多容器应用程序，但 Docker Compose 可以通过在文件中定义所有 `docker run` 选项来简化运行。

### 创建 Compose 文件

要使用 Compose，您需要一个 `compose.yaml` 文件。在与 `Dockerfile` 相同的目录中，创建一个名为 `compose.yaml` 的新文件。

在 IDE 或文本编辑器中打开 `compose.yaml` 文件并添加以下内容。

```yaml
services:
  jupyter:
    build:
      context: .
    ports:
      - 8889:8888
    volumes:
      - jupyter-data:/home/jovyan/work
    command: start-notebook.py --NotebookApp.token='my-token'

volumes:
  jupyter-data:
    name: jupyter-data
```

此 Compose 文件指定了您在 `docker run` 命令中使用的所有选项。有关 Compose 指令的更多详细信息，请参阅 [Compose 文件参考](/reference/compose-file/_index.md)。

在继续之前，保存对 `compose.yaml` 文件的更改。

### 使用 Compose 运行容器

打开终端，切换到 `compose.yaml` 文件所在的位置，然后运行以下命令。

```console
$ docker compose up --build
```

此命令构建您的镜像并使用 `compose.yaml` 文件中指定的指令将其作为容器运行。`--build` 选项确保您的镜像被重新构建，如果您对 `Dockerfile` 进行了更改，这是必要的。

要访问容器，请在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

在终端中，按 `ctrl`+ `c` 停止容器。

## 共享您的工作

通过共享您的镜像和 notebook，您可以创建一个可移植且可复制的研究环境，其他数据科学家可以轻松访问和使用。此过程不仅促进协作，还确保您的工作在可以无兼容性问题运行的环境中得到保存。

要共享您的镜像和数据，您将使用 [Docker Hub](https://hub.docker.com/)。Docker Hub 是一个基于云的注册表服务，可让您共享和分发容器镜像。

### 共享您的镜像

1. [注册](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade)或登录 [Docker Hub](https://hub.docker.com)。

2. 重命名您的镜像，以便 Docker 知道要推送到哪个仓库。打开终端并运行以下 `docker tag` 命令。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker tag my-jupyter-image YOUR-USER-NAME/my-jupyter-image
   ```

3. 运行以下 `docker push` 命令将镜像推送到 Docker Hub。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker push YOUR-USER-NAME/my-jupyter-image
   ```

4. 验证您已将镜像推送到 Docker Hub。
   1. 转到 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **Repositories**。
   3. 查看仓库的 **Last pushed** 时间。

其他用户现在可以使用 `docker run` 命令下载并运行您的镜像。他们需要将 `YOUR-USER-NAME` 替换为您的 Docker ID。

```console
$ docker run --rm -p 8889:8888 YOUR-USER-NAME/my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

### 共享您的卷

此示例使用 Docker Desktop 图形用户界面。或者，在命令行界面中，您可以[备份卷](/engine/storage/volumes/#back-up-a-volume)，然后[使用 ORAS CLI 推送](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md#push-a-volume)。

1. 登录 Docker Desktop。
2. 在 Docker Dashboard 中，选择 **Volumes**。
3. 通过选择名称来选择 **jupyter-data** 卷。
4. 选择 **Exports** 选项卡。
5. 选择 **Quick export**。
6. 对于 **Location**，选择 **Registry**。
7. 在 **Registry** 下的文本框中，指定您的 Docker ID、卷的名称和标签。例如，`YOUR-USERNAME/jupyter-data:latest`。
8. 选择 **Save**。
9. 验证您已将卷导出到 Docker Hub。
   1. 转到 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **Repositories**。
   3. 查看仓库的 **Last pushed** 时间。

其他用户现在可以下载并导入您的卷。要导入卷然后与您的镜像一起运行：

1. 登录 Docker Desktop。
2. 在 Docker Dashboard 中，选择 **Volumes**。
3. 选择 **Create** 创建新卷。
4. 为新卷指定名称。对于此示例，使用 `jupyter-data-2`。
5. 选择 **Create**。
6. 在卷列表中，通过选择名称来选择 **jupyter-data-2** 卷。
7. 选择 **Import**。
8. 对于 **Location**，选择 **Registry**。
9. 在 **Registry** 下的文本框中，指定与您导出卷的仓库相同的名称。例如，`YOUR-USERNAME/jupyter-data:latest`。
10. 选择 **Import**。
11. 在终端中，运行 `docker run` 以使用导入的卷运行您的镜像。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker run --rm -p 8889:8888 -v jupyter-data-2:/home/jovyan/work YOUR-USER-NAME/my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
   ```

## 总结

在本指南中，您学习了如何利用 Docker 和 JupyterLab 创建可重现的数据科学环境，促进数据科学项目的开发和共享。这包括运行个人 JupyterLab 服务器、使用必要的工具和包自定义环境，以及与其他数据科学家共享 notebooks 和环境。

相关信息：

- [Dockerfile 参考](/reference/dockerfile/)
- [Compose 文件参考](/reference/compose-file/)
- [Docker CLI 参考](reference/cli/docker/)
- [Jupyter Docker Stacks 文档](https://jupyter-docker-stacks.readthedocs.io/en/latest/)
