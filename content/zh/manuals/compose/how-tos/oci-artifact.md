---
title: 将 Docker Compose 应用程序作为 OCI 构件进行打包和部署
linkTitle: OCI 构件应用程序
weight: 110
description: 了解如何通过符合 OCI 标准的镜像库打包、发布并安全地运行 Docker Compose 应用程序。
keywords: cli, compose, oci, docker hub, 构件, 发布, 打包, 分发, docker compose oci 支持
params:
  sidebar:
    badge:
      color: green
      text: 新增
---

{{< summary-bar feature_name="Compose OCI 构件" >}}

Docker Compose 支持使用 [OCI 构件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)，允许您通过容器镜像库打包和分发您的 Compose 应用程序。这意味着您可以将 Compose 文件与容器镜像一起存储，从而更轻松地对多容器应用程序进行版本控制、共享和部署。

## 将您的 Compose 应用程序作为 OCI 构件发布

要将您的 Compose 应用程序作为 OCI 构件分发，您可以使用 `docker compose publish` 命令将其发布到符合 OCI 标准的镜像库。这样其他人就可以直接从镜像库部署您的应用程序。

发布功能支持 Compose 的大多数组合功能，如 overrides（覆盖）、extends（继承）或 include（包含），但存在 [一些限制](#局限性)。

### 基本步骤

1. 导航到您的 Compose 应用程序目录。确保您位于包含 `compose.yml` 文件的目录中，或者您正在使用 `-f` 标志指定您的 Compose 文件。

2. 在终端中登录您的 Docker 账户，以便通过 Docker Hub 的身份验证。

   ```console
   $ docker login
   ```

3. 使用 `docker compose publish` 命令将您的应用程序作为 OCI 构件推送：

   ```console
   $ docker compose publish username/my-compose-app:latest
   ```
   如果您有多个 Compose 文件，请运行：

   ```console
   $ docker compose -f compose-base.yml -f compose-production.yml publish username/my-compose-app:latest
   ```

### 高级发布选项

发布时，您可以传递额外的选项： 
- `--oci-version`：指定 OCI 版本（默认自动确定）。
- `--resolve-image-digests`：将镜像标签固定为摘要（digests）。
- `--with-env`：在发布的 OCI 构件中包含环境变量。

Compose 会检查并确保您的配置中没有敏感数据，并显示您的环境变量以确认您是否要发布它们。

```text
...
您即将发布 OCI 构件中的敏感数据。
请仔细核对，确保没有泄露敏感数据
AWS Client ID
"services.serviceA.environment.AWS_ACCESS_KEY_ID": xxxxxxxxxx
AWS Secret Key
"services.serviceA.environment.AWS_SECRET_ACCESS_KEY": aws"xxxx/xxxx+xxxx+"
Github 身份验证
"GITHUB_TOKEN": ghp_xxxxxxxxxx
JSON Web Token
"": xxxxxxx.xxxxxxxx.xxxxxxxx
私钥
"": -----BEGIN DSA PRIVATE KEY-----
xxxxx
-----END DSA PRIVATE KEY-----
您确定要发布这些敏感数据吗？ [y/N]:y

您即将发布 OCI 构件中的环境变量。
请仔细核对，确保没有泄露敏感数据
Service/Config  serviceA
FOO=bar
Service/Config  serviceB
FOO=bar
QUIX=
BAR=baz
您确定要发布这些环境变量吗？ [y/N]: 
```

如果您拒绝，发布过程将停止，不会向镜像库发送任何内容。

## 局限性

将 Compose 应用程序作为 OCI 构件发布存在一些限制。您不能发布以下 Compose 配置：
- 服务包含绑定挂载（bind mounts）
- 服务仅包含 `build` 部分
- 包含使用 `include` 属性引入的本地文件。要成功发布，请确保所有包含的本地文件也已发布。由于支持远程 `include`，随后您可以使用 `include` 来引用这些文件。

## 启动 OCI 构件应用程序

要启动使用 OCI 构件的 Docker Compose 应用程序，您可以使用 `-f`（或 `--file`）标志，后接 OCI 构件引用。这允许您指定存储在镜像库中作为 OCI 构件的 Compose 文件。

`oci://` 前缀表示应从符合 OCI 标准的镜像库拉取 Compose 文件，而不是从本地文件系统加载。

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

然后，使用 `docker compose up` 命令运行该 Compose 应用程序，并使用 `-f` 标志指向您的 OCI 构件：

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

### 故障排除

当您从 OCI 构件运行应用程序时，Compose 可能会显示警告消息，要求您确认以下内容，以限制运行恶意应用程序的风险：

- 所使用的插值变量及其值的列表
- 应用程序所使用的所有环境变量列表
- 您的 OCI 构件应用程序是否正在使用其他远程资源，例如通过 [`include`](/reference/compose-file/include/)。

```text 
$ REGISTRY=myregistry.com docker compose -f oci://docker.io/username/my-compose-app:latest up

在配置中找到以下变量：
VARIABLE     VALUE                SOURCE        REQUIRED    DEFAULT
REGISTRY     myregistry.com      command-line   yes         
TAG          v1.0                environment    no          latest
DOCKERFILE   Dockerfile          default        no          Dockerfile
API_KEY      <unset>             none           no          

您确定要使用这些变量继续吗？ [Y/n]:y

警告：此 Compose 项目包含来自远程源的文件：
- oci://registry.example.com/stack:latest
远程包含可能存在恶意风险。请确保您信任该来源。
您确定要继续吗？ [y/N]: 
```

如果您同意启动应用程序，Compose 将显示所有来自 OCI 构件的资源下载到的目录：

```text
...
您确定要继续吗？ [y/N]: y

您的 compose 栈 "oci://registry.example.com/stack:latest" 存储在 "~/Library/Caches/docker-compose/964e715660d6f6c3b384e05e7338613795f7dcd3613890cfa57e3540353b9d6d" 中
```

`docker compose publish` 命令支持非交互式执行，通过包含 `-y`（或 `--yes`）标志可以跳过确认提示： 

```console
$ docker compose publish -y username/my-compose-app:latest
```

## 下一步

- [了解 Docker Hub 中的 OCI 构件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)
- [Compose publish 命令](/reference/cli/docker/compose/publish.md)
- [理解 `include`](/reference/compose-file/include.md)
