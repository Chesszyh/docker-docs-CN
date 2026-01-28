---
description: Inspect the application
keywords: tutorial, cluster management, swarm mode, get started
title: 检查 swarm 上的服务
weight: 40
notoc: true
---

当你已经[部署了服务](deploy-service.md)到 swarm 后，你可以使用 Docker CLI 查看在 swarm 中运行的服务的详细信息。

1.  如果你还没有，打开终端并 ssh 到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行 `docker service inspect --pretty <SERVICE-ID>` 以易于阅读的格式显示服务的详细信息。

    要查看 `helloworld` 服务的详细信息：

    ```console
    [manager1]$ docker service inspect --pretty helloworld

    ID:		9uk4639qpg7npwf3fn2aasksr
    Name:		helloworld
    Service Mode:	REPLICATED
     Replicas:		1
    Placement:
    UpdateConfig:
     Parallelism:	1
    ContainerSpec:
     Image:		alpine
     Args:	ping docker.com
    Resources:
    Endpoint Mode:  vip
    ```

    > [!TIP]
    >
    > 要以 json 格式返回服务详细信息，请运行不带 `--pretty` 标志的相同命令。

    ```console
    [manager1]$ docker service inspect helloworld
    [
    {
        "ID": "9uk4639qpg7npwf3fn2aasksr",
        "Version": {
            "Index": 418
        },
        "CreatedAt": "2016-06-16T21:57:11.622222327Z",
        "UpdatedAt": "2016-06-16T21:57:11.622222327Z",
        "Spec": {
            "Name": "helloworld",
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": "alpine",
                    "Args": [
                        "ping",
                        "docker.com"
                    ]
                },
                "Resources": {
                    "Limits": {},
                    "Reservations": {}
                },
                "RestartPolicy": {
                    "Condition": "any",
                    "MaxAttempts": 0
                },
                "Placement": {}
            },
            "Mode": {
                "Replicated": {
                    "Replicas": 1
                }
            },
            "UpdateConfig": {
                "Parallelism": 1
            },
            "EndpointSpec": {
                "Mode": "vip"
            }
        },
        "Endpoint": {
            "Spec": {}
        }
    }
    ]
    ```

3.  运行 `docker service ps <SERVICE-ID>` 查看哪些节点正在运行该服务：

    ```console
    [manager1]$ docker service ps helloworld

    NAME                                    IMAGE   NODE     DESIRED STATE  CURRENT STATE           ERROR               PORTS
    helloworld.1.8p1vev3fq5zm0mi8g0as41w35  alpine  worker2  Running        Running 3 minutes
    ```

    在本例中，`helloworld` 服务的一个实例正在 `worker2` 节点上运行。你可能会看到服务在你的管理节点上运行。默认情况下，swarm 中的管理节点可以像工作节点一样执行任务。

    Swarm 还会显示服务任务的 `DESIRED STATE` 和 `CURRENT STATE`，以便你可以查看任务是否按照服务定义运行。

4.  在任务运行的节点上运行 `docker ps` 以查看任务容器的详细信息。

    > [!TIP]
    >
    > 如果 `helloworld` 在你的管理节点以外的节点上运行，你必须 ssh 到那个节点。

    ```console
    [worker2]$ docker ps

    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    e609dde94e47        alpine:latest       "ping docker.com"   3 minutes ago       Up 3 minutes                            helloworld.1.8p1vev3fq5zm0mi8g0as41w35
    ```

## 下一步

接下来，你将更改在 swarm 中运行的服务的规模。

{{< button text="更改规模" url="scale-service.md" >}}
