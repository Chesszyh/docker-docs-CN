---
title: 使用主机网络进行网络连接
description: 使用主机网络进行网络连接的教程，禁用网络隔离
keywords: networking, host, standalone
aliases:
  - /network/network-tutorial-host/
---

本系列教程介绍如何使用独立容器直接绑定到 Docker 主机的网络，不进行网络隔离。有关其他网络主题，请参阅[概述](/manuals/engine/network/_index.md)。

## 目标

本教程的目标是启动一个 `nginx` 容器，该容器直接绑定到 Docker 主机的 80 端口。从网络角度来看，这与 `nginx` 进程直接在 Docker 主机上运行而不是在容器中运行具有相同级别的隔离。然而，在所有其他方面，如存储、进程命名空间和用户命名空间，`nginx` 进程与主机是隔离的。

## 先决条件

- 此过程要求 Docker 主机上的 80 端口可用。要使 Nginx 监听不同的端口，请参阅 [`nginx` 镜像的文档](https://hub.docker.com/_/nginx/)

- `host` 网络驱动程序仅适用于 Linux 主机，并且在 Docker Desktop 4.34 及更高版本中作为可选功能提供。要在 Docker Desktop 中启用此功能，请导航到**设置**中的**资源**选项卡，然后在**网络**下选择**启用主机网络**。

## 操作步骤

1.  以分离进程的方式创建并启动容器。`--rm` 选项表示容器退出/停止后将被删除。`-d` 标志表示以分离模式（在后台）启动容器。

    ```console
    $ docker run --rm -d --network host --name my_nginx nginx
    ```

2.  通过浏览器访问
    [http://localhost:80/](http://localhost:80/) 来访问 Nginx。

3.  使用以下命令检查您的网络堆栈：

    - 检查所有网络接口，并验证没有创建新的接口。

      ```console
      $ ip addr show
      ```

    - 使用 `netstat` 命令验证哪个进程绑定到 80 端口。您需要使用 `sudo`，因为该进程由 Docker 守护进程用户拥有，否则您将无法看到其名称或 PID。

      ```console
      $ sudo netstat -tulpn | grep :80
      ```

4.  停止容器。由于容器是使用 `--rm` 选项启动的，因此它将被自动删除。

    ```console
    docker container stop my_nginx
    ```

## 其他网络教程

- [独立网络教程](/manuals/engine/network/tutorials/standalone.md)
- [Overlay 网络教程](/manuals/engine/network/tutorials/overlay.md)
- [Macvlan 网络教程](/manuals/engine/network/tutorials/macvlan.md)
