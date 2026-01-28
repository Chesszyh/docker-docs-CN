---
description: 查找 Docker Desktop 已知问题
keywords: mac, troubleshooting, known issues, Docker Desktop
title: 已知问题
tags: [ Troubleshooting ]
weight: 30
aliases:
 - /desktop/troubleshoot/known-issues/
---

{{< tabs >}}
{{< tab name="For Mac with Intel chip" >}}
- Mac Activity Monitor 报告 Docker 使用的内存是实际使用量的两倍。这是由于 [macOS 中的一个 bug](https://docs.google.com/document/d/17ZiQC1Tp9iH320K-uqVLyiJmk4DHJ3c4zgQetJiKYQM/edit?usp=sharing)。

- 在从 `.dmg` 运行 `Docker.app` 后强制弹出 `.dmg` 可能导致鲸鱼图标无响应、Docker 任务在 Activity Monitor 中显示为无响应，以及某些进程消耗大量 CPU 资源。重新启动并重新启动 Docker 可解决这些问题。

- Docker Desktop 在 macOS 10.10 Yosemite 及更高版本中使用 `HyperKit` 虚拟机监控程序 (https://github.com/docker/hyperkit)。如果您使用与 `HyperKit` 存在冲突的开发工具（例如 [Intel Hardware Accelerated Execution Manager (HAXM)](https://software.intel.com/en-us/android/articles/intel-hardware-accelerated-execution-manager/)），当前的解决方法是不要同时运行它们。您可以通过临时退出 Docker Desktop 来暂停 `HyperKit`，同时使用 HAXM。这样您可以继续使用其他工具，并防止 `HyperKit` 产生干扰。

- 如果您使用的应用程序（如 [Apache Maven](https://maven.apache.org/)）需要 `DOCKER_HOST` 和 `DOCKER_CERT_PATH` 环境变量的设置，请指定这些变量以通过 Unix 套接字连接到 Docker 实例。例如：

  ```console
  $ export DOCKER_HOST=unix:///var/run/docker.sock
  ```

{{< /tab >}}
{{< tab name="For Mac with Apple silicon" >}}

- 当未安装 Rosetta 2 时，某些命令行工具无法工作。
  - 旧版本 1.x 的 `docker-compose`。请改用 Compose V2 - 输入 `docker compose`。
  - `docker-credential-ecr-login` 凭证助手。
- 某些镜像不支持 ARM64 架构。您可以添加 `--platform linux/amd64` 以使用模拟运行（或构建）Intel 镜像。

   但是，尝试在 Apple silicon 机器上通过模拟运行基于 Intel 的容器可能会崩溃，因为 QEMU 有时无法运行容器。此外，文件系统更改通知 API（`inotify`）在 QEMU 模拟下不工作。即使容器在模拟下正确运行，它们也会比原生等效版本更慢并使用更多内存。

   总之，在基于 Arm 的机器上运行基于 Intel 的容器应被视为"尽力而为"。我们建议在 Apple silicon 机器上尽可能运行 `arm64` 容器，并鼓励容器作者生成 `arm64` 或多架构版本的容器。随着越来越多的镜像被重建以[支持多种架构](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)，这个问题应该会越来越少见。
- 当 TCP 流半关闭时，用户偶尔可能会遇到数据丢失。

{{< /tab >}}
{{< /tabs >}}
