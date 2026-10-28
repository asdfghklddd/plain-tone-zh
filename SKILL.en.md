---
name: plain-tone-zh
description: Chinese-first writing and editing rules (English translation) that fix three habits of AI-written text — insurance-clause hedging and disclaimers; "not A but B" / "although A, B" reversal and concession templates; empty slide titles and inflated endings; plus UI, slide-layout and report-page microcopy (less helper text, keep labels and destructive-action consequences). Use when drafting or rewriting slides, reports, documents, articles, product copy or UI copy, or when the user says "remove the AI tone", "talk like a person" or "no disclaimers". Not for pure fact lookups or code changes.
version: 5.0.0
license: MIT
---

# plain-tone-zh (English translation)

This is a translation of `SKILL.md`. The rules were written for Chinese; Chinese phrases are kept where the phrase itself is the target, with an English gloss. If you install this as an agent skill, use one of the two files, not both (they share the same `name`).

The user's explicit instructions override this skill. When they conflict, follow the user without stopping to ask.

The skill has two passes: the **drafting pass** (writing new text) and the **editing pass** (fixing existing text). Their rules differ, so keep them apart: drafting may restructure; editing changes only the problem sentences and keeps the original facts and level of certainty. The [tags] after each rule name the source; see the source table in the README.

Companion files in the same folder:
- `anti-examples.en.md` / `anti-examples.md`: 35 anti-examples to check before delivery
- `editor-pass-prompt.en.md` / `editor-pass-prompt.md`: the full editing-pass prompt
- `tone_check.py`: automatic checker (standard library only)
- `custom-instructions-compact.en.md` / `custom-instructions-compact.md`: short version for chat-product custom instructions

## 0. Floor rules (both passes; these win any conflict)

1. Add no facts, numbers, names, dates, cases, user feedback or citations that aren't in the material. If material is missing, write less or leave it out; don't leave "TBD" markers in the deliverable. [SRH][HZ][OIL][HW]
2. Lose no information: keep negations, conditions, scope, comparison targets, time, completion status, attribution and responsible party. Don't turn "may" into "will", "planned" into "done", or correlation into causation. [SRH][HZ]
3. Unsourced claims in the original ("studies show", "experts believe") keep their attribution; don't strip it into a bare fact. You may note "source missing" outside the text. [SRH]

## 1. Drafting pass: how to write

Positive instructions first; prohibitions are supplements.

- **Conclusion first, then support.** The first sentence states the main judgment or the action; support follows. One idea per paragraph; each sentence follows from the previous one. [OAI][OIL]
- **Every sentence carries new information:** at least one of a number, object, action or result. Restating the same point in other words doesn't count. Inventory the material before writing; every paragraph should rest on a specific piece of it. [HW][X public discussion]
- **Main clause first.** Who did what, then time, reason, condition. "Optimization was carried out" (进行了优化) becomes what was changed; "growth was achieved" (实现了增长) becomes how much it grew. [HW][HZ#27]
- **Plain words, precise verbs.** Use lists only for items that are truly parallel, sequential or easier to compare. [OAI][OIL]
- **Keep function words that do work.** In Chinese, 的 / 了 / 就 stay when they carry grammar or tone; don't compress into telegraph style. [OIL][HZ]
- **Vary sentence length;** don't end every paragraph with a short punchy verdict. [HW]
- **Model-text slot.** If the user supplies a sample text, put it in a [Sample] slot and copy its sentence length, word choice and paragraph structure, not its content. [v4]
- **Spoken draft → written draft (optional).** For a hard paragraph, first say it in spoken language, then convert to written style, changing wording only, adding nothing. [v4]

## 2. The three main problems (behavior rules, not word lists)

### 2.1 Reversal / contrast templates
**What's banned is the move:** setting up a misreading the reader doesn't hold, then knocking it down to make the second half sound bigger. Surface forms include 不是A而是B ("not A but B"), 不在于A而在于B ("the point isn't A, it's B"), 你以为A其实B ("you think A, actually B"), 表面A实际B ("on the surface A, in reality B"), 看似A实则B ("seems A, is actually B"), 与其说A不如说B ("less A than B"), A不重要重要的是B ("A doesn't matter, what matters is B"), 这是A不是B ("this is A, not B"), "This isn't about X. It's about Y.", "X, not Y", "this is X, not Y", and reworded variants (不是A，是B; 回头才发现 "only in hindsight did I realize"; 恰恰相反 "quite the opposite"). [HW v1.1][OAI][HZ#1][v4]
- Replacement: state B directly and put the evidence next to it.
- **Keep it when** A is a real mistaken belief the reader may actually hold, or both halves carry information ("the error happens at save, not at upload"). [HZ#1]

### 2.2 Concession (虽然…但… "although…, …")
- Give the conclusion first, then state the limitation in its own sentence. Don't pad every judgment with "although X, Y". [own rule; see HZ#5 "keep real limitations"]
- **Keep it when** the turn itself is information ("this option is cheap, but takes two weeks to deploy"). At most one per slide or paragraph.

### 2.3 Insurance clauses, disclaimers, stacked qualifiers
- **Delete:** 仅供参考 "for reference only", 不构成任何建议 "not advice", 以实际为准 "actual results prevail", 因人而异 "varies by person", 请谨慎 "please be careful", 咨询专业人士 "consult a professional", 需结合自身情况 "consider your own situation", "as an AI…"; warnings and compliance checklists added for hypothetical risks. [OAI][HZ#23][OIL]
- **Delete:** repeated qualifiers at the same level of uncertainty (可能或许 "possibly perhaps", 在一定程度上可能 "may to some extent"). [HZ#9][OIL]
- **Delete:** meta-commentary about what you won't do, what's out of scope, how things are classified (本页不讨论技术选型 "this slide doesn't cover tech choices", 需要指出的是 "it should be pointed out", 让我们深入看看 "let's dive in"). [OAI][HZ#4][HZ#5]
- **Zero defense by default:** ordinary work reports, course material, proposals and product intros state the material directly, the way a person would. No verification checklists, "to be verified / TBD" markers, risk notes, limitation sections or disclaimers, and no "things to note" at the end. Scope that belongs to the material goes into the sentence itself ("the sample is 412 orders from Aug–Sep"), not a separate warning. [v3]
- **No insurance line in every slide footer** ("to be verified", "results ≠ this product's performance", "historical price, not current"), and don't collect them into an "unverified items" slide either — delete them. Image nature (concept render / prototype) may stay as a short caption. [v2]
- **Rewrite defensive "to avoid…" clauses as positive specs:** "keep the knob, to avoid overriding the user's choice" → "manual knob setting takes priority over auto". [v2]
- **Don't end with "further testing / validation / review is still needed".** Stop at the last concrete result or next step. [v4]
- **Exception:** write risk, uncertainty or disclaimer content only when the user asks, or says it's a risk, compliance, audit, legal or investment-research report — and keep it in one place. [OAI: user instructions win][v3]
- **Consequence text on destructive UI actions is not a disclaimer.** Saying what a delete, pay or close-account button will do is operating information; see section 8. [v5]

## 3. Other frequent problems

- Jargon / AI-favorite words: 赋能 "empower", 抓手 "lever", 闭环 "closed loop", 底层逻辑 "underlying logic", 打通 "connect end-to-end", 全方位 "all-round", 助力 "boost", 重塑 "reshape", 颗粒度 "granularity"; delve, leverage, foster, genuinely. Replace with the concrete action. [HW][OAI][OIL]
- Empty scene-setting openers: 随着…的不断发展 "with the continuous development of…", 在当今…时代下 "in today's … era". Start with the content. [OIL][HZ#30]
- Vague attribution: 业内普遍认为 "the industry widely believes", 很多用户反馈 "many users report". Name the source; if there's none, cut the attribution or mark it as missing (the editing pass keeps attribution, see floor rule 3). [OIL][SRH]
- Forced triplets ("innovation, breakthroughs and new possibilities") and parallel four-character phrases. [HZ#6][HZ#29][HW]
- Chat residue: 当然可以 "of course", 好问题 "great question", 希望对你有帮助 "hope this helps". [OIL][HZ#22]
- Don't use dashes to build suspense in the final text. [HW][HZ#8]

## 4. Slide rules (layer 2)

- **One point per slide;** the title is that point written as a conclusion: subject + action/judgment + number. Example: "Q3 revenue ¥42M, up 18% YoY, mostly from new East China clients". [OIL title rule][X public discussion]
- No table-of-contents or noun titles (Background, Overview, Summary, Outlook, Competitor Overview, Key Takeaways); no "X: simple, but not casual" colon-plus-twist slogans; no "Innovation-driven · Value-led" parallel slogans. The checker can't catch noun titles; check them yourself while drafting. [OIL][v2]
- Every quantity, time and attribution in a title needs support in the material. [OIL]
- At most 4 bullets per slide, one line each, one fact each; no three-level nesting. [OAI list rule][own limit]
- The last slide gives next steps (who, what, when), not an uplifting wrap-up. [OIL][HW][HZ#31]
- Get an outline table of "one conclusion + evidence per slide" from the user or the material before layout; don't let the model free-write the copy. [X public discussion]
- For slides/PDFs, export each slide's copy to markdown and run the checker before layout.
- Subtitles, captions and footers on the layout follow section 8.

## 5. Editing pass: fixing existing text (layer 3)

Full prompt: `editor-pass-prompt.en.md`. Key points:
1. Read it through first and note the claims, numbers, conditions and qualifiers to keep. [HZ][SRH]
2. Change only problem sentences; leave good ones untouched. Don't summarize-and-rewrite, and don't rework fluent sentences to show effort. [SRH][HZ]
3. Rewrite sentences that hit 2.1–2.3 with the matching replacement. Delete disclaimer and verification content outright; don't move it or merge it into a list. Keep only wording that changes factual meaning (sample range, time range), written into the text. 
4. Compare sentence by sentence with the original: any new claim, dropped qualifier or changed strength? If unsure, revert that change. [SRH]
5. By default deliver only the text, no hit list or self-score. If the user asks to "only flag problems", list the problem snippets and the direction of the fix. [SRH][HZ]

## 6. Automatic check and send-back (layer 4)

If you can run code:
```
python3 tone_check.py draft.md
```
- Any hard hit (reversal, "this is X, not Y", disclaimer, "further validation needed", verification list / TBD, stacked qualifiers, meta-commentary, inflated ending, empty title, chat residue, "click here", slogan, unlabeled input, destructive action without consequence), or more than one concession → FAIL.
- On FAIL, hand the line numbers and tips to the editing pass, re-check, up to 3 rounds. Anything still failing: decide item by item whether it meets a "keep it when" condition; if so, keep it and say so in one line outside the text.
- For UI work, check the `.html` / `.jsx` file directly; markup inside code blocks is checked too. Two or more per-section helper lines, or three or more always-visible hint lines, → FAIL. Hints tied to an input via `aria-describedby` and hints that state a consequence don't count.
- Soft hits are hints; judge them in context. The script only matches surface forms and misses reworded reversals. PASS doesn't mean the writing is good; a final read-through decides. [OIL tone_lint's positioning][HW check_prose]
- The checker's patterns are mostly Chinese. For English text it covers a subset (see README).

## 7. Before delivery (v4)

1. **Read the anti-example file.** Before drafting, read `anti-examples.en.md`, at least each entry's check question.
2. **Last step: go through every entry.** After the editing pass and the script, answer the check question for AE-01 through AE-35. If anything matches, rewrite that sentence and start over, until nothing matches. Keep this check out of the deliverable.
3. **Stop when done.** No summary, reminders, next-step suggestions, "want me to…?" or "if you'd like…", unless the user asks.
4. **Re-paste the core rules in long conversations.** After several turns models drift back to their default style; paste the compact rules (`custom-instructions-compact.en.md`) before each request for a new draft.

## 8. Front-end copy: UI, slide layout, report pages (v5)

Applies to web and app screens, forms, dialogs, dashboards, and to subtitles, captions and footers in slides and reports. Body paragraphs still follow sections 1–4.

**Write less; let the structure explain.**
- Hierarchy, grouping, spacing and one clear primary action do the explaining. Text fills only what the structure can't. If size, position and alignment already separate things, don't add "Note", "Tip" or "Info". [v5]
- Don't add by default: slogan subtitles ("Everything at your fingertips", "Collaboration made simple"), tutorial paragraphs at the top of a page, a helper line under every card or section, "Click here to…", "Here you can…", "This section lets you…". [v5]
- Labels are nouns or short verb phrases: "Email", not "Please enter your email address below". Buttons name the action and the object: "Export PDF", "Delete 3 files"; not "OK" or "Click here". [v5]
- When extra information is needed (definitions, how a number is calculated, what a rare field means), put it behind an info icon + tooltip instead of always-visible grey text. The info icon has an accessible name (e.g. `aria-label="How conversion is calculated"`) and opens on keyboard focus. [v5]
- Same for slides and report pages: the title is the conclusion (section 4); no slogan subtitles; no "The chart above shows…". Captions carry only what the chart can't show: definition, unit, source. [v5]

**Keep these three kinds of text.**
- Form labels and accessible names: every input, select and toggle has a visible label or `aria-label`; a placeholder is not a label. Icon-only buttons have an `aria-label`. A clean screen comes from cutting redundancy, not labels. [v5]
- Consequences of destructive or irreversible actions: for delete, pay, close account, or any change that can't be edited afterwards, say next to the button or in the confirm dialog what will happen, whether it can be undone, and how much money or data is involved. E.g. "You can restore it from Trash within 30 days", "Your card ending 4821 will be charged $29". State the concrete consequence, not "Please proceed with caution". [v5]
- The next step: someone opening the screen for the first time, without reading anything, knows where to click next and what happens when they do. If they don't, fix the layout and button labels; don't add a tutorial paragraph. [v5]

**Order when rewriting an existing screen.**
1. Cut redundant labels, subtitles, helper text and slogans first; keep the three kinds above.
2. Walk the main flow as a first-time user. Where it gets unclear, adjust layout, hierarchy and button labels first; then add a tooltip; always-visible text comes last.
3. Run `tone_check.py`, then go through AE-29 to AE-35.

## Credits

This skill paraphrases and merges the following MIT-licensed projects (mostly paraphrase; short example phrases kept as-is):
- 说人话 shuorenhua © 2026 MrGeDiao — https://github.com/MrGeDiao/shuorenhua
- 活人感写作 human-writing © 2026 Human Writing Skill contributors — https://github.com/KKKKhazix/human-writing
- oil-tone © 2026 oil-oil — https://github.com/oil-oil/oil-tone
- Humanizer-zh © 2026 歸藏 — https://github.com/op7418/Humanizer-zh
- OpenAI model prompting guide, writing-style section — https://developers.openai.com/api/docs/guides/latest-model (paraphrased only; not openly licensed text)
