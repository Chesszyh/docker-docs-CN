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
keywords: build, buildx, buildkit, 检查, 验证, 配置, lint
---

{{< summary-bar feature_name="Build checks" >}}

构建检查（Build checks）是 Dockerfile 1.8 中引入的一项功能。它允许您在执行构建之前验证构建配置并进行一系列检查。您可以将其视为 Dockerfile 和构建选项的一种高级 lint（静态分析）形式，或者是构建的空运行（dry-run）模式。

您可以在 [构建检查参考](/reference/build-checks/) 中找到可用检查的列表及其说明。

## 构建检查如何工作

通常，当您运行构建时，Docker 会按照指定的步骤执行 Dockerfile 中的构建步骤和构建选项。使用构建检查时，Docker 不执行构建步骤，而是检查您提供的 Dockerfile 和选项，并报告检测到的任何问题。

构建检查适用于：

- 在运行构建之前验证您的 Dockerfile 和构建选项。
- 确保您的 Dockerfile 和构建选项符合最新的最佳实践。
- 识别 Dockerfile 和构建选项中的潜在问题或反模式。

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Dockerfile 编辑体验吗？请查看 [Docker VS Code 扩展 (Beta)](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它支持 lint、代码导航和漏洞扫描。

## 带检查的构建

以下版本支持构建检查：

- Buildx 0.15.0 及更高版本
- [docker/build-push-action](https://github.com/docker/build-push-action) 6.6.0 及更高版本
- [docker/bake-action](https://github.com/docker/bake-action) 5.6.0 及更高版本

调用构建时默认会运行检查，并在构建输出中显示任何违规项。例如，以下命令既构建镜像又运行检查：

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED
...

1 warning found (use --debug to expand):
  - Lint Rule 'JSONArgsRecommended': JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 7)

```

在此示例中，构建成功运行，但报告了 [JSONArgsRecommended](/reference/build-checks/json-args-recommended/) 警告，因为 `CMD` 指令应使用 JSON 数组语法。

使用 GitHub Actions 时，检查结果会显示在拉取请求的 diff（差异）视图中。

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

![GitHub Actions 构建检查注解](./images/gha-check-annotations.png)

### 更详细的输出

普通 `docker build` 的检查警告会显示一条简明消息，包含规则名称、说明以及 Dockerfile 中出现问题的行号。如果您想查看有关检查的更详细信息，可以使用 `--debug` 标志。例如：

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

使用 `--debug` 标志时，输出将包含指向该检查文档的链接，以及发现问题的 Dockerfile 代码片段。

## 仅检查构建而不实际构建

要在不实际构建的情况下运行构建检查，您可以像往常一样使用 `docker build` 命令，但要加上 `--check` 标志。示例如下：

```console
$ docker build --check .
```

此命令不会执行构建步骤，而是仅运行检查并报告发现的任何问题。如果有任何问题，将在输出中报告。例如：

```text {title="带 --check 的输出"}
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

带 `--check` 的输出会显示该检查的 [详细消息](#更详细的输出)。

与普通构建不同，如果使用 `--check` 标志时报告了任何违规项，该命令将以非零状态码退出。

## 发现违规项时停止构建

默认情况下，构建检查违规项会作为警告报告，退出代码为 0。您可以使用 Dockerfile 中的 `check=error=true` 指令，将 Docker 配置为在报告违规项时使构建失败。这将导致在运行构建检查之后、实际执行构建之前，构建因出错而停止。

```dockerfile {title=Dockerfile,linenos=true,hl_lines=2}
# syntax=docker/dockerfile:1
# check=error=true

FROM alpine
CMD echo "Hello, world!"
```

如果没有 `# check=error=true` 指令，此构建将以状态码 0 完成。但是，有了该指令后，构建检查违规将导致非零状态码：

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

您还可以通过传递 `BUILDKIT_DOCKERFILE_CHECK` 构建参数在 CLI 上设置错误指令：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=error=true" .
```

## 跳过检查

默认情况下，构建镜像时会运行所有检查。如果您想跳过特定检查，可以在 Dockerfile 中使用 `check=skip` 指令。`skip` 参数接受您想要跳过的检查 ID 的 CSV 字符串。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing

FROM alpine AS BASE_STAGE
CMD echo "Hello, world!"
```

构建此 Dockerfile 不会产生检查违规。

您还可以通过传递带有您想跳过的检查 ID CSV 字符串的 `BUILDKIT_DOCKERFILE_CHECK` 构建参数来跳过检查。例如：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing" .
```

要跳过所有检查，请使用 `skip=all` 参数：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all
```

## 组合检查指令的 error 和 skip 参数

要同时跳过特定检查并在发现违规时报错，请将 `skip` 和 `error` 参数以分号 (`;`) 分隔传递给 Dockerfile 中的 `check` 指令或构建参数。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing;error=true
```

```console {title="构建参数"}
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing;error=true" .
```

## 实验性检查

在检查晋升为稳定版之前，它们可能会作为实验性检查提供。实验性检查默认禁用。要查看可用实验性检查列表，请参阅 [构建检查参考](/reference/build-checks/)。

要启用所有实验性检查，请将 `BUILDKIT_DOCKERFILE_CHECK` 构建参数设置为 `experimental=all`：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=experimental=all" .
```

您还可以在 Dockerfile 中使用 `check` 指令启用实验性检查：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=experimental=all
```

要选择性地启用实验性检查，您可以将想要启用的检查 ID 的 CSV 字符串传递给 Dockerfile 中的 `check` 指令或作为构建参数。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=experimental=JSONArgsRecommended,StageNameCasing
```

请注意，`experimental` 指令优先于 `skip` 指令，这意味着实验性检查将运行，无论您设置了什么样的 `skip` 指令。例如，如果您设置了 `skip=all` 并启用了实验性检查，实验性检查仍然会运行：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all;experimental=all
```

## 延伸阅读

有关使用构建检查的更多信息，请参阅：

- [构建检查参考](/reference/build-checks/)
- [使用 GitHub Actions 验证构建配置](/manuals/build/ci/github-actions/checks.md)
