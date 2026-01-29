---
title: 自定义 Compose Bridge 
linkTitle: 自定义
weight: 20
description: 了解如何使用 Go 模板和 Compose 扩展自定义 Compose Bridge 转换
keywords: docker compose bridge, 自定义 compose bridge, compose bridge 模板, compose 转 kubernetes, compose bridge 转换, go 模板 docker

---

{{< summary-bar feature_name="Compose bridge" >}}

本页介绍了 Compose Bridge 如何利用模板化技术高效地将 Docker Compose 文件翻译为 Kubernetes 清单。它还说明了如何根据特定要求和需求自定义这些模板，以及如何构建自己的转换（transformation）。

## 工作原理 

Compose bridge 使用转换功能让您将 Compose 模型转换为另一种形式。 

转换被打包为一个 Docker 镜像，它接收完全解析后的 Compose 模型（作为 `/in/compose.yaml`），并可以在 `/out` 下生成任何目标格式的文件。

Compose Bridge 包含一个使用 Go 模板的默认 Kubernetes 转换，您可以通过替换或扩展模板来进行自定义。

### 语法

Compose Bridge 使用模板将 Compose 配置文件转换为 Kubernetes 清单。模板是使用 [Go 模板语法](https://pkg.go.dev/text/template) 的纯文本文件。这支持插入逻辑和数据，使模板能够根据 Compose 模型动态调整。

执行模板时，它必须生成一个 YAML 文件，这是 Kubernetes 清单的标准格式。只要使用 `---` 分隔，就可以生成多个文件。

每个 YAML 输出文件都以自定义标题表示法开始，例如：

```yaml
#! manifest.yaml
```

在以下示例中，模板迭代 `compose.yaml` 文件中定义的各服务。对于每个服务，都会生成一个专用的 Kubernetes 清单文件，其名称根据服务命名并包含指定的配置。

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

您可以通过运行 `docker compose config` 生成输入模型。此规范的 YAML 输出作为 Compose Bridge 转换的输入。在模板内部，使用点号表示法访问来自 `compose.yaml` 的数据，从而允许您在嵌套的数据结构中进行导航。例如，要访问服务的部署模式，您可以使用 `service.deploy.mode`：

 ```yaml
# 迭代 yaml 序列
{{ range $name, $service := .services }}  # 使用点号表示法访问嵌套属性
  {{ if eq $service.deploy.mode "global" }}
kind: DaemonSet
  {{ end }}
{{ end }}
```

您可以查看 [Compose 规范 JSON 模式](https://github.com/compose-spec/compose-go/blob/main/schema/compose-spec.json) 以获取 Compose 模型的完整概览。此模式概述了 Compose 模型中所有可能的配置及其数据类型。 

### 助手函数 (Helpers)

作为 Go 模板语法的一部分，Compose Bridge 提供了一组 YAML 助手函数，旨在高效地操作模板中的数据：

- `seconds`：将 [时长](/reference/compose-file/extension.md#specifying-durations) 转换为整数
- `uppercase`：将字符串转换为大写
- `title`：将字符串中每个单词的首字母大写
- `safe`：将字符串转换为安全标识符，将除小写 a-z 以外的所有字符替换为 `-`
- `truncate`：从列表中移除前 N 个元素
- `join`：使用分隔符将列表中的元素组合成单个字符串
- `base64`：将字符串编码为 base64，Kubernetes 中用于编码 secret
- `map`：根据以 `"value -> newValue"` 字符串表示的映射来转换值 
- `indent`：以 N 个空格的缩进编写字符串内容
- `helmValue`：在最终文件中将字符串内容编写为模板值

在以下示例中，模板检查是否为服务指定了运行状况检查间隔，应用 `seconds` 函数将该间隔转换为秒，并将该值分配给 `periodSeconds` 属性。

```yaml
{{ if $service.healthcheck.interval }}
            periodSeconds: {{ $service.healthcheck.interval | seconds }}{{ end }}
{{ end }}
```

## 自定义

由于 Kubernetes 是一个多功能平台，有许多方法可以将 Compose 概念映射到 Kubernetes 资源定义中。Compose Bridge 允许您自定义转换，以匹配您自己的基础设施决策和偏好，具有不同级别的灵活性和工作量。

### 修改默认模板

您可以通过运行 `docker compose bridge transformations create --from docker/compose-bridge-kubernetes my-template` 提取默认转换 `docker/compose-bridge-kubernetes` 使用的模板，并根据需要调整模板。 

模板会被提取到以您的模板名称命名的目录中（本例中为 `my-template`）。它包含一个允许您创建自己的镜像以分发模板的 Dockerfile，以及一个包含模板文件的目录。您可以自由编辑现有文件、删除它们或 [添加新文件](#添加您自己的模板)，以便随后生成满足您需求的 Kubernetes 清单。然后，您可以使用生成的 Dockerfile 将更改打包到新的转换镜像中，随后即可与 Compose Bridge 配合使用：

```console
$ docker build --tag mycompany/transform --push .
```

然后，您可以使用您的转换作为替代方案：

```console
$ docker compose bridge convert --transformations mycompany/transform 
```

### 添加您自己的模板

对于 Compose Bridge 默认转换未管理的资源，您可以构建自己的模板。`compose.yaml` 模型可能无法提供填充目标清单所需的所有配置属性。如果是这种情况，您可以依赖 Compose 自定义扩展来更好地描述应用程序，并提供一种不可知（agnostic）的转换。 

例如，如果您在 `compose.yaml` 文件的服务定义中添加了 `x-virtual-host` 元数据，可以使用以下自定义属性来生成 Ingress 规则：

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

打包到 Docker 镜像后，在将 Compose 模型转换为 Kubernetes 时，除了其他转换外，您还可以使用此自定义模板：

```console
$ docker compose bridge convert \
    --transformation docker/compose-bridge-kubernetes \
    --transformation mycompany/transform 
```

### 构建您自己的转换

虽然 Compose Bridge 模板可以轻松进行最小限度修改的自定义，但您可能希望进行重大更改，或者依赖现有的转换工具。

Compose Bridge 转换是一个 Docker 镜像，旨在从 `/in/compose.yaml` 获取 Compose 模型，并在 `/out` 下生成平台清单。这个简单的契约使得使用 [Kompose](https://kompose.io/) 捆绑替代转换变得容易：

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

此 Dockerfile 捆绑了 Kompose，并根据 Compose Bridge 转换契约定义了运行此工具的命令。

