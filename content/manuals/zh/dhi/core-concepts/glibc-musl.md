---
title: Docker 强化镜像中的 glibc 和 musl 支持
linktitle: glibc 和 musl
description: 比较 DHIs 的 glibc 和 musl 变体，为您的应用程序的兼容性、大小和性能需求选择合适的基础镜像。
keywords: glibc vs musl, alpine musl image, debian glibc container, docker hardened images compatibility, c library in containers
---

Docker 强化镜像（DHI）的构建优先考虑安全性，同时不牺牲与更广泛开源和企业软件生态系统的兼容性。这种兼容性的一个关键方面是支持常见的 Linux 标准库：`glibc` 和 `musl`。

## 什么是 glibc 和 musl？

当您运行基于 Linux 的容器时，镜像的 C 库在应用程序与操作系统交互方面起着关键作用。大多数现代 Linux 发行版依赖于以下标准 C 库之一：

- `glibc`（GNU C 库）：Debian、Ubuntu 和 Red Hat Enterprise Linux 等主流发行版上的标准 C 库。它得到广泛支持，通常被认为是跨语言、框架和企业软件最兼容的选项。

- `musl`：`glibc` 的轻量级替代品，常用于 Alpine Linux 等精简发行版。虽然它提供更小的镜像大小和性能优势，但 `musl` 并不总是与期望使用 `glibc` 的软件完全兼容。

## DHI 兼容性

DHI 镜像提供基于 `glibc`（例如 Debian）和基于 `musl`（例如 Alpine）的变体。对于兼容性至关重要的企业应用程序和语言运行时，我们建议使用基于 glibc 的 DHI 镜像。

## 如何选择，glibc 还是 musl？

Docker 强化镜像提供基于 glibc（Debian）和基于 musl（Alpine）的变体，允许您为您的工作负载选择最佳匹配。

选择基于 Debian（`glibc`）的镜像如果：

- 您需要与企业工作负载、语言运行时或专有软件的广泛兼容性。
- 您正在使用 .NET、Java 或带有依赖 `glibc` 的本机扩展的 Python 等生态系统。
- 您希望最小化由于库不兼容而导致的运行时错误风险。

选择基于 Alpine（`musl`）的镜像如果：

- 您希望以更小的镜像大小和减少的表面积获得最小的占用空间。
- 您正在构建一个自定义或严格控制的应用程序堆栈，其中依赖项是已知和经过测试的。
- 您优先考虑启动速度和精简部署而不是最大兼容性。

如果您不确定，请从基于 Debian 的镜像开始以确保兼容性，并在您对应用程序的依赖项有信心后评估 Alpine。
