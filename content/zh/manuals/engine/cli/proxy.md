---
title: 在 Docker CLI 中使用代理服务器
linkTitle: 代理配置
weight: 20
description: 如何配置 Docker 客户端 CLI 以使用代理服务器
keywords: network, networking, proxy, client, 网络, 代理, 客户端
---

本页介绍了如何配置 Docker CLI，通过容器中的环境变量来使用代理。

本页不介绍如何为 Docker Desktop 配置代理。相关说明请参阅 [配置 Docker Desktop 使用 HTTP/HTTPS 代理](/manuals/desktop/settings-and-maintenance/settings.md#proxies)。

如果您是在没有 Docker Desktop 的情况下运行 Docker Engine，请参考 [配置 Docker 守护进程使用代理](/manuals/engine/daemon/proxy.md)，了解如何为 Docker 守护进程 (`dockerd`) 本身配置代理服务器。

如果您的容器需要使用 HTTP、HTTPS 或 FTP 代理服务器，您可以通过不同方式进行配置：

- [配置 Docker 客户端](#configure-the-docker-client)
- [使用 CLI 设置代理](#set-proxy-using-the-cli)

> [!NOTE]
> 
> 遗憾的是，目前还没有定义 Web 客户端应如何处理代理环境变量的标准，也没有定义它们的格式。
> 
> 如果您对这些变量的历史感兴趣，可以查看 GitLab 团队关于该主题的博文：[我们需要谈谈：能否标准化 NO_PROXY？](https://about.gitlab.com/blog/2021/01/27/we-need-to-talk-no-proxy/)。

## 配置 Docker 客户端

您可以使用位于 `~/.docker/config.json` 的 JSON 配置文件为 Docker 客户端添加代理配置。构建和容器将使用此文件中指定的配置。

```json
{
 "proxies": {
   "default": {
     "httpProxy": "http://proxy.example.com:3128",
     "httpsProxy": "https://proxy.example.com:3129",
     "noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
   }
 }
}
```

> [!WARNING]
> 
> 代理设置可能包含敏感信息。例如，某些代理服务器要求在其 URL 中包含身份验证信息，或者其地址可能会暴露您公司环境的 IP 地址或主机名。
> 
> 环境变量以明文形式存储在容器的配置中，因此可以通过远程 API 进行检查，或者在使用 `docker commit` 时提交到镜像中。

保存文件后配置立即生效，无需重启 Docker。但是，配置仅适用于新的容器和构建，不会影响现有容器。

下表描述了可用的配置参数。

| 属性         | 描述                                                                         |
| :----------- | :---------------------------------------------------------------------------------- |
| `httpProxy`  | 设置 `HTTP_PROXY` 和 `http_proxy` 环境变量及构建参数。   |
| `httpsProxy` | 设置 `HTTPS_PROXY` 和 `https_proxy` 环境变量及构建参数。 |
| `ftpProxy`   | 设置 `FTP_PROXY` 和 `ftp_proxy` 环境变量及构建参数。     |
| `noProxy`    | 设置 `NO_PROXY` 和 `no_proxy` 环境变量及构建参数。       |
| `allProxy`   | 设置 `ALL_PROXY` 和 `all_proxy` 环境变量及构建参数。     |

这些设置仅用于配置容器的代理环境变量，不作为 Docker CLI 或 Docker Engine 本身的代理设置。 
参考 [环境变量](/reference/cli/docker/#environment-variables) 和 [配置 Docker 守护进程使用代理服务器](/manuals/engine/daemon/proxy.md) 章节，了解如何为 CLI 和守护进程配置代理设置。

### 使用代理配置运行容器

当您启动容器时，其与代理相关的环境变量会被设置为反映 `~/.docker/config.json` 中的代理配置。

例如，假设代理配置如 [前一节](#configure-the-docker-client) 所示，您运行的容器的环境变量将设置如下：

```console
$ docker run --rm alpine sh -c 'env | grep -i  _PROXY'
https_proxy=http://proxy.example.com:3129
HTTPS_PROXY=http://proxy.example.com:3129
http_proxy=http://proxy.example.com:3128
HTTP_PROXY=http://proxy.example.com:3128
no_proxy=*.test.example.com,.example.org,127.0.0.0/8
NO_PROXY=*.test.example.com,.example.org,127.0.0.0/8
```

### 使用代理配置进行构建

当您调用构建时，与代理相关的构建参数会根据 Docker 客户端配置文件中的代理设置自动预填充。

假设代理配置如 [前一节](#configure-the-docker-client) 所示，构建期间的环境变量设置如下：

```console
$ docker build \
  --no-cache \
  --progress=plain \
  - <<EOF
FROM alpine
RUN env | grep -i _PROXY
EOF
```

```console
#5 [2/2] RUN env | grep -i _PROXY
#5 0.100 HTTPS_PROXY=https://proxy.example.com:3129
#5 0.100 no_proxy=*.test.example.com,.example.org,127.0.0.0/8
#5 0.100 NO_PROXY=*.test.example.com,.example.org,127.0.0.0/8
#5 0.100 https_proxy=https://proxy.example.com:3129
#5 0.100 http_proxy=http://proxy.example.com:3128
#5 0.100 HTTP_PROXY=http://proxy.example.com:3128
#5 DONE 0.1s
```

### 为每个守护进程配置代理设置

`~/.docker/config.json` 中 `proxies` 下的 `default` 键配置了客户端连接的所有守护进程的代理设置。要为单个守护进程配置代理，请使用守护进程的地址代替 `default` 键。

以下示例配置了默认代理配置，并为地址为 `tcp://docker-daemon1.example.com` 的 Docker 守护进程配置了 no-proxy 覆盖：

```json
{
 "proxies": {
   "default": {
     "httpProxy": "http://proxy.example.com:3128",
     "httpsProxy": "https://proxy.example.com:3129",
     "noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
   },
   "tcp://docker-daemon1.example.com": {
     "noProxy": "*.internal.example.net"
   }
 }
}
```

## 使用 CLI 设置代理

除了 [配置 Docker 客户端](#configure-the-docker-client) 之外，您还可以在调用 `docker build` 和 `docker run` 命令时在命令行中指定代理配置。

命令行上的代理配置对构建使用 `--build-arg` 标志，对需要带代理运行容器的情况使用 `--env` 标志。

```console
$ docker build --build-arg HTTP_PROXY="http://proxy.example.com:3128" .
$ docker run --env HTTP_PROXY="http://proxy.example.com:3128" redis
```

有关可用于 `docker build` 命令的所有代理相关构建参数的列表，请参阅 [预定义参数 (Predefined ARGs)](/reference/dockerfile.md#predefined-args)。这些代理值仅在构建容器中可用，不会包含在构建输出中。

## 构建时的代理环境变量

不要使用 `ENV` Dockerfile 指令来指定构建的代理设置。应改用构建参数 (build arguments)。

为代理使用环境变量会将配置嵌入到镜像中。如果该代理是内部代理，那么从该镜像创建的容器可能无法访问它。

在镜像中嵌入代理设置还存在安全风险，因为这些值可能包含敏感信息。
