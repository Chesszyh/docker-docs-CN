---
title: 源文件约定
description: 如何格式化新的 .md 文件
keywords: 源文件, 贡献, 风格指南
weight: 30
---

## 文件名

当您为新内容创建新的 .md 文件时，请确保：
- 文件名尽可能短
- 尽量将文件名保持在一个或两个单词
- 使用破折号分隔单词。例如：
  - `add-seats.md` 和 `remove-seats.md`。
  - `multiplatform-images` 优于 `multi-platform-images`。

## Front matter

给定页面的 front matter 位于 Markdown 文件顶部的部分，以三个连字符开始和结束。它包含 YAML 内容。
支持以下键。标题、描述和关键字是必需的。

| 键 | 必需 | 描述 |
|---|---|---|
| title | 是 | 页面标题。这会作为 `<h1>` 级别的标题添加到 HTML 输出中。 |
| description | 是 | 描述页面内容的句子。这会添加到 HTML 元数据中。它不会在页面上呈现。 |
| keywords | 是 | 以逗号分隔的关键字列表。这些会添加到 HTML 元数据中。 |
| aliases | 否 | 应重定向到当前页面的页面 YAML 列表。在构建时，此处列出的每个页面都会��建一个 HTML 存根，其中包含到此页面的 302 重定向。 |
| notoc | 否 | `true` 或 `false`。如果为 `true`，则不会为此页面的 HTML 输出生成页内 TOC。默认为 `false`。适用于某些没有页内标题的登录页面。 |
| toc_min | 否 | 如果 `notoc` 设置为 `true`，则忽略。页内 TOC 中包含的最低标题级别。默认为 `2`，以显示 `<h2>` 标题为最低级别。 |
| toc_max | 否 | 如果 `notoc` 设置为 `false`，则忽略。页内 TOC 中包含的最高标题级别。默认为 `3`，以显示 `<h3>` 标题。设置为与 `toc_min` 相同，以仅显示 `toc_min` 级别的标题。 |
| sitemap | 否 | 从搜索引擎索引中排除该页面。当设置为 `false` 时，该页面将从 `sitemap.xml` 中排除，并且会将 `<meta name="robots" content="noindex"/>` 标头添加到该页面。 |
| sidebar.reverse | 否 | 此部分页面的此参数会更改该部分中页面的排序顺序。通常按权重或标题显示在顶部的页面将改为显示在底部附近，反之亦然。 |
| sidebar.goto | 否 | 设置此项以更改侧边栏应为此条目指向的 URL。请参阅[无页面侧边栏条目](#pageless-sidebar-entries)。 |
| sidebar.badge | 否 | 设置此项以为此页面的侧边栏条目添加徽章。此参数选项包含两个字段：`badge.text` 和 `badge.color`。 |

这是一个有效（但经过精心设计）的页面元数据示例。
front matter 中元数据元素的顺序并不重要。

```text
---
description: 在 Ubuntu 上安装 Docker 引擎的说明
keywords: 要求, apt, 安装, ubuntu, 安装, 卸载, 升级, 更新
title: 在 Ubuntu 上安装 Docker 引擎
aliases:
- /ee/docker-ee/ubuntu/
- /engine/installation/linux/docker-ce/ubuntu/
- /engine/installation/linux/docker-ee/ubuntu/
- /engine/installation/linux/ubuntu/
- /engine/installation/linux/ubuntulinux/
- /engine/installation/ubuntulinux/
- /install/linux/docker-ce/ubuntu/
- /install/linux/docker-ee/ubuntu/
- /install/linux/ubuntu/
- /installation/ubuntulinux/
toc_max: 4
---
```

## 正文

页面的正文（关键字除外）在 front matter 之后开始。

### 文本长度

拆分长行（最好最多 80 个字符）可以更轻松地就小块文本提供反馈。

## 无页面侧边栏条目

如果您想向侧边栏添加条目，但希望链接指向其他位置，则可以使用 `sidebar.goto` 参数。
这与设置为 `always` 的 `build.render` 结合使用非常有用，它会在侧边栏中创建一个无页面的条目，该条目链接到另一个页面。

```text
---
title: 虚拟侧边栏链接
build:
  render: never
sidebar:
  goto: /some/other/page/
weight: 30
---
```
