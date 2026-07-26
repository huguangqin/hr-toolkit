# -*- coding: utf-8 -*-
"""清理本次产生的两篇草稿：字面转义旧稿 + 重发稿，避免重复。"""
import os
import json
import requests

APPID = os.environ.get("WX_APPID")
APPSECRET = os.environ.get("WX_APPSECRET")
TO_DELETE = [
    "PIz1VNN6cucI18dyCACScL_PRLgOrTgT2mJegK7EXIYZRsnHIVHjfcGB8ZlSgzUZ",  # 早期 ensure_ascii=True 字面转义稿(真乱码)
    "PIz1VNN6cucI18dyCACScBjfF9WSZR6SV-rCY2hflMfhpokh_fvvEVUGtC84MeiE",  # 重发稿(内容正确但是重复)
]
tok = requests.get(
    "https://api.weixin.qq.com/cgi-bin/token",
    params={"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET},
    timeout=10,
).json()["access_token"]
for m in TO_DELETE:
    r = requests.post(
        "https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=" + tok,
        data=json.dumps({"media_id": m}, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    print("删除", m[-12:], "->", r.json().get("errmsg"), r.json().get("errcode"))
