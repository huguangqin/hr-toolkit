#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动推送公众号草稿：本地精编 HTML + 题图  ->  公众号草稿箱

这是"自动推送"的实现路径（对应微信公众平台开放接口）：
  1. 用 appid + appsecret 取 access_token
  2. 上传题图为永久素材，拿 media_id / url
  3. 把 HTML 里的本地题图路径替换为微信 url，并保留 <style> 以保证排版
  4. 调用 drafts/add 创建草稿（仅入草稿箱，不群发）

使用前（凭据不要写进代码或记忆，用环境变量临时传入）：
  pip install requests
  $env:WX_APPID="你的appid"
  $env:WX_APPSECRET="你的appsecret"
  python push_to_mp.py

依赖：Python 3，requests。Windows PowerShell 设置环境变量用 $env:。
"""
import os
import re
import glob
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
APPID = os.environ.get("WX_APPID")
APPSECRET = os.environ.get("WX_APPSECRET")


def _find(ext):
    files = glob.glob(os.path.join(BASE, "*" + ext))
    if not files:
        raise FileNotFoundError("未找到 %s 文件" % ext)
    return files[0]


HTML_PATH = _find(".html")
IMG_PATH = _find(".png")


def get_token():
    r = requests.get(
        "https://api.weixin.qq.com/cgi-bin/token",
        params={"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError("获取 access_token 失败: %s" % data)
    return data["access_token"]


def upload_image(token):
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image" % token
    with open(IMG_PATH, "rb") as f:
        r = requests.post(url, files={"media": f}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "media_id" not in data:
        raise RuntimeError("上传图片失败: %s" % data)
    return data["media_id"], data.get("url", "")


def build_content(img_url):
    html = open(HTML_PATH, encoding="utf-8").read()
    style = re.search(r"<style>(.*?)</style>", html, re.S)
    body = re.search(r"<body[^>]*>(.*?)</body>", html, re.S)
    if not body:
        raise RuntimeError("HTML 结构异常，找不到 body")
    inner = body.group(1)
    # 题图本地路径 -> 微信 url
    inner = re.sub(r'src="[^"]*Clean_modern_flat_illustration[^"]*"', 'src="%s"' % img_url, inner)
    # 去掉内部作者备注（发布前清理）
    inner = re.sub(r'<p class="footnote">.*?</p>', "", inner, flags=re.S)
    style_block = "<style>%s</style>" % style.group(1) if style else ""
    return style_block + inner


def add_draft(token, article):
    url = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=%s" % token
    r = requests.post(url, json={"articles": [article]}, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    if not APPID or not APPSECRET:
        raise SystemExit("缺少环境变量 WX_APPID / WX_APPSECRET，请先设置后再运行。")
    token = get_token()
    media_id, img_url = upload_image(token)
    content = build_content(img_url)
    article = {
        "title": "HR 面试总靠感觉？一张表搞定",
        "author": "大勤",
        "digest": "一张结构化面试评估表，把'凭感觉'变成'有证据'。完整模板在 GitHub：hr-toolkit。",
        "content": content,
        "thumb_media_id": media_id,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    res = add_draft(token, article)
    print("草稿创建结果:", res)
    if "media_id" in res:
        print("[OK] 已写入公众号草稿箱，去后台「草稿箱」确认即可（不会自动群发）。")


if __name__ == "__main__":
    main()
