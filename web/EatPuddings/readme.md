---
title: EatPuddings writeup
autho: koali
---

# EatPuddings



## 出题思路

一部分借鉴了hackergame的思路，另外想考js的链判断运算符和Null判断运算符（其实是那段时间刚刚看到所以就拿来出题了23333）

## 题目描述

我要吃布丁！！

## 解题思路

翻一下js，可以看到这一段关键代码

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

意思是cps>20的时候会执行Re这个浏览器接口对象，给flag.php传一个name参数，参数的内容是`(a?.o||((+ +'a'+'o')??!!a?.a)).toLocaleLowerCase()`的执行结果。那就很简单了，有两种做法。

第一种是得到这个参数的值，手动get一下。

第二种是js调试，可以打断点去调这个cps，把它改大一些（这里做法就五花八门啦）

### 解一

最简单的办法就是把`(a?.o||((+ +'a'+'o')??!!a?.a)).toLocaleLowerCase()`这一串拿去控制台执行一下，很快就得到答案了。

首先把这个表达式拆开来看

`a?.o||((+ +'a'+'o')??!!a?.a)`

=>`a?.o` 

=>`+ +'a'+'o'`

=>`!!a?.a`

=>`((+ +'a'+'o')??!!a?.a)`

差不多就是这四部分。

第一部分是`a?.o`，判断a对象是否存在一个o属性，如果不存在就返回undefined。

第二部分是`+ +'a'+'o'`，这里涉及到类型转换的问题，`+'a'`本身会返回一个NaN，告诉你这不是一个数字（Not a Number），因为'a'不能被解析成数字使用。所以可以化简为`+'NaN'+'o'`，也就是'NaNo'。

第三部分是`!!a?.a`，和第一部分一样，`a?.a`会返回一个undefined，但是前面加了!!，相当于取反两次，`!a?.a`返回true，`!!a?.a`返回false。

最后一个部分是`??`的使用，也就是如果`+ +'a'+'o'`不是undefined或null就返回它，否则返回`!!a?.a`。那结果显而易见，后面的内容可以直接忽略，返回`NaNo`

综上，最后返回的结果是`NaNo`，再执行`toLocaleLowerCase()`就能得到`nano`，也就是name的值。所以只需要访问/flag.php?name=nano就能拿到flag。

参考链接

https://stackoverflow.com/questions/57456188/why-is-the-result-of-ba-a-a-tolowercase-banana

https://juejin.cn/post/6867691960452022280

https://blog.csdn.net/yun_master/article/details/115015113



### 解二

js调试也很方便，可以试着在有关cps这个参数的地方打上断点，然后改值就行。这里需要注意一下时间不能太久，可以考虑换成无尽模式。

### 非预期

有人写外挂QAQ