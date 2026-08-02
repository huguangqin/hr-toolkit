# -*- coding: utf-8 -*-
"""
批量推送「企业文化与敬业度」12 篇方法论文章到公众号草稿箱。

用法：
    WX_APPID=xxx WX_APPSECRET=yyy python push_wh.py

- 复用 push_to_mp.py（按标题幂等、不群发、封面按 html 词干精准匹配）。
- 每篇标题已压到 <=64 字符（微信草稿标题上限），含悬念。
- 仅入草稿箱，不群发；群发需大勤后台确认。
- 凭据仅走环境变量，不落库。
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PUSH = os.path.join(HERE, "push_to_mp.py")

# (html 文件, 草稿标题, 摘要)
ARTICLES = [
    ("文化价值观提炼表.html",
     "价值观写满墙却没人信？这张表，把口号炼成行为",
     "3至5条，每条配行为红线"),
    ("员工敬业度问卷.html",
     "团队状态靠猜？这张问卷，把敬业度量出来",
     "匿名+维度，测完必改"),
    ("文化行为准则对照表.html",
     "价值观怎么考？这张表，把文化写成行为分",
     "正面行为+禁区，挂钩考核"),
    ("新员工文化融入表.html",
     "新人只学业务不懂文化？这张表，90天种进去",
     "30讲60带90评，认同早生"),
    ("文化故事收集表.html",
     "文化靠喊没用？这张表，用真事替你说话",
     "真实故事，比口号有力"),
    ("仪式感活动设计表.html",
     "活动办了像没办？这张表，把仪式办进心里",
     "小成本大感知，人人参与"),
    ("内部沟通渠道矩阵.html",
     "消息传着传着就变味？这张表，把渠道理顺",
     "上中下三向，各有频率"),
    ("员工认可计划表.html",
     "年终才夸人，早凉了？这张表，把认可做日常",
     "及时具体公开，小额高频"),
    ("组织氛围诊断表.html",
     "敬业度还行氛围却差？这张表，把病灶照出来",
     "信任公平协作压力，四维画像"),
    ("离职雇主品牌表.html",
     "人走了就成对手？这张表，把离职变校友",
     "访谈+校友群，回流有门"),
    ("多元包容推行表.html",
     "DEI只是喊口号？这张表，把包容做进机制",
     "多元+包容，目标可测"),
    ("文化价值观考核表.html",
     "业绩好就能任性？这张表，把文化钉进考核",
     "权重+否决，价值观硬约束"),
]


def main():
    if not os.environ.get("WX_APPSECRET"):
        print("[错误] 未检测到 WX_APPSECRET 环境变量，请通过环境变量临时传入后重试。")
        sys.exit(1)
    ok = 0
    for html, title, digest in ARTICLES:
        path = os.path.join(HERE, html)
        if not os.path.exists(path):
            print(f"[跳过] 文件不存在: {html}")
            continue
        cmd = [sys.executable, PUSH, path, title, digest]
        print(f"\n=== 推送: {title} ===")
        r = subprocess.run(cmd)
        if r.returncode == 0:
            ok += 1
        else:
            print(f"[失败] {title} (returncode={r.returncode})")
    print(f"\n完成：成功 {ok}/{len(ARTICLES)} 篇。仅入草稿箱，不群发。")


if __name__ == "__main__":
    main()
