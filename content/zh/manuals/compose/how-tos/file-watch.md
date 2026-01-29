---
description: 使用文件监听在您工作时自动更新运行中的服务
keywords: compose, file watch, 实验性
title: 使用 Compose Watch
weight: 50
---

{{< summary-bar feature_name="Compose 文件监听" >}}

{{% include "compose/watch.md" %}}

`watch` 遵循以下文件路径规则：
* 除忽略文件模式外，所有路径均相对于项目目录
* 目录会被递归监听
* 不支持通配符（Glob）模式
* `.dockerignore` 中的规则适用
  * 使用 `ignore` 选项定义要忽略的其他路径（语法相同）
  * 常见 IDE（Vim、Emacs、JetBrains 等）的临时/备份文件会被自动忽略
  * `.git` 目录会被自动忽略

您不需要为 Compose 项目中的所有服务都开启 `watch`。在某些情况下，只有项目的一部分（例如 Javascript 前端）可能适合自动更新。

Compose Watch 旨在配合使用 `build` 属性基于本地源代码构建的服务。对于依赖于通过 `image` 属性指定的预构建镜像的服务，它不会跟踪其更改。

## Compose Watch 与绑定挂载 (bind mounts) 的对比

Compose 支持在服务容器内共享宿主机目录。监听模式并不会取代此功能，而是作为一种特别适合在容器中开发的辅助功能而存在。

更重要的是，`watch` 允许比绑定挂载更细的粒度。监听规则允许您忽略监听树中的特定文件或整个目录。

例如，在 JavaScript 项目中，忽略 `node_modules/` 目录有两个好处：
* 性能：在某些配置下，包含许多小文件的文件树可能会导致高 I/O 负载
* 多平台：如果宿主机操作系统或架构与容器不同，编译后的产物将无法共享

例如，在 Node.js 项目中，不建议同步 `node_modules/` 目录。尽管 JavaScript 是解释执行的，但 `npm` 包可能包含不可在不同平台间移植的原生代码。

## 配置

`watch` 属性定义了一组规则，用于根据本地文件更改来控制服务的自动更新。

每条规则都需要一个 `path`（路径）模式和在检测到修改时要采取的 `action`（操作）。`watch` 有两种可能的操作，根据 `action` 的不同，可能还接受或需要其他字段。 

监听模式可以配合许多不同的语言和框架使用。具体的路径和规则会因项目而异，但概念是一样的。 

### 前提条件

为了正常工作，`watch` 依赖于一些常用的可执行文件。请确保您的服务镜像包含以下二进制文件：
* stat
* mkdir
* rmdir

`watch` 还要求容器的 `USER` 能够写入目标路径，以便更新文件。一种常见的模式是使用 Dockerfile 中的 `COPY` 指令将初始内容复制到容器中。为了确保这些文件归属于配置的用户，请使用 `COPY --chown` 标志：

```dockerfile
# 以非特权用户身份运行
FROM node:18
RUN useradd -ms /bin/sh -u 1001 app
USER app

# 安装依赖项
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

# 将源文件复制到应用程序目录
COPY --chown=app:app . /app
```

### `action`

#### 同步 (Sync)

如果 `action` 设置为 `sync`（同步），Compose 会确保您宿主机上对文件的任何更改都会自动同步到服务容器内的相应文件中。

`sync` 非常适合支持“热重载（Hot Reload）”或同等功能的框架。

更广泛地说，对于许多开发用例，`sync` 规则可以代替绑定挂载。

#### 重新构建 (Rebuild)

如果 `action` 设置为 `rebuild`（重新构建），Compose 会自动使用 BuildKit 构建新镜像并替换运行中的服务容器。

其行为与运行 `docker compose up --build <svc>` 相同。

重新构建非常适合编译型语言，或者作为需要完整镜像重构的特定文件（例如 `package.json`）修改后的回退方案。

#### 同步 + 重启 (Sync + Restart)

如果 `action` 设置为 `sync+restart`（同步+重启），Compose 会将您的更改同步到服务容器并重启它们。 

当配置文件发生更改，且您不需要重新构建镜像而只需重启服务容器的主进程时，`sync+restart` 是理想的选择。例如，当您更新数据库配置或 `nginx.conf` 文件时，它的效果会非常好。

>[!TIP]
>
> 利用 [镜像层缓存](/build/cache) 和 [多阶段构建](/build/building/multi-stage/) 优化您的 `Dockerfile`，以实现快速的增量重新构建。

### `path` 和 `target`

`target` 字段控制路径如何映射到容器中。

对于 `path: ./app/html` 且 `./app/html/index.html` 发生更改的情况：

* `target: /app/html` -> `/app/html/index.html`
* `target: /app/static` -> `/app/static/index.html`
* `target: /assets` -> `/assets/index.html`

### `ignore`

`ignore` 模式是相对于当前 `watch` 操作中定义的 `path` 的，而不是相对于项目目录。在下面的示例 1 中，忽略路径将相对于 `path` 属性中指定的 `./web` 目录。

## 示例 1

此最小示例针对具有以下结构的 Node.js 应用程序：
```text
myproject/
├── web/
│   ├── App.jsx
│   ├── index.js
│   └── node_modules/
├── Dockerfile
├── compose.yaml
└── package.json
```

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /src/web
          ignore:
            - node_modules/
        - action: rebuild
          path: package.json
```

在此示例中，运行 `docker compose up --watch` 时，将使用项目根目录下基于 `Dockerfile` 构建的镜像启动 `web` 服务容器。`web` 服务运行 `npm start` 命令，随后会在打包器（Webpack、Vite、Turbopack 等）启用热模块替换（Hot Module Reload）的情况下启动应用程序的开发版本。

服务启动后，监听模式开始监控目标目录和文件。之后，每当 `web/` 目录中的源文件发生更改时，Compose 都会将该文件同步到容器内 `/src/web` 下的相应位置。例如，`./web/App.jsx` 被复制到 `/src/web/App.jsx`。

复制完成后，打包器会更新正在运行的应用程序，而无需重启。

在这种情况下，`ignore` 规则将应用于 `myproject/web/node_modules/` ，而不是 `myproject/node_modules/`。

与源代码文件不同，添加新依赖项无法实时完成，因此每当 `package.json` 发生更改时，Compose 都会重新构建镜像并重新创建 `web` 服务容器。

此模式适用于许多语言和框架，例如 Python 配合 Flask：可以同步 Python 源文件，而对 `requirements.txt` 的更改应触发重新构建。

## 示例 2 

调整前面的示例以演示 `sync+restart`：

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /app/web
          ignore:
            - node_modules/
        - action: sync+restart
          path: ./proxy/nginx.conf
          target: /etc/nginx/conf.d/default.conf

  backend:
    build:
      context: backend
      target: builder
```

这种设置展示了如何在 Docker Compose 中使用 `sync+restart` 操作，高效地开发和测试具有前端 Web 服务器和后端服务的 Node.js 应用程序。该配置确保应用程序代码和配置文件的更改能够快速同步并应用，且 `web` 服务会根据需要重启以反映更改。

## 使用 `watch`

{{% include "compose/configure-watch.md" %}}

> [!NOTE]
>
> 如果您不希望应用程序日志与（重新）构建日志以及文件系统同步事件混在一起，也可以配合使用专门的 `docker compose watch` 命令。

> [!TIP]
>
> 查看 [`dockersamples/avatars`](https://github.com/dockersamples/avatars) 或 [Docker 文档的本地设置](https://github.com/docker/docs/blob/main/CONTRIBUTING.md) 以获取 Compose `watch` 的演示。

## 参考

- [Compose 开发规范](/reference/compose-file/develop.md)
