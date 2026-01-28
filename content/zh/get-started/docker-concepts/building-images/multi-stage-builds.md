---
title: 多阶段构建
keywords: concepts, build, images, container, docker desktop, 概念, 构建, 镜像, 容器
description: 此概念页面将向您介绍多阶段构建的目的及其好处
summary: |
  通过将构建环境与最终运行环境分离，您可以显著减小镜像大小和攻击面。在本指南中，您将开启多阶段构建的力量，以创建精简且高效的 Docker 镜像，这对于最小化开销和增强生产环境中的部署至关重要。
weight: 5
alias: 
 - /guides/docker-concepts/building-images/multi-stage-builds/
---

{{< youtube-embed vR185cjwxZ8 >}}

## 解释

在传统构建中，所有构建指令都在单个构建容器中按顺序执行：下载依赖项、编译代码和打包应用程序。所有这些层最终都会进入您的最终镜像。这种方法可行，但它会导致镜像庞大，带有不必要的重量并增加了安全风险。这就是多阶段构建的用武之地。

多阶段构建在您的 Dockerfile 中引入了多个阶段，每个阶段都有特定的目的。可以将其视为在多个不同环境中并发运行构建的不同部分的能力。通过将构建环境与最终运行环境分离，您可以显著减小镜像大小和攻击面。这对于具有大型构建依赖项的应用程序尤其有利。

多阶段构建建议用于所有类型的应用程序。

- 对于解释型语言，如 JavaScript、Ruby 或 Python，您可以在一个阶段中构建并压缩代码，然后将生产就绪的文件复制到较小的运行时镜像中。这优化了您的部署镜像。
- 对于编译型语言，如 C、Go 或 Rust，多阶段构建允许您在一个阶段中进行编译，并将编译后的二进制文件复制到最终的运行时镜像中。无需在最终镜像中捆绑整个编译器。


以下是使用伪代码的简化多阶段构建结构示例。注意有多个 `FROM` 语句和一个新的 `AS <stage-name>`。此外，第二阶段中的 `COPY` 语句是 `--from` 前一个阶段进行复制。


```dockerfile
# 阶段 1：构建环境
FROM builder-image AS build-stage 
# 安装构建工具（例如 Maven, Gradle）
# 复制源代码
# 构建命令（例如 compile, package）

# 阶段 2：运行环境
FROM runtime-image AS final-stage  
# 从构建阶段复制应用程序构件（例如 JAR 文件）
COPY --from=build-stage /path/in/build/stage /path/to/place/in/final/stage
# 定义运行时配置（例如 CMD, ENTRYPOINT） 
```


此 Dockerfile 使用两个阶段：

- 构建阶段使用包含编译应用程序所需的构建工具的基础镜像。它包括安装构建工具、复制源代码和执行构建命令的指令。
- 最终阶段使用适合运行应用程序的较小基础镜像。它从构建阶段复制编译后的构件（例如 JAR 文件）。最后，它定义了用于启动应用程序的运行时配置（使用 `CMD` 或 `ENTRYPOINT`）。


## 试一试

在本实践指南中，您将开启多阶段构建的力量，为示例 Java 应用程序创建精简且高效的 Docker 镜像。您将使用一个基于 Spring Boot 并使用 Maven 构建的简单 “Hello World” 应用程序作为示例。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。


2. 打开此[预初始化项目](https://start.spring.io/#!type=maven-project&language=java&platformVersion=3.4.0-M3&packaging=jar&jvmVersion=21&groupId=com.example&artifactId=spring-boot-docker&name=spring-boot-docker&description=Demo%20project%20for%20Spring%20Boot&packageName=com.example.spring-boot-docker&dependencies=web)以生成 ZIP 文件。如下所示：


    ![Spring Initializr 工具截图，选择了 Java 21, Spring Web 和 Spring Boot 3.4.0](images/multi-stage-builds-spring-initializer.webp?border=true)


    [Spring Initializr](https://start.spring.io/) 是一个用于 Spring 项目的快速启动生成器。它提供了一个可扩展的 API 来生成基于 JVM 的项目，并实现了几个常见的概念——如 Java、Kotlin 和 Groovy 的基本语言生成。

    选择 **Generate**（生成）以创建并下载此项目的 zip 文件。

    在此演示中，您将 Maven 构建自动化与 Java、Spring Web 依赖项以及用于元数据的 Java 21 配对。


3. 导航到项目目录。解压文件后，您将看到以下项目目录结构：


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

   `src/main/java` 目录包含项目的源代码，`src/test/java` 目录包含测试源代码，`pom.xml` 文件是项目的项目对象模型 (POM)。

   `pom.xml` 文件是 Maven 项目配置的核心。它是一个单一的配置文件，包含了构建定制项目所需的大部分信息。POM 非常庞大，看起来可能令人畏惧。值得庆幸的是，您还不需要理解每一个细节就能有效地使用它。

4. 创建一个显示 "Hello World!" 的 RESTful Web 服务。

    
    在 `src/main/java/com/example/spring_boot_docker/` 目录下，您可以修改 `SpringBootDockerApplication.java` 文件，内容如下：


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

    `SpringbootDockerApplication.java` 文件首先声明了您的 `com.example.spring_boot_docker` 包并导入了必要的 Spring 框架。此 Java 文件创建了一个简单的 Spring Boot Web 应用程序，当用户访问其主页时会响应 "Hello World"。


### 创建 Dockerfile

现在您有了项目，可以准备创建 `Dockerfile` 了。

 1. 在包含所有其他文件夹和文件（如 src, pom.xml 等）的同一文件夹中创建一个名为 `Dockerfile` 的文件。

 2. 在 `Dockerfile` 中，通过添加以下行来定义您的基础镜像：

     ```dockerfile
     FROM eclipse-temurin:21.0.2_13-jdk-jammy
     ```

 3. 现在，使用 `WORKDIR` 指令定义工作目录。这将指定后续命令运行的位置以及文件将复制到容器镜像内部的目录。

     ```dockerfile
     WORKDIR /app
     ```

 4. 将 Maven 包装器脚本和项目的 `pom.xml` 文件复制到 Docker 容器内的当前工作目录 `/app` 中。

     ```dockerfile
     COPY .mvn/ .mvn
     COPY mvnw pom.xml ./
     ```

 5. 在容器内执行一条命令。它运行 `./mvnw dependency:go-offline` 命令，该命令使用 Maven 包装器 (`./mvnw`) 下载项目的所有依赖项，而无需构建最终的 JAR 文件（有助于加快构建速度）。

     ```dockerfile
     RUN ./mvnw dependency:go-offline
     ```

 6. 将项目中的 `src` 目录从主机机器复制到容器内的 `/app` 目录。

     ```dockerfile
     COPY src ./src
     ```


 7. 设置容器启动时要执行的默认命令。此命令指示容器运行带有 `spring-boot:run` 目标的 Maven 包装器 (`./mvnw`)，这将构建并执行您的 Spring Boot 应用程序。

     ```dockerfile
     CMD ["./mvnw", "spring-boot:run"]
     ```

    完成后，您应该拥有以下 Dockerfile：

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


 1. 执行以下命令来构建 Docker 镜像：


    ```console
    $ docker build -t spring-helloworld .
    ```

 2. 使用 `docker images` 命令检查 Docker 镜像的大小：

    ```console
    $ docker images
    ```

    这样做会产生类似以下的输出：

    ```console
    REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
    spring-helloworld   latest    ff708d5ee194   3 minutes ago    880MB
    ```


    此输出显示您的镜像大小为 880MB。它包含完整的 JDK、Maven 工具链等。在生产环境中，您的最终镜像不需要这些。


### 运行 Spring Boot 应用程序

1. 构建好镜像后，是时候运行容器了。

    ```console
    $ docker run -p 8080:8080 spring-helloworld
    ```

    然后您将在容器日志中看到类似以下的输出：

    ```plaintext
    [INFO] --- spring-boot:3.3.4:run (default-cli) @ spring-boot-docker ---
    [INFO] Attaching agents: []
    
         .   ____          _            __ _ _
        /\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
       ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
        \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
         '  |____| .__|_| |_|_| |_\[\__, | / / / /
        =========|_|==============|___/=/_/_/_/
    
        :: Spring Boot ::                (v3.3.4)
    
    2024-09-29T23:54:07.157Z  INFO 159 --- [spring-boot-docker] [           main]
    c.e.s.SpringBootDockerApplication        : Starting SpringBootDockerApplication using Java
    21.0.2 with PID 159 (/app/target/classes started by root in /app)
     ….
     ```


2. 通过 Web 浏览器访问 [http://localhost:8080](http://localhost:8080) 或通过此 curl 命令访问您的 “Hello World” 页面：

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

    请注意，此 Dockerfile 已分为两个阶段。

    - 第一阶段与之前的 Dockerfile 相同，提供用于构建应用程序的 Java 开发工具包 (JDK) 环境。此阶段被命名为 `builder`。

    - 第二阶段是名为 `final` 的新阶段。它使用了更精简的 `eclipse-temurin:21.0.2_13-jre-jammy` 镜像，仅包含运行应用程序所需的 Java 运行时环境 (JRE)。此镜像提供的 Java 运行时环境 (JRE) 足以运行编译后的应用程序（JAR 文件）。

    
   > 对于生产环境使用，强烈建议您使用 `jlink` 生成自定义的类似 JRE 的运行时。虽然所有版本的 Eclipse Temurin 都有 JRE 镜像，但 `jlink` 允许您创建一个仅包含应用程序所需 Java 模块的最小运行时。这可以显著减小最终镜像的大小并提高安全性。[参考此页面](https://hub.docker.com/_/eclipse-temurin)了解更多信息。

   使用多阶段构建，Docker 构建使用一个基础镜像进行编译、打包和单元测试，然后使用另一个单独的镜像进行应用程序运行时。因此，最终镜像的大小较小，因为它不包含任何开发或调试工具。通过将构建环境与最终运行环境分离，您可以显著减小镜像大小并提高最终镜像的安全性。


2. 现在，重新构建镜像并运行即用型生产版本。

    ```console
    $ docker build -t spring-helloworld-builder .
    ```

    此命令使用位于当前目录中的 `Dockerfile` 文件中的最终阶段构建名为 `spring-helloworld-builder` 的 Docker 镜像。


     > [!NOTE]
     >
     > 在您的多阶段 Dockerfile 中，最终阶段 (final) 是默认的构建目标。这意味着如果您没有在 `docker build` 命令中显式地使用 `--target` 标志指定目标阶段，Docker 默认会自动构建最后一个阶段。您可以使用 `docker build -t spring-helloworld-builder --target builder .` 仅构建带有 JDK 环境的 builder 阶段。


3. 使用 `docker images` 命令查看镜像大小差异：

    ```console
    $ docker images
    ```

    您将得到类似以下的输出：

    ```console
    spring-helloworld-builder latest    c5c76cb815c0   24 minutes ago      428MB
    spring-helloworld         latest    ff708d5ee194   About an hour ago   880MB
    ```

    您的最终镜像只有 428 MB，而原始构建大小为 880 MB。


    通过优化每个阶段并仅包含必要内容，您能够在保持相同功能的同时显著减小总体镜像大小。这不仅提高了性能，还使您的 Docker 镜像更轻量、更安全且更易于管理。

## 其他资源

* [多阶段构建](/build/building/multi-stage/)
* [Dockerfile 最佳实践](/develop/develop-images/dockerfile_best-practices/)
* [基础镜像](/build/building/base-images/)
* [Spring Boot Docker](https://spring.io/guides/topicals/spring-boot-docker)