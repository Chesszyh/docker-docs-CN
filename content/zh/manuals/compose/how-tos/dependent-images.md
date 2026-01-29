---
description: 为具有共享定义的多个服务构建镜像
keywords: compose, build
title: 构建依赖镜像
weight: 50
---

{{< summary-bar feature_name="Compose 依赖镜像" >}}

为了减少推送/拉取时间并减轻镜像重量，Compose 应用程序的一种常见做法是让各服务尽可能多地共享基础层。通常情况下，您会为所有服务选择相同的操作系统基础镜像。但您还可以更进一步，当镜像共享相同的系统软件包时，也共享镜像层。此时需要解决的挑战是如何避免在所有服务中重复完全相同的 Dockerfile 指令。

为了进行说明，本页假设您希望使用 `alpine` 基础镜像构建所有服务，并安装 `openssl` 系统包。

## 多阶段 Dockerfile

推荐的方法是在单个 Dockerfile 中对共享声明进行分组，并利用多阶段构建功能，从而使各服务的镜像都基于此共享声明构建。

Dockerfile:

```dockerfile
FROM alpine as base
RUN /bin/sh -c apk add --update --no-cache openssl

FROM base as service_a
# 构建 service a
...

FROM base as service_b
# 构建 service b
...
```

Compose 文件：

```yaml
services:
  a:
     build:
       target: service_a
  b:
     build:
       target: service_b
```

## 使用另一个服务的镜像作为基础镜像

一种流行的模式是在另一个服务中将某个服务的镜像重用为基础镜像。由于 Compose 不解析 Dockerfile，它无法自动检测服务之间的这种依赖关系，从而无法正确排序构建执行。

a.Dockerfile:

```dockerfile
FROM alpine
RUN /bin/sh -c apk add --update --no-cache openssl
```

b.Dockerfile:

```dockerfile
FROM service_a
# 构建 service b
```

Compose 文件：

```yaml
services:
  a:
     image: service_a 
     build:
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
```

旧版的 Docker Compose v1 过去是按顺序构建镜像的，这使得这种模式可以开箱即用。Compose v2 使用 BuildKit 来优化构建并并行构建镜像，因此需要显式声明。

推荐的方法是将依赖的基础镜像声明为附加上下文（additional build context）：

Compose 文件：

```yaml
services:
  a:
     image: service_a
     build: 
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM service_a` 将解析为对必须首先构建的服务 "a" 的依赖关系
         service_a: "service:a"
```

使用 `additional_contexts` 属性，您可以引用由另一个服务构建的镜像，而无需显式为其命名：

b.Dockerfile:

```dockerfile

FROM base_image  
# `base_image` 不会解析为实际镜像。它用于指向具名附加上下文

# 构建 service b
```

Compose 文件：

```yaml
services:
  a:
     build: 
       dockerfile: a.Dockerfile
       # 构建的镜像将被标记为 <project_name>_a
  b:
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM base_image` 将解析为对必须首先构建的服务 "a" 的依赖关系
         base_image: "service:a"
```

## 使用 Bake 构建

使用 [Bake](/manuals/build/bake/_index.md) 可以让您传递所有服务的完整构建定义，并以最有效的方式编排构建执行。

要启用此功能，请在运行 Compose 时在环境中设置 `COMPOSE_BAKE=true` 变量。

```console
$ COMPOSE_BAKE=true docker compose build
[+] Building 0.0s (0/1)                                                         
 => [internal] load local bake definitions                                 0.0s
...
[+] Building 2/2 manifest list sha256:4bd2e88a262a02ddef525c381a5bdb08c83  0.0s
 ✔ service_b  Built                                                        0.7s 
 ✔ service_a  Built    
```

也可以通过编辑 `$HOME/.docker/config.json` 配置文件，将 Bake 选为默认构建器：
```json
{
  ...
  "plugins": {
    "compose": {
      "build": "bake"
    }
  }
  ...
}
```

## 其他资源

- [Docker Compose 构建参考](/reference/cli/docker/compose/build.md)
- [了解多阶段 Dockerfile](/manuals/build/building/multi-stage.md)
