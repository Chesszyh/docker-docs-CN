---
description: 了解 Docker Hub 的可信内容。
keywords: Docker Hub, Hub, trusted content
title: 可信内容
weight: 15
aliases:
- /trusted-content/official-images/using/
- /trusted-content/official-images/
---

Docker Hub 的可信内容（Trusted Content）提供精心策划的高质量、安全镜像选择，旨在让开发人员对其使用的资源的可靠性和安全性充满信心。这些镜像稳定、定期更新，并遵循行业最佳实践，使其成为构建和部署应用程序的坚实基础。Docker Hub 的可信内容包括 Docker 官方镜像、经过验证的发布商镜像和 Docker 赞助的开源软件镜像。

## Docker 官方镜像

Docker 官方镜像（Docker Official Images）是托管在 Docker Hub 上的一组精选 Docker 仓库。

Docker 建议您在项目中使用 Docker 官方镜像。这些镜像具有清晰的文档，遵循最佳实践，并且定期更新。Docker 官方镜像支持大多数常见用例，非常适合新的 Docker 用户。高级用户可以受益于更专业的镜像变体，也可以在学习 `Dockerfile` 的过程中审查 Docker 官方镜像。

> [!NOTE]
>
> 使用 Docker 官方镜像须遵守 [Docker 服务条款](https://www.docker.com/legal/docker-terms-service/)。

这些镜像提供了基本的基础仓库，作为大多数用户的起点。

其中包括操作系统，如 [Ubuntu](https://hub.docker.com/_/ubuntu/) 和 [Alpine](https://hub.docker.com/_/alpine/)，编程语言运行时，如 [Python](https://hub.docker.com/_/python) 和 [Node](https://hub.docker.com/_/node)，以及其他基本工具，如 [memcached](https://hub.docker.com/_/memcached) 和 [MySQL](https://hub.docker.com/_/mysql)。

这些镜像是 [Docker Hub 上最安全的镜像](https://www.docker.com/blog/enhancing-security-and-transparency-with-docker-official-images/)之一。这一点尤其重要，因为 Docker 官方镜像是 Docker Hub 上最受欢迎的镜像之一。通常，Docker 官方镜像很少或没有包含 CVE 的软件包。

这些镜像体现了 [Dockerfile 最佳实践](/manuals/build/building/best-practices.md)，并提供清晰的文档作为其他 Dockerfile 作者的参考。

属于此计划的镜像在 Docker Hub 上有一个特殊徽章，使您更容易识别属于 Docker 官方镜像的项目。

![Docker 官方镜像徽章](../images/official-image-badge-iso.png)

### 支持的标签和相应的 Dockerfile 链接

每个 Docker 官方镜像的仓库描述都包含一个 **Supported tags and respective Dockerfile links**（支持的标签和相应的 Dockerfile 链接）部分，列出了所有当前标签以及创建具有这些标签的镜像的 Dockerfile 链接。本节的目的是显示可用的镜像变体。

![示例：Ubuntu 支持的标签](../images/supported_tags.webp)

列在同一行上的标签都引用相同的底层镜像。多个标签可以指向同一个镜像。例如，在上面取自 `ubuntu` Docker 官方镜像仓库的截图中，标签 `24.04`、`noble-20240225`、`noble` 和 `devel` 都引用同一个镜像。

Docker 官方镜像的 `latest` 标签通常针对易用性进行了优化，包含各种有用的软件，如开发人员和构建工具。通过将镜像标记为 `latest`，镜像维护者实际上是建议将该镜像用作默认镜像。换句话说，如果您不知道使用哪个标签或不熟悉底层软件，您可能应该从 `latest` 镜像开始。随着您对软件和镜像变体的理解加深，您可能会发现其他镜像变体更适合您的需求。

### Slim 镜像

许多语言栈，如 [Node.js](https://hub.docker.com/_/node/)、[Python](https://hub.docker.com/_/python/) 和 [Ruby](https://hub.docker.com/_/ruby/) 都有 `slim` 标签变体，旨在提供轻量级、生产就绪的基础镜像，包含更少的软件包。

`slim` 镜像的典型使用模式是作为[多阶段构建](https://docs.docker.com/build/building/multi-stage/)最终阶段的基础镜像。例如，您在构建的第一阶段使用 `latest` 变体构建应用程序，然后将应用程序复制到基于 `slim` 变体的最终阶段。以下是一个示例 `Dockerfile`。

```dockerfile
FROM node:latest AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
FROM node:slim
WORKDIR /app
COPY --from=build /app /app
CMD ["node", "app.js"]
```

### Alpine 镜像

许多 Docker 官方镜像仓库还提供 `alpine` 变体。这些镜像构建在 [Alpine Linux](https://www.alpinelinux.org/) 发行版之上，而不是 Debian 或 Ubuntu。Alpine Linux 专注于为容器镜像提供小型、简单和安全的基础，Docker 官方镜像的 `alpine` 变体通常旨在仅安装必要的软件包。因此，Docker 官方镜像的 `alpine` 变体通常比 `slim` 变体更小。

需要注意的主要警告是 Alpine Linux 使用 [musl libc](https://musl.libc.org/) 而不是 [glibc](https://www.gnu.org/software/libc/)。此外，为了最小化镜像大小，基于 Alpine 的镜像通常默认不包含 Git 或 Bash 等工具。根据程序中 libc 需求或假设的深度，您可能会因为缺少库或工具而遇到问题。

当您使用 Alpine 镜像作为基础时，请考虑以下选项以使您的程序与 Alpine Linux 和 musl 兼容：

- 针对 musl libc 编译您的程序
- 将 glibc 库静态链接到您的程序中
- 完全避免 C 依赖（例如，在没有 CGO 的情况下构建 Go 程序）
- 在 Dockerfile 中自己添加所需的软件。

如果您不熟悉，请参阅 Docker Hub 上 `alpine` 镜像的[描述](https://hub.docker.com/_/alpine)，了解如何安装软件包的示例。

### 代号

带有看起来像《玩具总动员》角色名称（例如 `bookworm`、`bullseye` 和 `trixie`）或形容词（如 `jammy` 和 `noble`）的标签，表示它们用作基础镜像的 Linux 发行版的代号。Debian 发布代号[基于《玩具总动员》角色](https://en.wikipedia.org/wiki/Debian_version_history#Naming_convention)，而 Ubuntu 采用"形容词 动物"的形式。例如，Ubuntu 24.04 的代号是"Noble Numbat"。

Linux 发行版指示符很有帮助，因为许多 Docker 官方镜像提供基于多个底层发行版版本构建的变体（例如，`postgres:bookworm` 和 `postgres:bullseye`）。

### 其他标签

除了这里描述的内容外，Docker 官方镜像标签可能还包含其他关于镜像变体用途的提示。通常，这些标签变体在 Docker 官方镜像仓库文档中有解释。阅读"如何使用此镜像"和"镜像变体"部分将帮助您了解如何使用这些变体。

## 经过验证的发布商镜像

Docker 经过验证的发布商计划（Docker Verified Publisher）提供来自经 Docker 验证的商业发布商的高质量镜像。

这些镜像帮助开发团队构建安全的软件供应链，在早期阶段最大限度地减少恶意内容的暴露，从而节省后期的时间和金钱。

属于此计划的镜像在 Docker Hub 上有一个特殊徽章，使用户更容易识别 Docker 已验证为高质量商业发布商的项目。

![Docker 经过验证的发布商徽章](../images/verified-publisher-badge-iso.png)

## Docker 赞助的开源软件镜像

Docker 赞助的开源软件（OSS）计划提供由 Docker 赞助的开源项目发布和维护的镜像。

属于此计划的镜像在 Docker Hub 上有一个特殊徽章，使用户更容易识别 Docker 已验证为可信、安全和活跃的开源项目。

![Docker 赞助的开源软件徽章](../images/sponsored-badge-iso.png)
