仔细读题，你就能被谐音梗带上正确的道路。zebra即斑马，斑马身上只有黑白两种颜色，降维打击的斑马，就变成了二维“马”。没错，本题的重要线索是，最终结果会是一个二维码。

将zebra拖入ida种分析，就可以得到大致逻辑，

![image-20220515232241312](C:\Users\11721\AppData\Roaming\Typora\typora-user-images\image-20220515232241312.png)

首先==的优先度大于=，所以将表达式f[i]==1的结果赋值给t[cou]，即当f[i]为时，t[cou]为1，f[i]为0则t[cou]为0。

再将t[cou]乘2，可以视为左移一位。

那么整体代码逻辑就出来了，将四个1或者0压缩成一个数。最后和给定的数组对比，如果正确就给出提示Now you can go further with \"from PIL import Image”。

也就是说，我们只需要从给出的数组逆向解压出输入的01二进制串。

那么01二进制串和二维码还有pil有什么关系呢。仔细观察可以发现，这个01字符串存储在一个9216长度的数组中，而9216=96*96，为什么不试着把01排列成96\*96的尺寸，每个01代表一个或黑或白的像素点呢？(9216这个数字肯定是有特殊含义的，解题过程中需要多尝试)

还原出01串后，使用pil的函数putpixel()绘图即可（其他绘图函数亦可）。

![image-20220515233332082](C:\Users\11721\AppData\Roaming\Typora\typora-user-images\image-20220515233332082.png)

![image-20220515233401246](C:\Users\11721\AppData\Roaming\Typora\typora-user-images\image-20220515233401246.png)