# Changelog

## 0.9.6

- Added morphology memory hints to the U7 algun/alguna cards.
- Added a design rule to include useful word-family and form-origin hints selectively.
- No cards were added or removed; total remains 1109 notes.

## 0.9.5

- Fixed the two U7 `algún / alguna` grammar cards whose **对比** field accidentally repeated the main answer.
- The masculine card now contrasts `¿Hay algún mercado por aquí?` with `¿Hay alguna farmacia por aquí?`; the feminine card shows the reverse comparison.
- Added an audit error for `grammar_pattern` cards whose `contrast_es` is identical to `answer_es`.
- No new cards were added; cumulative total remains 1109 notes.

## 0.9.4

- Fixed five U7 `dialogue_response` cards whose learner-visible **训练目标** field was empty.
- Added concise transferable training goals for immigration/customs prompts about stay duration, occupation, declarations, medications, and luggage count.
- Updated the dialogue-response back template so a legacy empty `UsageZH` never renders a blank labeled box.
- Strengthened card-design audit: every active `dialogue_response` must now have a non-empty learner-visible training goal.
- No Spanish audio text changed; cumulative total remains 1109 notes.

## 0.9.3

- Expanded the regional note for `el menú del día` so it explains what the Spanish concept is, how Mexican `comida corrida` overlaps with it, and why the two are not strict synonyms.
- Added a card-design rule that regional notes must label the relationship explicitly: exact equivalent, near-equivalent, more common local default, or recognition-only item.
- No cards were added or removed; cumulative total remains 1109 notes.

## 0.9.2

- Added a 31-card backlog cleanup for NVH U3, U5, and U6 after comparing active Anki coverage against the textbook's core vocabulary and communication resources.
- U3: added the character sense of `abierto/a` and recognition-oriented `bajito/a`, `gordito/a`, with usage notes to avoid confusing `ser abierto/a` with `estar abierto/a`.
- U5: restored high-value textbook food/service language including `caliente`, `al mediodía`, `muchas veces`, `el menú del día`, `el plato combinado`, `el bocadillo`, `la tapa`, plus `medio litro de agua`, `una barra de pan`, `una tableta de chocolate`, `¿Se come caliente o frío?`, and recognition-response cards for `¿Qué le pongo?` / `¿Qué van a tomar?`.
- U6: restored high-value city/transport vocabulary including `el centro comercial`, `el punto de información`, `la panadería`, `la zapatería`, `la frutería`, `la tienda de ropa`, `la tienda de regalos`, `la oficina de correos`, `los servicios`, `el barco`, `la bicicleta`, and `el puerto`.
- Added a focused `dónde` vs `adónde` concept card, active `¿Adónde va?`, and a route-sequencing concept for `Primero / Después / Al final`.
- Regional notes keep Spain-heavy textbook items primarily for recognition while preserving Mexico/Latin-America active-output priorities (`los baños`, `sándwich/torta`, `comida corrida`, etc.).
- New cumulative total: 1109 notes.

## 0.9.1

- Completed the Phase 2 practical quantifier set with active singular `algún + masculine noun` and `alguna + feminine noun` retrieval.
- Expanded the quantifier concept card to distinguish `unos/unas`, `algún/alguna`, `algunos/as`, `varios/as`, `pocos/as`, and `un poco de`.
- Added `¿Hay algún mercado por aquí?` and `¿Hay alguna farmacia por aquí?` as focused grammar-pattern cards.
- New cumulative total: 1078 notes.

## 0.9.0

- Added 57 active NVH U7 Phase 2 notes and advanced `unidad_nvh_07.json` to `phase2_active` / content version `0.2.0`.
- Covered the newly taught `pretérito perfecto`: its communicative purpose, regular participle formation, high-frequency irregular participles (`hecho, visto, dicho, puesto, abierto, escrito, vuelto, sido`), and travel-experience markers such as `alguna vez, ya, todavía no, nunca, hasta ahora`.
- Added learner-error contrasts from the live lesson, including missing `haber`, `nunca` vs `todavía no`, `visitar allí` vs `estar allí`, personal `a` with people, `comprado` vs `comparado`, and `muchas fotos`.
- Formalized `muy / mucho / mucho-a-os-as` with one conceptual rule and focused production cards.
- Closed a real lexical coverage gap around English-like quantity needs: `unos/unas`, `algunos/as`, `varios/as`, `pocos/as`, and `un poco de`. The deck now explicitly distinguishes neutral “some / a few” from scarcity-oriented `pocos/as`.
- Added textbook travel-preparation vocabulary and chunks that had appeared without enough active instruction: `alquilar` (with Mexico `rentar` calibration), `el consulado`, `el itinerario`, `vacunarse`, `la guía`, `hacer el equipaje`, `cambiar dinero`, and `reservar una mesa`.
- Added useful U7 travel/culture vocabulary encountered in the source or lesson: `el crucero`, `el malecón`, `el plato típico`, and `al aire libre`.
- Added three natural-speed listening dialogues for travel experience, pre-trip preparation, and quantity expressions.
- Phase 2 intentionally stops before the complaints/apologies block, so no unreached complaint content was activated.
- New cumulative total: 1076 notes.

## 0.8.2

- Redesigned all six U7 `-go` first-person cards so a new verb is not tested by inflection before its lexical meaning has been introduced.
- Each card now retrieves the infinitive and yo form together, e.g. `“说”（动词）：说出原形 + yo 形式。` → `decir, digo` and `“来”... ` → `venir, vengo`.
- Applied the same combined format to `hacer/hago`, `poner/pongo`, `salir/salgo`, `traer/traigo`, `decir/digo`, and `venir/vengo` for a consistent learning sequence.
- Added a card-design rule: never test an inflected form of a lemma before lexical introduction; when a new verb and irregular form arrive together, combine them into one retrieval unit.
- The six answer-audio texts changed, so a normal `build_deck.command` run will generate only those missing new audio files and reuse all unaffected cache entries.

## 0.8.1

- Fixed two learner-facing U7 Chinese prompts without changing UIDs or Spanish targets.
- `NVH-U7-R1-L03-P002`: changed the front from “我不介意，但我父母介意。” to “我不介意噪音，但我父母介意。” so the object required by `No me molesta el ruido...` is explicit.
- `NVH-U7-R1-L02-P003`: changed the hotel-date prompt to “酒店前台问：您要订哪几天？【用 para 提问】” so the intended `¿Para qué fechas?` retrieval is uniquely cued.
- No audio text changed, so existing TTS cache can be reused; a normal `build_deck.command` rebuild is sufficient.

## 0.8.0

- Rebuilt NVH U7 Phase 1 from scratch under new `NVH-U7-R1-...` UIDs; no UID is reused from `inactive_content/`, which remains reference-only.
- Added 57 active U7 Phase 1 notes covering Mexico immigration/customs, hotel booking and services, focused `por/para` use, `molestar`, contrastive `pues`, six high-frequency yo `-go` forms, `traer/llevar`, and learner-error contrasts.
- Deliberately stopped before systematic `pretérito perfecto` instruction; prebuilt perfect-tense and later complaint cards remain inactive.
- Added a new `listening_dialogue` Note Type with model ID `1607392327`. Existing Note Type model IDs and field contracts remain unchanged.
- Added four 3–4 turn listening cards. Each full dialogue is synthesized in one request rather than line-by-line.
- Added a dedicated `listening_dialogue` TTS profile at speed 1.08 with realistic Latin-American connected speech, no A1 slowdown, no pedagogical pauses, no word-by-word articulation, natural reductions, linking and turn-taking rhythm.
- Made the audio cache profile-aware so the same text can safely have different normal-card and listening-dialogue renderings.
- Extended card-design audit and documentation for listening-dialogue length, transcript hiding, and natural listening-load requirements.
- New cumulative total: 1019 notes.

## 0.7.3

- Fixed `mistake_contrast` cards that exposed their only correct answer on the front. Cards without a wrong candidate now show the prompt alone; cards with two candidates shuffle their order.
- Removed incomplete pseudo-choices from four U6 fill-in cards and hid empty wrong-answer boxes on the back.
- Added an audit error for incomplete `wrong_es` choices.

## 0.7.2

- Cleaned generated local artifacts from the repository layout: `github_upload/`, `output/`, `release/`, Python caches, temporary preview/report files, and stale generated ZIP history are now treated as rebuildable outputs instead of source files.
- Added `.gitignore` entries for generated deck artifacts, upload copies, local audio cache, Python caches, and generated reports/previews.
- Synchronized release metadata in `config/deck_config.json` with the current version line so future deck builds no longer use the stale `v0_6_6` output name.
- Reduced `prebuilds/` to TSV source inputs only; historical APKGs, manifests, and bundle ZIPs are generated artifacts and are no longer kept in the source repository.
- Removed obsolete root-level historical audit snapshots; active design rules remain in `docs/` and `scripts/audit_card_design.py`.

## 0.7.1

- Further strengthened the global TTS instruction against word-by-word delivery, emphasizing connected prosodic groups, no micro-pauses between short function words, and natural liaison between consonant-final and vowel-initial words.
- Added exact `text_instruction_overrides` for high-value U6 travel sentences that commonly sound unnatural when read word by word, including `¿Hay una farmacia por aquí?`, `¿Dónde está la oficina de turismo?`, `¿Puedo ir en metro?`, `¿Este autobús va al centro?`, route directions with `en dirección al centro`, and `¿Cuánto se tarda?`.
- Documented the per-text override workflow for future audio cleanup.

## 0.7.0

- Strengthened the global TTS instruction to require connected speech within prosodic groups, with explicit examples such as `por aquí`, `está abierto`, `dónde está`, `quién es`, `en el centro`, `va al centro`, and `cuánto se tarda`.
- Documented that common Spanish word groups should be produced with natural enlace, sinalefa, and resilabificación instead of word-by-word cuts.

## 0.6.9

- Updated global TTS instructions for more natural Latin American Spanish audio, aiming for a Mexico-adjacent neutral accent, realistic conversational grouping, friendlier travel/service intonation, and less word-by-word classroom reading.
- Adjusted TTS speed from `1.0` to `1.03` for future regenerated audio.
- Documented the current audio style target in `readme.md`.

## 0.6.8

- Added explicit `pattern` / `usage_zh` labels to the U6 reusable travel sentence frames, including `hay/no hay`, `¿Dónde está...?`, `¿Me puede recomendar...?`, `¿A qué hora...?`, `¿Puedo ir...?`, `¿Tengo que...?`, `Tiene que...`, route confirmations with `¿verdad?`, and `¿Cuánto se tarda?`.
- Expanded the learner-facing principles: if a card is mainly teaching a transferable sentence frame, that frame must be visible on the card.
- Generalized the design audit so common reusable U6-style chunk patterns fail when `pattern` is left blank.

## 0.6.7

- Clarified `NVH-U6-L01-P081` as a `¿Sabe si + 陈述句?` pattern card, while keeping `los lunes` as a secondary usage note.
- Updated card-design principles and the learner-perspective audit: reusable sentence frames must be named in learner-visible fields.
- Added an audit rule that fails `¿Sabe si ...?` production cards when the transferable pattern is not labeled.

## 0.6.6

- Added `docs/learner_perspective_audit.md`, a learner-facing review of card design risks and release checklist additions.
- Fixed remaining exact-prompt ambiguity where the same Chinese front mapped to multiple Spanish targets:
  - `AA1-U01-L02-P003`: clarified `¿A qué te dedicas?`.
  - `AA1-U01-L07-P006`: clarified `¿En qué trabajas?` as the `trabajar` target.
  - `AA1-U01-L03-P005`: clarified `¡Hasta luego!`.
  - `AA1-U01-L03-P006`: clarified `¡Nos vemos!`.
  - `NVH-U04-LX-V012`: clarified `trabajar` as the verb.
  - `NVH-U04-LX-V047`: clarified `el trabajo` as the noun.
- Added an audit rule that fails when the same visible `prompt_zh` maps to multiple different Spanish targets in vocabulary, chunk-production, or grammar-pattern cards.
- Updated `docs/card_design_principles.md` with the same-prompt/multiple-target learner rule.

## 0.6.5

- Removed 40 learner-visible internal migration notes from U6 replacement cards (`Replaces retired pseudo-dialogue card ...`).
- Added an audit rule to fail if learner-visible fields contain internal repository metadata such as retired-card replacement notes or UID bookkeeping.
- Updated `docs/card_design_principles.md` to keep implementation and migration metadata out of Anki card displays.

## 0.6.4

- Added a vocabulary prompt disambiguation rule to `docs/card_design_principles.md`: Chinese prompts must clarify part of speech and sense when one Chinese gloss can map to multiple Spanish targets.
- Updated ambiguous vocabulary prompts:
  - `AA1-U03-TC-V002`: `出口` -> `出口（名词：通道/标识）` for `la salida`.
  - `NVH-U03-L06-V002`: `出口` -> `出口（动词：出口商品）` for `exportar`.
  - `NVH-U04-LX-V005`: `告别` -> `告别；告别语（名词）` for `la despedida`.
  - `NVH-U04-LX-V007`: `告别` -> `告别（动词/反身）` for `despedirse`.

## 0.6.3

- Retired `NVH-U6-L01-P069` (`Prefiero conocer dos lugares`) because the Spanish answer does not match the Chinese prompt `我最想了解两个地方。`; `prefiero` means "I prefer / I would rather", not "what I most want to...".
- Updated `docs/u6_legacy_v047_cleanup.md` with natural replacement candidates for the classroom task: `Quiero conocer dos lugares en particular.` and `Me interesa conocer dos lugares sobre todo.`

## 0.6.2

- Added a formal natural-expression gate to `docs/card_design_principles.md`: active Spanish targets must be natural real-life output, not merely grammatical literal translations.
- Documented `desayunar en un café típico` as the model U6 cleanup example for retiring low-value, translation-like bare phrases.
- No active card content changed from v0.6.1.

## 0.6.1

- Retired `NVH-U6-L01-P061` (`desayunar en un café típico`) because it is understandable but not the preferred natural travel output, and its component targets are already covered elsewhere.
- Updated `docs/u6_legacy_v047_cleanup.md` with better alternatives: `desayunar en una cafetería local` and `desayunar en un café tradicional`.

## 0.6.0

- Retired the duplicate U6 future-prebuild card `NVH-U6-L01-P060` (`ir al teatro`), because U4 already covers `el teatro` and the U6 card only tested a bare phrase.
- Updated `docs/u6_legacy_v047_cleanup.md` with the `ir al teatro` cleanup note and Anki search term.
- Established this as the cleaned U6 baseline after the v047 travel-prebuild audit.

## 0.5.9

- Retired 15 U6 standalone vocabulary cards that duplicated words already covered in U2, U3, or U5.
- Kept the active U6 vocabulary list focused on true U6 gaps: `la catedral`, `la oficina de turismo`, `la estación de metro`, `la cafetería`, `el centro histórico`, `el semáforo`, `el puente`, `la línea`, and `el plano de la ciudad`.
- Updated `docs/u6_legacy_v047_cleanup.md` with the retired duplicate-vocabulary UID list and earlier coverage references.

## 0.5.8

- Retired the duplicate U6 future-prebuild card `NVH-U6-L01-P059` (`ir de compras`), because U2 already covers `Quiero ir de compras.` and `las compras`.
- Updated `docs/u6_legacy_v047_cleanup.md` with the `ir de compras` cleanup note and Anki search term.

## 0.5.7

- Added `docs/u6_legacy_v047_cleanup.md` documenting the seven legacy v047 `production salida` pseudo-paragraph cards that may remain in Anki after earlier imports.
- Recorded Anki Browse search terms for deleting or suspending old `小段落` cards that are not part of the active content.
- No active card content changed from v0.5.6.

## 0.5.6

- Retired the two v0.5.5 replacement cards `NVH-U6-L01-P111` and `NVH-U6-L01-P112` after duplicate review showed their targets were already covered by earlier U6 cards.
- Kept `NVH-U6-L01-P050` retired without adding near-duplicate replacements.
- Clarified the card-design principle for splitting long paragraph cards: add replacement cards only for genuinely missing targets.

## 0.5.5

- Retired the oversized U6 paragraph-output card `NVH-U6-L01-P050`, which asked for seven sentences in a single Anki review.
- Added two smaller replacement output cards: `NVH-U6-L01-P111` and `NVH-U6-L01-P112`.
- Tightened the card-design audit so `小段落：` prompts must stay within 2-3 Spanish sentences.
- Updated `docs/card_design_principles.md` to keep long speaking tasks out of normal Anki review cards.

## 0.5.4

- Fixed U6 pseudo-dialogue cards imported from v047: 40 `dialogue_response` cards with only a Spanish question or only a Spanish answer were retired and rebuilt as `chunk_production` output cards (`NVH-U6-L01-P071` through `NVH-U6-L01-P110`).
- Tightened the card-design audit so `dialogue_response` must include both `question_es` and `answer_es`.
- Updated the v047 integration script so Chinese -> Spanish question cards are no longer inferred as dialogue cards just because the Spanish side is a question.
- Updated `docs/card_design_principles.md` to document the stricter `dialogue_response` contract.

## 0.5.3

- Added `docs/card_design_principles.md` to define the note type contract and card design rules used after the U6 travel prebuild cleanup.
- Added `scripts/audit_card_design.py` to catch card-design issues before release, including Chinese text in audio fields, slash-separated alternatives in main answer fields, recognition prompts stored as production cards, fake paragraph fragments, and units collapsed into one lesson.
- Integrated card-design audit into `scripts/build_deck.py` and `validate_content.command`.
- Split `NVH-U03-L02-M001` into two smaller mistake cards so each card tests one contrast only.
- Kept U7-U9 inactive while U6 is brought back to the formal U1-U5 standard.
- Updated release metadata to `0.5.3`.

## 0.5.0

- Created the travel prebuild repository release.
- Preserved the full `anki_v046` code repository and cumulative source content.
- Included uploaded `anki_v047_nvh_u6_prebuild` artifacts under `prebuilds/v047/`.
- Added generated v048-v050 travel prebuild artifacts under `prebuilds/v048_v050/` and `release/`.
- Added `scripts/build_travel_prebuild.py`, the generator used for v048-v050.
- Added `travel_prebuild_readme.md` and `travel_prebuild_manifest.json`.
- Kept U8 as a Mirador review package rather than a heavy new-content unit.
- Used v047 TSV as the hard dedupe baseline for v048-v050.
- Final note counts:
  - v047 U6 prebuild: 146
  - v048 U7 prebuild: 133
  - v049 U8 Mirador review: 64
  - v050 U9 prebuild: 157
  - combined v048-v050 travel pack: 354

## 0.4.6

- Formally closed NVH U5 `Comer con gusto`; `content/unidad_nvh_05.json` is now `complete` and content version `0.3.0`.
- Added 45 new notes in the final U5 closeout: 17 vocabulary, 6 rule/concept, 5 grammar-pattern, 10 chunk-production, 1 dialogue-response, and 6 mistake-contrast notes.
- Closed the Aula bridge gap for `este / esta / estos / estas / esto`, including standalone `este/esta` vs neutral `esto` and the learner error `esto taco → este taco`.
- Completed `pedir` as `pido / pides / pide / pedimos / piden`, while preserving the real-life distinction between discussing an order (`¿Qué vas a pedir?`) and directly ordering from staff (`Dos tacos, por favor / Quería...`).
- Added targeted `ir` retrieval for `vas`, `vamos`, and `van`; the deck still avoids broad conjugation-table drilling.
- Added Mexico Food Core I: `taco`, `maíz`, `frijol/frijoles`, `cilantro`, `crema`, `piña`, `sopa`, `caldo`, `quesadilla`, plus restaurant essentials `vaso`, `hielo`, `refresco`, `sin`, `gramo`, `litro`.
- Added high-value Costa Rica/food description vocabulary `típico/a`, `delicioso/a` and the chunk `rico en vitaminas`; existing `salsa` and `tropical` were reused instead of duplicated.
- Added a deliberately small authentic Travel Core set: `¿Aceptan tarjeta?`, `¿Me da...?`, `¿Me puede dar...?`, `¿Qué me recomienda?`, `¿Tiene algo sin...?`, `¿Lo puede hacer sin...?`, `La cuenta, por favor`, `Un vaso de agua con hielo`, and `¿Qué vas a pedir?`.
- Added the real-life distinction `tacos de pescado` (dish/type) vs `con pescado` (ingredient/accompaniment).
- Added final learner-error cards from the U5 closeout check: direct-object gender/number, `pedir` e→i, `estar + bueno` plural agreement, `de` vs `con`, demonstratives, and restaurant checkout.
- Low-value recipe/video vocabulary such as `remolacha`, `sésamo`, and `cebollino` remains intentionally outside active retrieval.
- No Note Type, deck ID, model ID, field order, template, or historical UID changes.
- New cumulative total: 841 notes.

## 0.4.5

- Continued NVH U5 `Comer con gusto`; `content/unidad_nvh_05.json` remains `in_progress` and advances from content version `0.1.0` to `0.2.0`.
- Added 81 new notes in this checkpoint: 24 vocabulary, 22 rule/concept, 18 grammar-pattern, 11 chunk-production, 4 dialogue-response, and 2 mistake-contrast notes.
- Covered the formally taught 100+ number system: `cien/ciento`, gender agreement of hundreds, `y` placement, `uno → un/una`, and irregular `quinientos / setecientos / novecientos`.
- Added the U5 direct-object system `lo / la / los / las`, including basic position, negation, two-verb placement (`Las quiero comprar / Quiero comprarlas`), and recognition of topic-fronting (`Las manzanas, las compro yo`).
- Added the U5 `se` block while preserving the textbook's A1 functional framing and recording the stricter distinction between impersonal `se` and passive `se`.
- Added telling time and action-time questions: `¿Qué hora es?`, `Es la una / Son las...`, `¿A qué hora...?`, direct numeric time reading, and recognition of the `menos` system.
- Added the taught frequency block: `todos los días`, `muchas/pocas veces`, `una/dos veces...`, `casi nunca`, `nunca`, plus `al día / por semana / al mes` patterns.
- Continued Aula América cross-checking instead of treating NVH in isolation: added `desayunar / almorzar`, the `almuerzo` vs Spain-oriented `comida/comer` contrast, and the explicitly taught weekday supplement (`lunes`–`domingo`, `el viernes / los viernes`).
- Added `ir` as a standalone high-frequency verb and active `ir / salir` patterns taught in class.
- Added lexical support that had appeared in U5 examples but lacked standalone retrieval: `té`, `tortilla`, `calamar`, `café`, `peso`, `mayonesa`, `chile`, `hora`, `día`, `fecha`, `vez`, `casi`, `nunca`, and `comida`.
- Corrected the existing `¿Cuántas quiere? — Un kilo y medio.` dialogue card by restoring the minimum context `Prefiero manzanas`, so `cuántas` and `quiere` are no longer ambiguous.
- Refined the previously published U3 date cards without changing their UIDs: birthday/event dates commonly use `el`, while direct reporting such as `Hoy es 28 de agosto` normally does not.
- Updated the existing `el almuerzo` and `salir` vocabulary notes to reflect the material now formally taught.
- Added learner-error contrasts for `quinientas ... pesos → quinientos ... pesos` and `setecientos ... personas → setecientas ... personas`.
- No Note Type, deck ID, model ID, field order, template, or historical UID changes.
- New cumulative total: 796 notes.

## 0.4.4

- Started NVH U5 `Comer con gusto` with an in-progress `content/unidad_nvh_05.json`.
- Added 68 notes for the first U5 checkpoint: 38 vocabulary, 8 rule/concept, 5 grammar-pattern, 11 chunk-production, 3 dialogue-response, and 3 mistake-contrast notes.
- Covered the opening food vocabulary, quantities/containers already taught, market buying and price questions, and `preferir / probar / poder / costar`.
- Reused existing standalone cards for `el agua`, `probar`, `picante`, `la tarjeta`, and `el efectivo` instead of duplicating them.
- Preserved NVH source terminology in notes while calibrating active Latin-American output: `camarón` records NVH/Spain `gamba`, and `papa` records NVH/Spain `patata`; `jugo` is retained as the current Latin-American classroom choice with Spain `zumo` noted.
- Added current learner-error contrasts for `cuentan → cuestan`, `quiero → quieres`, and `pedemos → podemos`.
- Added the current concept work on `todo` and the unified core meaning of `más`.
- Kept later U5 grammar deferred: direct-object pronouns, impersonal `se`, numbers above 100, time/frequency, and the full `pedir` paradigm.
- No Note Type, deck ID, model ID, field order, template, or historical UID changes.
- New cumulative total: 715 notes.

## 0.4.3

- Closed NVH U1-U4 after Mirador with a focused 36-note final patch: 27 vocabulary notes + 9 active collocation chunks.
- Corrected the v0.4.2 source-audit error: Mirador 4 does contain the `HACER / TENER / TOMAR / LLEVAR` collocation activity.
- Added remaining high-value U2 profession/contact vocabulary: `enfermero/a`, `policía`, `informático/a`, `arquitecto/a`, `veterinario/a`, `escritor/a`, `programador/a`, `cantante`, `jubilado/a`, `punto`, `guion bajo`.
- Completed the main U3 person-description opposites with `mayor`, `feo/a`, `antipático/a`, `pesimista`, `alegre`, and `triste`.
- Added U4 support nouns and active collocations such as `tener frío`, `tener prisa`, `tener tiempo`, `hacer la maleta`, `tomar un taxi`, `tomar una cerveza`, `tomar el sol`, `llevar gafas`, and `llevar zapatos negros`.
- Added a deliberately small classroom supplement from the final Mirador dialogue: `entrenar`, `las pesas`, `cocinar`, and `por la mañana / por la tarde / por la noche`.
- Kept lower-priority printed items passive rather than dumping every word into Anki.
- No Note Type, deck ID, template, TTS contract, or historical UID changes.
- New cumulative total: 647 notes.

## 0.4.2

- Added a 74-note `NVH U1-U4 Lexical Catch-up` before closing Mirador U4.
- Re-scanned NVH U1-U3 lexical objectives and `Más que palabras`, plus U4 Mirador review vocabulary.
- Added standalone retrieval cards for high-frequency words that had previously appeared only inside chunks or grammar examples.
- Added missing profession/workplace vocabulary, personal/contact-information nouns, key person-description words, and Mirador greeting/relationship expressions.
- Added Latin-American calibration for `computadora / ordenador`, `celular / móvil`, and `camarero / mesero`.
- Added `normalmente` with a compact `-mente ≈ -ly` word-formation reminder.
- Kept the update lexical: no new grammar block was introduced.
- Corrected source scope: the `hacer / tener / tomar / llevar` collocation table discussed in class is not present in this edition's Mirador 4 and is therefore not counted as NVH textbook coverage.
- New cumulative total: 611 notes.

## 0.4.1

- Nos vemos hoy U3《Me gusta mi gente》正式收口；`content/unidad_nvh_03.json` 从 `in_progress` 更新为 `complete`，内容版本提升到 `0.2.0`。
- 完成 Nos vemos U3 ↔ Aula América U5 最终覆盖审计，并在同一 v0.4.1 中做 Travel Core III 缺口补充；相对 v0.4.0 累计新增 53 张，U3 + Bridge + Travel Core III 共 174 张。
- 新增 `interesar`，并沿用 `gustar / encantar` 的同一底层结构：`interesa/interesan` + `me/te/le/nos/les`。
- 新增 `un amigo mío / una amiga mía`、`¿Con quién...?`、`favorito/a`、`¿Qué tipo de música te gusta más?`。
- 新增音乐话题的紧凑词汇组：`pop / rock / jazz / música clásica / música electrónica / música latina / reguetón / salsa`。
- 加入拉美口语 `bien + adjetivo` 的被动识别卡；主动输出仍优先更通用的 `muy`。
- 从 Chocolates Valor / Guatemala 可理解输入中只抽取可复用的高价值内容：`producto / exportar / naturaleza / fascinante / oficial / limitar con`、`más de + número`、`el español` vs `hablar español`、`trabajar con X`。
- 根据本轮真实输出新增错误卡：`¿Cuándo tu cumpleaños?`、`¿Dónde es tu hotel?`、`Tiene...` vs `Tengo...`、`Tengo los padres viven...`、语言名称小写、`Me gusta más el pop` 语序，以及 `¿Quién es? / ¿Cómo es? / ¿Dónde vive?` 信息类型辨析。
- 不机械加入 `parecer + adjetivo`、`exesposo/a`、`tener unos 30 años` 和文化阅读中的低频专名；这些登记为延后内容。
- Travel Core III 重新核对全卡组后，只追加 12 个此前确实缺失的高频旅行词：`el avión / la terminal / el asiento / el cajero automático / la propina / la tarjeta de embarque / el equipaje de mano / la aduana / el retraso / el barrio / la contraseña / picante`；已有旅行词不重复创建。
- 保留既有 deck ID、Note Type model ID、字段顺序、模板、Cedar 拉美西语 TTS 配置和全部历史 UID；无不兼容迁移。
- 本次仍不在分发包中生成 MP3 或 `.apkg`；本地 Builder 会复用旧 `audio_cache`，只为新增西语文本生成缺失音频。

### card counts

- chunk_production: 96
- dialogue_response: 41
- vocabulary: 253
- grammar_pattern: 43
- rule_concept: 52
- mistake_contrast: 48
- pronunciation: 4
- total: 537

## 0.4.0

- 课程主线正式从 Aula América 切换为 Nos vemos hoy；旧 Aula América Unidad 1–3 内容完整保留，Aula América 继续作为拉美西语校准、旅行表达补充和覆盖审计来源。
- 新增 `content/unidad_nvh_03.json`，用于保存 Nos vemos hoy U3《Me gusta mi gente》的 Bridge Lesson 与当前学习进度，避免与历史 `content/unidad_03.json` 冲突。
- 本版新增 121 张卡，不再把“每天 40 张新卡”当作单次制卡数量上限；卡片数量改由内容覆盖、学习依赖和单卡提取质量决定。
- Bridge 新增 `probar`、`Estados Unidos / estadounidense`、`coche / carro`、`Encantado`、`Igualmente`、`Tenemos una reserva`，以及西班牙 `vosotros` 的被动识别规则。
- 家庭与关系新增核心亲属词、`pareja / esposo/a / novio/a / compañero/a de trabajo`，并系统化 `mi/mis · tu/tus · su/sus · nuestro/a/os/as`。
- 增加 `su` 歧义消解：`de + 人/代词`，并针对本轮真实错误加入 `nuestro madre → nuestra madre`、`su padres → sus padres`、`tu el hotel → su hotel` 等辨析。
- 人物描述新增高频外貌/性格形容词、`tener el pelo... / tener los ojos...`、身体部位定冠词母规则、婚姻状态 `estar + estado`。
- `gustar` 系统新增 `me/te/le/nos/les`、`A + 人 + le`、`A mí me...`、`también / tampoco / A mí sí / A mí no`，并从 Aula 对应内容补充高频 `encantar`。
- 针对真实输出错误新增 `Le gusta... y le encantan...` 的第二个 `le`、`un poco + adj` vs `un poco de + n`、形容词复数一致、`muy alto` 等辨析。
- 日期部分新增 12 个月、`¿Cuándo es tu cumpleaños?`、`el + día + de + mes`、拉美优先 `el primero de...`、`Creo que...`。
- `Nos vemos` 主线内容仍使用原有七种 Note Type、既有 model ID、字段顺序、模板、deck ID 和 Cedar 拉美西语 TTS 配置；不做不兼容迁移。
- 技术上的 deck 名称和输出文件前缀暂时保留历史 `Aula América A1` 命名，以降低既有工作流变化；内容来源已在 README 与各 content 文件中明确区分。
- 本次不在分发包中生成 MP3 或 `.apkg`；用户本地运行 `build_deck.command` 后，Builder 会复用旧 `audio_cache` 并仅为新增西语文本生成缺失音频。

### card counts

- chunk_production: 92
- dialogue_response: 38
- vocabulary: 223
- grammar_pattern: 39
- rule_concept: 46
- mistake_contrast: 42
- pronunciation: 4
- total: 484

## 0.3.3

- 在 Unidad 3 收口后按 Travel Core 逐步释放原则新增 22 张高频旅行词汇卡，使本轮与 v0.3.2 新增的 18 张 Unidad 3 卡合计正好 40 张新卡。
- 本批不追求教材词表覆盖，而按当前已掌握的 `ser / estar / hay / tener`、地点表达和酒店/城市场景筛选能立即理解和使用的词。
- 新增建筑与出入口：`la entrada / la salida / la puerta / el ascensor / la escalera`。
- 新增交通与导航：`la parada / el metro / el mapa / la dirección / la izquierda / la derecha / la esquina`。
- 新增支付与城市生活：`la tarjeta / el efectivo / el dinero / el mercado / el supermercado`。
- 新增旅行状态词：`abierto/-a / cerrado/-a / gratis / ocupado/-a / disponible`。
- 例句尽量只调用已经学过的语法；少量必要的新搭配（如 `a la izquierda / en efectivo / con tarjeta`）作为完整高频句块直接提供。
- 加入有意义的构词/词族提示：`salir → la salida`、`super- + mercado → supermercado`；不机械拆解其他词。
- `el ascensor` 标注墨西哥常见 `el elevador`，继续以广泛拉美可理解表达为默认。
- 不生成 MP3 或 `.apkg`；继续由用户本地使用自己的 API key 生成缺失音频。
- 保持既有 UID、deck ID、Note Type model ID、字段顺序、模板和 TTS 配置不变。

### card counts

- chunk_production: 86
- dialogue_response: 29
- vocabulary: 151
- grammar_pattern: 28
- rule_concept: 31
- mistake_contrast: 34
- pronunciation: 4
- total: 363

## 0.3.2

- Unidad 3 正式收口，在 v0.3.1 基础上新增 18 张高价值卡；不把文化听力中的偶发低频词机械制卡。
- 补齐教材明确要求但此前未单独覆盖的 `unos / unas` 与 `cuáles`。Aula América 的 Unidad 3 语法总结明确列出不定冠词复数、`cuál / cuáles`、天气与最高级。
- 新增旅行/地理高频方位词 `el norte / el sur / el este / el oeste`，以及 `la lengua`、`tropical`、`seco/-a`。
- 新增 `tener` vs `hay` 的信息视角：主体“具有” vs 某处“存在”，并用 hotel/gimnasio 与英语 has / there is 对照。
- 把 `nevar → nieva (e→ie)` 与 `llover → llueve (o→ue)` 接回 Unidad 2 已学的词干变化母规则；不要求背完整天气动词人称表。
- 新增 `¿dónde?` vs `donde`、地点块前置语序，以及 `pueblo → pueblito` 的 `-ito/-ita` 构词提示。
- 根据本轮真实错误新增 `de el → del`、最高级比较范围 `de`、`hay + 定冠词`、`en todo el país` vs `del país` 四张易错卡。
- 在既有 `el pueblo`、`el idioma`、`llover`、`nevar` 词汇卡的说明中加入有意义的构词/关联提示，不修改 Note Type 字段或模板。
- 不生成 MP3 或 `.apkg`；继续保留 Cedar TTS 配置，由用户本地使用自己的 API key 生成新增缺失音频。
- 保持既有 UID、deck ID、Note Type model ID、字段顺序、模板和 TTS 配置不变。

### card counts

- chunk_production: 86
- dialogue_response: 29
- vocabulary: 129
- grammar_pattern: 28
- rule_concept: 31
- mistake_contrast: 34
- pronunciation: 4
- total: 341

## 0.3.1

- 新增 Unidad 3 第二批 39 张卡，继续沿用“基础词汇 → 规则理解 → 语法模式 → 高频句块 → 问答情景 → 易错综合”的依赖顺序。
- 补充位置句块 `al lado de / delante de / detrás de / entre`，以及 `río / montaña / lago / mar / isla / costa / desierto` 等地理核心词。
- 补充天气系统：`viento / nube / nublado / templado / llover / nevar`，并建立 `hace + 名词 / estar + 状态 / 天气动词 / el clima + ser` 的统一理解框架。
- 新增最高级与比较范围：`el/la/los/las + más + adjetivo + de...`、上下文明确时省略名词、`en` 表位置与 `de` 表比较范围。
- 继续强化 `Hay + 新出现的东西 + 位置`，把本轮真实出现的 `Hay un museo está...` 和缺少 `estar` 的错误加入易错辨析。
- 加入 `una de las montañas`，并把 `piso` 作为 Travel Core 词汇保留；考虑到楼层编号存在地区与建筑习惯差异，不把“二楼 = segundo piso”固化成主动输出卡。
- 加入本轮真实错误：形容词复数配合 `interesantes`、`mucho viento`、`nieve → nieva`；错误句继续不生成音频。
- 不生成 MP3 或 `.apkg`；保留现有 Cedar TTS 配置，用户在本地使用自己的 API key 生成新增缺失音频。
- 保持既有 UID、deck ID、Note Type model ID、字段顺序、模板和 TTS 配置不变。

### card counts

- chunk_production: 86
- dialogue_response: 29
- vocabulary: 122
- grammar_pattern: 26
- rule_concept: 26
- mistake_contrast: 30
- pronunciation: 4
- total: 323

## 0.3.0

- 新增 Unidad 3 第一批 27 张卡，覆盖城市与天气词汇、`ser / estar / hay`、新旧信息流、`muy / mucho`、位置句块和疑问词。
- 复用 Unidad 2 已有的 `el país`、`el hotel`、`el restaurante`、`el centro`、`el museo`、`la gente`、`aquí` 等前置词，避免重复卡。
- 把用户真实出现的 `en cerca` 错误纳入易错辨析，并强化 `hay` 与 `estar` 的信息功能差异。
- 疑问词卡避免宽泛枚举，优先使用单一、明确、有语境的提取任务。
- 保持既有 UID、deck ID、Note Type ID、字段顺序、模板和 TTS 配置不变。

## 0.2.3

- 新增 39 张 Unidad 2 基础/Travel Core 词汇卡。
- 新卡按依赖顺序组织：词汇 → 发音 → 规则 → 语法 → 句块 → 问答 → 易错综合。
- 名词默认连冠词学习；补齐 salir/viaje/noche/compras/bailar/playa/cine/amigo 等前置词。
- Travel Core 覆盖交通、证件/行李、酒店、餐厅、城市地点；正确例句继续纳入 TTS。
- 保持既有 UID、deck ID、Note Type ID 和字段不变。


## 0.2.2

### audio

- 将“每个西语例句都应有发音”设为卡组固定规则。
- `vocabulary` 的 `ExampleES`、`rule_concept` 的 `ExampleES`、对话问答、主动表达等原本已有 TTS，继续保留。
- 为 `grammar_pattern` 的 `ContrastES` 增加 TTS 生成与播放，因此语法卡中显示的正确对比例句/形式也可直接听发音。
- `mistake_contrast` 中的错误句 `WrongES` 继续不生成音频，避免把错误形式作为模仿输入；正确句 `CorrectES` 仍有音频。
- 不改变 deck ID、Note Type model ID、字段顺序、模板数量或既有 UID；无需做 Note Type 迁移。
- 本次未生成音频或 `.apkg`；本地构建时会只为新增纳入 TTS 的文本生成缺失音频。

## 0.2.1

### vocabulary

- 在 Unidad 2 完成语法与句块收口后，新增 25 张基础词汇补强卡，使表达能力与词汇增长同步推进
- 新增课堂/教材导航词：`actividad`、`clase`、`compañero/-a`、`curso`、`ejercicio`、`gramática`、`pronunciación`、`información`
- 新增基础时间与地点词：`año`、`mes`、`semana`、`fin de semana`、`país`、`pueblo`、`aquí`
- 新增旅行、媒体和生活词：`precio`、`canción`、`película`、`periódico`、`revista`、`excursión`
- 新增高频动词：`buscar`、`cenar`、`mejorar`、`comprar`，并用已学 `querer + infinitivo` 等结构提供例句
- 词汇筛选以 Aula Internacional 1 单词表的 Unidad 2 覆盖检查为参考，同时以 Aula América 1 主线与旅行/日常实用性为优先，不追求把文化阅读中的偶发低频词全部制卡
- 保留 deck ID、Note Type model ID、字段顺序、模板、样式、既有 UID 和 TTS 配置
- 本次未生成新音频或 `.apkg`；本地构建时仅需生成新增西语文本的缺失音频

### card counts

- chunk_production: 76
- dialogue_response: 25
- vocabulary: 57
- grammar_pattern: 18
- rule_concept: 16
- mistake_contrast: 22
- pronunciation: 4
- total: 218

## 0.2.0

### content

- 新增完整 `content/unidad_02.json`，覆盖 Unidad 2 的核心交际目标、语法、介词搭配、语言能力与休闲活动
- 强化 `querer + infinitivo`，并针对主动输出中真实出现的 `Quiero hablo...`、`Queremos comemos...` 等错误加入易错辨析卡
- 加入规则现在时 `-ar / -er / -ir` 的拉美五人称模式，以及 `querer`、`entender` 的 `e → ie` 词干变化理解
- 加入 `porque / para / por`、`viajar a / por`、`hablar con`、personal `a`、`a + el → al` 等 Unidad 2 介词重点
- 加入语言能力表达：`hablar / escuchar / entender / leer` 与 `bien / bastante bien / un poco / regular / mal / nada de`
- 加入定冠词 `el / la / los / las`、`el idioma`、`la gente`、`el aula / las aulas` 等关键例外
- 加入 `querer a + persona` 的感情义，并保留中性拉美西语的现有 TTS 配置
- 不新增独立发音卡：Unidad 2 未引入需要脱离现有发音系统单独记忆的新音位规则；相关语流继续由现有发音课程与 TTS 覆盖
- 保留既有 deck ID、Note Type model ID、字段顺序、模板、样式、UID 与 TTS 配置
- 本次未生成新音频或 `.apkg`；本地构建时只需为新增文本生成缺失音频

### unidad 2 card counts

- chunk_production: 27
- dialogue_response: 8
- vocabulary: 7
- grammar_pattern: 10
- rule_concept: 9
- mistake_contrast: 9
- pronunciation: 0
- total: 70

## 0.1.5

### tts

- 将全局语音风格改为正常、清晰的自然会话速度，并明确要求保留西语的自然连读与重新分节
- 明确要求把所有输入按西班牙语发音，即使拼写与英语单词相同
- 为 `once` 加入单条覆盖提示，指定其为西语数字 11，避免读成英语 `once`
- 为 `¿Quién es?` 加入单条覆盖提示，要求两词自然连接，不在中间加入人为停顿
- 构建脚本新增 `text_instruction_overrides` 支持；单条提示会进入缓存哈希，后续可只重生成受影响的音频
- 本次未生成音频或 `.apkg`；请运行 `refresh_audio.command` 重新生成全部语音

## 0.1.4

### content

- 完成 Unidad 1 补遗：`nombre / apellido`、`tú / usted`、`tu / su`
- 加入 `¿En qué trabajas?`、`Trabajo como…`、`Trabajo en…` 的职业表达
- 补充 `nosotros / ustedes / ellos / ellas` 及复数人称形式
- 明确 `¿Quién es?` 与 `¿Cómo se llama?` 的使用场景差异
- 加入正式称呼 `señor / señora + apellido`、三类动词原形及新增易错辨析
- 加入 `ustedes`、`rt / tr / dr` 的个性化发音卡
- 修订原有 `¿Quién es?` 卡片的语用说明
- 保留现有 UID、Note Type、deck ID、model ID、字段顺序、模板、样式与 OpenAI TTS 配置
- 本次未生成新音频或 `.apkg`；本地构建时仅生成缺失音频

### card counts

- chunk_production: 49
- dialogue_response: 17
- vocabulary: 25
- grammar_pattern: 8
- rule_concept: 7
- mistake_contrast: 13
- pronunciation: 4
- total: 123

## 0.1.3

### content

- 补齐 Unidad 1 的问候、告别、课堂求助、拼写、联系方式和第三人称问答
- 加入 0–15 与整十数字的基础词汇卡，以及 16–99 的构词规则卡
- 加入 `ser`、`tener`、`llamarse` 的实际人称转换卡
- 加入阴阳性、主语省略和疑问词重音规则卡
- 加入用户真实错误形成的易错辨析卡
- 加入字母 `c` 与 `g` 的发音听辨卡
- 保留 OpenAI `gpt-4o-mini-tts`、`cedar`、中性拉美西语和现有缓存规则

### card counts

- chunk_production: 37
- dialogue_response: 13
- vocabulary: 25
- grammar_pattern: 6
- rule_concept: 3
- mistake_contrast: 9
- pronunciation: 2
- total: 95

## 0.1.2

### fixed

- 验证器忽略 `venv`、`audio_cache`、`output`、`release` 和其他生成目录
- 构建时不再检查第三方 Python 包的文件名
- 验证失败时显示简洁提示，不再抛出 `CalledProcessError` traceback

## 0.1.1

### fixed

- 验证器忽略 `.DS_Store`、`.keep` 以及其他隐藏文件
- 隐藏的操作系统元数据不再导致验证失败
- 文件命名规则仍适用于所有正式项目文件


## 0.1.0

### added

- 建立长期维护的仓库结构
- 冻结七种 Note Type
- 加入 Note Type 契约哈希
- 加入 UID、字段、问号、文件名自动验证
- 加入 GitHub 安全上传目录生成器
- 加入累积 release 目录
- 加入所有七种卡片类型的样式预览

### preserved

- 保留原有 deck ID
- 保留三种已有 Note Type 的 model ID
- 保留三种已有 Note Type 的字段顺序
- 保留 21 张现有卡的 UID
- 保留 cedar、中性拉美西语和当前语速
- 保留旧音频缓存哈希规则

### content

- chunk_production: 14
- dialogue_response: 4
- mistake_contrast: 3
- total: 21
