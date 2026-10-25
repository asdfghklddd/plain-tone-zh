# plain-tone-zh

[中文](README.md) | English

Writing rules for ChatGPT, Grok, Claude and Codex, plus a checker script. Written Chinese-first, with full English translations of the rules and prompts. It targets three habits that show up when AI writes slides and documents:

1. Insurance-clause hedging and disclaimers, such as:
   > "for reference only", "actual results may vary", "may to some extent", "further validation is still needed"
2. Reversal and concession templates, such as:
   > "not A but B", "you might think A, but actually B", "although A, B", "this is X, not Y"
3. Empty slide titles and inflated endings, such as:
   > "Background", "Summary & Outlook", "the future is bright", "a key step forward"

The rules target behavior, with word lists as examples only. Models reword a banned phrase and keep the habit, so the skill bans the move itself: inventing a misreading the reader never had, then knocking it down.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Full skill (layers 1–4) with frontmatter, for Codex, Claude Code and other agents |
| `custom-instructions-compact.md` / `.en.md` | Compact rules: 805 Chinese characters / 1,427 English characters, fits ChatGPT or Grok custom instructions (1,500 limit) |
| `editor-pass-prompt.md` / `.en.md` | Second-pass editing prompt (layer 3) |
| `anti-examples.md` / `.en.md` | 28 anti-examples, each with a check question to run before delivery |
| `tone_check.py` | Checker, Python standard library only; prints per-line hits, a weighted score and PASS/FAIL (layer 4) |
| `tests/` | 8 bad samples, 8 rewrites, 3 false-positive sets; results in `tests/results.md` (Chinese) |

## Four layers

1. **Layer 1, writing rules:** conclusion first, new information in every sentence, main clause first; plus behavior-level bans on the three habits. Applies while drafting.
2. **Layer 2, slide rules:** one point per slide, the title is that point with a number, at most 4 bullets, the last slide gives next steps.
3. **Layer 3, editing pass:** a separate round that changes only problem sentences and compares each against the original for added or lost information. Drafting may restructure; editing must stay faithful, so they run separately.
4. **Layer 4, check and send back:** when `tone_check.py` fails a draft, the hit lines go back to layer 3, up to 3 rounds. Finish by walking through `anti-examples.md`.

## Quick start

- **ChatGPT:** Settings → Personalization → Custom instructions. Paste `custom-instructions-compact.en.md` (or the Chinese version) into "How would you like ChatGPT to respond?". For slides, give it an outline table of "one conclusion + evidence per slide" first. After the draft, open a new chat and run `editor-pass-prompt.en.md`.
- **Grok:** Settings → Customize, paste the same compact rules. Run the editing pass with a different model.
- **Claude Code:** copy the folder to `~/.claude/skills/plain-tone-zh/`. `SKILL.md` and `tone_check.py` must sit in the same folder.
- **Codex:** same, at `~/.codex/skills/plain-tone-zh/`.
- **API:** use the body of `SKILL.md` (without frontmatter) as the system prompt. After generation call `tone_check.check(text)`; on FAIL, send `editor-pass-prompt.md` plus the hit lines, up to 3 rounds.
- **English rules for agents:** agents load `SKILL.md`. To use the English version, copy `SKILL.en.md` over `SKILL.md` in the install folder.

## Checker

```
python3 tone_check.py draft.md            # per-line hits + verdict; exit code 1 on FAIL
python3 tone_check.py draft.md --json     # machine-readable
cat draft.txt | python3 tone_check.py -   # read stdin
python3 tone_check.py draft.md --max-score 6 --max-concessive 1   # thresholds
python3 tests/run_tests.py                # regression tests
```

Verdict rules:

- **hard** (any hit = FAIL): reversal templates, the "this is X / not Y" pattern, disclaimers, "further validation needed" endings, verification lists and TBD markers, stacked qualifiers, meta-commentary, inflated endings, empty slide titles, chat residue.
- **soft** (hint only): short contrasts, "not only… but also", a single concession, jargon, nominalized verbs, scene-setting openers, footer caveats, defensive "to avoid…" clauses.
- More than one concession → FAIL. Weighted score above 6 and above 15 per 1,000 characters → FAIL.
- Lines starting with `>` and code blocks are skipped.

The script matches surface forms. It misses reworded reversals, forced triplets and invented numbers, so read the draft after a PASS.

**English support:** the rules and prompts are fully translated. The checker is Chinese-first and covers a subset of English: reversals, stacked hedges, disclaimers, meta-commentary, buzzwords, "further testing" endings, table-of-contents titles, and concessions. English inflated endings and chat residue aren't detected yet. The test set has one English sample pair (`06-doc-en.md`). English patterns the checker knows, by category:

> reversal: it's not X, it's Y / not just X but Y / this is X, not Y · hedge: could potentially · disclaimer: not financial advice · meta: it's worth noting, let's dive · buzzwords: leverage, delve, foster · ending: further testing is needed

## Test results

Numbers from `tests/results.md`; reproduce with `python3 tests/run_tests.py` (19/19 pass).

| Test | Result |
|---|---|
| 8 bad samples (`tests/before/`) | 8/8 FAIL, 54 hard hits in total |
| 8 rewrites (`tests/after/`) | 8/8 PASS, 0 hard, 1 soft |
| 3 false-positive sets: 14 legitimate sentences using 不是/但/虽然/验证/风险提示 (not, but, although, verify, risk note) | 3/3 PASS, 0 hard, 3 soft |

Hits in the seven v1 bad samples: reversal 10, meta-commentary 9, jargon 9, empty title 8, disclaimer 8, inflated ending 8, stacked qualifier 7, concession 4. The one soft hit left in the rewrites is a training-slide title about stating the conclusion first, which is the slide's actual topic.

The samples and rewrites were written by hand with made-up numbers; none are real GPT or Grok output. The tests show the script separates the two styles. How well a given model follows the rules shows up in your own drafts.

## Credits

This pack paraphrases and merges four MIT-licensed projects and a section of OpenAI's writing guidance. None of their text is copied into this repo; the rules and regexes are rewritten.

| Tag | Project | Author | License |
|---|---|---|---|
| SRH | [说人话 shuorenhua](https://github.com/MrGeDiao/shuorenhua) | MrGeDiao | MIT |
| HW | [活人感写作 human-writing](https://github.com/KKKKhazix/human-writing) | Human Writing Skill contributors | MIT |
| OIL | [oil-tone](https://github.com/oil-oil/oil-tone) | oil-oil | MIT |
| HZ | [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 歸藏 | MIT |
| OAI | [OpenAI model prompting guide, writing-style section](https://developers.openai.com/api/docs/guides/latest-model) | OpenAI | Not openly licensed; paraphrased only |

`tone_check.py` regexes are adapted from human-writing's `check_prose.py` and oil-tone's `tone_lint.py`. The slide-title rules, Chinese disclaimer list, weights and thresholds are this project's own. `anti-examples.md` entries come from public 2026 discussion on X about ChatGPT and Grok writing style, paraphrased with handles and links removed.

The per-rule source table is in the [Chinese README](README.md#规则来源对照).

## Resolving conflicts

| Conflict | Decision |
|---|---|
| Delete all disclaimers, or keep uncertainty? | Delete by default. Scope that belongs to the material (sample, time range) goes into the sentence. Risk content only when the user asks, or for risk, compliance, audit, legal or investment-research reports, in one place. |
| Ban words, or ban patterns? | Patterns; word lists are examples. human-writing's v1.1 changelog records that banning only the surface form let models reword and keep going. |
| Always delete "not" / "but"? | Keep them when both halves carry information or the contrast corrects a real misconception. The checker marks these as soft. |
| Cut as hard as possible? | Keep Chinese function words (的 / 了 / 就) that carry grammar or tone; don't write telegraph style. |
| Delete unsourced claims? | The editing pass keeps the attribution and notes "source missing" outside the text; the drafting pass doesn't write unsourced claims. |

## Changelog

- **v4:** added `anti-examples.md` (28 entries, 7 groups); SKILL.md section 7 "Before delivery" (read the anti-examples, final item-by-item check, stop when done, re-paste rules in long chats), plus a model-text slot and a spoken→written two-step; banned the "this is X / not Y" pattern and "further testing / validation / review" endings. Checker adds this_not, further_check and verify_list; new sample 08 and `false_positive_v4.md`. First public release, with English versions.
- **v3:** zero defense by default — no verification lists, TBDs, risk notes or disclaimers, except in risk/compliance reports.
- **v2:** from real generated slide decks: footer caveats and defensive "to avoid…" clauses.
- **v1:** first merge of 5 sources.

## License

MIT, see [LICENSE](LICENSE).
