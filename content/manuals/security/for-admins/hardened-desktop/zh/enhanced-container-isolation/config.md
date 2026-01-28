---
description: 增强容器隔离的高级配置
title: ECI 高级配置选项
linkTitle: 高级配置
keywords: enhanced container isolation, Docker Desktop, Docker socket, bind mount, configuration
aliases:
 - /desktop/hardened-desktop/enhanced-container-isolation/config/
weight: 30
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

## Docker socket 挂载权限

默认情况下，启用增强容器隔离（ECI）后，Docker Desktop 不允许将 Docker Engine socket 绑定挂载到容器中：

```console
$ docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock docker:cli
docker: Error response from daemon: enhanced container isolation: docker socket mount denied for container with image "docker.io/library/docker"; image is not in the allowed list; if you wish to allow it, configure the docker socket image list in the Docker Desktop settings.
```
这可以防止恶意容器获取对 Docker Engine 的访问权限，因为这种访问可能允许它们执行供应链攻击。例如，构建并推送恶意镜像到组织的仓库或类似操作。

但是，某些合法的用例需要容器访问 Docker Engine socket。例如，流行的 [Testcontainers](https://testcontainers.com/) 框架有时会将 Docker Engine socket 绑定挂载到容器中以管理它们或执行测试后清理。同样，某些 Buildpack 框架，例如 [Paketo](https://paketo.io/)，需要将 Docker socket 绑定挂载到容器中。

管理员可以选择性地配置 ECI 以允许将 Docker Engine socket 绑定挂载到容器中，但以受控的方式进行。

这可以通过 [`admin-settings.json`](../settings-management/configure-json-file.md) 文件中的 Docker Socket 挂载权限部分完成。例如：


```json
{
  "configurationFileVersion": 2,
  "enhancedContainerIsolation": {
    "locked": true,
    "value": true,
    "dockerSocketMount": {
      "imageList": {
        "images": [
          "docker.io/localstack/localstack:*",
          "docker.io/testcontainers/ryuk:*",
          "docker:cli"
        ],
        "allowDerivedImages": true
      },
      "commandList": {
        "type": "deny",
        "commands": ["push"]
      }
    }
  }
}
```

> [!TIP]
>
> 您现在也可以在 [Docker Admin Console](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md) 中配置这些设置。

如上所示，将 Docker socket 绑定挂载到容器中有两个配置：`imageList` 和 `commandList`。下面将分别描述。

### 镜像列表

`imageList` 是允许绑定挂载 Docker socket 的容器镜像列表。默认情况下，该列表为空，启用 ECI 时不允许任何容器绑定挂载 Docker socket。但是，管理员可以使用以下任一格式将镜像添加到列表中：

| 镜像引用格式  | 描述 |
| :---------------------- | :---------- |
| `<image_name>[:<tag>]`  | 镜像名称，带可选标签。如果省略标签，则使用 `:latest` 标签。如果标签是通配符 `*`，则表示"该镜像的任何标签"。 |
| `<image_name>@<digest>` | 镜像名称，带特定仓库摘要（例如，由 `docker buildx imagetools inspect <image>` 报告的摘要）。这意味着只允许与该名称和摘要匹配的镜像。 |

镜像名称遵循标准约定，因此可以指向任何镜像仓库和仓库。

在前面的示例中，镜像列表配置了三个镜像：

```json
"imageList": {
  "images": [
    "docker.io/localstack/localstack:*",
    "docker.io/testcontainers/ryuk:*",
    "docker:cli"
  ]
}
```

这意味着使用 `docker.io/localstack/localstack` 或 `docker.io/testcontainers/ryuk` 镜像（任何标签）或 `docker:cli` 镜像的容器，在启用 ECI 时允许绑定挂载 Docker socket。因此，以下命令可以工作：

```console
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock docker:cli sh
/ #
```

> [!TIP]
>
> 对允许的镜像要有限制性，如[建议](#建议)中所述。

通常，使用标签通配符格式指定镜像更容易，例如 `<image-name>:*`，因为这样每当使用新版本的镜像时，就不需要更新 `imageList`。或者，您可以使用不可变标签，例如 `:latest`，但它不像通配符那样好用，因为例如 Testcontainers 使用特定版本的镜像，不一定是最新版本。

启用 ECI 后，Docker Desktop 会定期从相应的镜像仓库下载允许镜像的镜像摘要，并将其存储在内存中。然后，当使用 Docker socket 绑定挂载启动容器时，Docker Desktop 会检查容器的镜像摘要是否与允许的摘要之一匹配。如果匹配，则允许容器启动，否则会被阻止。

由于摘要比较，无法通过将不允许的镜像重新标记为允许的镜像名称来绑过 Docker socket 挂载权限。换句话说，如果用户执行：

```console
$ docker image rm <allowed_image>
$ docker tag <disallowed_image> <allowed_image>
$ docker run -v /var/run/docker.sock:/var/run/docker.sock <allowed_image>
```

则标签操作成功，但 `docker run` 命令失败，因为不允许镜像的镜像摘要与仓库中允许镜像的摘要不匹配。

### 派生镜像的 Docker Socket 挂载权限

{{< summary-bar feature_name="Docker Scout Mount Permissions" >}}

如上一节所述，管理员可以通过 `imageList` 配置允许挂载 Docker socket 的容器镜像列表。

这适用于大多数场景，但并非总是如此，因为它需要预先知道应允许 Docker socket 挂载的镜像名称。某些容器工具（如 [Paketo](https://paketo.io/) buildpacks）会构建需要 Docker socket 绑定挂载的临时本地镜像。由于这些临时镜像的名称事先未知，`imageList` 是不够的。

为了克服这个问题，从 Docker Desktop 4.34 版本开始，Docker Socket 挂载权限不仅适用于 `imageList` 中列出的镜像；它们还适用于从 `imageList` 中镜像派生（即从其构建）的任何本地镜像。

也就是说，如果一个名为"myLocalImage"的本地镜像是从"myBaseImage"构建的（即 Dockerfile 中有 `FROM myBaseImage`），那么如果"myBaseImage"在 `imageList` 中，"myBaseImage"和"myLocalImage"都允许挂载 Docker socket。

例如，要使 Paketo buildpacks 与 Docker Desktop 和 ECI 一起工作，只需将以下镜像添加到 `imageList`：

```json
"imageList": {
  "images": [
    "paketobuildpacks/builder:base"
  ],
  "allowDerivedImages": true
}
```

当 buildpack 运行时，它将创建一个从 `paketobuildpacks/builder:base` 派生的临时镜像，并将 Docker socket 挂载到其中。ECI 将允许这样做，因为它会注意到临时镜像是从允许的镜像派生的。

该行为默认禁用，必须通过如上所示设置 `"allowDerivedImages": true` 显式启用。通常建议您禁用此设置，除非您知道需要它。

一些注意事项：

* 设置 `"allowedDerivedImages" :true` 会影响容器的启动时间，最多增加 1 秒，因为 Docker Desktop 需要对容器镜像执行更多检查。

* `allowDerivedImages` 设置仅适用于从允许镜像构建的仅限本地镜像。也就是说，派生镜像不能存在于远程仓库中，因为如果存在，您只需在 `imageList` 中列出其名称即可。

* 要使派生镜像检查工作，父镜像（即 `imageList` 中的镜像）必须在本地存在（即必须已从仓库显式拉取）。这通常不是问题，因为需要此功能的工具（例如 Paketo buildpacks）会预先拉取父镜像。

* 仅适用于 Docker Desktop 4.34 和 4.35 版本：`allowDerivedImages` 设置适用于 `imageList` 中使用显式标签指定的所有镜像（例如 `<name>:<tag>`）。它不适用于使用上一节中描述的标签通配符指定的镜像（例如 `<name>:*`）。在 Docker Desktop 4.36 及更高版本中，此限制不再适用，这意味着 `allowDerivedImages` 设置适用于使用或不使用通配符标签指定的镜像。这使得管理 ECI Docker socket 镜像列表更加容易。

### 允许所有容器挂载 Docker socket

在 Docker Desktop 4.36 及更高版本中，可以配置镜像列表以允许任何容器挂载 Docker socket。您可以通过在 `imageList` 中添加 `"*"` 来实现：

```json
"imageList": {
  "images": [
    "*"
  ]
}
```

这告诉 Docker Desktop 允许所有容器挂载 Docker socket，这增加了灵活性但降低了安全性。它还改善了使用增强容器隔离时的容器启动时间。

建议您仅在明确列出允许的容器镜像不够灵活的场景中使用此选项。

### 命令列表

除了前面章节中描述的 `imageList` 之外，ECI 还可以进一步限制容器可以通过绑定挂载的 Docker socket 发出的命令。这是通过 Docker socket 挂载权限的 `commandList` 完成的，它作为 `imageList` 的补充安全机制（即像第二道防线）。

例如，假设 `imageList` 配置为允许镜像 `docker:cli` 挂载 Docker socket，并使用它启动一个容器：

```console
$ docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock sh
/ #
```

默认情况下，这允许容器通过该 Docker socket 发出任何命令（例如，构建并推送镜像到组织的仓库），这通常是不希望的。

为了提高安全性，可以配置 `commandList` 来限制容器内进程可以在绑定挂载的 Docker socket 上发出的命令。根据您的偏好，`commandList` 可以配置为"拒绝"列表（默认）或"允许"列表。

列表中的每个命令由其名称指定，如 `docker --help` 报告的（例如，"ps"、"build"、"pull"、"push"等）。此外，允许使用以下命令通配符来阻止整组命令：

| 命令通配符  | 描述 |
| :---------------- | :---------- |
| "container\*"     | 指所有 "docker container ..." 命令 |
| "image\*"         | 指所有 "docker image ..." 命令 |
| "volume\*"        | 指所有 "docker volume ..." 命令 |
| "network\*"       | 指所有 "docker network ..." 命令 |
| "build\*"         | 指所有 "docker build ..." 命令 |
| "system\*"        | 指所有 "docker system ..." 命令 |

例如，以下配置阻止 Docker socket 上的 `build` 和 `push` 命令：

```json
"commandList": {
  "type": "deny",
  "commands": ["build", "push"]
}
```

因此，如果在容器内，您在绑定挂载的 Docker socket 上发出这些命令中的任何一个，它们都会被阻止：

```console
/ # docker push myimage
Error response from daemon: enhanced container isolation: docker command "/v1.43/images/myimage/push?tag=latest" is blocked; if you wish to allow it, configure the docker socket command list in the Docker Desktop settings or admin-settings.
```

同样：

```console
/ # curl --unix-socket /var/run/docker.sock -XPOST http://localhost/v1.43/images/myimage/push?tag=latest
Error response from daemon: enhanced container isolation: docker command "/v1.43/images/myimage/push?tag=latest" is blocked; if you wish to allow it, configure the docker socket command list in the Docker Desktop settings or admin-settings.
```

请注意，如果 `commandList` 配置为"允许"列表，则效果相反：只有列出的命令才会被允许。是将列表配置为允许还是拒绝列表取决于用例。

### 建议

* 对允许绑定挂载 Docker socket 的容器镜像列表（即 `imageList`）要有限制性。通常，只允许绝对需要且您信任的镜像。

* 如果可能，在 `imageList` 中使用标签通配符格式（例如 `<image_name>:*`），因为这消除了由于镜像标签更改而需要更新 `admin-settings.json` 文件的需要。

* 在 `commandList` 中，阻止您不希望容器执行的命令。例如，对于本地测试（例如 Testcontainers），绑定挂载 Docker socket 的容器通常创建/运行/删除容器、卷和网络，但通常不构建镜像或将其推送到仓库（尽管有些可能合法地这样做）。允许或阻止哪些命令取决于用例。

  - 请注意，容器通过绑定挂载的 Docker socket 发出的所有"docker"命令也将在增强容器隔离下执行（即结果容器使用 Linux 用户命名空间，敏感系统调用被审查等）。

### 注意事项和限制

* 当 Docker Desktop 重新启动时，允许挂载 Docker socket 的镜像可能会意外地被阻止挂载。当远程仓库中的镜像摘要更改（例如，":latest"镜像已更新）且该镜像的本地副本（例如，来自先前的 `docker pull`）不再与远程仓库中的摘要匹配时，可能会发生这种情况。在这种情况下，请删除本地镜像并重新拉取（例如，`docker rm <image>` 和 `docker pull <image>`）。

* 无法允许对使用仅限本地镜像（即不在镜像仓库中的镜像）的容器进行 Docker socket 绑定挂载，除非它们是[从允许镜像派生的](#派生镜像的-docker-socket-挂载权限)或者您已[允许所有容器挂载 Docker socket](#允许所有容器挂载-docker-socket)。这是因为 Docker Desktop 从镜像仓库拉取允许镜像的摘要，然后使用它与镜像的本地副本进行比较。

* `commandList` 配置适用于所有允许绑定挂载 Docker socket 的容器。因此，无法为每个容器单独配置。

* `commandList` 中尚不支持以下命令：

| 不支持的命令  | 描述 |
| :------------------- | :---------- |
| `compose`              | Docker Compose |
| `dev`                  | 开发环境 |
| `extension`            | 管理 Docker Extensions |
| `feedback`             | 向 Docker 发送反馈 |
| `init`                 | 创建 Docker 相关的启动文件 |
| `manifest`             | 管理 Docker 镜像清单 |
| `plugin`              | 管理插件 |
| `sbom`                 | 查看软件物料清单（SBOM） |
| `scout`                | Docker Scout |
| `trust`                | 管理 Docker 镜像的信任 |

> [!NOTE]
>
> 运行"真正的"Docker-in-Docker（即在容器内运行 Docker Engine）时，Docker socket 挂载权限不适用。在这种情况下，没有将主机的 Docker socket 绑定挂载到容器中，因此容器没有风险利用主机 Docker Engine 的配置和凭据来执行恶意活动。增强容器隔离能够安全地运行 Docker-in-Docker，而不会给外部容器在 Docker Desktop 虚拟机中提供真正的 root 权限。
