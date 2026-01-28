---
_build:
  list: never
  publishResources: false
  render: never
---

# 关于这些文件

此目录中的文件是存根文件，它们包含了 `/_includes/cli.md` 文件，该文件解析从 [`docker/cli`](https://github.com/docker/cli) 仓库生成的 YAML 文件。这些 YAML 文件被解析后生成类似 </reference/cli/docker/build/> 的输出文件。

## 输出是如何生成的

输出文件由两个来源组成：

- **描述（Description）** 和 **用法（Usage）** 部分直接来自该仓库中的 CLI 源代码。

- **扩展描述（Extended Description）** 和 **示例（Examples）** 部分从以下位置拉取到 YAML 中：Docker CLI 命令来自 [https://github.com/docker/cli/tree/master/docs/reference/commandline](https://github.com/docker/cli/tree/master/docs/reference/commandline)，Docker Compose 命令来自 [https://github.com/docker/compose/tree/v2/docs/reference](https://github.com/docker/compose/tree/v2/docs/reference)。具体来说，会解析 `## Description` 和 `## Examples` 标题下的 Markdown 内容。请向这些仓库提交文本更正。

## 更新 YAML 文件

生成 YAML 文件的流程仍在调整中。请联系 @thaJeztah 确认。请确保使用正确的 `docker/cli` 发布分支（例如 `19.03` 分支）来生成 YAML 文件。

生成 YAML 文件后，将 [https://github.com/docker/docs/tree/main/_data/engine-cli](https://github.com/docker/docs/tree/main/_data/engine-cli) 中的 YAML 文件替换为新生成的文件，然后提交拉取请求。
