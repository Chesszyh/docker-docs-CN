--driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem,servername=<TLS服务器名称>
      tcp://localhost:1234

    或者，使用 `docker-container://` URL 方案连接到该 BuildKit 容器，无需指定端口：

    ```console
    $ docker buildx create \
      --name remote-container \
      --driver remote \
      docker-container://remote-container
    ```

## 示例：在 Kubernetes 中运行远程 BuildKit

本指南展示了如何通过手动创建一个 BuildKit `Deployment` 来实现类似于 `kubernetes` 驱动的设置。虽然 `kubernetes` 驱动在底层会自动执行此操作，但有时您可能希望手动扩展 BuildKit。此外，在从 Kubernetes pod 内部执行构建时，Buildx 构建器需要在每个 pod 内部重新创建或在 pod 之间进行复制。

1. 按照 [此处的说明](https://github.com/moby/buildkit/tree/master/examples/kubernetes) 创建一个 `buildkitd` 的 Kubernetes deployment。

   按照指南，使用 [create-certs.sh](https://github.com/moby/buildkit/blob/master/examples/kubernetes/create-certs.sh) 为 BuildKit 守护进程和客户端创建证书，并创建一个 BuildKit pod 的 deployment 以及连接它们的 service。

2. 假设该 service 名为 `buildkitd`，在 Buildx 中创建一个远程构建器，并确保列出的证书文件存在：

   ```console
   $ docker buildx create \
     --name remote-kubernetes \
     --driver remote \
     --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem \
     tcp://buildkitd.default.svc:1234
   ```

请注意，这仅在集群内部有效，因为 BuildKit 设置指南仅创建了一个 `ClusterIP` 类型的 service。要远程访问构建器，您需要设置并使用 Ingress，这超出了本指南的范围。

### 调试 Kubernetes 中的远程构建器

如果您在访问部署在 Kubernetes 中的远程构建器时遇到问题，可以使用 `kube-pod://` URL 方案通过 Kubernetes API 直接连接到某个 BuildKit pod。请注意，此方法仅连接到 deployment 中的单个 pod。

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

然后，您可以将远程驱动指向 `tcp://localhost:1234`。

```