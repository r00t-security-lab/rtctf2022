## 骗！偷袭！绑架勒索！【任务B：情报收集】

*Misc ?*, by EZForever

### 题目描述

**本题的剧情接续【任务A】，但是不需要解出那道题。**

作业保住了的同学们松了一口气。不过，延续社团传统，一个活生生的勒索病毒摆在眼前，不好好分析一番是不可能放过它的，如果可能的话溯源看看是谁这么黑心。

出人意料的是，勒索病毒本身似乎是被处理过，什么来源信息都找不到。摆在同学们眼前的唯一线索，就是这封发到邮箱里的勒索信了。

“作者肯定会把自己的名字写在哪里吧……”同学们想着。

**本题答案为人名（由英文字母构成，无空格等特殊符号），不遵守flag格式。**

*附件：~~`email.mht`~~ `email.public.mht`*

*提示：*
> 这封勒索信是`EZForever`收到的，他是勒索病毒的受害者，不是作者（不是这道题的答案）。
> 
> `ezforever@example.com`是他的邮箱，和这道题无关。

### 解析

答案： `ZHANGSAN`

张三的奇妙冒险又开始了……虽然要到解出题来才会发现是他。

本题“考点”在题给文件的文件格式MHTML。简单来讲，MHTML可以把HTML网页和网页用到的各种资源“打包”成一整个文件，方便传输和储存。MHTML文件头还可以包含电子邮件的若干字段。因为这些特性，MHTML是多媒体电子邮件格式的事实标准。

MHTML文件一般使用MHT或EML扩展名——前者代表打包的网页，后者代表电子邮件。为什么同样的格式要分两种扩展呢？因为网页和电子邮件使用打包内容的方式不一样。

对于打包的网页，MHTML文件中的所有内容共同构成同一个网页。例如说，对于一个网页index.html以及引用的两张图片a.jpg与b.jpg，打包成MHT画成图大概是这样：

| 文件名 | Content-Type |
| - | - |
| index.html | `text/html` |
| a.jpg | `image/jpeg` |
| b.jpg | `image/jpeg` |

MHTML中的M代表MIME，那个出现在Content-Type字段里的东西。对于像上图一样打包的网页，MHTML文件头里的Content-Type字段为`multipart/related`。

而对于电子邮件，因为要照顾不支持HTML的邮件客户端，一般一封邮件中会带有同样内容的两种版本：HTML原版，以及用于兼容的纯文本版本。EML画成图长这样：

| 内容 | Content-Type |
| - | - |
| 纯文本邮件 | `text/plain` |
| HTML邮件 | `text/html` |

邮件客户端会从后往前查找第一个支持的格式并显示。此时MHTML文件头里的Content-Type字段为`multipart/alternative`。

这道题有趣的地方就在这了。题给文件是一封电子邮件，但扩展名是MHT。因为扩展名决定文件关联（至少在Windows上），这封邮件会被交给浏览器打开。测试表明现代版本的Chromium浏览器会忽略`multipart/alternative`，强行只显示MHTML文件的第一部分，但IE和其他电子邮件客户端是正确地从后往前查找支持格式的。题给文件画成图是这样：

| 内容 | Content-Type | |
| - | - | - |
| “浏览器不支持”报错信息 | `text/plain` | <- Chromium显示这个 |
| 隐藏信息 | `application/xml+WannaEscape` | |
| 勒索信本体 | `text/html` | <- IE显示这个 |

隐藏信息的Content-Type是瞎写的，没有浏览器支持就不会显示。在这里按MHTML格式要求加一层base64，就可以在邮件中夹带任意数据了。直接按文本打开勒索信（F12不行，浏览器只会提供自己认识的部分的源代码），拿出来隐藏的base64，解个码，就能得到嵌着作者名字的XML：

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- WannaEscape v1.00 by ZHANGSAN, 2022-03-31 -->
<WannaEscape>
	<email>ezforever@example.com</email>
	<infected>2022-04-01T06:25:22.000Z</infected>
</WannaEscape>
```

预期解其实不要求对MHTML有多了解，而是更偏向探索的过程——发现不同浏览器打开文件显示内容不同，从而想到去看一眼源代码，base64的隐藏数据就映入眼帘了。~~不过忘记了升级到Win11的同学电脑上没有IE……已经在暴打我自己了~~

MHTML还有其他格式，如POST表单用的`multipart/form-data`，在此不再赘述，感兴趣的同学可以去阅读格式标准[RFC2557](https://www.rfc-editor.org/rfc/rfc2557)。

---

## 骗！偷袭！绑架勒索！【任务B2：幕后黑手】

*Misc ?*, by EZForever

*本题在完成【任务B】后可见。*

### 题目描述

**本题的剧情接续【任务B】。**

所以这个勒索病毒是张三做的咯？他一个遵纪守法好青年怎么开始做黑产了？

想到这，你突然意识到，自从去年五一张三[去探险结果“掉进湖里”](https://zybuluo.com/EZForever/note/1793801)之后，你都没怎么和他联系过。这个学期开始甚至连人影都见不到了。

你掏出手机、打开QQ，打算就勒索病毒的事盘问他一番。

对面没有回应。

“可能他忙着赶作业没看见吧。”你耸耸肩，心想。

不过转天早上起床，手机上的消息记录却着实把你吓了一跳。

晚上三点半，张三回了你的消息，一连回了十几条，但是都被撤回了。他还发了个文件过来，因为QQ缓存了没被撤回。

你又试图发消息过去，但是对面下线了。

众所周知张三老谜语人了，但发生这样的事情很难让人不多想。再回头看那封勒索信，你越看，越觉得事有蹊跷……

张三发生了什么？是什么，或者谁，让他走上了黑产的道路？

**本题答案为由英文字母构成，无空格等特殊符号，不遵守flag格式。**

*附件：`hint.zip`*

### 解析

答案： `KOALI`/`KOALIMADEMEDOTHIS`/`KOALIMADEMEDOTHISIVEBEENABDUCTEDSENDHELP`

嗯，对，张三老谜语人了。

题给文件解压缩之后只有一个特殊字符：` `，UTF-8编码`C2 A0`。这个是[一种特殊的空格](https://www.compart.com/en/unicode/U+00A0)，一般用于网页排版不允许换行的地方。题目明示勒索信里有蹊跷，重新打开勒索信，全文搜索这种空格，会发现只有三段包含这个特殊字符，这三段的换行还非常乱：

```
Please check the
current price and buy
some Dogecoins, then send the
correct amount
to the address specified below.
```

后面剩下的两端的换行虽然正常，但是在正文中间夹着`<i></i>`，每个标签都圈出了一个字母：

```
We strongly re<i>c</i>ommend you to not remove the software, and disable your anti-virus for a while, until you pay and the paym<i>e</i>nt gets processed.
```

> We strongly re*c*ommend you to not remove the software, and disable your anti-virus for a while, until you pay and the paym*e*nt gets processed.

把所有圈出来的字母单独提出来，得到另一个提示：“spaces”，即“空格”。

额，的确，早就看出来空格有问题了。这里就需要一点脑洞才能继续了。提示说的空格是指普通空格，如果在上面“错落有致”的段落里把所有空格标出来，可以发现每行的两种空格最多只有四个：

```
Please#check+the                #+
current#price+and+buy           #++
some+Dogecoins,+then+send+the   ++++
correct+amount                  +
to+the#address+specified+below. +#++
```

这些空格其实构成了摩尔斯电码（[这里有个交互式码表，挺有趣的](https://morsecode.world/international/morse2.html)），解码出来就能得到张三隐藏的信息：“KOALI MADE ME DO THIS, I'VE BEEN ABDUCTED, SEND HELP”。看来他是被绑架了，做这个勒索病毒也是被胁迫的。

~~又在迫害koali阿姨，拖出去~~

## 花絮

1. 新生赛出题期间我[Puzzling SE](https://puzzling.stackexchange.com/)刷得有点上头……任务B2的灵感就来源于这上面[把电子邮件](https://puzzling.stackexchange.com/questions/30523/fwd-re-karen-is-missing)[玩出花来](https://puzzling.stackexchange.com/questions/36256/this-is-it-this-is-the-one-find-your-wife)的几个系列题目。任务A和任务B则纯粹是为了这点醋包了顿饺子。
2. 从题目名称开始，整道题都满是张三最终遭遇的伏笔：“绑架勒索”、勒索病毒叫WannaEscape（“想逃”）、一个学期没见过人影、发的消息“被”撤回……
3. 解答内鬼的问题，为什么选用`&nbsp;`作为特殊空格：Unicode定义了[一大堆](https://jkorpela.fi/chars/spaces.html)各种宽度的空格，但所有编辑器都正常显示而且宽度和标准空格一致的空格只有这一种。造成解题上的迷惑我深表歉意。~~（才怪，出题人怎么会好心道歉）~~
4. 为什么koali阿姨出现得这么突兀？是因为原定计划在任务B2后面还有一道题：“任务B3：法外狂徒”（知道人被绑架了肯定要去救他对吧），而这道题的设计思路是koali提出来的。不过因为是道线下misc，现在疫情封校没法出也没法做，便只能搁置了。

