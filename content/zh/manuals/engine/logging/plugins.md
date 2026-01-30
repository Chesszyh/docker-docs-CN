---
description: 了解用于扩展和自定义 Docker 日志能力的日志驱动程序插件
title: 使用日志驱动程序插件
keywords: logging, driver, plugins, monitoring, 日志, 驱动程序, 插件
---

Docker 日志插件允许您在 [内置日志驱动程序](configure.md) 之外，扩展和自定义 Docker 的日志能力。日志服务提供商可以 [实现自己的插件](/manuals/engine/extend/plugins_logging.md)，并将其发布在 Docker Hub 或私有注册表上。本主题展示了日志服务的使用者如何配置 Docker 以使用该插件。

## 安装日志驱动程序插件

要安装日志驱动程序插件，请使用 `docker plugin install <org/image>` 命令，具体取决于插件开发者提供的信息。

您可以使用 `docker plugin ls` 列出所有已安装的插件，也可以使用 `docker inspect` 检查特定插件。

## 将插件配置为默认日志驱动程序

安装插件后，您可以配置 Docker 守护进程将其作为默认驱动程序，方法是将插件名称设置为 `daemon.json` 中 `log-driver` 键的值，详见 [日志概览](configure.md#configure-the-default-logging-driver)。如果日志驱动程序支持额外选项，您可以在同一个文件中将它们设置为 `log-opts` 数组的值。

## 配置容器使用插件作为日志驱动程序

安装插件后，您可以通过向 `docker run` 指定 `--log-driver` 标志，配置容器使用该插件作为其日志驱动程序，详见 [日志概览](configure.md#configure-the-logging-driver-for-a-container)。如果日志驱动程序支持额外选项，您可以使用一个或多个 `--log-opt` 标志来指定它们，其中选项名称为键，选项值为值。
