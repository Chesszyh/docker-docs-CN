---
title: 测试你的 Ruby on Rails 部署
linkTitle: 测试你的部署
weight: 50
keywords: deploy, kubernetes, ruby
description: 了解如何使用 Kubernetes 进行本地开发
aliases:
  - /language/ruby/deploy/
  - /guides/language/ruby/deploy/
---

## 先决条件

- 完成本指南的所有前几节，从 [容器化 Ruby on Rails 应用程序](containerize.md) 开始。
- 在 Docker Desktop 中 [启用 Kubernetes](/manuals/desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将你的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。这允许你在部署之前在本地 Kubernetes 上测试和调试你的工作负载。

## 创建 Kubernetes YAML 文件

在你的 `docker-ruby-on-rails` 目录中，创建一个名为 `docker-ruby-on-rails-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和你在 [为你的 Ruby on Rails 应用程序配置 CI/CD](configure-github-actions.md) 中创建的存储库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-ruby-on-rails-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: ruby-on-rails
  template:
    metadata:
      labels:
        service: ruby-on-rails
    spec:
      containers:
        - name: ruby-on-rails-container
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: docker-ruby-on-rails-demo
  namespace: default
spec:
  type: NodePort
  selector:
    service: ruby-on-rails
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，用 `---` 分隔：

- 一个 Deployment，描述了一组可扩展的相同 Pod。在这种情况下，你只会得到一个副本，或你的 Pod 的副本。该 Pod（在 `template` 下描述）中只有一个容器。该容器是根据 GitHub Actions 在 [为你的 Ruby on Rails 应用程序配置 CI/CD](configure-github-actions.md) 中构建的镜像创建的。
- 一个 NodePort 服务，它将流量从主机上的端口 30001 路由到它路由到的 Pod 内的端口 8001，允许你从网络访问你的应用程序。

要了解有关 Kubernetes 对象的更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用程序

1. 在终端中，导航到 `docker-ruby-on-rails` 并将你的应用程序部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-ruby-on-rails-kubernetes.yaml
   ```

   你应该看到类似以下的输出，表明你的 Kubernetes 对象已成功创建。

   ```shell
   deployment.apps/docker-ruby-on-rails-demo created
   service/docker-ruby-on-rails-demo created
   ```

2. 通过列出你的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   你的部署应列出如下：

   ```shell
   NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
   docker-ruby-on-rails-demo  1/1     1            1           15s
   ```

   这表明你在 YAML 中请求的所有 Pod 都已启动并运行。对你的服务进行同样的检查。

   ```console
   $ kubectl get services
   ```

   你应该会得到类似以下的输出。

   ```shell
   NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
   kubernetes                  ClusterIP   10.96.0.1       <none>        443/TCP          23h
   docker-ruby-on-rails-demo   NodePort    10.99.128.230   <none>        3000:30001/TCP   75s
   ```

   除了默认的 `kubernetes` 服务外，你还可以看到你的 `docker-ruby-on-rails-demo` 服务，在端口 30001/TCP 上接受流量。

3. 要在 Kubernetes 上运行的 Ruby on Rails 应用程序中创建并迁移数据库，你需要遵循以下步骤。

   **获取当前的 Pod**：
   首先，你需要识别在 Kubernetes 集群中运行的 Pod。执行以下命令以列出 `default` 命名空间中的当前 Pod：

   ```sh
   # Get the current pods in the cluster in the namespace default
   $ kubectl get pods
   ```

   此命令将显示 `default` 命名空间中所有 Pod 的列表。查找前缀为 `docker-ruby-on-rails-demo-` 的 Pod。这是一个示例输出：

   ```console
   NAME                                         READY   STATUS    RESTARTS      AGE
   docker-ruby-on-rails-demo-7cbddb5d6f-qh44l   1/1     Running   2 (22h ago)   9d
   ```

   **执行迁移命令**：
   一旦你识别了正确的 Pod，使用 `kubectl exec` 命令在 Pod 内运行数据库迁移。

   ```sh
   $ kubectl exec -it docker-ruby-on-rails-demo-7cbddb5d6f-qh44l -- rails db:migrate RAILS_ENV=development
   ```

   此命令在指定的 Pod 中打开交互式终端会话 (`-it`) 并运行 `rails db:migrate` 命令，环境设置为 development (`RAILS_ENV=development`)。

   通过遵循这些步骤，你确保你的数据库在 Kubernetes 集群中运行的 Ruby on Rails 应用程序内正确迁移。此过程有助于在部署和更新期间维护应用程序数据结构的完整性和一致性。

4. 打开浏览器并转到 [http://localhost:30001](http://localhost:30001)，你应该看到 Ruby on Rails 应用程序正在运行。

5. 运行以下命令来拆除你的应用程序。

   ```console
   $ kubectl delete -f docker-ruby-on-rails-kubernetes.yaml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将你的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)
