---
title: 地草你的 Go 部署
linkTitle: 地草你的部署
weight: 50
keywords: deploy, go, local, development
description: 了解如何部署你的 Go 应用
aliases:
  - /language/golang/deploy/
  - /guides/language/golang/deploy/
---

## 先行条件

- 完成本指南的所有前面部分，从 [ 构建 Go 镜像 ](build-images.md) 开始。
- 在 Docker Desktop 中 [ 开启 Kubernetes](/manuals/desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

## 概览

在本节中，你将学习如何使用 Docker Desktop 将应用程部署到开发机器上功能完备的 Kubernetes 环境中。这允许你在部署之前在本地 Kubernetes 上测试和调调工作载。

## 创建 Kubernetes YAML 文件

在你的项目目录中，创建一个名为 `docker-go-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和你在 [ 为你的 Go 应用配置 CI/CD ](configure-ci-cd.md) 中创建的存储库名称。

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
        - env:
            - name: PGDATABASE
              value: mydb
            - name: PGPASSWORD
              value: whatever
            - name: PGHOST
              value: db
            - name: PGPORT
              value: "5432"
            - name: PGUSER
              value: postgres
          image: DOCKER_USERNAME/REPO_NAME
          name: server
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              hostPort: 8080
              protocol: TCP
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
              value: mydb
            - name: POSTGRES_PASSWORD
              value: whatever
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
    - name: "8080"
      port: 8080
      targetPort: 8080
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

在这个 Kubernetes YAML 文件中，有四个对象，由 `---` 分隔。除了用于数据库的服务和部署之外，另外两个对象是：

- 一个 Deployment（部署），描述一组可扩展的相同 Pod。在这种情况下，你将只获得一个复制，或者你的 Pod 的复制。该 Pod（在 `template` 下方描述）中只有一个容器。该容器是根据 GitHub Actions 在 [ 为你的 Go 应用配置 CI/CD ](configure-ci-cd.md) 中构建的镜像创建的。
- 一个 NodePort 服务，它将流量从主机上的端口 30001 路由到其路由到的 Pod 内部的 8080 端口，从而允许你从网络访问你的应用。

要了解关于 Kubernetes 对象的更多信息，请参遷 [ Kubernetes 文档 ](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用

1. 在终端中，逸航到项目目录并将应用部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-go-kubernetes.yaml
   ```

   你应该会看到相似以下内容的输出，表明你的 Kubernetes 对象已成功创建。

   ```shell
   deployment.apps/db created
   service/db created
   deployment.apps/server created
   service/server created
   ```

2. 通过列出你的部署来确保证一切正常。

   ```console
   $ kubectl get deployments
   ```

   你的部署应列出如下所示：

   ```shell
   NAME     READY   UP-TO-DATE   AVAILABLE   AGE
   db       1/1     1            1           76s
   server   1/1     1            1           76s
   ```

   这表明所有的 Pod 都已启动并在运行中。对你的服务进行假的检查。

   ```console
   $ kubectl get services
   ```

   你应该得到相似以下的输出。

   ```shell
   NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
   db           ClusterIP   10.96.156.90    <none>        5432/TCP         2m8s
   kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          164m
   server       NodePort    10.102.94.225   <none>        8080:30001/TCP   2m8s
   ```

   除了默认的 `kubernetes` 服务外，你还可以看到你的 `server` 服务和 `db` 服务。`server` 服务正在接受端口 30001/TCP 上的流量。

3. 打开终端并 curl 你的应用以验证它正在运行。

   ```console
   $ curl --request POST \
     --url http://localhost:30001/send \
     --header 'content-type: application/json' \
     --data '{"value": "Hello, Oliver!"}'
   ```

   你应该收到以下消息。

   ```json
   { "value": "Hello, Oliver!" }
   ```

4. 运行以下命令以移除你的应用。

   ```console
   $ kubectl delete -f docker-go-kubernetes.yaml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将应用程部署到开发机器上功能完备的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [ 使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)
- [ Swarm 模式概览](/manuals/engine/swarm/_index.md)
