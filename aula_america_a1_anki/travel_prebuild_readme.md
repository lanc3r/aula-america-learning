# anki_v0_7_3_source_repo

This repository is a travel prebuild extension of `anki_v046`.

It preserves the original cumulative source deck through v0.4.6 and adds
prebuilt travel packages for NVH U6-U9:

- `anki_v047_nvh_u6_prebuild`
- `anki_v048_nvh_u7_prebuild`
- `anki_v049_nvh_u8_mirador_review`
- `anki_v050_nvh_u9_prebuild`
- `anki_v048_v050_nvh_travel_pack`

## Version Order

Historical direct-import packages used this order:

1. Existing cumulative deck from v0.4.6
2. `anki_v047_nvh_u6_prebuild.apkg`
3. `anki_v048_nvh_u7_prebuild.apkg`
4. `anki_v049_nvh_u8_mirador_review.apkg`
5. `anki_v050_nvh_u9_prebuild.apkg`

Alternatively, after importing v047, import:

`anki_v048_v050_nvh_travel_pack.apkg`

Do not import both the separate v048-v050 APKG files and the combined
v048-v050 APKG into the same Anki profile.

The cleaned source repository keeps the TSV source inputs only. APKGs,
manifests, and bundle ZIPs are generated artifacts and should be rebuilt when
needed rather than committed.

## Repository Layout

- `content/`: original cumulative source JSON through v0.4.6.
- `scripts/build_deck.py`: original cumulative deck builder.
- `scripts/build_travel_prebuild.py`: travel prebuild generator used for v048-v050.
- `prebuilds/v047/`: uploaded U6 TSV baseline, included for ordering and dedupe.
- `prebuilds/v048_v050/`: generated v048-v050 TSV source inputs.

## Dedupe Rule

The v048-v050 generator uses
`prebuilds/v047/anki_v047_nvh_u6_prebuild.tsv` as its hard dedupe baseline.
New cards whose normalized `front` or `back` exactly matched v047 were skipped.

Final cross-check:

- v048 vs v047 exact front/back overlaps: 0
- v049 vs v047 exact front/back overlaps: 0
- v050 vs v047 exact front/back overlaps: 0
- combined v048-v050 vs v047 exact front/back overlaps: 0

## Counts

| Package | Notes/Cards |
| --- | ---: |
| `anki_v047_nvh_u6_prebuild` | 146 |
| `anki_v048_nvh_u7_prebuild` | 133 |
| `anki_v049_nvh_u8_mirador_review` | 64 |
| `anki_v050_nvh_u9_prebuild` | 157 |
| `anki_v048_v050_nvh_travel_pack` | 354 |

## Scope

The travel prebuilds are ordered by future lesson blocks:

1. Basic vocabulary
2. Core structures
3. High-frequency collocations
4. Complete chunks
5. Scenario Q&A
6. Error contrasts
7. Short output prompts

The content combines NVH core material, Aula America alignment, Latin America
travel upgrades, and U5-U7/U6-U7 review bridges. U8 is a Mirador review unit
and is intentionally lighter than the new-content units.


## Repository integration fix

This repository now includes the travel prebuild content as first-class source data:

- `content/unidad_nvh_06.json` integrates `anki_v047_nvh_u6_prebuild` in order after U5.
- `content/unidad_nvh_07.json` integrates `anki_v048_nvh_u7_prebuild`.
- `content/unidad_nvh_08.json` integrates `anki_v049_nvh_u8_mirador_review`.
- `content/unidad_nvh_09.json` integrates `anki_v050_nvh_u9_prebuild`.

Run `build_deck.command` from the repository root. The normal v046 build pipeline will read `content/unidad_*.json`, collect Spanish audio fields, prompt for an OpenAI API key when audio is missing, generate audio into `audio_cache/`, and build `release/aula_america_a1_v0_5_0.apkg`.

Validation status after integration: `scripts/validate_content.py` passes with 1341 total notes. Current scratch cache has 1693 missing audio texts, so the next full build should enter audio generation.
