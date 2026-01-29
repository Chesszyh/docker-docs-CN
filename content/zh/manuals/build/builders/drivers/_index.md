---
title: 构建驱动程序 (Build drivers)
description: 构建驱动程序是关于 BuildKit 后端如何运行以及在何处运行的配置。
keywords: build, buildx, driver, builder, docker-container, kubernetes, remote
aliases:
  - /build/buildx/drivers/
  - /build/building/drivers/
  - /build/buildx/multiple-builders/
  - /build/drivers/
---

构建驱动程序是关于 BuildKit 后端如何运行以及在何处运行的配置。驱动程序设置是可定制的，允许对构建器进行细粒度控制。Buildx 支持以下驱动程序：

- `docker`：使用 Docker 守护进程中捆绑的 BuildKit 库。
- `docker-container`：使用 Docker 创建一个专用的 BuildKit 容器。
- `kubernetes`：在 Kubernetes 集群中创建 BuildKit Pod。
- `remote`：直接连接到手动管理的 BuildKit 守护进程。

不同的驱动程序支持不同的用例。默认的 `docker` 驱动程序优先考虑简单性和易用性。它对缓存和输出格式等高级功能的支持有限，且不可配置。其他驱动程序提供了更大的灵活性，更擅长处理高级场景。

下表概述了驱动程序之间的一些区别。

| 功能 | `docker` | `docker-container` | `kubernetes` | `remote` |
| :--- | :---: | :---: | :---: | :---: |
| **自动加载镜像** | ✅ | | | |
| **缓存导出** | ✓\* | ✅ | ✅ | ✅ |
| **Tarball 输出** | | ✅ | ✅ | ✅ |
| **多架构镜像** | | ✅ | ✅ | ✅ |
| **BuildKit 配置** | | ✅ | ✅ | 外部管理 |

\* _`docker` 驱动程序并不支持所有的缓存导出选项。有关更多信息，请参阅 [缓存存储后端](/manuals/build/cache/backends/_index.md)。_

## 加载到本地镜像库

与使用默认的 `docker` 驱动程序不同，使用其他驱动程序构建的镜像不会自动加载到本地镜像库中。如果您未指定输出，构建结果将仅导出到构建缓存中。

要使用非默认驱动程序构建镜像并将其加载到镜像库，请在构建命令中使用 `--load` 标志：

   ```console
   $ docker buildx build --load -t <image> --builder=container .
   ...
   => exporting to oci image format                                                                                                      7.7s
   => => exporting layers                                                                                                                4.9s
   => => exporting manifest sha256:4e4ca161fa338be2c303445411900ebbc5fc086153a0b846ac12996960b479d3                                      0.0s
   => => exporting config sha256:adf3eec768a14b6e183a1010cb96d91155a82fd722a1091440c88f3747f1f53f                                        0.0s
   => => sending tarball                                                                                                                 2.8s
   => importing to docker
   ```

   使用此选项，镜像在构建完成后即可在镜像库中使用：

   ```console
   $ docker image ls
   REPOSITORY                       TAG               IMAGE ID       CREATED             SIZE
   <image>                          latest            adf3eec768a1   2 minutes ago       197MB
   ```

### 默认加载

{{< summary-bar feature_name="默认加载" >}}

您可以将自定义构建驱动程序配置为以类似于默认 `docker` 驱动程序的方式工作，默认情况下将镜像加载到本地镜像库。为此，请在创建构建器时设置 `default-load` 驱动程序选项：

```console
$ docker buildx create --driver-opt default-load=true
```

请注意，就像 `docker` 驱动程序一样，如果您使用 `--output` 指定了不同的输出格式，除非您还显式指定了 `--output type=docker` 或使用了 `--load` 标志，否则结果将不会加载到镜像库。

## 下一步

阅读有关每个驱动程序的详细信息：

- [Docker 驱动程序](./docker.md)
- [Docker 容器驱动程序](./docker-container.md)
- [Kubernetes 驱动程序](./kubernetes.md)
- [远程驱动程序](./remote.md)
