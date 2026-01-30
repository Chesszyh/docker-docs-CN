---
description: 使用内容信托自动化推送和拉取镜像
keywords: trust, security, docker, documentation, automation, 信任, 安全, 自动化
title: 内容信托自动化
---

将 Docker 内容信托集成到现有的自动化系统中非常常见。为了允许工具封装 Docker 并推送受信任的内容，可以通过环境变量将相关信息传递给客户端。

本指南遵循 [使用 Docker 内容信托签署镜像](index.md#signing-images-with-docker-content-trust) 中描述的步骤。请确保您已理解并遵循相关前提条件。

当直接使用 Notary 客户端时，它使用其 [自己的一组环境变量](https://github.com/theupdateframework/notary/blob/master/docs/reference/client-config.md#environment-variables-optional)。

## 添加授权私钥

要自动化将授权私钥导入本地 Docker 信任库，我们需要为新密钥提供一个密码。每次使用该授权签署标签时，都需要此密码。

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust key load delegation.key --name jeff
Loading key from "delegation.key"...
Successfully imported key from delegation.key
```

## 添加授权公钥

如果在添加授权公钥的同时初始化仓库，则需要使用本地 Notary 规范根密钥的密码来创建仓库的信任数据。如果仓库已经初始化，则只需要仓库密码。

```console
# 如果需要，导出本地根密钥密码。
$ export DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE="rootpassphrase123"

# 导出仓库密码
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="repopassphrase123"

# 初始化仓库并推送授权
$ docker trust signer add --key delegation.crt jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Initializing signed repository for registry.example.com/admin/demo...
Successfully initialized "registry.example.com/admin/demo"
Successfully added signer: registry.example.com/admin/demo
```

## 签署镜像

最后，在签署镜像时，我们需要导出签名密钥的密码。该密码是在使用 `$ docker trust key load` 将密钥加载到本地 Docker 信任库时创建的。

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust sign registry.example.com/admin/demo:1
Signing and pushing trust data for local image registry.example.com/admin/demo:1, may overwrite remote trust data
The push refers to repository [registry.example.com/admin/demo]
428c97da766c: Layer already exists
2: digest: sha256:1a6fd470b9ce10849be79e99529a88371dff60c60aab424c077007f6979b4812 size: 524
Signing and pushing trust metadata
Successfully signed registry.example.com/admin/demo:1
```

## 使用内容信托进行构建

您也可以在启用内容信托的情况下进行构建。在运行 `docker build` 命令之前，您应该手动或通过脚本设置环境变量 `DOCKER_CONTENT_TRUST`。考虑下面的简单 Dockerfile。

```dockerfile
# syntax=docker/dockerfile:1
FROM docker/trusttest:latest
RUN echo
```

`FROM` 标签正在拉取一个已签署的镜像。您不能构建一个 `FROM` 镜像既不存在于本地也未经过签署的镜像。鉴于标签 `latest` 存在内容信托数据，以下构建应该会成功：

```console
$  docker build -t docker/trusttest:testing .
Using default tag: latest
latest: Pulling from docker/trusttest

b3dbab3810fc: Pull complete
a9539b34a6ab: Pull complete
Digest: sha256:d149ab53f871
```

如果启用了内容信托，而从依赖于没有信任数据标签的 Dockerfile 构建，会导致构建命令失败：

```console
$  docker build -t docker/trusttest:testing .
unable to process Dockerfile: No trust data for notrust
```

## 相关信息

* [内容信托的授权](trust_delegation.md)
* [Docker 中的内容信托](index.md)
* [管理内容信托密钥](trust_key_mng.md)
* [在内容信托沙箱中实践](trust_sandbox.md)
