---
title: 构建密钥
linkTitle: 密钥
weight: 30
description: 安全地管理凭据和其他密钥
keywords: build, secrets, credentials, passwords, tokens, ssh, git, auth, http
tags: [Secrets]
---

构建密钥（build secret）是任何敏感信息，例如密码或 API 令牌，在应用程序构建过程中被使用。

构建参数和环境变量不适合用于向构建传递密钥，因为它们会保留在最终镜像中。相反，你应该使用密钥挂载或 SSH 挂载，它们可以安全地向构建公开密钥。

## 构建密钥的类型

- [密钥挂载](#密钥挂载)是用于向构建传递密钥的通用挂载。密钥挂载从构建客户端获取密钥，并在构建指令执行期间临时在构建容器内部提供它。例如，如果你的构建需要与私有工件服务器或 API 通信，这很有用。
- [SSH 挂载](#ssh-挂载)是用于在构建内部提供 SSH 套接字或密钥的专用挂载。当你需要在构建中获取私有 Git 仓库时，它们通常被使用。
- [远程上下文的 Git 认证](#远程上下文的-git-认证)是一组预定义的密钥，用于当你使用同时也是私有仓库的远程 Git 上下文进行构建时。这些密钥是"预检"密钥：它们不在构建指令中使用，而是用于向构建器提供获取上下文所需的凭据。

## 使用构建密钥

对于密钥挂载和 SSH 挂载，使用构建密钥是一个两步过程。首先你需要将密钥传递给 `docker build` 命令，然后你需要在 Dockerfile 中使用密钥。

要将密钥传递给构建，使用 [`docker build --secret` 标志](/reference/cli/docker/buildx/build.md#secret)，或 [Bake](../bake/reference.md#targetsecret) 的等效选项。

{{< tabs >}}
{{< tab name="CLI" >}}

```console
$ docker build --secret id=aws,src=$HOME/.aws/credentials .
```

{{< /tab >}}
{{< tab name="Bake" >}}

```hcl
variable "HOME" {
  default = null
}

target "default" {
  secret = [
    "id=aws,src=${HOME}/.aws/credentials"
  ]
}
```

{{< /tab >}}
{{< /tabs >}}

要在构建中使用密钥并使其对 `RUN` 指令可用，在 Dockerfile 中使用 [`--mount=type=secret`](/reference/dockerfile.md#run---mounttypesecret) 标志。

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

## 密钥挂载

密钥挂载将密钥作为文件或环境变量公开给构建容器。你可以使用密钥挂载向构建传递敏感信息，例如 API 令牌、密码或 SSH 密钥。

### 来源

密钥的来源可以是[文件](/reference/cli/docker/buildx/build.md#file)或[环境变量](/reference/cli/docker/buildx/build.md#env)。当你使用 CLI 或 Bake 时，可以自动检测类型。你也可以使用 `type=file` 或 `type=env` 显式指定它。

以下示例将环境变量 `KUBECONFIG` 挂载到密钥 ID `kube`，作为构建容器中 `/run/secrets/kube` 的文件。

```console
$ docker build --secret id=kube,env=KUBECONFIG .
```

当你使用来自环境变量的密钥时，你可以省略 `env` 参数，将密钥绑定到与变量同名的文件。在以下示例中，`API_TOKEN` 变量的值被挂载到构建容器中的 `/run/secrets/API_TOKEN`。

```console
$ docker build --secret id=API_TOKEN .
```

### 目标

在 Dockerfile 中使用密钥时，默认情况下密钥被挂载为文件。密钥在构建容器内的默认文件路径是 `/run/secrets/<id>`。你可以使用 Dockerfile 中 `RUN --mount` 标志的 `target` 和 `env` 选项自定义密钥在构建容器中的挂载方式。

以下示例获取密钥 id `aws` 并将其挂载到构建容器中 `/run/secrets/aws` 的文件。

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

要将密钥挂载为具有不同名称的文件，在 `--mount` 标志中使用 `target` 选项。

```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp ...
```

要将密钥挂载为环境变量而不是文件，在 `--mount` 标志中使用 `env` 选项。

```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=aws-session-token,env=AWS_SESSION_TOKEN \
    aws s3 cp ...
```

可以同时使用 `target` 和 `env` 选项将密钥同时挂载为文件和环境变量。

## SSH 挂载

如果你想在构建中使用的凭据是 SSH 代理套接字或密钥，你可以使用 SSH 挂载而不是密钥挂载。克隆私有 Git 仓库是 SSH 挂载的常见用例。

以下示例使用 [Dockerfile SSH 挂载](/reference/dockerfile.md#run---mounttypessh)克隆私有 GitHub 仓库。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD git@github.com:me/myprivaterepo.git /src/
```

要将 SSH 套接字传递给构建，你使用 [`docker build --ssh` 标志](/reference/cli/docker/buildx/build.md#ssh)，或 [Bake](../bake/reference.md#targetssh) 的等效选项。

```console
$ docker buildx build --ssh default .
```

## 远程上下文的 Git 认证

BuildKit 支持两个预定义的构建密钥，`GIT_AUTH_TOKEN` 和 `GIT_AUTH_HEADER`。使用它们在使用远程私有 Git 仓库构建时指定 HTTP 认证参数，包括：

- 使用私有 Git 仓库作为构建上下文进行构建
- 在构建中使用 `ADD` 获取私有 Git 仓库

例如，假设你在 `https://gitlab.com/example/todo-app.git` 有一个私有 GitLab 项目，你想使用该仓库作为构建上下文运行构建。未经认证的 `docker build` 命令会失败，因为构建器无权拉取该仓库：

```console
$ docker build https://gitlab.com/example/todo-app.git
[+] Building 0.4s (1/1) FINISHED
 => ERROR [internal] load git source https://gitlab.com/example/todo-app.git
------
 > [internal] load git source https://gitlab.com/example/todo-app.git:
0.313 fatal: could not read Username for 'https://gitlab.com': terminal prompts disabled
------
```

要将构建器认证到 Git 服务器，将 `GIT_AUTH_TOKEN` 环境变量设置为包含有效的 GitLab 访问令牌，并将其作为密钥传递给构建：

```console
$ GIT_AUTH_TOKEN=$(cat gitlab-token.txt) docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://gitlab.com/example/todo-app.git
```

`GIT_AUTH_TOKEN` 也可以与 `ADD` 一起使用，作为构建的一部分获取私有 Git 仓库：

```dockerfile
FROM alpine
ADD https://gitlab.com/example/todo-app.git /src
```

### HTTP 认证方案

默认情况下，通过 HTTP 的 Git 认证使用 Bearer 认证方案：

```http
Authorization: Bearer <GIT_AUTH_TOKEN>
```

如果你需要使用 Basic 方案，带有用户名和密码，你可以设置 `GIT_AUTH_HEADER` 构建密钥：

```console
$ export GIT_AUTH_TOKEN=$(cat gitlab-token.txt)
$ export GIT_AUTH_HEADER=basic
$ docker build \
  --secret id=GIT_AUTH_TOKEN \
  --secret id=GIT_AUTH_HEADER \
  https://gitlab.com/example/todo-app.git
```

BuildKit 目前只支持 Bearer 和 Basic 方案。

### 多个主机

你可以按主机设置 `GIT_AUTH_TOKEN` 和 `GIT_AUTH_HEADER` 密钥，这让你可以为不同的主机名使用不同的认证参数。要指定主机名，将主机名作为后缀附加到密钥 ID：

```console
$ export GITLAB_TOKEN=$(cat gitlab-token.txt)
$ export GERRIT_TOKEN=$(cat gerrit-username-password.txt)
$ export GERRIT_SCHEME=basic
$ docker build \
  --secret id=GIT_AUTH_TOKEN.gitlab.com,env=GITLAB_TOKEN \
  --secret id=GIT_AUTH_TOKEN.gerrit.internal.example,env=GERRIT_TOKEN \
  --secret id=GIT_AUTH_HEADER.gerrit.internal.example,env=GERRIT_SCHEME \
  https://gitlab.com/example/todo-app.git
```
