---
title: 更新应用程序
weight: 30
linkTitle: "第二部分：更新应用程序"
keywords: 入门, 设置, 定位, 快速入门, 介绍, 概念, 容器,
  docker desktop
description: 对您的应用程序进行更改
aliases:
 - /get-started/03_updating_app/
 - /guides/workshop/03_updating_app/
---

在[第一部分](./02_our_app.md)中，您容器化了一个待办事项应用程序。在这一部分中，您将更新应用程序和镜像。您还将学习如何停止和删除容器。

## 更新源代码

在以下步骤中，当您没有任何待办事项列表项时，您将把“空文本”更改为“您还没有待办事项！在上面添加一个！”


1. 在 `src/static/js/app.js` 文件中，更新第 56 行以使用新的空文本。

   ```diff
   - <p className="text-center">No items yet! Add one above!</p>
   + <p className="text-center">You have no todo items yet! Add one above!</p>
   ```

2. 使用 `docker build` 命令构建您的更新版本的镜像。

   ```console
   $ docker build -t getting-started .
   ```

3. 使用更新后的代码启动一个新容器。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

您可能看到了如下错误：

```console
docker: Error response from daemon: driver failed programming external connectivity on endpoint laughing_burnell 
(bb242b2ca4d67eba76e79474fb36bb5125708ebdabd7f45c8eaf16caaabde9dd): Bind for 127.0.0.1:3000 failed: port is already allocated.
```

发生此错误是因为您无法在旧容器仍在运行时启动新容器。原因是旧容器已经在使用主机的端口 3000，并且机器上只有一个进程（包括容器）可以侦听特定端口。要解决此问题，您需要删除旧容器。

## 删除旧容器

要删除容器，您首先需要停止它。一旦它停止了，您就可以删除它。您可以使用 CLI 或 Docker Desktop 的图形界面删除旧容器。选择您最熟悉��选项。

{{< tabs >}}
{{< tab name="CLI" >}}

### 使用 CLI 删除容器

1. 使用 `docker ps` 命令获取容器的 ID。

   ```console
   $ docker ps
   ```

2. 使用 `docker stop` 命令停止容器。将 `<the-container-id>` 替换为 `docker ps` 中的 ID。

   ```console
   $ docker stop <the-container-id>
   ```

3. 容器停止后，您可以使用 `docker rm` 命令将其删除。

   ```console
   $ docker rm <the-container-id>
   ```

> [!NOTE]
>
> 您可以通过向 `docker rm` 命令添加 `force` 标志来在一个命令中停止和删除容器。例如：`docker rm -f <the-container-id>`

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

### 使用 Docker Desktop 删除容器

1. 打开 Docker Desktop 到 **Containers** 视图。
2. 为要删除的容器选择 **Actions** 列下的垃圾桶图标。
3. 在确认对话框中，选择 **Delete forever**。

{{< /tab >}}
{{< /tabs >}}

### 启动更新后的应用程序容器

1. 现在，使用 `docker run` 命令启动您更新后的应用程序。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

2. 在 [http://localhost:3000](http://localhost:3000) 上刷新您的浏览器，您应该会看到您更新后的帮助文本。

## 总结

在本节中，您学习了如何更新和重新构建容器，以及如何停止和删除容器。

相关信息：
 - [docker CLI 参考](/reference/cli/docker/)

## 后续步骤

接下来，您将学习如何与他人共享镜像。

{{< button text="共享应用程序" url="04_sharing_app.md" >}}
