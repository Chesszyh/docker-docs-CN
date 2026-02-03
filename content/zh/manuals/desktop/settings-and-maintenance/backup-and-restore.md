---
title: 如何备份与还原您的 Docker Desktop 数据
linkTitle: 备份与还原数据
keywords: Docker Desktop, 备份, backup, 还原, restore, 迁移, 重新安装, 容器, 镜像, 卷
weight: 20
aliases:
 - /desktop/backup-and-restore/
---

按照此流程可以备份和还原您的镜像及容器数据。如果您想重置虚拟机磁盘，或将 Docker 环境迁移到新电脑，这将非常有用。

> [!IMPORTANT]
>
> 如果您使用卷（Volumes）或绑定挂载（Bind-mounts）来存储容器数据，则可能不需要备份容器本身。但在重新安装后，请务必记住创建容器时使用的选项，或者使用 [Docker Compose 文件](/reference/compose-file/_index.md) 以便按照相同的配置重新创建容器。

## 保存您的数据

1. 使用 [`docker container commit`](/reference/cli/docker/container/commit.md) 将您的容器提交为镜像。

   提交容器会将文件系统的更改以及某些容器配置（如标签和环境变量）保存为本地镜像。请注意，环境变量可能包含敏感信息（如密码或代理身份验证），因此在将生成的镜像推送到注册表时请务必小心。

   另请注意，挂载到容器的卷中的文件系统更改不会包含在镜像中，必须单独进行备份。

   如果您使用 [命名卷](/manuals/engine/storage/_index.md#更多关于挂载类型的详细信息) 来存储容器数据（如数据库），请参阅存储部分的 [备份、还原或迁移数据卷](/manuals/engine/storage/volumes.md#备份-还原或迁移数据卷) 页面。

2. 使用 [`docker push`](/reference/cli/docker/image/push.md) 将您在本地构建并希望保留的任何镜像推送到 [Docker Hub 注册表](/manuals/docker-hub/_index.md)。

   > [!TIP]
   >
   > 如果您的镜像包含敏感内容，请 [将存储库可见性设置为私有](/manuals/docker-hub/repos/_index.md)。

   或者，使用 [`docker image save -o images.tar image1 [image2 ...]`](/reference/cli/docker/image/save.md) 将您希望保留的任何镜像保存到本地 `.tar` 文件中。

备份数据后，您可以卸载当前版本的 Docker Desktop，[安装其他版本](/manuals/desktop/release-notes.md)，或将 Docker Desktop 恢复出厂设置。

## 还原您的数据

1. 加载您的镜像。

   - 如果您已推送到 Docker Hub：
   
      ```console
      $ docker pull <我的备份镜像>
      ```
   
   - 如果您保存了 `.tar` 文件：
   
      ```console
      $ docker image load -i images.tar
      ```

2. 根据需要，使用 [`docker run`](/reference/cli/docker/container/run.md) 或 [Docker Compose](/manuals/compose/_index.md) 重新创建您的容器。

要还原卷数据，请参阅 [备份、还原或迁移数据卷](/manuals/engine/storage/volumes.md#备份-还原或迁移数据卷)。