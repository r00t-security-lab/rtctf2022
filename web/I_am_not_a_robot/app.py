from typing import List
from fastapi import FastAPI, Form, HTTPException, Request, Response, Cookie
import sql
import uvicorn
from fastapi.responses import HTMLResponse
import jwt
import createPicture
from fastapi.staticfiles import StaticFiles
import random
import requests

os=__import__("os")
if not os.path.exists('pic'):
  os.makedirs('pic')
del os

NUM=500
form="""<form method="POST"><input type="text" name="ans"><input type="submit" value="提交"></form>"""
cheat="""<title>直钩钓鱼</title><br><br>如果你输入比赛平台的账户与密码的话, 我就50.2%相信你是人类!<form method="POST" action="/cheat">username:<br><input type="text" name="username"><br>password:<br><input type="text" name="password"><br><input type="submit" value="提交"></form>"""

def youWontLikeThis(username,password):
  import requests
  import re
  sess=requests.Session()
  nonce=re.findall("""(?<=<input id="nonce" name="nonce" type="hidden" value=").*?(?=">)""",sess.get("http://81.69.243.226:4000/login").text)[0]
  sess.post('http://81.69.243.226:4000/login',data={"name":username,"password":password,"nonce":nonce,"_submit":"Submit"})
  csrf_token=re.findall("""(?<='csrfNonce': ").*?(?=",)""",sess.get("http://81.69.243.226:4000/challenges").text)[0]
  ans2=sess.post('http://81.69.243.226:4000/api/v1/challenges/attempt',json={"challenge_id":6,"submission":"r00t{愿者上钩}"},headers={'CSRF-Token':csrf_token})
  return ans2.text.find("You don't have the permission")==-1

class jwtException(Exception):
  pass

app = FastAPI(docs_url=None,redoc_url=None)
app.mount("/pic", StaticFiles(directory="pic"), name="pic")

def validationNum(cookie: str)->dict:
  try: 
    data = jwt.decode(cookie, "admin", algorithms=['HS256'])
    return data
  except Exception: 
    if cookie==None:
      return {'n':0,'problem':'-1'}
    raise jwtException()
  
@app.exception_handler(jwtException)
async def jwtException_exception_handler(request: Request, exc: jwtException):
  res=HTMLResponse(status_code=401,content="""<h1>不要动我的小饼干!</h1><meta http-equiv="refresh" content="1;url=/">""")
  res.set_cookie('workedOutCaptchaNumber', '', max_age=0)
  return res

blackList=['eval','exec','import','system','getattr','open','kill','+','*']
def filter(s: str)-> List[str]:
  return [black for black in blackList if black in s]

@app.get("/",response_class=HTMLResponse)
def get(response: Response, workedOutCaptchaNumber: str=Cookie(None)):
  lastInfo=validationNum(workedOutCaptchaNumber)
  exist=__import__('os').path.exists('pic/'+lastInfo['problem']+'.webp')
  if lastInfo['n']==0 or not exist:
    picDir=createPicture.createPic()
    response.set_cookie('workedOutCaptchaNumber', jwt.encode({'problem':picDir,'n':lastInfo['n']}, 'admin', algorithm='HS256'))
    return f"你只需要连续答对{NUM-lastInfo['n']}题就可以证明你是人类啦! <br>提示: 你应当使用分数回答除法题。<br><img src='/pic/{picDir}.webp' height=100px>"+form+(cheat if lastInfo['n']==0 else '')
  else:
    return f"你只需要再连续答对{NUM-lastInfo['n']}题就可以证明你是人类啦! <br>提示: 你应当使用分数回答除法题。<br><img src='/pic/{lastInfo['problem']}.webp' height=100px>"+form

@app.post("/",response_class=HTMLResponse)
def post(response: Response, workedOutCaptchaNumber: str=Cookie(None), ans: str=Form('None')):
  #过滤
  ls=filter(ans)
  if ls.__len__()!=0:
    response.set_cookie('workedOutCaptchaNumber', '', max_age=0)
    return f"""<h1>不要让我看到{ls}!</h1><meta http-equiv="refresh" content="1;url=/">"""
  
  lastInfo=validationNum(workedOutCaptchaNumber)
  picDir=createPicture.createPic()
  
  try:
    ans=str(eval(ans))
    print(ans)
  except Exception as e:
    print("except:",e,'\n',ans)
    response.set_cookie('workedOutCaptchaNumber', '', max_age=0)
    return f"""<h1>{e}</h1><meta http-equiv="refresh" content="1;url=/">"""
  
  queryAns=sql.get("select ans from problem where id=?? limit 1",lastInfo['problem'])
  if queryAns.__len__() and queryAns[0][0]==ans:
    if lastInfo['n']+1>=NUM:
      return "r0v0t{l @nn n07 a r0b0t!}"
    response.set_cookie('workedOutCaptchaNumber', jwt.encode({'problem':picDir,'n':lastInfo['n']+1}, 'admin', algorithm='HS256'))
    return f"""<meta http-equiv="refresh" content="0;url=/?noSamePost={random.getrandbits(32)}">"""
  else:
    response.set_cookie('workedOutCaptchaNumber', jwt.encode({'problem':picDir,'n':0}, 'admin', algorithm='HS256'))
    return f"""回答错误! 这种简单题的答案怎么会是{ans}呢! 请重新开始验证吧......<meta http-equiv="refresh" content="1;url=/?noSamePost={random.getrandbits(32)}">"""

@app.post("/cheat",response_class=HTMLResponse)
def wishFish(response: Response, workedOutCaptchaNumber: str=Cookie(None), username: str=Form('aodsiufcbv'), password: str=Form('3456bw7xasdfg')):
  lastInfo=validationNum(workedOutCaptchaNumber)
  if youWontLikeThis(username,password):
    response.set_cookie('workedOutCaptchaNumber', jwt.encode({'problem':lastInfo['problem'],'n':251}, 'admin', algorithm='HS256'))
    return f"""<h1>愿者上钩!</h1><meta http-equiv="refresh" content="1;url=/">"""
  else:
    return f"""<h1>你骗我QAQ</h1><meta http-equiv="refresh" content="1;url=/">"""

if __name__ == "__main__":
  uvicorn.run(app="app:app", host="0.0.0.0", port=8080)
