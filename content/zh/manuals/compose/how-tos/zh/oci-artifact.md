---
title: 将 Docker Compose 应用程序打包并部署为 OCI 制品
linkTitle: OCI 制品应用程序
weight: 110
description: 了解如何从符合 OCI 标准的镜像仓库打包、发布和安全运行 Docker Compose 应用程序。
keywords: cli, compose, oci, docker hub, artificats, publish, package, distribute, docker compose oci support
params:
  sidebar:
    badge:
      color: green
      text: New
---

{{< summary-bar feature_name="Compose OCI artifact" >}}

Docker Compose 支持使用 [OCI 制品（OCI artifacts）](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)，允许您通过容器镜像仓库打包和分发 Compose 应用程序。这意味着您可以将 Compose 文件与容器镜像一起存储，从而更容易对多容器应用程序进行版本控制、共享和部署。

## 将您的 Compose 应用程序发布为 OCI 制品

要将您的 Compose 应用程序作为 OCI 制品分发，您可以使用 `docker compose publish` 命令将其发布到符合 OCI 标准的镜像仓库。这允许其他人直接从镜像仓库部署您的应用程序。

发布功能支持 Compose 的大多数组合功能，如 overrides、extends 或 include，[但有一些限制](#limitations)。

### 一般步骤

1. 导航到您的 Compose 应用程序目录。
   确保您位于包含 `compose.yml` 文件的目录中，或者使用 `-f` 标志指定 Compose 文件。

2. 在终端中，登录到您的 Docker 账户以便与 Docker Hub 进行身份验证。

   ```console
   $ docker login
   ```

3. 使用 `docker compose publish` 命令将您的应用程序作为 OCI 制品推送：

   ```console
   $ docker compose publish username/my-compose-app:latest
   ```
   如果您有多个 Compose 文件，请运行：

   ```console
   $ docker compose -f compose-base.yml -f compose-production.yml publish username/my-compose-app:latest
   ```

### 高级发布选项

发布时，您可以传递其他选项：
- `--oci-version`：指定 OCI 版本（默认自动确定）。
- `--resolve-image-digests`：将镜像标签固定为摘要。
- `--with-env`：在发布的 OCI 制品中包含环境变量。

Compose 会检查以确保您的配置中没有任何敏感数据，并显示您的环境变量以确认您要发布它们。

```text
...
you are about to publish sensitive data within your OCI artifact.
please double check that you are not leaking sensitive data
AWS Client ID
"services.serviceA.environment.AWS_ACCESS_KEY_ID": xxxxxxxxxx
AWS Secret Key
"services.serviceA.environment.AWS_SECRET_ACCESS_KEY": aws"xxxx/xxxx+xxxx+"
Github authentication
"GITHUB_TOKEN": ghp_xxxxxxxxxx
JSON Web Token
"": xxxxxxx.xxxxxxxx.xxxxxxxx
Private Key
"": -----BEGIN DSA PRIVATE KEY-----
xxxxx
-----END DSA PRIVATE KEY-----
Are you ok to publish these sensitive data? [y/N]:y

you are about to publish environment variables within your OCI artifact.
please double check that you are not leaking sensitive data
Service/Config  serviceA
FOO=bar
Service/Config  serviceB
FOO=bar
QUIX=
BAR=baz
Are you ok to publish these environment variables? [y/N]:
```

如果您拒绝，发布过程将停止，不会向镜像仓库发送任何内容。

## 限制

将 Compose 应用程序发布为 OCI 制品存在一些限制。您不能发布以下 Compose 配置：
- 包含绑定挂载的服务
- 仅包含 `build` 部分的服务
- 使用 `include` 属性包含本地文件的配置。要成功发布，请确保任何包含的本地文件也已发布。然后您可以使用 `include` 来引用这些文件，因为支持远程 `include`。

## 启动 OCI 制品应用程序

要启动使用 OCI 制品的 Docker Compose 应用程序，您可以使用 `-f`（或 `--file`）标志后跟 OCI 制品引用。这允许您指定存储在镜像仓库中作为 OCI 制品的 Compose 文件。

`oci://` 前缀表示 Compose 文件应从符合 OCI 标准的镜像仓库拉取，而不是从本地文件系统加载。

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

然后要运行 Compose 应用程序，使用带有 `-f` 标志指向您的 OCI 制品的 `docker compose up` 命令：

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

### 故障排除

当您从 OCI 制品运行应用程序时，Compose 可能会显示警告消息，要求您确认以下内容以限制运行恶意应用程序的风险：

- 使用的插值变量列表及其值
- 应用程序使用的所有环境变量列表
- 如果您的 OCI 制品应用程序正在使用其他远程资源，例如通过 [`include`](/reference/compose-file/include/)。

```text
$ REGISTRY=myregistry.com docker compose -f oci://docker.io/username/my-compose-app:latest up

Found the following variables in configuration:
VARIABLE     VALUE                SOURCE        REQUIRED    DEFAULT
REGISTRY     myregistry.com      command-line   yes
TAG          v1.0                environment    no          latest
DOCKERFILE   Dockerfile          default        no          Dockerfile
API_KEY      <unset>             none           no

Do you want to proceed with these variables? [Y/n]:y

Warning: This Compose project includes files from remote sources:
- oci://registry.example.com/stack:latest
Remote includes could potentially be malicious. Make sure you trust the source.
Do you want to continue? [y/N]:
```

如果您同意启动应用程序，Compose 会显示 OCI 制品中所有资源下载到的目录：

```text
...
Do you want to continue? [y/N]: y

Your compose stack "oci://registry.example.com/stack:latest" is stored in "~/Library/Caches/docker-compose/964e715660d6f6c3b384e05e7338613795f7dcd3613890cfa57e3540353b9d6d"
```

`docker compose publish` 命令支持非交互式执行，允许您通过包含 `-y`（或 `--yes`）标志来跳过确认提示：

```console
$ docker compose publish -y username/my-compose-app:latest
```

## 后续步骤

- [了解 Docker Hub 中的 OCI 制品](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)
- [Compose publish 命令](/reference/cli/docker/compose/publish.md)
- [理解 `include`](/reference/compose-file/include.md)
