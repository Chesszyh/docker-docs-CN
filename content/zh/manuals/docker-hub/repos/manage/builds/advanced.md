---
description: 自动构建
keywords: automated, build, images
title: 自动构建和自动测试的高级选项
linkTitle: 高级选项
weight: 40
aliases:
- /docker-hub/builds/advanced/
---

> [!NOTE]
>
> 自动构建需要 Docker Pro、Team 或 Business 订阅。

以下选项允许您自定义自动构建和自动测试流程。

## 构建和测试的环境变量

构建过程会设置若干实用的环境变量，这些变量在自动构建、自动测试以及执行钩子时可用。

> [!NOTE]
>
> 这些环境变量仅对构建和测试过程可用，不会影响您服务的运行环境。

* `SOURCE_BRANCH`：当前正在测试的分支或标签的名称。
* `SOURCE_COMMIT`：正在测试的提交的 SHA1 哈希值。
* `COMMIT_MSG`：正在测试和构建的提交的消息。
* `DOCKER_REPO`：正在构建的 Docker 仓库的名称。
* `DOCKERFILE_PATH`：当前正在构建的 dockerfile 路径。
* `DOCKER_TAG`：正在构建的 Docker 仓库标签。
* `IMAGE_NAME`：正在构建的 Docker 仓库的名称和标签。（此变量是 `DOCKER_REPO`:`DOCKER_TAG` 的组合。）

如果您在 `docker-compose.test.yml` 文件中使用这些构建环境变量进行自动测试，请在 `sut` 服务的 environment 中声明它们，如下所示。

```yaml
services:
  sut:
    build: .
    command: run_tests.sh
    environment:
      - SOURCE_BRANCH
```


## 覆盖构建、测试或推送命令

Docker Hub 允许您在自动构建和测试过程中使用钩子（hooks）来覆盖和自定义 `build`、`test` 和 `push` 命令。例如，您可以使用构建钩子来设置仅在构建过程中使用的构建参数。您还可以设置[自定义构建阶段钩子](#custom-build-phase-hooks)来在这些命令之间执行操作。

> [!IMPORTANT]
>
>请谨慎使用这些钩子。这些钩子文件的内容会替换基本的 `docker` 命令，因此您必须在钩子中包含类似的构建、测试或推送命令，否则您的自动化流程将无法完成。

要覆盖这些阶段，请在源代码仓库中与 Dockerfile 同级的目录下创建一个名为 `hooks` 的文件夹。创建名为 `hooks/build`、`hooks/test` 或 `hooks/push` 的文件，并包含构建器进程可以执行的命令，例如 `docker` 和 `bash` 命令（需要适当地以 `#!/bin/bash` 作为前缀）。

这些钩子在 [Ubuntu](https://releases.ubuntu.com/) 实例上运行，该实例包含 Perl 或 Python 等解释器，以及 `git` 或 `curl` 等实用工具。请参阅 [Ubuntu 文档](https://ubuntu.com/) 获取可用解释器和实用工具的完整列表。

## 自定义构建阶段钩子

您可以通过创建钩子在构建过程的各阶段之间运行自定义命令。钩子允许您为自动构建和自动测试流程提供额外的指令。

在源代码仓库中与 Dockerfile 同级的目录下创建一个名为 `hooks` 的文件夹。将定义钩子的文件放在该文件夹中。钩子文件可以包含 `docker` 命令和 `bash` 命令，只要它们以 `#!/bin/bash` 作为适当的前缀。构建器会在每个步骤之前和之后执行文件中的命令。

可用的钩子如下：

* `hooks/post_checkout`
* `hooks/pre_build`
* `hooks/post_build`
* `hooks/pre_test`
* `hooks/post_test`
* `hooks/pre_push`（仅在执行构建规则或[自动构建](index.md)时使用）
* `hooks/post_push`（仅在执行构建规则或[自动构建](index.md)时使用）

### 构建钩子示例

#### 覆盖 "build" 阶段以设置变量

Docker Hub 允许您在钩子文件中或从自动构建界面定义构建环境变量，然后可以在钩子中引用这些变量。

以下示例定义了一个构建钩子，该钩子使用 `docker build` 参数根据 Docker Hub 构建设置中定义的变量值来设置 `CUSTOM` 变量。`$DOCKERFILE_PATH` 是您提供的要构建的 Dockerfile 名称的变量，`$IMAGE_NAME` 是正在构建的镜像的名称。

```console
$ docker build --build-arg CUSTOM=$VAR -f $DOCKERFILE_PATH -t $IMAGE_NAME .
```

> [!IMPORTANT]
>
> `hooks/build` 文件会覆盖构建器使用的基本 `docker build` 命令，因此您必须在钩子中包含类似的构建命令，否则自动构建将失败。

请参阅 [docker build 文档](/reference/cli/docker/buildx/build.md#build-arg)了解更多关于 Docker 构建时变量的信息。

#### 推送到多个仓库

默认情况下，构建过程仅将镜像推送到配置了构建设置的仓库。如果您需要将同一镜像推送到多个仓库，可以设置 `post_push` 钩子来添加额外的标签并推送到更多仓库。

```console
$ docker tag $IMAGE_NAME $DOCKER_REPO:$SOURCE_COMMIT
$ docker push $DOCKER_REPO:$SOURCE_COMMIT
```

## 源仓库或分支克隆

当 Docker Hub 从源代码仓库拉取分支时，它执行浅克隆（shallow clone），仅克隆指定分支的最新提交。这样做的优点是可以最大限度地减少从仓库传输的数据量，并加快构建速度，因为它只拉取必要的最少代码。

因此，如果您需要执行依赖于其他分支的自定义操作，例如 `post_push` 钩子，您将无法检出该分支，除非您执行以下操作之一：

* 您可以通过以下方式获取目标分支的浅检出：

    ```console
    $ git fetch origin branch:mytargetbranch --depth 1
    ```

* 您也可以"取消浅克隆"（unshallow），这会获取整个 Git 历史记录（可能需要很长时间/传输大量数据），方法是在 fetch 命令中使用 `--unshallow` 标志：

    ```console
    $ git fetch --unshallow origin
    ```
