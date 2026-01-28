---
title: 在 Docker 中使用 CA 证书
linkTitle: CA 证书
description: 学习如何在 Docker 主机和 Linux 容器中安装和使用 CA 证书
keywords: docker, networking, ca, certs, host, container, proxy
---

> [!CAUTION]
> 在生产容器中使用中间人（MITM）CA 证书时应遵循最佳实践。
> 如果被入侵，攻击者可能会
> 拦截敏感数据、伪造可信服务或执行
> 中间人攻击。在继续之前请咨询你的安全团队。

如果你的公司使用检查 HTTPS 流量的代理，你可能需要将
所需的根证书添加到你的主机机器和 Docker 容器
或镜像中。这是因为 Docker 及其容器在拉取镜像或
进行网络请求时，需要信任代理的证书。

在主机上，添加根证书可以确保任何 Docker 命令（如
`docker pull`）都能正常工作。对于容器，你需要在构建过程中或
运行时将根证书添加到容器的信任存储中。这确保容器内运行的应用程序可以
通过代理通信而不会遇到安全警告或
连接失败。

## 将 CA 证书添加到主机

以下部分描述如何在 macOS 或
Windows 主机上安装 CA 证书。对于 Linux，请参阅你的发行版的文档。

### macOS

1. 下载你的 MITM 代理软件的 CA 证书。
2. 打开**钥匙串访问**应用程序。
3. 在钥匙串访问中，选择**系统**，然后切换到**证书**标签。
4. 将下载的证书拖放到证书列表中。如果提示，请输入密码。
5. 找到新添加的证书，双击它，然后展开**信任**部分。
6. 为该证书设置**始终信任**。如果提示，请输入密码。
7. 启动 Docker Desktop 并验证 `docker pull` 是否正常工作，假设 Docker Desktop 已配置为使用 MITM 代理。

### Windows

选择是否要使用 Microsoft
管理控制台（MMC）或你的网络浏览器安装证书。

{{< tabs >}}
{{< tab name="MMC" >}}

1. 下载 MITM 代理软件的 CA 证书。
2. 打开 Microsoft 管理控制台（`mmc.exe`）。
3. 在 MMC 中添加**证书管理单元**。
   1. 选择**文件** → **添加/删除管理单元**，然后选择**证书** → **添加 >**。
   2. 选择**计算机帐户**，然后点击**下一步**。
   3. 选择**本地计算机**，然后选择**完成**。
4. 导入 CA 证书：
   1. 从 MMC 中，展开**证书（本地计算机）**。
   2. 展开**受信任的根证书颁发机构**部分。
   3. 右键单击**证书**，选择**所有任务**和**导入…**。
   4. 按照提示导入你的 CA 证书。
5. 选择**完成**，然后选择**关闭**。
6. 启动 Docker Desktop 并验证 `docker pull` 是否成功（假设 Docker Desktop 已配置为使用 MITM 代理服务器）。

> [!NOTE]
> 根据使用的 SDK 和/或运行时/框架，除了将 CA 证书添加到操作系统的信任
> 存储之外，可能还需要进一步的步骤。

{{< /tab >}}
{{< tab name="Web browser" >}}

1. 下载你的 MITM 代理软件的 CA 证书。
2. 打开你的网络浏览器，进入**设置**并打开**管理证书**
3. 选择**受信任的根证书颁发机构**标签。
4. 选择**导入**，然后浏览下载的 CA 证书。
5. 选择**打开**，然后选择**将所有证书放入以下存储**。
6. 确保选中**受信任的根证书颁发机构**，然后选择**下一步**。
7. 选择**完成**，然后选择**关闭**。
8. 启动 Docker Desktop 并验证 `docker pull` 是否成功（假设 Docker Desktop 已配置为使用 MITM 代理服务器）。

{{< /tab >}}
{{< /tabs >}}

## 将 CA 证书添加到 Linux 镜像和容器

如果你需要运行依赖于内部或自定义
证书的容器化工作负载，例如在具有企业代理或安全
服务的环境中，你必须确保容器信任这些证书。如果不
添加必要的 CA 证书，容器内的应用程序在尝试连接到
HTTPS 端点时可能会遇到请求失败或安全警告。

通过在构建时[将 CA 证书添加到镜像](#将证书添加到镜像)，
你可以确保从该镜像启动的任何容器都会信任
指定的证书。这对于需要无缝访问内部 API、数据库或其他生产服务的应用程序特别重要。

在无法重建镜像的情况下，你可以直接[将
证书添加到容器](#将证书添加到容器)。但是，
在运行时添加的证书在容器被销毁或
重新创建时不会保留，因此这种方法通常用于临时修复或测试
场景。

## 将证书添加到镜像

> [!NOTE]
> 以下命令适用于 Ubuntu 基础镜像。如果你的构建使用
> 不同的 Linux 发行版，请使用相应的包管理命令
>（`apt-get`、`update-ca-certificates` 等）。

要在构建容器镜像时向其添加 CA 证书，请将
以下指令添加到你的 Dockerfile。

```dockerfile
# Install the ca-certificate package
RUN apt-get update && apt-get install -y ca-certificates
# Copy the CA certificate from the context to the build container
COPY your_certificate.crt /usr/local/share/ca-certificates/
# Update the CA certificates in the container
RUN update-ca-certificates
```

### 将证书添加到容器

> [!NOTE]
> 以下命令适用于基于 Ubuntu 的容器。如果你的容器
> 使用不同的 Linux 发行版，请使用相应的包管理命令
>（`apt-get`、`update-ca-certificates` 等）。

要将 CA 证书添加到正在运行的 Linux 容器：

1. 下载你的 MITM 代理软件的 CA 证书。
2. 如果证书不是 `.crt` 格式，将其转换为 `.crt` 格式：

   ```console {title="Example command"}
   $ openssl x509 -in cacert.der -inform DER -out myca.crt
   ```

3. 将证书复制到正在运行的容器中：

    ```console
    $ docker cp myca.crt <containerid>:/tmp
    ```

4. 附加到容器：

    ```console
    $ docker exec -it <containerid> sh
    ```

5. 确保已安装 `ca-certificates` 包（更新证书所需）：

    ```console
    # apt-get update && apt-get install -y ca-certificates
    ```

6. 将证书复制到 CA 证书的正确位置：

    ```console
    # cp /tmp/myca.crt /usr/local/share/ca-certificates/root_cert.crt
    ```

7. 更新 CA 证书：

    ```console
    # update-ca-certificates
    ```

    ```plaintext {title="Example output"}
    Updating certificates in /etc/ssl/certs...
    rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
    1 added, 0 removed; done.
    ```

8. 验证容器可以通过 MITM 代理通信：

    ```console
    # curl https://example.com
    ```

    ```plaintext {title="Example output"}
    <!doctype html>
    <html>
    <head>
        <title>Example Domain</title>
    ...
    ```
