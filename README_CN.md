# Docker中文文档

## Building locally

```shell
docker compose watch
```

`README.md`没说怎么构建静态网站，而是在`CONTRIBUTING.md`里提到的。执行以上命令后，访问`http://localhost:1313/`即可查看效果。

容器一旦构建后，如果不终止`watch`(实时监控修改)，则会一直运行。可以通过`docker compose down`来停止容器。