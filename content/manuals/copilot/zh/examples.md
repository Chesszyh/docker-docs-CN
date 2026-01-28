---
title: Docker 代理的示例提示词
linkTitle: 示例提示词
description: |
  探索与 Docker 代理交互的示例提示词，了解如何自动化执行诸如项目 Docker 化或创建拉取请求等任务。
weight: 30
---

{{< summary-bar feature_name="Docker GitHub Copilot" >}}

## 使用场景

以下是您可以向 Docker 代理提问的一些问题类型示例：

### 询问一般的 Docker 问题

您可以询问关于 Docker 的一般性问题。例如：

- `@docker what is a Dockerfile?`
- `@docker how do I build a Docker image?`
- `@docker how do I run a Docker container?`
- `@docker what does 'docker buildx imagetools inspect' do?`

### 获取项目容器化帮助

您可以请求代理帮助您容器化现有项目：

- `@docker can you help create a compose file for this project?`
- `@docker can you create a Dockerfile for this project?`

#### 创建拉取请求

Docker 代理将分析您的项目，生成必要的文件，并在适用的情况下，提议使用必要的 Docker 资产创建拉取请求。

自动针对您的仓库创建拉取请求的功能仅在代理生成新的 Docker 资产时可用。

### 分析项目漏洞

代理可以帮助您通过 [Docker Scout](/manuals/scout/_index.md) 改善安全状况：

- `@docker can you help me find vulnerabilities in my project?`
- `@docker does my project contain any insecure dependencies?`

代理将使用 Docker Scout 分析您项目的依赖项，并报告您是否存在任何[已知 CVE（常见漏洞和暴露）](/manuals/scout/deep-dive/advisory-db-sources.md)的风险。

![Copilot 漏洞报告](images/copilot-vuln-report.png?w=500px&border=1)

## 限制

- 代理目前无法访问您仓库中的特定文件，例如编辑器中当前打开的文件，或者您在聊天消息中传递的文件引用。

## 反馈

如有问题或反馈，请访问 [GitHub 反馈仓库](https://github.com/docker/copilot-issues)。
