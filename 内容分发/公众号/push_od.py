# -*- coding: utf-8 -*-
"""
批量推送「组织发展 OD」12 篇方法论文章到公众号草稿箱。

用法：
    WX_APPID=xxx WX_APPSECRET=yyy python push_od.py

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
    ("组织架构设计画布.html",
     "部门越拆越乱：这张画布，定清谁拍板",
     "钱德勒结构跟随战略，用画布定架构与汇报"),
    ("部门职责说明书模板.html",
     "三部门都管都不管：职责书，终结扯皮",
     "权责对等+RACI，把边界写进可签字的说明书"),
    ("岗位说明书JD模板.html",
     "招来总货不对板：JD模板，把要什么写清",
     "KSAO 分级，把岗位要求写可验证"),
    ("胜任力模型构建表.html",
     "同岗有人封神有人垮：胜任力词典，画差距",
     "McClelland 冰山模型，把能力显性化"),
    ("职级体系双通道表.html",
     "技术大牛只能当官：双通道，让专家不必转管理",
     "M/P 双序列同级同薪，留住核心专家"),
    ("晋升评估答辩表.html",
     "晋升全凭老板印象：答辩表，把标准摊开",
     "BARS 行为锚定，晋升透明可说服"),
    ("组织诊断7S表.html",
     "没犯规却走不动：7S表，照出隐形病灶",
     "麦肯锡7S，软硬对齐照出组织错位"),
    ("管控模式选择表.html",
     "一管就死一放就乱：管控表，拿捏分寸",
     "财务/战略/运营三型，按成熟度选"),
    ("跨部门RACI矩阵.html",
     "开会都到没人拍板：RACI，把责落给人",
     "唯一A负责制，终结集体负责=没人负责"),
    ("组织变革管理表.html",
     "新制度推行必遇阻：变革表，先安人再改事",
     "变革曲线+ADKAR，先安人再改事"),
    ("组织效能看板.html",
     "人越多效率越低：效能看板，数字揭穿",
     "管理幅度+人效，用指标量化组织效率"),
    ("授权审批矩阵.html",
     "什么都等老板签：授权表，把权分下去",
     "授权分级+红线，把权分下去留红线"),
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
