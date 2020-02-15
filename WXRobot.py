# -*- coding: utf-8 -*-
from flask import request
from flask import Flask, make_response
import hashlib
import requests
import json
import time
import re
import xml.etree.ElementTree as ET

#author:uniartisan
#blog: https://blog.uniartisan.com

app = Flask(__name__)
# app.debug = True

@app.route("/")
def index():
    return "Hello World!"

@app.route('/Weixin', methods=['GET'])                          # 获取Wechat临时参数
# route() 装饰器用于把一个函数绑定到一个 URL
# 在微信公众号修改配置那里，如果你写的是“/wechat/”在括号里，就要在二级域名后面加上，不然就会出现token验证失败
def wechat_tuling():
    if request.method == 'GET':
        my_signature = request.args.get('signature', '')        # 获取携带 signature微信加密签名的参数
        my_timestamp = request.args.get('timestamp', '')        # 获取携带随机数timestamp的参
        my_nonce = request.args.get('nonce', '')                # 获取携带时间戳nonce的参数
        my_echostr = request.args.get('echostr', '')            # 获取携带随机字符串echostr的参数
        token = 'YourToken'                                        # 这里输入你要在微信公众号里面填的token，保持一致
        data = [token, my_timestamp, my_nonce]
        data.sort()                                             # 进行字典排序
        temp = ''.join(data)                                    # 拼接成字符串
        mysignature = hashlib.sha1(temp.encode('utf-8')).hexdigest()
        # 判断请求来源，将三个参数字符串拼接成一个字符串进行sha1加密,记得转换为utf-8格式
        if my_signature == mysignature:                         # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
            return make_response(my_echostr)
        else:
            return ''
            
@app.route('/Weixin', methods=['POST'])                         # 文本传输，仅兼容 明文、兼容模式     
def autoplay():
    # 下面这里是对请求解析，返回图灵机器人的回复
    xml = ET.fromstring(request.data)
    # 获取用户发送的原始数据
    # fromstring()就是解析xml的函数，然后通过标签进行find()，即可得到标记内的内容。
    toUser = xml.find('ToUserName').text
    fromUser = xml.find('FromUserName').text
    msgType = xml.find("MsgType").text
    # 获取向服务器发送的消息
    createTime = xml.find("CreateTime")
    content = xml.find('Content').text
    xml_sta = '<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>'
    # 返回数据包xml的文本回复格式
    if msgType == 'text':
        # 判断消息类型, 如果返回的字段是text，则是文字
        tuling_reply = reply(content)
        # 调用图灵机器人api回复赋值给xml里面的content，这里定义为tuling_reply
        res = make_response(xml_sta % (fromUser, toUser, str(int(time.time())), tuling_reply))
        # 微信公众号做出响应，自动回复的格式如上
        res.content_type = 'application/xml'
        # 定义回复的类型为xml
        return res
        # 输出自动回复
    else:
        # 如果输入非文字的则会提示下面这句话
        return '我还只会文字，请等我慢慢成长，谢谢！'          
        
def reply(info):
        # 调用图灵机器人api
        api = 'http://openapi.tuling123.com/openapi/api/v2'
        # 请求api接口的网址
        data = {
            "perception": {
                "inputText": {
                    "text": info
                }
            },
            "userInfo": {
                "apiKey": "Yourkey",
                "userId": 'Weixin',
            }
        }
        # 请求的数据（这里只有对话的，可以添加url或者其他，有问题查看官方文档
        jsondata = json.dumps(data)
        # 根据官方文档，需要把利用json.dumps()方法把字典转化成json格式字符串
        response = requests.post(api, data=jsondata)
        # 发起post请求
        robot_res = json.loads(response.content, encoding='utf-8')
        # 把json格式的数据再转化成Python数据输出
        robot_reply = robot_res["results"][0]['values']['text']
        return robot_reply

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)          # 加上host这段，就可以在浏览器访问你的网址, 建议配合nginx反向代理
