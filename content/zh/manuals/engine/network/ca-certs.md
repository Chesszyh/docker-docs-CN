---
title: 在 Docker 中使用 CA 证书
linkTitle: CA 证书
description: 了解如何在 Docker 主机和 Linux 容器中安装和使用 CA 证书
keywords: docker, networking, ca, certs, host, container, proxy, 网络, 证书, 主机, 容器, 代理
---

> [!CAUTION]
> 在生产容器中使用中间人 (Man-in-the-Middle, MITM) CA 证书时，应遵循最佳实践。如果证书泄露，攻击者可能会拦截敏感数据、伪造受信服务或执行中间人攻击。在继续操作之前，请咨询您的安全团队。

如果您的公司使用检查 HTTPS 流量的代理，您可能需要将所需的根证书添加到主机以及 Docker 容器或镜像中。这是因为 Docker 及其容器在拉取镜像或发出网络请求时，需要信任代理的证书。

在主机上添加根证书可确保任何 Docker 命令 (如 `docker pull`) 都能正常运行。对于容器，您需要在构建过程中或运行时将根证书添加到容器的信任库中。这可确保容器内运行的应用程序可以通过代理进行通信，而不会遇到安全警告或连接失败。

## 将 CA 证书添加到主机

以下部分介绍了如何在 macOS 或 Windows 主机上安装 CA 证书。对于 Linux，请参阅您的发行版文档。

### macOS

1. 下载您的 MITM 代理软件的 CA 证书。
2. 打开 **Keychain Access** (钥匙串访问) 应用程序。
3. 在 Keychain Access 中，选择 **System** (系统)，然后切换到 **Certificates** (证书) 选项卡。
4. 将下载的证书拖放到证书列表中。如果提示，请输入您的密码。
5. 找到新添加的证书，双击它，然后展开 **Trust** (信任) 部分。
6. 将证书设置为 **Always Trust** (始终信任)。如果提示，请输入您的密码。
7. 启动 Docker Desktop 并验证 `docker pull` 是否正常工作 (假设 Docker Desktop 已配置为使用 MITM 代理)。

### Windows

选择您想要使用 Microsoft 管理控制台 (MMC) 还是 Web 浏览器安装证书。

{{< tabs >}}
{{< tab name="MMC" >}}

1. 下载 MITM 代理软件的 CA 证书。
2. 打开 Microsoft 管理控制台 (`mmc.exe`)。
3. 在 MMC 中添加 **Certificates Snap-In** (证书管理单元)。
   1. 选择 **File** (文件) → **Add/Remove Snap-in** (添加/删除管理单元)，然后选择 **Certificates** (证书) → **Add >** (添加)。
   2. 选择 **Computer Account** (计算机帐户)，然后选择 **Next** (下一步)。
   3. 选择 **Local computer** (本地计算机)，然后选择 **Finish** (完成)。
4. 导入 CA 证书：
   1. 在 MMC 中，展开 **Certificates (Local Computer)** (证书 (本地计算机))。
   2. 展开 **Trusted Root Certification Authorities** (受信任的根证书颁发机构) 部分。
   3. 右键单击 **Certificates** (证书)，选择 **All Tasks** (所有任务) 和 **Import…** (导入…)。
   4. 按照提示导入您的 CA 证书。
5. 选择 **Finish** (完成) 然后选择 **Close** (关闭)。
6. 启动 Docker Desktop 并验证 `docker pull` 是否成功 (假设 Docker Desktop 已配置为使用 MITM 代理服务器)。

> [!NOTE]
> 根据所使用的 SDK 和/或运行时/框架，除了将 CA 证书添加到操作系统的信任库之外，可能还需要进一步的步骤。

{{< /tab >}}
{{< tab name="Web 浏览器" >}}

1. 下载您的 MITM 代理软件的 CA 证书。
2. 打开 Web 浏览器，进入 **Settings** (设置) 并打开 **Manage certificates** (管理证书)。
3. 选择 **Trusted Root Certification Authorities** (受信任的根证书颁发机构) 选项卡。
4. 选择 **Import** (导入)，然后浏览并选择下载的 CA 证书。
5. 选择 **Open** (打开)，然后选择 **Place all certificates in the following store** (将所有证书放入以下存储)。
6. 确保已选择 **Trusted Root Certification Authorities** 并选择 **Next** (下一步)。
7. 选择 **Finish** (完成) 然后选择 **Close** (关闭)。
8. 启动 Docker Desktop 并验证 `docker pull` 是否成功 (假设 Docker Desktop 已配置为使用 MITM 代理服务器)。

{{< /tab >}}
{{< /tabs >}}

## 将 CA 证书添加到 Linux 镜像和容器

如果您需要运行依赖内部或自定义证书的容器化工作负载 (例如在具有企业代理或安全服务的环境中)，必须确保容器信任这些证书。如果不添加必要的 CA 证书，容器内的应用程序在尝试连接到 HTTPS 端点时可能会遇到请求失败或安全警告。

通过在构建时 [将 CA 证书添加到镜像](#add-certificates-to-images)，您可以确保从该镜像启动的任何容器都将信任指定的证书。这对于在生产环境中需要无缝访问内部 API、数据库或其他服务的应用程序尤为重要。

在无法重新构建镜像的情况下，您可以改为直接 [将证书添加到容器](#add-certificates-to-containers)。但是，如果容器被销毁或重新创建，在运行时添加的证书将不会保留，因此此方法通常用于临时修复或测试场景。

## 将证书添加到镜像

> [!NOTE]
> 以下命令适用于基于 Ubuntu 的镜像。如果您的构建使用不同的 Linux 发行版，请使用等效的软件包管理命令 (`apt-get`、`update-ca-certificates` 等)。

要在构建容器镜像时向其添加 CA 证书，请在 Dockerfile 中添加以下指令。

```dockerfile
# 安装 ca-certificate 软件包
RUN apt-get update && apt-get install -y ca-certificates
# 将 CA 证书从上下文复制到构建容器中
COPY your_certificate.crt /usr/local/share/ca-certificates/
# 更新容器中的 CA 证书
RUN update-ca-certificates
```

### 将证书添加到容器

> [!NOTE]
> 以下命令适用于基于 Ubuntu 的容器。如果您的容器使用不同的 Linux 发行版，请使用等效的软件包管理命令 (`apt-get`、`update-ca-certificates` 等)。

要向正在运行的 Linux 容器添加 CA 证书：

1. 下载您的 MITM 代理软件的 CA 证书。
2. 如果证书格式不是 `.crt`，请将其转换为 `.crt` 格式：

   ```console {title="示例命令"}
   $ openssl x509 -in cacert.der -inform DER -out myca.crt
   ```

3. 将证书复制到正在运行的容器中：

    ```console
    $ docker cp myca.crt <containerid>:/tmp
    ```

4. 进入容器：

    ```console
    $ docker exec -it <containerid> sh
    ```

5. 确保已安装 `ca-certificates` 软件包 (更新证书所需)：

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

    ```plaintext {title="示例输出"}
    Updating certificates in /etc/ssl/certs...
    rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
    1 added, 0 removed; done.
    ```

8. 验证容器是否可以通过 MITM 代理通信：

    ```console
    # curl https://example.com
    ```

    ```plaintext {title="示例输出"}
    <!doctype html>
    <html>
    <head>
        <title>Example Domain</title>
    ...
    ```
