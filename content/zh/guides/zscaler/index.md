---
title: 在 Zscaler 环境中使用 Docker
tags: [networking, admin]
summary: |
  本指南介绍如何将 Zscaler 的根证书嵌入 Docker 镜像，使容器能够安全地与 Zscaler 代理配合工作，避免 SSL 错误。
params:
  time: 10 分钟
---

在许多企业环境中，网络流量会通过 HTTPS 代理（如 Zscaler）进行拦截和监控。虽然 Zscaler 确保了安全合规性和网络控制，但它可能会给使用 Docker 的开发者带来问题，特别是在构建过程中可能出现 SSL 证书验证错误。本指南概述了如何配置 Docker 容器和构建以正确处理 Zscaler 的自定义证书，确保在受监控环境中顺利运行。

## 证书在 Docker 中的作用

当 Docker 构建或运行容器时，它经常需要从互联网获取资源——无论是从注册表拉取基础镜像、下载依赖项，还是与外部服务通信。在代理环境中，Zscaler 会拦截 HTTPS 流量并将远程服务器的证书替换为自己的证书。然而，Docker 默认不信任这个 Zscaler 证书，导致 SSL 错误。

```plaintext
x509: certificate signed by unknown authority
```

这些错误的发生是因为 Docker 无法验证 Zscaler 提供的证书的有效性。为避免此问题，您必须配置 Docker 以信任 Zscaler 的证书。

## 为 Docker Desktop 配置 Zscaler 代理

根据 Zscaler 的部署方式，您可能需要手动配置 Docker Desktop 代理设置以使用 Zscaler 代理。

如果您通过 [Zscaler Client Connector](https://help.zscaler.com/zscaler-client-connector/what-is-zscaler-client-connector) 将 Zscaler 用作系统级代理，设备上的所有流量都会自动通过 Zscaler 路由，因此 Docker Desktop 会自动使用 Zscaler 代理，无需额外配置。

如果您未将 Zscaler 用作系统级代理，请在 Docker Desktop 中手动配置代理设置。可以使用[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)为组织中的所有客户端设置代理设置，或在 Docker Desktop GUI 中的[**设置 > 资源 > 代理**](/manuals/desktop/settings-and-maintenance/settings.md#proxies)下编辑代理配置。

## 在 Docker 镜像中安装根证书

要使容器能够使用和信任 Zscaler 代理，需要将证书嵌入镜像并配置镜像的信任存储。在镜像构建时安装证书是首选方法，因为它消除了启动时配置的需要，并提供了可审计、一致的环境。

### 获取根证书

获取根证书最简单的方法是从管理员已安装证书的机器上导出。您可以使用 Web 浏览器或系统的证书管理服务（例如 Windows 证书存储）。

#### 示例：使用 Google Chrome 导出证书

1. 在 Google Chrome 中，导航到 `chrome://certificate-manager/`。
2. 在**本地证书**下，选择**查看导入的证书**。
3. 找到 Zscaler 根证书，通常标记为 **Zscaler Root CA**。
4. 打开证书详情并选择**导出**。
5. 以 ASCII PEM 格式保存证书。
6. 在文本编辑器中打开导出的文件，确认它包含 `-----BEGIN CERTIFICATE-----` 和 `-----END CERTIFICATE-----`。

获取证书后，将其存储在可访问的仓库中，如 JFrog Artifactory 或 Git 仓库。或者使用通用存储，如 AWS S3。

### 使用证书进行构建

要在构建镜像时安装这些证书，请将证书复制到构建容器中并更新信任存储。示例 Dockerfile 如下所示：

```dockerfile
FROM debian:bookworm
COPY zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
```

这里，`zscaler-root-ca.crt` 是根证书，位于构建上下文的根目录（通常在应用程序的 Git 仓库中）。

如果您使用制品仓库，可以使用 `ADD` 指令直接获取证书。您还可以使用 `--checksum` 标志来验证证书的内容摘要是否正确。

```dockerfile
FROM debian:bookworm
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d \
    https://artifacts.example/certs/zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
```

#### 使用多阶段构建

对于需要在最终运行时镜像中使用证书的多阶段构建，请确保在最终阶段进行证书安装。

```dockerfile
FROM debian:bookworm AS build
WORKDIR /build
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git
RUN --mount=target=. cmake -B output/

FROM debian:bookworm-slim AS final
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d \
    https://artifacts.example/certs/zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
WORKDIR /app
COPY --from=build /build/output/bin .
ENTRYPOINT ["/app/bin"]
```

## 结论

将 Zscaler 根证书直接嵌入 Docker 镜像可确保容器在 Zscaler 代理环境中顺利运行。通过使用这种方法，您可以减少潜在的运行时错误，并创建一致、可审计的配置，使 Docker 在受监控网络中平稳运行。
