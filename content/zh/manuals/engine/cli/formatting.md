---
description: CLI 和日志输出格式化参考
keywords: format, formatting, output, templates, log, 格式化, 输出, 模板
title: 格式化命令和日志输出
weight: 40
alias:
  - /engine/admin/formatting/
  - /config/formatting/
---

Docker 支持 [Go 模板 (Go templates)](https://golang.org/pkg/text/template/)，您可以使用它来操纵某些命令和日志驱动程序的输出格式。

Docker 提供了一组基本函数来处理模板元素。以下所有示例均使用 `docker inspect` 命令，但许多其他 CLI 命令也具有 `--format` 标志，并且许多 CLI 命令参考文档中都包含自定义输出格式的示例。

> [!NOTE]
>
> 使用 `--format` 标志时，您需要注意您的 shell 环境。
> 在 POSIX shell (如 Linux/macOS 的 Bash) 中，您可以使用单引号运行以下命令：
>
> ```console
> $ docker inspect --format '{{join .Args " , "}}'
> ```
>
> 否则，在 Windows shell (例如 PowerShell) 中，您需要使用单引号，但要按如下方式转义参数内部的双引号：
>
> ```console
> $ docker inspect --format '{{join .Args " , "}}'
> ```
>

## join

`join` 将字符串列表连接起来以创建一个单一字符串。它在列表中的每个元素之间放置一个分隔符。

```console
$ docker inspect --format '{{join .Args " , "}}' container
```

## table

`table` 指定您希望在其输出中看到的字段。

```console
$ docker image list --format "table {{.ID}}	{{.Repository}}	{{.Tag}}	{{.Size}}"
```

## json

`json` 将元素编码为 json 字符串。

```console
$ docker inspect --format '{{json .Mounts}}' container
```

## lower

`lower` 将字符串转换为其小写表示形式。

```console
$ docker inspect --format "{{lower .Name}}" container
```

## split

`split` 将字符串切分为由分隔符分隔的字符串列表。

```console
$ docker inspect --format '{{split .Image ":"}}' container
```

## title

`title` 将字符串的首字母大写。

```console
$ docker inspect --format "{{title .Name}}" container
```

## upper

`upper` 将字符串转换为其大写表示形式。

```console
$ docker inspect --format "{{upper .Name}}" container
```

## pad

`pad` 为字符串添加空格填充。您可以指定在字符串之前和之后添加的空格数。

```console
$ docker image list --format '{{pad .Repository 5 10}}'
```

此示例在镜像仓库名称前添加 5 个空格，在后面添加 10 个空格。

## truncate

`truncate` 将字符串缩短到指定的长度。如果字符串短于指定的长度，则保持不变。

```console
$ docker image list --format '{{truncate .Repository 15}}'
```

此示例显示镜像仓库名称，如果长度超过 15 个字符，则将其截断为前 15 个字符。

## println

`println` 在新行打印每个值。

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' container
```

## 提示 (Hint)

要查出哪些数据可以打印，请将所有内容显示为 json：

```console
$ docker container ls --format='{{json .}}'
```

