---
description: CLI and log output formatting reference
keywords: format, formatting, output, templates, log
title: Format command and log output
weight: 40
aliases:
  - /engine/admin/formatting/
  - /config/formatting/
---

Docker 支持 [Go 模板](https://golang.org/pkg/text/template/)，您可以使用它来操控某些命令和日志驱动程序的输出格式。

Docker 提供了一组基本函数来操作模板元素。
以下所有示例都使用 `docker inspect` 命令，但许多其他 CLI 命令都有 `--format` 标志，许多 CLI 命令参考都包含自定义输出格式的示例。

> [!NOTE]
>
> 使用 `--format` 标志时，您需要注意您的 shell 环境。
> 在 POSIX shell 中，您可以使用单引号运行以下命令：
>
> ```console
> $ docker inspect --format '{{join .Args " , "}}'
> ```
>
> 否则，在 Windows shell（例如 PowerShell）中，您需要使用单引号，但要转义参数内的双引号，如下所示：
>
> ```console
> $ docker inspect --format '{{join .Args \" , \"}}'
> ```
>

## join

`join` 连接字符串列表以创建单个字符串。
它在列表中的每个元素之间放置一个分隔符。

```console
$ docker inspect --format '{{join .Args " , "}}' container
```

## table

`table` 指定您想要查看其输出的字段。

```console
$ docker image list --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## json

`json` 将元素编码为 json 字符串。

```console
$ docker inspect --format '{{json .Mounts}}' container
```

## lower

`lower` 将字符串转换为小写表示形式。

```console
$ docker inspect --format "{{lower .Name}}" container
```

## split

`split` 将字符串按分隔符切分为字符串列表。

```console
$ docker inspect --format '{{split .Image ":"}}' container
```

## title

`title` 将字符串的首字符大写。

```console
$ docker inspect --format "{{title .Name}}" container
```

## upper

`upper` 将字符串转换为大写表示形式。

```console
$ docker inspect --format "{{upper .Name}}" container
```

## pad

`pad` 向字符串添加空白填充。您可以指定在字符串前后添加的空格数。

```console
$ docker image list --format '{{pad .Repository 5 10}}'
```

此示例在镜像仓库名称前添加 5 个空格，在名称后添加 10 个空格。

## truncate

`truncate` 将字符串缩短到指定长度。如果字符串短于指定长度，则保持不变。

```console
$ docker image list --format '{{truncate .Repository 15}}'
```

此示例显示镜像仓库名称，如果超过 15 个字符则截断为前 15 个字符。

## println

`println` 将每个值打印在新行上。

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' container
```

## 提示

要找出可以打印哪些数据，可以将所有内容显示为 json：

```console
$ docker container ls --format='{{json .}}'
```
