---
license: cc-by-4.0
task_categories:
  - automatic-speech-recognition
language:
  - gu
pretty_name: Gujarati ASR leaderboard
tags:
  - asr
  - gujarati
  - benchmark
  - evaluation
---

# Gujarati ASR, with error bars

Nine systems. 6,873 utterances. Three public benchmarks. Same audio for every model.

Every number is a corpus CER with a 95% interval over utterances, and every "this beats that" is a
paired bootstrap on identical samples.

**Best on this benchmark: `indic-transcribe-core`, 4.26% macro CER (95% CI 4.09–4.44).**

| # | Model | Macro CER | 95% CI | Macro WER |
|---|---|---|---|---|
| 1 | indic-transcribe-core | 4.26 | 4.09–4.44 | 14.58 |
| 2 | sravaani-1.0 | 5.12 | 4.94–5.30 | 17.01 |
| 3 | gemma-4-E4B-ctx | 6.35 | 6.16–6.55 | 20.02 |
| 4 | gemma-4-E4B-grpo | 6.35 | 6.18–6.52 | 19.97 |
| 5 | gemma-4-E4B-sft | 6.44 | 6.27–6.61 | 20.22 |
| 6 | gemma-4-E4B-step5 | 10.01 | 9.77–10.27 | 27.92 |
| 7 | gemma-4-E4B-it | 10.71 | 10.37–11.08 | 28.80 |
| 8 | whisper-gujarati-small | 18.88 | 18.38–19.39 | 34.72 |
| 9 | whisper-small | 119.52 | 117.21–122.05 | 280.02 |

## Datasets

| Dataset | Split | Utterances | Audio |
|---|---|---|---|
| `google/fleurs` (`gu_in`) | test | 1,000 | read speech, FLoRes sentences |
| `ai4bharat/IndicVoices` (`gujarati`) | valid | 2,968 | spontaneous, crowd-sourced, varied mics |
| `ai4bharat/Kathbath` (`gujarati`) | valid | 2,905 | narrative and conversational prompts |

Revisions are pinned. Two IndicVoices rows are filtered by the loader (under 0.3 s or empty
transcript), so 2,968 of 2,970 raw rows are scored.

## Files

| File | Contents |
|---|---|
| `leaderboard.md` | macro table, per-dataset table, paired tests |
| `leaderboard.csv` | per model × dataset cells |
| `leaderboard.json` | full board including intervals and comparisons |
| `report.html` | rendered report |
| `predictions/*.csv` | per-utterance references, hypotheses, metrics, latency |

Anyone can recompute a number from `predictions/` instead of trusting the table.

## Notes

- Corpus CER is edit-weighted over characters, not a mean of sentence scores.
- Utterances that fail inference are stored with a tag and excluded from scoring, so coverage
  loss is visible instead of silently improving a score.
- Decoding is whatever each system ships with. Batch sizes differ. This is a systems comparison,
  not a compute-matched one.
- CER is a text metric. It does not measure whether a transcript is usable downstream.
- One seed. Intervals cover sampling of utterances, not run-to-run variance from batching or
  nondeterministic kernels.

Code and full write-up: https://github.com/virajsh4h/gujarati-asr-bench
