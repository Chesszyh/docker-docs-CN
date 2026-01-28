---
title: 如何备份和恢复 Docker Desktop 数据
linkTitle: 备份和恢复数据
keywords: Docker Desktop, backup, restore, migration, reinstall, containers, images,
  volumes
weight: 20
aliases:
 - /desktop/backup-and-restore/
---

使用此流程来备份和恢复您的镜像和容器数据。如果您想要重置虚拟机磁盘或将 Docker 环境迁移到新计算机，这将非常有用。

> [!IMPORTANT]
>
> 如果您使用卷（volumes）或绑定挂载（bind-mounts）来存储容器数据，可能不需要备份您的容器，但请确保记住创建容器时使用的选项，或者使用 [Docker Compose 文件](/reference/compose-file/_index.md)（如果您想在重新安装后使用相同的配置重新创建容器）。

## 保存您的数据

1. 使用 [`docker container commit`](/reference/cli/docker/container/commit.md) 将容器提交为镜像。

   提交容器会将文件系统更改和一些容器配置（如标签和环境变量）存储为本地镜像。请注意，环境变量可能包含敏感信息（如密码或代理认证信息），因此在将生成的镜像推送到镜像仓库时请谨慎操作。

   另请注意，附加到容器的卷中的文件系统更改不包含在镜像中，必须单独备份。

   如果您使用[命名卷](/manuals/engine/storage/_index.md#more-details-about-mount-types)来存储容器数据（如数据库），请参阅存储部分中的[备份、恢复或迁移数据卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)页面。

2. 使用 [`docker push`](/reference/cli/docker/image/push.md) 将您在本地构建的任何想要保留的镜像推送到 [Docker Hub 镜像仓库](/manuals/docker-hub/_index.md)。

   > [!TIP]
   >
   > 如果您的镜像包含敏感内容，请[将仓库可见性设置为私有](/manuals/docker-hub/repos/_index.md)。

   或者，使用 [`docker image save -o images.tar image1 [image2 ...]`](/reference/cli/docker/image/save.md) 将您想要保留的任何镜像保存到本地 `.tar` 文件。

备份数据后，您可以卸载当前版本的 Docker Desktop 并[安装其他版本](/manuals/desktop/release-notes.md)或将 Docker Desktop 重置为出厂默认设置。

## 恢复您的数据

1. 加载您的镜像。

   - 如果您推送到了 Docker Hub：

      ```console
      $ docker pull <my-backup-image>
      ```

   - 如果您保存了 `.tar` 文件：

      ```console
      $ docker image load -i images.tar
      ```

2. 如果需要，使用 [`docker run`](/reference/cli/docker/container/run.md) 或 [Docker Compose](/manuals/compose/_index.md) 重新创建您的容器。

要恢复卷数据，请参阅[备份、恢复或迁移数据卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)。
