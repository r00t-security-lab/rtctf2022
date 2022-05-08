# ezSQL

- 出题人&验题人: pyy
- 这题和`免费的留言板`是连起来的, 源码在`massage_board`文件夹内。

## 题目内容

简单的SQL题, 你只需要登录进去就可以啦!

(网站打开的时候可能比较慢, 请耐心等待几秒)

tips: 可能不需要注册也可以登录的吧?

tips2: 背后的数据库不是mySQL, 是sqlite哦~

## 出题思路

SQL注入还是挺常用的, 来考一下。

本题注册是一个误导(或者说你能猜到邀请码是`r0v0t 2022 with randomToken`也可以(?) )。用的是sqlite数据库, 所以`#`是无法注释后面的字符的。语句用的是双引号围起来的username和password, 一般搜万能密码然后输进去试就可以进去。我试了一下, 好像sqlmap打不通(也可能是我不会用2333)。

## 解题思路

### 预期解1

一般注入有`没有引号包裹的`, `单引号包裹`, `双引号包裹`这三种。我们这题用户名打一个`"`进去, 发现报错。那就是双引号包裹的。偷看一下源码, 发现语句是`select * from accounts where username="{username}" and password="{password}";`(不能偷看源码的话就要猜了, 不过一般都是这个语句)。所以我们构造一句`select * from accounts where username="" or 1=1 or "" and password="233";`。这样的话只要数据库里有数据, 就会返回数据, 由于一般判断条件就是返回的条数>=1所以就登陆成功了。

有的同学可能构造的是select * from accounts where username="`" or "1"="1`" and password="233"; ,由于or优先级低于and, 所以最后条件会这样执行: username="" or ("1"="1" and password="233"), 最后不会有数据返回。

## 题外话

留言板题也可以使用高级的sql注入来解。关键词: 布尔盲注。注意要用sqlite的注入语句, 这些语句可以在hackbar里找到。
