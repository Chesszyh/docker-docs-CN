---
description: 了解不可变标签以及它们如何帮助在 Docker Hub 上保持镜像版本一致性。
keywords: Docker Hub, Hub, repository content, tags, immutable tags, version control
title: Docker Hub 上的不可变标签
linkTitle: 不可变标签
weight: 11
---
{{< summary-bar feature_name="Immutable tags" >}}

不可变标签（Immutable tags）提供了一种方式，确保特定的镜像版本在发布到 Docker Hub 后保持不变。此功能通过防止意外覆盖重要的镜像版本，帮助保持容器部署的一致性和可靠性。

## 什么是不可变标签？

不可变标签是一种镜像标签，一旦推送到 Docker Hub，就不能被覆盖或删除。这确保了镜像的特定版本在其整个生命周期中保持完全相同，提供以下优势：

- 版本一致性
- 可重复构建
- 防止意外覆盖
- 更好的安全性和合规性

## 启用不可变标签

要为您的仓库启用不可变标签：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 选择要启用不可变标签的仓库。
4. 转到 **Settings** > **General**。
5. 在 **Tag mutability settings** 下，选择以下选项之一：
   - **All tags are mutable (Default)**：
     标签可以更改为引用不同的镜像。这允许您在不创建新标签的情况下重新定向标签。
   - **All tags are immutable**：
     标签创建后不能更新为指向不同的镜像。这确保了一致性并防止意外更改。这包括 `latest` 标签。
   - **Specific tags are immutable**：
     使用正则表达式值定义创建后不能更新的特定标签。
6. 选择 **Save**。

启用后，所有标签都会锁定到其特定的镜像，确保每个标签始终指向相同的镜像版本且不能被修改。

> [!NOTE]
> 此正则表达式实现遵循 [Go regexp 包](https://pkg.go.dev/regexp)，该包基于 RE2 引擎。有关更多信息，请访问 [RE2 正则表达式语法](https://github.com/google/re2/wiki/Syntax)。

## 使用不可变标签

当启用不可变标签时：

- 您不能使用相同的标签名称推送新镜像
- 您必须为每个新镜像版本使用新的标签名称

要推送镜像，请为更新的镜像创建新标签并将其推送到仓库。
