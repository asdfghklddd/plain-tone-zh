#!/usr/bin/env python3
"""tone_check.py v4 — 合并版文风检查器（只用标准库）。
v4 新增：这是X不是Y / this is X, not Y、仍需进一步测试/验证/复盘、验证清单/未验证项/待补 区块（来自 anti-examples.md）。

检测：翻案/对比模板、让步转折、限定词堆叠、免责/保险条款、元叙述（"我不会…"）、
黑话/AI 高频词、空泛 PPT 标题、拔高结尾、聊天残留。
输出：逐行命中 + 分类计数 + 加权分 + PASS/FAIL。退出码 0=PASS, 1=FAIL。

正则来源（改写合并，非逐字复制）：
  human-writing scripts/check_prose.py（翻案句与变形）  MIT © Human Writing Skill contributors
  oil-tone scripts/tone_lint.py（套话、模糊归因、乐观结尾、重复限定）  MIT © oil-oil
  Humanizer-zh SKILL.md 第 1/5/9/23/31 条（分类思路）  MIT © 歸藏
  OpenAI GPT-6 Astra 提示指南·写作风格段（英文 slop 词、"X, not Y"、"what you won't do"）
  其余（PPT 标题、免责词表、阈值、权重）为本方案自拟。

用法：
  python3 tone_check.py file.md [file2 ...]
  cat draft.txt | python3 tone_check.py -
  python3 tone_check.py file.md --json        # 机器可读
  python3 tone_check.py file.md --max-score 6 # 调整阈值
"""
import re, sys, json, argparse

S = r"[^。！？!?\n]"  # 句内字符
# (类别, 严重度 hard/soft, 权重, 正则, 建议)
RULES = [
 # ---- 1. 翻案/对比模板（hard）----
 ("contrast","hard",3, rf"(?:并)?不是{S}{{0,60}}?而是", "删掉假想的 X，直接说 Y，把依据放旁边"),
 ("contrast","hard",3, rf"并非{S}{{0,60}}?而是", "同上"),
 ("contrast","hard",3, rf"不在于{S}{{0,60}}?而在于", "直接说关键是什么"),
 ("contrast","hard",3, rf"与其说{S}{{0,60}}?(?:不如|倒不如|毋宁)", "直接给判断"),
 ("contrast","hard",3, rf"(?:你|很多人|大家|我们)?(?:总|一直|都)?以为[^！？\n]{{2,50}}?(?:其实|实际上|事实上|才发现|才明白)", "读者没有这个误解就别替他立"),
 ("contrast","hard",3, rf"(?:表面上?|看似|看起来){S}{{0,40}}?(?:其实|实际上|实则|本质上)", "直接说实际情况"),
 ("contrast","hard",3, rf"{S}{{1,20}}不重要，重要的是", "直接说重要的是什么"),
 ("contrast","hard",3, r"(?i)\b(?:it'?s|this is|that'?s|this isn'?t|it isn'?t)\s+(?:not\s+)?(?:just\s+|only\s+|about\s+)?[^.\n]{1,50}?[.,;—–-]\s*(?:it'?s|this is)\s+(?:about\s+)?", "State Y directly"),
 ("contrast","hard",3, r"(?i)\bnot\s+(?:just|only|merely)\s+[^.\n]{1,40}?,?\s+but\s+(?:also\s+)?", "State the point directly"),
 # ---- 2. 对比模板软命中（soft，常有合法用法）----
 ("contrast_soft","soft",1, rf"(?:并)?不是{S}{{1,30}}，(?:更|才)?是", "确认否定部分是否纠正了真实误解"),
 ("contrast_soft","soft",1, rf"不(?:仅|只)(?:仅)?{S}{{1,30}}(?:更|还|也)是", "两部分都有信息才保留"),
 ("contrast_soft","soft",1, r"恰恰相反|答案是否定的|回头(?:看|一看)?才(?:发现|明白)", "确认反转是否真实存在"),
 # ---- 3. 让步转折（soft，堆叠时加罚）----
 ("concessive","soft",1, rf"(?:虽然|虽说|尽管|固然){S}{{0,40}}?(?:但|但是|却|仍|依然|不过)", "先给结论；限制只写一次并具体化"),
 ("concessive","soft",1, r"(?i)\b(?:while|although|though)\b[^.\n]{3,60},", "Lead with the claim"),
 # ---- 4. 限定词堆叠（hard）----
 ("hedge_stack","hard",2, r"(?:可能|或许|也许|大概|似乎|在一定程度上|某种程度上)[^。！？\n]{0,8}(?:可能|或许|也许|大概|似乎|在一定程度上|某种程度上)", "同一层不确定只留一个词"),
 ("hedge_stack","hard",2, r"在(?:一定|某种)程度上", "写出程度（数字/范围）或删除"),
 ("hedge_stack","hard",2, r"(?i)\b(?:could|might|may)\s+(?:potentially|possibly|perhaps)\b|\bpotentially\s+(?:could|might)\b", "One hedge max"),
 # ---- 5. 免责/保险条款（hard）----
 ("disclaimer","hard",3, r"仅供参考|不构成(?:任何)?[^。\n]{0,8}建议|(?:具体|一切)?以实际(?:情况)?为准|因人而异|请(?:务必)?谨慎(?:决策|判断|对待|操作)?|风险自(?:担|负)|(?:请)?(?:咨询|寻求)专业(?:人士|意见|机构)|需(?:要)?结合(?:自身|实际|具体)(?:情况)?|具体情况具体分析|(?:我们|本文|以上内容)?(?:无法|不能)(?:保证|确保)[^。\n]{0,10}(?:准确|完整|有效)|作为(?:一个)?(?:AI|人工智能)|截至我的(?:知识|训练)", "删除；真实的不确定写一次、贴着数字、说清缺什么"),
 ("disclaimer","hard",3, r"(?i)not (?:financial|legal|investment|medical) advice|consult (?:a|your) (?:professional|advisor)|as of my (?:last|knowledge)|i (?:cannot|can'?t) guarantee|for (?:informational|reference) purposes only", "Delete; state real uncertainty once, next to the number"),
 ("disclaimer","soft",1, r"需(?:要)?进一步(?:评估|研究|观察|论证)|有待(?:进一步)?(?:观察|验证)|仍(?:存在|有)(?:一定的?)?不确定性", "写清缺哪项数据、何时补"),
 # ---- 6. 元叙述 / 说自己不做什么（hard）----
 ("meta","hard",2, r"(?:本文|这里|以下|此处)(?:不|并不)(?:讨论|涉及|展开)|我(?:不会|不打算|并不是要)|不要误会|需要(?:特别)?(?:指出|说明|强调)的是|值得(?:注意|一提|关注)的是|让我们(?:一起)?(?:深入|来看|看看)|接下来(?:让我们|我们来)|说白了|总而言之|综上所述", "删掉预告和自我辩护，直接写内容"),
 ("meta","hard",2, r"(?i)\b(?:it'?s worth noting|importantly|in short:|bottom line:|let'?s dive|delve into|to be clear,|i won'?t)\b", "Delete the frame"),
 ("meta","soft",1, r"先说结论|随着[^。\n]{0,16}(?:不断|持续)?的?(?:发展|演变|推进)|进行了?(?:系统性的?|全面的?|深入的?)?(?:优化|调整|分析|研究|探讨|升级)", "直接写结论/动作；'进行+动词'还原成动词"),
 # ---- 7. 黑话 / AI 高频词（soft）----
 ("buzzword","soft",1, r"赋能|抓手|闭环|底层逻辑|颗粒度|打通|组合拳|全方位|多维度|全链路|深度融合|助力|重塑|破局|生态化|一站式|新范式|降维打击|毋庸置疑|不可否认|至关重要|不言而喻|无缝|极致", "换成具体动作或结果"),
 ("buzzword","soft",1, r"(?i)\b(?:leverage|delve|foster|genuinely|seamless(?:ly)?|robust|holistic|synergy|game[- ]changer|unlock(?:s|ing)? the)\b", "Use a plain verb"),
 # ---- 8. 拔高结尾（hard）----
 ("ending","hard",3, r"未来可期|开启(?:了)?(?:全新|新的?)篇章|迈出(?:了)?(?:至关重要|重要|关键|坚实)的一步|让我们携手|携手(?:共进|共创|并进)|共创(?:美好)?未来|赢得未来|无限(?:可能|潜力)|值得(?:我们)?(?:期待|深思)|为[^。\n]{1,20}奠定(?:了)?(?:坚实的?)?基础|(?:彰显|凸显)(?:了)?[^。\n]{0,16}(?:意义|价值|重要性)|(?:标志着|代表着)[^。\n]{0,20}(?:重要|关键)(?:一步|时刻|转折)", "删掉；以最后一个具体结果或下一步收尾"),
 # ---- 10. 页脚保险句 / 防御性从句（v2，来自 Grok 实测稿）----
 ("caveat","soft",1, r"待(?:实测|验证|确认|核实|评估)|(?:效果|结果|数据)?(?:尚)?未经?(?:验证|实测)|不等于[^。\n]{0,12}(?:效果|结论|表现)|非现价|仅为(?:概念|示意)|(?:图片|图像)?为(?:AI)?(?:概念|示意)(?:图|渲染)", "同一份稿子只在一处集中写清缺什么证据，别每页贴一句"),
 ("guard","soft",1, r"[；;，,]\s*避免[^。\n]{2,20}", "防御性从句：若是真实设计约束，改成正面规格（如'旋钮优先于自动'）"),
 # ---- 11. v4：用户反面案例库新增（hard）----
 ("this_not","hard",3, r"这(?:就)?是[^，,。！？\n]{1,30}[，,]\s*(?:而)?(?:不是|并非|而非)[^。！？\n]{1,30}", "“这是X，不是Y”：直接说X，删掉没人提过的Y（AE-02/AE-03）"),
 ("this_not","hard",3, r"(?i)\b(?:this|that|it)\s+is\s+(?:a\s+|an\s+)?[^,.;\n]{1,40},\s*not\s+(?:a\s+|an\s+|just\s+)?\w+", "'this is X, not Y': state X only"),
 ("further_check","hard",3, r"(?:仍|还|尚)(?:然)?(?:需要?|有待)(?:进一步|继续|持续)?(?:的)?(?:测试|验证|复盘|研究|观察|评估|核实)", "删掉“仍需进一步测试/验证/复盘”式结尾，停在最后一个具体结果（AE-19）"),
 ("further_check","hard",3, r"(?i)\b(?:further|more)\s+(?:testing|validation|research|investigation)\s+(?:is|are|will be)\s+(?:needed|required)", "Delete; end on the last concrete result"),
 ("verify_list","hard",3, r"【待(?:补|验证|确认)】|\[待补\]", "删掉“待补/待验证”标记；缺材料就不写（AE-20）"),
 # ---- 9. 聊天残留（hard）----
 ("chat","hard",2, r"希望(?:这|以上)?(?:对你|对您|能)(?:有所)?帮助|当然可以|这是一个(?:非常|很)?好的问题|如(?:需|有)(?:更多|任何)(?:信息|帮助|问题)|(?:欢迎|随时)(?:告诉我|联系)", "删除"),
]
# PPT 空泛标题：只对"标题行"检测（# 开头，或 ≤22 字且无句号）
TITLE_RULES = [
 (r"[：:][^，,。]{1,12}[，,](?:但|却|更)", "冒号+转折式口号标题，改成结论句"),
 (r"(?:赋能|驱动|引领|新篇章|新范式|新征程|新时代|全面升级|破局|重塑|蝶变|再出发|再启航|向未来|行稳致远)", "口号词标题，改成'对象+动作/判断+数字'"),
 (r"^(?:#+\s*)?(?:关于)?[^，。]{0,10}(?:的思考|的探索|的实践|之道|之路)$", "空泛标题，写出具体判断"),
 (r"^(?:#+\s*)?(?:背景|概述|总结|展望|小结|结语|未来展望|核心价值|主要内容|Overview|Summary|Conclusion|Next Steps|Key Takeaways)\s*$", "目录式标题，改成本页结论"),
 (r"^(?:#+\s*)?\S{2,4}[·|｜/]\S{2,4}[·|｜/]\S{2,4}\s*$", "四字词排比标题，改成结论句"),
]

def is_title(line):
    s = line.strip()
    if not s: return False
    if re.match(r"^#{1,6}\s", s): return True
    if re.match(r"^(?:标题|Title|Slide\s*\d+|第\s*\d+\s*页)\s*[:：]", s, re.I): return True
    body = re.sub(r"^[-*\d.\s]+", "", s)
    return len(body) <= 22 and not re.search(r"[。！？.!?]$", body) and not s.startswith(("-", "*", "•"))

def strip_code(text):
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)

def check(text, max_score=6.0, max_concessive=1):
    text = strip_code(text)
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(">"):  # 引用原文不检
            continue
        for cat, sev, w, pat, tip in RULES:
            for m in re.finditer(pat, line):
                hits.append(dict(line=n, cat=cat, sev=sev, w=w, text=m.group(0)[:50], tip=tip))
        if re.match(r"^\s*(?:#+\s*|[-*•]\s*|\d+[.、]\s*)?(?:附[:：]?\s*)?(?:验证清单|未验证(?:项|事项|清单)?|待验证(?:项|事项|清单)?|待补(?:充)?(?:项|事项|清单|信息)?|风险提示|局限(?:说明|性)?|免责(?:声明|说明)?)\s*[:：]?\s*$", line):
            hits.append(dict(line=n, cat="verify_list", sev="hard", w=3, text=line.strip()[:50], tip="未经要求的验证清单/待补/风险提示/免责区块：整块删除（AE-20；用户要求或风控报告除外）"))
        if is_title(line):
            t = re.sub(r"^(?:标题|Title|Slide\s*\d+|第\s*\d+\s*页)\s*[:：]\s*", "", line.strip(), flags=re.I)
            for pat, tip in TITLE_RULES:
                if re.search(pat, t):
                    hits.append(dict(line=n, cat="empty_title", sev="hard", w=2, text=t[:50], tip=tip)); break
    counts = {}
    for h in hits: counts[h["cat"]] = counts.get(h["cat"], 0) + 1
    chars = max(len(re.sub(r"\s", "", text)), 1)
    score = sum(h["w"] for h in hits)
    per1k = round(score * 1000 / chars, 1)
    hard = sum(1 for h in hits if h["sev"] == "hard")
    reasons = []
    if hard: reasons.append(f"{hard} 处 hard 命中（翻案/这是X不是Y/免责/仍需进一步验证/验证清单/堆叠限定/元叙述/拔高结尾/空标题/聊天残留，任一即 FAIL）")
    if counts.get("concessive", 0) > max_concessive: reasons.append(f"让步转折 {counts['concessive']} 处 > {max_concessive}")
    if counts.get("caveat", 0) >= 3: reasons.append(f"保险句 {counts['caveat']} 处 ≥3（每页一句免责=保险条款，集中到一处）")
    if counts.get("guard", 0) >= 3: reasons.append(f"防御性'避免…'从句 {counts['guard']} 处 ≥3")
    if score > max_score and per1k > 15: reasons.append(f"加权分 {score} > {max_score} 且密度 {per1k}/千字 > 15")
    return dict(chars=chars, score=score, per1k=per1k, counts=counts, hard=hard,
                soft=len(hits) - hard, verdict="FAIL" if reasons else "PASS", reasons=reasons, hits=hits)

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-score", type=float, default=6.0); ap.add_argument("--max-concessive", type=int, default=1)
    a = ap.parse_args(); bad = False; out = {}
    for f in a.files:
        text = sys.stdin.read() if f == "-" else open(f, encoding="utf-8").read()
        r = check(text, a.max_score, a.max_concessive); out[f] = r; bad |= r["verdict"] == "FAIL"
        if a.json: continue
        for h in r["hits"]:
            print(f"{f}:{h['line']}: [{h['sev'].upper()}:{h['cat']}] 「{h['text']}」 → {h['tip']}")
        print(f"== {f}: {r['verdict']} | 分 {r['score']} ({r['per1k']}/千字) | hard {r['hard']} soft {r['soft']} | {r['counts']}")
        for x in r["reasons"]: print("   原因:", x)
        if r["verdict"] == "FAIL":
            print("   → 把上面的行号和建议交给 editor-pass-prompt.md 的第二遍改稿，改完再跑本脚本，直到 PASS（最多 3 轮）。")
    if a.json: print(json.dumps(out, ensure_ascii=False, indent=1))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
