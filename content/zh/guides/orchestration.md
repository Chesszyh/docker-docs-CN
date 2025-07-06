---
title: 部署和编排
keywords: 编排, 部署, kubernetes, swarm,
description: 了解 Docker 的一些基础知识并安装 Docker Desktop。
aliases:
  - /get-started/orchestration/
  - /guides/deployment-orchestration/orchestration/
summary: |
  探索 Docker 容器编排的基础知识。
tags: [deploy]
params:
  time: 10 分钟
---

容器化为将应用程序迁移和扩展到
云和数据中心提供了机会。容器有效地保证了这些应用程序在
任何地方都以相同的方式运行，让您能够快速轻松地利用所有
这些环境。此外，随着您扩展应用程序，您需要一些
工具来帮助自动化这些应用程序的维护，实现
故障容器的自动替换，并管理
这些容器在其生命周期内的更新和重新配置的推出。

用于管理、扩展和维护容器化应用程序的工具称为
编排器。两个最流行的编排工具是 Kubernetes 和
Docker Swarm。Docker Desktop 为这两个
编排器提供了开发环境。

高级模块教您如何：

1. [在您的开发机器上设置和使用 Kubernetes 环境](kube-deploy.md)
2. [在您的开发机器上设置和使用 Swarm 环境](swarm-deploy.md)

## 开启 Kubernetes

Docker Desktop 可以快速轻松地为您设置 Kubernetes。请按照适用于您的操作系统的设置和验证说明进行操作：

{{< tabs group="os" >}}
{{< tab name="Mac and Linux" >}}

### Mac

1.  从 Docker 仪表板，导航到 **设置**，然后选择 **Kubernetes** 选项卡。

2.  选中标有 **启用 Kubernetes** 的复选框，然后选择 **应用**。Docker Desktop 会自动为您设置 Kubernetes。当您在 **设置** 中看到“Kubernetes _正在运行_”旁边的绿灯时，您就知道 Kubernetes 已成功启用。

3.  要确认 Kubernetes 已启动并正在运行，请创建一个名为 `pod.yaml` 的文本文件，其中包含以下内容：

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: demo
    spec:
      containers:
        - name: testpod
          image: alpine:latest
          command: ["ping", "8.8.8.8"]
    ```

    这描述了一个带有一个容器的 pod，隔离了一个对 8.8.8.8 的简单 ping。

4.  在终端中，导航到您创建 `pod.yaml` 的位置并创建您的 pod：

    ```console
    $ kubectl apply -f pod.yaml
    ```

5.  检查您的 pod 是否已启动并正在运行：

    ```console
    $ kubectl get pods
    ```

    您应该会看到类似以下的内容：

    ```shell
    NAME      READY     STATUS    RESTARTS   AGE
    demo      1/1       Running   0          4s
    ```

6.  检查您是否获得了 ping 进程所期望的日志：

    ```console
    $ kubectl logs demo
    ```

    您应该会看到一个健康的 ping 进程的输出：

    ```shell
    PING 8.8.8.8 (8.8.8.8): 56 data bytes
    64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
    64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
    64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
    ...
    ```

7.  最后，拆除您的测试 pod：

    ```console
    $ kubectl delete -f pod.yaml
    ```

{{< /tab >}}
{{< tab name="Windows" >}}

### Windows

1. 从 Docker 仪表板，导航到 **设置**，然后选择 **Kubernetes** 选项卡。

2. 选中标有 **启用 Kubernetes** 的复选框，然后选择 **应用**。Docker Desktop 会自动为您设置 Kubernetes。当您在 **设置** 菜单中看到“Kubernetes _正在运行_”旁边的绿灯时，您就知道 Kubernetes 已成功启用。

3. 要确认 Kubernetes 已启动并正在运行，请创建一个名为 `pod.yaml` 的文本文件，其中包含以下内容：

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: demo
   spec:
     containers:
       - name: testpod
         image: alpine:latest
         command: ["ping", "8.8.8.8"]
   ```

   这描述了一个带有一个容器的 pod，隔离了一个对 8.8.8.8 的简单 ping。

4. 在 PowerShell 中，导航到您创建 `pod.yaml` 的位置并创建您的 pod：

   ```console
   $ kubectl apply -f pod.yaml
   ```

5. 检查您的 pod 是否已启动并正在运行：

   ```console
   $ kubectl get pods
   ```

   您应该会看到类似以下的内容：

   ```shell
   NAME      READY     STATUS    RESTARTS   AGE
   demo      1/1       Running   0          4s
   ```

6. 检查您是否获得了 ping 进程所期望的日志：

   ```console
   $ kubectl logs demo
   ```

   您应该会看到一个健康的 ping 进程的输出：

   ```shell
   PING 8.8.8.8 (8.8.8.8): 56 data bytes
   64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
   64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
   64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
   ...
   ```

7. 最后，拆除您的测试 pod：

   ```console
   $ kubectl delete -f pod.yaml
   ```

{{< /tab >}}
{{< /tabs >}}

## 启用 Docker Swarm

Docker Desktop 主要在 Docker Engine 上运行，其中包含运行 Swarm 所需的一切。请按照适用于您的操作系统的设置和验证说明进行操作：

{{< tabs group="os" >}}
{{< tab name="Mac" >}}

### Mac

1. 打��终端，并初始化 Docker Swarm 模式：

   ```console
   $ docker swarm init
   ```

   如果一切顺利，您应该会看到类似以下的消息：

   ```shell
   Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.

   To add a worker to this swarm, run the following command:

       docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377

   To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
   ```

2. 运行一个简单的 Docker 服务，该服务使用基于 alpine 的文件系统，并隔离一个对 8.8.8.8 的 ping：

   ```console
   $ docker service create --name demo alpine:latest ping 8.8.8.8
   ```

3. 检查您的服务是否创建了一个正在运行的容器：

   ```console
   $ docker service ps demo
   ```

   您应该会看到类似以下的内容：

   ```shell
   ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
   463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
   ```

4. 检查您是否获得了 ping 进程所期望的日志：

   ```console
   $ docker service logs demo
   ```

   您应该会看到一个健康的 ping 进程的输出：

   ```shell
   demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
   ...
   ```

5. 最后，拆除您的测试服务：

   ```console
   $ docker service rm demo
   ```

{{< /tab >}}
{{< tab name="Windows" >}}

### Windows

1. 打开 PowerShell，并初始化 Docker Swarm 模式：

   ```console
   $ docker swarm init
   ```

   如果一切顺利，您应该会看到类似以下的消息：

   ```shell
   Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.

   To add a worker to this swarm, run the following command:

       docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377

   To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
   ```

2. 运行一个简单的 Docker 服务，该服务使用基于 alpine 的文件系统，并隔离一个对 8.8.8.8 的 ping：

   ```console
   $ docker service create --name demo alpine:latest ping 8.8.8.8
   ```

3. 检查您的服务是否创建了一个正在运行的容器：

   ```console
   $ docker service ps demo
   ```

   您应该会看到类似以下的内容：

   ```shell
   ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
   463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
   ```

4. 检查您是否获得了 ping 进程所期望的日志：

   ```console
   $ docker service logs demo
   ```

   您应该会看到一个健康的 ping 进程的输出：

   ```shell
   demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
   ...
   ```

5. 最后，拆除您的测试服务：

   ```console
   $ docker service rm demo
   ```

{{< /tab >}}
{{< /tabs >}}

## 结论

此时，您已确认可以在 Kubernetes 和 Swarm 中运行简单的容器化工作负载。下一步是编写一个 YAML 文件，描述如何运行和管理这些容器。

- [部署到 Kubernetes](kube-deploy.md)
- [部署到 Swarm](swarm-deploy.md)

## CLI 参考

本文中使用的所有 CLI 命令的进一步文档可在此处获得：

- [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
- [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)
- [`kubectl logs`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- [`kubectl delete`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)
- [`docker swarm init`](/reference/cli/docker/swarm/init/)
- [`docker service *`](/reference/cli/docker/service/)
