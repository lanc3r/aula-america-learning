# Card Design Principles

This repository uses structured note types, not generic Basic cards. Every card
must have one clear training purpose. These rules exist to prevent the travel
prebuild problems found in NVH U6: Chinese text in audio fields, multiple main
answers in one card, recognition cards stored as production cards, and all cards
being assigned to a single lesson.

## Phase Coverage Audit

At every mid-unit Anki checkpoint, audit three layers before writing new cards:

1. **Explicit textbook targets**: grammar, vocabulary, and communicative functions that the
   current pages expect the learner to use.
2. **Source expressions that appeared but were never promoted to usable knowledge**:
   high-frequency words or chunks may occur in examples, readings, or tasks without having
   received a clear classroom introduction.
3. **Real learner production gaps**: when the learner repeatedly needs a common concept
   (for example, “some / a few”) but cannot express it, compare the need against the source
   and current deck, then add a focused card if it is high-frequency and reusable.

Do not turn this into exhaustive textbook mining. Skip low-value cultural or one-off words
unless they are useful for travel, daily communication, future source comprehension, or a
real learner need. Always deduplicate against the cumulative active deck before adding cards.

## Useful Morphology and Etymology Hints

When a word's origin, stem, prefix, suffix, shortened form, or transparent word-family relation materially helps comprehension or retention, point it out both in class and in the learner-visible Anki note/explanation. Keep it brief and practical.

Use these hints selectively. Do not mechanically decompose every word, and do not invent a modern word-building analysis just because two forms look similar.

Good examples:

- `alguno → algún` before a masculine singular noun: a shortened form, not modern `algo + un`.
- `nación → nacional → nacionalidad`: a transparent word family.
- `posible → imposible`: a productive negative prefix.
- `computar → computador/computadora`: a useful derivational family when it helps recognition.

Prefer useful modern morphology and word-family links over etymological trivia. Historical origin is worth showing only when it genuinely makes the word easier to understand or remember.

Also point out common productive endings and recurring form changes when they help the learner predict meaning or grammar. High-value examples include `-miento / -imiento`, `-ción`, `-dad`, `-ería`, `-dor / -dora`, `-mente`, and common shortened forms such as `alguno → algún`.

For pronominal infinitives, explain that the grammatical element is `-se`. With an `-ar` verb this often appears as `-arse`, e.g. `hospedar + se → hospedarse`. On first introduction, show the compact person pattern `me / te / se / nos / se` with one familiar verb. Do not imply that every pronominal verb is literally reflexive in meaning.


## Natural Expression Gate

Every Spanish target must sound like something a real speaker would plausibly
say in the intended situation. A card is not acceptable just because the Spanish
is grammatically understandable.

Before adding a production card, check:

- Is this the natural default wording for travel or daily conversation?
- Would a Latin American or Mexican speaker accept it without it sounding like
  translated Chinese or English?
- Is the context specific enough to make the phrase worth active retrieval?
- Is the card teaching a new target, rather than recombining words already
  covered elsewhere?

If the answer is uncertain, prefer one of these options:

- make it a recognition note instead of an active production card
- put the expression in `usage_zh` as an alternate or classroom note
- replace it with a more natural travel sentence
- leave it out until class discussion confirms the need

Bad:

- `在典型咖啡馆吃早饭` -> `desayunar en un café típico`

Better, depending on meaning:

- `在当地咖啡馆吃早饭` -> `desayunar en una cafetería local`
- `在传统咖啡馆吃早饭` -> `desayunar en un café tradicional`
- `在酒店附近的咖啡馆吃早饭` -> `desayunar en una cafetería cerca del hotel`

Do not keep low-value bare phrases whose only merit is that they are
grammatical. Long-term Anki cards should optimize for reusable, natural output.

## Core Learning Order

Each unit must be split into lesson blocks before cards are written.

Default order:

1. Basic vocabulary
2. Core structures
3. High-frequency collocations
4. Complete sentence chunks
5. Situational questions and answers
6. Mistake contrasts
7. Listening comprehension dialogues
8. Short paragraph output

Do not put an entire unit into one lesson unless it is genuinely tiny.

## Note Type Contract

### vocabulary

Use for one word or one fixed phrase.

Good:

- `la farmacia`
- `el museo`
- `la oficina de turismo`
- `la cafetería`

Do not use for:

- full sentences
- dialogue
- grammar rules
- multiple alternatives in one answer

Nouns should normally include the article.

Chinese prompts and meanings must disambiguate part of speech and sense when a
Chinese word could map to several Spanish targets. Do not rely on the learner to
guess which lexical target the card wants.

Good:

- `出口（名词：通道/标识）` -> `la salida`
- `出口（动词：出口商品）` -> `exportar`
- `告别；告别语（名词）` -> `la despedida`
- `告别（动词/反身）` -> `despedirse`

Bad:

- `出口` -> `la salida`
- `出口` -> `exportar`
- `告别` -> `la despedida`
- `告别` -> `despedirse`

If two cards share the same Chinese gloss, add a parenthetical cue to
`prompt_zh` and cross-reference the contrasting word in `usage_zh`.

The same visible `prompt_zh` must not point to multiple different Spanish
answers within the same note type. If two Spanish answers are both valid, either
make one a usage note or disambiguate the front prompt enough that the learner
knows which answer is being trained.

Good:

- `稍后见。` -> `¡Hasta luego!`
- `回头见 / 到时见。` -> `¡Nos vemos!`
- `你是做什么的？（¿A qué te dedicas?）` -> `¿A qué te dedicas?`
- `你做什么工作？（用 trabajar）` -> `¿En qué trabajas?`

Bad:

- `回头见。` -> `¡Hasta luego!`
- `回头见。` -> `¡Nos vemos!`
- `你做什么工作？` -> `¿A qué te dedicas?`
- `你做什么工作？` -> `¿En qué trabajas?`

Regional differences must explain the relationship, not just list a local alternative. In `usage_zh` / `regional_variant`, state whether the regional item is an exact equivalent, a near-equivalent, a more common local default, or only a recognition item. Add one short usage explanation when a bare substitution could mislead the learner.

Good:

- `menú del día`: common in Spain for a fixed-price daily set menu.
- Mexico: `comida corrida` is a common near-equivalent for an inexpensive fixed lunch; it is not a strict one-to-one synonym.

Bad:

- `México: también comida corrida.`

Learner-visible fields must not contain repository or migration metadata.
Implementation notes belong in docs, changelogs, scripts, tags, or audit reports,
not on Anki cards.

Bad in `note`, `usage_zh`, or any visible field:

- `Replaces retired pseudo-dialogue card NVH-U6-L01-D001.`
- `retired UID: ...`
- internal UID references whose only purpose is repository bookkeeping

### chunk_production

Use for Chinese/context prompt to one natural Spanish sentence or chunk.
Short paragraph prompts are allowed only when they train a compact 2-3 sentence
output that can be graded in one review.
When retiring an oversized paragraph card, split out only genuinely missing
targets; do not create replacement cards for sentences already covered by
nearby question, route, or location cards.

Good:

- `博物馆在街的尽头。` -> `El museo está al final de la calle.`
- `最好步行去。` -> `Es mejor ir a pie.`

Do not use for:

- `听到 X 你要理解成什么？`
- `A / B` as the main Spanish answer
- full conjugation tables
- fake paragraph fragments like `小段落：我的酒店在市中心。`
- long speaking tasks with four or more sentences

The main Spanish answer should be one target. Put variants in `usage_zh` or
`note`, not in the audio field.

If the real training target is a reusable sentence frame, make that frame
visible in `usage_zh` or `pattern`. Do not leave the learner guessing which
part of a full sentence transfers to new situations.

Good:

- `您知道博物馆周一开门吗？` -> `¿Sabe si el museo abre los lunes?`
- `usage_zh`: `句式：¿Sabe si ...? = 您知道是否……吗？后面接陈述句语序。`
- `pattern`: `¿Sabe si + 陈述句?`
- `您能推荐一家咖啡馆/咖啡店吗？` -> `¿Me puede recomendar un café o una cafetería?`
- `pattern`: `¿Me puede recomendar...?`
- `我可以坐地铁去吗？` -> `¿Puedo ir en metro?`
- `pattern`: `¿Puedo ir + 交通方式?`

Bad:

- same card with only `los lunes = 每周一/周一这一天类。`
- same card with only a vocabulary note while the sentence frame is unlabeled

### dialogue_response

Use for real situational question/response work.

Allowed patterns:

- Spanish question -> Spanish answer

Do not use for plain Spanish -> Chinese recognition or for Chinese -> Spanish
sentence production. If a learner should produce a question from Chinese, use
`chunk_production` instead. A `dialogue_response` card must always include both
`question_es` and `answer_es`; otherwise the review screen looks like a response
task but has no response to train.

`usage_zh` is displayed as **训练目标** on the back, so it must be a short, learner-visible explanation of the transferable skill being trained. Do not leave it empty. Prefer goals such as “听懂停留时长询问并直接回答时间长度” over simply repeating the Chinese meaning of the answer.

### grammar_pattern

Use for one structure or pattern.

Do not test an inflected form of a lemma the learner has not yet been introduced to.
If a new verb is introduced together with an irregular or high-value form, prefer one
combined retrieval target that asks for the infinitive and the target form together.

Good:

- `“说”（动词）：说出原形 + yo 形式。` -> `decir, digo`
- `“来”（动词）：说出原形 + yo 形式。` -> `venir, vengo`

Bad:

- first exposure: `venir -> yo?` -> `vengo`
- first exposure: `decir -> yo?` -> `digo`

Once the lemma is already established vocabulary, later cards may test only the inflected
form when that isolated retrieval is genuinely useful.

Good:

- `ir a + el museo = ir al museo`
- `enfrente de + el banco = enfrente del banco`
- `seguir -> siga` for usted command recognition

Do not use for wide tables or several forms at once. Related forms may appear in
the explanation, but the answer field should test one main target.

If `contrast_es` is shown as **对比** on the back, it must contain a genuinely contrasting form or example. Never repeat `answer_es` there just to fill the field. If no contrast adds learning value, leave it empty.

### mistake_contrast

Use only when there is a real likely error.

Good:

- `¿Dónde está la oficina...?` vs `¿Dónde es...?`
- `¿Hay una farmacia cerca de aquí?` vs `¿Hay una farmacia está cerca?`
- `la cafetería` vs `la cafetera`

Every card should explain the error source: Chinese transfer, English transfer,
form confusion, structure confusion, or Spain-oriented textbook wording versus
more useful Latin American wording.

### rule_concept

Use for conceptual explanations, not direct sentence production.

Good:

- `hay` vs `estar`
- `entrada` vs `boleto`
- `por aquí` vs `cerca de aquí`

The main answer is usually Chinese. Spanish examples are supporting evidence.

### listening_dialogue

Use for short, realistic listening-comprehension scenes, normally 3-6 dialogue turns.

Front:
- audio first
- one concise Chinese listening task
- no transcript or vocabulary hints that reveal the answer

Back:
- complete Spanish transcript
- concise Chinese meaning
- one useful listening focus, such as linked speech or a reduced function word

The full dialogue is synthesized in one TTS request. Do not generate each line separately
and stitch the clips together. The listening profile must use real conversational speed,
connected speech, natural reductions and normal turn-taking pauses. Do not slow the
dialogue down for A1 learners and do not insert pedagogical pauses between semantic chunks.

Keep unfamiliar material low. A listening card should recombine mostly known language
so the learner has to understand speech rather than memorize a transcript.

### short paragraph output

There is no separate note type for this yet. Use `chunk_production`, but make it
a real paragraph task:

- `prompt_zh`: ask for a short paragraph
- `spanish`: 3-6 connected sentences
- `meaning_zh`: complete Chinese meaning

Do not split a paragraph into several cards labelled `小段落：...`.

## Audio Field Rules

Audio fields must contain Spanish only.

Audio fields include:

- `spanish`
- `question_es`
- `answer_es`
- `correct_es`
- `word_es`
- `example_es`
- `answer_es`
- `contrast_es`
- `target_es`

Never put Chinese, explanations, or slash-separated alternatives in these
fields.

Bad:

- `Sigue todo derecho. / Sigue todo recto.`
- `请/您一直往前走。`
- `una cafetería / un café`

Good:

- main answer: `Sigue todo derecho.`
- usage note: `也可听到 Sigue todo recto.`

## Prebuild Conversion Rule

Never mechanically convert a Basic TSV row into a structured note type.

For every imported row, decide first:

- Is this vocabulary?
- Is this sentence production?
- Is this listening recognition?
- Is this a real dialogue?
- Is this a grammar pattern?
- Is this a mistake contrast?
- Is this paragraph output?

If the training purpose is unclear, do not add the card yet.

## Required Checks Before Release

Before building an APKG, run:

```bash
python3 scripts/validate_content.py
python3 scripts/audit_card_design.py
```

`build_deck.command` also runs both checks before audio generation and deck
building.
