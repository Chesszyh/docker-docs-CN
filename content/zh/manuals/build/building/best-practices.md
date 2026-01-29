--- 
title: 构建最佳实践
linkTitle: 最佳实践 (Best practices)
weight: 60
description: 编写清晰、可靠 Dockerfile 的提示、建议和指南
keywords: 基础镜像, dockerfile, 最佳实践, hub, 官方镜像
tags: [最佳实践]
alias:
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

多阶段构建通过在镜像构建和最终输出之间建立更清晰的分隔，帮助您减小最终镜像的大小。将 Dockerfile 指令拆分为不同的阶段，以确保生成的输出仅包含运行应用程序所需的文件。

使用多个阶段还可以通过并行执行构建步骤来提高构建效率。

有关更多信息，请参阅 [多阶段构建](/manuals/build/building/multi-stage.md)。

### 创建可重用阶段

如果您有多个具有大量共同点的镜像，请考虑创建一个包含共享组件的可重用阶段，并在此基础上构建您的独特阶段。Docker 只需要构建一次通用阶段。这意味着您的派生镜像能更有效地利用 Docker 宿主机的内存，并且加载速度更快。

维护一个通用的基础阶段（“不要重复自己”）比维护多个执行类似任务的不同阶段要容易得多。

## 选择正确的基础镜像

实现镜像安全的第一步是选择正确的基础镜像。在选择镜像时，请确保它来自可信源，并保持其体积尽可能小。

- [Docker 官方镜像](https://hub.docker.com/search?image_filter=official) 是经过策划的集合，具有清晰的文档，推广最佳实践，并定期更新。它们为许多应用程序提供了可信的起点。

- [已验证发布者 (Verified Publisher)](https://hub.docker.com/search?image_filter=store) 镜像是与 Docker 合作的组织发布和维护的高质量镜像，Docker 负责验证其仓库内容的真实性。

- [Docker 赞助的开源项目 (Docker-Sponsored Open Source)](https://hub.docker.com/search?image_filter=open_source) 镜像是通过 [开源项目计划](../../docker-hub/image-library/trusted-content.md#docker-sponsored-open-source-software-images) 由 Docker 赞助的开源项目发布和维护的。

在选择基础镜像时，请留意表示该镜像属于这些计划的徽章。

![Docker Hub 官方和已验证发布者镜像](../images/hub-official-images.webp)

在根据 Dockerfile 构建自己的镜像时，请确保选择符合您要求的最小基础镜像。较小的基础镜像不仅具有便携性和快速下载的优势，还能减小镜像体积，并尽量减少通过依赖项引入的漏洞。

您还应该考虑使用两类基础镜像：一个用于构建和单元测试，另一个（通常更精简）用于生产。在开发的后期阶段，您的镜像可能不再需要编译、构建系统和调试工具等构建工具。具有最小依赖项的小型镜像可以显著减少攻击面。

## 经常重新构建镜像

Docker 镜像是不变的。构建镜像就是拍摄该时刻镜像的快照。这包括您在构建中使用的任何基础镜像、库或其他软件。为了保持您的镜像最新且安全，请确保经常使用更新后的依赖项重新构建镜像。

为了确保在构建中获得最新版本的依赖项，可以使用 `--no-cache` 选项来避免缓存命中。

```console
$ docker build --no-cache -t my-image:my-tag .
```

以下 Dockerfile 使用了 `ubuntu` 镜像的 `24.04` 标签。随着时间的推移，由于发布者使用新的安全补丁和更新后的库重新构建镜像，该标签可能会指向 `ubuntu` 镜像的不同底层版本。通过使用 `--no-cache`，您可以避免缓存命中，并确保重新下载基础镜像和依赖项。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:24.04
RUN apt-get -y update && apt-get install -y --no-install-recommends python3
```

另外请考虑 [固定基础镜像版本](#固定基础镜像版本)。

## 使用 .dockerignore 进行排除

为了在不重新组织源码库的情况下排除与构建无关的文件，请使用 `.dockerignore` 文件。此文件支持类似于 `.gitignore` 文件的排除模式。

例如，排除所有带有 `.md` 扩展名的文件：

```plaintext
*.md
```

有关如何创建它的信息，请参阅 [Dockerignore 文件](/manuals/build/concepts/context.md#dockerignore-files)。

## 创建临时容器

由 Dockerfile 定义的镜像应该生成尽可能临时的容器。这里的“临时”意味着容器可以被停止和销毁，然后通过最少的设置和配置被重新构建和替换。

请参考“12 因素应用 (The Twelve-factor App)”方法论下的 [进程 (Processes)](https://12factor.net/processes)，以了解以这种无状态方式运行容器的动机。

## 不要安装不必要的软件包

避免仅仅因为可能有用就安装额外或不必要的软件包。例如，您不需要在数据库镜像中包含文本编辑器。

避免安装额外或不必要的软件包可以降低镜像复杂性、减少依赖项、减小文件体积并缩短构建时间。

## 解耦应用程序

每个容器应该只关注一件事。将应用程序解耦到多个容器中可以更轻松地水平扩展和重用容器。例如，一个 Web 应用程序栈可能由三个独立的容器组成，每个容器都有自己独特的镜像，以解耦的方式管理 Web 应用程序、数据库和内存缓存。

将每个容器限制为一个进程是一个很好的经验法则，但这不是死板的规定。例如，容器不仅可以 [通过 init 进程生成](/manuals/engine/containers/multi-service_container.md)，一些程序也可能自行生成额外的进程。例如，[Celery](https://docs.celeryq.dev/) 可以生成多个 worker 进程，而 [Apache](https://httpd.apache.org/) 可以为每个请求创建一个进程。

请根据您的最佳判断，保持容器尽可能整洁和模块化。如果容器依赖于其他容器，您可以使用 [Docker 容器网络](/manuals/engine/network/_index.md) 来确保这些容器能够通信。

## 对多行参数排序

只要可能，请按字母数字顺序对多行参数进行排序，以方便维护。这有助于避免软件包重复，并使列表更易于更新。这也使得拉取请求 (PR) 更易于阅读和审查。在反斜杠 (`\`) 前添加一个空格也会有所帮助。

以下是来自 [buildpack-deps 镜像](https://github.com/docker-library/buildpack-deps) 的示例：

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

构建镜像时，Docker 会逐步执行 Dockerfile 中的指令，按指定的顺序执行每一条。对于每条指令，Docker 都会检查是否可以从构建缓存中重用该指令。

了解构建缓存的工作原理以及缓存失效如何发生，对于确保更快的构建至关重要。有关 Docker 构建缓存以及如何优化构建的更多信息，请参阅 [Docker 构建缓存](/manuals/build/cache/_index.md)。

## 固定基础镜像版本

镜像标签是可变的，这意味着发布者可以更新标签以指向新的镜像。这很有用，因为它允许发布者更新标签以指向镜像的较新版本。而作为镜像使用者，这意味着当您重新构建镜像时，会自动获得新版本。

例如，如果您在 Dockerfile 中指定 `FROM alpine:3.21`，`3.21` 会解析为 `3.21` 的最新补丁版本。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:3.21
```

在某一时刻，`3.21` 标签可能指向镜像的 3.21.1 版本。如果您在 3 个月后重新构建镜像，相同的标签可能指向不同的版本，例如 3.21.4。这种发布流程是最佳实践，大多数发布者都采用这种标签策略，但它并非强制性的。

这种做法的缺点是您无法保证每次构建都得到相同的内容。这可能会导致破坏性变更，也意味着您没有所使用的确切镜像版本的审计追踪。

为了完全保障您的供应链完整性，您可以将镜像版本固定到特定的摘要 (digest)。通过将镜像固定到摘要，即使发布者用新镜像替换了标签，您也能保证始终使用相同的镜像版本。例如，以下 Dockerfile 将 Alpine 镜像固定到与之前相同的标签 `3.21`，但这次还附带了摘要引用。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

使用此 Dockerfile，即使发布者更新了 `3.21` 标签，您的构建仍将使用固定的镜像版本：`a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c`。

虽然这有助于避免意外更改，但每次想要更新时都必须手动查找并包含基础镜像版本的摘要，这也很繁琐。而且您也选择了放弃自动安全修复，这通常是您希望得到的。

Docker Scout 默认的 [**基础镜像保持最新 (Up-to-Date Base Images)** 策略](../../scout/policy/_index.md#基础镜像保持最新) 会检查您使用的基础镜像版本是否确实是最新版本。此策略还会检查 Dockerfile 中固定的摘要是否对应正确的版本。如果发布者更新了您固定的镜像，策略评估将返回“不合规”状态，提示您应该更新镜像。

Docker Scout 还支持自动修复工作流，以保持基础镜像最新。当有新的镜像摘要可用时，Docker Scout 可以自动在您的代码库中发起拉取请求，以更新您的 Dockerfile 以使用最新版本。这比使用会自动更改版本的标签更好，因为您拥有控制权，并且拥有更改发生的时间和方式的审计追踪。

有关使用 Docker Scout 自动更新基础镜像的更多信息，请参阅 [修复 (Remediation)](/manuals/scout/policy/remediation.md)。

## 在 CI 中构建并测试镜像

当您向源码控制系统提交更改或创建拉取请求时，请使用 [GitHub Actions](../ci/github-actions/_index.md) 或其他 CI/CD 流水线来自动构建和标记 Docker 镜像并进行测试。

## Dockerfile 指令

遵循以下关于如何正确使用 [Dockerfile 指令](/reference/dockerfile.md) 的建议，以创建一个高效且易于维护的 Dockerfile。

> [!TIP]
> 
> 想要在 VS Code 中获得更好的 Dockerfile 编辑体验吗？
> 请查看 [Docker VS Code 扩展 (Beta)](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它支持 lint、代码导航和漏洞扫描。

### FROM

只要可能，请使用当前的官方镜像作为您镜像的基础。Docker 推荐使用 [Alpine 镜像](https://hub.docker.com/_/alpine/)，因为它经过严格控制且体积很小（目前小于 6 MB），同时仍然是一个完整的 Linux 发行版。

有关 `FROM` 指令的更多信息，请参阅 [Dockerfile FROM 指令参考](/reference/dockerfile.md#from)。

### LABEL

您可以为镜像添加标签（labels），以帮助按项目组织镜像、记录许可信息、辅助自动化或出于其他原因。对于每个标签，添加一行以 `LABEL` 开头，包含一个或多个键值对。以下示例显示了不同的可接受格式。说明性注释已内联包含。

包含空格的字符串必须加引号或对空格进行转义。内部引号字符 (`"`) 也必须进行转义。例如：

```dockerfile
# 设置一个或多个单独的标签
LABEL com.example.version="0.0.1-beta"
LABEL vendor1="ACME Incorporated"
LABEL vendor2=ZENITH\ Incorporated
LABEL com.example.release-date="2015-02-12"
LABEL com.example.version.is-production=""
```

一个镜像可以有多个标签。在 Docker 1.10 之前，建议将所有标签合并到单个 `LABEL` 指令中，以防止创建额外的层。现在这已不再必要，但仍然支持合并标签。例如：

```dockerfile
# 在一行设置多个标签
LABEL com.example.version="0.0.1-beta" com.example.release-date="2015-02-12"
```

上述示例也可以写成：

```dockerfile
# 一次设置多个标签，使用续行符拆分长行
LABEL vendor=ACME\ Incorporated \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2015-02-12"
```

请参阅 [了解对象标签](/manuals/engine/manage-resources/labels.md) 获取有关可接受的标签键和值的指南。有关查询标签的信息，请参考 [管理对象上的标签](/manuals/engine/manage-resources/labels.md#管理对象上的标签) 中与过滤相关的项。另请参阅 Dockerfile 参考中的 [LABEL](/reference/dockerfile.md#label)。

### RUN

将过长或复杂的 `RUN` 语句拆分为由反斜杠分隔的多行，以提高 Dockerfile 的可读性、可理解性和可维护性。

例如，您可以使用 `&&` 运算符链接命令，并使用转义字符将长命令分解为多行。

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
```

默认情况下，反斜杠转义换行符，但您可以使用 [`escape` 指令](/reference/dockerfile.md#escape) 更改它。

您还可以使用 here documents（在此文档）运行多个命令，而无需使用管道操作符链接它们：

```dockerfile
RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
EOF
```

有关 `RUN` 的更多信息，请参阅 [Dockerfile RUN 指令参考](/reference/dockerfile.md#run)。

#### apt-get

在基于 Debian 的镜像中，`RUN` 指令的一个常见用例是使用 `apt-get` 安装软件。由于 `apt-get` 会安装软件包，因此 `RUN apt-get` 命令有几个需要留意的、违反直觉的行为。

务必在同一个 `RUN` 语句中将 `RUN apt-get update` 与 `apt-get install` 结合使用。例如：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
```

在 `RUN` 语句中单独使用 `apt-get update` 会导致缓存问题，并导致随后的 `apt-get install` 指令失败。例如，在以下 Dockerfile 中就会出现此问题：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y --no-install-recommends curl
```

构建镜像后，所有层都在 Docker 缓存中。假设您稍后修改了 `apt-get install`，添加了一个额外的软件包，如下面的 Dockerfile 所示：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y --no-install-recommends curl nginx
```

Docker 认为初始指令和修改后的指令是相同的，并重用之前步骤的缓存。结果 `apt-get update` 不会被执行，因为构建使用了缓存版本。由于 `apt-get update` 没有运行，您的构建可能会得到过时版本的 `curl` 和 `nginx` 软件包。

使用 `RUN apt-get update && apt-get install -y --no-install-recommends` 可以确保您的 Dockerfile 安装最新的软件包版本，无需进一步的编码或手动干预。这种技术被称为“缓存粉碎 (cache busting)”。您还可以通过指定软件包版本来实现缓存粉碎。这被称为“版本固定 (version pinning)”。例如：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo=1.3.*
```

版本固定会强制构建获取特定的版本，无论缓存中有什么。此技术还可以减少由于所需软件包发生意外更改而导致的失败。

下面是一个格式良好的 `RUN` 指令，展示了所有的 `apt-get` 建议。

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

`s3cmd` 参数指定了版本 `1.1.*`。如果镜像之前使用了旧版本，指定新版本会导致 `apt-get update` 的缓存粉碎，并确保安装新版本。在每行中列出软件包还可以防止重复软件包的错误。

此外，当您通过移除 `/var/lib/apt/lists` 来清理 apt 缓存时，会减小镜像体积，因为 apt 缓存不会存储在层中。由于 `RUN` 语句以 `apt-get update` 开头，软件包缓存总是在 `apt-get install` 之前刷新。

官方的 Debian 和 Ubuntu 镜像 [自动运行 `apt-get clean`](https://github.com/debuerreotype/debuerreotype/blob/c9542ab785e72696eb2908a6dbc9220abbef39/scripts/debuerreotype-minimizing-config#L87-L109)，因此无需显式调用。

#### 使用管道

某些 `RUN` 命令依赖于将一个命令的输出通过管道符 (`|`) 传递给另一个命令的能力，如下例所示：

```dockerfile
RUN wget -O - https://some.site | wc -l > /number
```

Docker 使用 `/bin/sh -c` 解释器执行这些命令，它只评估管道中最后一个操作的退出代码来决定是否成功。在上面的例子中，只要 `wc -l` 命令成功，即使 `wget` 命令失败，此构建步骤也会成功并生成新镜像。

如果您希望命令在管道的任何阶段由于错误而失败，请在前面加上 `set -o pipefail &&`，以确保意外错误能防止构建在无意中成功。例如：

```dockerfile
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number
```

> [!NOTE]
> 
> 并非所有 shell 都支持 `-o pipefail` 选项。
> 
> 在基于 Debian 的镜像上的 `dash` shell 等情况下，请考虑使用 `RUN` 的 _exec_ 形式来显式选择确实支持 `pipefail` 选项的 shell。例如：
> 
> ```dockerfile
> RUN ["/bin/bash", "-c", "set -o pipefail && wget -O - https://some.site | wc -l > /number"]
> ```

### CMD

`CMD` 指令应被用于运行镜像中包含的软件，以及任何参数。`CMD` 几乎总是应该以 `CMD ["executable", "param1", "param2"]` 的形式使用。因此，如果镜像是针对某种服务（如 Apache 和 Rails），您应该运行类似于 `CMD ["apache2","-DFOREGROUND"]` 的命令。事实上，对于任何基于服务的镜像，都推荐使用这种形式的指令。

在大多数其他情况下，`CMD` 应被赋予一个交互式 shell，如 bash、python 和 perl。例如，`CMD ["perl", "-de0"]`、`CMD ["python"]` 或 `CMD ["php", "-a"]`。使用这种形式意味着当您执行类似于 `docker run -it python` 的命令时，您将被带入一个可用的 shell 中，随时待命。`CMD` 很少以 `CMD ["param", "param"]` 的方式与 [`ENTRYPOINT`](/reference/dockerfile.md#entrypoint) 结合使用，除非您和您的预期用户已经非常熟悉 `ENTRYPOINT` 的工作原理。

有关 `CMD` 的更多信息，请参阅 [Dockerfile CMD 指令参考](/reference/dockerfile.md#cmd)。

### EXPOSE

`EXPOSE` 指令指示容器监听连接的端口。因此，您应该为您的应用程序使用通用的传统端口。例如，包含 Apache Web 服务器的镜像将使用 `EXPOSE 80`，而包含 MongoDB 的镜像将使用 `EXPOSE 27017` 等等。

对于外部访问，您的用户可以执行带有标志的 `docker run` 命令，指示如何将指定的端口映射到他们选择的端口。对于容器链接，Docker 提供了从接收容器返回到源容器路径的环境变量（例如 `MYSQL_PORT_3306_TCP`）。

有关 `EXPOSE` 的更多信息，请参阅 [Dockerfile EXPOSE 指令参考](/reference/dockerfile.md#expose)。

### ENV

为了使新软件更易于运行，您可以使用 `ENV` 来为您容器安装的软件更新 `PATH` 环境变量。例如，`ENV PATH=/usr/local/nginx/bin:$PATH` 确保 `CMD ["nginx"]` 可以直接运行。

`ENV` 指令对于提供您想要容器化的服务所特有的必需环境变量也很有用，例如 Postgres 的 `PGDATA`。

最后，`ENV` 还可以用于设置常用的版本号，以便更轻松地维护版本升级，如下例所示：

```dockerfile
ENV PG_MAJOR=9.3
ENV PG_VERSION=9.3.4
RUN curl -SL https://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgres && …
ENV PATH=/usr/local/postgres-$PG_MAJOR/bin:$PATH
```

类似于在程序中使用常量变量而不是硬编码值，这种方法允许您更改单个 `ENV` 指令，以自动提升容器中软件的版本。

每一行 `ENV` 都会创建一个新的中间层，就像 `RUN` 命令一样。这意味着即使您在以后的层中取消设置环境变量，它仍然存在于此层中，并且其值可以被转储。您可以通过创建一个如下所示的 Dockerfile 并构建它来进行测试。

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

为了防止这种情况并真正取消设置环境变量，请使用带有 shell 命令的 `RUN` 命令，在单个层中完成设置、使用和取消设置变量的操作。您可以用 `;` 或 `&&` 分隔命令。如果您使用第二种方法，且其中一个命令失败，则 `docker build` 也会失败。这通常是一个好主意。使用 `\` 作为 Linux Dockerfile 的续行符可以提高可读性。您也可以将所有命令放入一个 shell 脚本中，并让 `RUN` 命令直接运行该 shell 脚本。

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

有关 `ENV` 的更多信息，请参阅 [Dockerfile ENV 指令参考](/reference/dockerfile.md#env)。

### ADD or COPY

`ADD` 和 `COPY` 在功能上是相似的。`COPY` 支持从 [构建上下文](/manuals/build/concepts/context.md) 或 [多阶段构建](/manuals/build/building/multi-stage.md) 中的某个阶段将文件基本复制到容器中。`ADD` 则支持从远程 HTTPS 和 Git URL 获取文件的功能，并且在从构建上下文添加文件时可以自动解压 tar 文件。

您通常会使用 `COPY` 在多阶段构建中将文件从一个阶段复制到另一个阶段。如果您需要临时将构建上下文中的文件添加到容器中以执行 `RUN` 指令，通常可以用绑定挂载 (bind mount) 代替 `COPY` 指令。例如，为 `RUN pip install` 指令临时添加一个 `requirements.txt` 文件：

```dockerfile
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt
```

与 `COPY` 相比，绑定挂载能更高效地将构建上下文中的文件包含在容器中。请注意，绑定挂载的文件仅为单个 `RUN` 指令临时添加，不会持久化到最终镜像中。如果您需要将构建上下文中的文件包含在最终镜像中，请使用 `COPY`。

当您需要下载远程构件作为构建的一部分时，`ADD` 指令是最佳选择。`ADD` 优于使用 `wget` 和 `tar` 等手动添加文件的方式，因为它能确保更精确的构建缓存。`ADD` 还内置了对远程资源校验和验证的支持，以及从 [Git URL](/reference/cli/docker/buildx/build.md#git-repositories) 解析分支、标签和子目录的协议。

以下示例使用 `ADD` 下载 .NET 安装程序。结合多阶段构建，最终阶段仅保留 .NET 运行时，没有中间文件。

```dockerfile
# syntax=docker/dockerfile:1

FROM scratch AS src
ARG DOTNET_VERSION = 8.0.0-preview.6.23329.7
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

有关 `ADD` 或 `COPY` 的更多信息，请参阅：
- [Dockerfile ADD 指令参考](/reference/dockerfile.md#add)
- [Dockerfile COPY 指令参考](/reference/dockerfile.md#copy)


### ENTRYPOINT

`ENTRYPOINT` 的最佳用途是设置镜像的主要命令，允许像运行该命令一样运行镜像，然后使用 `CMD` 作为默认标志。

以下是一个针对命令行工具 `s3cmd` 的镜像示例：

```dockerfile
ENTRYPOINT ["s3cmd"]
CMD ["--help"]
```

您可以使用以下命令运行镜像并显示命令帮助：

```console
$ docker run s3cmd
```

或者，您可以使用正确的参数来执行命令，如下例所示：

```console
$ docker run s3cmd ls s3://mybucket
```

这非常有用，因为如上条命令所示，镜像名称可以兼作对二进制文件的引用。

`ENTRYPOINT` 指令还可以与助手脚本结合使用，使其能够以类似于上述命令的方式工作，即使启动工具可能需要多个步骤。

例如，[Postgres 官方镜像](https://hub.docker.com/_/postgres/) 使用以下脚本作为其 `ENTRYPOINT`：

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


此脚本使用 [Bash 的 `exec` 命令](https://wiki.bash-hackers.org/commands/builtin/exec)，使最终运行的应用程序成为容器的 PID 1。这允许应用程序接收发送到容器的任何 Unix 信号。有关更多信息，请参阅 [`ENTRYPOINT` 参考](/reference/dockerfile.md#entrypoint)。

在以下示例中，一个助手脚本被复制到容器中，并在容器启动时通过 `ENTRYPOINT` 运行：

```dockerfile
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["postgres"]
```

此脚本允许您以几种方式与 Postgres 交互。

它可以简单地启动 Postgres：

```console
$ docker run postgres
```

或者，您可以用它运行 Postgres 并向服务器传递参数：

```console
$ docker run postgres postgres --help
```

最后，您可以用它启动一个完全不同的工具，如 Bash：

```console
$ docker run --rm -it postgres bash
```

有关 `ENTRYPOINT` 的更多信息，请参阅 [Dockerfile ENTRYPOINT 指令参考](/reference/dockerfile.md#entrypoint)。

### VOLUME

您应该使用 `VOLUME` 指令来暴露任何数据库存储区域、配置存储或由 Docker 容器创建的文件和文件夹。强烈建议您对镜像中任何可变或用户可维护的部分组合使用 `VOLUME`。

有关 `VOLUME` 的更多信息，请参阅 [Dockerfile VOLUME 指令参考](/reference/dockerfile.md#volume)。

### USER

如果服务可以在没有特权的情况下运行，请使用 `USER` 切换到非 root 用户。首先在 Dockerfile 中创建用户和组，示例如下：

```dockerfile
RUN groupadd -r postgres && useradd --no-log-init -r -g postgres postgres
```

> [!NOTE]
> 
> 考虑使用显式的 UID/GID。
> 
> 镜像中的用户和组被分配了一个不确定的 UID/GID，因为无论镜像是否重新构建，“下一个”UID/GID 都会被分配。因此，如果它是关键的，您应该分配一个显式的 UID/GID。

> [!NOTE]
> 
> 由于 Go 语言的 archive/tar 包在处理稀疏文件时存在 [未解决的 Bug](https://github.com/golang/go/issues/13548)，在 Docker 容器内部尝试创建一个具有极大 UID 的用户可能会导致磁盘耗尽，因为容器层中的 `/var/log/faillog` 被 NULL (\0) 字符填满了。一种解决方法是给 useradd 传递 `--no-log-init` 标志。Debian/Ubuntu 的 `adduser` 封装器不支持此标志。

避免安装或使用 `sudo`，因为它具有不可预测的 TTY 和信号转发行为，可能会导致问题。如果您确实需要类似于 `sudo` 的功能（例如以 `root` 身份初始化守护进程但以非 `root` 身份运行它），请考虑使用 [“gosu”](https://github.com/tianon/gosu)。

最后，为了减少层数和复杂性，请避免频繁地来回切换 `USER`。

有关 `USER` 的更多信息，请参阅 [Dockerfile USER 指令参考](/reference/dockerfile.md#user)。

### WORKDIR

为了清晰和可靠，您应该始终为 `WORKDIR` 使用绝对路径。此外，您应该使用 `WORKDIR` 而不是大量使用像 `RUN cd … && do-something` 这样难以阅读、排除故障和维护的指令。

有关 `WORKDIR` 的更多信息，请参阅 [Dockerfile WORKDIR 指令参考](/reference/dockerfile.md#workdir)。

### ONBUILD

`ONBUILD` 命令在当前 Dockerfile 构建完成后执行。`ONBUILD` 在任何派生自（`FROM`）当前镜像的子镜像中执行。可以将 `ONBUILD` 命令看作是父 Dockerfile 传达给子 Dockerfile 的指令。

Docker 构建在执行子 Dockerfile 中的任何命令之前先执行 `ONBUILD` 命令。

`ONBUILD` 对于将要基于给定镜像构建的镜像非常有用。例如，您会为语言栈镜像使用 `ONBUILD`，这类镜像在 Dockerfile 内部构建用该语言编写的任意用户软件，如您在 [Ruby 的 `ONBUILD` 变体](https://github.com/docker-library/ruby/blob/c43fef8a60cea31eb9e7d960a076d633cb62ba8d/2.4/jessie/onbuild/Dockerfile) 中所见。

使用 `ONBUILD` 构建的镜像应该获得单独的标签。例如，`ruby:1.9-onbuild` 或 `ruby:2.0-onbuild`。

在 `ONBUILD` 中放置 `ADD` 或 `COPY` 时要小心。如果新构建的上下文缺少正在添加的资源，onbuild 镜像将发生灾难性的失败。如上所述，添加一个单独的标签有助于减轻这种情况，因为它允许 Dockerfile 作者做出选择。

有关 `ONBUILD` 的更多信息，请参阅 [Dockerfile ONBUILD 指令参考](/reference/dockerfile.md#onbuild)。
