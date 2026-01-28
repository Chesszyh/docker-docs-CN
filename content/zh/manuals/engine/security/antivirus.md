---
title: 防病毒软件与 Docker
description: General guidelines for using antivirus software with Docker
keywords: antivirus, security
---

当防病毒软件扫描 Docker 使用的文件时，这些文件可能会以某种方式被锁定，导致 Docker 命令挂起。

减少这些问题的一种方法是将 Docker 数据目录（Linux 上为 `/var/lib/docker`，Windows Server 上为 `%ProgramData%\docker`，Mac 上为 `$HOME/Library/Containers/com.docker.docker/`）添加到防病毒软件的排除列表中。然而，这样做的代价是 Docker 镜像、容器的可写层或卷中的病毒或恶意软件将不会被检测到。如果你确实选择将 Docker 的数据目录从后台病毒扫描中排除，你可能需要安排一个定期任务，该任务会停止 Docker，扫描数据目录，然后重新启动 Docker。
