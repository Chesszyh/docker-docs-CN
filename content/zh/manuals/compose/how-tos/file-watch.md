---
description: 使用文件监视在您工作时自动更新正在运行的服务
keywords: compose, file watch, experimental, 文件监视, 实验性
title: 使用 Compose Watch
weight: 50
aliases:
- /compose/file-watch/
---

{{< summary-bar feature_name="Compose file watch" >}}

{{% include "compose/watch.md" %}}

`watch` 遵循以下文件路径规则：
* 除忽略文件模式外，所有路径都相对于项目目录
* 目录被递归监视
* 不支持 Glob 模式
* `.dockerignore` 中的规则适用
  * 使用 `ignore` 选项定义要忽略的其他路径（语法相同）
  * 常见 IDE（Vim、Emacs、JetBrains 等）的临时/备份文件会自动忽略
  * `.git` 目录会自动忽略

您无需为 Compose 项目中的所有服务都打开 `watch`。在某些情况下，只有项目的一部分，例如 Javascript 前端，可能适合自动更新。

Compose Watch 旨在与使用 `build` 属性从本地源代码构建的服务一起使用。它不会跟踪依赖于由 `image` 属性指定的预构建镜像的服务的更改。

## Compose Watch 与绑定挂载

Compose 支持在服务容器内共享主机目录。监视模式不会取代此功能，而是作为专门用于在容器中开发的伴侣而存在。

更重要的是，`watch` 允许比绑定挂载更实用的粒度。监视规则允许您忽略监视树中的特定文件或整个目录。

例如，在 JavaScript 项目中，忽略 `node_modules/` 目录有两个好处：
* 性能。在某些配置中，具有许多小文件的文件树可能会导致高 I/O 负载
* 多平台。如果主机操作系统或体系结构与容器不同，则无法共享已编译的工件

例如，在 Node.js 项目中，不建议同步 `node_modules/` 目录。尽管 JavaScript 是解释性的，但 `npm` 包可能包含在平台之间不可移植的本机代码。

## 配置

`watch` 属性定义了一个规则列表，用于根据本地文件更改控制自动服务更新。

每个规则都需要一个 `path` 模式和一个在检测到修改时要执行的 `action`。`watch` 有两种可能的操作，并且根据 `action`，可能会接受或需要其他字段。

监视模式可以与许多不同的语言和框架一起使用。
具体的路径和规则因项目而异，但概念保持不变。

### 先决条件

为了正常工作，`watch` 依赖于常见的可执行文件。确保您的服务镜像包含以下二进制文件：
* stat
* mkdir
* rmdir

`watch` 还要求容器的 `USER` 可以写入目标路径，以便它可以更新文件。一种常见的模式是��用 Dockerfile 中的 `COPY` 指令将初始内容复制到容器中。为确保此类文件归配置的用户所有，请使用 `COPY --chown` 标志：

```dockerfile
# 以非特权用户身份运行
FROM node:18
RUN useradd -ms /bin/sh -u 1001 app
USER app

# 安装依赖项
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

# 将源文件复制到应用程序目录中
COPY --chown=app:app . /app
```

### `action`

#### Sync

如果 `action` 设置为 `sync`，Compose 会确保您对主机上文件所做的任何更改都会自动与服务容器中的相应文件匹配。

`sync` 非常适合支持“热重载”或等效功能的框架。

更一般地说，`sync` 规则可以代替许多开发用例的绑定挂载。

#### Rebuild

如果 `action` 设置为 `rebuild`，Compose 会自动使用 BuildKit 构建一个新镜像并替换正在运行的服务容器。

该行为与运行 `docker compose up --build <svc>` 相同。

Rebuild 非常适合已编译的语言，或作为修改需要完全重新构建镜像的特定文件（例如 `package.json`）的回退。

#### Sync + Restart

如果 `action` 设置为 `sync+restart`，Compose 会将您的更改与服务容器同步并重新启动它们。

当配置文件更改时，`sync+restart` 非常理想，您无需重新构建镜像，只需重新启动服务容器的主进程即可。
例如，当您更新数据库配置或 `nginx.conf` 文件时，它会很好地工作。

>[!TIP]
>
> 通过[镜像层缓存](/build/cache)和[多阶段构建](/build/building/multi-stage/)优化您的 `Dockerfile` 以实现快速的增量重建。

### `path` 和 `target`

`target` 字段控制路径如何映射到容器中。

对于 `path: ./app/html` 和对 `./app/html/index.html` 的更改：

* `target: /app/html` -> `/app/html/index.html`
* `target: /app/static` -> `/app/static/index.html`
* `target: /assets` -> `/assets/index.html`

### `ignore`

`ignore` 模式相对于当前 `watch` 操作中定义的 `path`，而不是项目目录。在下面的示例 1 中，忽略路径将相对于 `path` 属性中指定的 `./web` 目录。

## 示例 1

这个最小的示例针对具有以下结构的 Node.js 应用程序：
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

在此示例中，当运行 `docker compose up --watch` 时，会使用从项目根目录中的 `Dockerfile` 构建的镜像启动 `web` 服务的容器。
`web` 服务运行 `npm start` 作为其命令，然后启动一个开发版本的应用程序，并在捆绑器（Webpack、Vite、Turbopack 等）中启用了热模块重载。

服务启动后，监视模式开始监视目标目录和文件。
然后，每当 `web/` 目录中的源文件发生更改时，Compose 都会将文件同步到容器内 `/src/web` 下的相应位置。
例如，`./web/App.jsx` 被复制到 `/src/web/App.jsx`。

复制后，捆绑器会更新正在运行的应用程序，而无需重新启动。

在这种情况下，`ignore` 规则将适用于 `myproject/web/node_modules/`，而不是 `myproject/node_modules/`。

与源代码文件不同，添加新依赖项不能动态完成，因此每当 `package.json` 发生更改时，Compose 都会重新构建镜像并重新创建 `web` 服务容器。

这种模式可以用于许多语言和框架，例如使用 Flask 的 Python：可以同步 Python 源文件，而对 `requirements.txt` 的更改应触发重新构建。

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

此设置演示了如何在 Docker Compose 中使用 `sync+restart` 操作来高效地开发和测试具有前端 Web 服务器和后端服务的 Node.js 应用程序。该配置可确保应用程序代码和配置文件的更改得到快速同步和应用，并根据需要重新启动 `web` 服务以反映更改。

## 使用 `watch`

{{% include "compose/configure-watch.md" %}}

> [!NOTE]
>
> 如果您不希望应用程序日志与（重新）构建日志和文件系统同步事件混合在一起，也可以使用专用的 `docker compose watch` 命令。

> [!TIP]
>
> 查看 [`dockersamples/avatars`](https://github.com/dockersamples/avatars) 或 [Docker 文档的本地设置](https://github.com/docker/docs/blob/main/CONTRIBUTING.md) 以获取 Compose `watch` 的演示。

## 参考

- [Compose Develop 规范](/reference/compose-file/develop.md)
