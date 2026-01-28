---
title: 使用 Docker Engine SDK 进行开发
linkTitle: SDK
weight: 10
description: 了解如何使用 Docker Engine SDK 以您选择的语言自动化 Docker 任务
keywords: developing, sdk, Docker Engine SDKs, install SDKs, SDK versions
aliases:
  - /develop/sdk/
  - /engine/api/sdks/
  - /engine/api/sdk/
---

Docker 提供了一个用于与 Docker 守护进程（daemon）交互的 API（称为 Docker Engine API），以及 Go 和 Python 的 SDK。这些 SDK 使您能够高效地构建和扩展 Docker 应用程序和解决方案。如果 Go 或 Python 不适合您的需求，您可以直接使用 Docker Engine API。

Docker Engine API 是一个 RESTful API，可通过 HTTP 客户端（如 `wget` 或 `curl`）访问，也可以使用大多数现代编程语言内置的 HTTP 库来访问。

## 安装 SDK

使用以下命令安装 Go 或 Python SDK。两个 SDK 可以同时安装并共存。

### Go SDK

```console
$ go get github.com/docker/docker/client
```

客户端需要较新版本的 Go。运行 `go version` 并确保您正在运行当前支持的 Go 版本。

有关更多信息，请参阅 [Docker Engine Go SDK 参考文档](https://godoc.org/github.com/docker/docker/client)。

### Python SDK

- 推荐方式：运行 `pip install docker`。

- 如果无法使用 `pip`：

  1.  [直接下载包](https://pypi.python.org/pypi/docker/)。
  2.  解压并进入解压后的目录。
  3.  运行 `python setup.py install`。

有关更多信息，请参阅 [Docker Engine Python SDK 参考文档](https://docker-py.readthedocs.io/)。

## 查看 API 参考

您可以[查看最新版本 API 的参考文档](/reference/api/engine/latest/)或[选择特定版本](/reference/api/engine/version-history/)。

## API 和 SDK 版本控制

您应该使用的 Docker Engine API 版本取决于您的 Docker 守护进程和 Docker 客户端的版本。有关详细信息，请参阅 API 文档中的[版本化的 API 和 SDK](/reference/api/engine/#versioned-api-and-sdk) 部分。

## SDK 和 API 快速入门

使用以下指南选择在您的代码中使用的 SDK 或 API 版本：

- 如果您正在开始一个新项目，请使用[最新版本](/reference/api/engine/latest/)，但要使用 API 版本协商或指定您正在使用的版本。这有助于避免意外情况。
- 如果您需要新功能，请将代码更新为至少使用支持该功能的最低版本，并优先使用您可以使用的最新版本。
- 否则，继续使用您的代码已经在使用的版本。

作为示例，`docker run` 命令可以使用 Docker API 直接实现，也可以使用 Python 或 Go SDK 实现。

{{< tabs >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"io"
	"os"

	"github.com/docker/docker/api/types/container"
        "github.com/docker/docker/api/types/image"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/stdcopy"
)

func main() {
    ctx := context.Background()
    cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
    if err != nil {
        panic(err)
    }
    defer cli.Close()

    reader, err := cli.ImagePull(ctx, "docker.io/library/alpine", image.PullOptions{})
    if err != nil {
        panic(err)
    }
    io.Copy(os.Stdout, reader)

    resp, err := cli.ContainerCreate(ctx, &container.Config{
        Image: "alpine",
        Cmd:   []string{"echo", "hello world"},
    }, nil, nil, nil, "")
    if err != nil {
        panic(err)
    }

    if err := cli.ContainerStart(ctx, resp.ID, container.StartOptions{}); err != nil {
        panic(err)
    }

    statusCh, errCh := cli.ContainerWait(ctx, resp.ID, container.WaitConditionNotRunning)
    select {
    case err := <-errCh:
        if err != nil {
            panic(err)
        }
    case <-statusCh:
    }

    out, err := cli.ContainerLogs(ctx, resp.ID, container.LogsOptions{ShowStdout: true})
    if err != nil {
        panic(err)
    }

    stdcopy.StdCopy(os.Stdout, os.Stderr, out)
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
print(client.containers.run("alpine", ["echo", "hello", "world"]))
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock -H "Content-Type: application/json" \
  -d '{"Image": "alpine", "Cmd": ["echo", "hello world"]}' \
  -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/create
{"Id":"1c6594faf5","Warnings":null}

$ curl --unix-socket /var/run/docker.sock -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/start

$ curl --unix-socket /var/run/docker.sock -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/wait
{"StatusCode":0}

$ curl --unix-socket /var/run/docker.sock "http://localhost/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/logs?stdout=1"
hello world
```

使用 cURL 通过 Unix 套接字连接时，主机名并不重要。上述示例使用 `localhost`，但任何主机名都可以。

> [!IMPORTANT]
>
> 上述示例假设您使用的是 cURL 7.50.0 或更高版本。旧版本的 cURL 在使用套接字连接时采用[非标准 URL 表示法](https://github.com/moby/moby/issues/17960)。
>
> 如果您使用的是旧版本的 cURL，请改用 `http:/<API version>/`，例如：`http:/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/start`。

{{< /tab >}}
{{< /tabs >}}

有关更多示例，请查看 [SDK 示例](examples.md)。

## 非官方库

社区支持了多种其他语言的库。它们未经 Docker 测试，因此如果遇到任何问题，请向库维护者提交问题。

| 语言                  | 库                                                                              |
|:----------------------|:--------------------------------------------------------------------------------|
| C                     | [libdocker](https://github.com/danielsuo/libdocker)                             |
| C#                    | [Docker.DotNet](https://github.com/ahmetalpbalkan/Docker.DotNet)                |
| C++                   | [lasote/docker_client](https://github.com/lasote/docker_client)                 |
| Clojure               | [clj-docker-client](https://github.com/into-docker/clj-docker-client)           |
| Clojure               | [contajners](https://github.com/lispyclouds/contajners)                         |
| Dart                  | [bwu_docker](https://github.com/bwu-dart/bwu_docker)                            |
| Erlang                | [erldocker](https://github.com/proger/erldocker)                                |
| Gradle                | [gradle-docker-plugin](https://github.com/gesellix/gradle-docker-plugin)        |
| Groovy                | [docker-client](https://github.com/gesellix/docker-client)                      |
| Haskell               | [docker-hs](https://github.com/denibertovic/docker-hs)                          |
| Java                  | [docker-client](https://github.com/spotify/docker-client)                       |
| Java                  | [docker-java](https://github.com/docker-java/docker-java)                       |
| Java                  | [docker-java-api](https://github.com/amihaiemil/docker-java-api)                |
| Java                  | [jocker](https://github.com/ndeloof/jocker)                                     |
| NodeJS                | [dockerode](https://github.com/apocas/dockerode)                                |
| NodeJS                | [harbor-master](https://github.com/arhea/harbor-master)                         |
| NodeJS                | [the-moby-effect](https://github.com/leonitousconforti/the-moby-effect)         |
| Perl                  | [Eixo::Docker](https://github.com/alambike/eixo-docker)                         |
| PHP                   | [Docker-PHP](https://github.com/docker-php/docker-php)                          |
| Ruby                  | [docker-api](https://github.com/swipely/docker-api)                             |
| Rust                  | [bollard](https://github.com/fussybeaver/bollard)                               |
| Rust                  | [docker-rust](https://github.com/abh1nav/docker-rust)                           |
| Rust                  | [shiplift](https://github.com/softprops/shiplift)                               |
| Scala                 | [tugboat](https://github.com/softprops/tugboat)                                 |
| Scala                 | [reactive-docker](https://github.com/almoehi/reactive-docker)                   |
| Swift                 | [docker-client-swift](https://github.com/valeriomazzeo/docker-client-swift)     |
