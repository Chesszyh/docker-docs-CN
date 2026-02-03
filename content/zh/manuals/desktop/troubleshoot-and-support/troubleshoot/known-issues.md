---
description: 查找 Docker Desktop 的已知问题
keywords: mac, troubleshooting, known issues, 已知问题, Docker Desktop
title: 已知问题
tags: [ Troubleshooting ]
weight: 30
aliases:
 - /desktop/troubleshoot/known-issues/
---

{{< tabs >}}
{{< tab name="针对搭载 Intel 芯片的 Mac" >}}
- Mac 活动监视器（Activity Monitor）报告的 Docker 内存占用量是实际占用量的两倍。这是由于 [macOS 中的一个 Bug](https://docs.google.com/document/d/17ZiQC1Tp9iH320K-uqVLyiJmk4DHJ3c4zgQetJiKYQM/edit?usp=sharing) 导致的。

- 在运行 `.dmg` 镜像中的 `Docker.app` 后强制退出该镜像，可能会导致鲸鱼图标无响应、活动监视器中显示 Docker 任务无响应，以及某些进程占用大量 CPU 资源。重启系统并重启 Docker 可解决此问题。

- Docker Desktop 在 macOS 10.10 Yosemite 及更高版本中使用 `HyperKit` 虚拟机管理程序（https://github.com/docker/hyperkit）。如果您正在使用的开发工具与 `HyperKit` 存在冲突，例如 [Intel Hardware Accelerated Execution Manager (HAXM)](https://software.intel.com/en-us/android/articles/intel-hardware-accelerated-execution-manager/)，目前的解决办法是不要同时运行它们。在使用 HAXM 时，可以通过暂时退出 Docker Desktop 来暂停 `HyperKit`。这样您就可以继续使用其他工具，并防止 `HyperKit` 造成干扰。

- 如果您使用的应用程序（如 [Apache Maven](https://maven.apache.org/)）需要设置 `DOCKER_HOST` 和 `DOCKER_CERT_PATH` 环境变量，请指定这些变量以通过 Unix 套接字连接到 Docker 实例。例如：

  ```console
  $ export DOCKER_HOST=unix:///var/run/docker.sock
  ```

{{< /tab >}}
{{< tab name="针对搭载 Apple 芯片的 Mac" >}}

- 如果未安装 Rosetta 2，某些命令行工具将无法工作：
  - 旧版本的 `docker-compose` (1.x)。请改用 Compose V2，输入 `docker compose`。
  - `docker-credential-ecr-login` 凭据辅助程序。
- 某些镜像不支持 ARM64 架构。您可以添加 `--platform linux/amd64` 标志，通过模拟方式运行（或构建）Intel 镜像。

   然而，在 Apple 芯片机器上通过模拟运行基于 Intel 的容器可能会导致崩溃，因为 QEMU 有时无法成功运行容器。此外，文件系统更改通知 API (`inotify`) 在 QEMU 模拟下无法正常工作。即使容器在模拟下能够正常运行，它们的速度也会比原生架构慢，且占用更多内存。

   总之，在 ARM 架构机器上运行基于 Intel 的容器应仅视为“尽力而为”。我们建议尽可能在 Apple 芯片机器上运行 `arm64` 容器，并鼓励容器作者提供其容器的 `arm64` 版本或多架构（multi-arch）版本。随着越来越多的镜像被重新构建以 [支持多种架构](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)，该问题将逐渐减少。
- 当 TCP 流处于半关闭状态时，用户偶尔可能会遇到数据丢失。

{{< /tab >}}
{{< /tabs >}}
