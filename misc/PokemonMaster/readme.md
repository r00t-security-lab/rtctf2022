# PokemonMaster

先讲讲解题思路，开始的选择技能画面提供了现有的技能供选择，但实际效果仍是输入到框中，所以这个输入框的内容实际是可以自己控制内容的，在已有的列表之外有一个技能可以解决开挂的喷火龙，那就是扮演(Role Play)，将英文输入进去直接选择就能得到这个技能，其实除了这个技能我还写了几个没什么用的技能，不知道有没有人试过。

![image-20220508173042164](http://picturebed-1310517892.file.myqcloud.com/2022/202205081730204.png)

然后讲讲怎么打这只喷火龙，设定上他是"储水"特性，受到水系技能会恢复血量，其他属性的技能有效但在受到致命伤时喷火龙会闪避本次攻击，那么该怎么办呢？其实这里我在两个地方设置了提示，一是选择界面有一行字提示你可选的思路，另一个是进入战斗后每坚持一回合都会有一句战斗提示，九个回合就能拿完

![image-20220508173401391](http://picturebed-1310517892.file.myqcloud.com/2022/202205081734433.png)

![image-20220508173117719](http://picturebed-1310517892.file.myqcloud.com/2022/202205081731766.png)

喷火龙不闪避水系技能，所以只要想办法换掉它的特性，它有概率释放"模仿"技能，而"扮演"可以获取对方的特性，恰巧甲贺忍蛙的特性让他不能获得其他特性，所以甲贺忍蛙使用扮演不会偷取"储水"特性，但是喷火龙模仿后会获得甲贺忍蛙这个没用的特性，从而可以被水系技能击败，所以第一个思路就是学习扮演，让喷火龙模仿后用水系技能带走；

甲贺忍蛙拥有独一无二的必杀技挣扎指的是他的挣扎技能可以无视条件一击必杀，"挣扎"是宝可梦系列一个特殊技能，当精灵所有技能的PP归零，无法释放技能时会自动使用这个技能，因此你要是能熬到技能用完就可以用挣扎打败喷火龙；这里还有一个方法，因为选技能的时候是允许选一样的技能的（虽然选了以后列表会消失，但其实还能选），你可以选一个烟幕降低自己中招的几率，宝可梦的命中下降还是力度蛮大的，而且喷火龙也不一直放招攻击，然后带三个水炮快速耗完PP值，就能用到挣扎，所以金手指其实是削弱，PP值变多了反而更难打了（

还有一种方式就是直接从源码里找flag，我特意把函数名写成了"captueFlag"，看懂可能需要一点点的JS基础，不过难度应该不大：

```react
captureFlag(){
    // console.log('captureFlagnow!');
    let Pokemon={
      Th:_.cloneDeep(skillIndex['Night Slash']),
      Fg:_.cloneDeep(skillIndex['Night Slash']),
      Yu:_.cloneDeep(skillIndex['Role Play']),
      Re:_.cloneDeep(skillIndex['Role Play']),
      Kmn:_.cloneDeep(skillIndex['Role Play']),
      Mstr:_.cloneDeep(skillIndex['Role Play']),
    }
    let megaTxt;
    for(let key in Pokemon){
      switch(key){
        case 'Th':{
          megaTxt=key[0]+key[1]+Pokemon[key].en_name[1]+Pokemon[key].en_name[6];
          megaTxt+='_'+Pokemon[key].en_name[1]+Pokemon[key].en_name[6];
          break;
        }
        case 'Fg':{
          megaTxt+='_'+key[0]+Pokemon[key].en_name[7]+Pokemon[key].en_name[8]+key[1]+':';
          break;
        }
        case 'Yu':{
          megaTxt+=key[0]+Pokemon[key].en_name[1]+key[1];
          break;
        }
        case 'Re':{
          megaTxt+='_'+Pokemon[key].en_name[7]+key[0]+key[1];
          break;
        }
        case 'Kmn':{
          megaTxt+='_'+Pokemon[key].en_name[5]+Pokemon[key].en_name[1]+key[0]+Pokemon[key].en_name[3]+key[1]+Pokemon[key].en_name[1]+key[2];
          break;
        }
        case 'Mstr':{
          megaTxt+='_'+key[0]+Pokemon[key].en_name[7]+key[1]+key[2]+Pokemon[key].en_name[3]+key[3];
          break;
        }
      }
    }
    this.state.pokemon=megaTxt;
    return ;
  }
```

还有很多师傅在控制台改源码得到了flag，但我不是很清楚在服务器上怎么用控制台改= =，下载到本地的话也许可以，但是得会起这项服务（或者开箱即用？），只能说师傅们太厉害了，让出题人涨姿势了；不过队里有大佬跟我提过下断点可以把React函数爆出来就能改了，我还没尝试过

最后就是有一位同学输给了喷火龙还是拿到了flag，我只能说天选之人（是不知道的bug！），真正的宝可梦代师

![QQ图片20220508175749](http://picturebed-1310517892.file.myqcloud.com/2022/202205081758990.png)

---

## 出题杂谈

因为出题的时候没有什么思路，就借之前写过的一个半成品项目完善了一下，写了个游戏题~（结果写了一个星期也就这点完成度）本来就是打算研究一下怎么写个PBO，然后和小伙伴打打对战（虽然根本不会），但是写着写着发现这个战斗系统算上特性、道具、场地似乎需要很大精力，可能还需要优化战斗系统的逻辑结构...于是就暂时搁置啦！如果有人感兴趣的话欢迎dd我一起讨论一下这个

PS：本题的战斗系统虽然不完善，但是没有偷懒，数值都是根据约定严格判定和计算的，除了喷火龙的挂