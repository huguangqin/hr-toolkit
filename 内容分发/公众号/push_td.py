# -*- coding: utf-8 -*-
"""
批量推送「培训与人才发展 TD」12 篇方法论文章到公众号草稿箱。

用法：
    WX_APPID=xxx WX_APPSECRET=yyy python push_td.py

- 复用 push_to_mp.py（按标题幂等、不群发、封面按 html 词干精准匹配）。
- 每篇标题已压到 <=64 字节（微信草稿标题上限），含悬念。
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
    ("培训需求分析.html",
     "培训花50万却没用：这张表先问该不该培训",
     "Goldstein 三层次需求分析，先问该不该培训"),
    ("年度培训计划.html",
     "排30门课只上8门：年度计划表，治计划荒",
     "产能对齐+刚性优先，做出能落地的年度计划"),
    ("课程设计画布.html",
     "请名师讲2小时学员刷手机：这张画布，把听变会",
     "ADDIE+ABCD 法，把听变成会"),
    ("内训师认证.html",
     "业务大牛上讲台卡壳：认证表选出真能讲的人",
     "三关认证+三级课酬，选出真能讲的内训师"),
    ("导师制.html",
     "新人导师签了约就消失：这张表，把放养变带教",
     "签约契约+四块内容地图，把放养变带教"),
    ("IDP个人发展.html",
     "骨干要离职说学不到东西：IDP把成长写进计划",
     "70-20-10 法则，把成长写进计划"),
    ("培训效果评估.html",
     "满意度4.8老板问有用吗：柯氏表，用数据说话",
     "柯氏四级+ROI，用数据回答老板的然后呢"),
    ("新员工onboarding.html",
     "新人没人管就走？onboarding这张表，30天留人",
     "30-60-90 天+Buddy，前30天接住新人"),
    ("人才盘点九宫格.html",
     "核心岗离职公司懵了：九宫格表，把雷提前标",
     "绩效×潜力九宫格+校准会，把雷提前标"),
    ("继任计划.html",
     "总监休假业务停摆：继任表让关键岗不只有他",
     " readiness 分级+红灯预警，关键岗不只有他"),
    ("供应商评估.html",
     "花8万买的课学员说水：供应商表，钱花在刀刃上",
     "五维加权+红线核查，钱花在刀刃上"),
    ("培训预算ROI.html",
     "预算年年涨老板问值不值：ROI表，算清这笔账",
     "含工时机会成本的 ROI 测算，算清这笔账"),
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
