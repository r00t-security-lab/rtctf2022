from typing import Any, Callable, Dict, List, Tuple
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re, functools


url='sqlite:///sql.db'


__all__=['get','set']

# echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
engine = create_engine(
  url, encoding='utf8', echo=False
)

# SQLAlchemy中，CRUD是通过会话进行管理的，所以需要先创建会话，
# 每一个SessionLocal实例就是一个数据库session
# flush指发送到数据库语句到数据库，但数据库不一定执行写入磁盘
# commit是指提交事务，将变更保存到数据库文件中
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)

session = SessionLocal()
# 创建基本映射类
# SqlBase = declarative_base()

def filter(input, fuzzy=False)->str:
  if input in [True,False]:
    return " ".join(['',str(input),''])
  elif input is None:
    return ' null '
  ans=str(input)
  if fuzzy:
    ans="".join(['%',ans,'%'])
  return "".join([" ('",ans.replace("'","''"),"') "])

def get(sentence:str, *args)-> List[Tuple]:
  func={'??':filter,'?l?':functools.partial(filter,fuzzy=True)}
  ls=re.split('(\\?\\?|\\?l\\?)',sentence)
  for i in range(1,len(ls),2):
    ls[i]=func[ls[i]](args[i//2])
  return session.execute(''.join(ls)).all()

# def queryObj(cls:BaseModel, sentence, *args)->List[Any]:
#   ls=queryList(sentence,*args)
#   return [cls.parse_obj(dic) for dic in ls]

def set(sentence:str, *args, **kwargs)-> bool:
  func={'??':filter,'?l?':functools.partial(filter,fuzzy=True)}
  ls=re.split('(\\?\\?|\\?l\\?)',sentence)
  for i in range(1,len(ls),2):
    ls[i]=func[ls[i]](args[i//2])
  try:
    session.execute(''.join(ls))
    return True
  except Exception as e:
    if 'echo' not in kwargs.keys() or kwargs['echo']==True:
      print('\033[31m'+str(e)+'\033[0m')
    return False
