## 骗！偷袭！绑架勒索！【任务A：数据恢复】

*Reverse 2/3*, by EZForever

### 题目描述

今年的四月一号愚人节，本来应该是个欢乐的日子，r00t战队的同学们却高兴不起来。

这天中午，一大半同学们的电脑上都出现了个奇怪的程序。没人知道这程序是怎么来的，它显示了个黑框框，运行了几秒钟，就消失了。

“应该没什么大事吧。”同学们想着。

直到他们打开了自己还没交的作业。

救救孩子吧，至少把这篇英语大作业恢复出来，下周就要交了。

**flag格式：r00t{%s}**

*附件：`required_essay.txt.WannaEscape` `WannaEscape.exe`*

---

那个“勒索病毒”会破坏题给文件并删除自身（或者不会？），除此之外什么都不会做。尽管如此，运行的时候务必小心。

不知道拿着这个“勒索病毒”该干什么？[去找位小姐姐帮你把它拆了吧~](https://www.zhihu.com/question/41774725/answer/92379575)

### 解析

flag: `r00t{50-l0n6-4nd-7h4nk5-f0r-4ll-7h3-f15h}`

一道还算简单的（？）基本（？）逆向，为了维持低难度，给的二进制带了调试符号，F5出来的代码和源代码已经基本一致了。容易让新同学看不懂的地方大概在C语言二进制文件操作（直接学C++了应该是讲不到这些函数的）。

核心算法是每字节加一个滚动的常量，复制份算法把加号改成减号就能完成解密，参见`exp.c`。flag在解密得到的论文内容中：

> ... Finally, once the most efficient and versatile algorithms are identified during the trial process, the final architecture of the rendering system will be redesigned, with the design decisions made to best fit the need of algorithms, \*and to incorporate a flag with value `r00t{50-l0n6-4nd-7h4nk5-f0r-4ll-7h3-f15h}`\*. ...

注意运行题给程序会破坏加密后的文件。

### 花絮

1. 其实这道题是为了把任务B的剧情圆上而出的，一开始设计为Rev3，但发现没人出Rev2，就降低难度当成Rev2放出来了……
2. 解密出来的论文其实是真的英语大作业——是鄙人的专业英语写作结课作业。写得太菜辣眼睛还请多多包涵。
3. 本题flag的梗来自[《银河系漫游指南》](https://hitchhikers.fandom.com/wiki/So_Long,_and_Thanks_for_All_the_Fish)。为什么这个梗和题目没关系呢？因为题目最初的设计是用这本书的文本的，但是pdf和epub都不方便提取文字，只好作罢。~~我太菜了对不起求放过~~
4. ~~joke's on you，[无符号整数运算是模2^n的](https://en.cppreference.com/w/cpp/language/operator_arithmetic#Overflows)，不叫溢出也不是UB。~~

