import json
from aiohttp import web
from endpoints.Gtime import GetTime
from endpoints.ApiHandler import base_img_request

# 初始化节点
routes = web.RouteTableDef()


# 基础返回  
@routes.get('/')
def hello_world(request):  # put application's code here
    print(f"[{GetTime()}] [request] /")
    return web.Response(body=json.dumps({'code':0,'message': 'Hello! Use path /shop-url or /shop-img to get valorant daily shop','info':'在path后添加/shop-img或者/shop-url来获取每日商店，前者会直接跳转，后者返回一个带图片url的json。示例: /shop-url?account=Riot账户&passwd=Riot密码&img_src=可选参数，自定义背景图'},ensure_ascii=False), status=200, content_type='application/json')


# 直接跳转图片
@routes.get('/shop-img')
async def get_dailshop_img(request):
    print(f"[{GetTime()}] [request] /shop-img")
    try:
        ret = await base_img_request(request)
        if ret['code']==0:
            return web.Response(headers={'Location': ret['message']},status=303)
        else:
            return web.Response(body=json.dumps(ret,ensure_ascii=False), content_type='application/json')
    except:
        return web.Response(body=json.dumps({'code':200,'message': 'unkown err','info':'未知错误'},ensure_ascii=False), content_type='application/json')
    
# 获取图片url
@routes.get('/shop-url')
async def get_dailshop_img(request):
    print(f"[{GetTime()}] [request] /shop-url")
    try:
        ret = await base_img_request(request)
        return web.Response(body=json.dumps(ret,ensure_ascii=False), content_type='application/json')
    except:
        return web.Response(body=json.dumps({'code':200,'message': 'unkown err','info':'未知错误'},ensure_ascii=False), content_type='application/json')




print(f"[API Start] starting at {GetTime()}")
app = web.Application()
app.add_routes(routes)
web.run_app(app, host='127.0.0.1', port=14725)