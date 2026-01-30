---
title: Swarm 任务状态
description: 了解在 Swarm 上调度的任务及其状态。
keywords: swarm, task, service, 任务, 状态
---

Docker 允许您创建可以启动任务的服务。服务是对期望状态的描述，而任务负责执行工作。工作按以下顺序在 Swarm 节点上进行调度：

1.  使用 `docker service create` 创建一个服务。
2.  请求发送到 Docker 管理节点 (manager node)。
3.  Docker 管理节点将服务调度到特定节点上运行。
4.  每个服务可以启动多个任务。
5.  每个任务都有一个生命周期，具有 `NEW`、`PENDING` 和 `COMPLETE` 等状态。

任务是执行单元，运行一次直至完成。当任务停止时，它不会再次执行，但可能会有一个新任务取代它的位置。

任务会经历多个状态，直到完成或失败。任务初始化时处于 `NEW` 状态。任务单向地向前推进这些状态，状态不会倒退。例如，一个任务永远不会从 `COMPLETE` 回到 `RUNNING`。

任务按以下顺序经历各状态：

| 任务状态    | 描述                                                                                                 |
| ----------- | ----------------------------------------------------------------------------------------------------------- |
| `NEW`       | 任务已初始化。                                                                                   |
| `PENDING`   | 已为任务分配资源。                                                                      |
| `ASSIGNED`  | Docker 已将任务分配给节点。                                                                          |
| `ACCEPTED`  | 任务已被工作节点接受。如果工作节点拒绝该任务，状态将变为 `REJECTED`。 |
| `READY`     | 工作节点已准备好启动任务。                                                                  |
| `PREPARING` | Docker 正在准备任务。                                                                               |
| `STARTING`  | Docker 正在启动任务。                                                                                |
| `RUNNING`   | 任务正在执行。                                                                                      |
| `COMPLETE`  | 任务退出且无错误代码。                                                                      |
| `FAILED`    | 任务退出且带有错误代码。                                                                         |
| `SHUTDOWN`  | Docker 请求任务关闭。                                                                     |
| `REJECTED`  | 工作节点拒绝了任务。                                                                          |
| `ORPHANED`  | 节点宕机时间过长。                                                                             |
| `REMOVE`    | 任务并非处于终止状态，但相关服务已被移除或规模缩减。                             |

## 查看任务状态

运行 `docker service ps <service-name>` 获取任务的状态。`CURRENT STATE` 字段显示任务的状态及其持续时间。

```console
$ docker service ps webserver
ID             NAME              IMAGE    NODE        DESIRED STATE  CURRENT STATE            ERROR                              PORTS
owsz0yp6z375   webserver.1       nginx    UbuntuVM    Running        Running 44 seconds ago
j91iahr8s74p    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 50 seconds ago    "No such container: webserver.…"
7dyaszg13mw2    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 5 hours ago       "No such container: webserver.…"
```

## 下一步

- [了解 Swarm 任务模型](https://github.com/docker/swarmkit/blob/master/design/task_model.md)
