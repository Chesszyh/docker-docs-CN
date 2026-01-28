---
title: 测试你的 Rust 部署
linkTitle: 测试你的部署
weight: 50
keywords: deploy, kubernetes, rust
description: 了解如何使用 Kubernetes 在本地测试你的 Rust 部署
aliases:
  - /language/rust/deploy/
  - /guides/language/rust/deploy/
---

## 先决条件

- 完成本指南的前几节，从 [开发你的 Rust 应用程序](develop.md) 开始。
- 在 Docker Desktop 中 [开启 Kubernetes](/manuals/desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将你的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。这允许你在部署之前在本地 Kubernetes 上测试和调试你的工作负载。

## 创建 Kubernetes YAML 文件

在你的 `docker-rust-postgres` 目录中，创建一个名为 `docker-rust-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和你在 [为你的 Rust 应用程序配置 CI/CD](configure-ci-cd.md) 中创建的存储库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: server
  strategy: {}
  template:
    metadata:
      labels:
        service: server
    spec:
      initContainers:
        - name: wait-for-db
          image: busybox:1.28
          command:
            [
              "sh",
              "-c",
              'until nc -zv db 5432; do echo "waiting for db"; sleep 2; done;',
            ]
      containers:
        - image: DOCKER_USERNAME/REPO_NAME
          name: server
          imagePullPolicy: Always
          ports:
            - containerPort: 8000
              hostPort: 5000
              protocol: TCP
          env:
            - name: ADDRESS
              value: 0.0.0.0:8000
            - name: PG_DBNAME
              value: example
            - name: PG_HOST
              value: db
            - name: PG_PASSWORD
              value: mysecretpassword
            - name: PG_USER
              value: postgres
            - name: RUST_LOG
              value: debug
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: db
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        service: db
    spec:
      containers:
        - env:
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_PASSWORD
              value: mysecretpassword
            - name: POSTGRES_USER
              value: postgres
          image: postgres
          name: db
          ports:
            - containerPort: 5432
              protocol: TCP
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  type: NodePort
  ports:
    - name: "5000"
      port: 5000
      targetPort: 8000
      nodePort: 30001
  selector:
    service: server
status:
  loadBalancer: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  ports:
    - name: "5432"
      port: 5432
      targetPort: 5432
  selector:
    service: db
status:
  loadBalancer: {}
```

在这个 Kubernetes YAML 文件中，有四个对象，用 `---` 分隔。除了数据库的 Service 和 Deployment 之外，另外两个对象是：

- 一个 Deployment，描述了一组可扩展的相同 Pod。在这种情况下，你只会得到一个副本，或你的 Pod 的副本。该 Pod（在 `template` 下描述）中只有一个容器。该容器是根据 GitHub Actions 在 [为你的 Rust 应用程序配置 CI/CD](configure-ci-cd.md) 中构建的镜像创建的。
- 一个 NodePort 服务，它将流量从主机上的端口 30001 路由到它路由到的 Pod 内的端口 5000，允许你从网络访问你的应用程序。

要了解有关 Kubernetes 对象的更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用程序

1. 在终端中，导航到 `docker-rust-postgres` 并将你的应用程序部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-rust-kubernetes.yaml
   ```

   你应该看到类似以下的输出，表明你的 Kubernetes 对象已成功创建。

   ```shell
   deployment.apps/server created
   deployment.apps/db created
   service/server created
   service/db created
   ```

2. 通过列出你的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   你的部署应列出如下：

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   db       1/1     1            1           2m21s
   server   1/1     1            1           2m21s
   ```

   这表明你在 YAML 中请求的所有 Pod 都已启动并运行。对你的服务进行同样的检查。

   ```console
   $ kubectl get services
   ```

   你应该会得到类似以下的输出。

   ```shell
   NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   db           ClusterIP   10.105.167.81    <none>        5432/TCP         109s
   kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          9d
   server       NodePort    10.101.235.213   <none>        5000:30001/TCP   109s
   ```

   除了默认的 `kubernetes` 服务外，你还可以看到你的 `service-entrypoint` 服务，在端口 30001/TCP 上接受流量。

3. 在终端中，curl 该服务。

   ```console
   $ curl http://localhost:30001/users
   [{"id":1,"login":"root"}]
   ```

4. 运行以下命令来拆除你的应用程序。

   ```console
   $ kubectl delete -f docker-rust-kubernetes.yaml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将你的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)
