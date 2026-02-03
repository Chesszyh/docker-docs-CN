---
title: 基础镜像 (Base images)
weight: 70
description: 了解什么是基础镜像以及如何创建它们
keywords: images, base image, 基础镜像, 示例
aliases:
- /articles/baseimages/
- /engine/articles/baseimages/
- /engine/userguide/eng-image/baseimages/
- /develop/develop-images/baseimages/
---

所有的 Dockerfile 都始于一个基础镜像。基础镜像是您的镜像所扩展的原始镜像。它对应 Dockerfile 中的 `FROM` 指令所指向的内容。

```dockerfile
FROM debian
```

在大多数情况下，您不需要创建自己的基础镜像。Docker Hub 包含一个庞大的 Docker 镜像库，非常适合用作构建任务的基础镜像。[Docker 官方镜像 (Docker Official Images)](../../docker-hub/image-library/trusted-content.md#docker-official-images) 拥有清晰的文档、推广最佳实践，并且会定期更新。此外，还有由受信任的发布伙伴创建、经 Docker 验证的 [Docker 认证发布者 (Docker Verified Publisher)](../../docker-hub/image-library/trusted-content.md#verified-publisher-images) 镜像。

## 创建基础镜像

如果您需要完全控制镜像的内容，可以从您选择的 Linux 发行版创建一个基础镜像，或者使用特殊的 `FROM scratch` 基础：

```dockerfile
FROM scratch
```

`scratch` 镜像通常用于创建仅包含应用程序所需内容的最小化镜像。参见 [使用 scratch 创建最小基础镜像](#使用-scratch-创建最小基础镜像)。

要创建一个发行版基础镜像，您可以使用打包为 `tar` 文件的根文件系统，并使用 `docker import` 将其导入到 Docker 中。创建基础镜像的过程取决于您想要打包的 Linux 发行版。参见 [使用 tar 创建完整镜像](#使用-tar-创建完整镜像)。

## 使用 scratch 创建最小基础镜像

保留的、最小化的 `scratch` 镜像作为构建容器的起点。在 `Dockerfile` 中使用 `scratch` 镜像会告知构建过程，您希望下一条命令成为镜像中的第一个文件系统层。

虽然 `scratch` 出现在 Docker 的 [Docker Hub 仓库](https://hub.docker.com/_/scratch) 中，但您无法拉取 (pull)、运行它，也无法为任何镜像打上名为 `scratch` 的标签。相反，您可以在 `Dockerfile` 中引用它。例如，使用 `scratch` 创建一个最小化容器：

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch
ADD hello /
CMD ["/hello"]
```

假设在 [构建上下文](/manuals/build/concepts/context.md) 的根目录下存在一个名为 `hello` 的可执行二进制文件。您可以使用以下 `docker build` 命令构建此 Docker 镜像：

```console
$ docker build --tag hello .
```

要运行您的新镜像，使用 `docker run` 命令：

```console
$ docker run --rm hello
```

只有当 `hello` 二进制文件没有运行时的任何依赖项时，此示例镜像才能成功执行。计算机程序往往依赖于运行时环境中存在的某些其他程序或资源。例如：

- 编程语言运行时
- 动态链接的 C 库
- CA 证书

在构建基础镜像（或任何镜像）时，这是一个需要考虑的重要方面。这也是为什么使用 `FROM scratch` 创建基础镜像除了小型、简单的程序外可能会非常困难的原因。另一方面，在镜像中仅包含您需要的内容，对于减小镜像体积和减少攻击面也非常重要。

## 使用 tar 创建完整镜像

通常情况下，请先从一台运行着您想要打包为基础镜像的发行版的机器开始。虽然对于某些工具（如 Debian 的 [Debootstrap](https://wiki.debian.org/Debootstrap)，也可用于构建 Ubuntu 镜像）来说，这并非强制要求。

例如，创建一个 Ubuntu 基础镜像：

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

在 [Moby GitHub 仓库](https://github.com/moby/moby/blob/master/contrib) 中有更多创建基础镜像的示例脚本。

## 更多资源

欲了解更多关于构建镜像和编写 Dockerfile 的信息，请参阅：

* [Dockerfile 参考](/reference/dockerfile.md)
* [Dockerfile 最佳实践](/manuals/build/building/best-practices.md)
* [Docker 官方镜像](../../docker-hub/image-library/trusted-content.md#docker-official-images)