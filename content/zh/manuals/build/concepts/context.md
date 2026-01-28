---
title: 构建上下文
weight: 30
description: 了解如何使用构建上下文从 Dockerfile 访问文件
keywords: build, buildx, buildkit, context, git, tarball, stdin
aliases:
  - /build/building/context/
---

`docker build` 和 `docker buildx build` 命令从 [Dockerfile](/reference/dockerfile.md) 和上下文构建 Docker 镜像。

## 什么是构建上下文？

构建上下文是构建过程可以访问的文件集合。传递给构建命令的位置参数指定了要用于构建的上下文：

```console
$ docker build [OPTIONS] PATH | URL | -
                         ^^^^^^^^^^^^^^
```

您可以将以下任何一种输入作为构建的上下文：

- 本地目录的相对或绝对路径
- Git 仓库、tarball 或纯文本文件的远程 URL
- 通过标准输入管道传递给 `docker build` 命令的纯文本文件或 tarball

### 文件系统上下文

当您的构建上下文是本地目录、远程 Git 仓库或 tar 文件时，它就成为构建器在构建期间可以访问的文件集合。`COPY` 和 `ADD` 等构建指令可以引用上下文中的任何文件和目录。

文件系统构建上下文是递归处理的：

- 当您指定本地目录或 tarball 时，所有子目录都会被包含
- 当您指定远程 Git 仓库时，仓库及其包含的所有子模块都会被包含

有关可用于构建的不同类型文件系统上下文的更多信息，请参阅：

- [本地文件](#local-context)
- [Git 仓库](#git-repositories)
- [远程 tarball](#remote-tarballs)

### 文本文件上下文

当您的构建上下文是纯文本文件时，构建器将该文件解释为 Dockerfile。使用这种方法，构建不使用文件系统上下文。

有关更多信息，请参阅[空构建上下文](#empty-context)。

## 本地上下文 {#local-context}

要使用本地构建上下文，您可以向 `docker build` 命令指定相对或绝对文件路径。以下示例显示使用当前目录 (`.`) 作为构建上下文的构建命令：

```console
$ docker build .
...
#16 [internal] load build context
#16 sha256:23ca2f94460dcbaf5b3c3edbaaa933281a4e0ea3d92fe295193e4df44dc68f85
#16 transferring context: 13.16MB 2.2s done
...
```

这使得当前工作目录中的文件和目录可供构建器使用。构建器在需要时从构建上下文加载所需的文件。

您也可以使用本地 tarball 作为构建上下文，通过将 tarball 内容管道传递给 `docker build` 命令。请参阅 [Tarballs](#local-tarballs)。

### 本地目录

考虑以下目录结构：

```text
.
├── index.ts
├── src/
├── Dockerfile
├── package.json
└── package-lock.json
```

如果将此目录作为上下文传递，Dockerfile 指令可以引用并包含这些文件到构建中。

```dockerfile
# syntax=docker/dockerfile:1
FROM node:latest
WORKDIR /src
COPY package.json package-lock.json .
RUN npm ci
COPY index.ts src .
```

```console
$ docker build .
```

### 从标准输入读取 Dockerfile 的本地上下文

使用以下语法，可以使用本地文件系统上的文件进行构建，同时从标准输入读取 Dockerfile。

```console
$ docker build -f- <PATH>
```

该语法使用 -f（或 --file）选项指定要使用的 Dockerfile，并使用连字符 (-) 作为文件名来指示 Docker 从标准输入读取 Dockerfile。

以下示例使用当前目录 (.) 作为构建上下文，并使用 here-document 通过标准输入传递的 Dockerfile 构建镜像。

```bash
# create a directory to work in
mkdir example
cd example

# create an example file
touch somefile.txt

# build an image using the current directory as context
# and a Dockerfile passed through stdin
docker build -t myimage:latest -f- . <<EOF
FROM busybox
COPY somefile.txt ./
RUN cat /somefile.txt
EOF
```

### 本地 tarball {#local-tarballs}

当您将 tarball 管道传递给构建命令时，构建将使用 tarball 的内容作为文件系统上下文。

例如，给定以下项目目录：

```text
.
├── Dockerfile
├── Makefile
├── README.md
├── main.c
├── scripts
├── src
└── test.Dockerfile
```

您可以创建目录的 tarball 并将其管道传递给构建以用作上下文：

```console
$ tar czf foo.tar.gz *
$ docker build - < foo.tar.gz
```

构建从 tarball 上下文解析 Dockerfile。您可以使用 `--file` 标志指定相对于 tarball 根目录的 Dockerfile 名称和位置。以下命令使用 tarball 中的 `test.Dockerfile` 进行构建：

```console
$ docker build --file test.Dockerfile - < foo.tar.gz
```

## 远程上下文

您可以指定远程 Git 仓库、tarball 或纯文本文件的地址作为构建上下文。

- 对于 Git 仓库，构建器会自动克隆仓库。请参阅 [Git 仓库](#git-repositories)。
- 对于 tarball，构建器会下载并解压 tarball 的内容。请参阅 [Tarballs](#remote-tarballs)。

如果远程 tarball 是文本文件，构建器不会收到[文件系统上下文](#filesystem-contexts)，而是假设远程文件是 Dockerfile。请参阅[空构建上下文](#empty-context)。

### Git 仓库 {#git-repositories}

当您将指向 Git 仓库位置的 URL 作为参数传递给 `docker build` 时，构建器使用该仓库作为构建上下文。

构建器执行仓库的浅克隆，只下载 HEAD 提交，而不是整个历史记录。

构建器递归克隆仓库及其包含的所有子模块。

```console
$ docker build https://github.com/user/myrepo.git
```

默认情况下，构建器克隆您指定的仓库的默认分支上的最新提交。

#### URL 片段

您可以将 URL 片段附加到 Git 仓库地址，使构建器克隆仓库的特定分支、标签和子目录。

URL 片段的格式是 `#ref:dir`，其中：

- `ref` 是分支、标签或提交哈希的名称
- `dir` 是仓库内的子目录

例如，以下命令使用 `container` 分支以及该分支中的 `docker` 子目录作为构建上下文：

```console
$ docker build https://github.com/user/myrepo.git#container:docker
```

下表显示了所有有效的后缀及其构建上下文：

| 构建语法后缀                   | 使用的提交                    | 使用的构建上下文 |
| ------------------------------ | ----------------------------- | ------------------ |
| `myrepo.git`                   | `refs/heads/<default branch>` | `/`                |
| `myrepo.git#mytag`             | `refs/tags/mytag`             | `/`                |
| `myrepo.git#mybranch`          | `refs/heads/mybranch`         | `/`                |
| `myrepo.git#pull/42/head`      | `refs/pull/42/head`           | `/`                |
| `myrepo.git#:myfolder`         | `refs/heads/<default branch>` | `/myfolder`        |
| `myrepo.git#master:myfolder`   | `refs/heads/master`           | `/myfolder`        |
| `myrepo.git#mytag:myfolder`    | `refs/tags/mytag`             | `/myfolder`        |
| `myrepo.git#mybranch:myfolder` | `refs/heads/mybranch`         | `/myfolder`        |

当您使用提交哈希作为 URL 片段中的 `ref` 时，请使用完整的 40 个字符的 SHA-1 提交哈希。不支持短哈希，例如截断为 7 个字符的哈希。

```bash
# ✅ The following works:
docker build github.com/docker/buildx#d4f088e689b41353d74f1a0bfcd6d7c0b213aed2
# ❌ The following doesn't work because the commit hash is truncated:
docker build github.com/docker/buildx#d4f088e
```

#### 保留 `.git` 目录

默认情况下，BuildKit 在使用 Git 上下文时不保留 `.git` 目录。您可以通过设置 [`BUILDKIT_CONTEXT_KEEP_GIT_DIR` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args) 来配置 BuildKit 保留该目录。如果您想在构建期间检索 Git 信息，这可能很有用：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
WORKDIR /src
RUN --mount=target=. \
  make REVISION=$(git rev-parse HEAD) build
```

```console
$ docker build \
  --build-arg BUILDKIT_CONTEXT_KEEP_GIT_DIR=1
  https://github.com/user/myrepo.git#main
```

#### 私有仓库

当您指定的 Git 上下文也是私有仓库时，构建器需要您提供必要的身份验证凭据。您可以使用 SSH 或基于令牌的身份验证。

如果您指定的 Git 上下文是 SSH 或 Git 地址，Buildx 会自动检测并使用 SSH 凭据。默认情况下，这使用 `$SSH_AUTH_SOCK`。您可以使用 [`--ssh` 标志](/reference/cli/docker/buildx/build.md#ssh) 配置要使用的 SSH 凭据。

```console
$ docker buildx build --ssh default git@github.com:user/private.git
```

如果您想改用基于令牌的身份验证，可以使用 [`--secret` 标志](/reference/cli/docker/buildx/build.md#secret) 传递令牌。

```console
$ GIT_AUTH_TOKEN=<token> docker buildx build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/user/private.git
```

> [!NOTE]
>
> 不要使用 `--build-arg` 传递密钥。

### 从标准输入读取 Dockerfile 的远程上下文

使用以下语法，可以使用本地文件系统上的文件进行构建，同时从标准输入读取 Dockerfile。

```console
$ docker build -f- <URL>
```

该语法使用 -f（或 --file）选项指定要使用的 Dockerfile，并使用连字符 (-) 作为文件名来指示 Docker 从标准输入读取 Dockerfile。

这在以下情况下很有用：您想从不包含 Dockerfile 的仓库构建镜像，或者您想使用自定义 Dockerfile 进行构建，而无需维护自己的仓库分支。

以下示例使用从标准输入传递的 Dockerfile 构建镜像，并从 GitHub 上的 [hello-world](https://github.com/docker-library/hello-world) 仓库添加 `hello.c` 文件。

```bash
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```

### 远程 tarball {#remote-tarballs}

如果您传递远程 tarball 的 URL，URL 本身会被发送到构建器。

```console
$ docker build http://server/context.tar.gz
#1 [internal] load remote build context
#1 DONE 0.2s

#2 copy /context /
#2 DONE 0.1s
...
```

下载操作将在运行 BuildKit 守护进程的主机上执行。请注意，如果您使用远程 Docker 上下文或远程构建器，这不一定是您发出构建命令的同一台机器。BuildKit 获取 `context.tar.gz` 并将其用作构建上下文。Tarball 上下文必须是符合标准 `tar` Unix 格式的 tar 归档，并且可以使用 `xz`、`bzip2`、`gzip` 或 `identity`（无压缩）格式之一进行压缩。

## 空上下文 {#empty-context}

当您使用文本文件作为构建上下文时，构建器将该文件解释为 Dockerfile。使用文本文件作为上下文意味着构建没有文件系统上下文。

当您的 Dockerfile 不依赖任何本地文件时，您可以使用空构建上下文进行构建。

### 如何在没有上下文的情况下构建

您可以通过标准输入流传递文本文件，或指向远程文本文件的 URL。

{{< tabs >}}
{{< tab name="Unix pipe" >}}

```console
$ docker build - < Dockerfile
```

{{< /tab >}}
{{< tab name="PowerShell" >}}

```powershell
Get-Content Dockerfile | docker build -
```

{{< /tab >}}
{{< tab name="Heredocs" >}}

```bash
docker build -t myimage:latest - <<EOF
FROM busybox
RUN echo "hello world"
EOF
```

{{< /tab >}}
{{< tab name="Remote file" >}}

```console
$ docker build https://raw.githubusercontent.com/dvdksn/clockbox/main/Dockerfile
```

{{< /tab >}}
{{< /tabs >}}

当您在没有文件系统上下文的情况下构建时，`COPY` 等 Dockerfile 指令无法引用本地文件：

```console
$ ls
main.c
$ docker build -<<< $'FROM scratch\nCOPY main.c .'
[+] Building 0.0s (4/4) FINISHED
 => [internal] load build definition from Dockerfile       0.0s
 => => transferring dockerfile: 64B                        0.0s
 => [internal] load .dockerignore                          0.0s
 => => transferring context: 2B                            0.0s
 => [internal] load build context                          0.0s
 => => transferring context: 2B                            0.0s
 => ERROR [1/1] COPY main.c .                              0.0s
------
 > [1/1] COPY main.c .:
------
Dockerfile:2
--------------------
   1 |     FROM scratch
   2 | >>> COPY main.c .
   3 |
--------------------
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum of ref 7ab2bb61-0c28-432e-abf5-a4c3440bc6b6::4lgfpdf54n5uqxnv9v6ymg7ih: "/main.c": not found
```

## .dockerignore 文件

您可以使用 `.dockerignore` 文件从构建上下文中排除文件或目录。

```text
# .dockerignore
node_modules
bar
```

这有助于避免将不需要的文件和目录发送到构建器，从而提高构建速度，特别是在使用远程构建器时。

### 文件名和位置

当您运行构建命令时，构建客户端会在上下文的根目录中查找名为 `.dockerignore` 的文件。如果该文件存在，与文件中模式匹配的文件和目录将在发送到构建器之前从构建上下文中移除。

如果您使用多个 Dockerfile，可以为每个 Dockerfile 使用不同的忽略文件。您可以使用特殊的命名约定来实现。将忽略文件放在与 Dockerfile 相同的目录中，并以 Dockerfile 的名称作为忽略文件的前缀，如以下示例所示。

```text
.
├── index.ts
├── src/
├── docker
│   ├── build.Dockerfile
│   ├── build.Dockerfile.dockerignore
│   ├── lint.Dockerfile
│   ├── lint.Dockerfile.dockerignore
│   ├── test.Dockerfile
│   └── test.Dockerfile.dockerignore
├── package.json
└── package-lock.json
```

如果两者都存在，特定于 Dockerfile 的忽略文件优先于构建上下文根目录的 `.dockerignore` 文件。

### 语法

`.dockerignore` 文件是一个以换行符分隔的模式列表，类似于 Unix shell 的文件通配符。忽略模式中的前导和尾随斜杠会被忽略。以下模式都会排除构建上下文根目录下 `foo` 子目录中名为 `bar` 的文件或目录：

- `/foo/bar/`
- `/foo/bar`
- `foo/bar/`
- `foo/bar`

如果 `.dockerignore` 文件中的一行在第 1 列以 `#` 开头，则该行被视为注释，在 CLI 解释之前会被忽略。

```gitignore
#/this/is/a/comment
```

如果您想了解 `.dockerignore` 模式匹配逻辑的精确细节，请查看 GitHub 上的 [moby/patternmatcher 仓库](https://github.com/moby/patternmatcher/tree/main/ignorefile)，其中包含源代码。

#### 匹配

以下代码片段显示了一个示例 `.dockerignore` 文件。

```text
# comment
*/temp*
*/*/temp*
temp?
```

此文件导致以下构建行为：

| 规则        | 行为                                                                                                                                                                                                      |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `# comment` | 被忽略。                                                                                                                                                                                                      |
| `*/temp*`   | 排除根目录的任何直接子目录中名称以 `temp` 开头的文件和目录。例如，纯文本文件 `/somedir/temporary.txt` 会被排除，目录 `/somedir/temp` 也是如此。 |
| `*/*/temp*` | 排除根目录下两级子目录中以 `temp` 开头的文件和目录。例如，`/somedir/subdir/temporary.txt` 会被排除。                                         |
| `temp?`     | 排除根目录中名称是 `temp` 加一个字符扩展名的文件和目录。例如，`/tempa` 和 `/tempb` 会被排除。                                                     |

匹配使用 Go 的 [`filepath.Match` 函数](https://golang.org/pkg/path/filepath#Match) 规则完成。预处理步骤使用 Go 的 [`filepath.Clean` 函数](https://golang.org/pkg/path/filepath/#Clean) 来修剪空白并移除 `.` 和 `..`。预处理后为空的行会被忽略。

> [!NOTE]
>
> 由于历史原因，模式 `.` 会被忽略。

除了 Go 的 `filepath.Match` 规则外，Docker 还支持特殊的通配符字符串 `**`，可以匹配任意数量的目录（包括零个）。例如，`**/*.go` 会排除在构建上下文中任何位置找到的所有以 `.go` 结尾的文件。

您可以使用 `.dockerignore` 文件排除 `Dockerfile` 和 `.dockerignore` 文件。这些文件仍会被发送到构建器，因为运行构建需要它们。但是，您无法使用 `ADD`、`COPY` 或绑定挂载将这些文件复制到镜像中。

#### 否定匹配

您可以在行前加上 `!`（感叹号）来为排除规则创建例外。以下是使用此机制的示例 `.dockerignore` 文件：

```text
*.md
!README.md
```

上下文目录下的所有 markdown 文件都会被排除，_除了_ `README.md`。请注意，子目录下的 markdown 文件仍然会被包含。

`!` 例外规则的位置会影响行为：`.dockerignore` 中与特定文件匹配的最后一行决定该文件是被包含还是被排除。考虑以下示例：

```text
*.md
!README*.md
README-secret.md
```

除了 `README-secret.md` 之外的 README 文件外，没有 markdown 文件会被包含在上下文中。

现在考虑这个示例：

```text
*.md
README-secret.md
!README*.md
```

所有 README 文件都会被包含。中间的行没有效果，因为 `!README*.md` 匹配 `README-secret.md` 且排在最后。

## 命名上下文

除了默认构建上下文（`docker build` 命令的位置参数）外，您还可以向构建传递额外的命名上下文。

命名上下文使用 `--build-context` 标志指定，后跟名称-值对。这允许您在构建期间包含来自多个来源的文件和目录，同时保持它们在逻辑上的分离。

```console
$ docker build --build-context docs=./docs .
```

在此示例中：

- 命名的 `docs` 上下文指向 `./docs` 目录。
- 默认上下文 (`.`) 指向当前工作目录。

### 在 Dockerfile 中使用命名上下文

Dockerfile 指令可以像引用多阶段构建中的阶段一样引用命名上下文。

例如，以下 Dockerfile：

1. 使用 `COPY` 指令将文件从默认上下文复制到当前构建阶段。
2. 绑定挂载命名上下文中的文件，以在构建过程中处理这些文件。

```dockerfile
# syntax=docker/dockerfile:1
FROM buildbase
WORKDIR /app

# Copy all files from the default context into /app/src in the build container
COPY . /app/src
RUN make bin

# Mount the files from the named "docs" context to build the documentation
RUN --mount=from=docs,target=/app/docs \
    make manpages
```

### 命名上下文的用例

使用命名上下文可以在构建 Docker 镜像时提供更大的灵活性和效率。以下是一些使用命名上下文可能有用的场景：

#### 示例：组合本地和远程来源

您可以为不同类型的来源定义单独的命名上下文。例如，考虑一个项目，应用程序源代码是本地的，但部署脚本存储在 Git 仓库中：

```console
$ docker build --build-context scripts=https://github.com/user/deployment-scripts.git .
```

在 Dockerfile 中，您可以独立使用这些上下文：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:latest

# Copy application code from the main context
COPY . /opt/app

# Run deployment scripts using the remote "scripts" context
RUN --mount=from=scripts,target=/scripts /scripts/main.sh
```

#### 示例：使用自定义依赖项进行动态构建

在某些场景中，您可能需要将配置文件或依赖项从外部来源动态注入到构建中。命名上下文通过允许您挂载不同的配置而无需修改默认构建上下文，使这变得简单直接。

```console
$ docker build --build-context config=./configs/prod .
```

示例 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM nginx:alpine

# Use the "config" context for environment-specific configurations
COPY --from=config nginx.conf /etc/nginx/nginx.conf
```

#### 示例：固定或覆盖镜像

您可以在 Dockerfile 中像引用镜像一样引用命名上下文。这意味着您可以通过使用命名上下文覆盖来更改 Dockerfile 中的镜像引用。例如，给定以下 Dockerfile：

```dockerfile
FROM alpine:{{% param example_alpine_version %}}
```

如果您想强制镜像引用解析为不同的版本，而无需更改 Dockerfile，可以向构建传递同名的上下文。例如：

```console
docker buildx build --build-context alpine:{{% param example_alpine_version %}}=docker-image://alpine:edge .
```

`docker-image://` 前缀将上下文标记为镜像引用。引用可以是本地镜像或注册表中的镜像。

### 使用 Bake 的命名上下文

[Bake](/manuals/build/bake/_index.md) 是内置于 `docker build` 的工具，允许您使用配置文件管理构建配置。Bake 完全支持命名上下文。

要在 Bake 文件中定义命名上下文：

```hcl {title=docker-bake.hcl}
target "app" {
  contexts = {
    docs = "./docs"
  }
}
```

这相当于以下 CLI 调用：

```console
$ docker build --build-context docs=./docs .
```

#### 使用命名上下文链接目标

除了使复杂的构建更易于管理外，Bake 还提供了超出 CLI 上 `docker build` 功能的额外特性。您可以使用命名上下文创建构建管道，其中一个目标依赖并构建在另一个目标之上。例如，考虑一个 Docker 构建设置，其中有两个 Dockerfile：

- `base.Dockerfile`：用于构建基础镜像
- `app.Dockerfile`：用于构建应用程序镜像

`app.Dockerfile` 使用 `base.Dockerfile` 生成的镜像作为其基础镜像：

```dockerfile {title=app.Dockerfile}
FROM mybaseimage
```

通常，您必须先构建基础镜像，然后将其加载到 Docker Engine 的本地镜像存储或推送到注册表。使用 Bake，您可以直接引用其他目标，在 `app` 目标和 `base` 目标之间创建依赖关系。

```hcl {title=docker-bake.hcl}
target "base" {
  dockerfile = "base.Dockerfile"
}

target "app" {
  dockerfile = "app.Dockerfile"
  contexts = {
    # the target: prefix indicates that 'base' is a Bake target
    mybaseimage = "target:base"
  }
}
```

使用此配置，`app.Dockerfile` 中对 `mybaseimage` 的引用将使用构建 `base` 目标的结果。构建 `app` 目标还会在必要时触发 `mybaseimage` 的重新构建：

```console
$ docker buildx bake app
```

### 进一步阅读

有关使用命名上下文的更多信息，请参阅：

- [`--build-context` CLI 参考](/reference/cli/docker/buildx/build.md#build-context)
- [在 Bake 中使用额外上下文](/manuals/build/bake/contexts.md)
