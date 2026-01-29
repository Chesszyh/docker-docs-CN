---
title: 在 GitHub Actions 中使用密钥
linkTitle: 构建密钥 (Build secrets)
description: 在 GitHub Actions 中使用密钥挂载的示例
keywords: ci, github actions, gha, buildkit, buildx, 密钥
tags: [密钥]
---

构建密钥（Build secret）是构建过程中消耗的敏感信息，例如密码或 API 令牌。Docker Build 支持两种形式的密钥：

- [密钥挂载](#密钥挂载) 将密钥作为文件添加到构建容器中（默认位于 `/run/secrets` 下）。
- [SSH 挂载](#SSH-挂载) 将 SSH 代理套接字或密钥添加到构建容器中。

本页展示了如何在 GitHub Actions 中使用密钥。有关密钥的通用介绍，请参阅 [构建密钥](../../building/secrets.md)。

## 密钥挂载

在以下示例中，使用并暴露了 GitHub 在工作流中提供的 [`GITHUB_TOKEN` 密钥](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret)。

首先，创建一个使用该密钥的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=github_token,env=GITHUB_TOKEN ...
```

在此示例中，密钥名称为 `github_token`。以下工作流使用 `secrets` 输入来暴露此密钥：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          tags: user/app:latest
          secrets: |
            "github_token=${{ secrets.GITHUB_TOKEN }}"
```

> [!NOTE]
>
> 您还可以通过 `secret-files` 输入向构建暴露密钥文件：
>
> ```yaml
> secret-files: |
>   "MY_SECRET=./secret.txt"
> ```

如果您正在使用 [GitHub 密钥 (secrets)](https://docs.github.com/en/actions/security-guides/encrypted-secrets) 并且需要处理多行值，则需要将键值对放在引号之间：

```yaml
secrets: |
  "MYSECRET=${{ secrets.GPG_KEY }}"
  GIT_AUTH_TOKEN=abcdefghi,jklmno=0123456789
  "MYSECRET=aaaaaaaa
  bbbbbbb
  ccccccccc"
  FOO=bar
  "EMPTYLINE=aaaa

  bbbb
  ccc"
  "JSON_SECRET={\"key1\":\"value1\",\"key2\":\"value2\"}"
```

| 键 | 值 |
| ---------------- | ----------------------------------- |
| `MYSECRET`       | `***********************`           |
| `GIT_AUTH_TOKEN` | `abcdefghi,jklmno=0123456789`       |
| `MYSECRET`       | `aaaaaaaa
bbbbbbb
ccccccccc`      |
| `FOO`            | `bar`                               |
| `EMPTYLINE`      | `aaaa

bbbb
ccc`                 |
| `JSON_SECRET`    | `{"key1":"value1","key2":"value2"}` | 

> [!NOTE]
>
> 引号符号需要双重转义。

## SSH 挂载

SSH 挂载允许您与 SSH 服务器进行身份验证。例如执行 `git clone`，或从私有仓库获取应用程序包。

以下 Dockerfile 示例使用 SSH 挂载从私有 GitHub 仓库获取 Go 模块。

```dockerfile {collapse=1}
# syntax=docker/dockerfile:1

ARG GO_VERSION="{{% param example_go_version %}}"

FROM golang:${GO_VERSION}-alpine AS base
ENV CGO_ENABLED=0
ENV GOPRIVATE="github.com/foo/*"
RUN apk add --no-cache file git rsync openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
WORKDIR /src

FROM base AS vendor
# 此步骤配置 git 并检查 ssh 密钥是否已加载
RUN --mount=type=ssh <<EOT
  set -e
  echo "Setting Git SSH protocol"
  git config --global url."git@github.com:".insteadOf "https://github.com/"
  (
    set +e
    ssh -T git@github.com
    if [ ! "$?" = "1" ]; then
      echo "No GitHub SSH key loaded exiting..."
      exit 1
    fi
  )
EOT
# 此步骤下载 go 模块
RUN --mount=type=bind,target=.
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=ssh \
    go mod download -x

FROM vendor AS build
RUN --mount=type=bind,target=.
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache \
    go build ...
```

要构建此 Dockerfile，您必须指定一个 SSH 挂载，以便构建器在带有 `--mount=type=ssh` 的步骤中使用。

以下 GitHub Action 工作流使用第三方 action `MrSquaare/ssh-setup-action` 在 GitHub runner 上引导 SSH 设置。该 action 创建由 GitHub Action 密钥 `SSH_GITHUB_PPK` 定义的私钥，并将其添加到 `SSH_AUTH_SOCK` 处的 SSH 代理套接字文件。构建步骤中的 SSH 挂载默认假定使用 `SSH_AUTH_SOCK` ，因此无需显式指定 SSH 代理套接字的 ID 或路径。

{{< tabs >}}
{{< tab name="`docker/build-push-action`" >}}

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          ssh: default
          push: true
          tags: user/app:latest
```

{{< /tab >}}
{{< tab name="`docker/bake-action`" >}}

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build
        uses: docker/bake-action@v6
        with:
          set: |
            *.ssh=default
```

{{< /tab >}}
{{< /tabs >}}
