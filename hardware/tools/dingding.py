#!/usr/bin/env python
# coding: utf-8

# ## dingding群机器人接口

import requests
import json
import time
import hmac
import hashlib
import base64
import urllib


def ding_send(data, key):
    headers = {"Content-Type": "application/json"}
    ################################
    json_data = json.dumps(data)
    print(json_data)
    ################################
    # timestamp = long(round(time.time() * 1000))
    timestamp = round(time.time() * 1000)
    print(timestamp)
    ################################
    secret = key
    secret_enc = secret.encode(encoding="utf-8")
    string_to_sign = "{}\n{}".format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode(encoding="utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(sign)
    ################################
    ding_url = "https://oapi.dingtalk.com/robot/send?access_token=a54adad7b6472fe1ef4c353f6e57f5d51ed76c3aa952ad681eeb909d670a729e&timestamp={0}&sign={1}".format(
        timestamp, sign
    )
    requests.post(url=ding_url, data=json_data, headers=headers)


def ding_fc(links, key):

    data = {
        "msgtype": "feedCard",
        "feedCard": {"links": []},
    }

    data["feedCard"]["links"] = links

    ding_send(data, key)


def ding_ac_multi(title, text, url, key):

    data = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": "",
            "text": "",
            "hideAvatar": "0",
            "btnOrientation": "0",
            "btns": [
                {"title": "aaaa", "actionURL": "https://www.dingtalk.com/"},
                {"title": "bbbb", "actionURL": "https://www.dingtalk.com/"},
            ],
        },
    }

    data["actionCard"]["title"] = title
    data["actionCard"]["text"] = text
    data["actionCard"]["singleURL"] = url

    ding_send(data, key)


def ding_ac_single(title, text, url, key):

    data = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": "",
            "text": "",
            "hideAvatar": "0",
            "btnOrientation": "0",
            "singleTitle": "阅读全文",
            "singleURL": "",
        },
    }

    data["actionCard"]["title"] = title
    data["actionCard"]["text"] = text
    data["actionCard"]["singleURL"] = url

    ding_send(data, key)


def ding_md(title, text, key, at_list, at_all=False):

    data = {
        "msgtype": "markdown",
        "markdown": {"title": "", "text": "",},
        "at": {"atMobiles": ["",], "isAtAll": False},
    }

    data["markdown"]["title"] = title
    data["markdown"]["text"] = text
    data["at"]["atMobiles"] = at_list
    data["at"]["isAtAll"] = at_all

    ding_send(data, key)


def ding_link(text, title, picurl, url, key):

    data = {
        "msgtype": "link",
        "link": {"text": "", "title": "", "picUrl": "", "messageUrl": ""},
    }
    data["link"]["text"] = text
    data["link"]["title"] = title
    data["link"]["picUrl"] = picurl
    data["link"]["messageUrl"] = url

    ding_send(data, key)


def ding_text(text, key, at_list, at_all=False):

    data = {
        "msgtype": "text",
        "text": {"content": "haha"},
        "at": {"atMobiles": ["",], "isAtAll": False},
    }

    data["text"]["content"] = text
    data["at"]["atMobiles"] = at_list
    data["at"]["isAtAll"] = at_all

    ding_send(data, key)


def main():
    at_list = [
        18500190963,
    ]
    key = "SEC149c65bfef0df7069427b7972730a3c4ed151871eb4d2b74e4ba38bf0aec5c0f"

    md = """
![screenshot](@lADOpwk3K80C0M0FoA) 
# 一绶标题
## 文字加粗、斜体

**bold**
*italic*

无序列表

- item1
- item2

链接
[this is a link](http://name.com)

"""

    links = []

    item = {
        "title": "时代的火车向前开",
        "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
        "picURL": "@lADOpwk3K80C0M0FoA",
    }

    links.append(item)
    links.append(item)
    links.append(item)
    links.append(item)

    ding_text("中国字", key, at_list)
    ding_link(
        "今天的天气真不错啊！！！", "天气", "http://www.baidu.com/pic", "http://www.baidu.com", key
    )

    ding_md("中国", md, key, at_list)
    ding_ac_single("中国", md, "http://www.baidu.com", key)
    ding_ac_multi("中国", md, "http://www.baidu.com", key)

    ding_fc(links, key)


if __name__ == "__main__":
    # execute only if run as a script
    # os.environ["DEBUSSY"] = "1"

    main()
