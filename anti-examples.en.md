# Anti-examples (don't write like this)

> Sources: entries are drawn from public complaints on X in 2026 about ChatGPT / Grok writing style, plus the maintainer's own requirements. To protect the posters, this file lists no handles or links and paraphrases the posts. A few words of the original phrasing are kept (in quotes) only where the sentence pattern itself is the point. Chinese patterns come with an English gloss.

**How to use:** after the draft is done and the editing pass has run, answer each AE's check question. If any answer is "yes", rewrite that spot and start over until nothing matches. Keep the check and the answers out of the deliverable unless the user asks.

## Reversal / contrast patterns

### AE-01
- Source: public X post (Chinese)
- Paraphrase: the conversation has been about B the whole time, and the model suddenly says "not A but B" (不是A而是B), though nobody ever mentioned A.
- Bad pattern: "not A but B" when nobody raised A
- Check: does the draft say "not A but B" about an A that never came up?

### AE-02
- Source: public X post (English)
- Paraphrase: ChatGPT now keeps saying "this is a X, not a Y", which replaced the older "not just X, it's Y".
- Bad pattern: "this is X, not Y" (这是X，不是Y)
- Check: any "this is X, not Y", "X rather than Y" or "X, not Y" closers?

### AE-03
- Source: public X post (Chinese)
- Paraphrase: lists four patterns the model repeats: "the results support X, but this step alone doesn't solve the problem"; "we can now say X, but not Y"; "this is X, not Y"; "not X, but Y".
- Bad pattern: those four fixed patterns
- Check: any of the four, including reworded variants?

### AE-04
- Source: public X post (Chinese)
- Paraphrase: for a while the model kept producing "actually it's not… but…" (其实不是…而是) and "if you'd like" (如果你愿意), and readers hated it.
- Bad pattern: "actually not… but…", "if you'd like"
- Check: any "actually it's not… but…", or an "if you'd like…" invitation at the end?

### AE-05
- Source: public X post (English)
- Paraphrase: mocks the AI's "sincere" voice: opening with "let's delve into"; contrast framing "it's not X, it's Y"; endless hedging while reluctantly agreeing ("there's nuance here, but your intuition points the right way").
- Bad pattern: delve opener + contrast framing + reluctant-agreement hedging
- Check: any "let's dive in" opener, or "there's nuance, but you're on the right track" style reluctant agreement?

### AE-06
- Source: maintainer requirement
- Paraphrase: far too many "not… but…" (不是…而是…) and "although… but…" (虽然…但…) structures.
- Bad pattern: overuse of those two structures
- Check: how many of each are in the text? Target is 0; a legitimate "although… but" at most once per slide.

## Hedging and stacked qualifiers

### AE-07
- Source: public X post (English)
- Paraphrase: the model hedges everything; the typical sentence is "you can do x, except where y and except where z, but that doesn't mean h".
- Bad pattern: several "except…" / "but that doesn't mean…" in one sentence
- Check: any sentence carrying two or more exceptions, conditions or "but that doesn't mean"?

### AE-08
- Source: public X post (English)
- Paraphrase: the model's answers look like "<answer>. <excessive hedging and defensive qualification>".
- Bad pattern: a defensive qualifier tacked on after the answer
- Check: right after a conclusion, is there a defensive qualifier or extra safety line?

### AE-09
- Source: public X post (English)
- Paraphrase: the model doesn't treat users as adults and keeps adding unnecessary caveats and qualifications.
- Bad pattern: unnecessary caveats and qualifications
- Check: any reminders or qualifiers the reader doesn't need (treating the reader as naive)?

### AE-10
- Source: public X post (English)
- Paraphrase: the model hides behind academic hedging; a lot of words that amount to "we can't know anything".
- Bad pattern: academic hedging that says nothing
- Check: any paragraph that leaves only "it's uncertain / it depends" and no usable judgment?

### AE-11
- Source: public X post (Chinese)
- Paraphrase: the poster wanted concise, clear task updates; the model piled up "not… but…" and listed a stack of restrictions for a simple discussion.
- Bad pattern: stacked "not… but…" and long lists of restrictions on simple topics
- Check: does a simple question get a long string of conditions or premises?

### AE-12
- Source: maintainer requirement
- Paraphrase: the model adds too many constraints that read like insurance clauses.
- Bad pattern: insurance-clause constraints
- Check: any contract-style constraint ("provided that…", "only if…", "please note…") the user didn't ask for?

## Disclaimers and risk notes

### AE-13
- Source: public X post (English)
- Paraphrase: the user feels every word must be airtight or ChatGPT starts inserting irrelevant disclaimers.
- Bad pattern: irrelevant disclaimers
- Check: any disclaimer unrelated to the content ("for reference only", "actual results may vary", "consult a professional", "not advice")?

### AE-14
- Source: public X post (English)
- Paraphrase: the model is maxed out on safety, disclaimers and hedges; the user has kept anti-disclaimer custom instructions for years because the model always answers in the most risk-averse way.
- Bad pattern: the most risk-averse phrasing
- Check: is the whole tone "maximally cautious, afraid of blame"? Any disclaimer that can go without losing information?

### AE-15
- Source: public X post (English)
- Paraphrase: endless disclaimers, qualifiers and pointless questions — like watching a movie with a friend who keeps listing why it couldn't really happen.
- Bad pattern: disclaimers + qualifiers + listing "why this might go wrong"
- Check: does the draft volunteer reasons or risks for things going wrong that nobody asked about?

### AE-16
- Source: public X post (English)
- Paraphrase: the model picks which custom instructions to follow; the user wrote "no disclaimers" and still keeps getting them.
- Bad pattern: adding disclaimers despite instructions
- Check: the user already said no disclaimers — are there still any?

### AE-17
- Source: public X post (English)
- Paraphrase: even when told to answer in one-syllable words, it still smuggles in a caveat.
- Bad pattern: a caveat squeezed into even the shortest text
- Check: does the shortest sentence, title or footer hide a reminder?

### AE-18
- Source: maintainer requirement
- Paraphrase: no sentences that work like disclaimer clauses.
- Bad pattern: disclaimer-like sentences
- Check: is any sentence there only to disclaim or deflect responsibility? Delete it.

## Verification lists and "to be verified" endings

### AE-19
- Source: public X post (Chinese)
- Paraphrase: the model's wrap-up is always "this still needs further testing, validation and review" (仍然需要进一步测试，验证，复盘), as if terrified of saying anything wrong.
- Bad pattern: ending with "needs further testing / validation / review"
- Check: does the ending or summary contain "still needs further testing / validation / review / research / observation"?

### AE-20
- Source: maintainer requirement
- Paraphrase: unless asked, or the document is explicitly a risk report, no verification checklists or similar over-cautious, defensive, disclaimer-type content. Nobody adds these to everyday work or class slides and PDFs.
- Bad pattern: unrequested verification checklists and defensive content
- Check: any verification checklist, unverified items, TBD, to-be-verified, risk note or limitations page (unless requested or a risk report)?

## Rebuttals and qualifiers nobody asked for

### AE-21
- Source: public X post (English)
- Paraphrase: the model keeps adding caveats nobody asked for, arguing against claims nobody made, and treats casual conversation like peer review.
- Bad pattern: unrequested caveats, rebuttals of claims nobody made
- Check: does the draft rebut something nobody said, or add a reminder nobody wanted?

### AE-22
- Source: public X post (English)
- Paraphrase: the model can't simply agree. State a view you both share and it opens an uninvited seminar: "with one nuance…", "I agree, with one caveat…", "basically right, but let me sharpen it: [aphorism]".
- Bad pattern: "but one thing…" after agreeing
- Check: after agreeing or concluding, is there an immediate "but one thing to note / one more detail"?

## Corporate / HR voice

### AE-23
- Source: public X post (English)
- Paraphrase: the model over-qualifies ordinary conversation, flattens humor and subtext, and sounds like corporate HR in a personality costume.
- Bad pattern: HR voice, over-qualification
- Check: any sentence that reads like an HR notice or official memo (thorough, polite, no stance)?

### AE-24
- Source: public X post (Chinese)
- Paraphrase: every answer is long and full of "correct nonsense"; even code comes with a long chain of fallback mechanisms.
- Bad pattern: correct-but-empty sentences, fallback padding
- Check: any sentence that is correct but carries no information, or a long passage written just to cover every case?

### AE-25
- Source: public X post (Chinese)
- Paraphrase: what grates most is the AI flavor and the deliberately short sentences.
- Bad pattern: AI flavor, artificially chopped sentences
- Check: any sentences chopped short to sound punchy (one aphorism per line, stacked)?

### AE-26
- Source: public X post (Chinese)
- Paraphrase: ask the model to polish your own article and it adds a pile of filler.
- Bad pattern: filler added while polishing
- Check: did the edit add set-up, summaries or stock phrases that weren't in the original?

## Closing summaries, reminders, suggestions

### AE-27
- Source: public X post (English)
- Paraphrase: it asks endless follow-up questions.
- Bad pattern: follow-up questions or offers at the end
- Check: does it end with "want me to…?" or "if you'd like…"?

### AE-28
- Source: public X post (English)
- Paraphrase: endless questions that lead nowhere.
- Bad pattern: aimless closing questions
- Check: does the text stop as soon as the content is delivered, with no added summary, reminder or next-step suggestion (unless requested)?
