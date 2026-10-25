# plain-tone-zh

中文 | [English](README.en.md)

一套给 ChatGPT、Grok、Claude、Codex 用的中文写作规则，加一个检查脚本。用来去掉 AI 写 PPT 和文档时最常见的三类毛病：

1. 保险条款式的限定和免责句，比如下面这些：
   > 仅供参考、以实际为准、在一定程度上可能、仍需进一步验证
2. 翻案和让步模板，比如下面这些：
   > 不是A而是B、你以为A其实B、虽然A但B、这是X不是Y
3. 空泛的 PPT 标题和拔高结尾，比如下面这些：
   > 背景、总结与展望、未来可期、迈出关键一步

规则按行为写，不只给禁用词表。模型换个说法照样会写翻案句，所以 skill 禁的是“先立一个读者没有的误解再推翻”这个动作，词表只当例子。

## 文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` / `SKILL.en.md` | 完整 skill（层 1–4），带 frontmatter，给 Codex、Claude Code 和其他 agent 用 |
| `custom-instructions-compact.md` / `.en.md` | 精简版规则，中文 805 字、英文 1427 字符，可直接贴进 ChatGPT 或 Grok 的自定义指令（上限 1500） |
| `editor-pass-prompt.md` / `.en.md` | 第二遍改稿提示词（层 3） |
| `anti-examples.md` / `.en.md` | 28 条反面案例，每条带一个检查问题，交稿前逐条对照 |
| `tone_check.py` | 检查脚本，只用 Python 标准库，输出逐行命中、加权分和 PASS/FAIL（层 4） |
| `tests/` | 8 份坏样稿、8 份改写稿、3 组误报测试，结果在 `tests/results.md` |

## 四层结构

1. **层 1 写作规则**：先结论后依据，每句带新信息，主干先行；加上三类毛病的行为级禁令。生成时生效。
2. **层 2 PPT 规则**：每页一个观点，标题写成带数字的结论句，每页最多 4 条，最后一页写下一步。
3. **层 3 编辑遍**：另开一轮，只改有问题的句子，逐句对照原文，查有没有新增或丢掉信息。生成可以重组结构，编辑必须保真，所以两遍分开做。
4. **层 4 检查与打回**：`tone_check.py` 判 FAIL 后，把命中行交给层 3 重改，最多 3 轮。最后对照 `anti-examples.md` 逐条过一遍。

## 快速开始

- **ChatGPT**：设置 → 个性化 → 自定义指令，把 `custom-instructions-compact.md` 全文贴进“你希望 ChatGPT 如何回复”。做 PPT 时先给它“每页一句结论 + 证据”的大纲表。成稿后新开一个对话，用 `editor-pass-prompt.md` 跑第二遍。
- **Grok**：设置 → 自定义（Customize），贴同一段精简版。第二遍改稿建议交给另一个模型做。
- **Claude Code**：把整个目录放到 `~/.claude/skills/plain-tone-zh/`，`SKILL.md` 和 `tone_check.py` 要在同一目录。
- **Codex**：同上，放到 `~/.codex/skills/plain-tone-zh/`。
- **API**：system 用 `SKILL.md` 正文（去掉 frontmatter）。生成后调用 `tone_check.check(text)`，结果是 FAIL 就把 `editor-pass-prompt.md` 和命中行一起发一次，最多 3 轮。
- **用英文规则**：agent 只读 `SKILL.md`。要英文版，把 `SKILL.en.md` 复制成安装目录里的 `SKILL.md`。

## 检查脚本

```
python3 tone_check.py draft.md            # 逐行命中 + 判定，FAIL 时退出码为 1
python3 tone_check.py draft.md --json     # 机器可读结果
cat draft.txt | python3 tone_check.py -   # 从标准输入读
python3 tone_check.py draft.md --max-score 6 --max-concessive 1   # 调阈值
python3 tests/run_tests.py                # 跑回归测试
```

判定规则：

- **hard**，任一命中即 FAIL：翻案模板、“这是X不是Y”句式、免责句、“进一步验证”式结尾、验证清单和待补标记、限定词堆叠、元叙述、拔高结尾、空泛 PPT 标题、聊天残留。
- **soft**，只提示：短对比句、递进句、单处让步转折、黑话、“进行+动词”、空背景开头、页脚保险句、防御性“避免…”从句。
- 让步转折超过 1 处判 FAIL；加权分大于 6 且每千字大于 15 分也判 FAIL。
- 以 `>` 开头的引用行和代码块不检查。

脚本只匹配字面。换了说法的翻案、强凑的三项排比、编造的数字它都抓不到，PASS 之后还要通读。

**英文支持**：规则和提示词都有英文版。脚本以中文为主，对英文只覆盖一部分：翻案句、限定词堆叠、免责句、元叙述、黑话、进一步测试式结尾、目录式标题和 although/while 让步句。英文的拔高结尾和聊天残留目前没有检测。测试集里只有 1 对英文样稿（`06-doc-en.md`）。脚本认得的英文翻案句式如下：

> it's not X, it's Y / not just X but Y / this is X, not Y / further testing is needed

## 测试结果

数字来自 `tests/results.md`，可用 `python3 tests/run_tests.py` 复现（19/19 通过）。

| 测试 | 结果 |
|---|---|
| 8 份坏样稿（`tests/before/`） | 8/8 FAIL，hard 合计 54 |
| 8 份改写稿（`tests/after/`） | 8/8 PASS，hard 0，soft 1 |
| 3 组误报测试，14 句正常使用“不是/但/虽然/验证/风险提示”的句子 | 3/3 PASS，hard 0，soft 3 |

改写前 7 份 v1 样稿的命中分布：翻案 10、元叙述 9、黑话 9、空标题 8、免责 8、拔高结尾 8、限定堆叠 7、让步 4。改写稿剩下的 1 处 soft 是培训课件标题“周会发言先说结论”，内容本身就在教人先说结论，属于合法用法。

样稿和改写稿都是手写的，数字是虚构的，没有用 GPT 或 Grok 的实际输出。这组测试说明脚本能区分两种写法，规则在各个模型上的实际效果要靠你自己的稿子检验。

## 来源与致谢

本方案转述并合并了下面四个 MIT 许可的开源项目和 OpenAI 的一段写作建议。仓库里没有复制它们的原文，规则和正则都是改写后的版本。

| 标签 | 项目 | 作者 | 许可 |
|---|---|---|---|
| SRH | [说人话 shuorenhua](https://github.com/MrGeDiao/shuorenhua) | MrGeDiao | MIT |
| HW | [活人感写作 human-writing](https://github.com/KKKKhazix/human-writing) | Human Writing Skill contributors | MIT |
| OIL | [oil-tone](https://github.com/oil-oil/oil-tone) | oil-oil | MIT |
| HZ | [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 歸藏 | MIT |
| OAI | [OpenAI 模型提示指南·写作风格段](https://developers.openai.com/api/docs/guides/latest-model) | OpenAI | 非开源文本，只转述 |

`tone_check.py` 的正则改写自 human-writing 的 `check_prose.py` 和 oil-tone 的 `tone_lint.py`。PPT 标题规则、中文免责词表、权重和阈值是本方案自己定的。`anti-examples.md` 的条目整理自 2026 年 X 上关于 ChatGPT 和 Grok 文风的公开讨论，已去掉账号和链接，内容为转述。

### 规则来源对照

SKILL.md 每条规则后的标签对应下表。“自拟”指五个来源里都没有直接对应的部分。

| 规则 | OAI | SRH | HW | OIL | HZ | 自拟 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 先结论后依据 | ● | | ● | ● | | |
| 每句带新信息，动笔前先清点材料 | | | ● | ● | | 部分 |
| 不新增事实，缺材料就写短或不写 | | ● | ● | ● | ● | |
| 保留否定、条件、情态和责任主体 | | ● | | | ● | |
| 无源说法保留归属 | | ● | | | ● | |
| 翻案腔按行为禁止，并列出变形 | ● | | ● | ● | ● #1 | |
| 对比模板的保留条件 | | | ● | ● | ● | |
| 让步转折先说结论，每页最多 1 处 | | | | ● | ● #5 | ● 主体 |
| 删除免责和保险句 | ● | | | | ● #23 | 中文免责词表 |
| 默认零防御，风控/合规报告除外 | ● | | | | | ● |
| 限定词堆叠 | ● | | | ● | ● #9 | |
| 元叙述 | ● | ● | ● | | ● #4 #5 | |
| 黑话和 AI 高频词 | ● | | ● | ● | ● #12 | |
| “进行+动词”、名词化 | | ● | ● | | ● #27 | |
| 空背景开头 | | | | ● | ● #30 | |
| 拔高结尾 | ● | | ● | ● | ● #31 | |
| 聊天残留 | | ● | | ● | ● #22 | |
| PPT 标题写成结论句 | | | | ● | ● #20 | 目录式标题词表 |
| 每页一个观点、最多 4 条、末页写下一步 | ● | | | | | ● |
| 生成和编辑分两遍 | | ● | ● | | ● | 拆分方式 |
| 编辑遍只改问题句，逐句对照原文 | | ● | | | ● | |
| 用户指令优先于 skill | ● | ● | | | ● | |
| 脚本检查、FAIL 打回、最多 3 轮 | | ● | ● | ● | ● | 阈值和轮数 |
| 反面案例逐条对照、交付完就停 | | | | | | ● |

## 冲突怎么裁决

| 冲突 | 裁决 |
|---|---|
| 免责句全删，还是保留不确定性 | 默认删。材料本身的范围（样本、时间）直接写进正文。用户要求或风控、合规、审计、法务、投研报告才写风险内容，集中放一处。 |
| 禁用词表，还是禁用写法 | 以写法为准，词表只作举例。human-writing v1.1 的更新日志记录过：只禁字面时，模型换个说法照样写。 |
| “不是”“但”一律删，还是看语境 | 两部分都有信息、或纠正的是真实误解时保留。脚本把这类句子归为 soft。 |
| 删得越狠越好，还是保留虚词和语气 | 保留承担语法和语气的“的”“了”“就”，不写成电报体。 |
| 无源说法直接删，还是保留 | 编辑遍保留归属，在正文外注“缺来源”；生成遍不写无源说法。 |

## 更新日志

- **v4**：新增 `anti-examples.md`（28 条，7 组）；SKILL.md 加第 7 节“交稿前”：读反面案例库、最后逐条对照、交付完就停、长对话重贴规则，另加范文槽和口语稿→正式稿两步写法；禁用“这是X不是Y”句式和“进一步测试/验证/复盘”式结尾。脚本加 this_not、further_check、verify_list 三类检测，新增 08 号样稿和 `false_positive_v4.md`。首次公开发布，附英文版。
- **v3**：默认零防御，不写验证清单、待补、风险提示、免责，风控/合规报告除外。
- **v2**：根据实际生成的 PPT 稿，加页脚保险句和防御性“避免…”从句检测。
- **v1**：合并 5 个来源的初版。

## 许可

MIT，见 [LICENSE](LICENSE)。
