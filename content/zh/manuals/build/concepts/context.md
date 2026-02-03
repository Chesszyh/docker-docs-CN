---
title: 构建上下文 (Build context)
weight: 30
description: 了解如何使用构建上下文从 Dockerfile 访问文件
keywords: build, buildx, buildkit, context, 上下文, git, tarball, stdin
aliases:
  - /build/building/context/
---

`docker build` 和 `docker buildx build` 命令通过 [Dockerfile](/reference/dockerfile.md) 和上下文（context）来构建 Docker 镜像。

## 什么是构建上下文？

构建上下文是您的构建任务可以访问的一组文件。您传递给 build 命令的匿名参数指定了您想要为构建使用的上下文：

```console
$ docker build [OPTIONS] PATH | URL | -
                         ^^^^^^^^^^^^^^
```

您可以传递以下任何输入作为构建上下文：

- 本地目录的相对或绝对路径
- Git 仓库、tar 包或纯文本文件的远程 URL
- 通过标准输入（stdin）传递给 `docker build` 命令的纯文本文件或 tar 包

### 文件系统上下文 (Filesystem contexts)

当您的构建上下文是一个本地目录、远程 Git 仓库或 tar 文件时，这些文件就构成了构建器在构建期间可以访问的文件集。`COPY` 和 `ADD` 等构建指令可以引用上下文中的任何文件和目录。

文件系统构建上下文会被递归处理：

- 当您指定一个本地目录或 tar 包时，所有子目录都会包含在内
- 当您指定一个远程 Git 仓库时，该仓库及其所有子模块都会包含在内

有关您可以配合构建使用的不同类型文件系统上下文的更多信息，请参阅：

- [本地文件](#本地上下文)
- [Git 仓库](#git-仓库)
- [远程 tar 包](#远程-tar-包)

### 文本文件上下文 (Text file contexts)

当您的构建上下文是一个纯文本文件时，构建器会将该文件解释为 Dockerfile。采用这种方法时，构建不使用文件系统上下文。

更多信息请参阅 [空构建上下文](#空上下文)。

## 本地上下文

要使用本地构建上下文，您可以为 `docker build` 命令指定一个相对或绝对文件路径。以下示例显示了一个使用当前目录 (`.`) 作为构建上下文的 build 命令：

```console
$ docker build .
... 
#16 [internal] load build context
#16 sha256:23ca2f94460dcbaf5b3c3edbaaa933281a4e0ea3d92fe295193e4df44dc68f85
#16 transferring context: 13.16MB 2.2s done
...
```

这使得当前工作目录中的文件和目录对构建器可用。构建器会在需要时从构建上下文中加载所需的文件。

您还可以将本地 tar 包用作构建上下文，方法是将 tar 包内容通过管道传输给 `docker build` 命令。参见 [Tar 包](#本地 tar 包)。

### 本地目录

假设有以下目录结构：

```text
.
├── index.ts
├── src/
├── Dockerfile
├── package.json
└── package-lock.json
```

如果您将此目录作为上下文传递，Dockerfile 指令可以引用这些文件并将其包含在构建中。

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

### 配合来自 stdin 的 Dockerfile 使用本地上下文

使用以下语法在利用本地文件系统文件的同时，从 stdin 读取 Dockerfile 进行镜像构建。

```console
$ docker build -f- <PATH>
```

该语法使用 `-f`（或 `--file`）选项指定要使用的 Dockerfile，并使用连字符 (`-`) 作为文件名，指示 Docker 从 stdin 读取 Dockerfile。

以下示例使用当前目录 (`.`) 作为构建上下文，并使用通过 stdin 传递的 here-document Dockerfile 构建镜像。

```bash
# 创建一个工作目录
mkdir example
cd example

# 创建一个示例文件
touch somefile.txt

# 使用当前目录作为上下文，并使用从 stdin 传递的 Dockerfile 构建镜像
docker build -t myimage:latest -f- . <<EOF
FROM busybox
COPY somefile.txt ./
RUN cat /somefile.txt
EOF
```

### 本地 tar 包

当您将 tar 包通过管道传输给 build 命令时，构建将使用该 tar 包的内容作为文件系统上下文。

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

您可以创建该目录的 tar 包并将其传给 build 以用作上下文：

```console
$ tar czf foo.tar.gz *
$ docker build - < foo.tar.gz
```

构建会从 tar 包上下文中解析 Dockerfile。您可以使用 `--file` 标志指定 Dockerfile 相对于 tar 包根目录的名称和位置。以下命令使用 tar 包中的 `test.Dockerfile` 进行构建：

```console
$ docker build --file test.Dockerfile - < foo.tar.gz
```

## 远程上下文

您可以指定远程 Git 仓库、tar 包或纯文本文件的地址作为构建上下文。

- 对于 Git 仓库，构建器会自动克隆该仓库。参见 [Git 仓库](#git-仓库)。
- 对于 tar 包，构建器会下载并解压该 tar 包的内容。参见 [远程 tar 包](#远程-tar-包)。

如果远程 tar 包是一个文本文件，构建器将不会收到 [文件系统上下文](#文件系统上下文)，而是假定该远程文件是一个 Dockerfile。参见 [空构建上下文](#空上下文)。

### Git 仓库

当您将指向 Git 仓库位置的 URL 作为参数传递给 `docker build` 时，构建器会使用该仓库作为构建上下文。

构建器执行浅克隆 (shallow clone)，仅下载 HEAD 提交，而不是整个历史记录。

构建器会递归克隆仓库及其包含的任何子模块。

```console
$ docker build https://github.com/user/myrepo.git
```

默认情况下，构建器克隆您指定的仓库默认分支上的最新提交。

#### URL 片段 (URL fragments)

您可以在 Git 仓库地址后附加 URL 片段，让构建器克隆特定的分支、标签和子目录。

URL 片段的格式为 `#ref:dir`，其中：

- `ref` 是分支名、标签名或提交哈希
- `dir` 是仓库内部的一个子目录

例如，以下命令使用 `container` 分支及该分支下的 `docker` 子目录作为构建上下文：

```console
$ docker build https://github.com/user/myrepo.git#container:docker
```

下表展示了所有有效的后缀及其对应的构建上下文：

| 构建语法后缀 | 使用的提交 | 使用的构建上下文 |
| ------------------------------ | ----------------------------- | ------------------ |
| `myrepo.git`                   | `refs/heads/<默认分支>` | `/`                |
| `myrepo.git#mytag`             | `refs/tags/mytag`             | `/`                |
| `myrepo.git#mybranch`          | `refs/heads/mybranch`         | `/`                |
| `myrepo.git#pull/42/head`      | `refs/pull/42/head`           | `/`                |
| `myrepo.git#:myfolder`         | `refs/heads/<默认分支>` | `/myfolder`        |
| `myrepo.git#master:myfolder`   | `refs/heads/master`           | `/myfolder`        |
| `myrepo.git#mytag:myfolder`    | `refs/tags/mytag`             | `/myfolder`        |
| `myrepo.git#mybranch:myfolder` | `refs/heads/mybranch`         | `/myfolder`        |

当您在 URL 片段中使用提交哈希作为 `ref` 时，请使用完整的 40 字符 SHA-1 哈希字符串。不支持短哈希（例如截断为 7 字符的哈希）。

```bash
# ✅ 以下操作有效：
docker build github.com/docker/buildx#d4f088e689b41353d74f1a0bfcd6d7c0b213aed2
# ❌ 以下操作无效，因为提交哈希被截断了：
docker build github.com/docker/buildx#d4f088e
```

#### 保留 `.git` 目录

默认情况下，BuildKit 在使用 Git 上下文时不保留 `.git` 目录。您可以通过设置 [`BUILDKIT_CONTEXT_KEEP_GIT_DIR` 构建参数](/reference/dockerfile.md#buildkit-内置构建参数) 来配置 BuildKit 保留该目录。如果您想在构建期间获取 Git 信息，这会非常有用：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
WORKDIR /src
RUN --mount=target=. \
  make REVISION=$(git rev-parse HEAD) build
```

```console
$ docker build \
  --build-arg BUILDKIT_CONTEXT_KEEP_GIT_DIR=1 \
  https://github.com/user/myrepo.git#main
```

#### 私有仓库

当您指定一个同时也是私有仓库的 Git 上下文时，构建器需要您提供必要的身份验证凭据。您可以使用 SSH 或基于令牌 (token) 的身份验证。

如果您指定的 Git 上下文是 SSH 或 Git 地址，Buildx 会自动检测并使用 SSH 凭据。默认情况下，这会使用 `$SSH_AUTH_SOCK`。您可以通过 [`--ssh` 标志](/reference/cli/docker/buildx/build.md#ssh) 配置要使用的 SSH 凭据。

```console
$ docker buildx build --ssh default git@github.com:user/private.git
```

如果您想改用基于令牌的身份验证，可以通过 [`--secret` 标志](/reference/cli/docker/buildx/build.md#secret) 传递令牌。

```console
$ GIT_AUTH_TOKEN=<令牌内容> docker buildx build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/user/private.git
```

> [!NOTE]
> 
> 请勿使用 `--build-arg` 来传递机密信息。

### 配合来自 stdin 的 Dockerfile 使用远程上下文

使用以下语法在利用远程上下文的同时，从 stdin 读取 Dockerfile 进行镜像构建。

```console
$ docker build -f- <URL>
```

该语法使用 `-f`（或 `--file`）选项指定要使用的 Dockerfile，并使用连字符 (`-`) 作为文件名，指示 Docker 从 stdin 读取 Dockerfile。

当您想要从一个不包含 Dockerfile 的仓库构建镜像，或者想要使用自定义 Dockerfile 构建而又不想维护自己的仓库分支时，这非常有用。

以下示例使用来自 stdin 的 Dockerfile 构建镜像，并从 GitHub 上的 [hello-world](https://github.com/docker-library/hello-world) 仓库添加 `hello.c` 文件。

```bash
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```

### 远程 tar 包

如果您传递远程 tar 包的 URL，该 URL 本身会被发送给构建器。

```console
$ docker build http://server/context.tar.gz
#1 [internal] load remote build context
#1 DONE 0.2s

#2 copy /context /
#2 DONE 0.1s
...
```

下载操作将在运行 BuildKit 守护进程的主机上执行。请注意，如果您使用的是远程 Docker 上下文或远程构建器，该主机不一定就是您发出 build 命令的机器。BuildKit 会获取 `context.tar.gz` 并将其用作构建上下文。tar 包上下文必须是符合标准 `tar` Unix 格式的归档文件，并且可以使用 `xz`、`bzip2`、`gzip` 或 `identity`（不压缩）格式中的任一种进行压缩。

## 空上下文

当您使用一个文本文件作为构建上下文时，构建器会将该文件解释为 Dockerfile。使用文本文件作为上下文意味着构建任务没有文件系统上下文。

当您的 Dockerfile 不依赖任何本地文件时，您可以使用空构建上下文进行构建。

### 如何在没有上下文的情况下构建

您可以通过标准输入流传递文本文件，或者指向远程文本文件的 URL。

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

当您在没有文件系统上下文的情况下构建时，Dockerfile 指令（如 `COPY`）无法引用本地文件：

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

这有助于避免将不需要的文件和目录发送给构建器，从而提高构建速度，特别是在使用远程构建器时。

### 文件名与位置

当您运行 build 命令时，构建客户端会在上下文的根目录下寻找名为 `.dockerignore` 的文件。如果该文件存在，则匹配文件中模式的文件和目录将在发送给构建器之前从构建上下文中移除。

如果您使用多个 Dockerfile，可以为每个 Dockerfile 使用不同的 ignore 文件。为此，您需要对 ignore 文件使用特殊的命名约定：将 ignore 文件放在与 Dockerfile 相同的目录下，并在 ignore 文件名前加上 Dockerfile 的名称，如下例所示。

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

如果两者都存在，特定于 Dockerfile 的 ignore 文件优先级高于构建上下文根目录下的 `.dockerignore` 文件。

### 语法

`.dockerignore` 文件是一个由换行符分隔的模式列表，类似于 Unix shell 的文件通配符 (globs)。忽略模式中开头和结尾的斜杠会被忽略。以下模式都会排除构建上下文根目录下 `foo` 子目录中名为 `bar` 的文件或目录：

- `/foo/bar/`
- `/foo/bar`
- `foo/bar/`
- `foo/bar`

如果 `.dockerignore` 文件中的某行以第 1 列的 `#` 开头，则该行被视为注释，在被 CLI 解释之前会被忽略。

```gitignore
#/这是一行注释
```

如果您想了解 `.dockerignore` 模式匹配逻辑的确切详情，请查看 GitHub 上的 [moby/patternmatcher 存储库](https://github.com/moby/patternmatcher/tree/main/ignorefile)，其中包含了源代码。

#### 匹配规则

以下代码片段展示了一个 `.dockerignore` 文件示例。

```text
# 注释
*/temp*
*/*/temp*
temp?
```

该文件会导致以下构建行为：

| 规则 | 行为 |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `# 注释` | 被忽略。 |
| `*/temp*` | 排除根目录下任何一级子目录中以 `temp` 开头的文件和目录。例如，普通文件 `/somedir/temporary.txt` 和目录 `/somedir/temp` 都会被排除。 |
| `*/*/temp*` | 排除根目录下两级深度子目录中以 `temp` 开头的文件和目录。例如，`/somedir/subdir/temporary.txt` 会被排除。 |
| `temp?` | 排除根目录下文件名比 `temp` 多出一个字符的文件和目录。例如，`/tempa` 和 `/tempb` 都会被排除。 |

匹配是使用 Go 语言的 [`filepath.Match` 函数](https://golang.org/pkg/path/filepath#Match) 规则完成的。预处理步骤使用 Go 语言的 [`filepath.Clean` 函数](https://golang.org/pkg/path/filepath/#Clean) 来修剪空白字符并移除 `.` 和 `..`。预处理后为空的行将被忽略。

> [!NOTE]
> 
> 出于历史原因，模式 `.` 会被忽略。

除了 Go 的 `filepath.Match` 规则外，Docker 还支持一个特殊的通配符字符串 `**`，它可以匹配任意层级的目录（包括零层）。例如，`**/*.go` 会排除构建上下文中任何位置找到的所有以 `.go` 结尾的文件。

您可以使用 `.dockerignore` 文件来排除 `Dockerfile` 和 `.dockerignore` 文件本身。这些文件仍会被发送到构建器，因为它们是运行构建所必需的。但您无法使用 `ADD`、`COPY` 或绑定挂载将这些文件复制到镜像中。

#### 取反匹配 (Negating matches)

您可以在行首加上 `!`（感叹号）来设置排除规则的例外。以下是一个使用此机制的 `.dockerignore` 文件示例：

```text
*.md
!README.md
```

上下文根目录下除 `README.md` 之外的所有 markdown 文件都会被排除。请注意，子目录下的 markdown 文件仍会被包含。

`!` 例外规则的位置会影响最终行为：`.dockerignore` 中匹配特定文件的最后一行决定了它是被包含还是被排除。考虑以下示例：

```text
*.md
!README*.md
README-secret.md
```

上下文中不会包含任何 markdown 文件，除非是符合 `README*.md` 但不是 `README-secret.md` 的文件。

再看这个示例：

```text
*.md
README-secret.md
!README*.md
```

所有的 README 文件都会被包含。中间那行没有效果，因为 `!README*.md` 匹配了 `README-secret.md` 且出现在最后。

## 命名上下文 (Named contexts)

除了默认的构建上下文（即传递给 `docker build` 命令的匿名参数）外，您还可以向构建任务传递额外的“命名上下文”。

命名上下文使用 `--build-context` 标志指定，后跟一个键值对。这允许您在构建期间包含来自多个源的文件和目录，同时保持它们在逻辑上的隔离。

```console
$ docker build --build-context docs=./docs .
```

在此示例中：

- 名为 `docs` 的上下文指向 `./docs` 目录。
- 默认上下文 (`.`) 指向当前工作目录。

### 在 Dockerfile 中使用命名上下文

Dockerfile 指令可以像引用多阶段构建中的阶段一样引用命名上下文。

例如，以下 Dockerfile：

1. 使用 `COPY` 指令将文件从默认上下文复制到当前构建阶段。
2. 绑定挂载一个命名上下文中的文件，作为构建的一部分进行处理。

```dockerfile
# syntax=docker/dockerfile:1
FROM buildbase
WORKDIR /app

# 将默认上下文中的所有文件复制到构建容器的 /app/src 目录
COPY . /app/src
RUN make bin

# 挂载名为 "docs" 的上下文中的文件来构建文档
RUN --mount=from=docs,target=/app/docs \
    make manpages
```

### 命名上下文的使用场景

使用命名上下文可以使构建 Docker 镜像更具灵活性和效率。以下是一些使用场景：

#### 示例：结合本地和远程源

您可以为不同类型的源定义独立的命名上下文。例如，考虑一个项目，其应用程序源代码在本地，但部署脚本存储在 Git 仓库中：

```console
$ docker build --build-context scripts=https://github.com/user/deployment-scripts.git .
```

在 Dockerfile 中，您可以独立使用这些上下文：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:latest

# 从主上下文复制应用代码
COPY . /opt/app

# 使用远程 "scripts" 上下文运行部署脚本
RUN --mount=from=scripts,target=/scripts /scripts/main.sh
```

#### 示例：带有自定义依赖项的动态构建

在某些场景下，您可能需要从外部源动态地向构建中注入配置文件或依赖项。命名上下文通过允许您在不修改默认构建上下文的情况下挂载不同的配置，使这一过程变得简单。

```console
$ docker build --build-context config=./configs/prod .
```

Dockerfile 示例：

```dockerfile
# syntax=docker/dockerfile:1
FROM nginx:alpine

# 使用 "config" 上下文获取环境特定的配置
COPY --from=config nginx.conf /etc/nginx/nginx.conf
```

#### 示例：固定或覆盖镜像

在 Dockerfile 中引用命名上下文的方式与引用镜像的方式相同。这意味着您可以通过使用命名上下文进行覆盖，从而更改 Dockerfile 中的镜像引用。例如，给定以下 Dockerfile：

```dockerfile
FROM alpine:{{% param example_alpine_version %}}
```

如果您想在不修改 Dockerfile 的情况下，强制镜像引用解析为另一个版本，可以向构建任务传递一个同名的上下文。例如：

```console
docker buildx build --build-context alpine:{{% param example_alpine_version %}}=docker-image://alpine:edge .
```

`docker-image://` 前缀将该上下文标记为一个镜像引用。该引用可以是本地镜像，也可以是您注册表中的镜像。

### 配合 Bake 使用命名上下文

[Bake](/manuals/build/bake/_index.md) 是内置于 `docker build` 中的工具，允许您通过配置文件管理构建配置。Bake 完全支持命名上下文。

在 Bake 文件中定义命名上下文：

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

除了使复杂的构建更易管理外，Bake 还提供了超出 CLI 上的 `docker build` 范围的额外功能。您可以使用命名上下文来创建构建流水线，其中一个目标依赖并构建在另一个目标之上。例如，考虑一个有两个 Dockerfile 的 Docker 构建设置：

- `base.Dockerfile`：用于构建基础镜像
- `app.Dockerfile`：用于构建应用程序镜像

`app.Dockerfile` 使用由 `base.Dockerfile` 生成的镜像作为其基础镜像：

```dockerfile {title=app.Dockerfile}
FROM mybaseimage
```

通常，您必须先构建基础镜像，然后将其加载到 Docker 引擎的本地镜像库或推送到注册表。通过 Bake，您可以直接引用其他目标，从而在 `app` 目标和 `base` 目标之间创建依赖关系。

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

通过此配置，`app.Dockerfile` 中对 `mybaseimage` 的引用将使用构建 `base` 目标产生的结果。构建 `app` 目标时，如果需要，也会触发 `base` 镜像的重新构建：

```console
$ docker buildx bake app
```

### 深入阅读

欲了解更多关于使用命名上下文的信息，请参阅：

- [`--build-context` CLI 参考](/reference/cli/docker/buildx/build.md#build-context)
- [配合额外的上下文使用 Bake](/manuals/build/bake/contexts.md)