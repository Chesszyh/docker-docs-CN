--- 
description: 了解支持存储驱动程序的技术。
keywords: container, storage, driver, btrfs, overlayfs, vfs, zfs, 容器, 存储, 驱动程序
title: 存储驱动程序
weight: 40
---

为了有效地使用存储驱动程序，了解 Docker 如何构建和存储镜像，以及容器如何使用这些镜像非常重要。您可以利用这些信息针对应用程序的数据持久化方式做出明智的选择，并避免在此过程中出现性能问题。

## 存储驱动程序与 Docker 卷 (Volumes)

Docker 使用存储驱动程序来存储镜像层，以及存储容器可写层中的数据。容器的可写层在容器被删除后不会持久化，但适合存储运行时生成的临时数据。存储驱动程序针对空间效率进行了优化，但 (取决于存储驱动程序) 写入速度低于原生文件系统性能，特别是对于使用写时复制 (copy-on-write) 文件系统的存储驱动程序。写密集型应用程序 (如数据库存储) 会受到性能开销的影响，特别是如果只读层中存在预先存在的数据。

对于写密集型数据、必须持久化到容器寿命之外的数据以及必须在容器之间共享的数据，请使用 Docker 卷。请参阅 [卷 (volumes) 部分](../volumes.md)，了解如何使用卷来持久化数据并提高性能。

## 镜像与层 (Images and layers)

Docker 镜像是从一系列层构建而来的。每一层代表镜像 Dockerfile 中的一条指令。除最后一层外，每一层都是只读的。考虑以下 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
LABEL org.opencontainers.image.authors="org@example.com"
COPY . /app
RUN make /app
RUN rm -r $HOME/.cache
CMD python /app/app.py
```

此 Dockerfile 包含四个命令。修改文件系统的命令会创建一个新层。`FROM` 语句从 `ubuntu:22.04` 镜像开始创建一个层。`LABEL` 命令仅修改镜像的元数据，不产生新层。`COPY` 命令从 Docker 客户端的当前目录添加一些文件。第一个 `RUN` 命令使用 `make` 命令构建应用程序，并将结果写入一个新层。第二个 `RUN` 命令移除一个缓存目录，并将结果写入一个新层。最后，`CMD` 指令指定容器内要运行的命令，这仅修改镜像的元数据，不产生镜像层。

每一层仅是与前一层相比的差异集合。请注意，*添加* 和 *移除* 文件都会产生一个新层。在上述示例中，虽然 `$HOME/.cache` 目录被移除了，但它在之前的层中仍然可用，并会计入镜像的总大小。请参阅 [编写 Dockerfile 的最佳实践](/manuals/build/building/best-practices.md) 和 [使用多阶段构建](/manuals/build/building/multi-stage.md) 部分，了解如何优化 Dockerfile 以获得高效的镜像。

层是相互堆叠的。当您创建一个新容器时，您在底层之上添加了一个新的可写层。这一层通常被称为“容器层”。对运行中的容器所做的所有更改 (如写入新文件、修改现有文件和删除文件) 都会写入这个薄的可写容器层。下图显示了一个基于 `ubuntu:15.04` 镜像的容器。

![基于 Ubuntu 镜像的容器层](images/container-layers.webp?w=450&h=300)

存储驱动程序处理这些层如何相互作用的细节。提供不同的存储驱动程序，它们在不同的情况下各有优缺点。

## 容器与层 (Container and layers)

容器和镜像之间的主要区别在于最顶部的可写层。所有向容器写入的添加新数据或修改现有数据的操作都存储在这个可写层中。当容器被删除时，可写层也会被删除。底层的镜像保持不变。

由于每个容器都有自己的可写容器层，且所有更改都存储在该层中，因此多个容器可以共享对同一底层镜像的访问，同时拥有自己的数据状态。下图显示了多个容器共享同一个 Ubuntu 15.04 镜像。

![共享同一个镜像的容器](images/sharing-layers.webp?w=600&h=300)

Docker 使用存储驱动程序来管理镜像层和可写容器层的内容。每个存储驱动程序处理实现的方式不同，但所有驱动程序都使用可堆叠的镜像层和写时复制 (CoW) 策略。

> [!NOTE]
> 
> 如果您需要多个容器共享访问完全相同的数据，请使用 Docker 卷。请参阅 [卷 (volumes) 部分](../volumes.md) 了解卷。

## 磁盘上的容器大小

要查看运行中容器的近似大小，可以使用 `docker ps -s` 命令。有两个不同的列与大小相关。

- `size`: 每个容器的可写层所使用的 (磁盘上的) 数据量。
- `virtual size`: 容器所使用的只读镜像数据量加上容器可写层的 `size`。多个容器可能共享部分或全部只读镜像数据。从同一个镜像启动的两个容器共享 100% 的只读数据，而使用具有共同层的不同镜像的两个容器则共享这些共同层。因此，您不能简单地将虚拟大小相加。这会过高估计总磁盘使用量，而且其偏差可能非常显著。

所有运行中的容器在磁盘上使用的总磁盘空间是每个容器的 `size` 和 `virtual size` 值的某种组合。如果多个容器从完全相同的镜像启动，则这些容器在磁盘上的总大小将是 SUM (`size` of containers) 加上一个镜像的大小 (`virtual size` - `size`)。

这还不包括容器占用磁盘空间的以下额外方式：

- [logging-driver](/manuals/engine/logging/_index.md) 存储的日志文件所占用的磁盘空间。如果您的容器生成大量日志数据且未配置日志轮转，这可能会非常显著。
- 容器使用的卷和绑定挂载。
- 容器配置文件所占用的磁盘空间，通常很小。
- 写入磁盘的内存 (如果启用了交换分区)。
- 检查点 (checkpoints)，如果您使用了实验性的检查点/恢复功能。

## 写时复制 (copy-on-write, CoW) 策略

写时复制是一种最大限度提高效率的共享和复制文件的策略。如果一个文件或目录存在于镜像的较低层中，而另一层 (包括可写层) 需要对其进行读取访问，它只需直接使用现有文件。当另一层第一次需要修改该文件时 (在构建镜像或运行容器时)，该文件会被复制到该层并进行修改。这最大限度地减少了 I/O 和每个后续层的大小。下面将更深入地解释这些优势。

### 共享促进更小的镜像

当您使用 `docker pull` 从仓库拉取镜像时，或者当您从本地尚不存在的镜像创建容器时，每一层都会被单独拉取并存储在 Docker 的本地存储区域 (在 Linux 主机上通常是 `/var/lib/docker/`)。您可以在此示例中看到正在拉取的层：

```console
$ docker pull ubuntu:22.04
22.04: Pulling from library/ubuntu
f476d66f5408: Pull complete
8882c27f669e: Pull complete
d9af21273955: Pull complete
f5029279ec12: Pull complete
Digest: sha256:6120be6a2b7ce665d0cbddc3ce6eae60fe94637c6a66985312d1f02f63cc0bcd
Status: Downloaded newer image for ubuntu:22.04
docker.io/library/ubuntu:22.04
```

每一层都存储在 Docker 主机本地存储区域内的独立目录中。要检查文件系统上的层，请列出 `/var/lib/docker/<storage-driver>` 的内容。本示例使用 `overlay2` 存储驱动程序：

```console
$ ls /var/lib/docker/overlay2
16802227a96c24dcbeab5b37821e2b67a9f921749cd9a2e386d5a6d5bc6fc6d3
377d73dbb466e0bc7c9ee23166771b35ebdbe02ef17753d79fd3571d4ce659d7
3f02d96212b03e3383160d31d7c6aeca750d2d8a1879965b89fe8146594c453d
ec1ec45792908e90484f7e629330666e7eee599f08729c93890a7205a6ba35f5
l
```

目录名称不对应层 ID。

现在想象您有两个不同的 Dockerfile。您使用第一个创建一个名为 `acme/my-base-image:1.0` 的镜像。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN apk add --no-cache bash
```

第二个基于 `acme/my-base-image:1.0`，但增加了一些额外的层：

```dockerfile
# syntax=docker/dockerfile:1
FROM acme/my-base-image:1.0
COPY . /app
RUN chmod +x /app/hello.sh
CMD /app/hello.sh
```

第二个镜像包含第一个镜像的所有层，加上由 `COPY` 和 `RUN` 指令创建的新层，以及一个读写容器层。Docker 已经拥有了第一个镜像的所有层，因此不需要再次拉取它们。这两个镜像共享它们共同拥有的任何层。

如果您从这两个 Dockerfile 构建镜像，可以使用 `docker image ls` 和 `docker image history` 命令来验证共享层的加密 ID 是否相同。

1. 创建一个新目录 `cow-test/` 并进入其中。

2. 在 `cow-test/` 中，创建一个名为 `hello.sh` 的新文件，内容如下：

   ```bash
   #!/usr/bin/env bash
   echo "Hello world"
   ```

3. 将上面第一个 Dockerfile 的内容复制到一个名为 `Dockerfile.base` 的新文件中。

4. 将上面第二个 Dockerfile 的内容复制到一个名为 `Dockerfile` 的新文件中。

5. 在 `cow-test/` 目录内，构建第一个镜像。不要忘记命令末尾的 `.`。这会设置 `PATH`，告诉 Docker 在哪里寻找需要添加到镜像中的任何文件。

   ```console
   $ docker build -t acme/my-base-image:1.0 -f Dockerfile.base .
   [+] Building 6.0s (11/11) FINISHED
   ... 
   => exporting to image                                                                         0.2s
   => => exporting layers                                                                        0.2s
   => => writing image sha256:da3cf8df55ee9777ddcd5afc40fffc3ead816bda99430bad2257de4459625eaa   0.0s
   => => naming to docker.io/acme/my-base-image:1.0                                              0.0s
   ```

6. 构建第二个镜像。

   ```console
   $ docker build -t acme/my-final-image:1.0 -f Dockerfile .
   ... 
   => exporting to image                                                                          0.1s
   => => exporting layers                                                                         0.1s
   => => writing image sha256:8bd85c42fa7ff6b33902ada7dcefaaae112bf5673873a089d73583b0074313dd    0.0s
   => => naming to docker.io/acme/my-final-image:1.0                                              0.0s
   ```

7. 查看镜像的大小。

   ```console
   $ docker image ls

   REPOSITORY             TAG     IMAGE ID         CREATED               SIZE
   acme/my-final-image    1.0     8bd85c42fa7f     About a minute ago    7.75MB
   acme/my-base-image     1.0     da3cf8df55ee     2 minutes ago         7.75MB
   ```

8. 查看每个镜像的历史记录。

   ```console
   $ docker image history acme/my-base-image:1.0

   IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
   da3cf8df55ee   5 minutes ago   RUN /bin/sh -c apk add --no-cache bash # bui…   2.15MB    buildkit.dockerfile.v0
   <missing>      7 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      7 weeks ago     /bin/sh -c #(nop) ADD file:f278386b0cef68136…   5.6MB
   ```

   有些步骤的大小为 `0B`，这些是仅元数据的更改，不产生镜像层，除了元数据本身外不占用任何空间。上面的输出显示该镜像由 2 个镜像层组成。

   ```console
   $ docker image history  acme/my-final-image:1.0

   IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
   8bd85c42fa7f   3 minutes ago   CMD ["/bin/sh" "-c" "/app/hello.sh"]            0B        buildkit.dockerfile.v0
   <missing>      3 minutes ago   RUN /bin/sh -c chmod +x /app/hello.sh # buil…   39B       buildkit.dockerfile.v0
   <missing>      3 minutes ago   COPY . /app # buildkit                          222B      buildkit.dockerfile.v0
   <missing>      4 minutes ago   RUN /bin/sh -c apk add --no-cache bash # bui…   2.15MB    buildkit.dockerfile.v0
   <missing>      7 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      7 weeks ago     /bin/sh -c #(nop) ADD file:f278386b0cef68136…   5.6MB
   ```

   请注意，第一个镜像的所有步骤也包含在最终镜像中。最终镜像包括来自第一个镜像的两层，以及在第二个镜像中添加的两层。

   `docker history` 输出中的 `<missing>` 行表示这些步骤要么是在另一个系统上构建的，或者是从 Docker Hub 拉取的 `alpine` 镜像的一部分，或者是使用 BuildKit 作为构建器构建的。在 BuildKit 之前，“经典”构建器会为每个步骤生成一个新的“中间”镜像用于缓存，而 `IMAGE` 列会显示该镜像的 ID。 
   
   BuildKit 使用自己的缓存机制，不再需要中间镜像进行缓存。请参阅 [BuildKit](/manuals/build/buildkit/_index.md) 了解更多有关 BuildKit 改进的信息。

9. 查看每个镜像的层

   使用 `docker image inspect` 命令查看每个镜像中层的加密 ID：

   ```console
   $ docker image inspect --format "{{json .RootFS.Layers}}" acme/my-base-image:1.0
   [
     "sha256:72e830a4dff5f0d5225cdc0a320e85ab1ce06ea5673acfe8d83a7645cbd0e9cf",
     "sha256:07b4a9068b6af337e8b8f1f1dae3dd14185b2c0003a9a1f0a6fd2587495b204a"
   ]
   ```
   
   ```console
   $ docker image inspect --format "{{json .RootFS.Layers}}" acme/my-final-image:1.0
   [
     "sha256:72e830a4dff5f0d5225cdc0a320e85ab1ce06ea5673acfe8d83a7645cbd0e9cf",
     "sha256:07b4a9068b6af337e8b8f1f1dae3dd14185b2c0003a9a1f0a6fd2587495b204a",
     "sha256:cc644054967e516db4689b5282ee98e4bc4b11ea2255c9630309f559ab96562e",
     "sha256:e84fb818852626e89a09f5143dbc31fe7f0e0a6a24cd8d2eb68062b904337af4"
   ]
   ```

   注意到两个镜像的前两层是完全相同的。第二个镜像额外添加了两层。共享的镜像层在 `/var/lib/docker/` 中仅存储一次，并且在向镜像注册表推送和拉取镜像时也是共享的。因此，共享镜像层可以减少网络带宽和存储占用。

   > [!TIP]
   > 
   > 使用 `--format` 选项格式化 Docker 命令的输出。
   > 
   > 上述示例使用 `docker image inspect` 命令配合 `--format` 选项来查看层 ID，并格式化为 JSON 数组。Docker 命令中的 `--format` 选项是一个强大的功能，它允许您从输出中提取和格式化特定信息，而不需要 `awk` 或 `sed` 等额外工具。要了解更多有关使用 `--format` 标志格式化输出的信息，请参阅 [格式化命令和日志输出部分](/manuals/engine/cli/formatting.md)。为了可读性，我们还使用了 [`jq` 工具](https://stedolan.github.io/jq/) 对 JSON 输出进行了美化。

### 复制使容器更加高效

当您启动一个容器时，会在其他层之上添加一个薄的可写容器层。容器对文件系统所做的任何更改都存储在这里。容器未更改的任何文件都不会被复制到这个可写层。这意味着可写层尽可能地小。

当修改容器中的现有文件时，存储驱动程序会执行写时复制 (copy-on-write) 操作。涉及的具体步骤取决于具体的存储驱动程序。对于 `overlay2` 驱动程序，写时复制操作遵循以下大致顺序：

*  在镜像层中搜索要更新的文件。该过程从最新的层开始，逐层向下搜索到基础层。找到结果后，将其添加到缓存中以加快未来的操作。
*  对找到的第一个文件副本执行 `copy_up` 操作，将文件复制到容器的可写层。
*  任何修改都针对该文件副本进行，容器无法看到存在于较低层中的只读文件副本。

Btrfs、ZFS 和其他驱动程序处理写时复制的方式不同。您可以在稍后关于这些驱动程序的详细描述中了解更多信息。

写入大量数据的容器比不写入数据的容器消耗更多空间。这是因为大多数写入操作都会在容器顶部的薄可写层中消耗新空间。请注意，更改文件的元数据 (例如更改文件权限或所有权) 也会导致 `copy_up` 操作，从而将文件复制到可写层。

> [!TIP]
> 
> 对于写密集型应用程序，请使用卷。
> 
> 对于写密集型应用程序，不要将数据存储在容器中。众所周知，此类应用程序 (如写密集型数据库) 特别是在只读层中存在预先存在的数据时，会产生问题。
> 
> 相反，应使用 Docker 卷，它独立于运行中的容器，并设计为高效的 I/O。此外，卷可以在容器之间共享，并且不会增加容器可写层的大小。请参阅 [使用卷](../volumes.md) 部分了解卷。

`copy_up` 操作会产生显著的性能开销。这种开销因使用的存储驱动程序而异。大文件、多层和深层目录树可能会使影响更加明显。由于每个 `copy_up` 操作仅在给定文件第一次被修改时发生，因此这缓解了一些影响。

为了验证写时复制的工作方式，以下过程启动了 5 个基于我们之前构建的 `acme/my-final-image:1.0` 镜像的容器，并检查它们占用的空间。

1. 在 Docker 主机的终端中运行以下 `docker run` 命令。末尾的字符串是每个容器的 ID。

   ```console
   $ docker run -dit --name my_container_1 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_2 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_3 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_4 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_5 acme/my-final-image:1.0 bash
   ```

2. 运行带有 `--size` 选项的 `docker ps` 命令，验证 5 个容器正在运行，并查看每个容器的大小。

   ```console
   $ docker ps --size --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Size}}"

   CONTAINER ID   IMAGE                     NAMES            SIZE
   cddae31c314f   acme/my-final-image:1.0   my_container_5   0B (virtual 7.75MB)
   939b3bf9e7ec   acme/my-final-image:1.0   my_container_4   0B (virtual 7.75MB)
   3ed3c1a10430   acme/my-final-image:1.0   my_container_3   0B (virtual 7.75MB)
   a5ff32e2b551   acme/my-final-image:1.0   my_container_2   0B (virtual 7.75MB)
   40ebdd763416   acme/my-final-image:1.0   my_container_1   0B (virtual 7.75MB)
   ```
   
   上面的输出显示所有容器共享镜像的只读层 (7.75MB)，但没有数据写入容器的文件系统，因此容器没有使用额外的存储空间。

   {{< accordion title="高级：用于容器的元数据和日志存储" >}}
   
   > [!NOTE]
   > 
   > 此步骤需要 Linux 机器，在 Docker Desktop 上不起作用，因为它需要访问 Docker 守护进程的文件存储。
   
   虽然 `docker ps` 的输出为您提供了容器可写层消耗磁盘空间的信息，但它不包括为每个容器存储的元数据和日志文件的信息。
   
   通过探索 Docker 守护进程的存储位置 (默认为 `/var/lib/docker`) 可以获得更多细节。
   
   ```console
   $ sudo du -sh /var/lib/docker/containers/*
   
   36K  /var/lib/docker/containers/3ed3c1a10430e09f253704116965b01ca920202d52f3bf381fbb833b8ae356bc
   ...
   ```
   
   每个容器在文件系统上仅占用 36k 的空间。

   {{< /accordion >}}

3. 每个容器的存储

   为了演示这一点，运行以下命令，在容器 `my_container_1`、`my_container_2` 和 `my_container_3` 的可写层中将单词 'hello' 写入一个文件：

   ```console
   $ for i in {1..3}; do docker exec my_container_$i sh -c 'printf hello > /out.txt'; done
   ```
   
   随后再次运行 `docker ps` 命令，显示这些容器现在各消耗 5 字节。此数据对每个容器是唯一的，且不共享。容器的只读层不受影响，且仍然由所有容器共享。

   ```console
   $ docker ps --size --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Size}}"

   CONTAINER ID   IMAGE                     NAMES            SIZE
   cddae31c314f   acme/my-final-image:1.0   my_container_5   0B (virtual 7.75MB)
   939b3bf9e7ec   acme/my-final-image:1.0   my_container_4   0B (virtual 7.75MB)
   3ed3c1a10430   acme/my-final-image:1.0   my_container_3   5B (virtual 7.75MB)
   a5ff32e2b551   acme/my-final-image:1.0   my_container_2   5B (virtual 7.75MB)
   40ebdd763416   acme/my-final-image:1.0   my_container_1   5B (virtual 7.75MB)
   ```

前面的示例说明了写时复制文件系统如何帮助使容器更加高效。写时复制不仅节省了空间，还减少了容器的启动时间。当您创建一个容器 (或从同一个镜像创建多个容器) 时，Docker 只需要创建薄薄的可写容器层。

如果 Docker 每次创建新容器时都必须对底层镜像栈进行完整复制，那么容器创建时间和使用的磁盘空间将会显著增加。这类似于虚拟机的工作方式，每个虚拟机有一个或多个虚拟磁盘。[`vfs` 存储](vfs-driver.md) 不提供 CoW 文件系统或其他优化。使用此存储驱动程序时，会为每个容器创建镜像数据的完整副本。

## 相关信息

* [卷 (Volumes)](../volumes.md)
* [选择存储驱动程序](select-storage-driver.md)
