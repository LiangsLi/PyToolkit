# PyToolkit
My personal Python programming toolkit

------------------------------------------

在新项目中使用本项目，参考:
+ [Git - 子模块](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)
+ [Git submodule 子模块的管理和使用 - 简书](https://www.jianshu.com/p/9000cd49822c)
-----------------------------------------

## 1、在新项目中使用本项目作为子项目：
```shell script
git submodule add https://github.com/LiangsLi/PyToolkit
```
## 2、更新本地的子项目：
```shell script
git submodule update --remote
```
## 3、克隆包含子项目的项目：
```shell script
git clone <项目地址>
git submodule init
git submodule update --remote
```
或者
```shell script
git clone <项目地址> assets --recursive
```
-------------------------------

