# -*- coding: utf-8 -*-
"""
批量推送「入离职与社保」12 篇方法论文章到公众号草稿箱。

用法：
    WX_APPID=xxx WX_APPSECRET=yyy python push_ru.py

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
    ("入职手续办理清单.html",
     "新人报到当天手忙脚乱？这张清单，一次办齐",
     "合同/社保/系统一日闭环，避开双倍工资"),
    ("员工信息登记表.html",
     "一张表填错，个税社保全乱？信息登记，从源头防错",
     "敏感信息加密建档，避免合规事故"),
    ("社保新参统增员表.html",
     "社保增员晚一天，公司多笔钱？这张表，锁定30日红线",
     "属地+基数+险种，三步不踩雷"),
    ("公积金开户增员表.html",
     "公积金比例随便定？这张表，把5%到12%定准",
     "基数比例合规，员工贷款不卡壳"),
    ("社保基数核定表.html",
     "基数年年按最低？这张表，把工资算全",
     "应发全口径，上下限不越线"),
    ("离职交接清单.html",
     "人走了客户也走了？这张清单，把交接锁死",
     "工作资产权限，三向签字闭环"),
    ("离职证明与社保减员表.html",
     "离职证明写错一句，员工能索赔？这张表，合规出证明",
     "减员转移不卡壳，员工再就业"),
    ("竞业限制管理表.html",
     "竞业签了却没用？这张表，把补偿和效力锁住",
     "范围期限补偿，三要素定生死"),
    ("保密与知识产权确认表.html",
     "代码专利归谁说不清？这张表，把IP钉死",
     "职务成果归公，泄密能追责"),
    ("劳务派遣外包合规表.html",
     "外包派遣分不清，公司背锅？这张表，画清边界",
     "三性+10%，假外包现形"),
    ("灵活用工合规表.html",
     "实习生当正式工用，公司赔了？这张表，把关系定对",
     "退休兼职众包，四类各归各"),
    ("社保税务稽核自查表.html",
     "稽核上门才补？这张表，平时就把雷排了",
     "人数基数险种，三对账自查"),
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
