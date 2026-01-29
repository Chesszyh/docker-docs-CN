---
title: 基础镜像 (Base images)
weight: 70
description: 了解基础镜像及其创建方式
keywords: 镜像, 基础镜像, 示例
---

所有的 Dockerfile 都从基础镜像开始。基础镜像是您的镜像所扩展的镜像。它指的是 Dockerfile 中 `FROM` 指令的内容。

```dockerfile
FROM debian
```

在大多数情况下，您不需要创建自己的基础镜像。Docker Hub 包含一个庞大的 Docker 镜像库，这些镜像适合在您的构建中用作基础镜像。[Docker 官方镜像](../../docker-hub/image-library/trusted-content.md#docker-official-images) 具有清晰的文档，推广最佳实践，并定期更新。还有 [Docker 已验证发布者 (Verified Publisher)](../../docker-hub/image-library/trusted-content.md#verified-publisher-images) 镜像，这些镜像由值得信赖的发布合作伙伴创建，并经 Docker 验证。

## 创建基础镜像

如果您需要完全控制镜像的内容，可以根据您选择的 Linux 发行版创建自己的基础镜像，或者使用特殊的 `FROM scratch` 基础镜像：

```dockerfile
FROM scratch
```

`scratch` 镜像通常用于创建仅包含应用程序所需内容的最小镜像。请参阅 [使用 scratch 创建最小基础镜像](#使用-scratch-创建最小基础镜像)。

要创建发行版基础镜像，您可以使用打包为 `tar` 文件的根文件系统，并通过 `docker import` 将其导入 Docker。创建您自己的基础镜像的过程取决于您想要打包的 Linux 发行版。请参阅 [使用 tar 创建完整镜像](#使用-tar-创建完整镜像)。

## 使用 scratch 创建最小基础镜像

预留的、最小化的 `scratch` 镜像作为构建容器的起点。使用 `scratch` 镜像向构建过程发出信号，表示您希望 `Dockerfile` 中的下一个命令成为镜像中的第一个文件系统层。

虽然 `scratch` 出现在 Docker 的 [Docker Hub 存储库](https://hub.docker.com/_/scratch)中，但您不能拉取它、运行它，或者将任何镜像命名为 `scratch`。相反，您可以在 `Dockerfile` 中引用它。例如，使用 `scratch` 创建一个最小容器：

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

要运行您的新镜像，请使用 `docker run` 命令：

```console
$ docker run --rm hello
```

只要 `hello` 二进制文件没有任何运行时依赖项，此示例镜像就可以成功执行。计算机程序往往依赖于运行时环境中存在的某些其他程序或资源。例如：

- 编程语言运行时
- 动态链接的 C 库
- CA 证书

在构建基础镜像或任何镜像时，这是一个需要考虑的重要方面。这就是为什么除了小型、简单的程序外，使用 `FROM scratch` 创建基础镜像可能会很困难。另一方面，在镜像中仅包含您需要的东西也很重要，以减少镜像大小和攻击面。

## 使用 tar 创建完整镜像

通常，从一台运行着您想要打包为基础镜像的发行版的机器开始，尽管对于某些工具（如 Debian 的 [Debootstrap](https://wiki.debian.org/Debootstrap)）来说这不是必需的，您也可以使用该工具构建 Ubuntu 镜像。

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

在 [Moby GitHub 仓库](https://github.com/moby/moby/blob/master/contrib) 中有更多用于创建基础镜像的示例脚本。

## 更多资源

有关构建镜像和编写 Dockerfile 的更多信息，请参阅：

* [Dockerfile 参考](/reference/dockerfile.md)
* [Dockerfile 最佳实践](/manuals/build/building/best-practices.md)
* [Docker 官方镜像](../../docker-hub/image-library/trusted-content.md#docker-official-images)
