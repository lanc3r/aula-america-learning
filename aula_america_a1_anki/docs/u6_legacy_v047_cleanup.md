# U6 legacy v047 cleanup

This note records legacy cards that may still exist in Anki after importing the
original `anki_v047_nvh_u6_prebuild` package. They are not part of the active
content.

## Legacy pseudo-paragraph cards

The original v047 TSV contained seven `production salida` rows that used
`小段落：` as a label but each tested only one sentence. These should be deleted
or suspended in Anki if they appear during review.

| TSV row | Search text | Spanish | Current status |
| --- | --- | --- | --- |
| 127 | `小段落：我的酒店在市中心。` | `Mi hotel está en el centro.` | Remove legacy card; low-value isolated sentence. |
| 128 | `小段落：酒店附近有一家药店。` | `Hay una farmacia cerca del hotel.` | Remove legacy card; covered by nearby `hay + cerca del hotel` question work. |
| 129 | `小段落：药店在酒店对面。` | `La farmacia está enfrente del hotel.` | Remove legacy card; exact sentence exists as a normal location card. |
| 130 | `小段落：我想去博物馆。` | `Quiero ir al museo.` | Remove legacy card; covered by `ir al museo` and route-question cards. |
| 131 | `小段落：我坐 3 号线，往历史中心方向。` | `Tomo la línea 3 en dirección al centro histórico.` | Remove legacy card; covered by route-recap and staff-direction cards. |
| 132 | `小段落：我在 Alameda 站下车。` | `Bajo en la estación Alameda.` | Remove legacy card; exact sentence exists as a normal route-recap card. |
| 133 | `小段落：博物馆步行五分钟。` | `El museo está a cinco minutos a pie.` | Remove legacy card; exact sentence exists as a normal location/time card. |

## Anki browse searches

Use these searches in Anki Browse if old v047 cards still appear:

```text
tag:nvh_u6 tag:production tag:salida
小段落
Quiero ir al museo
Hay una farmacia cerca del hotel
Tomo la línea 3 en dirección al centro histórico
```

## Current rule

Do not keep single-sentence cards whose only purpose is to be part of a fake
paragraph. If a paragraph task is useful for class, keep it as a speaking prompt
outside normal Anki review. Active Anki cards should train individual missing
targets, compact 2-3 sentence outputs, or real situational responses.

Also apply the natural-expression gate before adding or keeping any active
production card. A Spanish answer that is merely understandable is not enough:
it should be the kind of wording a real speaker would naturally use in the
intended travel or daily-life situation. If the phrase feels like translated
Chinese or English, either replace it with a natural sentence, downgrade it to
recognition, or leave it out.

## Retired duplicate future-prebuild cards

The original v047 TSV also contained U6 future-prebuild cards for bare phrases
that were already covered by earlier units. They are retired in active content.

`ir de compras` is already covered by U2:

- `AA1-U02-L01-P007`: `Quiero ir de compras.`
- `AA1-U02-L00-V004`: `las compras`, with the example `Quiero ir de compras.`

`ir al teatro` is already covered by U4:

- `NVH-U04-LX-V066`: `el teatro`, with the example `Me gusta el teatro.`

`desayunar en un café típico` was also retired. It is understandable but not
the preferred travel output; `desayunar en una cafetería local` or `desayunar
en un café tradicional` is more natural if this meaning is needed. The component
targets are already covered by earlier cards for `desayunar`, `típico/a`, and
`el café` / `la cafetería`. This is the model example for the natural-expression
gate: do not keep a card simply because the literal Spanish can be understood.

`Prefiero conocer dos lugares` was retired because it does not match the Chinese
prompt `我最想了解两个地方。` closely enough. `Prefiero...` means "I prefer / I
would rather...", not "what I most want to...". If this classroom task is needed
later, use a natural contextual sentence such as `Quiero conocer dos lugares en
particular.` or `Me interesa conocer dos lugares sobre todo.`

If the old U6 cards appear in Anki, delete or suspend them:

```text
ir de compras
ir al teatro
desayunar en un café típico
Prefiero conocer dos lugares
```

## Retired duplicate U6 vocabulary

The following U6 vocabulary cards were retired because the same standalone word
was already covered before U6. Keep the earlier card and use U6 only for new
route, transport, and city-function targets.

| Retired UID | Spanish | Earlier coverage |
| --- | --- | --- |
| `NVH-U6-L01-V001` | `la farmacia` | `AA1-U02-L00-V038` |
| `NVH-U6-L01-V002` | `el hotel` | `AA1-U02-L00-V019` |
| `NVH-U6-L01-V003` | `el museo` | `AA1-U02-L00-V036` |
| `NVH-U6-L01-V004` | `la plaza` | `AA1-U02-L00-V035` |
| `NVH-U6-L01-V009` | `el café` | `NVH-U05-L05-V042` |
| `NVH-U6-L01-V010` | `el banco` | `AA1-U02-L00-V039` |
| `NVH-U6-L01-V011` | `el centro` | `AA1-U02-L00-V034` |
| `NVH-U6-L01-V013` | `la calle` | `AA1-U02-L00-V033` |
| `NVH-U6-L01-V016` | `la parada` | `AA1-U03-TC-V006` |
| `NVH-U6-L01-V017` | `la estación` | `AA1-U02-L00-V010` |
| `NVH-U6-L01-V019` | `el autobús` | `AA1-U02-L00-V014` |
| `NVH-U6-L01-V020` | `el metro` | `AA1-U03-TC-V007` |
| `NVH-U6-L01-V021` | `el taxi` | `AA1-U02-L00-V015` |
| `NVH-U6-L01-V023` | `la entrada` | `AA1-U03-TC-V001` |
| `NVH-U6-L01-V024` | `el boleto` | `AA1-U02-L00-V011` |

The active U6 standalone vocabulary is limited to U6-specific gaps:

```text
la catedral
la oficina de turismo
la estación de metro
la cafetería
el centro histórico
el semáforo
el puente
la línea
el plano de la ciudad
```
