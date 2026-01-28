---
title: 多阶段构建
keywords: concepts, build, images, container, docker desktop
description: 本概念页面将教您了解多阶段构建的目的及其优势
summary: |
  通过将构建环境与最终运行时环境分离，您可以显著减小镜像大小和攻击面。在本指南中，您将解锁多阶段构建的强大功能，创建精简高效的 Docker 镜像，这对于最小化开销和增强生产环境中的部署至关重要。
weight: 5
aliases:
 - /guides/docker-concepts/building-images/multi-stage-builds/
---

{{< youtube-embed vR185cjwxZ8 >}}

## 概念解释

在传统构建中，所有构建指令按顺序在单个构建容器中执行：下载依赖项、编译代码和打包应用程序。所有这些层最终都会出现在最终镜像中。这种方法有效，但会导致镜像体积庞大，携带不必要的内容并增加安全风险。这就是多阶段构建的用武之地。

多阶段构建在 Dockerfile 中引入多个阶段，每个阶段都有特定的目的。可以将其视为能够在多个不同环境中并发运行构建的不同部分。通过将构建环境与最终运行时环境分离，您可以显著减小镜像大小和攻击面。这对于具有大型构建依赖项的应用程序特别有益。

多阶段构建推荐用于所有类型的应用程序。

- 对于解释型语言，如 JavaScript、Ruby 或 Python，您可以在一个阶段构建和压缩代码，并将生产就绪的文件复制到更小的运行时镜像中。这可以优化您的镜像以便部署。
- 对于编译型语言，如 C、Go 或 Rust，多阶段构建允许您在一个阶段编译，并将编译后的二进制文件复制到最终运行时镜像中。无需在最终镜像中捆绑整个编译器。


以下是使用伪代码的多阶段构建结构的简化示例。请注意有多个 `FROM` 语句和一个新的 `AS <stage-name>`。此外，第二阶段中的 `COPY` 语句正在 `--from` 前一阶段复制。


```dockerfile
# Stage 1: Build Environment
FROM builder-image AS build-stage
# Install build tools (e.g., Maven, Gradle)
# Copy source code
# Build commands (e.g., compile, package)

# Stage 2: Runtime environment
FROM runtime-image AS final-stage
#  Copy application artifacts from the build stage (e.g., JAR file)
COPY --from=build-stage /path/in/build/stage /path/to/place/in/final/stage
# Define runtime configuration (e.g., CMD, ENTRYPOINT)
```


这个 Dockerfile 使用两个阶段：

- 构建阶段使用包含编译应用程序所需构建工具的基础镜像。它包括安装构建工具、复制源代码和执行构建命令的命令。
- 最终阶段使用适合运行应用程序的更小基础镜像。它从构建阶段复制编译后的工件（例如 JAR 文件）。最后，它定义启动应用程序的运行时配置（使用 `CMD` 或 `ENTRYPOINT`）。


## 动手实践

在本动手指南中，您将解锁多阶段构建的强大功能，为示例 Java 应用程序创建精简高效的 Docker 镜像。您将使用一个基于 Spring Boot 的简单"Hello World"应用程序，使用 Maven 构建作为示例。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。


2. 打开这个[预初始化的项目](https://start.spring.io/#!type=maven-project&language=java&platformVersion=3.4.0-M3&packaging=jar&jvmVersion=21&groupId=com.example&artifactId=spring-boot-docker&name=spring-boot-docker&description=Demo%20project%20for%20Spring%20Boot&packageName=com.example.spring-boot-docker&dependencies=web)以生成 ZIP 文件。以下是它的样子：


    ![Spring Initializr 工具的截图，选择了 Java 21、Spring Web 和 Spring Boot 3.4.0](images/multi-stage-builds-spring-initializer.webp?border=true)


    [Spring Initializr](https://start.spring.io/) 是 Spring 项目的快速入门生成器。它提供可扩展的 API 来生成基于 JVM 的项目，并实现了几个常见概念——如 Java、Kotlin 和 Groovy 的基本语言生成。

    选择 **Generate** 创建并下载此项目的 zip 文件。

    对于此演示，您将 Maven 构建自动化与 Java、Spring Web 依赖项和 Java 21 配对作为元数据。


3. 浏览项目目录。解压文件后，您将看到以下项目目录结构：


    ```plaintext
    spring-boot-docker
    ├── HELP.md
    ├── mvnw
    ├── mvnw.cmd
    ├── pom.xml
    └── src
        ├── main
        │   ├── java
        │   │   └── com
        │   │       └── example
        │   │           └── spring_boot_docker
        │   │               └── SpringBootDockerApplication.java
        │   └── resources
        │       ├── application.properties
        │       ├── static
        │       └── templates
        └── test
            └── java
                └── com
                    └── example
                        └── spring_boot_docker
                            └── SpringBootDockerApplicationTests.java

    15 directories, 7 files
    ```

   `src/main/java` 目录包含项目的源代码，`src/test/java` 目录包含测试源代码，`pom.xml` 文件是项目的项目对象模型（POM）。

   `pom.xml` 文件是 Maven 项目配置的核心。它是一个单一的配置文件，包含构建自定义项目所需的大部分信息。POM 很庞大，看起来可能令人生畏。幸运的是，您现在还不需要了解每个细节就可以有效地使用它。

4. 创建显示"Hello World!"的 RESTful Web 服务。


    在 `src/main/java/com/example/spring_boot_docker/` 目录下，您可以使用以下内容修改 `SpringBootDockerApplication.java` 文件：


    ```java
    package com.example.spring_boot_docker;

    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RestController;


    @RestController
    @SpringBootApplication
    public class SpringBootDockerApplication {

        @RequestMapping("/")
            public String home() {
            return "Hello World";
        }

    	public static void main(String[] args) {
    		SpringApplication.run(SpringBootDockerApplication.class, args);
    	}

    }
    ```

    `SpringbootDockerApplication.java` 文件首先声明 `com.example.spring_boot_docker` 包并导入必要的 Spring 框架。这个 Java 文件创建一个简单的 Spring Boot Web 应用程序，当用户访问其主页时响应"Hello World"。


### 创建 Dockerfile

现在您有了项目，可以准备创建 `Dockerfile` 了。

 1. 在包含所有其他文件夹和文件（如 src、pom.xml 等）的同一文件夹中创建一个名为 `Dockerfile` 的文件。

 2. 在 `Dockerfile` 中，通过添加以下行定义您的基础镜像：

     ```dockerfile
     FROM eclipse-temurin:21.0.2_13-jdk-jammy
     ```

 3. 现在，使用 `WORKDIR` 指令定义工作目录。这将指定未来命令将在哪里运行，以及文件将被复制到容器镜像中的哪个目录。

     ```dockerfile
     WORKDIR /app
     ```

 4. 将 Maven 包装器脚本和项目的 `pom.xml` 文件复制到 Docker 容器内的当前工作目录 `/app` 中。

     ```dockerfile
     COPY .mvn/ .mvn
     COPY mvnw pom.xml ./
     ```

 5. 在容器内执行命令。它运行 `./mvnw dependency:go-offline` 命令，使用 Maven 包装器（`./mvnw`）下载项目的所有依赖项，而不构建最终的 JAR 文件（对于更快的构建很有用）。

     ```dockerfile
     RUN ./mvnw dependency:go-offline
     ```

 6. 将主机上项目的 `src` 目录复制到容器内的 `/app` 目录。

     ```dockerfile
     COPY src ./src
     ```


 7. 设置容器启动时要执行的默认命令。此命令指示容器使用 `spring-boot:run` 目标运行 Maven 包装器（`./mvnw`），这将构建并执行您的 Spring Boot 应用程序。

     ```dockerfile
     CMD ["./mvnw", "spring-boot:run"]
     ```

    这样，您应该得到以下 Dockerfile：

    ```dockerfile
    FROM eclipse-temurin:21.0.2_13-jdk-jammy
    WORKDIR /app
    COPY .mvn/ .mvn
    COPY mvnw pom.xml ./
    RUN ./mvnw dependency:go-offline
    COPY src ./src
    CMD ["./mvnw", "spring-boot:run"]
    ```

### 构建容器镜像


 1. 执行以下命令构建 Docker 镜像：


    ```console
    $ docker build -t spring-helloworld .
    ```

 2. 使用 `docker images` 命令检查 Docker 镜像的大小：

    ```console
    $ docker images
    ```

    这样做将产生类似以下的输出：

    ```console
    REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
    spring-helloworld   latest    ff708d5ee194   3 minutes ago    880MB
    ```


    此输出显示您的镜像大小为 880MB。它包含完整的 JDK、Maven 工具链等。在生产中，您不需要在最终镜像中包含这些。


### 运行 Spring Boot 应用程序

1. 现在您已经构建了镜像，是时候运行容器了。

    ```console
    $ docker run -p 8080:8080 spring-helloworld
    ```

    然后您将在容器日志中看到类似以下的输出：

    ```plaintext
    [INFO] --- spring-boot:3.3.4:run (default-cli) @ spring-boot-docker ---
    [INFO] Attaching agents: []

         .   ____          _            __ _ _
        /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
       ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
        \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
         '  |____| .__|_| |_|_| |_\__, | / / / /
        =========|_|==============|___/=/_/_/_/

        :: Spring Boot ::                (v3.3.4)

    2024-09-29T23:54:07.157Z  INFO 159 --- [spring-boot-docker] [           main]
    c.e.s.SpringBootDockerApplication        : Starting SpringBootDockerApplication using Java
    21.0.2 with PID 159 (/app/target/classes started by root in /app)
     ….
     ```


2. 通过 Web 浏览器访问 [http://localhost:8080](http://localhost:8080) 或通过以下 curl 命令访问您的"Hello World"页面：

    ```console
    $ curl localhost:8080
    Hello World
    ```

### 使用多阶段构建

1. 考虑以下 Dockerfile：

    ```dockerfile
    FROM eclipse-temurin:21.0.2_13-jdk-jammy AS builder
    WORKDIR /opt/app
    COPY .mvn/ .mvn
    COPY mvnw pom.xml ./
    RUN ./mvnw dependency:go-offline
    COPY ./src ./src
    RUN ./mvnw clean install

    FROM eclipse-temurin:21.0.2_13-jre-jammy AS final
    WORKDIR /opt/app
    EXPOSE 8080
    COPY --from=builder /opt/app/target/*.jar /opt/app/*.jar
    ENTRYPOINT ["java", "-jar", "/opt/app/*.jar"]
    ```

    请注意，此 Dockerfile 已分成两个阶段。

    - 第一阶段与之前的 Dockerfile 保持相同，提供用于构建应用程序的 Java 开发工具包（JDK）环境。此阶段的名称为 builder。

    - 第二阶段是名为 `final` 的新阶段。它使用更精简的 `eclipse-temurin:21.0.2_13-jre-jammy` 镜像，仅包含运行应用程序所需的 Java 运行时环境（JRE）。此镜像提供 Java 运行时环境（JRE），足以运行编译后的应用程序（JAR 文件）。


   > 对于生产使用，强烈建议您使用 jlink 生成自定义的类似 JRE 的运行时。Eclipse Temurin 的所有版本都提供 JRE 镜像，但 `jlink` 允许您创建仅包含应用程序所需 Java 模块的最小运行时。这可以显著减小最终镜像的大小并提高安全性。[参考此页面](https://hub.docker.com/_/eclipse-temurin)了解更多信息。

   使用多阶段构建，Docker 构建使用一个基础镜像进行编译、打包和单元测试，然后使用单独的镜像作为应用程序运行时。因此，最终镜像更小，因为它不包含任何开发或调试工具。通过将构建环境与最终运行时环境分离，您可以显著减小镜像大小并提高最终镜像的安全性。


2. 现在，重新构建镜像并运行生产就绪的构建。

    ```console
    $ docker build -t spring-helloworld-builder .
    ```

    此命令使用 Dockerfile 文件中的最终阶段构建名为 `spring-helloworld-builder` 的 Docker 镜像，该文件位于当前目录中。


     > [!NOTE]
     >
     > 在多阶段 Dockerfile 中，最终阶段（final）是构建的默认目标。这意味着如果您没有在 `docker build` 命令中使用 `--target` 标志明确指定目标阶段，Docker 将默认自动构建最后一个阶段。您可以使用 `docker build -t spring-helloworld-builder --target builder .` 仅构建具有 JDK 环境的 builder 阶段。


3. 使用 `docker images` 命令查看镜像大小差异：

    ```console
    $ docker images
    ```

    您将得到类似以下的输出：

    ```console
    spring-helloworld-builder latest    c5c76cb815c0   24 minutes ago      428MB
    spring-helloworld         latest    ff708d5ee194   About an hour ago   880MB
    ```

    您的最终镜像仅为 428 MB，而原始构建大小为 880 MB。


    通过优化每个阶段并仅包含必要的内容，您能够在保持相同功能的同时显著减小整体镜像大小。这不仅提高了性能，还使您的 Docker 镜像更轻量、更安全、更易于管理。

## 其他资源

* [多阶段构建](/build/building/multi-stage/)
* [Dockerfile 最佳实践](/develop/develop-images/dockerfile_best-practices/)
* [基础镜像](/build/building/base-images/)
* [Spring Boot Docker](https://spring.io/guides/topicals/spring-boot-docker)
