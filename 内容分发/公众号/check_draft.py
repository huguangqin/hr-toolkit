#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读确认：列出公众号草稿箱前几条，验证草稿是否入库（不创建、不修改）。"""
import os
import requests

APPID = os.environ.get("WX_APPID")
APPSECRET = os.environ.get("WX_APPSECRET")

r = requests.get(
    "https://api.weixin.qq.com/cgi-bin/token",
    params={"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET},
    timeout=10,
)
r.encoding = "utf-8"
tok = r.json()["access_token"]

url = "https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=%s" % tok
resp = requests.post(url, json={"offset": 0, "count": 5, "no_content": 1}, timeout=30)
resp.encoding = "utf-8"
resp = resp.json()

print("草稿总数 total_count:", resp.get("total_count"))
for a in resp.get("item", []):
    art = a["content"]["news_item"][0]
    print("media_id:", a.get("media_id"), "| title:", art.get("title"))
