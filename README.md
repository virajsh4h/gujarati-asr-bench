# Gujarati ASR, with error bars

Most Gujarati ASR comparisons are a single number per model, on different splits, through different
normalisers. This is one split, one normaliser, one harness, and an interval on every number. I
built it to see where my own fine-tunes actually stand against the strongest open systems, on
identical audio.

Nine systems. 6,873 utterances. Three public benchmarks. Same audio for every model.

Every number below is a corpus CER with a 95% interval over utterances, and every "this beats
that" is a paired bootstrap on identical samples. Nothing here is a single-run headline.

**Best on this benchmark: indic-transcribe-core, 4.26% macro CER (95% CI 4.09–4.44).**

**My fine-tune of Gemma-4-E4B: 6.35% (6.16–6.55). 2.09 points behind the best system, and the
gap is real (p < 0.001).**

| # | Model | Macro CER | 95% CI | Macro WER | Utterances |
|---|---|---|---|---|---|
| 1 | indic-transcribe-core | 4.26 | 4.09–4.44 | 14.58 | 6873/6873 |
| 2 | sravaani-1.0 | 5.12 | 4.94–5.30 | 17.01 | 6873/6873 |
| 3 | gemma-4-E4B-ctx | 6.35 | 6.16–6.55 | 20.02 | 6873/6873 |
| 4 | gemma-4-E4B-grpo | 6.35 | 6.18–6.52 | 19.97 | 6872/6873 |
| 5 | gemma-4-E4B-sft | 6.44 | 6.27–6.61 | 20.22 | 6873/6873 |
| 6 | gemma-4-E4B-step5 | 10.01 | 9.77–10.27 | 27.92 | 6873/6873 |
| 7 | gemma-4-E4B-it | 10.71 | 10.37–11.08 | 28.80 | 6873/6873 |
| 8 | whisper-gujarati-small | 18.88 | 18.38–19.39 | 34.72 | 6873/6873 |
| 9 | whisper-small | 119.52 | 117.21–122.05 | 280.02 | 6873/6873 |

Per-dataset breakdown, RTF, script-drift and loop rates: [`results/harness/leaderboard.md`](results/harness/leaderboard.md).

## What is actually measured

| Dataset | Split | Utterances | What the audio is |
|---|---|---|---|
| FLEURS (`google/fleurs`, `gu_in`) | test | 1,000 | read speech, FLoRes sentences |
| IndicVoices (`ai4bharat/IndicVoices`) | valid | 2,968 | spontaneous, crowd-sourced, varied mics |
| Kathbath (`ai4bharat/Kathbath`) | valid | 2,905 | narrative and conversational prompts |

Revisions are pinned in `gujasr/manifests.py`. Two IndicVoices rows are dropped by the loader
(under 0.3 s or empty transcript), so the expected count is 2,968 from 2,970 raw.

All text goes through one normaliser: NFC, zero-width joiners stripped, Gujarati digits mapped
to ASCII, punctuation and underscore to space, whitespace collapsed, lowercased. Corpus CER is
edit-weighted, not a mean of sentence scores. Utterances that fail inference are stored with a
tag and excluded from scoring, so coverage loss is visible instead of silently improving a score.

## What the table says

**1. Top two are closer than the headline, and the gap still holds.** sravaani-1.0 is 0.86 points
behind on the macro, but only 0.35 on FLEURS, 0.26 on Kathbath, and 1.95 on IndicVoices. All three
differences survive the paired test. The 0.35 FLEURS number is exactly the kind that gets quoted as
"competitive" without saying which dataset.

**2. My own stage-2 gains are dataset-specific, and mostly small.** SFT to GRPO is −0.17 points on
IndicVoices (p < 0.001), −0.05 on FLEURS and −0.03 on Kathbath (neither significant). SFT to
context-injection is −0.11 on Kathbath (p = 0.002), −0.30 on IndicVoices (p = 0.07), and +0.14 on
FLEURS (p = 0.14). One dataset moving is not a method working.

**3. IndicVoices is where systems fall apart.** Every model is worse there than on the other two.
indic-transcribe-core goes 2.41 → 5.36. sravaani-1.0 goes 2.67 → 7.31 and inserts non-Gujarati
script in 17.3% of its output. Gemma-4-E4B-it goes 7.77 → 16.59. Read speech flatters every
system on this list.

**4. Whisper without a Gujarati tokenizer does not merely do badly, it loops.** whisper-small,
no fine-tune: 119.52% CER, non-Gujarati script in 98% of outputs, repetition loops in 15.9% of
FLEURS and 29.0% of IndicVoices. A CER above 100% is possible because the corpus denominator is
the reference length and the model emits far more characters than it heard.

**5. Throughput spans an order of magnitude.** indic-transcribe-core runs at RTF 0.078, sravaani
at 0.0065, the Gemma adapters between 0.015 and 0.021 on an A100 80GB. sravaani is 12× cheaper per
audio second than the best-scoring system and 0.86 points behind it on the metric — the trade is
real, not rhetorical.

## What this does not say

- These are 6,873 utterances of read, narrative and crowd-sourced speech. No telephone audio, no
  far-field recordings, no code-switching, no Gujarati-English mix. Numbers will move.
- Decoding is whatever each system ships with. Batch sizes differ, Gemma adapters cap at 8. This is
  a systems comparison, not a compute-matched one.
- CER is a text metric. It does not measure whether a transcript is usable for a downstream task.
- One seed. The bootstrap covers sampling of utterances, not run-to-run variance from batching or
  nondeterministic kernels.

## Reproduce

```bash
pip install -e ".[eval]"
python -m gujasr run --models bodhan sravaani whisper-gu whisper --datasets fleurs indicvoices kathbath
python -m gujasr report --out results/harness
python -m gujasr verify --db results/harness.sqlite
```

`requirements-lock.txt` pins the exact environment the table was produced in. `gujasr run` with
`bodhan`, `sravaani`, `whisper-gu`, `whisper` and `gemma4` re-runs five rows from public weights.
The four adapted Gemma stages are in the repo, but their checkpoints are not published, so those
rows come from the stored run.

CPU-only tests, no GPU, no model download:

```bash
pip install jiwer numpy pytest && pytest -q
```

## How the harness stays honest

| Mechanism | What it prevents |
|---|---|
| Run key = hash(model, dataset, scoring config, code sha, normaliser version) | resuming into rows produced by a different config |
| Bootstrap interval on every corpus rate | quoting a 0.1-point gap that is sampling noise |
| Paired bootstrap on identical utterances | comparing models that saw different samples |
| Failure rows stored with a tag | a crashed batch quietly raising the score |
| Coverage shown as n/expected in every table | a partial run ranked against a complete one |
| `gujasr verify` recomputes every row from raw text | drift between stored and current normaliser |

Model code is untouched. Every checkpoint still loads through `build_adapter()` in
`run_baselines_optimized.py`; the harness wraps it, it does not reimplement it. Those adapter and
training files are in this repo, unchanged.

## Reproduction check

I re-ran the four public models through the harness on the same pinned data: 27,492 utterances
across twelve model × dataset cells. Against the stored rows, corpus CER moved by at most 0.05
points.

| Model | FLEURS | IndicVoices | Kathbath |
|---|---|---|---|
| indic-transcribe-core | +0.02 | 0.00 | +0.01 |
| sravaani-1.0 | 0.00 | +0.01 | 0.00 |
| whisper-gujarati-small | 0.00 | 0.00 | 0.00 |
| whisper-small | −0.05 | 0.00 | 0.00 |

sravaani's adapter writes each batch to `/dev/shm`; 96 of its 6,873 reads failed there in the
re-run. The harness stored them as tagged failures and scored the remaining 6,777, so its coverage
is 2,936/2,968 on IndicVoices and 2,841/2,905 on Kathbath. CER on the scored rows did not move. A
dropped batch would have silently raised or lowered that number; here it is visible.

## Layout

```
gujasr/                     harness: config, manifests, metrics, store, runner, adapters, report, cli
tests/                      25 tests, CPU only
results/harness/            leaderboard.md, leaderboard.csv, leaderboard.json, report.html
configs/                    run configuration
scripts/                    huggingface upload
run_baselines_optimized.py  model adapters and decode paths, unchanged
gu_normalizer.py            text normaliser used for every row
step5_gemma_zero.py         constrained-decode stage
train_step6_sft.py          SFT adapter
train_step7_grpo.py         GRPO adapter
gemma4_ctx_adapter.py       context-injection adapter
```

Per-utterance predictions are published with the leaderboard so anyone can recompute a number
instead of trusting it.

## Licences

Code is MIT. Tables and predictions are CC BY 4.0, as are the three source datasets (FLEURS,
IndicVoices, Kathbath). No audio is redistributed; the prediction files contain references,
hypotheses and metrics only.
