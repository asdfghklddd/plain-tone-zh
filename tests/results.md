# 测试结果（2026-10-16，tone_check.py v1.0）

全部样稿均为本方案**自拟的 SYNTHETIC 样本**，改写稿中的数字也是虚构的，只用于演示规则效果，不是真实数据。改写由本方案作者按 SKILL.md 手工完成，**不是 GPT/Grok 实测输出**。

## 改写前后

| 样稿 | 类型 | 改前 判定/加权分/hard/soft | 改后 判定/加权分/hard/soft |
|---|---|---|---|
| 01-ppt-quarterly.md | PPT | FAIL / 28 / 9 / 5 | PASS / 0 / 0 / 0 |
| 02-ppt-ai-strategy.md | PPT | FAIL / 24 / 9 / 2 | PASS / 0 / 0 / 0 |
| 03-ppt-product.md | PPT | FAIL / 13 / 4 / 3 | PASS / 0 / 0 / 0 |
| 04-doc-market.md | 文档 | FAIL / 17 / 6 / 1 | PASS / 0 / 0 / 0 |
| 05-doc-report.md | 文档 | FAIL / 23 / 8 / 3 | PASS / 0 / 0 / 0 |
| 06-doc-en.md | 文档 | FAIL / 13 / 4 / 3 | PASS / 0 / 0 / 0 |
| 07-ppt-training.md | PPT | FAIL / 20 / 8 / 0 | PASS / 1 / 0 / 1 |
| **合计** | | hard 48，soft 17，7/7 FAIL | hard 0，soft 1，7/7 PASS |

改前各类命中（合计）：
contrast 10, meta 9, buzzword 9, empty_title 8, disclaimer 8, ending 8, hedge_stack 7, concessive 4, contrast_soft 1, chat 1

改后剩余 1 处 soft：after/07 标题“周会发言先说结论”命中“先说结论”（meta soft）。这是合法用法（培训内容本身就是教人先说结论）。初版脚本把它列为 hard 导致误判 FAIL，已降为 soft，这是本轮测试中发现并修正的一个误报。

## 误报测试

`false_positive.md`：5 句正常使用“不是/但/虽然”的句子 → **PASS，0 hard，0 soft**。

`false_positive_stress.md`：3 句更容易误报的合法句 → **PASS，0 hard，2 soft**（“虽然样本只有 68 条，但…”命中 concessive；“这不是 bug，是配置写错了”命中 contrast_soft）。soft 只提示不判 FAIL，这正是把它们设为 soft 的原因；但如果一页里有 2 处以上合法的“虽然…但”，会因让步阈值被判 FAIL，需人工放行。

## 已知漏检（脚本抓不到）
- 换了说法的翻案（如“真正决定成败的，是…”这种无‘不是’的抬价句）。
- 强凑三项排比（before/03 的“创新、突破和全新的可能”未命中）。
- 编造的数字/事实——脚本无法判断真假，只能靠编辑遍的对照核查。

复现：`python3 tone_check.py tests/before/*.md tests/after/*.md tests/false_positive*.md`，或 `python3 tests/run_tests.py`。逐条命中见 `results.json`。

---

# v4 回归测试（2026-10-16，tone_check.py v4）

新增检测：`this_not`（这是X，不是Y / this is X, not Y）、`further_check`（仍需进一步测试/验证/复盘/研究）、`verify_list`（验证清单/未验证项/待补/风险提示/免责 区块标题，【待补】标记）。均为 hard。

| 文件 | 判定 | hard / soft |
|---|---|---|
| before/01–07（原有坏样稿） | 7/7 FAIL | hard 合计 48（与 v3 相同，无回归） |
| after/01–07（原有改写稿） | 7/7 PASS | hard 0，soft 1（after/07“先说结论”，同前） |
| before/08-ppt-v4-patterns.md（新，自拟） | FAIL | hard 6：this_not 2、further_check 2、verify_list 2；soft 1 |
| after/08-ppt-v4-patterns.md（新，自拟） | PASS | 0 / 0 |
| false_positive.md | PASS | 0 / 0 |
| false_positive_stress.md | PASS | 0 / 2（同前） |
| false_positive_v4.md（新：6 句含“这是/不是/还需要…测试/验证/风险提示/It is”的正常句） | PASS | 0 / 1（“不是我说的，是财务部…”命中 contrast_soft，只提示） |

合计：8 份坏样稿全部 FAIL（hard 54），8 份改写稿全部 PASS（hard 0），3 组误报测试全部 PASS（hard 0）。

v4 已知漏检：`anti-examples.md` 里大部分条目（没人问的反驳、同意后加“但有一点”、HR 腔、刻意短句、结尾追问）脚本抓不到，靠交稿前逐条对照。新样稿仍是自拟，不是 GPT/Grok 输出。
