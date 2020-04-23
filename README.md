# PyToolkit
My personal Python programming toolkit

----------------

在新项目中使用本项目，参考[Git - 子模块](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)

1. 在新项目X中添加本项目为子项目：
```shell script
git submodule add https://github.com/LiangsLi/PyToolkit
```
2. 将本项目拉取到新项目X中(同时也会拉取其他的子项目)：
```shell script
git submodule init
git submodule update
```
3. 在新项目中使用

若要更新子项目，执行：
```shell script
git submodule update --remote
```