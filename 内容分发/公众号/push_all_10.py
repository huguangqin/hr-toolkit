#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量推送 10 篇员工关系热点文章到公众号草稿箱（仅草稿、不群发）。

用法（凭据仅用环境变量临时传入，不落库）：
  WX_APPID=wx6d1b9918671b7f70 WX_APPSECRET=xxxxxxxx python push_all_10.py

依赖：push_to_mp.py（单篇推送，已处理内联样式 / UTF-8 乱码 / 封面匹配 / 按标题幂等）。
每篇调用 push_to_mp.py <html> <标题> <摘要>，封面由 _find_cover() 按 html 词干精准匹配。
微信草稿标题硬上限 64 字节(UTF-8)，_safe_title 兜底截断，避免 45003。
"""
import os
import sys
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
APPID = os.environ.get("WX_APPID")
APPSECRET = os.environ.get("WX_APPSECRET")

if not APPID or not APPSECRET:
    sys.exit("缺少环境变量 WX_APPID / WX_APPSECRET，发布前请提供（仅临时传入，不落库）。")


def _safe_title(s, limit=64):
    """微信草稿标题 UTF-8 上限 64 字节；超长在字符边界截断并加省略号，防 45003。"""
    b = s.encode("utf-8")
    if len(b) <= limit:
        return s
    cut = b[:limit - 3]  # 留 3 字节给 …
    while cut and (cut[-1] & 0xC0) == 0x80:  # 退掉半截多字节字符
        cut = cut[:-1]
    return cut.decode("utf-8", "ignore") + "…"


# (html 文件名, 草稿标题, 摘要) —— 标题按"制造悬念/激发好奇心"规则，且压到 ≤64 字节
ARTICLES = [
    ("超龄用工协议.html",
     "返聘退休员工，这张协议不签公司要兜底",
     "超龄劳动者用工协议模板与返聘风险点，公众号精编版，完整工具表见 GitHub hr-toolkit。"),
    ("超龄工伤.html",
     "退休返聘摔成伤残，公司赔了23万",
     "超龄劳动者工伤待遇与商业保险兜底方案，完整工具表见 GitHub hr-toolkit。"),
    ("竞业天价索赔.html",
     "离职被索赔180万：“不签别入职”",
     "竞业限制天价索赔案例与签约红线，完整工具表见 GitHub hr-toolkit。"),
    ("竞业范围过宽.html",
     "离职前签了张清单，跳槽赔了100万",
     "竞业限制范围过宽认定与合规边界，完整工具表见 GitHub hr-toolkit。"),
    ("职场性骚扰.html",
     "女员工被发“想你了”，公司赔了38万",
     "职场性骚扰防治的企业责任与投诉处理流程，完整工具表见 GitHub hr-toolkit。"),
    ("试用期违法解除.html",
     "试用期说开就开？公司赔了6个月工资",
     "试用期合法解除与录用条件确认书，完整工具表见 GitHub hr-toolkit。"),
    ("规章制度公示.html",
     "发了800封邮件，仲裁却判“没公示”",
     "规章制度合法性与民主公示留痕，完整工具表见 GitHub hr-toolkit。"),
    ("违纪解除.html",
     "偷拿200块被开除，反而赔了8万",
     "违纪行为分级与解除证据链，完整工具表见 GitHub hr-toolkit。"),
    ("协商解除谈判.html",
     "“给你N+1明天走”：员工为何要2N",
     "协商解除补偿测算与谈判话术，完整工具表见 GitHub hr-toolkit。"),
    ("用工合规自查.html",
     "社保稽查上门前，公司连夜改了7处",
     "用工合规七大维度自查清单，完整工具表见 GitHub hr-toolkit。"),
]

ok = fail = 0
for html, title, digest in ARTICLES:
    path = os.path.join(BASE, html)
    if not os.path.exists(path):
        print("[SKIP] 缺少文件:", html)
        fail += 1
        continue
    safe_title = _safe_title(title)
    env = dict(os.environ, WX_APPID=APPID, WX_APPSECRET=APPSECRET)
    r = subprocess.run(
        [sys.executable, os.path.join(BASE, "push_to_mp.py"), path, safe_title, digest],
        env=env, capture_output=True, text=True, encoding="utf-8",
    )
    if r.returncode == 0 and ("[OK]" in r.stdout or "media_id" in r.stdout):
        print("[OK]   %s" % safe_title)
        ok += 1
    else:
        print("[FAIL] %s" % safe_title)
        print(r.stdout)
        print(r.stderr)
        fail += 1

print("\n完成：成功 %d 篇，失败 %d 篇（仅入草稿箱，不群发）。" % (ok, fail))
