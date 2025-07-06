---
title: 获取 Docker Desktop
keywords: 概念, 容器, docker desktop
description: 此概念页面将教您下载 Docker Desktop 并在 Windows、Mac 和 Linux 上安装它
summary: |
  对于
  深入研究容器化的开发人员来说，启动并运行 Docker Desktop 是至关重要的第一步，它为管理 Docker 容器提供了一个无缝且
  用户友好的界面。Docker Desktop
  简化了在
  容器中构建、共享和运行应用程序的过程，确保了不同环境之间的一致性。
weight: 1
aliases:
 - /getting-started/get-docker-desktop/
---

{{< youtube-embed C2bPVhiNU-0 >}}

## 说明

Docker Desktop 是用于构建镜像、运行容器等功能的一体化软件包。
本指南将引导您完成安装过程，使您能够亲身体验 Docker Desktop。


> **Docker Desktop 条款**
>
> 在大型企业（超过 250
> 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/?_gl=1*1nyypal*_ga*MTYxMTUxMzkzOS4xNjgzNTM0MTcw*_ga_XJWPQMJYHQ*MTcxNjk4MzU4Mi4xMjE2LjEuMTcxNjk4MzkzNS4xNy4wLjA.)。

<div class="not-prose">
{{< card
  title="Docker Desktop for Mac"
  description="[下载 (Apple Silicon)](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64) | [下载 (Intel)](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64) | [安装说明](/desktop/setup/install/mac-install)"
  icon="/icons/AppleMac.svg" >}}

{{< card
  title="Docker Desktop for Windows"
  description="[下载](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows) | [安装说明](/desktop/setup/install/windows-install)"
  icon="/icons/Windows.svg" >}}

{{< card
  title="Docker Desktop for Linux"
  description="[安装说明](/desktop/setup/install/linux/)"
  icon="/icons/Linux.svg" >}}
</div>

安装完成后，完成设置过程，您就可以运行 Docker 容器了。

## 动手试试

在这个动手指南中，您将看到如何使用 Docker Desktop 运行 Docker 容器。

按照说明使用 CLI 运行容器。


## 运行您的第一个容器

打开您的 CLI 终端并运�� `docker run` 命令来启动一个容器：



```console
$ docker run -d -p 8080:80 docker/welcome-to-docker
```

## 访问前端

对于此容器，前端可在端口 `8080` 上访问。要打开网站，请在浏览器中访问 [http://localhost:8080](http://localhost:8080)。





![在容器中运行的 Nginx Web 服务器的登录页面的屏幕截图](../docker-concepts/the-basics/images/access-the-frontend.webp?border=true)

## 使用 Docker Desktop 管理容器


1. 打开 Docker Desktop 并选择左侧边栏上的 **Containers** 字段。
2. 您可以查看有关您的容器的信息，包括日志和文件，甚至可以通过选择 **Exec** 选项卡来访问 shell。

   ![在 Docker Desktop 中执行正在运行的容器的屏幕截图](images/exec-into-docker-container.webp?border=true)


3. 选择 **Inspect** 字段以获取有关容器的详细信息。您可以执行各种操作，例如暂停、恢复、启动或停止容器，或浏览 **Logs**、**Bind mounts**、**Exec**、**Files** 和 **Stats** 选项卡。

![在 Docker Desktop 中检查正在运行的容器的屏幕截图](images/inspecting-container.webp?border=true)

Docker Desktop 通过简化不同环境中应用程序的设置、配置和兼容性，为开发人员简化了容器管理，从而解决了环境不一致和部署挑战的痛点��

## 下一步是什么？

现在您已经安装了 Docker Desktop 并运行了您的第一个容器，是时候开始使用容器进行开发了。

{{< button text="使用容器进行开发" url="develop-with-containers" >}}
