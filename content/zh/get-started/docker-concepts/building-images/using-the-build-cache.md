---
title: 使用构建缓存
keywords: concepts, build, images, container, docker desktop, 概念, 构建, 镜像, 容器
description: 此概念页面将向您介绍构建缓存、哪些更改会使缓存失效以及如何有效地使用构建缓存。
summary: |
  有效地使用构建缓存允许您通过重用先前构建的结果并跳过不必要的步骤来实现更快的构建。为了最大化缓存使用并避免资源密集且耗时的重建，了解缓存失效的工作原理至关重要。在本指南中，您将学习如何高效地使用 Docker 构建缓存，以简化 Docker 镜像开发和持续集成工作流程。
weight: 4
aliases: 
 - /guides/docker-concepts/building-images/using-the-build-cache/
---

{{< youtube-embed Ri6jMknjprY >}}

## 解释

考虑您为 [getting-started](./writing-a-dockerfile/) 应用程序创建的以下 Dockerfile。


```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "./src/index.js"]
```

当您运行 `docker build` 命令创建新镜像时，Docker 会执行 Dockerfile 中的每条指令，并按指定的顺序为每条命令创建一个层。对于每条指令，Docker 都会检查是否可以重用先前构建中的指令。如果它发现您之前已经执行过类似的指令，Docker 就不需要重新执行。相反，它将使用缓存的结果。这样，您的构建过程就会变得更快、更高效，从而节省您宝贵的时间和资源。

有效地使用构建缓存可以让您通过重用先前构建的结果并跳过不必要的工作来实现更快的构建。
为了最大化缓存使用并避免资源密集且耗时的重新构建，了解缓存失效的工作原理非常重要。
以下是一些可能导致缓存失效的情况示例：

- 对 `RUN` 指令命令的任何更改都会使该层失效。如果 Dockerfile 中的 `RUN` 命令有任何修改，Docker 会检测到更改并使构建缓存失效。

- 使用 `COPY` 或 `ADD` 指令复制到镜像中的文件的任何更改。Docker 会留意项目目录中文件的任何改动。无论是内容的变化还是权限等属性的变化，Docker 都会将这些修改视为触发缓存失效。

- 一旦一层失效，其后的所有层也会失效。如果由于更改导致之前的任何层（包括基础镜像或中间层）失效，Docker 会确保依赖它的后续层也失效。这保持了构建过程的同步并防止了不一致。

在编写或编辑 Dockerfile 时，请留意不必要的缓存未命中，以确保构建运行得尽可能快且高效。

## 试一试

在本实践指南中，您将学习如何有效地为 Node.js 应用程序使用 Docker 构建缓存。

### 构建应用程序

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 打开终端并[克隆此示例应用程序](https://github.com/dockersamples/todo-list-app)。


    ```console
    $ git clone https://github.com/dockersamples/todo-list-app
    ```

3. 进入 `todo-list-app` 目录：


    ```console
    $ cd todo-list-app
    ```

    在此目录中，您将找到一个名为 `Dockerfile` 的文件，内容如下：


    ```dockerfile
    FROM node:20-alpine
    WORKDIR /app
    COPY . .
    RUN yarn install --production
    EXPOSE 3000
    CMD ["node", "./src/index.js"]
    ```

4. 执行以下命令构建 Docker 镜像：

    ```console
    $ docker build .
    ```

    以下是构建过程的结果：

    ```console
    [+] Building 20.0s (10/10) FINISHED
    ```

    第一行表示整个构建过程耗时 *20.0 秒*。第一次构建可能需要一些时间，因为它会安装依赖项。

5. 在不进行更改的情况下重新构建。

   现在，在不更改源代码或 Dockerfile 的情况下重新运行 `docker build` 命令，如下所示：

    ```console
    $ docker build .
    ```

   只要命令和上下文保持不变，初始构建之后的后续构建就会更快，因为有缓存机制。Docker 会缓存构建过程中生成的中间层。当您在不更改 Dockerfile 或源代码的情况下重新构建镜像时，Docker 可以重用缓存的层，从而显著加快构建速度。

    ```console
    [+] Building 1.0s (9/9) FINISHED                                                                            docker:desktop-linux
     => [internal] load build definition from Dockerfile                                                                        0.0s
     => => transferring dockerfile: 187B                                                                                        0.0s
     ...
     => [internal] load build context                                                                                           0.0s
     => => transferring context: 8.16kB                                                                                         0.0s
     => CACHED [2/4] WORKDIR /app                                                                                               0.0s
     => CACHED [3/4] COPY . .                                                                                                   0.0s
     => CACHED [4/4] RUN yarn install --production                                                                              0.0s
     => exporting to image                                                                                                      0.0s
     => => exporting layers                                                                                                     0.0s
     => => exporting manifest
   ```


   利用缓存层，后续构建仅用 1.0 秒就完成了。无需重复安装依赖项等耗时步骤。


    <table>
      <tr>
       <td>步骤
       </td>
       <td>描述
       </td>
       <td>耗时 (第一次运行)
       </td>
       <td>耗时 (第二次运行)
       </td>
      </tr>
      <tr>
       <td>1
       </td>
       <td>从 Dockerfile 加载构建定义
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>2
       </td>
       <td>加载 docker.io/library/node:20-alpine 的元数据
       </td>
       <td>2.7 秒
       </td>
       <td>0.9 秒
       </td>
      </tr>
      <tr>
       <td>3
       </td>
       <td>加载 .dockerignore
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>4
       </td>
       <td>加载构建上下文
    <p>
    (上下文大小：4.60MB)
       </td>
       <td>0.1 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>5
       </td>
       <td>设置工作目录 (WORKDIR)
       </td>
       <td>0.1 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>6
       </td>
       <td>将本地代码复制到容器中
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>7
       </td>
       <td>运行 yarn install --production
       </td>
       <td>10.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>8
       </td>
       <td>导出层
       </td>
       <td>2.2 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>9
       </td>
       <td>导出最终镜像
       </td>
       <td>3.0 秒
       </td>
       <td>0.0 秒
       </td>
     </tr>
    </table>


    回到 `docker image history` 输出，您会看到 Dockerfile 中的每个命令都会成为镜像中的一个新层。您可能还记得，当您更改镜像时，必须重新安装 `yarn` 依赖项。有没有办法解决这个问题？每次构建都重新安装相同的依赖项没有太大意义，对吧？

    为了解决这个问题，请重构 Dockerfile，使依赖项缓存保持有效，除非确实需要使其失效。对于基于 Node 的应用程序，依赖项在 `package.json` 文件中定义。如果该文件发生更改，您需要重新安装依赖项，但如果该文件未更改，则使用缓存的依赖项。因此，首先仅复制该文件，然后安装依赖项，最后复制其他所有内容。这样，只有在 `package.json` 文件发生更改时，才需要重新创建 yarn 依赖项。

6. 更新 Dockerfile 以首先复制 `package.json` 文件，安装依赖项，然后再复制其他所有内容。

     ```dockerfile
     FROM node:20-alpine
     WORKDIR /app
     COPY package.json yarn.lock ./
     RUN yarn install --production 
     COPY . . 
     EXPOSE 3000
     CMD ["node", "src/index.js"]
     ```

7. 在 Dockerfile 所在的同一文件夹中创建一个名为 `.dockerignore` 的文件，内容如下。

     ```plaintext
     node_modules
     ```

8. 构建新镜像：

    ```console
    $ docker build .
    ```

    然后您将看到如下所示的输出：

    ```console
    [+] Building 16.1s (10/10) FINISHED
    => [internal] load build definition from Dockerfile                                               0.0s
    => => transferring dockerfile: 175B                                                               0.0s
    => [internal] load .dockerignore                                                                  0.0s
    => => transferring context: 2B                                                                    0.0s
    => [internal] load metadata for docker.io/library/node:21-alpine                                  0.0s
    => [internal] load build context                                                                  0.8s
    => => transferring context: 53.37MB                                                               0.8s
    => [1/5] FROM docker.io/library/node:21-alpine                                                    0.0s
    => CACHED [2/5] WORKDIR /app                                                                      0.0s
    => [3/5] COPY package.json yarn.lock ./                                                           0.2s
    => [4/5] RUN yarn install --production                                                           14.0s
    => [5/5] COPY . .                                                                                 0.5s
    => exporting to image                                                                             0.6s
    => => exporting layers                                                                            0.6s
    => => writing image     
    sha256:d6f819013566c54c50124ed94d5e66c452325327217f4f04399b45f94e37d25        0.0s
    => => naming to docker.io/library/node-app:2.0                                                 0.0s
    ```

    您会看到所有的层都被重新构建了。这完全没问题，因为您对 Dockerfile 进行了相当大的更改。

9. 现在，对 `src/static/index.html` 文件进行更改（例如将标题改为 "The Awesome Todo App"）。

10. 构建 Docker 镜像。这一次，您的输出应该看起来有点不同。

    ```console
    $ docker build -t node-app:3.0 .
    ```

    您将看到如下所示的输出：

    ```console
    [+] Building 1.2s (10/10) FINISHED 
    => [internal] load build definition from Dockerfile                                               0.0s
    => => transferring dockerfile: 37B                                                                0.0s
    => [internal] load .dockerignore                                                                  0.0s
    => => transferring context: 2B                                                                    0.0s
    => [internal] load metadata for docker.io/library/node:21-alpine                                  0.0s 
    => [internal] load build context                                                                  0.2s
    => => transferring context: 450.43kB                                                              0.2s
    => [1/5] FROM docker.io/library/node:21-alpine                                                    0.0s
    => CACHED [2/5] WORKDIR /app                                                                      0.0s
    => CACHED [3/5] COPY package.json yarn.lock ./                                                    0.0s
    => CACHED [4/5] RUN yarn install --production                                                     0.0s
    => [5/5] COPY . .                                                                                 0.5s 
    => exporting to image                                                                             0.3s
    => => exporting layers                                                                            0.3s
    => => writing image     
    sha256:91790c87bcb096a83c2bd4eb512bc8b134c757cda0bdee4038187f98148e2eda       0.0s
    => => naming to docker.io/library/node-app:3.0                                                 0.0s
    ```

    首先，您应该注意到构建速度快得多。您会看到几个步骤正在使用以前缓存的层。这是个好消息；您正在使用构建缓存。推送和拉取此镜像及其更新也将快得多。

通过遵循这些优化技术，您可以使 Docker 构建更快速、更高效，从而缩短迭代周期并提高开发生产力。

## 其他资源

* [通过缓存管理优化构建](/build/cache/)
* [缓存存储后端](/build/cache/backends/)
* [构建缓存失效](/build/cache/invalidation/)


## 下一步

现在您已经了解了如何有效地使用 Docker 构建缓存，您可以开始学习多阶段构建了。

{{< button text="多阶段构建" url="multi-stage-builds" >}}