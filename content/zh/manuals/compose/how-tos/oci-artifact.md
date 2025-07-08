---
title: 将 Docker Compose 应用程序打包并部署为 OCI 工件
linkTitle: OCI 工件应用程序
weight: 110
description: 了解如何从符合 OCI 的注册表中打包、发布和安全地运行 Docker Compose 应用程序。
keywords: cli, compose, oci, docker hub, artificats, publish, package, distribute, docker compose oci support, OCI, 工件, 发布, 打包, 分发
params:
  sidebar:
    badge:
      color: green
      text: New
---

{{< summary-bar feature_name="Compose OCI artifact" >}}

Docker Compose 支持使用 [OCI 工件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)，允许您通过容器注册表打包和分发您的 Compose 应用程序。这意味着您可以将 Compose 文件与容器镜像一起存储，从而更轻松地对多容器应用程序进行版本控制、共享和部署。

## 将您的 Compose 应用程序发布为 OCI 工件

要将您的 Compose 应用程序作为 OCI 工件分发，您可以使用 `docker compose publish` 命令将其发布到符合 OCI 的注册表。
这允许其他人直接从注册表部署您的应用程序。

发布功能支持 Compose 的大多数组合功能，例如覆盖、扩展或包含，但有[一些限制](#limitations)���

### 一般步骤

1. 导航到您的 Compose 应用程序的目录。
   确保您位于包含 `compose.yml` 文件的目录中，或者您正在使用 `-f` 标志指定您的 Compose 文件。

2. 在您的终端中，登录到您的 Docker 帐户，以便您通过 Docker Hub 进行身份验证。

   ```console
   $ docker login
   ```

3. 使用 `docker compose publish` 命令将您的应用程序作为 OCI 工件推送：

   ```console
   $ docker compose publish username/my-compose-app:latest
   ```
   如果您有多个 Compose 文件，请运行：

   ```console
   $ docker compose -f compose-base.yml -f compose-production.yml publish username/my-compose-app:latest
   ```

### 高级发布选项

发布时，您可以传递其他选项：
- `--oci-version`：指定 OCI 版本（默认为自动确定）。
- `--resolve-image-digests`：将镜像标签固定到摘要。
- `--with-env`：在已发布的 OCI 工件中包含环境变量。

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

如果您拒绝，发布过程将停止，不会向注册表发送任何内容。

## 限制

将 Compose 应用程序作为 OCI 工件发布存在限制。您无法发布具有以下特征的 Compose 配置：
- 包含绑定挂载的服务
- 仅包含 `build` 部分的服务
- 使用 `include` 属性包含本地文件。要成功发布，请确保任何包含的本地文件也已发布。然后，您可以使用 `include` 将这些文件引用为远程 `include`，因为支持远程 `include`。

## 启动 OCI 工件应用程序

要启动使用 OCI 工件的 Docker Compose 应用程序，您可以使用 `-f`（或 `--file`）标志，后跟 OCI 工件引用。这允许您指定存储在注册表中的 OCI 工件中的 Compose 文件。

`oci://` 前���表示应从符合 OCI 的注册表中拉取 Compose 文件，而不是从本地文件系统加载。

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

然后，要运行 Compose 应用程序，请使用 `docker compose up` 命令，并将 `-f` 标志指向您的 OCI 工件：

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

### 故障排除

当您从 OCI 工件运行应用程序时，Compose 可能会显示警告消息，要求您确认以下内容，以限制运行恶意应用程序的风险：

- 使用的插值变量及其值的列表
- 应用程序使用的所有环境变量的列表
- 如果您的 OCI 工件应用程序正在使用其他远程资源，例如通过 [`include`](/reference/compose-file/include/)。

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

如果您同意启动应用程序，Compose 会显示已从 OCI 工件下载所有资源的目录：

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

- [了解 Docker Hub 中的 OCI 工件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)
- [Compose publish 命令](/reference/cli/docker/compose/publish.md)
- [了解 `include`](/reference/compose-file/include.md)
