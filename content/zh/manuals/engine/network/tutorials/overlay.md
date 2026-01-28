---
title: 使用 overlay 网络进行网络连接
description: 在多个 Docker 守护进程上使用 swarm 服务和独立容器进行网络连接的教程
keywords: networking, bridge, routing, ports, swarm, overlay
aliases:
- /engine/userguide/networking/get-started-overlay/
- /network/network-tutorial-overlay/
---

本系列教程介绍 swarm 服务的网络连接。有关独立容器的网络连接，请参阅[独立容器网络连接](/manuals/engine/network/tutorials/standalone.md)。如果您需要了解更多关于 Docker 网络的一般知识，请参阅[概述](/manuals/engine/network/_index.md)。

此页面包含以下教程。您可以在 Linux、Windows 或 Mac 上运行每个教程，但对于最后一个教程，您需要在其他地方运行第二个 Docker 主机。

- [使用默认 overlay 网络](#使用默认-overlay-网络)演示如何使用 Docker 在您初始化或加入 swarm 时自动为您设置的默认 overlay 网络。此网络不是生产系统的最佳选择。

- [使用用户定义的 overlay 网络](#使用用户定义的-overlay-网络)展示如何创建和使用您自己的自定义 overlay 网络来连接服务。这是生产环境中运行服务的推荐方式。

- [为独立容器使用 overlay 网络](#为独立容器使用-overlay-网络)展示如何使用 overlay 网络在不同 Docker 守护进程上的独立容器之间进行通信。

## 先决条件

这些教程要求您至少有一个单节点 swarm，这意味着您已经在主机上启动了 Docker 并运行了 `docker swarm init`。您也可以在多节点 swarm 上运行这些示例。

## 使用默认 overlay 网络

在此示例中，您将启动一个 `alpine` 服务，并从各个服务容器的角度检查网络的特性。

本教程不涉及 overlay 网络实现方式的操作系统特定细节，而是专注于从服务的角度来看 overlay 是如何工作的。

### 先决条件

本教程需要三台可以相互通信的物理或虚拟 Docker 主机。本教程假设三台主机在同一网络上运行，没有涉及防火墙。

这些主机将被称为 `manager`、`worker-1` 和 `worker-2`。`manager` 主机将同时充当管理者和工作者，这意味着它既可以运行服务任务，也可以管理 swarm。`worker-1` 和 `worker-2` 将仅充当工作者。

如果您没有三台主机，一个简单的解决方案是在云服务提供商（如 Amazon EC2）上设置三台 Ubuntu 主机，它们都在同一网络上，允许该网络上所有主机之间的所有通信（使用 EC2 安全组等机制），然后按照 [Ubuntu 上 Docker Engine - Community 的安装说明](/manuals/engine/install/ubuntu.md)进行操作。

### 演练

#### 创建 swarm

在此过程结束时，所有三个 Docker 主机都将加入 swarm，并将使用名为 `ingress` 的 overlay 网络连接在一起。

1.  在 `manager` 上初始化 swarm。如果主机只有一个网络接口，则 `--advertise-addr` 标志是可选的。

    ```console
    $ docker swarm init --advertise-addr=<IP-ADDRESS-OF-MANAGER>
    ```

    记下打印出来的文本，因为它包含您将用于将 `worker-1` 和 `worker-2` 加入 swarm 的令牌。最好将令牌存储在密码管理器中。

2.  在 `worker-1` 上加入 swarm。如果主机只有一个网络接口，则 `--advertise-addr` 标志是可选的。

    ```console
    $ docker swarm join --token <TOKEN> \
      --advertise-addr <IP-ADDRESS-OF-WORKER-1> \
      <IP-ADDRESS-OF-MANAGER>:2377
    ```

3.  在 `worker-2` 上加入 swarm。如果主机只有一个网络接口，则 `--advertise-addr` 标志是可选的。

    ```console
    $ docker swarm join --token <TOKEN> \
      --advertise-addr <IP-ADDRESS-OF-WORKER-2> \
      <IP-ADDRESS-OF-MANAGER>:2377
    ```

4.  在 `manager` 上列出所有节点。此命令只能从管理者执行。

    ```console
    $ docker node ls

    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    d68ace5iraw6whp7llvgjpu48 *   ip-172-31-34-146    Ready               Active              Leader
    nvp5rwavvb8lhdggo8fcf7plg     ip-172-31-35-151    Ready               Active
    ouvx2l7qfcxisoyms8mtkgahw     ip-172-31-36-89     Ready               Active
    ```

    您也可以使用 `--filter` 标志按角色过滤：

    ```console
    $ docker node ls --filter role=manager

    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    d68ace5iraw6whp7llvgjpu48 *   ip-172-31-34-146    Ready               Active              Leader

    $ docker node ls --filter role=worker

    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    nvp5rwavvb8lhdggo8fcf7plg     ip-172-31-35-151    Ready               Active
    ouvx2l7qfcxisoyms8mtkgahw     ip-172-31-36-89     Ready               Active
    ```

5.  在 `manager`、`worker-1` 和 `worker-2` 上列出 Docker 网络，并注意它们现在都有一个名为 `ingress` 的 overlay 网络和一个名为 `docker_gwbridge` 的桥接网络。这里只显示 `manager` 的列表：

    ```console
    $ docker network ls

    NETWORK ID          NAME                DRIVER              SCOPE
    495c570066be        bridge              bridge              local
    961c6cae9945        docker_gwbridge     bridge              local
    ff35ceda3643        host                host                local
    trtnl4tqnc3n        ingress             overlay             swarm
    c8357deec9cb        none                null                local
    ```

`docker_gwbridge` 将 `ingress` 网络连接到 Docker 主机的网络接口，以便流量可以流入和流出 swarm 管理者和工作者。如果您创建 swarm 服务而不指定网络，它们将连接到 `ingress` 网络。建议您为每个将一起工作的应用程序或应用程序组使用单独的 overlay 网络。在下一个过程中，您将创建两个 overlay 网络并将服务连接到每个网络。

#### 创建服务

1.  在 `manager` 上创建一个名为 `nginx-net` 的新 overlay 网络：

    ```console
    $ docker network create -d overlay nginx-net
    ```

    您不需要在其他节点上创建 overlay 网络，因为当其中一个节点开始运行需要它的服务任务时，它将自动创建。

2.  在 `manager` 上创建一个连接到 `nginx-net` 的 5 副本 Nginx 服务。该服务将向外部发布 80 端口。所有服务任务容器可以相互通信，而无需打开任何端口。

    > [!NOTE]
    >
    > 服务只能在管理者上创建。

    ```console
    $ docker service create \
      --name my-nginx \
      --publish target=80,published=80 \
      --replicas=5 \
      --network nginx-net \
      nginx
      ```

      当您不为 `--publish` 标志指定 `mode` 时，使用的默认发布模式是 `ingress`，这意味着如果您浏览到 `manager`、`worker-1` 或 `worker-2` 的 80 端口，您将连接到 5 个服务任务中某一个的 80 端口，即使您浏览的节点上当前没有运行任务。如果您想使用 `host` 模式发布端口，您可以在 `--publish` 输出中添加 `mode=host`。但是，在这种情况下，您还应该使用 `--mode global` 而不是 `--replicas=5`，因为在给定节点上只有一个服务任务可以绑定给定端口。

3.  运行 `docker service ls` 来监控服务启动的进度，这可能需要几秒钟。

4.  在 `manager`、`worker-1` 和 `worker-2` 上检查 `nginx-net` 网络。请记住，您不需要在 `worker-1` 和 `worker-2` 上手动创建它，因为 Docker 为您创建了它。输出会很长，但请注意 `Containers` 和 `Peers` 部分。`Containers` 列出了从该主机连接到 overlay 网络的所有服务任务（或独立容器）。

5.  从 `manager` 上使用 `docker service inspect my-nginx` 检查服务，并注意有关服务使用的端口和端点的信息。

6.  创建一个新网络 `nginx-net-2`，然后更新服务以使用此网络而不是 `nginx-net`：

    ```console
    $ docker network create -d overlay nginx-net-2
    ```

    ```console
    $ docker service update \
      --network-add nginx-net-2 \
      --network-rm nginx-net \
      my-nginx
    ```

7.  运行 `docker service ls` 验证服务已更新并且所有任务已重新部署。运行 `docker network inspect nginx-net` 验证没有容器连接到它。对 `nginx-net-2` 运行相同的命令，并注意所有服务任务容器都连接到它。

    > [!NOTE]
    >
    > 即使 overlay 网络会在 swarm 工作节点上根据需要自动创建，但它们不会自动删除。

8.  从 `manager` 清理服务和网络。运行以下命令。管理者将指示工作者自动删除网络。

    ```console
    $ docker service rm my-nginx
    $ docker network rm nginx-net nginx-net-2
    ```

## 使用用户定义的 overlay 网络

### 先决条件

本教程假设 swarm 已经设置好，并且您在管理者上。

### 演练

1.  创建用户定义的 overlay 网络。

    ```console
    $ docker network create -d overlay my-overlay
    ```

2.  使用 overlay 网络启动服务，并将 80 端口发布到 Docker 主机上的 8080 端口。

    ```console
    $ docker service create \
      --name my-nginx \
      --network my-overlay \
      --replicas 1 \
      --publish published=8080,target=80 \
      nginx:latest
    ```

3.  运行 `docker network inspect my-overlay`，通过查看 `Containers` 部分验证 `my-nginx` 服务任务是否连接到它。

4.  删除服务和网络。

    ```console
    $ docker service rm my-nginx

    $ docker network rm my-overlay
    ```

## 为独立容器使用 overlay 网络

此示例演示 DNS 容器发现——具体来说，是如何使用 overlay 网络在不同 Docker 守护进程上的独立容器之间进行通信。步骤如下：

- 在 `host1` 上，将节点初始化为 swarm（管理者）。
- 在 `host2` 上，将节点加入 swarm（工作者）。
- 在 `host1` 上，创建一个可附加的 overlay 网络（`test-net`）。
- 在 `host1` 上，在 `test-net` 上运行一个交互式 [alpine](https://hub.docker.com/_/alpine/) 容器（`alpine1`）。
- 在 `host2` 上，在 `test-net` 上运行一个交互式且分离的 [alpine](https://hub.docker.com/_/alpine/) 容器（`alpine2`）。
- 在 `host1` 上，从 `alpine1` 的会话中 ping `alpine2`。

### 先决条件

对于此测试，您需要两个可以相互通信的不同 Docker 主机。每个主机必须在两个 Docker 主机之间打开以下端口：

- TCP 端口 2377
- TCP 和 UDP 端口 7946
- UDP 端口 4789

设置此环境的一个简单方法是拥有两个虚拟机（在本地或在 AWS 等云服务提供商上），每个虚拟机都安装并运行 Docker。如果您使用 AWS 或类似的云计算平台，最简单的配置是使用安全组，该安全组在两个主机之间打开所有入站端口，并从您客户端的 IP 地址打开 SSH 端口。

此示例将 swarm 中的两个节点称为 `host1` 和 `host2`。此示例还使用 Linux 主机，但相同的命令在 Windows 上也可以工作。

### 演练

1.  设置 swarm。

    a.  在 `host1` 上，初始化一个 swarm（如果提示，使用 `--advertise-addr` 指定与 swarm 中其他主机通信的接口的 IP 地址，例如 AWS 上的私有 IP 地址）：


    ```console
    $ docker swarm init
    Swarm initialized: current node (vz1mm9am11qcmo979tlrlox42) is now a manager.

    To add a worker to this swarm, run the following command:

        docker swarm join --token SWMTKN-1-5g90q48weqrtqryq4kj6ow0e8xm9wmv9o6vgqc5j320ymybd5c-8ex8j0bc40s6hgvy5ui5gl4gy 172.31.47.252:2377

    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
    ```

    b.  在 `host2` 上，按照上面的说明加入 swarm：

    ```console
    $ docker swarm join --token <your_token> <your_ip_address>:2377
    This node joined a swarm as a worker.
    ```

    如果节点无法加入 swarm，`docker swarm join` 命令会超时。要解决此问题，在 `host2` 上运行 `docker swarm leave --force`，验证您的网络和防火墙设置，然后重试。

2.  在 `host1` 上，创建一个名为 `test-net` 的可附加 overlay 网络：

    ```console
    $ docker network create --driver=overlay --attachable test-net
    uqsof8phj3ak0rq9k86zta6ht
    ```

    > 注意返回的 **NETWORK ID** —— 当您从 `host2` 连接到它时会再次看到它。

3.  在 `host1` 上，启动一个连接到 `test-net` 的交互式（`-it`）容器（`alpine1`）：

    ```console
    $ docker run -it --name alpine1 --network test-net alpine
    / #
    ```

4.  在 `host2` 上，列出可用的网络——注意 `test-net` 尚不存在：

    ```console
    $ docker network ls
    NETWORK ID          NAME                DRIVER              SCOPE
    ec299350b504        bridge              bridge              local
    66e77d0d0e9a        docker_gwbridge     bridge              local
    9f6ae26ccb82        host                host                local
    omvdxqrda80z        ingress             overlay             swarm
    b65c952a4b2b        none                null                local
    ```

5.  在 `host2` 上，启动一个连接到 `test-net` 的分离（`-d`）且交互式（`-it`）的容器（`alpine2`）：

    ```console
    $ docker run -dit --name alpine2 --network test-net alpine
    fb635f5ece59563e7b8b99556f816d24e6949a5f6a5b1fbd92ca244db17a4342
    ```

    > [!NOTE]
    >
    > 自动 DNS 容器发现仅适用于唯一的容器名称。

6. 在 `host2` 上，验证 `test-net` 已创建（并且与 `host1` 上的 `test-net` 具有相同的 NETWORK ID）：

    ```console
    $ docker network ls
    NETWORK ID          NAME                DRIVER              SCOPE
    ...
    uqsof8phj3ak        test-net            overlay             swarm
    ```

7.  在 `host1` 上，在 `alpine1` 的交互终端中 ping `alpine2`：

    ```console
    / # ping -c 2 alpine2
    PING alpine2 (10.0.0.5): 56 data bytes
    64 bytes from 10.0.0.5: seq=0 ttl=64 time=0.600 ms
    64 bytes from 10.0.0.5: seq=1 ttl=64 time=0.555 ms

    --- alpine2 ping statistics ---
    2 packets transmitted, 2 packets received, 0% packet loss
    round-trip min/avg/max = 0.555/0.577/0.600 ms
    ```

    两个容器使用连接两个主机的 overlay 网络进行通信。如果您在 `host2` 上运行另一个_非分离_的 alpine 容器，您可以从 `host2` ping `alpine1`（这里我们添加了 [remove 选项](/reference/cli/docker/container/run/#rm)以自动清理容器）：

    ```sh
    $ docker run -it --rm --name alpine3 --network test-net alpine
    / # ping -c 2 alpine1
    / # exit
    ```

8.  在 `host1` 上，关闭 `alpine1` 会话（这也会停止容器）：

    ```console
    / # exit
    ```

9.  清理您的容器和网络：

    您必须在每个主机上独立停止和删除容器，因为 Docker 守护进程独立运行，这些是独立容器。您只需要在 `host1` 上删除网络，因为当您在 `host2` 上停止 `alpine2` 时，`test-net` 会消失。

    a.  在 `host2` 上，停止 `alpine2`，检查 `test-net` 是否已删除，然后删除 `alpine2`：

    ```console
    $ docker container stop alpine2
    $ docker network ls
    $ docker container rm alpine2
    ```

    a.  在 `host1` 上，删除 `alpine1` 和 `test-net`：

    ```console
    $ docker container rm alpine1
    $ docker network rm test-net
    ```

## 其他网络教程

- [主机网络教程](/manuals/engine/network/tutorials/host.md)
- [独立网络教程](/manuals/engine/network/tutorials/standalone.md)
- [Macvlan 网络教程](/manuals/engine/network/tutorials/macvlan.md)
