---
title: 测试你的 Node.js 部署
linkTitle: 测试你的部署
weight: 50
keywords: deploy, kubernetes, node, node.js
description: 学习如何本地部署以测试和调试你的 Kubernetes 部署
aliases:
  - /language/nodejs/deploy/
  - /guides/language/nodejs/deploy/
---

## 前提条件

- 完成本指南之前的所有章节，从[容器化 Node.js 应用程序](containerize.md)开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将应用程序部署到开发机器上功能完备的 Kubernetes 环境中。这允许你在部署之前在本地测试和调试 Kubernetes 上的工作负载。

## 创建 Kubernetes YAML 文件

在克隆的仓库目录中，创建一个名为 `docker-node-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和在[为 Node.js 应用程序配置 CI/CD](configure-ci-cd.md)中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-nodejs-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      todo: web
  template:
    metadata:
      labels:
        todo: web
    spec:
      containers:
        - name: todo-site
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: todo-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    todo: web
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

- 一个 Deployment（部署），描述一组可扩展的相同 Pod。在这种情况下，你只会得到一个副本，即你的 Pod 的一个副本。该 Pod 在 `template` 下描述，其中只有一个容器。该容器是根据在[为 Node.js 应用程序配置 CI/CD](configure-ci-cd.md)中由 GitHub Actions 构建的镜像创建的。
- 一个 NodePort 服务，它将流量从主机的 30001 端口路由到它所路由的 Pod 内部的 3000 端口，允许你从网络访问你的应用程序。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用程序

1. 在终端中，导航到你创建 `docker-node-kubernetes.yaml` 的位置，并将应用程序部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-node-kubernetes.yaml
   ```

   你应该会看到类似以下的输出，表明你的 Kubernetes 对象已成功创建。

   ```shell
   deployment.apps/docker-nodejs-demo created
   service/todo-entrypoint created
   ```

2. 通过列出你的部署来确保一切正常工作。

   ```console
   $ kubectl get deployments
   ```

   你的部署应该如下所示：

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   docker-nodejs-demo   1/1     1            1           6s
   ```

   这表明你在 YAML 中请求的所有 Pod 都已启动并运行。对你的服务执行相同的检查。

   ```console
   $ kubectl get services
   ```

   你应该会得到类似以下的输出。

   ```shell
   NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          7d22h
   todo-entrypoint   NodePort    10.111.101.229   <none>        3000:30001/TCP   33s
   ```

   除了默认的 `kubernetes` 服务外，你还可以看到你的 `todo-entrypoint` 服务，它在 30001/TCP 端口接受流量。

3. 打开浏览器，访问 `localhost:30001` 查看你的应用程序。你应该会看到你的应用程序。

4. 运行以下命令删除你的应用程序。

   ```console
   $ kubectl delete -f docker-node-kubernetes.yaml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将应用程序部署到开发机器上功能完备的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)
