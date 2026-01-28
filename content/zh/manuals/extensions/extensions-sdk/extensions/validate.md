---
title: 验证您的扩展
linkTitle: 验证
description: 扩展创建过程的第三步
keywords: Docker, Extensions, sdk, validate, install
aliases:
 - /desktop/extensions-sdk/extensions/validation/
 - /desktop/extensions-sdk/build/build-install/
 - /desktop/extensions-sdk/dev/cli/build-test-install-extension/
 - /desktop/extensions-sdk/extensions/validate/
weight: 20
---

在分享或发布扩展之前，请先验证您的扩展。验证扩展可确保该扩展：

- 使用在 Marketplace 中正确显示所需的[镜像标签](labels.md)构建
- 可以正常安装和运行

Extensions CLI 允许您在本地安装和运行扩展之前验证它。

验证会检查扩展的 `Dockerfile` 是否指定了所有必需的标签，以及元数据文件是否符合 JSON schema 文件的规范。

要验证，请运行：

```console
$ docker extension validate <name-of-your-extension>
```

如果您的扩展有效，将显示以下消息：

```console
The extension image "name-of-your-extension" is valid
```

在构建镜像之前，也可以仅验证 `metadata.json` 文件：

```console
$ docker extension validate /path/to/metadata.json
```

用于验证 `metadata.json` 文件的 JSON schema 可以在[发布页面](https://github.com/docker/extensions-sdk/releases/latest)找到。
