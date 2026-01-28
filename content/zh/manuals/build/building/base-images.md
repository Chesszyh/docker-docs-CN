---
title: 基础镜像
weight: 70
description: 了解基础镜像及其创建方式
keywords: images, base image, examples
aliases:
- /articles/baseimages/
- /engine/articles/baseimages/
- /engine/userguide/eng-image/baseimages/
- /develop/develop-images/baseimages/
---

所有 Dockerfile 都从一个基础镜像（base image）开始。
基础镜像是你的镜像所扩展的镜像。
它指的是 Dockerfile 中 `FROM` 指令的内容。

```dockerfile
FROM debian
```

在大多数情况下，你不需要创建自己的基础镜像。Docker Hub 包含大量适合作为构建基础镜像的 Docker 镜像库。[Docker 官方镜像](../../docker-hub/image-library/trusted-content.md#docker-official-images)具有清晰的文档、推广最佳实践，并且定期更新。此外还有 [Docker 认证发布者](../../docker-hub/image-library/trusted-content.md#verified-publisher-images)镜像，由可信的发布合作伙伴创建，经过 Docker 验证。

## 创建基础镜像

如果你需要完全控制镜像的内容，你可以从你选择的 Linux 发行版创建自己的基础镜像，或者使用特殊的 `FROM scratch` 基础：

```dockerfile
FROM scratch
```

`scratch` 镜像通常用于创建仅包含应用程序所需内容的最小镜像。参见[使用 scratch 创建最小基础镜像](#使用-scratch-创建最小基础镜像)。

要创建发行版基础镜像，你可以使用打包为 `tar` 文件的根文件系统，并使用 `docker import` 将其导入到 Docker。创建自己的基础镜像的过程取决于你想要打包的 Linux 发行版。参见[使用 tar 创建完整镜像](#使用-tar-创建完整镜像)。

## 使用 scratch 创建最小基础镜像

保留的最小 `scratch` 镜像作为构建容器的起点。使用 `scratch` 镜像向构建过程发出信号，表示你希望 `Dockerfile` 中的下一条命令成为镜像中的第一个文件系统层。

虽然 `scratch` 出现在 Docker 的 [Docker Hub 仓库](https://hub.docker.com/_/scratch)中，但你无法拉取、运行它，或使用名称 `scratch` 标记任何镜像。相反，你可以在你的 `Dockerfile` 中引用它。例如，使用 `scratch` 创建一个最小容器：

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch
ADD hello /
CMD ["/hello"]
```

假设在[构建上下文](/manuals/build/concepts/context.md)的根目录存在一个名为 `hello` 的可执行二进制文件。你可以使用以下 `docker build` 命令构建这个 Docker 镜像：

```console
$ docker build --tag hello .
```

要运行你的新镜像，使用 `docker run` 命令：

```console
$ docker run --rm hello
```

只有当 `hello` 二进制文件没有任何运行时依赖时，这个示例镜像才能成功执行。计算机程序往往依赖于运行时环境中存在的某些其他程序或资源。例如：

- 编程语言运行时
- 动态链接的 C 库
- CA 证书

在构建基础镜像或任何镜像时，这是一个需要考虑的重要方面。这就是为什么使用 `FROM scratch` 创建基础镜像可能很困难，除非是小型、简单的程序。另一方面，只在镜像中包含你需要的内容也很重要，以减少镜像大小和攻击面。

## 使用 tar 创建完整镜像

通常，从运行你想要打包为基础镜像的发行版的工作机器开始，尽管对于某些工具（如 Debian 的 [Debootstrap](https://wiki.debian.org/Debootstrap)）这不是必需的，你也可以使用它来构建 Ubuntu 镜像。

例如，要创建 Ubuntu 基础镜像：

```dockerfile
$ sudo debootstrap noble noble > /dev/null
$ sudo tar -C noble -c . | docker import - noble

sha256:81ec9a55a92a5618161f68ae691d092bf14d700129093158297b3d01593f4ee3

$ docker run noble cat /etc/lsb-release

DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04.2 LTS"
```

在 [Moby GitHub 仓库](https://github.com/moby/moby/blob/master/contrib)中有更多创建基础镜像的示例脚本。

## 更多资源

有关构建镜像和编写 Dockerfile 的更多信息，请参阅：

* [Dockerfile 参考](/reference/dockerfile.md)
* [Dockerfile 最佳实践](/manuals/build/building/best-practices.md)
* [Docker 官方镜像](../../docker-hub/image-library/trusted-content.md#docker-official-images)
