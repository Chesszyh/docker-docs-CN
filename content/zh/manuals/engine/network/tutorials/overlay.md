--- 
title: 使用 overlay 网络进行联网
description: 使用跨多个 Docker 守护进程的 swarm 服务和独立容器进行联网的教程
keywords: networking, bridge, routing, ports, swarm, overlay, 网络, 覆盖网络
alias:
- /engine/userguide/networking/get-started-overlay/
- /network/network-tutorial-overlay/
---

本系列教程涉及 swarm 服务的联网。有关独立容器的联网，请参阅 [使用独立容器进行联网](/manuals/engine/network/tutorials/standalone.md)。如果您需要了解更多关于 Docker 联网的常规知识，请参阅 [概览](/manuals/engine/network/_index.md)。

本页包含以下教程。您可以在 Linux、Windows 或 Mac 上运行每一个教程，但对于最后一个教程，您需要另一台在别处运行的 Docker 主机。

- [使用默认 overlay 网络](#use-the-default-overlay-network) 演示了如何使用 Docker 在您初始化或加入 swarm 时自动为您设置的默认 overlay 网络。该网络不是生产系统的最佳选择。

- [使用用户定义 overlay 网络](#use-a-user-defined-overlay-network) 展示了如何创建和使用您自己的自定义 overlay 网络来连接服务。这是生产中运行服务的推荐做法。

- [为独立容器使用 overlay 网络](#use-an-overlay-network-for-standalone-containers) 展示了如何在不同 Docker 守护进程上的独立容器之间使用 overlay 网络进行通信。

## 前提条件

这些教程要求您至少有一个单节点 swarm，这意味着您已经启动了 Docker 并在主机上运行了 `docker swarm init`。您也可以在多节点 swarm 上运行这些示例。

## 使用默认 overlay 网络

在此示例中，您将启动一个 `alpine` 服务，并从单个服务容器的角度检查网络的特性。

本教程不深入探讨 overlay 网络实现的操作系统特定细节，而是关注 overlay 从服务角度来看是如何运作的。

### 前提条件

本教程需要三台可以相互通信的物理或虚拟 Docker 主机。本教程假设这三台主机运行在同一个网络上，且没有涉及防火墙。

这些主机将被分别称为 `manager`、`worker-1` 和 `worker-2`。`manager` 主机将同时作为管理节点和工作节点运行，这意味着它既可以运行服务任务，也可以管理 swarm。`worker-1` 和 `worker-2` 将仅作为工作节点运行。

如果您手头没有三台主机，一个简单的解决方案是在 Amazon EC2 等云提供商上设置三台 Ubuntu 主机，让它们都在同一个网络上，且允许该网络上所有主机之间的所有通信 (使用 EC2 安全组等机制)，然后按照 [Ubuntu 上的 Docker Engine 安装说明](/manuals/engine/install/ubuntu.md) 进行操作。

### 演练

#### 创建 swarm

在此过程结束时，所有三台 Docker 主机都将加入 swarm，并使用名为 `ingress` 的 overlay 网络连接在一起。

1.  在 `manager` 上初始化 swarm。如果主机只有一个网络接口，`--advertise-addr` 标志是可选的。

    ```console
    $ docker swarm init --advertise-addr=<IP-ADDRESS-OF-MANAGER>
    ```

    记下打印出的文本，因为其中包含您将用来让 `worker-1` 和 `worker-2` 加入 swarm 的令牌。建议将该令牌存储在密码管理器中。

2.  在 `worker-1` 上加入 swarm。如果主机只有一个网络接口，`--advertise-addr` 标志是可选的。

    ```console
    $ docker swarm join --token <TOKEN> \
      --advertise-addr <IP-ADDRESS-OF-WORKER-1> \
      <IP-ADDRESS-OF-MANAGER>:2377
    ```

3.  在 `worker-2` 上加入 swarm。如果主机只有一个网络接口，`--advertise-addr` 标志是可选的。

    ```console
    $ docker swarm join --token <TOKEN> \
      --advertise-addr <IP-ADDRESS-OF-WORKER-2> \
      <IP-ADDRESS-OF-MANAGER>:2377
    ```

4.  在 `manager` 上列出所有节点。此命令只能在管理节点上执行。

    ```console
    $ docker node ls

    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    d68ace5iraw6whp7llvgjpu48 *   ip-172-31-34-146    Ready               Active              Leader
    nvp5rwavvb8lhdggo8fcf7plg     ip-172-31-35-151    Ready               Active
    ouvx2l7qfcxisoyms8mtkgahw     ip-172-31-36-89     Ready               Active
    ```

    您也可以使用 `--filter` 标志按角色进行过滤：

    ```console
    $ docker node ls --filter role=manager

    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    d68ace5iraw6whp7llvgjpu48 *   ip-172-31-34-146    Ready               Active              Leader

    $ docker node ls --filter role=worker

    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    nvp5rwavvb8lhdggo8fcf7plg     ip-172-31-35-151    Ready               Active
    ouvx2l7qfcxisoyms8mtkgahw     ip-172-31-36-89     Ready               Active
    ```

5.  在 `manager`、`worker-1` 和 `worker-2` 上列出 Docker 网络，注意它们现在各有一个名为 `ingress` 的 overlay 网络和一个名为 `docker_gwbridge` 的 bridge 网络。这里仅显示 `manager` 的列表：

    ```console
    $ docker network ls

    NETWORK ID          NAME                DRIVER              SCOPE
    495c570066be        bridge              bridge              local
    961c6cae9945        docker_gwbridge     bridge              local
    ff35ceda3643        host                host                local
    trtnl4tqnc3n        ingress             overlay             swarm
    c8357deec9cb        none                null                local
    ```

`docker_gwbridge` 将 `ingress` 网络连接到 Docker 主机的网络接口，以便流量可以往返于 swarm 管理节点和工作节点。如果您创建 swarm 服务且未指定网络，它们将连接到 `ingress` 网络。建议为您将要协同工作的每个应用程序或应用程序组使用独立的 overlay 网络。在下一个过程中，您将创建两个 overlay 网络并将一个服务连接到其中每一个。

#### 创建服务

1.  在 `manager` 上创建一个名为 `nginx-net` 的新 overlay 网络：

    ```console
    $ docker network create -d overlay nginx-net
    ```

    您不需要在其他节点上创建该 overlay 网络，因为当其中一个节点开始运行需要该网络的某个服务任务时，它会自动被创建。

2.  在 `manager` 上创建一个连接到 `nginx-net` 的 5 副本 Nginx 服务。该服务将向外界发布 80 端口。所有服务任务容器都可以在不开放任何端口的情况下相互通信。

    > [!NOTE]
    > 
    > 服务只能在管理节点上创建。

    ```console
    $ docker service create \
      --name my-nginx \
      --publish target=80,published=80 \
      --replicas=5 \
      --network nginx-net \
      nginx
      ```

      当您不为 `--publish` 标志指定 `mode` 时，使用的默认发布模式是 `ingress`。这意味着如果您访问 `manager`、`worker-1` 或 `worker-2` 的 80 端口，您将被连接到 5 个服务任务之一的 80 端口，即使您访问的节点上当前没有正在运行的任务。如果您想使用 `host` 模式发布端口，可以在 `--publish` 输出中添加 `mode=host`。但是，在这种情况下您还应该使用 `--mode global` 而不是 `--replicas=5`，因为在给定的节点上只有一个服务任务可以绑定给定的端口。

3.  运行 `docker service ls` 来监控服务启动的进度，这可能需要几秒钟。

4.  在 `manager`、`worker-1` 和 `worker-2` 上检查 `nginx-net` 网络。记住您不需要在 `worker-1` 和 `worker-2` 上手动创建它，因为 Docker 已经为您创建了。输出会很长，但请注意 `Containers` 和 `Peers` 部分。`Containers` 列出了连接到该主机的 overlay 网络的所有服务任务 (或独立容器)。

5.  在 `manager` 上，使用 `docker service inspect my-nginx` 检查服务，并注意有关服务使用的端口和端点的信息。

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

7.  运行 `docker service ls` 验证服务已更新且所有任务都已重新部署。运行 `docker network inspect nginx-net` 验证没有容器连接到它。对 `nginx-net-2` 运行同样的命令，注意到所有服务任务容器都连接到了它。

    > [!NOTE]
    > 
    > 尽管根据需要会自动在 swarm 工作节点上创建 overlay 网络，但它们不会被自动移除。

8.  清理服务和网络。在 `manager` 上运行以下命令。管理节点将指示工作节点自动移除网络。

    ```console
    $ docker service rm my-nginx
    $ docker network rm nginx-net nginx-net-2
    ```

## 使用用户定义 overlay 网络

### 前提条件

本教程假设 swarm 已经设置好且您正在管理节点上。

### 演练

1.  创建用户定义 overlay 网络。

    ```console
    $ docker network create -d overlay my-overlay
    ```

2.  启动一个使用该 overlay 网络的且将 80 端口发布到 Docker 主机 8080 端口的服务。

    ```console
    $ docker service create \
      --name my-nginx \
      --network my-overlay \
      --replicas 1 \
      --publish published=8080,target=80 \
      nginx:latest
    ```

3.  运行 `docker network inspect my-overlay` 并通过查看 `Containers` 部分验证 `my-nginx` 服务任务是否已连接到它。

4.  移除服务和网络。

    ```console
    $ docker service rm my-nginx

    $ docker network rm my-overlay
    ```

## 为独立容器使用 overlay 网络

此示例演示了 DNS 容器发现 —— 具体而言，是如何在不同 Docker 守护进程上的独立容器之间使用 overlay 网络进行通信。步骤如下：

- 在 `host1` 上，将该节点初始化为一个 swarm (管理节点)。
- 在 `host2` 上，将该节点加入该 swarm (工作节点)。
- 在 `host1` 上，创建一个可连接的 overlay 网络 (`test-net`)。
- 在 `host1` 上，运行一个连接到 `test-net` 的交互式 [alpine](https://hub.docker.com/_/alpine/) 容器 (`alpine1`)。
- 在 `host2` 上，运行一个连接到 `test-net` 的交互式、且分离的 [alpine](https://hub.docker.com/_/alpine/) 容器 (`alpine2`)。
- 在 `host1` 上，在 `alpine1` 会话中 ping `alpine2`。

### 前提条件

对于此测试，您需要两台可以相互通信的不同 Docker 主机。每台主机必须在两台 Docker 主机之间开放以下端口：

- TCP 端口 2377
- TCP 和 UDP 端口 7946
- UDP 端口 4789

一种简单的设置方法是使用两个 VM (本地或在 AWS 等云提供商上)，每个 VM 都安装并运行了 Docker。如果您正在使用 AWS 或类似的云计算平台，最简单的配置是使用一个安全组，该安全组开放两台主机之间的所有入站端口以及来自您客户端 IP 地址的 SSH 端口。

此示例将我们 swarm 中的两个节点称为 `host1` 和 `host2`。此示例也使用 Linux 主机，但相同的命令在 Windows 上也适用。

### 演练

1.  设置 swarm。

    a.  在 `host1` 上，初始化一个 swarm (如果提示，使用 `--advertise-addr` 指定与 swarm 中其他主机通信的接口 IP 地址，例如 AWS 上的私有 IP 地址)：

    ```console
    $ docker swarm init
    Swarm initialized: current node (vz1mm9am11qcmo979tlrlox42) is now a manager.

    To add a worker to this swarm, run the following command:

        docker swarm join --token SWMTKN-1-5g90q48weqrtqryq4kj6ow0e8xm9wmv9o6vgqc5j320ymybd5c-8ex8j0bc40s6hgvy5ui5gl4gy 172.31.47.252:2377

    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
    ```

    b.  在 `host2` 上，按照上面的指示加入 swarm：

    ```console
    $ docker swarm join --token <your_token> <your_ip_address>:2377
    This node joined a swarm as a worker.
    ```

    如果节点未能加入 swarm，`docker swarm join` 命令将超时。要解决此问题，在 `host2` 上运行 `docker swarm leave --force`，验证您的网络和防火墙设置，然后重试。

2.  在 `host1` 上，创建一个名为 `test-net` 的可连接 overlay 网络：

    ```console
    $ docker network create --driver=overlay --attachable test-net
    uqsof8phj3ak0rq9k86zta6ht
    ```

    > 注意返回的 **NETWORK ID** —— 当您从 `host2` 连接到它时，您将再次看到它。

3.  在 `host1` 上，启动一个交互式 (`-it`) 容器 (`alpine1`)，该容器连接到 `test-net`：

    ```console
    $ docker run -it --name alpine1 --network test-net alpine
    / #
    ```

4.  在 `host2` 上，列出可用的网络 —— 注意 `test-net` 尚未存在：

    ```console
    $ docker network ls
    NETWORK ID          NAME                DRIVER              SCOPE
    ec299350b504        bridge              bridge              local
    66e77d0d0e9a        docker_gwbridge     bridge              local
    9f6ae26ccb82        host                host                local
    omvdxqrda80z        ingress             overlay             swarm
    b65c952a4b2b        none                null                local
    ```

5.  在 `host2` 上，启动一个分离 (`-d`) 且交互式 (`-it`) 的容器 (`alpine2`)，该容器连接到 `test-net`：

    ```console
    $ docker run -dit --name alpine2 --network test-net alpine
    fb635f5ece59563e7b8b99556f816d24e6949a5f6a5b1fbd92ca244db17a4342
    ```

    > [!NOTE]
    > 
    > 自动 DNS 容器发现仅适用于唯一的容器名称。

6. 在 `host2` 上，验证 `test-net` 已创建 (并且具有与 `host1` 上的 `test-net` 相同的 NETWORK ID)：

    ```console
    $ docker network ls
    NETWORK ID          NAME                DRIVER              SCOPE
    ...
    uqsof8phj3ak        test-net            overlay             swarm
    ```

7.  在 `host1` 上，在 `alpine1` 的交互式终端内 ping `alpine2`：

    ```console
    / # ping -c 2 alpine2
    PING alpine2 (10.0.0.5): 56 data bytes
    64 bytes from 10.0.0.5: seq=0 ttl=64 time=0.600 ms
    64 bytes from 10.0.0.5: seq=1 ttl=64 time=0.555 ms

    --- alpine2 ping statistics ---
    2 packets transmitted, 2 packets received, 0% packet loss
    round-trip min/avg/max = 0.555/0.577/0.600 ms
    ```

    这两个容器通过连接两台主机的 overlay 网络进行通信。如果您在 `host2` 上运行另一个 *非分离* 的 alpine 容器，您可以从 `host2` ping `alpine1` (这里我们添加了 [移除选项](/reference/cli/docker/container/run/#rm) 以便自动清理容器)：

    ```sh
    $ docker run -it --rm --name alpine3 --network test-net alpine
    / # ping -c 2 alpine1
    / # exit
    ```

8.  在 `host1` 上，关闭 `alpine1` 会话 (这也会停止容器)：

    ```console
    / # exit
    ```

9.  清理您的容器和网络：

    由于 Docker 守护进程独立运行且这些是独立容器，您必须在每台主机上分别停止并移除容器。您只需要在 `host1` 上移除网络，因为当您在 `host2` 上停止 `alpine2` 时，`test-net` 就会消失。

    a.  在 `host2` 上，停止 `alpine2`，检查 `test-net` 是否已移除，然后移除 `alpine2`：

    ```console
    $ docker container stop alpine2
    $ docker network ls
    $ docker container rm alpine2
    ```

    a.  在 `host1` 上，移除 `alpine1` 和 `test-net`：

    ```console
    $ docker container rm alpine1
    $ docker network rm test-net
    ```

## 其他联网教程

- [Host 网络教程](/manuals/engine/network/tutorials/host.md)
- [独立运行网络教程](/manuals/engine/network/tutorials/standalone.md)
- [Macvlan 网络教程](/manuals/engine/network/tutorials/macvlan.md)
