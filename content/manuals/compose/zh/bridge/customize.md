---
title: 自定义 Compose Bridge
linkTitle: 自定义
weight: 20
description: 了解如何使用 Go 模板和 Compose 扩展自定义 Compose Bridge 转换
keywords: docker compose bridge, customize compose bridge, compose bridge templates, compose to kubernetes, compose bridge transformation, go templates docker

---

{{< summary-bar feature_name="Compose bridge" >}}

本页面解释了 Compose Bridge 如何利用模板来高效地将 Docker Compose 文件转换为 Kubernetes 清单。它还解释了如何根据您的特定需求自定义这些模板，或如何构建您自己的转换。

## 工作原理

Compose Bridge 使用转换功能让您将 Compose 模型转换为另一种形式。

转换被打包为 Docker 镜像，该镜像接收完全解析的 Compose 模型作为 `/in/compose.yaml`，并可以在 `/out` 下生成任何目标格式的文件。

Compose Bridge 包含一个使用 Go 模板的默认 Kubernetes 转换，您可以通过替换或扩展模板来自定义它。

### 语法

Compose Bridge 使用模板将 Compose 配置文件转换为 Kubernetes 清单。模板是使用 [Go 模板语法](https://pkg.go.dev/text/template)的纯文本文件。这使得可以插入逻辑和数据，使模板根据 Compose 模型动态和适应性地工作。

当模板执行时，它必须生成一个 YAML 文件，这是 Kubernetes 清单的标准格式。只要用 `---` 分隔，就可以生成多个文件。

每个 YAML 输出文件以自定义头部注释开始，例如：

```yaml
#! manifest.yaml
```

在以下示例中，模板遍历 `compose.yaml` 文件中定义的服务。对于每个服务，会生成一个专用的 Kubernetes 清单文件，根据服务命名并包含指定的配置。

```yaml
{{ range $name, $service := .services }}
---
#! {{ $name }}-manifest.yaml
# Generated code, do not edit
key: value
## ...
{{ end }}
```

### 输入

您可以通过运行 `docker compose config` 生成输入模型。这个规范的 YAML 输出作为 Compose Bridge 转换的输入。在模板中，使用点表示法访问 `compose.yaml` 中的数据，允许您浏览嵌套的数据结构。例如，要访问服务的部署模式，您可以使用 `service.deploy.mode`：

 ```yaml
# iterate over a yaml sequence
{{ range $name, $service := .services }}
  # access a nested attribute using dot notation
  {{ if eq $service.deploy.mode "global" }}
kind: DaemonSet
  {{ end }}
{{ end }}
```

您可以查看 [Compose Specification JSON schema](https://github.com/compose-spec/compose-go/blob/main/schema/compose-spec.json) 以全面了解 Compose 模型。此 schema 概述了 Compose 模型中所有可能的配置及其数据类型。

### 辅助函数

作为 Go 模板语法的一部分，Compose Bridge 提供了一组 YAML 辅助函数，用于在模板中高效地操作数据：

- `seconds`：将[持续时间](/reference/compose-file/extension.md#specifying-durations)转换为整数
- `uppercase`：将字符串转换为大写字符
- `title`：通过将每个单词的首字母大写来转换字符串
- `safe`：将字符串转换为安全标识符，用 `-` 替换所有字符（小写 a-z 除外）
- `truncate`：从列表中删除前 N 个元素
- `join`：使用分隔符将列表中的元素组合成单个字符串
- `base64`：将字符串编码为 base64，用于 Kubernetes 中编码密钥
- `map`：根据表示为 `"value -> newValue"` 字符串的映射转换值
- `indent`：按 N 个空格缩进写入字符串内容
- `helmValue`：在最终文件中将字符串内容作为模板值写入

在以下示例中，模板检查是否为服务指定了健康检查间隔，应用 `seconds` 函数将此间隔转换为秒，并将值分配给 `periodSeconds` 属性。

```yaml
{{ if $service.healthcheck.interval }}
            periodSeconds: {{ $service.healthcheck.interval | seconds }}{{ end }}
{{ end }}
```

## 自定义

由于 Kubernetes 是一个多功能平台，有很多方法可以将 Compose 概念映射到 Kubernetes 资源定义。Compose Bridge 允许您自定义转换以匹配您自己的基础设施决策和偏好，具有不同程度的灵活性和工作量。

### 修改默认模板

您可以通过运行 `docker compose bridge transformations create --from docker/compose-bridge-kubernetes my-template` 提取默认转换 `docker/compose-bridge-kubernetes` 使用的模板，并调整模板以满足您的需求。

模板被提取到以您的模板名称命名的目录中，在本例中为 `my-template`。它包含一个 Dockerfile，让您可以创建自己的镜像来分发您的模板，以及一个包含模板文件的目录。您可以自由编辑现有文件、删除它们或[添加新文件](#添加您自己的模板)，以便随后生成满足您需求的 Kubernetes 清单。然后，您可以使用生成的 Dockerfile 将您的更改打包到新的转换镜像中，然后与 Compose Bridge 一起使用：

```console
$ docker build --tag mycompany/transform --push .
```

然后您可以使用您的转换作为替代：

```console
$ docker compose bridge convert --transformations mycompany/transform
```

### 添加您自己的模板

对于 Compose Bridge 默认转换不管理的资源，您可以构建自己的模板。`compose.yaml` 模型可能不提供填充目标清单所需的所有配置属性。如果是这种情况，您可以依赖 Compose 自定义扩展来更好地描述应用程序，并提供与平台无关的转换。

例如，如果您在 `compose.yaml` 文件的服务定义中添加 `x-virtual-host` 元数据，您可以使用以下自定义属性生成 Ingress 规则：

```yaml
{{ $project := .name }}
#! {{ $name }}-ingress.yaml
# Generated code, do not edit
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: virtual-host-ingress
  namespace: {{ $project }}
spec:
  rules:
{{ range $name, $service := .services }}
{{ range index $service "x-virtual-host" }}
  - host: ${{ . }}
    http:
      paths:
      - path: "/"
        backend:
          service:
            name: ${{ name }}
            port:
              number: 80
{{ end }}
{{ end }}
```

一旦打包到 Docker 镜像中，您可以在将 Compose 模型转换为 Kubernetes 时使用此自定义模板，作为其他转换的补充：

```console
$ docker compose bridge convert \
    --transformation docker/compose-bridge-kubernetes \
    --transformation mycompany/transform
```

### 构建您自己的转换

虽然 Compose Bridge 模板使得用最少的更改进行自定义变得容易，但您可能希望进行重大更改，或依赖现有的转换工具。

Compose Bridge 转换是一个 Docker 镜像，设计为从 `/in/compose.yaml` 获取 Compose 模型并在 `/out` 下生成平台清单。这个简单的约定使得使用 [Kompose](https://kompose.io/) 打包替代转换变得容易：

```Dockerfile
FROM alpine

# Get kompose from github release page
RUN apk add --no-cache curl
ARG VERSION=1.32.0
RUN ARCH=$(uname -m | sed 's/armv7l/arm/g' | sed 's/aarch64/arm64/g' | sed 's/x86_64/amd64/g') && \
    curl -fsL \
    "https://github.com/kubernetes/kompose/releases/download/v${VERSION}/kompose-linux-${ARCH}" \
    -o /usr/bin/kompose
RUN chmod +x /usr/bin/kompose

CMD ["/usr/bin/kompose", "convert", "-f", "/in/compose.yaml", "--out", "/out"]
```

这个 Dockerfile 打包了 Kompose 并定义了根据 Compose Bridge 转换约定运行此工具的命令。
