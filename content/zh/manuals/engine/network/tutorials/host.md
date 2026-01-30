---
title: 使用 host 网络进行联网
description: 使用 host 网络进行联网的教程，禁用网络隔离
keywords: networking, host, standalone, 网络, 主机模式, 独立运行
---

本系列教程涉及直接绑定到 Docker 主机网络、没有网络隔离的独立容器的联网。有关其他联网主题，请参阅 [概览](/manuals/engine/network/_index.md)。

## 目标

本教程的目标是启动一个直接绑定到 Docker 主机 80 端口的 `nginx` 容器。从联网的角度来看，这与 `nginx` 进程直接运行在 Docker 主机上而不是容器中具有相同的隔离级别。然而，在所有其他方面 (如存储、进程命名空间和用户命名空间)，`nginx` 进程与主机是隔离的。

## 前提条件

- 此过程要求 Docker 主机上的 80 端口可用。要让 Nginx 在其他端口监听，请参阅 [`nginx` 镜像文档](https://hub.docker.com/_/nginx/)。

- `host` 联网驱动程序仅在 Linux 主机上工作，并且作为 Docker Desktop 4.34 及更高版本中的一项可选功能。要在 Docker Desktop 中启用此功能，请导航到 **Settings** 中的 **Resources** 选项卡，然后在 **Network** 下选择 **Enable host networking**。

## 步骤

1.  创建一个容器并将其作为分离 (detached) 进程启动。`--rm` 选项意味着一旦容器退出/停止就将其移除。`-d` 标志意味着在后台启动容器。

    ```console
    $ docker run --rm -d --network host --name my_nginx nginx
    ```

2.  通过访问 [http://localhost:80/](http://localhost:80/) 来访问 Nginx。

3.  使用以下命令检查您的网络栈：

    - 检查所有网络接口并验证是否没有创建新的接口。

      ```console
      $ ip addr show
      ```

    - 使用 `netstat` 命令验证哪个进程绑定到了 80 端口。您需要使用 `sudo`，因为该进程归 Docker 守护进程用户所有，否则您将无法看到其名称或 PID。

      ```console
      $ sudo netstat -tulpn | grep :80
      ```

4.  停止容器。由于它是使用 `--rm` 选项启动的，它将被自动移除。

    ```console
    docker container stop my_nginx
    ```

## 其他联网教程

- [独立运行网络教程](/manuals/engine/network/tutorials/standalone.md)
- [Overlay 网络教程](/manuals/engine/network/tutorials/overlay.md)
- [Macvlan 网络教程](/manuals/engine/network/tutorials/macvlan.md)
