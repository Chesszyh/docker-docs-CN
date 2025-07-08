---
title: 自定义 Compose Bridge
linkTitle: 自定义
weight: 20
description: 了解如何使用 Go 模板和 Compose 扩展来自定义 Compose Bridge 转换
keywords: docker compose bridge, customize compose bridge, compose bridge templates, compose to kubernetes, compose bridge transformation, go templates docker, 自定义, 模板, 转换
---

{{< summary-bar feature_name="Compose bridge" >}}

本页介绍 Compose Bridge 如何利用模板将 Docker Compose 文件高效地转换为 Kubernetes 清单。它还介绍了如何根据您的特定要求和需求自定义这些模板，或者如何构建自己的转换。

## 工作原理

Compose Bridge 使用转换让您可以将 Compose 模型转换为另一种形式。

转换被打包为一个 Docker 镜像，它接收完全解析的 Compose 模型作为 `/in/compose.yaml`，并可以在 `/out` 下生成任何目标格式的文件。

Compose Bridge 包含一个使用 Go 模板的默认 Kubernetes 转换，您可以通过替换或扩展模板来自定义该转换。

### 语法

Compose Bridge 利用模板将 Compose 配置文件转换为 Kubernetes 清单。模板是使用 [Go 模板语法](https://pkg.go.dev/text/template)的纯文本文件。这使得可以插入逻辑和数据，使模板根据 Compose 模型变得动态和适应性强。

当模板执行时，它必须生成一个 YAML 文件，这是 Kubernetes 清单的标准格式。只要用 `---` 分隔，就可以生成多个文件。

每个 YAML 输出文件都以自定义的标题表示法开头，例如：

```yaml
#! manifest.yaml
```

在以下示例中，模板遍历 `compose.yaml` 文件中定义的服务。对于每个服务，都会生成一个专用的 Kubernetes 清单文件，根据服务命名并包含指定的配置。

```yaml
{{ range $name, $service := .services }}
---
#! {{ $name }}-manifest.yaml
# 生成的代码，请勿编辑
key: value
## ...
{{ end }}
```

### 输入

您可以通过运行 `docker compose config` 来生成输入模型。这个规范的 YAML 输出作为 Compose Bridge 转换的输入。在模板中，使用点表示法访问 `compose.yaml` 中的数据，允许您浏览嵌套的数据结构。例如，要访问服务的部署模式，您将使用 `service.deploy.mode`：

 ```yaml
# 遍历 yaml 序列
{{ range $name, $service := .services }}
  # 使用点表示法访问嵌套属性
  {{ if eq $service.deploy.mode "global" }}
kind: DaemonSet
  {{ end }}
{{ end }}
```

您可以查看 [Compose 规范 JSON 模式](https://github.com/compose-spec/compose-go/blob/main/schema/compose-spec.json)以全面了解 Compose 模型。此模式概述了 Compose 模型中所有可能的配置及其数据类型。

### 帮助程序

作为 Go 模板语法的一部分，Compose Bridge 提供了一组 YAML 帮助程序函数，旨在有效地操作模板中的数据：

- `seconds`：将[持续时间](/reference/compose-file/extension.md#specifying-durations)转换为整数
- `uppercase`：将字符串转换为大写字符
- `title`：通过将每个单词的首字母大写来转换字符串
- `safe`：将字符串转换为安全标识符，将所有字符（小写 a-z 除外）替换为 `-`
- `truncate`：从列表中删除 N 个第一个元素
- `join`：使用分隔符将列表中的元素分组为单个字符串
- `base64`：将字符串编码为 base64，用于在 Kubernetes 中编码密钥
- `map`：根据表示为 `"value -> newValue"` 字符串的映射转换值
- `indent`：将字符串内容缩进 N 个空格
- `helmValue`：将字符串内容作为模板值写入最终文件

在以下示例中，模板检查是否为服务指定了健康检查间隔，应用 `seconds` 函数将此间隔转换为秒，并将该值分配给 `periodSeconds` 属性。

```yaml
{{ if $service.healthcheck.interval }}
            periodSeconds: {{ $service.healthcheck.interval | seconds }}{{ end }}
{{ end }}
```

## 自定义

由于 Kubernetes 是一个多功能的平台，因此有很多方法可以将 Compose 概念映射到 Kubernetes 资源定义中。Compose Bridge 允许您自定义转换以匹配您自己的基础架构决策和偏好，具有不同程度的灵活性和工作量。

### 修改默认模板

您可以通过运行 `docker compose bridge transformations create --from docker/compose-bridge-kubernetes my-template` 来提取默认转换 `docker/compose-bridge-kubernetes` 使用的模板，并调整模板以满足您的需求。

模板被提取到一个以您的模板名称命名的目录中，在本例中为 `my-template`。
它包括一个 Dockerfile，可让您创建自己的镜像来分发您的模板，以及一个包含模板文件的目录。
您可以自由编辑现有文件、删除它们或[添加新文件](#add-your-own-templates)以随后生成满足您需求的 Kubernetes 清单。
然后，您可以使用生成的 Dockerfile 将您的更改打包到一个新的转换镜像中，然后您可以将该镜像与 Compose Bridge 一起使用：

```console
$ docker build --tag mycompany/transform --push .
```

然后，您可以将您的转换用作替代品：

```console
$ docker compose bridge convert --transformations mycompany/transform 
```

### 添加您自己的模板

对于 Compose Bridge 默认转换未管理的资源，您可以构建自己的模板。`compose.yaml` 模型可能无法提供填充目标清单所需的所有配置属性。如果是这种情况，您可以依赖 Compose 自定义扩展来更好地描述应用程序，并提供与平台无关的转换。

例如，如果您将 `x-virtual-host` 元数据添加到 `compose.yaml` 文件中的服务定义中，您可以使用以下自定义属性来生成 Ingress 规则：

```yaml
{{ $project := .name }}
#! {{ $name }}-ingress.yaml
# 生成的代码，请勿编辑
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

一旦打包到 Docker 镜像中，您就可以在将 Compose 模型转换为 Kubernetes 时使用此自定义模板，以及其他转换：

```console
$ docker compose bridge convert \
    --transformation docker/compose-bridge-kubernetes \
    --transformation mycompany/transform 
```

### 构建您自己的转换

虽然 Compose Bridge 模板可以轻松地进行最少的更改进行自定义，但您可能希望进行重大更改，或者依赖于现有的转换工具。

Compose Bridge 转换是一个 Docker 镜像，旨在从 `/in/compose.yaml` 获取 Compose 模型并在 `/out` 下生成平台清单。这个简单的约定使得使用 [Kompose](https://kompose.io/) 捆绑备用转换变得容易：

```Dockerfile
FROM alpine

# 从 github 发布页面获取 kompose
RUN apk add --no-cache curl
ARG VERSION=1.32.0
RUN ARCH=$(uname -m | sed 's/armv7l/arm/g' | sed 's/aarch64/arm64/g' | sed 's/x86_64/amd64/g') && \
    curl -fsL \
    "https://github.com/kubernetes/kompose/releases/download/v${VERSION}/kompose-linux-${ARCH}" \
    -o /usr/bin/kompose
RUN chmod +x /usr/bin/kompose

CMD ["/usr/bin/kompose", "convert", "-f", "/in/compose.yaml", "--out", "/out"]
```

此 Dockerfile 捆绑了 Kompose 并定义了根据 Compose Bridge 转换合同运行此工具的命令。
