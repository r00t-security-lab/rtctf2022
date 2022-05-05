from fastapi import FastAPI, Request, Response
import uvicorn
import redis
from fastapi.responses import HTMLResponse

app = FastAPI()
r=redis.Redis(host="127.0.0.1",port=6379)

@app.middleware("http")
async def slowApi(request: Request, call_next):
  #print(request.headers.items())
  ip:str=request.headers.get('X-Forwarded-For') or request.client.host
  ip=ip.split(",")[0]
  if r.get(ip) is not None:
    return HTMLResponse(f"""Your IP is {ip}. Too many requests! <meta http-equiv="refresh" content="2;url=/">""",429)
  r.set(ip,1,px=1000)
  response = await call_next(request)
  return response

@app.get("/wp",response_class=HTMLResponse)
async def flag():
  return "tips: 通过敏感目录泄露, 我们往往能获取网站的源代码和敏感的URL地址, 如网站的后台地址等。此外, 可以通过Banner信息来获得解题思路。如得知网站是用ThinkPHP的Web框架编写时, 我们可以尝试ThinkPHP框架的相关历史漏洞。或者得知这个网站是Windows服务器, 那么我们在测试上传漏洞时可以根据Windows的特性进行尝试。<br>------布什·沃·兹吉便德<br>r00t{70952145-19f6-4acd-9d58-21b32c990dae}"

@app.get("/Admin",response_class=HTMLResponse)
async def dream():
  return "或者你也去做个梦? 不过据说两个人不会做相同的梦来着。"

@app.get("/",response_class=HTMLResponse)
async def root():
  return "有一天, 一个flag飞入我的梦中。我看见它, 仿佛久旱逢甘霖, 又似他乡遇故知。它是如此的美妙! 我迫不及待地将其记录下来, 放在了这个网站的某个地方。<br><!--每个ip的访问间隔最好超过10秒, 1秒也行, 随便你。\n你知道吗: 状态码429是说你访问频率太高了, 并不是说这个页面不存在哦~\n虽然php是世界上最好的语言, 但还是fastapi得我心。-->"

if __name__ == "__main__":
  uvicorn.run(app="app:app", host="0.0.0.0", port=8080)
