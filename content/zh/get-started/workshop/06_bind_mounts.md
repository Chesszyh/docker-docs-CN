---
title: 使用绑定挂载
weight: 60
linkTitle: "第五部分：使用绑定挂载"
keywords: 'get started, setup, orientation, quickstart, intro, concepts, containers, docker desktop, 入门, 设置, 概览, 快速入门, 简介, 概念, 容器'
description: 在我们的应用程序中使用绑定挂载
aliases:
 - /guides/walkthroughs/access-local-folder/
 - /get-started/06_bind_mounts/
 - /guides/workshop/06_bind_mounts/
---

在[第四部分](./05_persisting_data.md)中，您使用了卷挂载来持久化数据库中的数据。当您需要某个持久位置来存储应用程序数据时，卷挂载是一个不错的选择。

绑定挂载是另一种类型的挂载，它允许您将主机文件系统中的目录共享到容器中。在开发应用程序时，您可以使用绑定挂载将源代码挂载到容器中。一旦您保存文件，容器就会立即看到您对代码所做的更改。这意味着您可以在容器中运行监视文件系统更改并对其做出响应的进程。

在本章中，您将了解如何使用绑定挂载和一个名为 [nodemon](https://npmjs.com/package/nodemon) 的工具来监视文件更改，然后自动重启应用程序。在大多数其他语言和框架中都有等效的工具。

## 快速卷类型比较

以下是使用 `--mount` 的命名卷和绑定挂载的示例：

- 命名卷：`type=volume,src=my-volume,target=/usr/local/data`
- 绑定挂载：`type=bind,src=/path/to/data,target=/usr/local/data`

下表概述了卷挂载和绑定挂载之间的主要区别。

|                                              | 命名卷                                      | 绑定挂载                                          |
| -------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------- |
| 主机位置                                | Docker 选择                                     | 您决定                                           |
| 使用容器内容填充新卷 | 是                                                | 否                                                   |
| 支持卷驱动程序                      | 是                                                | 否                                                   |

## 尝试绑定挂载

在查看如何使用绑定挂载来开发应用程序之前，您可以运行一个快速实验，以实际了解绑定挂载的工作原理。

1. 验证您的 `getting-started-app` 目录是否位于 Docker Desktop 文件共享设置中定义的目录中。此设置定义了您可以与容器共享文件系统的哪些部分。有关访问设置的详细信息，请参阅[文件共享](/manuals/desktop/settings-and-maintenance/settings.md#file-sharing)。

    > [!NOTE]
    > **File sharing**（文件共享）选项卡仅在 Hyper-V 模式下可用，因为在 WSL 2 模式和 Windows 容器模式下文件会自动共享。

2. 打开终端并将目录更改为 `getting-started-app` 目录。

3. 运行以下命令以在带有绑定挂载的 `ubuntu` 容器中启动 `bash`。

   {{< tabs >}}
   {{< tab name="Mac / Linux" >}}

   ```console
   $ docker run -it --mount type=bind,src="$(pwd)",target=/src ubuntu bash
   ```
   
   {{< /tab >}}
   {{< tab name="Command Prompt" >}}

   ```console
   $ docker run -it --mount "type=bind,src=%cd%,target=/src" ubuntu bash
   ```
   
   {{< /tab >}}
   {{< tab name="Git Bash" >}}

   ```console
   $ docker run -it --mount type=bind,src="/$(pwd)",target=/src ubuntu bash
   ```
   
   {{< /tab >}}
   {{< tab name="PowerShell" >}}

   ```console
   $ docker run -it --mount "type=bind,src=$($pwd),target=/src" ubuntu bash
   ```
   
   {{< /tab >}}
   {{< /tabs >}}
   
   `--mount type=bind` 选项告诉 Docker 创建一个绑定挂载，其中 `src` 是主机机器上的当前工作目录 (`getting-started-app`)，`target` 是该目录在容器内应该出现的位置 (`/src`)。

4. 运行命令后，Docker 在容器文件系统的根目录中启动一个交互式 `bash` 会话。

   ```console
   root@ac1237fad8db:/# pwd
   /
   root@ac1237fad8db:/# ls
   bin   dev  home  media  opt   root  sbin  srv  tmp  var
   boot  etc  lib   mnt    proc  run   src   sys  usr
   ```

5. 将目录更改为 `src` 目录。

   这是您在启动容器时挂载的目录。列出此目录的内容将显示与主机机器上 `getting-started-app` 目录中相同的文件。

   ```console
   root@ac1237fad8db:/# cd src
   root@ac1237fad8db:/src# ls
   Dockerfile  node_modules  package.json  spec  src  yarn.lock
   ```

6. 创建一个名为 `myfile.txt` 的新文件。

   ```console
   root@ac1237fad8db:/src# touch myfile.txt
   root@ac1237fad8db:/src# ls
   Dockerfile  myfile.txt  node_modules  package.json  spec  src  yarn.lock
   ```

7. 打开主机上的 `getting-started-app` 目录，观察 `myfile.txt` 文件是否在目录中。

   ```text
   ├── getting-started-app/
   │ ├── Dockerfile
   │ ├── myfile.txt
   │ ├── node_modules/
   │ ├── package.json
   │ ├── spec/
   │ ├── src/
   │ └── yarn.lock
   ```

8. 从主机删除 `myfile.txt` 文件。
9. 在容器中，再次列出 `app` 目录的内容。观察文件现在是否消失了。

   ```console
   root@ac1237fad8db:/src# ls
   Dockerfile  node_modules  package.json  spec  src  yarn.lock
   ```

10. 使用 `Ctrl` + `D` 停止交互式容器会话。

这就是关于绑定挂载的简要介绍。此过程演示了如何在主机和容器之间共享文件，以及更改如何立即反映在双方。现在您可以使用绑定挂载来开发软件了。

## 开发容器

使用绑定挂载是本地开发设置的常见做法。优点是开发机器不需要安装所有的构建工具和环境。只需一个 docker run 命令，Docker 就会拉取依赖项和工具。

### 在开发容器中运行您的应用程序

以下步骤描述了如何运行带有绑定挂载的开发容器，该容器执行以下操作：

- 将您的源代码挂载到容器中
- 安装所有依赖项
- 启动 `nodemon` 以监视文件系统更改

您可以使用 CLI 或 Docker Desktop 运行带有绑定挂载的容器。

{{< tabs >}}
{{< tab name="Mac / Linux CLI" >}}

1. 确保您当前没有任何 `getting-started` 容器正在运行。

2. 从 `getting-started-app` 目录运行以下命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
       -w /app --mount type=bind,src="$(pwd)",target=/app \
       node:18-alpine \
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的细分：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w /app` - 设置“工作目录”或命令运行的当前目录
   - `--mount type=bind,src="$(pwd)",target=/app` - 将主机的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:18-alpine` - 要使用的镜像。请注意，这是 Dockerfile 中您的应用程序的基础镜像
   - `sh -c "yarn install && yarn run dev"` - 命令。您正在使用 `sh` 启动 shell（alpine 没有 `bash`），运行 `yarn install` 以安装包，然后运行 `yarn run dev` 以启动开发服务器。如果您查看 `package.json`，您会看到 `dev` 脚本启动了 `nodemon`。

3. 您可以使用 `docker logs <container-id>` 查看日志。当您看到以下内容时，您就知道已准备就绪：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   查看完日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="PowerShell CLI" >}}

1. 确保您当前没有任何 `getting-started` 容器正在运行。

2. 从 `getting-started-app` 目录运行以下命令。

   ```powershell
   $ docker run -dp 127.0.0.1:3000:3000 `
       -w /app --mount "type=bind,src=$pwd,target=/app" `
       node:18-alpine `
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的细分：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w /app` - 设置“工作目录”或命令运行的当前目录
   - `--mount "type=bind,src=$pwd,target=/app"` - 将主机的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:18-alpine` - 要使用的镜像。请注意，这是 Dockerfile 中您的应用程序的基础镜像
   - `sh -c "yarn install && yarn run dev"` - 命令。您正在使用 `sh` 启动 shell（alpine 没有 `bash`），运行 `yarn install` 以安装包，然后运行 `yarn run dev` 以启动开发服务器。如果您查看 `package.json`，您会看到 `dev` 脚本启动了 `nodemon`。

3. 您可以使用 `docker logs <container-id>` 查看日志。当您看到以下内容时，您就知道已准备就绪：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   查看完日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="Command Prompt CLI" >}}

1. 确保您当前没有任何 `getting-started` 容器正在运行。

2. 从 `getting-started-app` 目录运行以下命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 ^
       -w /app --mount "type=bind,src=%cd%,target=/app" ^
       node:18-alpine ^
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的细分：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w /app` - 设置“工作目录”或命令运行的当前目录
   - `--mount "type=bind,src=%cd%,target=/app"` - 将主机的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:18-alpine` - 要使用的镜像。请注意，这是 Dockerfile 中您的应用程序的基础镜像
   - `sh -c "yarn install && yarn run dev"` - 命令。您正在使用 `sh` 启动 shell（alpine 没有 `bash`），运行 `yarn install` 以安装包，然后运行 `yarn run dev` 以启动开发服务器。如果您查看 `package.json`，您会看到 `dev` 脚本启动了 `nodemon`。

3. 您可以使用 `docker logs <container-id>` 查看日志。当您看到以下内容时，您就知道已准备就绪：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   查看完日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="Git Bash CLI" >}}

1. 确保您当前没有任何 `getting-started` 容器正在运行。

2. 从 `getting-started-app` 目录运行以下命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
       -w //app --mount type=bind,src="/$(pwd)",target=/app \
       node:18-alpine \
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的细分：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w //app` - 设置“工作目录”或命令运行的当前目录
   - `--mount type=bind,src="/$(pwd)",target=/app` - 将主机的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:18-alpine` - 要使用的镜像。请注意，这是 Dockerfile 中您的应用程序的基础镜像
   - `sh -c "yarn install && yarn run dev"` - 命令。您正在使用 `sh` 启动 shell（alpine 没有 `bash`），运行 `yarn install` 以安装包，然后运行 `yarn run dev` 以启动开发服务器。如果您查看 `package.json`，您会看到 `dev` 脚本启动了 `nodemon`。

3. 您可以使用 `docker logs <container-id>` 查看日志。当您看到以下内容时，您就知道已准备就绪：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   查看完日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

确保您当前没有任何 `getting-started` 容器正在运行。

运行带有绑定挂载的镜像。

1. 选择 Docker Desktop 顶部的搜索框。
2. 在搜索窗口中，选择 **Images**（镜像）选项卡。
3. 在搜索框中，指定容器名称 `getting-started`。

   > [!TIP]
   > 
   >  使用搜索过滤器过滤镜像并仅显示 **Local images**（本地镜像）。

4. 选择您的镜像，然后选择 **Run**（运行）。
5. 选择 **Optional settings**（可选设置）。
6. 在 **Host path**（主机路径）中，指定主机机器上 `getting-started-app` 目录的路径。
7. 在 **Container path**（容器路径）中，指定 `/app`。
8. 选择 **Run**（运行）。

您可以使用 Docker Desktop 查看容器日志。

1. 在 Docker Desktop 中选择 **Containers**（容器）。
2. 选择您的容器名称。

当您看到以下内容时，您就知道已准备就绪：

```console
nodemon -L src/index.js
[nodemon] 2.0.20
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `node src/index.js`
Using sqlite database at /etc/todos/todo.db
Listening on port 3000
```

{{< /tab >}}
{{< /tabs >}}

### 使用开发容器开发您的应用程序

更新主机机器上的应用程序，并查看更改在容器中的反映。

1. 在 `src/static/js/app.js` 文件的第 109 行，将 "Add Item" 按钮更改为简单的 "Add"：

   ```diff
   - {submitting ? 'Adding...' : 'Add Item'}
   + {submitting ? 'Adding...' : 'Add'}
   ```

   保存文件。

2. 刷新 Web 浏览器中的页面，由于绑定挂载，您应该几乎立即看到更改反映出来。Nodemon 检测到更改并重启服务器。Node 服务器重启可能需要几秒钟。如果出现错误，请尝试几秒钟后刷新。

   ![更新后的添加按钮标签截图](images/updated-add-button.webp)

3. 随意进行您想要进行的任何其他更改。每次进行更改并保存文件时，由于绑定挂载，更改都会反映在容器中。当 Nodemon 检测到更改时，它会自动重启容器内的应用程序。完成后，停止容器并使用以下命令构建新镜像：

   ```console
   $ docker build -t getting-started .
   ```

## 总结

此时，您可以持久化数据库并在开发时查看应用程序中的更改，而无需重建镜像。

除了卷挂载和绑定挂载，Docker 还支持其他挂载类型和存储驱动程序，以处理更复杂和专用的用例。

相关信息：

 - [docker CLI 参考](/reference/cli/docker/)
 - [在 Docker 中管理数据](https://docs.docker.com/storage/)

## 下一步

为了让您的应用程序为生产做好准备，您需要将数据库从 SQLite 迁移到可以更好地扩展的数据库。为简单起见，您将继续使用关系数据库，并将应用程序切换为使用 MySQL。但是，您应该如何运行 MySQL？您如何允许容器相互通信？您将在下一节中了解这一点。

{{< button text="多容器应用程序" url="07_multi_container.md" >}}
