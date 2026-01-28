---
title: 构建最佳实践
linkTitle: 最佳实践
weight: 60
description: 编写干净、可靠 Dockerfile 的提示、技巧和指南
keywords: base images, dockerfile, best practices, hub, official image
tags: [Best practices]
aliases:
  - /articles/dockerfile_best-practices/
  - /engine/articles/dockerfile_best-practices/
  - /engine/userguide/eng-image/dockerfile_best-practices/
  - /develop/develop-images/dockerfile_best-practices/
  - /develop/develop-images/guidelines/
  - /develop/develop-images/instructions/
  - /develop/dev-best-practices/
  - /develop/security-best-practices/
---

## 使用多阶段构建

多阶段构建（multi-stage builds）让你可以减小最终镜像的大小，通过在镜像构建和最终输出之间创建更清晰的分离。将你的 Dockerfile 指令拆分为不同的阶段，以确保生成的输出仅包含运行应用程序所需的文件。

使用多个阶段还可以通过并行执行构建步骤来让你更高效地构建。

有关更多信息，请参阅[多阶段构建](/manuals/build/building/multi-stage.md)。

### 创建可重用阶段

如果你有多个具有大量共同内容的镜像，考虑创建一个包含共享组件的可重用阶段，并基于该阶段构建你的独特阶段。Docker 只需要构建一次公共阶段。这意味着你的派生镜像可以更有效地使用 Docker 主机上的内存，并且加载速度更快。

维护一个公共基础阶段（"不要重复自己"）也比维护多个执行类似操作的不同阶段更容易。

## 选择正确的基础镜像

实现安全镜像的第一步是选择正确的基础镜像。在选择镜像时，确保它来自可信来源并保持小巧。

- [Docker 官方镜像](https://hub.docker.com/search?image_filter=official)是精选的镜像集合，具有清晰的文档，推广最佳实践，并且定期更新。它们为许多应用程序提供了可信的起点。

- [认证发布者](https://hub.docker.com/search?image_filter=store)镜像是由与 Docker 合作的组织发布和维护的高质量镜像，Docker 验证其仓库中内容的真实性。

- [Docker 赞助开源项目](https://hub.docker.com/search?image_filter=open_source)由通过[开源项目](../../docker-hub/image-library/trusted-content.md#docker-sponsored-open-source-software-images)获得 Docker 赞助的开源项目发布和维护。

当你选择基础镜像时，注意表明镜像属于这些项目的徽章。

![Docker Hub 官方和认证发布者镜像](../images/hub-official-images.webp)

从 Dockerfile 构建自己的镜像时，确保选择符合你要求的最小基础镜像。更小的基础镜像不仅提供可移植性和快速下载，还能缩小镜像大小并最大限度地减少通过依赖项引入的漏洞数量。

你还应该考虑使用两种类型的基础镜像：一种用于构建和单元测试，另一种（通常更精简）用于生产环境。在开发的后期阶段，你的镜像可能不需要构建工具，如编译器、构建系统和调试工具。具有最小依赖项的小型镜像可以大大降低攻击面。

## 经常重建你的镜像

Docker 镜像是不可变的。构建镜像就是拍摄该镜像在那一刻的快照。这包括任何基础镜像、库或你在构建中使用的其他软件。为了保持镜像最新和安全，确保经常使用更新的依赖项重建镜像。

为了确保在构建中获得最新版本的依赖项，你可以使用 `--no-cache` 选项来避免缓存命中。

```console
$ docker build --no-cache -t my-image:my-tag .
```

以下 Dockerfile 使用 `ubuntu` 镜像的 `24.04` 标签。随着时间推移，该标签可能会解析为不同的底层 `ubuntu` 镜像版本，因为发布者使用新的安全补丁和更新的库重建镜像。使用 `--no-cache`，你可以避免缓存命中并确保下载新的基础镜像和依赖项。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:24.04
RUN apt-get -y update && apt-get install -y --no-install-recommends python3
```

另请考虑[固定基础镜像版本](#固定基础镜像版本)。

## 使用 .dockerignore 排除文件

要排除与构建无关的文件，而无需重组源代码仓库，请使用 `.dockerignore` 文件。此文件支持类似于 `.gitignore` 文件的排除模式。

例如，要排除所有扩展名为 `.md` 的文件：

```plaintext
*.md
```

有关创建此文件的信息，请参阅 [Dockerignore 文件](/manuals/build/concepts/context.md#dockerignore-files)。

## 创建临时容器

你的 Dockerfile 定义的镜像应该生成尽可能临时的容器。临时意味着容器可以被停止和销毁，然后用最少的设置和配置重建和替换。

参考 _The Twelve-factor App_ 方法论下的[进程](https://12factor.net/processes)，以了解以这种无状态方式运行容器的动机。

## 不要安装不必要的包

避免仅仅因为"可能有用"就安装额外或不必要的包。例如，你不需要在数据库镜像中包含文本编辑器。

当你避免安装额外或不必要的包时，你的镜像具有更低的复杂性、更少的依赖项、更小的文件大小和更短的构建时间。

## 解耦应用程序

每个容器应该只关注一件事。将应用程序解耦到多个容器中可以更容易地水平扩展和重用容器。例如，一个 Web 应用程序堆栈可能由三个独立的容器组成，每个容器都有自己独特的镜像，以解耦的方式管理 Web 应用程序、数据库和内存缓存。

将每个容器限制为一个进程是一个很好的经验法则，但这不是硬性规则。例如，容器不仅可以[使用 init 进程生成](/manuals/engine/containers/multi-service_container.md)，某些程序还可能自行生成额外的进程。例如，[Celery](https://docs.celeryq.dev/) 可以生成多个工作进程，[Apache](https://httpd.apache.org/) 可以为每个请求创建一个进程。

使用你的最佳判断来保持容器尽可能干净和模块化。如果容器相互依赖，你可以使用 [Docker 容器网络](/manuals/engine/network/_index.md)来确保这些容器可以通信。

## 对多行参数进行排序

尽可能按字母顺序对多行参数进行排序，以便于维护。这有助于避免包的重复，并使列表更容易更新。这也使 PR 更容易阅读和审查。在反斜杠（`\`）前添加空格也有帮助。

以下是来自 [buildpack-deps 镜像](https://github.com/docker-library/buildpack-deps)的示例：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
  bzr \
  cvs \
  git \
  mercurial \
  subversion \
  && rm -rf /var/lib/apt/lists/*
```

## 利用构建缓存

构建镜像时，Docker 会按照指定顺序逐步执行 Dockerfile 中的指令。对于每条指令，Docker 会检查是否可以重用构建缓存中的指令。

了解构建缓存的工作原理以及缓存失效的发生方式，对于确保更快的构建至关重要。有关 Docker 构建缓存以及如何优化构建的更多信息，请参阅 [Docker 构建缓存](/manuals/build/cache/_index.md)。

## 固定基础镜像版本

镜像标签是可变的，这意味着发布者可以更新标签以指向新镜像。这很有用，因为它让发布者可以更新标签以指向镜像的较新版本。作为镜像使用者，这意味着当你重建镜像时，会自动获得新版本。

例如，如果你在 Dockerfile 中指定 `FROM alpine:3.21`，`3.21` 会解析为 `3.21` 的最新补丁版本。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:3.21
```

在某个时间点，`3.21` 标签可能指向镜像的版本 3.21.1。如果你在 3 个月后重建镜像，同一标签可能指向不同的版本，如 3.21.4。这种发布工作流程是最佳实践，大多数发布者使用这种标签策略，但这不是强制执行的。

这样做的缺点是，你无法保证每次构建都获得相同的结果。这可能导致破坏性更改，也意味着你没有使用的确切镜像版本的审计跟踪。

为了完全保护你的供应链完整性，你可以将镜像版本固定到特定的摘要。通过将镜像固定到摘要，即使发布者用新镜像替换标签，你也能保证始终使用相同的镜像版本。例如，以下 Dockerfile 将 Alpine 镜像固定到与之前相同的标签 `3.21`，但这次还带有摘要引用。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

使用这个 Dockerfile，即使发布者更新 `3.21` 标签，你的构建仍将使用固定的镜像版本：`a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c`。

虽然这可以帮助你避免意外更改，但每次想要更新时都必须手动查找并包含基础镜像版本的镜像摘要也更加繁琐。而且你放弃了自动安全修复，这可能是你想要获得的。

Docker Scout 的默认[**最新基础镜像**策略](../../scout/policy/_index.md#up-to-date-base-images)检查你使用的基础镜像版本实际上是否是最新版本。此策略还检查 Dockerfile 中固定的摘要是否对应正确的版本。如果发布者更新了你固定的镜像，策略评估会返回不合规状态，表明你应该更新镜像。

Docker Scout 还支持自动修复工作流程，以保持基础镜像最新。当有新的镜像摘要可用时，Docker Scout 可以自动在你的仓库上提出拉取请求，以更新你的 Dockerfile 使用最新版本。这比使用自动更改版本的标签更好，因为你可以控制，并且你有更改发生的时间和方式的审计跟踪。

有关使用 Docker Scout 自动更新基础镜像的更多信息，请参阅[修复](/manuals/scout/policy/remediation.md)。

## 在 CI 中构建和测试你的镜像

当你提交更改到源代码控制或创建拉取请求时，使用 [GitHub Actions](../ci/github-actions/_index.md) 或其他 CI/CD 流水线来自动构建和标记 Docker 镜像并进行测试。

## Dockerfile 指令

遵循以下关于如何正确使用 [Dockerfile 指令](/reference/dockerfile.md)来创建高效且可维护的 Dockerfile 的建议。

> [!TIP]
>
> 想在 VS Code 中获得更好的 Dockerfile 编辑体验？
> 查看 [Docker VS Code 扩展（Beta）](https://marketplace.visualstudio.com/items?itemName=docker.docker)，提供 linting、代码导航和漏洞扫描功能。

### FROM

尽可能使用当前的官方镜像作为镜像的基础。Docker 推荐 [Alpine 镜像](https://hub.docker.com/_/alpine/)，因为它受到严格控制且体积小（目前不到 6 MB），同时仍然是一个完整的 Linux 发行版。

有关 `FROM` 指令的更多信息，请参阅 [FROM 指令的 Dockerfile 参考](/reference/dockerfile.md#from)。

### LABEL

你可以为镜像添加标签，以帮助按项目组织镜像、记录许可信息、辅助自动化或其他原因。对于每个标签，添加以 `LABEL` 开头的一行，包含一个或多个键值对。以下示例展示了不同的可接受格式。内联包含解释性注释。

包含空格的字符串必须加引号或转义空格。内部引号字符（`"`）也必须转义。例如：

```dockerfile
# Set one or more individual labels
LABEL com.example.version="0.0.1-beta"
LABEL vendor1="ACME Incorporated"
LABEL vendor2=ZENITH\ Incorporated
LABEL com.example.release-date="2015-02-12"
LABEL com.example.version.is-production=""
```

一个镜像可以有多个标签。在 Docker 1.10 之前，建议将所有标签合并到单个 `LABEL` 指令中，以防止创建额外的层。这不再必要，但仍然支持合并标签。例如：

```dockerfile
# Set multiple labels on one line
LABEL com.example.version="0.0.1-beta" com.example.release-date="2015-02-12"
```

上面的示例也可以写成：

```dockerfile
# Set multiple labels at once, using line-continuation characters to break long lines
LABEL vendor=ACME\ Incorporated \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2015-02-12"
```

有关可接受的标签键和值的指南，请参阅[理解对象标签](/manuals/engine/manage-resources/labels.md)。有关查询标签的信息，请参阅[管理对象上的标签](/manuals/engine/manage-resources/labels.md#manage-labels-on-objects)中与过滤相关的项目。另请参阅 Dockerfile 参考中的 [LABEL](/reference/dockerfile.md#label)。

### RUN

将长的或复杂的 `RUN` 语句拆分为用反斜杠分隔的多行，以使你的 Dockerfile 更具可读性、可理解性和可维护性。

例如，你可以使用 `&&` 运算符链接命令，并使用转义字符将长命令拆分为多行。

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
```

默认情况下，反斜杠转义换行符，但你可以使用 [`escape` 指令](/reference/dockerfile.md#escape)更改它。

你还可以使用 here documents 运行多个命令而无需用管道运算符链接它们：

```dockerfile
RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
EOF
```

有关 `RUN` 的更多信息，请参阅 [RUN 指令的 Dockerfile 参考](/reference/dockerfile.md#run)。

#### apt-get

`RUN` 指令在基于 Debian 的镜像中的一个常见用例是使用 `apt-get` 安装软件。因为 `apt-get` 安装包，`RUN apt-get` 命令有几个需要注意的反直觉行为。

始终在同一个 `RUN` 语句中将 `RUN apt-get update` 与 `apt-get install` 组合使用。例如：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
```

单独在 `RUN` 语句中使用 `apt-get update` 会导致缓存问题，并导致后续的 `apt-get install` 指令失败。例如，以下 Dockerfile 会出现此问题：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y --no-install-recommends curl
```

构建镜像后，所有层都在 Docker 缓存中。假设你后来通过添加额外的包来修改 `apt-get install`，如以下 Dockerfile 所示：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y --no-install-recommends curl nginx
```

Docker 将初始指令和修改后的指令视为相同，并重用之前步骤的缓存。结果是 `apt-get update` 没有执行，因为构建使用了缓存版本。因为 `apt-get update` 没有运行，你的构建可能会获得过时版本的 `curl` 和 `nginx` 包。

使用 `RUN apt-get update && apt-get install -y --no-install-recommends` 确保你的 Dockerfile 安装最新的包版本，无需进一步编码或手动干预。这种技术称为缓存破坏。你也可以通过指定包版本来实现缓存破坏。这称为版本固定。例如：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo=1.3.*
```

版本固定强制构建检索特定版本，而不管缓存中的内容。这种技术还可以减少由于所需包中的意外更改而导致的失败。

以下是一个格式良好的 `RUN` 指令，演示了所有 `apt-get` 建议。

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    aufs-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    mercurial \
    reprepro \
    ruby1.9.1 \
    ruby1.9.1-dev \
    s3cmd=1.1.* \
    && rm -rf /var/lib/apt/lists/*
```

`s3cmd` 参数指定版本 `1.1.*`。如果镜像之前使用的是旧版本，指定新版本会导致 `apt-get update` 的缓存破坏，并确保安装新版本。在每行列出包也可以防止包重复的错误。

此外，当你通过删除 `/var/lib/apt/lists` 来清理 apt 缓存时，它会减小镜像大小，因为 apt 缓存不会存储在层中。由于 `RUN` 语句以 `apt-get update` 开始，包缓存总是在 `apt-get install` 之前刷新。

官方 Debian 和 Ubuntu 镜像[自动运行 `apt-get clean`](https://github.com/debuerreotype/debuerreotype/blob/c9542ab785e72696eb2908a6dbc9220abbabef39/scripts/debuerreotype-minimizing-config#L87-L109)，因此不需要显式调用。

#### 使用管道

某些 `RUN` 命令依赖于使用管道字符（`|`）将一个命令的输出通过管道传递给另一个命令的能力，如以下示例所示：

```dockerfile
RUN wget -O - https://some.site | wc -l > /number
```

Docker 使用 `/bin/sh -c` 解释器执行这些命令，该解释器只评估管道中最后一个操作的退出代码来确定成功。在上面的示例中，只要 `wc -l` 命令成功，即使 `wget` 命令失败，此构建步骤也会成功并生成新镜像。

如果你希望命令在管道的任何阶段因错误而失败，请在前面添加 `set -o pipefail &&`，以确保意外错误不会导致构建无意中成功。例如：

```dockerfile
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number
```

> [!NOTE]
>
> 并非所有 shell 都支持 `-o pipefail` 选项。
>
> 在基于 Debian 镜像的 `dash` shell 等情况下，考虑使用 `RUN` 的 _exec_ 形式来显式选择支持 `pipefail` 选项的 shell。例如：
>
> ```dockerfile
> RUN ["/bin/bash", "-c", "set -o pipefail && wget -O - https://some.site | wc -l > /number"]
> ```

### CMD

`CMD` 指令应用于运行镜像中包含的软件及其任何参数。`CMD` 几乎总是应该使用 `CMD ["executable", "param1", "param2"]` 的形式。因此，如果镜像用于服务（如 Apache 和 Rails），你会运行类似 `CMD ["apache2","-DFOREGROUND"]` 的命令。事实上，对于任何基于服务的镜像，都推荐使用这种形式的指令。

在大多数其他情况下，`CMD` 应该给出一个交互式 shell，如 bash、python 和 perl。例如，`CMD ["perl", "-de0"]`、`CMD ["python"]` 或 `CMD ["php", "-a"]`。使用这种形式意味着当你执行类似 `docker run -it python` 的命令时，你会进入一个可用的 shell，随时可以使用。`CMD` 很少应该以 `CMD ["param", "param"]` 的方式与 [`ENTRYPOINT`](/reference/dockerfile.md#entrypoint) 结合使用，除非你和你的预期用户已经非常熟悉 `ENTRYPOINT` 的工作原理。

有关 `CMD` 的更多信息，请参阅 [CMD 指令的 Dockerfile 参考](/reference/dockerfile.md#cmd)。

### EXPOSE

`EXPOSE` 指令指示容器监听连接的端口。因此，你应该为应用程序使用常见的传统端口。例如，包含 Apache Web 服务器的镜像将使用 `EXPOSE 80`，而包含 MongoDB 的镜像将使用 `EXPOSE 27017` 等。

对于外部访问，你的用户可以使用标志执行 `docker run`，指示如何将指定端口映射到他们选择的端口。对于容器链接，Docker 提供了从接收容器返回源容器路径的环境变量（例如，`MYSQL_PORT_3306_TCP`）。

有关 `EXPOSE` 的更多信息，请参阅 [EXPOSE 指令的 Dockerfile 参考](/reference/dockerfile.md#expose)。

### ENV

为了使新软件更容易运行，你可以使用 `ENV` 来更新容器安装的软件的 `PATH` 环境变量。例如，`ENV PATH=/usr/local/nginx/bin:$PATH` 确保 `CMD ["nginx"]` 正常工作。

`ENV` 指令还可用于提供你想要容器化的服务所需的特定环境变量，如 Postgres 的 `PGDATA`。

最后，`ENV` 还可用于设置常用版本号，以便更容易维护版本升级，如以下示例所示：

```dockerfile
ENV PG_MAJOR=9.3
ENV PG_VERSION=9.3.4
RUN curl -SL https://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgres && …
ENV PATH=/usr/local/postgres-$PG_MAJOR/bin:$PATH
```

与程序中使用常量变量而不是硬编码值类似，这种方法让你可以通过更改单个 `ENV` 指令来自动升级容器中软件的版本。

每个 `ENV` 行都会创建一个新的中间层，就像 `RUN` 命令一样。这意味着即使你在未来的层中取消设置环境变量，它仍然保留在这一层中，其值可以被转储。你可以通过创建如下 Dockerfile 并构建它来测试这一点。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ENV ADMIN_USER="mark"
RUN echo $ADMIN_USER > ./mark
RUN unset ADMIN_USER
```

```console
$ docker run --rm test sh -c 'echo $ADMIN_USER'

mark
```

要防止这种情况并真正取消设置环境变量，请使用带有 shell 命令的 `RUN` 命令，在单个层中设置、使用和取消设置变量。你可以用 `;` 或 `&&` 分隔命令。如果使用第二种方法，如果其中一个命令失败，`docker build` 也会失败。这通常是个好主意。对于 Linux Dockerfile，使用 `\` 作为行继续字符可以提高可读性。你也可以将所有命令放入 shell 脚本中，让 `RUN` 命令只运行该 shell 脚本。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN export ADMIN_USER="mark" \
    && echo $ADMIN_USER > ./mark \
    && unset ADMIN_USER
CMD sh
```

```console
$ docker run --rm test sh -c 'echo $ADMIN_USER'

```

有关 `ENV` 的更多信息，请参阅 [ENV 指令的 Dockerfile 参考](/reference/dockerfile.md#env)。

### ADD 或 COPY

`ADD` 和 `COPY` 功能相似。`COPY` 支持从[构建上下文](/manuals/build/concepts/context.md)或[多阶段构建](/manuals/build/building/multi-stage.md)中的阶段将文件基本复制到容器中。`ADD` 支持从远程 HTTPS 和 Git URL 获取文件的功能，以及在从构建上下文添加文件时自动解压 tar 文件。

你通常会希望使用 `COPY` 在多阶段构建中从一个阶段复制文件到另一个阶段。如果你需要临时从构建上下文向容器添加文件以执行 `RUN` 指令，你通常可以用绑定挂载替代 `COPY` 指令。例如，要临时添加 `requirements.txt` 文件用于 `RUN pip install` 指令：

```dockerfile
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt
```

绑定挂载比 `COPY` 更高效地将文件从构建上下文包含到容器中。请注意，绑定挂载的文件仅在单个 `RUN` 指令期间临时添加，不会保留在最终镜像中。如果你需要在最终镜像中包含来自构建上下文的文件，请使用 `COPY`。

当你需要下载远程工件作为构建的一部分时，`ADD` 指令最适合。`ADD` 比使用 `wget` 和 `tar` 等手动添加文件更好，因为它确保更精确的构建缓存。`ADD` 还内置支持远程资源的校验和验证，以及从 [Git URL](/reference/cli/docker/buildx/build.md#git-repositories) 解析分支、标签和子目录的协议。

以下示例使用 `ADD` 下载 .NET 安装程序。结合多阶段构建，最终阶段只保留 .NET 运行时，没有中间文件。

```dockerfile
# syntax=docker/dockerfile:1

FROM scratch AS src
ARG DOTNET_VERSION=8.0.0-preview.6.23329.7
ADD --checksum=sha256:270d731bd08040c6a3228115de1f74b91cf441c584139ff8f8f6503447cebdbb \
    https://dotnetcli.azureedge.net/dotnet/Runtime/$DOTNET_VERSION/dotnet-runtime-$DOTNET_VERSION-linux-arm64.tar.gz /dotnet.tar.gz

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0.0-preview.6-bookworm-slim-arm64v8 AS installer

# Retrieve .NET Runtime
RUN --mount=from=src,target=/src <<EOF
mkdir -p /dotnet
tar -oxzf /src/dotnet.tar.gz -C /dotnet
EOF

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0.0-preview.6-bookworm-slim-arm64v8

COPY --from=installer /dotnet /usr/share/dotnet
RUN ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet
```

有关 `ADD` 或 `COPY` 的更多信息，请参阅以下内容：
- [ADD 指令的 Dockerfile 参考](/reference/dockerfile.md#add)
- [COPY 指令的 Dockerfile 参考](/reference/dockerfile.md#copy)


### ENTRYPOINT

`ENTRYPOINT` 的最佳用途是设置镜像的主命令，允许该镜像像运行该命令一样运行，然后使用 `CMD` 作为默认标志。

以下是命令行工具 `s3cmd` 的镜像示例：

```dockerfile
ENTRYPOINT ["s3cmd"]
CMD ["--help"]
```

你可以使用以下命令运行镜像并显示命令的帮助：

```console
$ docker run s3cmd
```

或者，你可以使用正确的参数执行命令，如以下示例所示：

```console
$ docker run s3cmd ls s3://mybucket
```

这很有用，因为镜像名称可以同时作为二进制文件的引用，如上面的命令所示。

`ENTRYPOINT` 指令还可以与辅助脚本结合使用，使其能够以与上述命令类似的方式工作，即使启动工具可能需要多个步骤。

例如，[Postgres 官方镜像](https://hub.docker.com/_/postgres/)使用以下脚本作为其 `ENTRYPOINT`：

```bash
#!/bin/bash
set -e

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"
```


此脚本使用 [`exec` Bash 命令](https://wiki.bash-hackers.org/commands/builtin/exec)，以便最终运行的应用程序成为容器的 PID 1。这允许应用程序接收发送到容器的任何 Unix 信号。有关更多信息，请参阅 [`ENTRYPOINT` 参考](/reference/dockerfile.md#entrypoint)。

在以下示例中，辅助脚本被复制到容器中，并在容器启动时通过 `ENTRYPOINT` 运行：

```dockerfile
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["postgres"]
```

此脚本让你可以以多种方式与 Postgres 交互。

它可以简单地启动 Postgres：

```console
$ docker run postgres
```

或者，你可以使用它运行 Postgres 并向服务器传递参数：

```console
$ docker run postgres postgres --help
```

最后，你可以使用它启动一个完全不同的工具，如 Bash：

```console
$ docker run --rm -it postgres bash
```

有关 `ENTRYPOINT` 的更多信息，请参阅 [ENTRYPOINT 指令的 Dockerfile 参考](/reference/dockerfile.md#entrypoint)。

### VOLUME

你应该使用 `VOLUME` 指令来暴露任何数据库存储区域、配置存储或 Docker 容器创建的文件和文件夹。强烈建议对镜像的任何可变或用户可维护部分的组合使用 `VOLUME`。

有关 `VOLUME` 的更多信息，请参阅 [VOLUME 指令的 Dockerfile 参考](/reference/dockerfile.md#volume)。

### USER

如果服务可以在没有权限的情况下运行，请使用 `USER` 切换到非 root 用户。首先在 Dockerfile 中创建用户和组，类似于以下示例：

```dockerfile
RUN groupadd -r postgres && useradd --no-log-init -r -g postgres postgres
```

> [!NOTE]
>
> 考虑显式的 UID/GID。
>
> 镜像中的用户和组被分配一个非确定性的 UID/GID，因为无论镜像重建如何，都会分配"下一个"UID/GID。因此，如果这很关键，你应该分配一个显式的 UID/GID。

> [!NOTE]
>
> 由于 Go archive/tar 包处理稀疏文件的[未解决 bug](https://github.com/golang/go/issues/13548)，尝试在 Docker 容器内创建具有非常大 UID 的用户可能导致磁盘耗尽，因为容器层中的 `/var/log/faillog` 被填充了 NULL (\0) 字符。一个解决方法是将 `--no-log-init` 标志传递给 useradd。Debian/Ubuntu 的 `adduser` 包装器不支持此标志。

避免安装或使用 `sudo`，因为它具有不可预测的 TTY 和信号转发行为，可能导致问题。如果你确实需要类似于 `sudo` 的功能，例如以 `root` 身份初始化守护程序但以非 `root` 身份运行它，请考虑使用 ["gosu"](https://github.com/tianon/gosu)。

最后，为了减少层和复杂性，避免频繁来回切换 `USER`。

有关 `USER` 的更多信息，请参阅 [USER 指令的 Dockerfile 参考](/reference/dockerfile.md#user)。

### WORKDIR

为了清晰和可靠，你应该始终为 `WORKDIR` 使用绝对路径。此外，你应该使用 `WORKDIR` 而不是像 `RUN cd … && do-something` 这样的大量指令，这些指令难以阅读、排错和维护。

有关 `WORKDIR` 的更多信息，请参阅 [WORKDIR 指令的 Dockerfile 参考](/reference/dockerfile.md#workdir)。

### ONBUILD

`ONBUILD` 命令在当前 Dockerfile 构建完成后执行。`ONBUILD` 在从当前镜像派生 `FROM` 的任何子镜像中执行。将 `ONBUILD` 命令视为父 Dockerfile 给子 Dockerfile 的指令。

Docker 构建在子 Dockerfile 中的任何命令之前执行 `ONBUILD` 命令。

`ONBUILD` 对于将从给定镜像构建 `FROM` 的镜像很有用。例如，你会对语言栈镜像使用 `ONBUILD`，该镜像在 Dockerfile 中构建用该语言编写的任意用户软件，正如你在 [Ruby 的 `ONBUILD` 变体](https://github.com/docker-library/ruby/blob/c43fef8a60cea31eb9e7d960a076d633cb62ba8d/2.4/jessie/onbuild/Dockerfile)中看到的那样。

使用 `ONBUILD` 构建的镜像应该获得单独的标签。例如，`ruby:1.9-onbuild` 或 `ruby:2.0-onbuild`。

在 `ONBUILD` 中放置 `ADD` 或 `COPY` 时要小心。如果新构建的上下文缺少正在添加的资源，onbuild 镜像会灾难性地失败。如上所述，添加单独的标签有助于通过允许 Dockerfile 作者做出选择来缓解这种情况。

有关 `ONBUILD` 的更多信息，请参阅 [ONBUILD 指令的 Dockerfile 参考](/reference/dockerfile.md#onbuild)。
