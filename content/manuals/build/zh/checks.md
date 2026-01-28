---
title: 检查您的构建配置
linkTitle: 构建检查
params:
  sidebar:
    badge:
      color: green
      text: New
weight: 30
description: 了解如何使用构建检查来验证您的构建配置。
keywords: build, buildx, buildkit, checks, validate, configuration, lint
---

{{< summary-bar feature_name="Build checks" >}}

构建检查（Build checks）是 Dockerfile 1.8 中引入的功能。它允许您在执行构建之前验证构建配置并进行一系列检查。可以将其视为 Dockerfile 和构建选项的高级 lint 形式，或者构建的试运行模式。

您可以在[构建检查参考](/reference/build-checks/)中找到可用检查的列表及每项检查的描述。

## 构建检查的工作原理

通常，当您运行构建时，Docker 会按照 Dockerfile 和构建选项中指定的方式执行构建步骤。使用构建检查时，Docker 不会执行构建步骤，而是检查您提供的 Dockerfile 和选项，并报告它检测到的任何问题。

构建检查适用于：

- 在运行构建之前验证您的 Dockerfile 和构建选项。
- 确保您的 Dockerfile 和构建选项符合最新的最佳实践。
- 识别 Dockerfile 和构建选项中的潜在问题或反模式。

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Dockerfile 编辑体验？
> 请查看 [Docker VS Code 扩展（Beta 版）](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它提供 lint、代码导航和漏洞扫描功能。

## 带检查的构建

构建检查支持于：

- Buildx 版本 0.15.0 及更高版本
- [docker/build-push-action](https://github.com/docker/build-push-action) 版本 6.6.0 及更高版本
- [docker/bake-action](https://github.com/docker/bake-action) 版本 5.6.0 及更高版本

调用构建时默认会运行检查，并在构建输出中显示任何违规。例如，以下命令既构建镜像又运行检查：

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED
...

1 warning found (use --debug to expand):
  - Lint Rule 'JSONArgsRecommended': JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 7)

```

在此示例中，构建成功运行，但报告了一个 [JSONArgsRecommended](/reference/build-checks/json-args-recommended/) 警告，因为 `CMD` 指令应该使用 JSON 数组语法。

使用 GitHub Actions 时，检查会显示在拉取请求的差异视图中。

```yaml
name: Build and push Docker images
on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build and push
        uses: docker/build-push-action@v6.6.0
```

![GitHub Actions 构建检查注释](./images/gha-check-annotations.png)

### 更详细的输出

常规 `docker build` 的检查警告会显示一条简洁的消息，包含规则名称、消息以及问题在 Dockerfile 中起源的行号。如果您想查看有关检查的更详细信息，可以使用 `--debug` 标志。例如：

```console
$ docker --debug build .
[+] Building 3.5s (11/11) FINISHED
...

 1 warning found:
 - JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 4)
JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals
More info: https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
Dockerfile:4
--------------------
   2 |
   3 |     FROM alpine
   4 | >>> CMD echo "Hello, world!"
   5 |
--------------------

```

使用 `--debug` 标志时，输出包含检查文档的链接，以及发现问题的 Dockerfile 代码片段。

## 不构建只检查

要运行构建检查而不实际构建，您可以像平常一样使用 `docker build` 命令，但需要添加 `--check` 标志。以下是一个示例：

```console
$ docker build --check .
```

此命令不会执行构建步骤，而只运行检查并报告它发现的任何问题。如果有任何问题，它们将在输出中报告。例如：

```text {title="Output with --check"}
[+] Building 1.5s (5/5) FINISHED
=> [internal] connecting to local controller
=> [internal] load build definition from Dockerfile
=> => transferring dockerfile: 253B
=> [internal] load metadata for docker.io/library/node:22
=> [auth] library/node:pull token for registry-1.docker.io
=> [internal] load .dockerignore
=> => transferring context: 50B
JSONArgsRecommended - https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals
Dockerfile:7
--------------------
5 |
6 |     COPY index.js .
7 | >>> CMD node index.js
8 |
--------------------
```

使用 `--check` 时，此输出显示检查的[详细消息](#more-verbose-output)。

与常规构建不同，如果使用 `--check` 标志时报告了任何违规，命令将以非零状态码退出。

## 在检查违规时使构建失败

默认情况下，构建的检查违规会作为警告报告，退出码为 0。您可以配置 Docker 在报告违规时使构建失败，方法是在 Dockerfile 中使用 `check=error=true` 指令。这将导致在运行构建检查后、实际构建执行之前，构建因错误而退出。

```dockerfile {title=Dockerfile,linenos=true,hl_lines=2}
# syntax=docker/dockerfile:1
# check=error=true

FROM alpine
CMD echo "Hello, world!"
```

如果没有 `# check=error=true` 指令，此构建将以退出码 0 完成。但是，有了该指令，构建检查违规会导致非零退出码：

```console
$ docker build .
[+] Building 1.5s (5/5) FINISHED
...

 1 warning found (use --debug to expand):
 - JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 5)
Dockerfile:1
--------------------
   1 | >>> # syntax=docker/dockerfile:1
   2 |     # check=error=true
   3 |
--------------------
ERROR: lint violation found for rules: JSONArgsRecommended
$ echo $?
1
```

您也可以通过传递 `BUILDKIT_DOCKERFILE_CHECK` 构建参数在 CLI 上设置 error 指令：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=error=true" .
```

## 跳过检查

默认情况下，构建镜像时会运行所有检查。如果您想跳过特定检查，可以在 Dockerfile 中使用 `check=skip` 指令。`skip` 参数接受要跳过的检查 ID 的 CSV 字符串。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing

FROM alpine AS BASE_STAGE
CMD echo "Hello, world!"
```

构建此 Dockerfile 不会产生检查违规。

您也可以通过传递包含要跳过的检查 ID 的 CSV 字符串的 `BUILDKIT_DOCKERFILE_CHECK` 构建参数来跳过检查。例如：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing" .
```

要跳过所有检查，请使用 `skip=all` 参数：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all
```

## 组合检查指令的 error 和 skip 参数

要同时跳过特定检查并在检查违规时报错，请在 Dockerfile 中的 `check` 指令或构建参数中传递用分号（`;`）分隔的 `skip` 和 `error` 参数。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing;error=true
```

```console {title="Build argument"}
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing;error=true" .
```

## 实验性检查

在检查被提升为稳定版之前，它们可能作为实验性检查提供。实验性检查默认是禁用的。要查看可用的实验性检查列表，请参阅[构建检查参考](/reference/build-checks/)。

要启用所有实验性检查，请将 `BUILDKIT_DOCKERFILE_CHECK` 构建参数设置为 `experimental=all`：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=experimental=all" .
```

您也可以在 Dockerfile 中使用 `check` 指令启用实验性检查：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=experimental=all
```

要有选择地启用实验性检查，您可以将要启用的检查 ID 的 CSV 字符串传递给 Dockerfile 中的 `check` 指令或作为构建参数。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=experimental=JSONArgsRecommended,StageNameCasing
```

请注意，`experimental` 指令优先于 `skip` 指令，这意味着无论您设置了什么 `skip` 指令，实验性检查都会运行。例如，如果您设置了 `skip=all` 并启用了实验性检查，实验性检查仍然会运行：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all;experimental=all
```

## 延伸阅读

有关使用构建检查的更多信息，请参阅：

- [构建检查参考](/reference/build-checks/)
- [使用 GitHub Actions 验证构建配置](/manuals/build/ci/github-actions/checks.md)
