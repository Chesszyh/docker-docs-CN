---
title: 从扩展与 Kubernetes 交互
linkTitle: 与 Kubernetes 交互
description: 如何从扩展连接到 Kubernetes 集群
keywords: Docker, Extensions, sdk, Kubernetes
aliases:
 - /desktop/extensions-sdk/dev/kubernetes/
 - /desktop/extensions-sdk/guides/kubernetes/
---

Extensions SDK 不提供任何直接与 Docker Desktop 管理的 Kubernetes 集群或使用其他工具（如 KinD）创建的任何其他集群交互的 API 方法。但是，本页提供了一种方法，让您可以使用其他 SDK API 从扩展间接与 Kubernetes 集群交互。

要请求直接与 Docker Desktop 管理的 Kubernetes 交互的 API，您可以在 Extensions SDK GitHub 仓库中为[此 issue](https://github.com/docker/extensions-sdk/issues/181) 投票。

## 先决条件

### 启用 Kubernetes

您可以使用 Docker Desktop 中内置的 Kubernetes 来启动一个 Kubernetes 单节点集群。
`kubeconfig` 文件用于与 `kubectl` 命令行工具或其他客户端配合使用时配置对 Kubernetes 的访问。
Docker Desktop 方便地在用户主目录中为用户提供本地预配置的 `kubeconfig` 文件和 `kubectl` 命令。这是希望从 Docker Desktop 使用 Kubernetes 的用户快速上手的便捷方式。

## 将 `kubectl` 作为扩展的一部分附带

如果您的扩展需要与 Kubernetes 集群交互，建议将 `kubectl` 命令行工具作为扩展的一部分包含进来。这样，安装您扩展的用户就可以在其主机上安装 `kubectl`。

要了解如何将 `kubectl` 命令行工具作为 Docker Extension 镜像的一部分为多个平台附带，请参阅[构建多架构扩展](../extensions/multi-arch.md#adding-multi-arch-binaries)。

## 示例

以下代码片段已在 [Kubernetes 示例扩展](https://github.com/docker/extensions-sdk/tree/main/samples/kubernetes-sample-extension)中整合。它展示了如何通过附带 `kubectl` 命令行工具与 Kubernetes 集群交互。

### 检查 Kubernetes API 服务器是否可达

一旦 `kubectl` 命令行工具在 `Dockerfile` 中添加到扩展镜像，并在 `metadata.json` 中定义，Extensions 框架会在安装扩展时将 `kubectl` 部署到用户的主机上。

您可以使用 JS API `ddClient.extension.host?.cli.exec` 来执行 `kubectl` 命令，例如，检查给定特定上下文时 Kubernetes API 服务器是否可达：

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "cluster-info",
  "--request-timeout",
  "2s",
  "--context",
  "docker-desktop",
]);
```

### 列出 Kubernetes 上下文

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "config",
  "view",
  "-o",
  "jsonpath='{.contexts}'",
]);
```

### 列出 Kubernetes 命名空间

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "get",
  "namespaces",
  "--no-headers",
  "-o",
  'custom-columns=":metadata.name"',
  "--context",
  "docker-desktop",
]);
```

## 持久化 kubeconfig 文件

以下是从主机文件系统持久化和读取 `kubeconfig` 文件的不同方法。用户可以随时向 `kubeconfig` 文件添加、编辑或删除 Kubernetes 上下文。

> 警告
>
> `kubeconfig` 文件非常敏感，如果被发现，攻击者可以获得对 Kubernetes 集群的管理访问权限。

### 扩展的后端容器

如果您需要扩展在读取 `kubeconfig` 文件后持久化它，您可以有一个后端容器，该容器公开 HTTP POST 端点以将文件内容存储在内存中或容器文件系统的某处。这样，如果用户从扩展导航到 Docker Desktop 的其他部分然后返回，您就不需要再次读取 `kubeconfig` 文件。

```typescript
export const updateKubeconfig = async () => {
  const kubeConfig = await ddClient.extension.host?.cli.exec("kubectl", [
    "config",
    "view",
    "--raw",
    "--minify",
    "--context",
    "docker-desktop",
  ]);
  if (kubeConfig?.stderr) {
    console.log("error", kubeConfig?.stderr);
    return false;
  }

  // call backend container to store the kubeconfig retrieved into the container's memory or filesystem
  try {
    await ddClient.extension.vm?.service?.post("/store-kube-config", {
      data: kubeConfig?.stdout,
    });
  } catch (err) {
    console.log("error", JSON.stringify(err));
  }
};
```

### Docker 卷

卷是持久化 Docker 容器生成和使用的数据的首选机制。您可以使用它们来持久化 `kubeconfig` 文件。
通过在卷中持久化 `kubeconfig`，当扩展窗格关闭时，您不需要再次读取 `kubeconfig` 文件。这使其非常适合在从扩展导航到 Docker Desktop 的其他部分时持久化数据。

```typescript
const kubeConfig = await ddClient.extension.host?.cli.exec("kubectl", [
  "config",
  "view",
  "--raw",
  "--minify",
  "--context",
  "docker-desktop",
]);
if (kubeConfig?.stderr) {
  console.log("error", kubeConfig?.stderr);
  return false;
}

await ddClient.docker.cli.exec("run", [
  "--rm",
  "-v",
  "my-vol:/tmp",
  "alpine",
  "/bin/sh",
  "-c",
  `"touch /tmp/.kube/config && echo '${kubeConfig?.stdout}' > /tmp/.kube/config"`,
]);
```

### 扩展的 `localStorage`

`localStorage` 是浏览器 Web 存储的机制之一。它允许用户在浏览器中将数据保存为键值对以供以后使用。
`localStorage` 不会在浏览器（扩展窗格）关闭时清除数据。这使其非常适合在从扩展导航到 Docker Desktop 的其他部分时持久化数据。

```typescript
localStorage.setItem("kubeconfig", kubeConfig);
```

```typescript
localStorage.getItem("kubeconfig");
```
