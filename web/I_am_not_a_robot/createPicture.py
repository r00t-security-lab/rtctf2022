from typing import Tuple
from PIL import Image,ImageDraw
import random
import sql
import uuid

def randomMathProblem()->Tuple[str,int]:
  #随机生成一个数字
  num1=random.randint(1,1000)
  num2=random.randint(1,1000)
  #随机生成一个运算符
  op=random.choice(['+','-','*','/'])
  #随机生成一个答案
  ans=eval(str(num1)+op+str(num2))
  #生成一个题目
  problem=str(num1)+op+str(num2)
  return problem,ans

def Str2pic(problem:str,dir:str)->None:
  im = Image.new("1", (problem.__len__()*6+5, 10), (1))
  dr = ImageDraw.Draw(im)
  dr.text((1, 0), problem, fill=0)
  im.save(dir)

def createPic()->str:
  problem,ans=randomMathProblem() 
  picNo=uuid.uuid1()
  Str2pic(problem,"pic/"+str(picNo)+".webp")
  sql.set("insert into problem values(??,??)",str(picNo),ans)
  return str(picNo)
