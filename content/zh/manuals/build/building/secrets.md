--- 
title: 构建机密 (Build secrets)
linkTitle: 机密
weight: 30
description: 安全地管理凭据和其他机密信息
keywords: build, secrets, credentials, passwords, tokens, ssh, git, auth, http, 机密, 凭据
tags: [Secrets]
---

构建机密 (Build secret) 是指作为应用程序构建过程一部分使用的任何敏感信息，例如密码或 API 令牌。

构建参数 (Build arguments) 和环境变量不适合用来向构建任务传递机密，因为它们会持久化在最终镜像中。相反，您应该使用机密挂载 (secret mounts) 或 SSH 挂载，它们能安全地将机密暴露给您的构建任务。

## 构建机密的类型

- [机密挂载 (Secret mounts)](#机密挂载) 是用于向构建任务传递机密的通用型挂载。机密挂载从构建客户端获取机密，并在构建指令执行期间暂时使其在构建容器内可用。例如，如果您的构建任务需要与私有的产物服务器或 API 通信，这就非常有用。
- [SSH 挂载](#ssh-挂载) 是专门用于使 SSH 套接字或密钥在构建内部可用的挂载。通常用于在构建过程中获取私有 Git 仓库。
- [远程上下文的 Git 身份验证](#远程上下文的-git-身份验证) 是一组预定义的机密，用于通过也是私有仓库的远程 Git 上下文进行构建。这些是“预检 (pre-flight)”机密：它们不会在构建指令内部被消耗，而是用于为构建器提供获取上下文所需的凭据。

## 使用构建机密

对于机密挂载和 SSH 挂载，使用构建机密分为两个步骤。首先，您需要将机密传递给 `docker build` 命令，然后您需要在 Dockerfile 中消费该机密。

要向构建任务传递机密，使用 [`docker build --secret` 标志](/reference/cli/docker/buildx/build.md#secret)，或 [Bake](../bake/reference.md#targetsecret) 中的等效选项。

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

要在构建中消费机密并使其对 `RUN` 指令可用，请在 Dockerfile 中使用 [`--mount=type=secret`](/reference/dockerfile.md#run---mounttypesecret) 标志。

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

## 机密挂载 (Secret mounts)

机密挂载将机密以文件或环境变量的形式暴露给构建容器。您可以使用机密挂载向构建任务传递敏感信息，如 API 令牌、密码或 SSH 密钥。

### 来源 (Sources)

机密的来源可以是 [文件](/reference/cli/docker/buildx/build.md#file) 或 [环境变量](/reference/cli/docker/buildx/build.md#env)。当您使用 CLI 或 Bake 时，系统可以自动检测类型。您也可以通过 `type=file` 或 `type=env` 显式指定。

以下示例将环境变量 `KUBECONFIG` 挂载到机密 ID `kube`，作为构建容器内 `/run/secrets/kube` 路径下的一个文件。

```console
$ docker build --secret id=kube,env=KUBECONFIG .
```

当您使用来自环境变量的机密时，如果机密名称与变量名相同，可以省略 `env` 参数。在以下示例中，`API_TOKEN` 变量的值被挂载到构建容器内的 `/run/secrets/API_TOKEN` 路径。

```console
$ docker build --secret id=API_TOKEN .
```

### 目标 (Target)

在 Dockerfile 中消费机密时，默认情况下机密被挂载为一个文件。构建容器内机密的默认文件路径是 `/run/secrets/<id>`。您可以使用 Dockerfile 中 `RUN --mount` 标志的 `target` 和 `env` 选项来自定义机密在构建容器中的挂载方式。

以下示例获取机密 ID `aws` 并将其挂载到构建容器内的 `/run/secrets/aws` 文件。

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

要将机密挂载为具有不同名称的文件，请使用 `--mount` 标志中的 `target` 选项。

```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp ...
```

要将机密挂载为环境变量而非文件，请使用 `--mount` 标志中的 `env` 选项。

```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=aws-session-token,env=AWS_SESSION_TOKEN \
    aws s3 cp ...
```

也可以同时使用 `target` 和 `env` 选项，将机密同时挂载为文件和环境变量。

## SSH 挂载

如果您想在构建中使用的凭据是 SSH 代理套接字或密钥，可以使用 SSH 挂载代替机密挂载。克隆私有 Git 仓库是 SSH 挂载的一个常见用例。

以下示例使用 [Dockerfile SSH 挂载](/reference/dockerfile.md#run---mounttypessh) 克隆一个私有 GitHub 仓库。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD git@github.com:me/myprivaterepo.git /src/
```

要向构建任务传递 SSH 套接字，使用 [`docker build --ssh` 标志](/reference/cli/docker/buildx/build.md#ssh)，或 [Bake](../bake/reference.md#targetssh) 中的等效选项。

```console
$ docker buildx build --ssh default .
```

## 远程上下文的 Git 身份验证

BuildKit 支持两个预定义的构建机密：`GIT_AUTH_TOKEN` 和 `GIT_AUTH_HEADER`。当使用远程私有 Git 仓库进行构建时，使用它们来指定 HTTP 身份验证参数，包括：

- 使用私有 Git 仓库作为构建上下文
- 在构建过程中通过 `ADD` 获取私有 Git 仓库

例如，假设您有一个私有的 GitLab 项目，地址为 `https://gitlab.com/example/todo-app.git`，且您想使用该仓库作为构建上下文运行构建。由于构建器未被授权拉取该仓库，未经身份验证的 `docker build` 命令将会失败：

```console
$ docker build https://gitlab.com/example/todo-app.git
[+] Building 0.4s (1/1) FINISHED
 => ERROR [internal] load git source https://gitlab.com/example/todo-app.git
------
 > [internal] load git source https://gitlab.com/example/todo-app.git:
0.313 fatal: could not read Username for 'https://gitlab.com': terminal prompts disabled
------
```

要让构建器向 Git 服务器进行身份验证，请设置 `GIT_AUTH_TOKEN` 环境变量以包含有效的 GitLab 访问令牌，并将其作为机密传递给构建任务：

```console
$ GIT_AUTH_TOKEN=$(cat gitlab-token.txt) docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://gitlab.com/example/todo-app.git
```

`GIT_AUTH_TOKEN` 同样适用于 `ADD` 指令，用于在构建过程中获取私有 Git 仓库：

```dockerfile
FROM alpine
ADD https://gitlab.com/example/todo-app.git /src
```

### HTTP 身份验证方案

默认情况下，通过 HTTP 进行的 Git 身份验证使用 Bearer 方案：

```http
Authorization: Bearer <GIT_AUTH_TOKEN>
```

如果您需要使用 Basic 方案（包含用户名和密码），可以设置 `GIT_AUTH_HEADER` 构建机密：

```console
$ export GIT_AUTH_TOKEN=$(cat gitlab-token.txt)
$ export GIT_AUTH_HEADER=basic
$ docker build \
  --secret id=GIT_AUTH_TOKEN \
  --secret id=GIT_AUTH_HEADER \
  https://gitlab.com/example/todo-app.git
```

BuildKit 目前仅支持 Bearer 和 Basic 方案。

### 多个主机

您可以基于每个主机设置 `GIT_AUTH_TOKEN` 和 `GIT_AUTH_HEADER` 机密，这允许您为不同的主机名使用不同的身份验证参数。要指定主机名，请将主机名作为后缀附加到机密 ID：

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