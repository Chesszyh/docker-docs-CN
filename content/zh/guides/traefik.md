---
title: 使用 Traefik 进行 HTTP 路由
description: &desc 使用 Traefik 轻松地在多个容器或非容器化工作负载之间路由流量
keywords: traefik, 容器支持的开发
linktitle: 使用 Traefik 进行 HTTP 路由
summary: *desc
tags: [networking]
params:
  time: 20 分钟
---

## 简介

在本地开发期间，通常需要运行多个 HTTP 服务。你可能同时拥有一个 API 和一个前端应用程序、一个用于模拟数据端点的 WireMock 服务，或者一个数据库可视化工具（例如 phpMyAdmin 或 pgAdmin）。在许多开发设置中，这些服务都暴露在不同的端口上，这不仅需要你记住哪个服务在哪个端口上，还可能引入其他问题（例如 CORS）。

反向代理可以通过作为单个暴露的服务，然后根据请求 URL（通过路径或主机名）将请求路由到适当的服务，从而极大地简化此设置。[Traefik](https://traefik.io/traefik/) 是一个现代的、云原生的反向代理和负载均衡器，它使开发和部署多服务应用程序变得更加容易。本指南将向你展示如何将 Traefik 与 Docker 结合��用以增强你的开发环境。

在本指南中，你将学习如何：

1. 使用 Docker 启动 Traefik
2. 配置路由规则以在两个容器之间分配流量
3. 在容器化开发环境中使用 Traefik
4. 使用 Traefik 将请求发送到非容器化工作负载

## 先决条件

要学习本操作指南，需要满足以下先决条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager) 和 [yarn](https://yarnpkg.com/)
- Docker 基础知识

## 将 Traefik 与 Docker 结合使用

Traefik 的独特功能之一是它能够以多种方式进行配置。当使用 Docker 提供程序时，Traefik 使用[标签](https://docs.docker.com/config/labels-custom-metadata/)从其他正在运行的容器中获取其配置。Traefik 将监视引擎事件（用于容器启动和停止），提取标签，并更新其配置。

虽然有[许多 Traefik 监视的标签](https://doc.traefik.io/traefik/routing/providers/docker/)，但最常见的两个是：

- `traefik.http.routers.<service-name>.rule` - 用于指示路由规则（[在此处查看所有可用规则](https://doc.traefik.io/traefik/routing/routers/#rule)）
- `traefik.http.services.<service-name>.loadbalancer.server.port` - 指示 Traefik 应将请求转发到的端口。请��意，此容器端口不需要在你的主机上暴露（[在此处阅读有关端口检测的信息](https://doc.traefik.io/traefik/providers/docker/#port-detection)）

让我们快速演示一下如何启动 Traefik，然后配置两个额外的容器，以便可以使用不同的主机名访问它们。

1. 为了让两个容器能够相互通信，它们需要位于同一个网络上。使用 `docker network create` 命令创建一个名为 `traefik-demo` 的网络：

   ```console
   $ docker network create traefik-demo
   ```

2. 使用以下命令启动一个 Traefik 容器。该命令在端口 80 上暴露 Traefik，挂载 Docker 套接字（用于监视容器以更新配置），并传递 `--providers.docker` 参数以将 Traefik 配置为使用 Docker 提供程序。

   ```console
   $ docker run -d --network=traefik-demo -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock traefik:v3.1.2 --providers.docker
   ```

3. 现在，启动一个简单的 Nginx 容器，并定义 Traefik 正在监视的标签以配置 HTTP 路由。请注意，Nginx 容器没有暴露任何端口。

   ```console
   $ docker run -d --network=traefik-demo --label 'traefik.http.routers.nginx.rule=Host(`nginx.localhost`)' nginx
   ```

   容器启动后，在浏览器中打开 [http://nginx.localhost](http://nginx.localhost) 以查看该应用���序（所有基于 Chromium 的浏览器都会在本地路由 \*.localhost 请求，无需额外设置）。

4. 启动将使用不同主机名的第二个应用程序。

   ```console
   $ docker run -d --network=traefik-demo --label 'traefik.http.routers.welcome.rule=Host(`welcome.localhost`)' docker/welcome-to-docker
   ```

   容器启动后，在浏览器中打开 http://welcome.localhost。你应该会看到一个“Welcome to Docker”网站。

## 在开发中使用 Traefik

现在你已经体验了 Traefik，是时候在开发环境中使用它了。在此示例中，你将使用一个具有拆分前端和后端的示例应用程序。此应用程序堆栈具有以下配置：

1. 所有对 /api 的请求都转到 API 服务
2. 所有其他对 localhost 的请求都转到前端客户端
3. 由于该应用程序使用 MySQL，因此 db.localhost 应提供 phpMyAdmin，以便在开发期间轻松访问数据库

![显示 Traefik 根据请求路径将请求路由到其他容器的架构图](./images/traefik-in-development.webp)

该应用程序可以在 GitHub 上的 [dockersamples/easy-http-routing-with-traefik](https://github.com/dockersamples/easy-http-routing-with-traefik) 访问。

1. 在 `compose.yaml` 文件中，Traefik 使用以下配置：

   ```yaml
   services:
     proxy:
       image: traefik:v3.1.2
       command: --providers.docker
       ports:
         - 80:80
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock
   ```

   请注意，这与之前使用的配置基本相同，但现在采用 Compose 语法。

2. 客户端服务具有以下配置，它将启动容器并为其提供标签以在 localhost 接收请求。

   ```yaml {hl_lines=[7,8]}
   services:
     # …
     client:
       image: nginx:alpine
       volumes:
         - "./client:/usr/share/nginx/html"
       labels:
         traefik.http.routers.client.rule: "Host(`localhost`)"
   ```

3. api 服务具有类似的配置，但你会注意到路由规则有两个条件——主机必须是“localhost”，并且 URL 路径必须具有“/api”前缀。由于此规则更具体，因此 Traefik 将首先评估它，而不是客户端规则。

   ```yaml {hl_lines=[7,8]}
   services:
     # …
     api:
       build: ./dev/api
       volumes:
         - "./api:/var/www/html/api"
       labels:
         traefik.http.routers.api.rule: "Host(`localhost`) && PathPrefix(`/api`)"
   ```

4. 最后，`phpmyadmin` 服务被配置为接收主机名“db.localhost”的请求。该服务还定义了环境变量以自动登录，从而更容易进入该应用程序。

   ```yaml {hl_lines=[5,6]}
   services:
     # …
     phpmyadmin:
       image: phpmyadmin:5.2.1
       labels:
         traefik.http.routers.db.rule: "Host(`db.localhost`)"
       environment:
         PMA_USER: root
         PMA_PASSWORD: password
   ```

5. 在启动堆栈之前，如果 Nginx 容器仍在运行，请停止它。

就是这样。现在，你只需要使用 `docker compose up` 启动 Compose 堆栈，所有服务和应用程序都将准备好进行开发。

## 将流量发送到非容器化工作负载

在某些情况下，你可能希望将请求转发到未在容器中运行的应用程序。在以下架构图中，使用了与之前相同的应用程序，但 API 和 React 应用程序现在在本机上运行。

![一个显示多个组件及其之间路由的架构图。Traefik 能够将请求发送到非容器化和容器化工作负载](images/traefik-non-containerized-workload-architecture.webp)

为此，Traefik 将需要使用另一种方法来配置自身。[文件提供程序](https://doc.traefik.io/traefik/providers/file/)允许你在 YAML 文档中定义路由规则。这是一个示例文件：

```yaml
http:
  routers:
    native-api:
      rule: "Host(`localhost`) && PathPrefix(`/api`)"
      service: native-api
    native-client:
      rule: "Host(`localhost`)"
      service: native-client

  services:
    native-api:
      loadBalancer:
        servers:
          - url: "http://host.docker.internal:3000/"
    native-client:
      loadBalancer:
        servers:
          - url: "http://host.docker.internal:5173/"
```

此配置指示对 `localhost/api` 的请求将转发到名为 `native-api` 的服务，然后该服务将请求转发到 http://host.docker.internal:3000。主机名 `host.docker.internal` 是 Docker Desktop 提供的用于向主机发送请求的名称。

使用此文件，唯一的变化是 Traefik 的 Compose 配置。具体来说，有两件事发生了变化：

1. 配置文件被挂载到 Traefik 容器中（确切的目标路径由你决定）
2. `command` 被更新以添加文件提供程序并指向配置文件的位置

```yaml
services:
  proxy:
    image: traefik:v3.1.2
    command: --providers.docker --providers.file.filename=/config/traefik-config.yaml --api.insecure
    ports:
      - 80:80
      - 8080:8080
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./dev/traefik-config.yaml:/config/traefik-config.yaml
```

### 启动示例应用程序

要运行将请求从 Traefik 转发到本机运行的应用程序的示例应用程序，请使用以下步骤：

1. 如果你的 Compose 堆栈仍在运行，请使用以下命令停止它：

   ```console
   $ docker compose down
   ```

2. 使用提���的 `compose-native.yaml` 文件启动应用程序：

   ```console
   $ docker compose -f compose-native.yaml up
   ```

   打开 [http://localhost](http://localhost) 将返回 502 Bad Gateway，因为其他应用程序尚未运行。

3. 通过运行以下步骤启动 API：

   ```console
   cd api
   yarn install
   yarn dev
   ```

4. 在新终端中（从项目根目录开始）通过运行以下步骤启动前端：

   ```console
   cd client
   yarn install
   yarn dev
   ```

5. 在 [http://localhost](http://localhost) 打开应用程序。你应该会看到一个从 [http://localhost/api/messages](http://localhost/api/messages) 获取消息的应用程序。你还可以打开 [http://db.localhost](http://db.localhost) 以直接从 Mongo 数据库查看或调整可用消息。Traefik 将确保请求正确路由到正确的容器或应用程序。

6. 完成后，运行 `docker compose down` 以停止容器，并通过按 `ctrl+c` 停止 Yarn 应用程序。

## 回顾

运行多个服务不必需要复杂的端口配置和良好的记忆力。使用 Traefik 等工具，可以轻松启动所需的服务并轻松访问它们——无论它们是用于应用程序本身（例如前端和后端）还是用于其他开发工具（例如 phpMyAdmin）。
