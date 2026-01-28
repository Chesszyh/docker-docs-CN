---
title: 构建驱动
description: 构建驱动是关于 BuildKit 后端如何运行以及在哪里运行的配置。
keywords: build, buildx, driver, builder, docker-container, kubernetes, remote
aliases:
  - /build/buildx/drivers/
  - /build/building/drivers/
  - /build/buildx/multiple-builders/
  - /build/drivers/
---

构建驱动（Build drivers）是关于 BuildKit 后端如何运行以及在哪里运行的配置。驱动设置是可定制的，允许对构建器进行细粒度控制。Buildx 支持以下驱动：

- `docker`：使用与 Docker 守护进程捆绑的 BuildKit 库。
- `docker-container`：使用 Docker 创建一个专用的 BuildKit 容器。
- `kubernetes`：在 Kubernetes 集群中创建 BuildKit Pod。
- `remote`：直接连接到手动管理的 BuildKit 守护进程。

不同的驱动支持不同的使用场景。默认的 `docker` 驱动优先考虑简单性和易用性。它对缓存和输出格式等高级功能的支持有限，且不可配置。其他驱动提供更多灵活性，更适合处理高级场景。

下表概述了各驱动之间的一些差异。

| 功能                         |  `docker`   | `docker-container` | `kubernetes` |      `remote`      |
| :--------------------------- | :---------: | :----------------: | :----------: | :----------------: |
| **自动加载镜像**             |     ✅      |                    |              |                    |
| **缓存导出**                 |     ✓\*     |         ✅         |      ✅      |         ✅         |
| **Tarball 输出**             |             |         ✅         |      ✅      |         ✅         |
| **多架构镜像**               |             |         ✅         |      ✅      |         ✅         |
| **BuildKit 配置**            |             |         ✅         |      ✅      | 外部管理           |

\* _`docker` 驱动不支持所有缓存导出选项。有关更多信息，请参阅[缓存存储后端](/manuals/build/cache/backends/_index.md)。_

## 加载到本地镜像存储

与使用默认 `docker` 驱动不同，使用其他驱动构建的镜像不会自动加载到本地镜像存储中。如果您不指定输出，构建结果仅导出到构建缓存。

要使用非默认驱动构建镜像并将其加载到镜像存储中，请在构建命令中使用 `--load` 标志：

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

   使用此选项后，镜像在构建完成后可在镜像存储中使用：

   ```console
   $ docker image ls
   REPOSITORY                       TAG               IMAGE ID       CREATED             SIZE
   <image>                          latest            adf3eec768a1   2 minutes ago       197MB
   ```

### 默认加载

{{< summary-bar feature_name="Load by default" >}}

您可以配置自定义构建驱动使其行为类似于默认的 `docker` 驱动，默认将镜像加载到本地镜像存储中。为此，在创建构建器时设置 `default-load` 驱动选项：

```console
$ docker buildx create --driver-opt default-load=true
```

请注意，就像使用 `docker` 驱动一样，如果您使用 `--output` 指定不同的输出格式，结果将不会加载到镜像存储中，除非您还显式指定 `--output type=docker` 或使用 `--load` 标志。

## 下一步

阅读关于每种驱动的详细信息：

  - [Docker 驱动](./docker.md)
  - [Docker container 驱动](./docker-container.md)
  - [Kubernetes 驱动](./kubernetes.md)
- [Remote 驱动](./remote.md)
