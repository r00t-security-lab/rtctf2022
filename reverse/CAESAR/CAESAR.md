本题的要点是zip伪加密和zip明文攻击。

将最初的压缩包放入010editor（或其他hex editor)找到对应16进制位即可。

首先找到压缩源文件目录区：50 4B 01 02：目录中文件文件头标记(0x02014b50) 

后面的14 00指压缩使用的 pkware 版本

再后面的14 00指解压文件所需 pkware 版本 
00 00为全局方式位标记（伪加密的关键） 
08 00为压缩方式 

![image-20220515222801954](C:\Users\11721\AppData\Roaming\Typora\typora-user-images\image-20220515222801954.png)

当这里的00 00为其他值（也就是你们拿到的zip）时，文件就会被伪加密，只需改回00 00就可以了。

解压文件后得到一个flag.zip和tips.txt

打开flag.zip，惊喜的发现里面也有个的tips.txt。将tips.txt使用zip压缩方式压缩后，对比两者CRC-32校验码，发现是相同的，说明两者是同一文件，查看tips.txt大小，满足明文攻击条件。直接将flag.zip和tips.zip放入ARCPHR进行明文攻击即可。