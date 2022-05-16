# Flaggybird

---

打游戏到39分，flag是真的白送啊（づ￣3￣）づ╭ flag～

如果键盘按坏了都打不到39，那么可以尝试一下逆向，其实**也**非常简单

提示说从 **pyinstaller** 入手，简单搜索一下就知道这个东西是一个python程序打包工具，搜逆向就能找到工具，如 [python-exe-unpacker](https://github.com/countercept/python-exe-unpacker) 或 [PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor) 等

简单做法是使用工具解压提取之后直接在目标文件夹在二进制文件中搜字符串 **r00t** 就出来了，方法有很多，如：

> `grep -arn r00t` 

或者直接定位到 flyppybird 文件

> `strings flyppybird | grep r00t`

当然 pyc 都提取出来了，是可以逆出游戏源代码的。flyppybird 文件理论上就是源码编译出来的 pyc，然而文件头部缺少了 pyc 的 *magic number*，手动补全改个后缀，随便找个pyc在线反编译网站扔进去，游戏源码就出来了，flag自然也在里面。