---
title: 构建上下文
weight: 30
description: 了解如何使用构建上下文从 Dockerfile 访问文件
keywords: build, buildx, buildkit, context, git, tarball, stdin, 上下文
alias:
  - /build/building/context/
---

`docker build` 和 `docker buildx build` 命令通过 [Dockerfile](/reference/dockerfile.md) 和上下文构建 Docker 镜像。

## 什么是构建上下文？

构建上下文是您的构建可以访问的文件集。您传递给构建命令的位置参数指定了您想要用于构建的上下文：

```console
$ docker build [OPTIONS] PATH | URL | -
                         ^^^^^^^^^^^^^^^
```

您可以将以下任何输入作为构建的上下文：

- 本地目录的相对或绝对路径
- Git 仓库、tar 包或纯文本文件的远程 URL
- 通过标准输入通过管道传输到 `docker build` 命令的纯文本文件或 tar 包

### 文件系统上下文

当您的构建上下文是本地目录、远程 Git 仓库或 tar 文件时，这些文件就成了构建器在构建期间可以访问的文件集。`COPY` 和 `ADD` 等构建指令可以引用上下文中的任何文件和目录。

文件系统构建上下文是递归处理的：

- 当您指定本地目录或 tar 包时，将包含所有子目录
- 当您指定远程 Git 仓库时，将包含该仓库及其所有子模块

有关可用于构建的不同类型文件系统上下文的更多信息，请参阅：

- [本地文件](#本地上下文)
- [Git 仓库](#git-仓库)
- [远程 tar 包](#远程-tar-包)

### 文本文件上下文

当您的构建上下文是纯文本文件时，构建器会将该文件解释为 Dockerfile。使用这种方法，构建不会使用文件系统上下文。

有关更多信息，请参阅 [空构建上下文](#空上下文)。

## 本地上下文

要使用本地构建上下文，您可以为 `docker build` 命令指定相对或绝对文件路径。以下示例显示了一个使用当前目录 (`.`) 作为构建上下文的构建命令：

```console
$ docker build .
... #16 [internal] load build context
#16 sha256:23ca2f94460dcbaf5b3c3edbaaa933281a4e0ea3d92fe295193e4df44dc68f85
#16 transferring context: 13.16MB 2.2s done
...
```

这使得当前工作目录中的文件和目录对构建器可用。构建器会根据需要在构建上下文中加载所需文件。

You can also use a local tarball as a build context by piping the tarball contents to the `docker build` command. See [Tarballs](#local-tar-packages).

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

如果您将此目录作为上下文传递，Dockerfile 指令可以在构建中引用并包含这些文件。

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

### 带有来自标准输入的 Dockerfile 的本地上下文

在使用来自标准输入的 Dockerfile 的同时，使用以下语法通过本地文件系统上的文件构建镜像。

```console
$ docker build -f- <PATH>
```

此语法使用 -f（或 --file）选项指定要使用的 Dockerfile，并使用连字符 (-) 作为文件名以指示 Docker 从标准输入读取 Dockerfile。

以下示例使用当前目录 (.) 作为构建上下文，并使用通过 here-document 经标准输入传递的 Dockerfile 构建镜像。

```bash
# 创建一个工作目录
mkdir example
cd example

# 创建一个示例文件
touch somefile.txt

# 使用当前目录作为上下文并使用通过标准输入传递的 Dockerfile 构建镜像
docker build -t myimage:latest -f- . <<EOF
FROM busybox
COPY somefile.txt ./
RUN cat /somefile.txt
EOF
```

### 本地 tar 包

当您将 tar 包通过管道传输到构建命令时，构建将使用 tar 包的内容作为文件系统上下文。

例如，假设有以下项目目录：

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

您可以为该目录创建一个 tar 包，并将其通过管道传输到构建中作为上下文：

```console
$ tar czf foo.tar.gz *
$ docker build - < foo.tar.gz
```

构建会从 tar 包上下文中解析 Dockerfile。您可以使用 `--file` 标志指定 Dockerfile 的名称和相对于 tar 包根目录的位置。以下命令使用 tar 包中的 `test.Dockerfile` 进行构建：

```console
$ docker build --file test.Dockerfile - < foo.tar.gz
```

## 远程上下文

您可以指定远程 Git 仓库、tar 包或纯文本文件的地址作为您的构建上下文。

- 对于 Git 仓库，构建器会自动克隆该仓库。参见 [Git 仓库](#git-仓库)。
- 对于 tar 包，构建器会下载并解压 tar 包的内容。参见 [Tar 包](#远程-tar-包)。

如果远程 tar 包其实是一个文本文件，构建器将不会接收到 [文件系统上下文](#文件系统上下文)，而是假定该远程文件是一个 Dockerfile。参见 [空构建上下文](#空上下文)。

### Git 仓库

当您将指向 Git 仓库位置的 URL 作为参数传递给 `docker build` 时，构建器会将该仓库用作构建上下文。

构建器会对仓库执行浅克隆，仅下载 HEAD 提交，而不是整个历史记录。

构建器会递归地克隆仓库及其包含的任何子模块。

```console
$ docker build https://github.com/user/myrepo.git
```

默认情况下，构建器克隆您指定的仓库默认分支上的最新提交。

#### URL 片段 (Fragments)

您可以在 Git 仓库地址后附加 URL 片段，以使构建器克隆仓库的特定分支、标签和子目录。

URL 片段的格式为 `#ref:dir`，其中：

- `ref` 是分支、标签或提交哈希的名称
- `dir` 是仓库内的子目录

例如，以下命令使用 `container` 分支及其中的 `docker` 子目录作为构建上下文：

```console
$ docker build https://github.com/user/myrepo.git#container:docker
```

下表列出了所有有效的后缀及其对应的构建上下文：

| 构建语法后缀            | 所用提交                   | 所用构建上下文 |
| :------------------------------ | :----------------------------- | :------------------ |
| `myrepo.git`                   | `refs/heads/<默认分支>` | `/`                |
| `myrepo.git#mytag`             | `refs/tags/mytag`             | `/`                |
| `myrepo.git#mybranch`          | `refs/heads/mybranch`         | `/`                |
| `myrepo.git#pull/42/head`      | `refs/pull/42/head`           | `/`                |
| `myrepo.git#:myfolder`         | `refs/heads/<默认分支>` | `/myfolder`        |
| `myrepo.git#master:myfolder`   | `refs/heads/master`           | `/myfolder`        |
| `myrepo.git#mytag:myfolder`    | `refs/tags/mytag`             | `/myfolder`        |
| `myrepo.git#mybranch:myfolder` | `refs/heads/mybranch`         | `/myfolder`        |

当您在 URL 片段中使用提交哈希作为 `ref` 时，请使用完整的 40 字符 SHA-1 哈希。不支持短哈希（例如截断为 7 个字符的哈希）。

```bash
# ✅ 以下方式有效：
docker build github.com/docker/buildx#d4f088e689b41353d74f1a0bfcd6d7c0b213aed2
# ❌ 以下方式无效，因为提交哈希被截断了：
docker build github.com/docker/buildx#d4f088e
```

#### 保留 `.git` 目录

默认情况下，在使用 Git 上下文时，BuildKit 不会保留 `.git` 目录。您可以通过设置 [`BUILDKIT_CONTEXT_KEEP_GIT_DIR` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args) 来配置 BuildKit 保留该目录。如果您想在构建期间获取 Git 信息，这会很有用：

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

当您指定一个同时也是私有仓库的 Git 上下文时，构建器需要您提供必要的身份验证凭据。您可以使用 SSH 或基于令牌（token）的身份验证。

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
> 不要将 `--build-arg` 用于传递密钥。

### 带有来自标准输入的 Dockerfile 的远程上下文

在使用来自标准输入的 Dockerfile 的同时，使用以下语法通过本地文件系统上的文件构建镜像。

```console
$ docker build -f- <URL>
```

此语法使用 -f（或 --file）选项指定要使用的 Dockerfile，并使用连字符 (-) 作为文件名以指示 Docker 从标准输入读取 Dockerfile。

在您想要从不包含 Dockerfile 的仓库构建镜像，或者想要使用自定义 Dockerfile 构建而不想维护该仓库的派生（fork）版本的情况下，这非常有用。

以下示例使用来自标准输入的 Dockerfile 构建镜像，并添加来自 GitHub 上 [hello-world](https://github.com/docker-library/hello-world) 仓库的 `hello.c` 文件。

```bash
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```

### 远程 tar 包

如果您将 URL 传递给远程 tar 包，URL 本身将被发送到构建器。

```console
$ docker build http://server/context.tar.gz
#1 [internal] load remote build context
#1 DONE 0.2s

#2 copy /context /
#2 DONE 0.1s
...
```

下载操作将在运行 BuildKit 守护进程的主机上执行。请注意，如果您使用的是远程 Docker 上下文或远程构建器，那并不一定与您发出构建命令的机器是同一台。BuildKit 会获取 `context.tar.gz` 并将其用作构建上下文。Tar 包上下文必须是符合标准 Unix `tar` 格式的归档文件，并且可以使用 `xz`、`bzip2`、`gzip` 或 `identity`（不压缩）格式中的任何一种进行压缩。

## 空上下文

当您使用文本文件作为构建上下文时，构建器会将该文件解释为 Dockerfile。使用文本文件作为上下文意味着构建过程没有文件系统上下文。

当您的 Dockerfile 不依赖于任何本地文件时，您可以使用空构建上下文进行构建。

### 如何在没有上下文的情况下进行构建

您可以使用标准输入流传递文本文件，或者指向远程文本文件的 URL。

{{< tabs >}}
{{< tab name="Unix 管道" >}}

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
{{< tab name="远程文件" >}}

```console
$ docker build https://raw.githubusercontent.com/dvdksn/clockbox/main/Dockerfile
```

{{< /tab >}}
{{< /tabs >}}

当您在没有文件系统上下文的情况下进行构建时，`COPY` 等 Dockerfile 指令无法引用本地文件：

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
 => ERROR [1/1] COPY main.c .
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

这有助于避免将不需要的文件和目录发送到构建器，从而提高构建速度，尤其是在使用远程构建器时。

### 文件名和位置

当您运行构建命令时，构建客户端会在上下文的根目录中寻找名为 `.dockerignore` 的文件。如果该文件存在，则在将构建上下文发送到构建器之前，匹配文件中模式的文件和目录将被从中移除。

如果您使用多个 Dockerfile，可以为每个 Dockerfile 使用不同的 ignore 文件。为此，您可以对 ignore 文件使用特殊的命名约定。将 ignore 文件放在与 Dockerfile 相同的目录中，并为 ignore 文件加上 Dockerfile 的名称作为前缀，如下例所示。

```text
.
├── index.ts
├── src/
├── docker
│   ├── build.Dockerfile
│   ├── build.Dockerfile.dockerignore
│   ├── lint.Dockerfile
│   ├── lint.Dockerfile.dockerignore
│   ├── test.Dockerfile
│   └── test.Dockerfile.dockerignore
├── package.json
└── package-lock.json
```

如果两者都存在，则特定于 Dockerfile 的 ignore 文件优先于构建上下文根目录下的 `.dockerignore` 文件。

### 语法

`.dockerignore` 文件是一个由换行符分隔的模式列表，类似于 Unix shell 的文件通配符（globs）。ignore 模式中的前导和尾随斜杠会被忽略。以下模式都会排除构建上下文根目录下 `foo` 子目录中名为 `bar` 的文件或目录：

- `/foo/bar/`
- `/foo/bar`
- `foo/bar/`
- `foo/bar`

如果 `.dockerignore` 文件中的某行以第 1 列的 `#` 开头，则该行被视为注释，在被 CLI 解释之前会被忽略。

```gitignore
#/this/is/a/comment
```

如果您有兴趣了解 `.dockerignore` 模式匹配逻辑的精确细节，请查看 GitHub 上的 [moby/patternmatcher 仓库](https://github.com/moby/patternmatcher/tree/main/ignorefile)，其中包含源代码。

#### 匹配 (Matching)

以下代码片段展示了一个 `.dockerignore` 文件示例。

```text
# comment
*/temp*
*/*/temp*
temp?
```

此文件会导致以下构建行为：

| 规则        | 行为                                                                                                                                                                                                      |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `# comment` | 已忽略。                                                                                                                                                                                                      |
| `*/temp*`   | 排除根目录下任何一级子目录中以 `temp` 开头的文件和目录。例如，普通文件 `/somedir/temporary.txt` 会被排除，目录 `/somedir/temp` 也会被排除。 |
| `*/*/temp*` | 排除根目录下任何二级子目录中以 `temp` 开头的文件和目录。例如，`/somedir/subdir/temporary.txt` 会被排除。                                         |
| `temp?`     | 排除根目录下名称为 `temp` 且后接一个任意字符的文件和目录。例如，`/tempa` 和 `/tempb` 会被排除。                                                     |

匹配是使用 Go 语言的 [`filepath.Match` 函数](https://golang.org/pkg/path/filepath#Match) 规则完成的。预处理步骤使用 Go 语言的 [`filepath.Clean` 函数](https://golang.org/pkg/path/filepath/#Clean) 来修剪空白字符并移除 `.` 和 `..`。预处理后为空的行将被忽略。

> [!NOTE]
> 
> 由于历史原因，模式 `.` 会被忽略。

除了 Go 的 `filepath.Match` 规则外，Docker 还支持一个特殊的通配符字符串 `**`，它可以匹配任意数量的目录（包括零个）。例如，`**/*.go` 排除构建上下文中任何位置发现的所有以 `.go` 结尾的文件。

您可以使用 `.dockerignore` 文件来排除 `Dockerfile` 和 `.dockerignore` 文件。这些文件仍然会被发送到构建器，因为运行构建需要它们。但是您无法使用 `ADD`、`COPY` 或绑定挂载将这些文件复制到镜像中。

#### 取反匹配 (Negating matches)

您可以在行首添加 `!`（感叹号）来为排除规则创建例外。以下是一个使用此机制的 `.dockerignore` 文件示例：

```text
*.md
!README.md
```

上下文目录正下方的所有 markdown 文件（除 `README.md` 外）都将从上下文中排除。请注意，子目录下的 markdown 文件仍然会被包含。

`!` 例外规则的位置会影响其行为：`.dockerignore` 中匹配特定文件的最后一行决定了它是被包含还是被排除。考虑以下示例：

```text
*.md
!README*.md
README-secret.md
```

除了除 `README-secret.md` 之外的 README 文件外，上下文中不包含任何 markdown 文件。

现在考虑这个示例：

```text
*.md
README-secret.md
!README*.md
```

所有的 README 文件都会被包含。中间那行没有效果，因为 `!README*.md` 匹配 `README-secret.md` 且排在最后。

## 命名上下文 (Named contexts)

除了默认构建上下文（`docker build` 命令的位置参数）之外，您还可以向构建传递额外的具名上下文（named contexts）。

命名上下文使用 `--build-context` 标志指定，后接一个名值对。这允许您在构建期间包含来自多个来源的文件和目录，同时保持它们在逻辑上的隔离。

```console
$ docker build --build-context docs=./docs .
```

在此示例中：

- 命名的 `docs` 上下文指向 `./docs` 目录。
- 默认上下文 (`.`) 指向当前工作目录。

### 在 Dockerfile 中使用命名上下文

Dockerfile 指令可以像引用多阶段构建中的阶段一样引用具名上下文。

例如，以下 Dockerfile：

1. 使用 `COPY` 指令将文件从默认上下文复制到当前构建阶段。
2. 绑定挂载一个具名上下文中的文件，以将这些文件作为构建的一部分进行处理。

```dockerfile
# syntax=docker/dockerfile:1
FROM buildbase
WORKDIR /app

# 将默认上下文中的所有文件复制到构建容器中的 /app/src
COPY . /app/src
RUN make bin

# 挂载名为 "docs" 的上下文中的文件来构建文档
RUN --mount=from=docs,target=/app/docs \
    make manpages
```

### 命名上下文的用例

使用命名上下文可以在构建 Docker 镜像时获得更大的灵活性和效率。以下是一些使用命名上下文可能会很有用的场景：

#### 示例：结合本地和远程源

您可以为不同类型的源定义独立的具名上下文。例如，考虑一个项目，其应用程序源代码在本地，但部署脚本存储在 Git 仓库中：

```console
$ docker build --build-context scripts=https://github.com/user/deployment-scripts.git .
```

在 Dockerfile 中，您可以独立使用这些上下文：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:latest

# 从主上下文复制应用程序代码
COPY . /opt/app

# 使用远程 "scripts" 上下文运行部署脚本
RUN --mount=from=scripts,target=/scripts /scripts/main.sh
```

#### 示例：带有自定义依赖项的动态构建

在某些场景下，您可能需要动态地从外部源向构建中注入配置文件或依赖项。命名上下文通过允许您在不修改默认构建上下文的情况下挂载不同的配置，使这一过程变得简单明了。

```console
$ docker build --build-context config=./configs/prod .
```

Dockerfile 示例：

```dockerfile
# syntax=docker/dockerfile:1
FROM nginx:alpine

# 为环境特定的配置使用 "config" 上下文
COPY --from=config nginx.conf /etc/nginx/nginx.conf
```

#### 示例：固定或覆盖镜像

您在 Dockerfile 中引用具名上下文的方式与引用镜像的方式相同。这意味着您可以通过使用具名上下文覆盖 Dockerfile 中的镜像引用。例如，假设有以下 Dockerfile：

```dockerfile
FROM alpine:{{% param example_alpine_version %}}
```

如果您想在不更改 Dockerfile 的情况下强制镜像引用解析为不同的版本，可以在构建时传递一个同名的上下文。例如：

```console
docker buildx build --build-context alpine:{{% param example_alpine_version %}}=docker-image://alpine:edge .
```

`docker-image://` 前缀将该上下文标记为镜像引用。该引用可以是本地镜像，也可以是镜像库中的镜像。

### 在 Bake 中使用命名上下文

[Bake](/manuals/build/bake/_index.md) 是内置于 `docker build` 中的工具，允许您使用配置文件管理构建配置。Bake 完全支持具名上下文。

在 Bake 文件中定义具名上下文：

```hcl {title=docker-bake.hcl}
target "app" {
  contexts = {
    docs = "./docs"
  }
}
```

这等同于以下 CLI 调用：

```console
$ docker build --build-context docs=./docs .
```

#### 使用命名上下文链接目标

除了使复杂的构建更易于管理外，Bake 还基于 CLI 上的 `docker build` 提供了额外的功能。您可以使用具名上下文来创建构建流水线，其中一个目标依赖于另一个目标并在此基础上进行构建。例如，考虑一个拥有两个 Dockerfile 的 Docker 构建设置：

- `base.Dockerfile`：用于构建基础镜像
- `app.Dockerfile`：用于构建应用程序镜像

`app.Dockerfile` 使用 `base.Dockerfile` 生成的镜像作为其基础镜像：

```dockerfile {title=app.Dockerfile}
FROM mybaseimage
```

通常，您必须先构建基础镜像，然后将其加载到 Docker Engine 的本地镜像库或推送到镜像库。通过 Bake，您可以直接引用其他目标，从而在 `app` 目标和 `base` 目标之间创建依赖关系。

```hcl {title=docker-bake.hcl}
target "base" {
  dockerfile = "base.Dockerfile"
}

target "app" {
  dockerfile = "app.Dockerfile"
  contexts = {
    # target: 前缀指示 'base' 是一个 Bake 目标
    mybaseimage = "target:base"
  }
}
```

通过此配置，`app.Dockerfile` 中对 `mybaseimage` 的引用将使用构建 `base` 目标的结果。如果需要，构建 `app` 目标还会触发 `mybaseimage` 的重新构建：

```console
$ docker buildx bake app
```

### 延伸阅读

有关使用具名上下文的更多信息，请参阅：

- [`--build-context` CLI 参考](/reference/cli/docker/buildx/build.md#build-context)
- [在 Bake 中使用附加上下文](/manuals/build/bake/contexts.md)
