# Learner Perspective Audit

This audit reviews the deck from the learner's review experience, not only from
the repository schema.

## Core Question

When the learner sees the front of a card, can they tell exactly what kind of
answer is expected, and is the answer worth long-term active recall?

## Current Hard Rules

### 1. The Front Must Identify The Target

The same visible Chinese prompt must not point to multiple Spanish answers in
the same note type. If two Spanish answers are both useful, the front prompt
must disambiguate them.

Fixed examples:

| Problem | Fix |
| --- | --- |
| `回头见。` -> `¡Hasta luego!` and `¡Nos vemos!` | `稍后见。` -> `¡Hasta luego!`; `回头见 / 到时见。` -> `¡Nos vemos!` |
| `你做什么工作？` -> `¿A qué te dedicas?` and `¿En qué trabajas?` | `你是做什么的？（¿A qué te dedicas?）`; `你做什么工作？（用 trabajar）` |
| `工作` -> `trabajar` and `el trabajo` | `工作（动词）`; `工作；职业活动（名词）` |

This is now enforced by `scripts/audit_card_design.py`.

### 2. Chinese Glosses Must Disambiguate Sense And Part Of Speech

A short Chinese gloss often hides multiple Spanish targets. The prompt must give
the learner enough information to retrieve the intended word without guessing.

Fixed examples:

| Prompt | Spanish |
| --- | --- |
| `出口（名词：通道/标识）` | `la salida` |
| `出口（动词：出口商品）` | `exportar` |
| `告别；告别语（名词）` | `la despedida` |
| `告别（动词/反身）` | `despedirse` |

### 3. No Repository Metadata On Cards

Migration notes, retired UIDs, replacement notes, and other implementation
bookkeeping must not appear in learner-visible fields.

Fixed example:

```text
Replaces retired pseudo-dialogue card NVH-U6-L01-D001.
```

This information belongs in docs, changelog, tags, or audit reports, not on
Anki cards. This is now enforced by `scripts/audit_card_design.py`.

### 4. Natural Output Beats Literal Translation

Spanish targets must be natural real-life output, especially for travel and
daily conversation. A grammatically understandable literal translation is not
enough.

Retired examples:

| Retired | Reason |
| --- | --- |
| `desayunar en un café típico` | Understandable but not preferred natural travel output. |
| `Prefiero conocer dos lugares.` for `我最想了解两个地方。` | `prefiero` means "I prefer / I would rather", not "what I most want to...". |

### 5. Note Type Must Match The Training Task

Do not disguise recognition, sentence production, or isolated lines as real
dialogue.

Fixed U6 issue:

- Old v047 pseudo-dialogue cards looked like listening response tasks but did
  not provide a complete real question-response pair.
- They were retired and rebuilt as `chunk_production` where appropriate.

If a full sentence is mainly teaching a reusable frame, the frame must be named
on the card. For example, `¿Sabe si el museo abre los lunes?` should explicitly
show `¿Sabe si + 陈述句?`; otherwise the learner may memorize the whole line
without noticing the transferable pattern.

The same applies to travel frames such as `¿Me puede recomendar...?`,
`¿Puedo ir...?`, `¿A qué hora...?`, `¿Dónde está...?`, `Tiene que...`,
and route confirmations ending in `¿verdad?`.

### 6. Do Not Make Fake Paragraph Cards

A card labelled `小段落：...` must not test one isolated sentence. A paragraph
task should be a compact 2-3 sentence output, or else it should stay outside
normal Anki review.

Fixed U6 issue:

- Seven old v047 `小段落：...` single-sentence cards are documented as legacy
  cards to delete or suspend in Anki.

## Current Residual Risks

### Historical Slash Alternatives

The design audit still reports 102 warnings for older supporting audio fields
with slash-separated alternatives. These are not current release blockers, but
they should be cleaned when those cards are next edited.

Risk:

- Audio for slash alternatives may be less clean.
- The learner may see multiple forms where one main target would be better.

Policy:

- New cards must use one main target.
- Variants belong in usage notes.
- Historical cards should be fixed opportunistically, not all at once unless a
  dedicated cleanup is scheduled.

### Long Explanations On The Back

Some older concept cards have long explanations. They are not wrong, but they
can turn a review into a mini-lesson.

Policy:

- Back explanations should normally be one short paragraph.
- If the explanation becomes a lesson, split it into a `rule_concept` card or
  move the extra detail to class notes.

### Duplicate Concept Coverage

Some early units intentionally repeat useful travel or social expressions. This
is acceptable only when each card trains a different cue, register, or context.

Policy:

- If two cards train the same Spanish output from nearly the same Chinese cue,
  retire the lower-value one.
- If both are useful variants, make the front prompt explicitly name the
  target pattern or context.

## Release Checklist Additions

Before future release:

```bash
python3 scripts/validate_content.py
python3 scripts/audit_card_design.py
```

Then review a mobile-style sample of:

- 10 vocabulary cards
- 10 chunk production cards
- 5 dialogue cards, if any
- 5 grammar or mistake cards

For each card, ask:

1. Do I know what answer the front is asking for?
2. Is there only one main target?
3. Is the Spanish natural and useful?
4. Is the back concise enough for review?
5. Is every visible detail useful to the learner right now?
