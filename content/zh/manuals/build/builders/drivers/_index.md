---
title: 构建驱动 (Build drivers)
description: 构建驱动是关于 BuildKit 后端如何运行以及在何处运行的配置。
keywords: build, buildx, driver, builder, docker-container, kubernetes, remote, 驱动, 构建器
aliases:
  - /build/buildx/drivers/
  - /build/building/drivers/
  - /build/buildx/multiple-builders/
  - /build/drivers/
---

构建驱动（Build drivers）是关于 BuildKit 后端如何运行以及在何处运行的配置。驱动设置是可以自定义的，允许对构建器进行精细化控制。Buildx 支持以下驱动：

- `docker`：使用 Docker 守护进程中捆绑的 BuildKit 库。
- `docker-container`：使用 Docker 创建一个专用的 BuildKit 容器。
- `kubernetes`：在 Kubernetes 集群中创建 BuildKit pod。
- `remote`：直接连接到手动管理的 BuildKit 守护进程。

不同的驱动支持不同的使用场景。默认的 `docker` 驱动优先考虑简单性和易用性。它对高级特性（如缓存和输出格式）的支持有限，且不可配置。其他驱动则提供了更多灵活性，更适合处理高级场景。

下表概述了各驱动之间的一些差异：

| 特性 | `docker` | `docker-container` | `kubernetes` | `remote` |
| :--------------------------- | :---------: | :----------------: | :----------: | :----------------: |
| **自动加载镜像** | ✅ | | | |
| **缓存导出** | ✓\* | ✅ | ✅ | ✅ |
| **Tarball 输出** | | ✅ | ✅ | ✅ |
| **多架构镜像** | | ✅ | ✅ | ✅ |
| **BuildKit 配置** | | ✅ | ✅ | 外部管理 |

\* _`docker` 驱动不支持所有的缓存导出选项。更多信息请参见 [缓存存储后端](/manuals/build/cache/backends/_index.md)。_

## 加载到本地镜像库

与使用默认的 `docker` 驱动不同，使用其他驱动构建的镜像不会自动加载到本地镜像库中。如果您不指定输出，构建结果仅导出到构建缓存中。

要使用非默认驱动构建镜像并将其加载到镜像库，请在 build 命令中使用 `--load` 标志：

   ```console
   $ docker buildx build --load -t <镜像名> --builder=container .
   ...
   => exporting to oci image format                                                                                                      7.7s
   => => exporting layers                                                                                                                4.9s
   => => exporting manifest sha256:4e4ca161fa338be2c303445411900ebbc5fc086153a0b846ac12996960b479d3                                      0.0s
   => => exporting config sha256:adf3eec768a14b6e183a1010cb96d91155a82fd722a1091440c88f3747f1f53f                                        0.0s
   => => sending tarball                                                                                                                 2.8s
   => importing to docker
   ```

   使用此选项后，镜像在构建完成后即可在镜像库中查看：

   ```console
   $ docker image ls
   REPOSITORY                       TAG               IMAGE ID       CREATED             SIZE
   <镜像名>                          latest            adf3eec768a1   2 minutes ago       197MB
   ```

### 默认加载 (Load by default)

{{< summary-bar feature_name="默认加载" >}}

您可以配置自定义构建驱动，使其行为与默认的 `docker` 驱动类似，即默认将镜像加载到本地镜像库。为此，在创建构建器时设置 `default-load` 驱动选项：

```console
$ docker buildx create --driver-opt default-load=true
```

请注意，与 `docker` 驱动类似，如果您通过 `--output` 指定了不同的输出格式，结果将不会加载到镜像库，除非您同时显式指定 `--output type=docker` 或使用 `--load` 标志。

## 下一步

了解各驱动的详细信息：

  - [Docker 驱动](./docker.md)
  - [Docker 容器驱动](./docker-container.md)
  - [Kubernetes 驱动](./kubernetes.md)
  - [远程驱动 (Remote driver)](./remote.md)