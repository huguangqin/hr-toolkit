#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动推送/更新公众号草稿：本地精编 HTML（全内联样式） + 列表封面  ->  公众号草稿箱

关键约束：
  1) 排版：微信草稿接口会【丢弃 <style> 块】，只认元素上的 style="..." 内联样式。
     因此 HTML 里所有样式必须写成内联，否则只剩 <b>/<strong> 加粗能生效。
  2) 乱码：请求体用 json.dumps(ensure_ascii=False) 以 UTF-8 字节发送，并显式带
     Content-Type: application/json; charset=utf-8；读取响应前强制 r.encoding='utf-8'
     （微信响应常不带 charset，requests 会误按 Latin-1 解码成假乱码）。
  3) 封面：草稿接口强制要求 thumb_media_id（列表封面），正文已不配图；若要发布时
     正文顶部也不显示封面，需在编辑器里手动勾选「不显示封面」。

幂等更新：
  先按 title 在草稿箱查找已有草稿，找到则 drafts/update 原地更新（修乱码 /
  改稿都不会堆重复草稿）；找不到才 drafts/add 新建。仅入草稿箱，不群发。

使用前（凭据不要写进代码或记忆，用环境变量临时传入）：
  pip install requests
  $env:WX_APPID="你的appid"
  $env:WX_APPSECRET="你的appsecret"
  python push_to_mp.py
"""
import os
import re
import glob
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
APPID = os.environ.get("WX_APPID")
APPSECRET = os.environ.get("WX_APPSECRET")

ARTICLE_TITLE = "HR 面试总靠感觉？一张表搞定"


def _find(ext):
    files = glob.glob(os.path.join(BASE, "*" + ext))
    if not files:
        raise FileNotFoundError("未找到 %s 文件" % ext)
    return files[0]


HTML_PATH = _find(".html")
IMG_PATH = _find(".png")


def post_json(url, payload):
    """以 UTF-8 字节发送 JSON（ensure_ascii=False），根治中文乱码。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    r = requests.post(url, data=body, headers=headers, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"  # 关键：微信响应常不带 charset，强制 UTF-8 解码，避免被当 Latin-1 误判乱码
    return r.json()


def get_token():
    r = requests.get(
        "https://api.weixin.qq.com/cgi-bin/token",
        params={"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET},
        timeout=10,
    )
    r.raise_for_status()
    r.encoding = "utf-8"
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError("获取 access_token 失败: %s" % data)
    return data["access_token"]


def upload_image(token):
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image" % token
    with open(IMG_PATH, "rb") as f:
        r = requests.post(url, files={"media": f}, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"
    data = r.json()
    if "media_id" not in data:
        raise RuntimeError("上传图片失败: %s" % data)
    return data["media_id"], data.get("url", "")


def build_content():
    """读取 HTML 正文。样式已全部内联（微信草稿接口会丢弃 <style> 块，
    只认 element 上的 style="..."），所以直接返回 body 内容即可。"""
    html = open(HTML_PATH, encoding="utf-8").read()
    body = re.search(r"<body[^>]*>(.*?)</body>", html, re.S)
    if not body:
        raise RuntimeError("HTML 结构异常，找不到 body")
    inner = body.group(1)
    # 去掉内部作者备注（发布前清理）
    inner = re.sub(r'<p class="footnote">.*?</p>', "", inner, flags=re.S)
    return inner


def find_existing_draft(token, title):
    url = "https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=%s" % token
    resp = post_json(url, {"offset": 0, "count": 20, "no_content": 1})
    for item in resp.get("item", []):
        art = item["content"]["news_item"][0]
        if art.get("title") == title:
            return item.get("media_id")
    return None


def add_draft(token, article):
    url = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=%s" % token
    return post_json(url, {"articles": [article]})


def update_draft(token, media_id, article):
    url = "https://api.weixin.qq.com/cgi-bin/draft/update?access_token=%s" % token
    return post_json(url, {"media_id": media_id, "index": 0, "articles": [article]})


def main():
    if not APPID or not APPSECRET:
        raise SystemExit("缺少环境变量 WX_APPID / WX_APPSECRET，请先设置后再运行。")
    token = get_token()
    # 上传列表封面图（微信草稿接口强制要求 thumb_media_id）；正文已不配图。
    media_id, _ = upload_image(token)
    content = build_content()
    article = {
        "title": ARTICLE_TITLE,
        "author": "大勤",
        "digest": "一张结构化面试评估表，把'凭感觉'变成'有证据'。完整模板在 GitHub：hr-toolkit。",
        "content": content,
        "thumb_media_id": media_id,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    existing = find_existing_draft(token, ARTICLE_TITLE)
    if existing:
        res = update_draft(token, existing, article)
        print("已原地更新草稿 media_id=%s :" % existing, res)
        if res.get("errcode", 0) == 0:
            print("[OK] 乱码草稿已原地修正，去后台「草稿箱」刷新确认即可（不会自动群发）。")
    else:
        res = add_draft(token, article)
        print("已新建草稿:", res)
        if "media_id" in res:
            print("[OK] 已写入公众号草稿箱，去后台「草稿箱」确认即可（不会自动群发）。")


if __name__ == "__main__":
    main()
