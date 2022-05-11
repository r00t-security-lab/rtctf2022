## Too Much Chaos

*Reverse 1*, by xyy & EZForever

### 题目描述

所谓逆向工程，就是要去看懂别人写的程序。

某位黑心出题人把这道题的flag写成程序扔了出来，但是没有人能把他的程序运行起来……

**注：** 使用Visual Studio的同学可能需要删除代码中的两行中文注释才能正常解题。

**本题flag格式：`r00t{%s}`**

*附件：`getflag.cpp`*

### 解析

flag: `r00t{w0W_y0u_kN0w_c_p1us_plUs_rEa11y_weLl}`

包含若干语法错误和逻辑错误的C++源码，需要逐步修正错误。

把代码拿去编译一次就能找出所有语法错误，修好之后能得到第一句提示。根据提示一步一步解决`reverse`和`calculate`两个函数中的逻辑错误，即可得到flag。

或者，仔细读一下代码也能直接读出程序的工作原理：字符串逆序后逐字节+3，自己重新写程序解密flag也是预期解。

刻意埋进代码里的所有错误如下，按函数和发现难易程度排序：
- 第47行：经典`int mian`
- 第54行：中文括号和分号
- 第57行：返回值引用了不存在的标识符
- 第28、31、35行：`calculate`函数调用`str.length`的地方全都写成了`str.len`
- 第44行：`my_char`写成了`my-char`
- 第23行：缺少分号
- 第19行：循环边界值有误导致交换操作执行了两次
- 第40行：指针变量自增有误导致死循环

`getflag.clean.cpp`是没引入任何错误的源代码。

### 花絮

至于后来加上的关于Visual Studio的备注……

这份源代码文件是UTF-8编码，但MSVC非常固执地使用BOM判断文件编码，没有BOM就是ANSI：

> By default, Visual Studio detects a byte-order mark to determine if the source file is in an encoded Unicode format, for example, UTF-16 or UTF-8. If no byte-order mark is found, it assumes that the source file is encoded in the current user code page, unless you use the `/source-charset` or `/utf-8` option to specify a character set name or code page.
> 
> —— [`/source-charset` (Set source character set) | Microsoft Docs](https://docs.microsoft.com/en-us/cpp/build/reference/source-charset-set-source-character-set)

这会导致在MSVC看来那两行中文注释是些奇怪的字符……巧合的是，最后一行注释的最后几个字节无法构成完整字符。为了完成编码，这一行最后的换行符`0x0a`被奇怪字符吃掉了。这就是编译器报错“`#else` 找不到 `#if`”的原因——`#if`被合并到了上一行注释里。

真正让人头大的是，Visual Studio的编辑器和IntelliSense是都认识UTF-8的，只有编译器不认识。今日份兼容小技巧+1。

