---
title: 配置 BuildKit
description: 了解如何为您的构建器配置 BuildKit。
keywords: build, buildkit, configuration, buildx, network, cni, registry
---

如果您使用 Buildx 创建 `docker-container` 或 `kubernetes` 构建器，可以
通过向 `docker buildx create` 命令传递
[`--config` 标志](/reference/cli/docker/buildx/create.md#config)
来应用自定义 [BuildKit 配置](toml-configuration.md)。

## 仓库镜像

您可以为构建定义要使用的仓库镜像。这样做会重定向
BuildKit 从不同的主机名拉取镜像。以下步骤演示了
为 `docker.io`（Docker Hub）定义镜像到 `mirror.gcr.io`。

1. 在 `/etc/buildkitd.toml` 创建一个 TOML 文件，内容如下：

   ```toml
   debug = true
   [registry."docker.io"]
     mirrors = ["mirror.gcr.io"]
   ```

   > [!NOTE]
   >
   > `debug = true` 在 BuildKit 守护进程中开启调试请求，当使用镜像时
   > 会记录一条消息。

2. 创建使用此 BuildKit 配置的 `docker-container` 构建器：

   ```console
   $ docker buildx create --use --bootstrap \
     --name mybuilder \
     --driver docker-container \
     --config /etc/buildkitd.toml
   ```

3. 构建镜像：

   ```bash
   docker buildx build --load . -f - <<EOF
   FROM alpine
   RUN echo "hello world"
   EOF
   ```

此构建器的 BuildKit 日志现在显示它使用了 GCR 镜像。您
可以通过响应消息包含 `x-goog-*` HTTP 头来判断。

```console
$ docker logs buildx_buildkit_mybuilder0
```

```text
...
time="2022-02-06T17:47:48Z" level=debug msg="do request" request.header.accept="application/vnd.docker.container.image.v1+json, */*" request.header.user-agent=containerd/1.5.8+unknown request.method=GET spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=1356 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=1469 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:25:17 GMT" response.header.etag="\"774380abda8f4eae9a149e5d5d3efc83\"" response.header.expires="Sun, 06 Feb 2022 18:25:17 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:57 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788077652182 response.header.x-goog-hash="crc32c=V3DSrg==" response.header.x-goog-hash.1="md5=d0OAq9qPTq6aFJ5dXT78gw==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=1469 response.header.x-guploader-uploadid=ADPycduqQipVAXc3tzXmTzKQ2gTT6CV736B2J628smtD1iDytEyiYCgvvdD8zz9BT1J1sASUq9pW_ctUyC4B-v2jvhIxnZTlKg response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=760 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=1471 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:35:13 GMT" response.header.etag="\"35d688bd15327daafcdb4d4395e616a8\"" response.header.expires="Sun, 06 Feb 2022 18:35:13 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:12 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788032100793 response.header.x-goog-hash="crc32c=aWgRjA==" response.header.x-goog-hash.1="md5=NdaIvRUyfar8201DleYWqA==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=1471 response.header.x-guploader-uploadid=ADPycdtR-gJYwC7yHquIkJWFFG8FovDySvtmRnZBqlO3yVDanBXh_VqKYt400yhuf0XbQ3ZMB9IZV2vlcyHezn_Pu3a1SMMtiw response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="do request" request.header.accept="application/vnd.docker.image.rootfs.diff.tar.gzip, */*" request.header.user-agent=containerd/1.5.8+unknown request.method=GET spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=1356 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=2818413 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:25:17 GMT" response.header.etag="\"1d55e7be5a77c4a908ad11bc33ebea1c\"" response.header.expires="Sun, 06 Feb 2022 18:25:17 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:06 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788026431708 response.header.x-goog-hash="crc32c=ZojF+g==" response.header.x-goog-hash.1="md5=HVXnvlp3xKkIrRG8M+vqHA==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=2818413 response.header.x-guploader-uploadid=ADPycdsebqxiTBJqZ0bv9zBigjFxgQydD2ESZSkKchpE0ILlN9Ibko3C5r4fJTJ4UR9ddp-UBd-2v_4eRpZ8Yo2llW_j4k8WhQ response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
...
```

## 设置仓库证书

如果您在 BuildKit 配置中指定仓库证书，守护进程
会将文件复制到容器的 `/etc/buildkit/certs` 目录下。以下
步骤展示了如何将自签名仓库证书添加到 BuildKit
配置。

1. 将以下配置添加到 `/etc/buildkitd.toml`：

   ```toml
   # /etc/buildkitd.toml
   debug = true
   [registry."myregistry.com"]
     ca=["/etc/certs/myregistry.pem"]
     [[registry."myregistry.com".keypair]]
       key="/etc/certs/myregistry_key.pem"
       cert="/etc/certs/myregistry_cert.pem"
   ```

   这告诉构建器使用指定位置（`/etc/certs`）的证书
   将镜像推送到 `myregistry.com` 仓库。

2. 创建使用此配置的 `docker-container` 构建器：

   ```console
   $ docker buildx create --use --bootstrap \
     --name mybuilder \
     --driver docker-container \
     --config /etc/buildkitd.toml
   ```

3. 检查构建器的配置文件（`/etc/buildkit/buildkitd.toml`），它
   显示证书配置现已在构建器中配置。

   ```console
   $ docker exec -it buildx_buildkit_mybuilder0 cat /etc/buildkit/buildkitd.toml
   ```

   ```toml
   debug = true

   [registry]

     [registry."myregistry.com"]
       ca = ["/etc/buildkit/certs/myregistry.com/myregistry.pem"]

       [[registry."myregistry.com".keypair]]
         cert = "/etc/buildkit/certs/myregistry.com/myregistry_cert.pem"
         key = "/etc/buildkit/certs/myregistry.com/myregistry_key.pem"
   ```

4. 验证证书在容器内：

   ```console
   $ docker exec -it buildx_buildkit_mybuilder0 ls /etc/buildkit/certs/myregistry.com/
   myregistry.pem    myregistry_cert.pem   myregistry_key.pem
   ```

现在您可以使用此构建器推送到仓库，它将使用证书进行认证：

```console
$ docker buildx build --push --tag myregistry.com/myimage:latest .
```

## CNI 网络

构建器的 CNI 网络对于处理并发构建期间的网络端口
争用非常有用。CNI 在默认的 BuildKit 镜像中[尚不可用](https://github.com/moby/buildkit/issues/28)。但您可以创建自己的包含
CNI 支持的镜像。

以下 Dockerfile 示例展示了具有 CNI 支持的自定义 BuildKit 镜像。
它使用 BuildKit 中[用于集成测试的 CNI 配置](https://github.com/moby/buildkit/blob/master//hack/fixtures/cni.json)
作为示例。您可以随意包含自己的 CNI 配置。

```dockerfile
# syntax=docker/dockerfile:1

ARG BUILDKIT_VERSION=v{{% param "buildkit_version" %}}
ARG CNI_VERSION=v1.0.1

FROM --platform=$BUILDPLATFORM alpine AS cni-plugins
RUN apk add --no-cache curl
ARG CNI_VERSION
ARG TARGETOS
ARG TARGETARCH
WORKDIR /opt/cni/bin
RUN curl -Ls https://github.com/containernetworking/plugins/releases/download/$CNI_VERSION/cni-plugins-$TARGETOS-$TARGETARCH-$CNI_VERSION.tgz | tar xzv

FROM moby/buildkit:${BUILDKIT_VERSION}
ARG BUILDKIT_VERSION
RUN apk add --no-cache iptables
COPY --from=cni-plugins /opt/cni/bin /opt/cni/bin
ADD https://raw.githubusercontent.com/moby/buildkit/${BUILDKIT_VERSION}/hack/fixtures/cni.json /etc/buildkit/cni.json
```

现在您可以构建此镜像，并使用
[`--driver-opt image` 选项](/reference/cli/docker/buildx/create.md#driver-opt)从它创建构建器实例：

```console
$ docker buildx build --tag buildkit-cni:local --load .
$ docker buildx create --use --bootstrap \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "image=buildkit-cni:local" \
  --buildkitd-flags "--oci-worker-net=cni"
```

## 资源限制

### 最大并行度

您可以限制 BuildKit 求解器的并行度，这对于
低功耗机器特别有用，可以在创建构建器时使用 [BuildKit 配置](toml-configuration.md)
配合 [`--config` 标志](/reference/cli/docker/buildx/create.md#config)。

```toml
# /etc/buildkitd.toml
[worker.oci]
  max-parallelism = 4
```

现在您可以[创建 `docker-container` 构建器](/manuals/build/builders/drivers/docker-container.md)，
它将使用此 BuildKit 配置来限制并行度。

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --config /etc/buildkitd.toml
```

### TCP 连接限制

每个仓库的 TCP 连接限制为 4 个同时连接用于
拉取和推送镜像，外加一个专用于元数据
请求的额外连接。此连接限制可防止您的构建在
拉取镜像时卡住。专用的元数据连接有助于减少整体构建
时间。

更多信息：[moby/buildkit#2259](https://github.com/moby/buildkit/pull/2259)
