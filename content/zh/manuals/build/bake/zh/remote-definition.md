---
title: 远程 Bake 文件定义
description: 使用 Git 或 HTTP 的远程文件定义进行 Bake 构建
keywords: build, buildx, bake, file, remote, git, http
---

您可以直接从远程 Git 仓库或 HTTPS URL 构建 Bake 文件：

```console
$ docker buildx bake "https://github.com/docker/cli.git#v20.10.11" --print
#1 [internal] load git source https://github.com/docker/cli.git#v20.10.11
#1 0.745 e8f1871b077b64bcb4a13334b7146492773769f7       refs/tags/v20.10.11
#1 2.022 From https://github.com/docker/cli
#1 2.022  * [new tag]         v20.10.11  -> v20.10.11
#1 DONE 2.9s
```

这会从指定的远程位置获取 Bake 定义并执行该文件中定义的组或目标。如果远程 Bake 定义没有指定构建上下文，上下文会自动设置为 Git 远程。例如，[这种情况](https://github.com/docker/cli/blob/2776a6d694f988c0c1df61cad4bfac0f54e481c8/docker-bake.hcl#L17-L26)使用 `https://github.com/docker/cli.git`：

```json
{
  "group": {
    "default": {
      "targets": ["binary"]
    }
  },
  "target": {
    "binary": {
      "context": "https://github.com/docker/cli.git#v20.10.11",
      "dockerfile": "Dockerfile",
      "args": {
        "BASE_VARIANT": "alpine",
        "GO_STRIP": "",
        "VERSION": ""
      },
      "target": "binary",
      "platforms": ["local"],
      "output": ["build"]
    }
  }
}
```

## 使用远程定义的本地上下文

当使用远程 Bake 定义进行构建时，您可能希望使用相对于执行 Bake 命令的目录的本地文件。您可以使用 `cwd://` 前缀将上下文定义为相对于命令上下文。

```hcl {title="https://github.com/dvdksn/buildx/blob/bake-remote-example/docker-bake.hcl"}
target "default" {
  context = "cwd://"
  dockerfile-inline = <<EOT
FROM alpine
WORKDIR /src
COPY . .
RUN ls -l && stop
EOT
}
```

```console
$ touch foo bar
$ docker buildx bake "https://github.com/dvdksn/buildx.git#bake-remote-example"
```

```text
...
 > [4/4] RUN ls -l && stop:
#8 0.101 total 0
#8 0.102 -rw-r--r--    1 root     root             0 Jul 27 18:47 bar
#8 0.102 -rw-r--r--    1 root     root             0 Jul 27 18:47 foo
#8 0.102 /bin/sh: stop: not found
```

如果您想使用特定的本地目录作为上下文，可以在 `cwd://` 前缀后附加路径。请注意，如果您确实指定了路径，它必须在执行命令的工作目录内。如果您使用绝对路径，或使用指向工作目录外部的相对路径，Bake 将抛出错误。

### 本地命名上下文

您还可以使用 `cwd://` 前缀将 Bake 执行上下文中的本地目录定义为命名上下文。

以下示例将 `docs` 上下文定义为 `./src/docs/content`，相对于运行 Bake 的当前工作目录作为命名上下文。

```hcl {title=docker-bake.hcl}
target "default" {
  contexts = {
    docs = "cwd://src/docs/content"
  }
  dockerfile = "Dockerfile"
}
```

相比之下，如果您省略 `cwd://` 前缀，路径将相对于构建上下文解析。

## 指定要使用的 Bake 定义

从远程 Git 仓库加载 Bake 文件时，如果仓库包含多个 Bake 文件，您可以使用 `--file` 或 `-f` 标志指定要使用的 Bake 定义：

```console
docker buildx bake -f bake.hcl "https://github.com/crazy-max/buildx.git#remote-with-local"
```

```text
...
#4 [2/2] RUN echo "hello world"
#4 0.270 hello world
#4 DONE 0.3s
```

## 组合本地和远程 Bake 定义

您还可以使用 `cwd://` 前缀与 `-f` 将远程定义与本地定义组合。

给定当前工作目录中的以下本地 Bake 定义：

```hcl
# local.hcl
target "default" {
  args = {
    HELLO = "foo"
  }
}
```

以下示例使用 `-f` 指定两个 Bake 定义：

- `-f bake.hcl`：此定义相对于 Git URL 加载。
- `-f cwd://local.hcl`：此定义相对于执行 Bake 命令的当前工作目录加载。

```console
docker buildx bake -f bake.hcl -f cwd://local.hcl "https://github.com/crazy-max/buildx.git#remote-with-local" --print
```

```json
{
  "target": {
    "default": {
      "context": "https://github.com/crazy-max/buildx.git#remote-with-local",
      "dockerfile": "Dockerfile",
      "args": {
        "HELLO": "foo"
      },
      "target": "build",
      "output": [
        {
          "type": "cacheonly"
        }
      ]
    }
  }
}
```

组合本地和远程 Bake 定义变得必要的一种情况是：当您在 GitHub Actions 中使用远程 Bake 定义进行构建，并希望使用 [metadata-action](https://github.com/docker/metadata-action) 生成标签、注释或标签时。metadata action 生成一个在运行器的本地 Bake 执行上下文中可用的 Bake 文件。要同时使用远程定义和本地"仅元数据"的 Bake 文件，请指定两个文件并对元数据 Bake 文件使用 `cwd://` 前缀：

```yml
      - name: Build
        uses: docker/bake-action@v6
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ steps.meta.outputs.bake-file }}
          targets: build
```

## 私有仓库中的远程定义

如果您想使用位于私有仓库中的远程定义，您可能需要为 Bake 指定获取定义时使用的凭据。

如果您可以使用默认的 `SSH_AUTH_SOCK` 对私有仓库进行身份验证，则无需为 Bake 指定任何额外的身份验证参数。Bake 会自动使用您的默认代理套接字。

对于使用 HTTP 令牌或自定义 SSH 代理的身份验证，请使用以下环境变量来配置 Bake 的身份验证策略：

- [`BUILDX_BAKE_GIT_AUTH_TOKEN`](../building/variables.md#buildx_bake_git_auth_token)
- [`BUILDX_BAKE_GIT_AUTH_HEADER`](../building/variables.md#buildx_bake_git_auth_header)
- [`BUILDX_BAKE_GIT_SSH`](../building/variables.md#buildx_bake_git_ssh)
