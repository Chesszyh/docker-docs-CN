---
title: 测试您的 Python 部署
linkTitle: 测试您的部署
weight: 50
keywords: deploy, kubernetes, python
description: 学习如何使用 Kubernetes 进行本地开发
aliases:
  - /language/python/deploy/
  - /guides/language/python/deploy/
---

## 前提条件

- 完成本指南之前的所有章节，从[使用容器进行 Python 开发](develop.md)开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

## 概述

在本节中，您将学习如何使用 Docker Desktop 将应用程序部署到开发机器上的完整 Kubernetes 环境。这使您可以在部署之前在本地测试和调试 Kubernetes 上的工作负载。

## 创建 Kubernetes YAML 文件

在您的 `python-docker-dev-example` 目录中，创建一个名为 `docker-postgres-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，添加以下内容。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: POSTGRES_PASSWORD
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-data
          persistentVolumeClaim:
            claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: default
spec:
  ports:
    - port: 5432
  selector:
    app: postgres
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: default
type: Opaque
data:
  POSTGRES_PASSWORD: cG9zdGdyZXNfcGFzc3dvcmQ= # Base64 编码的密码（例如 'postgres_password'）
```

在您的 `python-docker-dev-example` 目录中，创建一个名为 `docker-python-kubernetes.yaml` 的文件。将 `DOCKER_USERNAME/REPO_NAME` 替换为您的 Docker 用户名和在[为您的 Python 应用程序配置 CI/CD](./configure-github-actions.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-python-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: fastapi
  template:
    metadata:
      labels:
        service: fastapi
    spec:
      containers:
        - name: fastapi-service
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: POSTGRES_PASSWORD
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_SERVER
              value: postgres
            - name: POSTGRES_PORT
              value: "5432"
          ports:
            - containerPort: 8001
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    service: fastapi
  ports:
    - port: 8001
      targetPort: 8001
      nodePort: 30001
```

在这些 Kubernetes YAML 文件中，有多个对象，通过 `---` 分隔：

- Deployment（部署）：描述一组可扩展的相同 Pod。在本例中，您将只获得一个副本，即一个 Pod 的副本。该 Pod 在 `template` 下描述，其中只有一个容器。该容器由 GitHub Actions 在[为您的 Python 应用程序配置 CI/CD](configure-github-actions.md) 中构建的镜像创建。
- Service（服务）：定义容器中端口的映射方式。
- PersistentVolumeClaim（持久卷声明）：定义在重启后持久化的数据库存储。
- Secret（密钥）：使用 Kubernetes Secret 资源存储数据库密码作为示例。
- NodePort 服务：将流量从主机的 30001 端口路由到其路由的 Pod 内部的 8001 端口，使您可以从网络访问应用程序。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

> [!NOTE]
>
> - `NodePort` 服务适用于开发/测试目的。对于生产环境，您应该实现 [ingress-controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)。

## 部署并检查您的应用程序

1. 在终端中，导航到 `python-docker-dev-example` 并将数据库部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-postgres-kubernetes.yaml
   ```

   您应该看到类似以下的输出，表明您的 Kubernetes 对象创建成功。

   ```console
   deployment.apps/postgres created
   service/postgres created
   persistentvolumeclaim/postgres-pvc created
   secret/postgres-secret created
   ```

   现在，部署您的 Python 应用程序。

   ```console
   kubectl apply -f docker-python-kubernetes.yaml
   ```

   您应该看到类似以下的输出，表明您的 Kubernetes 对象创建成功。

   ```console
   deployment.apps/docker-python-demo created
   service/service-entrypoint created
   ```

2. 通过列出您的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   您的部署应该列出如下：

   ```console
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   docker-python-demo   1/1     1            1           48s
   postgres             1/1     1            1           2m39s
   ```

   这表明您在 YAML 中请求的所有 Pod 都已启动并运行。对服务进行相同的检查。

   ```console
   $ kubectl get services
   ```

   您应该得到类似以下的输出。

   ```console
   NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.43.0.1      <none>        443/TCP          13h
   postgres             ClusterIP   10.43.209.25   <none>        5432/TCP         3m10s
   service-entrypoint   NodePort    10.43.67.120   <none>        8001:30001/TCP   79s
   ```

   除了默认的 `kubernetes` 服务外，您可以看到您的 `service-entrypoint` 服务在 30001/TCP 端口接受流量，以及内部的 `ClusterIP` `postgres` 开放 `5432` 端口以接受来自 Python 应用的连接。

3. 在终端中，curl 该服务。请注意，本示例中没有部署数据库。

   ```console
   $ curl http://localhost:30001/
   Hello, Docker!!!
   ```

4. 运行以下命令来删除您的应用程序。

   ```console
   $ kubectl delete -f docker-python-kubernetes.yaml
   $ kubectl delete -f docker-postgres-kubernetes.yaml
   ```

## 总结

在本节中，您学习了如何使用 Docker Desktop 将应用程序部署到开发机器上的完整 Kubernetes 环境。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)
