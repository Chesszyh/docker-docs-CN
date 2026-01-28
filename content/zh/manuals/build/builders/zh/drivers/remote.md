---
title: Remote 驱动
description: |
  Remote 驱动允许您连接到您手动设置和配置的远程 BuildKit 实例。
keywords: build, buildx, driver, builder, remote
aliases:
  - /build/buildx/drivers/remote/
  - /build/building/drivers/remote/
  - /build/drivers/remote/
---

Buildx remote 驱动允许处理更复杂的自定义构建工作负载，使您能够连接到外部管理的 BuildKit 实例。这对于需要手动管理 BuildKit 守护进程的场景，或者 BuildKit 守护进程从其他来源暴露的场景非常有用。

## 概要

```console
$ docker buildx create \
  --name remote \
  --driver remote \
  tcp://localhost:1234
```

下表描述了可以传递给 `--driver-opt` 的特定于驱动的可用选项：

| 参数           | 类型    | 默认值           | 描述                                                           |
| -------------- | ------- | ---------------- | -------------------------------------------------------------- |
| `key`          | String  |                  | 设置 TLS 客户端密钥。                                          |
| `cert`         | String  |                  | 要呈现给 `buildkitd` 的 TLS 客户端证书的绝对路径。             |
| `cacert`       | String  |                  | 用于验证的 TLS 证书颁发机构的绝对路径。                        |
| `servername`   | String  | 端点主机名       | 请求中使用的 TLS 服务器名称。                                  |
| `default-load` | Boolean | `false`          | 自动将镜像加载到 Docker Engine 镜像存储。                      |

## 示例：通过 Unix 套接字连接远程 BuildKit

本指南向您展示如何创建一个设置，其中 BuildKit 守护进程监听 Unix 套接字，并让 Buildx 通过它连接。

1. 确保已安装 [BuildKit](https://github.com/moby/buildkit)。

   例如，您可以使用以下命令启动 buildkitd 实例：

   ```console
   $ sudo ./buildkitd --group $(id -gn) --addr unix://$HOME/buildkitd.sock
   ```

   或者，[参见此处](https://github.com/moby/buildkit/blob/master/docs/rootless.md)了解以无根模式运行 buildkitd，或[参见此处](https://github.com/moby/buildkit/tree/master/examples/systemd)了解将其作为 systemd 服务运行的示例。

2. 检查您是否有一个可以连接的 Unix 套接字。

   ```console
   $ ls -lh /home/user/buildkitd.sock
   srw-rw---- 1 root user 0 May  5 11:04 /home/user/buildkitd.sock
   ```

3. 使用 remote 驱动将 Buildx 连接到它：

   ```console
   $ docker buildx create \
     --name remote-unix \
     --driver remote \
     unix://$HOME/buildkitd.sock
   ```

4. 使用 `docker buildx ls` 列出可用的构建器。然后您应该会在其中看到 `remote-unix`：

   ```console
   $ docker buildx ls
   NAME/NODE           DRIVER/ENDPOINT                        STATUS  PLATFORMS
   remote-unix         remote
     remote-unix0      unix:///home/.../buildkitd.sock        running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
   default *           docker
     default           default                                running linux/amd64, linux/386
   ```

您可以使用 `docker buildx use remote-unix` 切换到这个新构建器作为默认构建器，或者使用 `--builder` 按每次构建指定：

```console
$ docker buildx build --builder=remote-unix -t test --load .
```

请记住，如果您想将构建结果加载到 Docker 守护进程中，需要使用 `--load` 标志。

## 示例：Docker 容器中的远程 BuildKit

本指南将向您展示如何创建类似于 `docker-container` 驱动的设置，通过手动启动一个 BuildKit Docker 容器并使用 Buildx remote 驱动连接到它。此过程将手动创建一个容器并通过其暴露的端口访问它。（您可能最好直接使用通过 Docker 守护进程连接到 BuildKit 的 `docker-container` 驱动，但这是为了说明目的。）

1.  为 BuildKit 生成证书。

    您可以使用这个 [bake 定义](https://github.com/moby/buildkit/blob/master/examples/create-certs)作为起点：

    ```console
    SAN="localhost 127.0.0.1" docker buildx bake "https://github.com/moby/buildkit.git#master:examples/create-certs"
    ```

    请注意，虽然可以在不使用 TLS 的情况下通过 TCP 暴露 BuildKit，但不建议这样做。这样做会允许在没有凭据的情况下任意访问 BuildKit。

2.  在 `.certs/` 中生成证书后，启动容器：

    ```console
    $ docker run -d --rm \
      --name=remote-buildkitd \
      --privileged \
      -p 1234:1234 \
      -v $PWD/.certs:/etc/buildkit/certs \
      moby/buildkit:latest \
      --addr tcp://0.0.0.0:1234 \
      --tlscacert /etc/buildkit/certs/daemon/ca.pem \
      --tlscert /etc/buildkit/certs/daemon/cert.pem \
      --tlskey /etc/buildkit/certs/daemon/key.pem
    ```

    此命令启动一个 BuildKit 容器，并将守护进程的端口 1234 暴露到 localhost。

3.  使用 Buildx 连接到这个正在运行的容器：

    ```console
    $ docker buildx create \
      --name remote-container \
      --driver remote \
      --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem,servername=<TLS_SERVER_NAME> \
      tcp://localhost:1234
    ```

    或者，使用 `docker-container://` URL 方案连接到 BuildKit 容器，而无需指定端口：

    ```console
    $ docker buildx create \
      --name remote-container \
      --driver remote \
      docker-container://remote-container
    ```

## 示例：Kubernetes 中的远程 BuildKit

本指南将向您展示如何通过手动创建 BuildKit `Deployment` 来创建类似于 `kubernetes` 驱动的设置。虽然 `kubernetes` 驱动会在后台执行此操作，但有时可能需要手动扩展 BuildKit。此外，当从 Kubernetes pod 内部执行构建时，需要在每个 pod 内重新创建 Buildx 构建器或在它们之间复制。

1. 按照[此处](https://github.com/moby/buildkit/tree/master/examples/kubernetes)的说明创建 `buildkitd` 的 Kubernetes deployment。

   按照指南，使用 [create-certs.sh](https://github.com/moby/buildkit/blob/master/examples/kubernetes/create-certs.sh) 为 BuildKit 守护进程和客户端创建证书，并创建一个 BuildKit pod 的 deployment 以及一个连接到它们的 service。

2. 假设该 service 名为 `buildkitd`，在 Buildx 中创建一个 remote 构建器，确保列出的证书文件存在：

   ```console
   $ docker buildx create \
     --name remote-kubernetes \
     --driver remote \
     --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem \
     tcp://buildkitd.default.svc:1234
   ```

请注意，这仅在集群内部工作，因为 BuildKit 设置指南仅创建了一个 `ClusterIP` service。要远程访问构建器，您可以设置并使用 ingress，这超出了本指南的范围。

### 在 Kubernetes 中调试远程构建器

如果您在访问部署在 Kubernetes 中的远程构建器时遇到问题，可以使用 `kube-pod://` URL 方案通过 Kubernetes API 直接连接到 BuildKit pod。请注意，此方法仅连接到 deployment 中的单个 pod。

```console
$ kubectl get pods --selector=app=buildkitd -o json | jq -r '.items[].metadata.name'
buildkitd-XXXXXXXXXX-xxxxx
$ docker buildx create \
  --name remote-container \
  --driver remote \
  kube-pod://buildkitd-XXXXXXXXXX-xxxxx
```

或者，使用 `kubectl` 的端口转发机制：

```console
$ kubectl port-forward svc/buildkitd 1234:1234
```

然后您可以将 remote 驱动指向 `tcp://localhost:1234`。
