---
_build:
  list: never
  publishResources: false
  render: never
---

# 关于这些文件

此目录中的文件是存根文件，其中包含文件 `/_includes/cli.md`，该文件解析从 [`docker/cli`](https://github.com/docker/cli) 仓库生成的 YAML 文件。YAML 文件被解析为输出文件，例如 </reference/cli/docker/build/>。

## 输出的生成方式

输出文件由两个来源组成：

- **描述**和**用法**部分直接来自该仓库中的 CLI 源代码。

- **扩展描述**和**示例**部分从 [https://github.com/docker/cli/tree/master/docs/reference/commandline](https://github.com/docker/cli/tree/master/docs/reference/commandline) 中的文件（用于 Docker CLI 命令）和 [https://github.com/docker/compose/tree/v2/docs/reference](https://github.com/docker/compose/tree/v2/docs/reference) 中的文件（用于 Docker Compose 命令）拉取到 YAML 中。
  具体来说，解析 `## Description` 和 `## Examples` 标题内的 Markdown。请在这些仓库中提交文本更正。

## 更新 YAML 文件

生成 YAML 文件的过程仍在不断变化。请咨询 @thaJeztah。请务必使用 `docker/cli` 的正确发布分支生成 YAML 文件，例如 `19.03` 分支。

生成 YAML 文件后，将 [https://github.com/docker/docs/tree/main/_data/engine-cli](https://github.com/docker/docs/tree/main/_data/engine-cli) 中的 YAML 文件替换为新生成的文件。提交拉取请求。
