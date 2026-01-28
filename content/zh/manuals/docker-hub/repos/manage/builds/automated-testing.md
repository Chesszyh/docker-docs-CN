---
description: 自动测试
keywords: Automated, testing, repository
title: 仓库自动测试
weight: 30
aliases:
- /docker-hub/builds/automated-testing/
---

> [!NOTE]
>
> 自动构建需要 Docker Pro、Team 或 Business 订阅。

Docker Hub 可以使用容器自动测试您源代码仓库的更改。您可以在任何 Docker Hub 仓库上启用 `Autotest`（自动测试），对源代码仓库的每个拉取请求运行测试，从而创建持续集成测试服务。

启用 `Autotest` 会为测试目的构建镜像，但不会自动将构建的镜像推送到 Docker 仓库。如果您想将构建的镜像推送到 Docker Hub 仓库，请启用[自动构建](index.md)。

## 设置自动测试文件

要设置自动测试，请创建一个 `docker-compose.test.yml` 文件，其中定义一个 `sut` 服务来列出要运行的测试。
`docker-compose.test.yml` 文件应位于包含用于构建镜像的 Dockerfile 的同一目录中。

例如：

```yaml
services:
  sut:
    build: .
    command: run_tests.sh
```

上面的示例构建仓库，并使用构建的镜像在容器内运行 `run_tests.sh` 文件。

您可以在此文件中定义任意数量的链接服务。唯一的要求是必须定义 `sut`。它的返回码决定测试是否通过。如果 `sut` 服务返回 `0`，则测试通过，否则测试失败。

> [!NOTE]
>
> 只有 `sut` 服务以及 [`depends_on`](/reference/compose-file/services.md#depends_on) 中列出的所有其他服务会被启动。如果您有轮询其他服务变化的服务，请确保将轮询服务包含在 [`depends_on`](/reference/compose-file/services.md#depends_on) 列表中，以确保所有服务都能启动。

如果需要，您可以定义多个 `docker-compose.test.yml` 文件。任何以 `.test.yml` 结尾的文件都用于测试，测试按顺序运行。
您还可以使用[自定义构建钩子](advanced.md#override-build-test-or-push-commands)来进一步自定义测试行为。

> [!NOTE]
>
> 如果您启用了自动构建，它们也会运行 `test.yml` 文件中定义的任何测试。

## 在仓库上启用自动测试

要在源代码仓库上启用测试，您必须首先在 Docker Hub 中创建一个关联的构建仓库。您的 `Autotest` 设置在与[自动构建](index.md)相同的页面上配置，但是您不需要启用自动构建就可以使用自动测试。自动构建是按分支或标签启用的，您完全不需要启用它。

只有配置为使用自动构建的分支才会将镜像推送到 Docker 仓库，无论 Autotest 设置如何。

1. 登录 Docker Hub 并选择 **My Hub** > **Repositories**。

2. 选择您想要启用 `Autotest` 的仓库。

3. 从仓库视图中，选择 **Builds** 选项卡。

4. 选择 **Configure automated builds**。

5. 按照[自动构建](index.md)中的说明配置自动构建设置。

    至少您必须配置：

    * 源代码仓库
    * 构建位置
    * 至少一个构建规则

6. 选择您的 **Autotest** 选项。

    可用的选项如下：

    * `Off`：不进行额外的测试构建。仅当测试被配置为自动构建的一部分时才运行测试。

    * `Internal pull requests`：对匹配构建规则的分支的任何拉取请求运行测试构建，但仅当拉取请求来自同一源仓库时。

    * `Internal and external pull requests`：对匹配构建规则的分支的任何拉取请求运行测试构建，包括拉取请求来自外部源仓库的情况。

    > [!IMPORTANT]
    >
    >出于安全目的，公共仓库上的外部拉取请求的自动测试受到限制。私有镜像不会被拉取，Docker Hub 中定义的环境变量也不可用。自动构建继续正常工作。

7. 选择 **Save** 保存设置，或选择 **Save and build** 保存并运行初始测试。

## 检查测试结果

在仓库的详情页面中，选择 **Timeline**。

从此选项卡，您可以查看仓库的任何待处理、进行中、成功和失败的构建及测试运行。

您可以选择任何时间线条目来查看每次测试运行的日志。
