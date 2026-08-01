#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量推送 12 篇薪酬方法论文章到公众号草稿箱（仅草稿、不群发）。

用法（凭据仅用环境变量临时传入，不落库）：
  WX_APPID=wx6d1b9918671b7f70 WX_APPSECRET=xxxxxxxx python push_salary.py

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
    ("岗位价值评估.html",
     "岗位价值评估：两岗工资差3千老板说不清",
     "岗位价值评估点因素法，让定薪第一次有依据，完整工具表见 GitHub hr-toolkit。"),
    ("薪酬调研对标.html",
     "薪酬调研对标：说有竞争力一查在30分位裸泳",
     "薪酬分位对标方法论，诊断真实竞争力，完整工具表见 GitHub hr-toolkit。"),
    ("薪酬结构设计.html",
     "薪酬结构设计：销售底薪4千研发2万同薪不同命",
     "固浮比设计方法论，同样的钱花对结构，完整工具表见 GitHub hr-toolkit。"),
    ("宽带薪酬矩阵.html",
     "宽带薪酬矩阵：同岗差一倍，被举报同工不同酬",
     "带宽/级差/重叠度算法，宽带薪酬不翻车，完整工具表见 GitHub hr-toolkit。"),
    ("年度调薪矩阵.html",
     "年度调薪矩阵：绩效A涨3%C涨8%好员工跑了",
     "CR值+绩效矩阵调薪，避免倒挂流失，完整工具表见 GitHub hr-toolkit。"),
    ("销售提成方案.html",
     "销售提成方案：销冠离职撂话'提成是骗人的'",
     "提成基数/累进/封顶/扣回设计，完整工具表见 GitHub hr-toolkit。"),
    ("年终奖个税筹划.html",
     "年终奖个税筹划：年终奖多发1块到手少2300",
     "个税盲区临界与两种算法对比，完整工具表见 GitHub hr-toolkit。"),
    ("股权激励框架.html",
     "股权激励框架：发了期权他反而跑了归属陷阱",
     "期权/RSU/归属cliff设计，完整工具表见 GitHub hr-toolkit。"),
    ("社保公积金自查.html",
     "社保公积金自查：按最低基数交社保省20万赔80万",
     "缴费基数合规自查清单，完整工具表见 GitHub hr-toolkit。"),
    ("薪酬沟通话术.html",
     "薪酬沟通话术：员工问涨得少，HR一句话谈离职",
     "涨薪谈判四步话术，完整工具表见 GitHub hr-toolkit。"),
    ("人效分析表.html",
     "人效分析表：工资涨20%利润反跌人效表一看就懂",
     "薪酬ROI与人效诊断，完整工具表见 GitHub hr-toolkit。"),
    ("新员工定薪表.html",
     "新员工定薪表：开18k被拒16k接了定薪的算法",
     "offer测算与防倒挂，完整工具表见 GitHub hr-toolkit。"),
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
