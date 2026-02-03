---
title: 在 GitHub Actions 中使用机密
linkTitle: 构建机密 (Build secrets)
description: 使用 GitHub Actions 进行机密挂载的示例
keywords: ci, github actions, gha, buildkit, buildx, secret, 机密, 凭据
tags: [Secrets]
---

构建机密 (Build secret) 是作为构建过程的一部分使用的敏感信息，如密码或 API 令牌。Docker Build 支持两种形式的机密：

- [机密挂载 (Secret mounts)](#机密挂载) 将机密以文件形式添加到构建容器中（默认位于 `/run/secrets` 下）。
- [SSH 挂载](#ssh-挂载) 将 SSH 代理套接字或密钥添加到构建容器中。

本页展示了如何在 GitHub Actions 中使用机密。有关机密的通用介绍，请参阅 [构建机密](../../building/secrets.md)。

## 机密挂载 (Secret mounts)

以下示例使用并暴露了 GitHub 在工作流中提供的 [`GITHUB_TOKEN` 机密](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret)。

首先，创建一个使用该机密的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=github_token,env=GITHUB_TOKEN ...
```

在此示例中，机密名称为 `github_token`。以下工作流使用 `secrets` 输入项暴露此机密：

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
> 您还可以使用 `secret-files` 输入项向构建过程暴露机密文件：
>
> ```yaml
> secret-files: |
>   "MY_SECRET=./secret.txt"
> ```

如果您使用的是 [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) 并需要处理多行数值，则需要将键值对放在引号之间：

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
  "JSON_SECRET={"key1":"value1","key2":"value2"}"
```

| 键 | 值 |
| ---------------- | ----------------------------------- |
| `MYSECRET` | `***********************` |
| `GIT_AUTH_TOKEN` | `abcdefghi,jklmno=0123456789` |
| `MYSECRET` | `aaaaaaaa
bbbbbbb
ccccccccc` |
| `FOO` | `bar` |
| `EMPTYLINE` | `aaaa

bbbb
ccc` |
| `JSON_SECRET` | `{"key1":"value1","key2":"value2"}` |

> [!NOTE]
>
> 针对引号需要使用双重转义。

## SSH 挂载

SSH 挂载允许您向 SSH 服务器进行身份验证。例如执行 `git clone`，或从私有仓库获取应用程序包。

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

要构建此 Dockerfile，您必须指定一个供构建器在带有 `--mount=type=ssh` 的步骤中使用的 SSH 挂载。

以下 GitHub Action 工作流使用 `MrSquaare/ssh-setup-action` 第三方 Action 在 GitHub 运行器上启动 SSH 设置。该 Action 创建由 GitHub Action 机密 `SSH_GITHUB_PPK` 定义的私钥，并将其添加到位于 `SSH_AUTH_SOCK` 的 SSH 代理套接字文件中。构建步骤中的 SSH 挂载默认假定使用 `SSH_AUTH_SOCK`，因此无需显式指定 SSH 代理套接字的 ID 或路径。

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