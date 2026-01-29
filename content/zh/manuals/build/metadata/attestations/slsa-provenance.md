--- 
title: 来源证明 (Provenance attestations)
keywords: build, attestations, provenance, slsa, git, metadata
description: >
  来源构建证明描述了镜像如何构建以及在何处构建。
---

来源证明包含关于构建过程的事实，包括以下细节：

- 构建时间戳
- 构建参数和环境
- 版本控制元数据
- 源代码详情
- 构建过程中消耗的材料（文件、脚本）

来源证明遵循 [SLSA 来源架构版本 0.2](https://slsa.dev/provenance/v0.2#schema)。

有关 BuildKit 如何填充这些来源属性的更多信息，请参阅 [SLSA 定义](slsa-definitions.md)。

## 创建来源证明

要创建来源证明，请将 `--attest type=provenance` 选项传递给 `docker buildx build` 命令：

```console
$ docker buildx build --tag <namespace>/<image>:<version> \
    --attest type=provenance,mode=[min,max] .
```

或者，您可以使用简写选项 `--provenance=true` 代替 `--attest type=provenance`。要使用简写选项指定 `mode` 参数，请使用：`--provenance=mode=max`。

有关如何通过 GitHub Actions 添加来源证明的示例，请参阅 [使用 GitHub Actions 添加证明](/manuals/build/ci/github-actions/attestations.md)。

## 模式 (Mode)

您可以使用 `mode` 参数来定义包含在来源证明中的详细程度。支持的值有 `mode=min`（默认）和 `mode=max`。

### 最小模式 (Min)

在 `min` 模式下，来源证明包含最少的信息集，例如：

- 构建时间戳
- 所使用的前端
- 构建材料
- 源码库及修订版本
- 构建平台
- 可复现性

构建参数的值、密钥的标识以及丰富的层元数据不包含在 `mode=min` 中。`min` 级别的来源证明可以安全地用于所有构建，因为它不会泄露构建环境任何部分的敏感信息。

以下 JSON 示例显示了使用 `min` 模式创建的来源证明中包含的信息：

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://slsa.dev/provenance/v0.2",
  "subject": [
    {
      "name": "pkg:docker/<registry>/<image>@<tag/digest>?platform=<platform>",
      "digest": {
        "sha256": "e8275b2b76280af67e26f068e5d585eb905f8dfd2f1918b3229db98133cb4862"
      }
    }
  ],
  "predicate": {
    "builder": { "id": "" },
    "buildType": "https://mobyproject.org/buildkit@v1",
    "materials": [
      {
        "uri": "pkg:docker/docker/dockerfile@1",
        "digest": {
          "sha256": "9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1a0dbc"
        }
      },
      {
        "uri": "pkg:docker/golang@1.19.4-alpine?platform=linux%2Farm64",
        "digest": {
          "sha256": "a9b24b67dc83b3383d22a14941c2b2b2ca6a103d805cac6820fd1355943beaf1"
        }
      }
    ],
    "invocation": {
      "configSource": { "entryPoint": "Dockerfile" },
      "parameters": {
        "frontend": "gateway.v0",
        "args": {
          "cmdline": "docker/dockerfile:1",
          "source": "docker/dockerfile:1",
          "target": "binaries"
        },
        "locals": [{ "name": "context" }, { "name": "dockerfile" }]
      },
      "environment": { "platform": "linux/arm64" }
    },
    "metadata": {
      "buildInvocationID": "c4a87v0sxhliuewig10gnsb6v",
      "buildStartedOn": "2022-12-16T08:26:28.651359794Z",
      "buildFinishedOn": "2022-12-16T08:26:29.625483253Z",
      "reproducible": false,
      "completeness": {
        "parameters": true,
        "environment": true,
        "materials": false
      },
      "https://mobyproject.org/buildkit@v1#metadata": {
        "vcs": {
          "revision": "a9ba846486420e07d30db1107411ac3697ecab68",
          "source": "git@github.com:<org>/<repo>.git"
        }
      }
    }
  }
}
```

### 最大模式 (Max)

`max` 模式包含了 `min` 模式中的所有信息，以及：

- 构建的 LLB 定义。这些显示了生成镜像所采取的确切步骤。
- 关于 Dockerfile 的信息，包括文件的完整 base64 编码版本。
- 描述构建步骤与镜像层之间关系的源码映射 (Source maps)。

只要可能，您应该优先选择 `mode=max`，因为它包含更多详细信息供分析。

> [!WARNING]
> 
> 请注意，`mode=max` 会暴露 [构建参数](/reference/cli/docker/buildx/build.md#build-arg) 的值。
> 
> 如果您滥用构建参数来传递凭据、身份验证令牌或其他密钥，则应重构构建，改用 [密钥挂载](/reference/cli/docker/buildx/build.md#secret) 传递密钥。密钥挂载不会泄露到构建之外，且绝不会包含在来源证明中。

## 检查来源证明

要探索通过 `image` 导出器导出的已创建来源证明，可以使用 [`imagetools inspect`](/reference/cli/docker/buildx/imagetools/inspect.md)。

使用 `--format` 选项，您可以为输出指定一个模板。所有与来源相关的数据都在 `.Provenance` 属性下可用。例如，获取 SLSA 格式的来源证明原始内容：

```console
$ docker buildx imagetools inspect <namespace>/<image>:<version> \
    --format "{{ json .Provenance.SLSA }}"
{
  "buildType": "https://mobyproject.org/buildkit@v1",
  ...
}
```

您还可以利用 Go 模板的完整功能构建更复杂的表达式。例如，对于使用 `mode=max` 生成的来源证明，您可以提取用于构建镜像的 Dockerfile 的完整源代码：

```console
$ docker buildx imagetools inspect <namespace>/<image>:<version> \
    --format '{{ range (index .Provenance.SLSA.metadata "https://mobyproject.org/buildkit@v1#metadata").source.infos }}{{ if eq .filename "Dockerfile" }}{{ .data }}{{ end }}{{ end }}' | base64 -d
FROM ubuntu:24.04
RUN apt-get update
...
```

## 来源证明示例

<!-- TODO: add a link to the definitions page, imported from moby/buildkit -->

以下示例展示了带有 `mode=max` 的来源证明的 JSON 表示形式：

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://slsa.dev/provenance/v0.2",
  "subject": [
    {
      "name": "pkg:docker/<registry>/<image>@<tag/digest>?platform=<platform>",
      "digest": {
        "sha256": "e8275b2b76280af67e26f068e5d585eb905f8dfd2f1918b3229db98133cb4862"
      }
    }
  ],
  "predicate": {
    "builder": { "id": "" },
    "buildType": "https://mobyproject.org/buildkit@v1",
    "materials": [
      {
        "uri": "pkg:docker/docker/dockerfile@1",
        "digest": {
          "sha256": "9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1a0dbc"
        }
      },
      {
        "uri": "pkg:docker/golang@1.19.4-alpine?platform=linux%2Farm64",
        "digest": {
          "sha256": "a9b24b67dc83b3383d22a14941c2b2b2ca6a103d805cac6820fd1355943beaf1"
        }
      }
    ],
    "buildConfig": {
      "llbDefinition": [
        {
          "id": "step4",
          "op": {
            "Op": {
              "exec": {
                "meta": {
                  "args": ["/bin/sh", "-c", "go mod download -x"],
                  "env": [
                    "PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                    "GOLANG_VERSION=1.19.4",
                    "GOPATH=/go",
                    "CGO_ENABLED=0"
                  ],
                  "cwd": "/src"
                },
                "mounts": [
                  { "input": 0, "dest": "/", "output": 0 },
                  {
                    "input": -1,
                    "dest": "/go/pkg/mod",
                    "output": -1,
                    "mountType": 3,
                    "cacheOpt": { "ID": "//go/pkg/mod" }
                  },
                  {
                    "input": 1,
                    "selector": "/go.mod",
                    "dest": "/src/go.mod",
                    "output": -1,
                    "readonly": true
                  },
                  {
                    "input": 1,
                    "selector": "/go.sum",
                    "dest": "/src/go.sum",
                    "output": -1,
                    "readonly": true
                  }
                ]
              }
            },
            "platform": { "Architecture": "arm64", "OS": "linux" },
            "constraints": {}
          },
          "inputs": ["step3:0", "step1:0"]
        }
      ]
    },
    "metadata": {
      "buildInvocationID": "edf52vxjyf9b6o5qd7vgx0gru",
      "buildStartedOn": "2022-12-15T15:38:13.391980297Z",
      "buildFinishedOn": "2022-12-15T15:38:14.274565297Z",
      "reproducible": false,
      "completeness": {
        "parameters": true,
        "environment": true,
        "materials": false
      },
      "https://mobyproject.org/buildkit@v1#metadata": {
        "vcs": {
          "revision": "a9ba846486420e07d30db1107411ac3697ecab68-dirty",
          "source": "git@github.com:<org>/<repo>.git"
        },
        "source": {
          "locations": {
            "step4": {
              "locations": [
                {
                  "ranges": [
                    { "start": { "line": 5 }, "end": { "line": 5 } },
                    { "start": { "line": 6 }, "end": { "line": 6 } },
                    { "start": { "line": 7 }, "end": { "line": 7 } },
                    { "start": { "line": 8 }, "end": { "line": 8 } }
                  ]
                }
              ]
            }
          },
          "infos": [
            {
              "filename": "Dockerfile",
              "data": "RlJPTSBhbHBpbmU6bGF0ZXN0Cg==",
              "llbDefinition": [
                {
                  "id": "step0",
                  "op": {
                    "Op": {
                      "source": {
                        "identifier": "local://dockerfile",
                        "attrs": {
                          "local.differ": "none",
                          "local.followpaths": "[\"Dockerfile\",\"Dockerfile.dockerignore\",\"dockerfile\"]",
                          "local.session": "s4j58ngehdal1b5hn7msiqaqe",
                          "local.sharedkeyhint": "dockerfile"
                        }
                      }
                    },
                    "constraints": {}
                  }
                },
                { "id": "step1", "op": { "Op": null }, "inputs": ["step0:0"] }
              ]
            }
          ]
        },
        "layers": {
          "step2:0": [
            [
              {
                "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                "digest": "sha256:261da4162673b93e5c0e7700a3718d40bcc086dbf24b1ec9b54bca0b82300626",
                "size": 3259190
              },
              {
                "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                "digest": "sha256:bc729abf26b5aade3c4426d388b5ea6907fe357dec915ac323bb2fa592d6288f",
                "size": 286218
              },
              {
                "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                "digest": "sha256:7f1d6579712341e8062db43195deb2d84f63b0f2d1ed7c3d2074891085ea1b56",
                "size": 116878653
              },
              {
                "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                "digest": "sha256:652874aefa1343799c619d092ab9280b25f96d97939d5d796437e7288f5599c9",
                "size": 156
              }
            ]
          ]
        }
      }
    }
  }
}
