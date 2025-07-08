---
title: 检查您的构建配置
linkTitle: 构建检查
params:
  sidebar:
    badge:
      color: green
      text: 新
weight: 30
description: 了解如何使用构建检查来验证您的构建配置。
keywords: build, buildx, buildkit, checks, validate, configuration, lint
---

{{< summary-bar feature_name="构建检查" >}}

构建检查是 Dockerfile 1.8 中引入的一项功能。它允许您在执行构建之前验证您的构建配置并进行一系列检查。将其视为 Dockerfile 和构建选项的高级 linting 形式，或构建的空运行模式。

您可以在[构建检查参考](/reference/build-checks/)中找到可用检查的列表以及每个检查的描述。

## 构建检查的工作原理

通常，当您运行构建时，Docker 会按照指定执行 Dockerfile 和构建选项中的构建步骤。通过构建检查，Docker 不会执行构建步骤，而是检查您提供的 Dockerfile 和选项，并报告它检测到的任何问题。

构建检查对于以下情况很有用：

- 在运行构建之前验证您的 Dockerfile 和构建选项。
- 确保您的 Dockerfile 和构建选项与最新的最佳实践保持同步。
- 识别 Dockerfile 和构建选项中潜在的问题或反模式。

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Dockerfile 编辑体验？
> 查看 [Docker VS Code 扩展（Beta）](https://marketplace.visualstudio.com/items?itemName=docker.docker)，了解 linting、代码导航和漏洞扫描。

## 带检查的构建

构建检查支持以下版本：

- Buildx 0.15.0 及更高版本
- [docker/build-push-action](https://github.com/docker/build-push-action) 6.6.0 及更高版本
- [docker/bake-action](https://github.com/docker/bake-action) 5.6.0 及更高版本

默认情况下，调用构建会运行检查，并在构建输出中显示任何违规。例如，以下命令既构建镜像又运行检查：

```console
$ docker build .
[+] 正在构建 3.5s (11/11) 完成
...

发现 1 个警告（使用 --debug 展开）：
  - Lint 规则 'JSONArgsRecommended'：建议 CMD 使用 JSON 参数以防止与 OS 信号相关的意外行为（第 7 行）

```

在此示例中，构建成功运行，但报告了[JSONArgsRecommended](/reference/build-checks/json-args-recommended/)警告，因为 `CMD` 指令应使用 JSON 数组语法。

使用 GitHub Actions，检查会显示在拉取请求的 diff 视图中。

```yaml
name: 构建并推送 Docker 镜像
on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 构建并推送
        uses: docker/build-push-action@v6.6.0
```

![GitHub Actions 构建检查注释](./images/gha-check-annotations.png)

### 更详细的输出

常规 `docker build` 的检查警告会显示一个简洁的消息，其中包含规则名称、消息以及 Dockerfile 中问题所在的行号。如果您想查看有关检查的更详细信息，可以使用 `--debug` 标志。例如：

```console
$ docker --debug build .
[+] 正在构建 3.5s (11/11) 完成
...

 发现 1 个警告：
 - JSONArgsRecommended: 建议 CMD 使用 JSON 参数以防止与 OS 信号相关的意外行为（第 4 行）
建议 ENTRYPOINT/CMD 使用 JSON 参数以防止与 OS 信号相关的意外行为
更多信息：https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
Dockerfile:4
--------------------
   2 |
   3 |     FROM alpine
   4 | >>> CMD echo "Hello, world!"
   5 |
--------------------

```

使用 `--debug` 标志，输出包括指向检查文档的链接，以及发现问题的 Dockerfile 片段。

## 不构建而检查构建

要在不实际构建的情况下运行构建检查，您可以像往常一样使用 `docker build` 命令，但要添加 `--check` 标志。
这是一个示例：

```console
$ docker build --check .
```

此命令不会执行构建步骤，而只会运行检查并报告发现的任何问题。如果存在任何问题，它们将在输出中报告。例如：

```text {title="--check 的输出"}
[+] 正在构建 1.5s (5/5) 完成
=> [internal] 连接到本地控制器
=> [internal] 从 Dockerfile 加载构建定义
=> => 正在传输 Dockerfile: 253B
=> [internal] 加载 docker.io/library/node:22 的元数据
=> [auth] library/node:pull registry-1.docker.io 的令牌
=> [internal] 加载 .dockerignore
=> => 正在传输上下文: 50B
JSONArgsRecommended - https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
建议 ENTRYPOINT/CMD 使用 JSON 参数以防止与 OS 信号相关的意外行为
Dockerfile:7
--------------------
5 |
6 |     COPY index.js .
7 | >>> CMD node index.js
8 |
--------------------
```

此 `--check` 输出显示了检查的[详细消息](#more-verbose-output)。

与常规构建不同，如果使用 `--check` 标志时报告任何违规，则命令将以非零状态代码退出。

## 检查违规时构建失败

默认情况下，构建检查违规报告为警告，退出代码为 0。您可以配置 Docker 在报告违规时使构建失败，方法是在 Dockerfile 中使用 `check=error=true` 指令。这将在运行构建检查后，实际构建执行之前，导致构建出错。

```dockerfile {title=Dockerfile,linenos=true,hl_lines=2}
# syntax=docker/dockerfile:1
# check=error=true

FROM alpine
CMD echo "Hello, world!"
```

如果没有 `# check=error=true` 指令，此构建将以退出代码 0 完成。但是，有了此指令，构建检查违规将导致非零退出代码：

```console
$ docker build .
[+] 正在构建 1.5s (5/5) 完成
...

 发现 1 个警告（使用 --debug 展开）：
 - JSONArgsRecommended: 建议 CMD 使用 JSON 参数以防止与 OS 信号相关的意外行为（第 5 行）
Dockerfile:1
--------------------
   1 | >>> # syntax=docker/dockerfile:1
   2 |     # check=error=true
   3 |
--------------------
错误：发现 lint 违规，规则为：JSONArgsRecommended
$ echo $?
1
```

您还可以通过传递 `BUILDKIT_DOCKERFILE_CHECK` 构建参数在 CLI 上设置错误指令：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=error=true" .
```

## 跳过检查

默认情况下，构建镜像时会运行所有检查。如果您想跳过特定检查，可以在 Dockerfile 中使用 `check=skip` 指令。`skip` 参数接受您要跳过的检查 ID 的 CSV 字符串。
例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing

FROM alpine AS BASE_STAGE
CMD echo "Hello, world!"
```

构建此 Dockerfile 不会导致任何检查违规。

您还可以通过传递 `BUILDKIT_DOCKERFILE_CHECK` 构建参数来跳过检查，该参数包含您要跳过的检查 ID 的 CSV 字符串。例如：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing" .
```

要跳过所有检查，请使用 `skip=all` 参数：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all
```

## 结合错误和跳过参数进行检查指令

要同时跳过特定检查并在检查违规时出错，请将 `skip` 和 `error` 参数用分号 (`;`) 分隔传递给 Dockerfile 中的 `check` 指令或作为构建参数。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing;error=true
```

```console {title="构建参数"}
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing;error=true" .
```

## 实验性检查

在检查升级到稳定版之前，它们可能作为实验性检查提供。实验性检查默认禁用。要查看可用的实验性检查列表，请参阅[构建检查参考](/reference/build-checks/)。

要启用所有实验性检查，请将 `BUILDKIT_DOCKERFILE_CHECK` 构建参数设置为 `experimental=all`：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=experimental=all" .
```

您还可以使用 `check` 指令在 Dockerfile 中启用实验性检查：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=experimental=all
```

请注意，`experimental` 指令优先于 `skip` 指令，这意味着无论您设置了什么 `skip` 指令，实验性检查都将运行。例如，如果您设置了 `skip=all` 并启用了实验性检查，实验性检查仍将运行：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all;experimental=all
```

## 进一步阅读

有关使用构建检查的更多信息，请参阅：

- [构建检查参考](/reference/build-checks/)
- [使用 GitHub Actions 验证构建配置](/manuals/build/ci/github-actions/checks.md)
