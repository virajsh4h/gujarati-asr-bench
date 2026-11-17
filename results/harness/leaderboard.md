# Gujarati ASR leaderboard

Corpus CER over fleurs, indicvoices, kathbath. Intervals are 95% bootstrap over utterances (2000 resamples, seed 0).

## Three-dataset macro

| # | Model | Macro CER | 95% CI | Macro WER | N |
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

## Per dataset

| Model | Dataset | N | CER | 95% CI | WER | Drift % | Loop % | RTF |
|---|---|---|---|---|---|---|---|---|
| gemma-4-E4B-ctx | fleurs | 1000/1000 | 5.78 | 5.45–6.12 | 19.93 | 0.0 | 0.0 | 0.0173 |
| gemma-4-E4B-ctx | indicvoices | 2968/2968 | 8.97 | 8.53–9.45 | 22.85 | 0.0 | 0.2 | 0.0211 |
| gemma-4-E4B-ctx | kathbath | 2905/2905 | 4.30 | 4.15–4.46 | 17.29 | 0.0 | 0.0 | 0.0168 |
| gemma-4-E4B-grpo | fleurs | 1000/1000 | 5.59 | 5.28–5.91 | 19.08 | 0.0 | 0.0 | 0.0160 |
| gemma-4-E4B-grpo | indicvoices | 2967/2968 | 9.09 | 8.76–9.45 | 23.54 | 0.0 | 0.3 | 0.0182 |
| gemma-4-E4B-grpo | kathbath | 2905/2905 | 4.38 | 4.21–4.54 | 17.30 | 0.0 | 0.0 | 0.0147 |
| gemma-4-E4B-it | fleurs | 1000/1000 | 7.77 | 7.24–8.41 | 24.68 | 3.7 | 0.1 | 0.0455 |
| gemma-4-E4B-it | indicvoices | 2968/2968 | 16.59 | 15.92–17.34 | 35.91 | 3.6 | 0.7 | 0.0500 |
| gemma-4-E4B-it | kathbath | 2905/2905 | 7.77 | 7.29–8.40 | 25.81 | 4.6 | 0.1 | 0.0462 |
| gemma-4-E4B-sft | fleurs | 1000/1000 | 5.63 | 5.31–5.97 | 19.22 | 0.0 | 0.0 | 0.0159 |
| gemma-4-E4B-sft | indicvoices | 2968/2968 | 9.27 | 8.90–9.63 | 23.93 | 0.0 | 0.3 | 0.0180 |
| gemma-4-E4B-sft | kathbath | 2905/2905 | 4.41 | 4.25–4.57 | 17.52 | 0.0 | 0.0 | 0.0146 |
| gemma-4-E4B-step5 | fleurs | 1000/1000 | 7.35 | 6.99–7.73 | 24.14 | 0.4 | 0.0 | 0.0275 |
| gemma-4-E4B-step5 | indicvoices | 2968/2968 | 15.90 | 15.29–16.56 | 35.25 | 0.1 | 0.1 | 0.0301 |
| gemma-4-E4B-step5 | kathbath | 2905/2905 | 6.79 | 6.58–7.00 | 24.35 | 0.3 | 0.0 | 0.0252 |
| indic-transcribe-core | fleurs | 1000/1000 | 5.01 | 4.58–5.48 | 15.87 | 0.0 | 0.0 | 0.0775 |
| indic-transcribe-core | indicvoices | 2968/2968 | 5.36 | 5.12–5.62 | 15.88 | 0.0 | 0.8 | 0.0760 |
| indic-transcribe-core | kathbath | 2905/2905 | 2.41 | 2.30–2.51 | 12.00 | 0.0 | 0.0 | 0.0810 |
| sravaani-1.0 | fleurs | 1000/1000 | 5.37 | 4.96–5.83 | 17.36 | 0.0 | 0.0 | 0.0078 |
| sravaani-1.0 | indicvoices | 2968/2968 | 7.31 | 6.98–7.66 | 20.95 | 17.3 | 1.0 | 0.0065 |
| sravaani-1.0 | kathbath | 2905/2905 | 2.67 | 2.55–2.78 | 12.73 | 0.1 | 0.0 | 0.0063 |
| whisper-gujarati-small | fleurs | 1000/1000 | 10.92 | 10.02–11.85 | 27.75 | 0.0 | 0.0 | 0.0109 |
| whisper-gujarati-small | indicvoices | 2968/2968 | 36.23 | 35.13–37.35 | 50.09 | 0.0 | 8.5 | 0.0111 |
| whisper-gujarati-small | kathbath | 2905/2905 | 9.48 | 8.94–10.06 | 26.33 | 0.0 | 0.1 | 0.0122 |
| whisper-small | fleurs | 1000/1000 | 102.43 | 99.13–105.87 | 258.29 | 98.3 | 15.9 | 0.0120 |
| whisper-small | indicvoices | 2968/2968 | 149.52 | 143.68–155.74 | 313.38 | 98.0 | 29.0 | 0.0184 |
| whisper-small | kathbath | 2905/2905 | 106.62 | 103.61–109.72 | 268.38 | 99.9 | 6.9 | 0.0196 |

## Paired against `bodhan`

| Model | Dataset | Δ CER | 95% CI | p | Significant |
|---|---|---|---|---|---|
| gemma-4-E4B-it | fleurs | 2.7514 | 2.1563–3.4225 | <0.001 | yes |
| gemma-4-E4B-ctx | fleurs | 0.7623 | 0.4267–1.0621 | <0.001 | yes |
| gemma-4-E4B-grpo | fleurs | 0.5732 | 0.1838–0.9167 | 0.004 | yes |
| gemma-4-E4B-sft | fleurs | 0.6197 | 0.2367–0.9535 | 0.001 | yes |
| gemma-4-E4B-step5 | fleurs | 2.3374 | 1.8993–2.7781 | <0.001 | yes |
| sravaani-1.0 | fleurs | 0.353 | 0.2506–0.4571 | <0.001 | yes |
| whisper-small | fleurs | 97.4189 | 94.1137–100.8343 | <0.001 | yes |
| whisper-gujarati-small | fleurs | 5.9064 | 4.9823–6.8374 | <0.001 | yes |
| gemma-4-E4B-it | indicvoices | 11.2333 | 10.6274–11.9412 | <0.001 | yes |
| gemma-4-E4B-ctx | indicvoices | 3.6123 | 3.2673–3.9848 | <0.001 | yes |
| gemma-4-E4B-grpo | indicvoices | 3.7324 | 3.5014–3.981 | <0.001 | yes |
| gemma-4-E4B-sft | indicvoices | 3.9088 | 3.6658–4.1416 | <0.001 | yes |
| gemma-4-E4B-step5 | indicvoices | 10.538 | 9.9911–11.1125 | <0.001 | yes |
| sravaani-1.0 | indicvoices | 1.9507 | 1.7468–2.1681 | <0.001 | yes |
| whisper-small | indicvoices | 144.1536 | 138.3672–150.4187 | <0.001 | yes |
| whisper-gujarati-small | indicvoices | 30.8712 | 29.882–31.8742 | <0.001 | yes |
| gemma-4-E4B-it | kathbath | 5.3623 | 4.9059–5.9666 | <0.001 | yes |
| gemma-4-E4B-ctx | kathbath | 1.8894 | 1.7692–2.0128 | <0.001 | yes |
| gemma-4-E4B-grpo | kathbath | 1.9678 | 1.8389–2.0965 | <0.001 | yes |
| gemma-4-E4B-sft | kathbath | 1.9986 | 1.8735–2.1225 | <0.001 | yes |
| gemma-4-E4B-step5 | kathbath | 4.3774 | 4.2013–4.5722 | <0.001 | yes |
| sravaani-1.0 | kathbath | 0.2596 | 0.1724–0.3503 | <0.001 | yes |
| whisper-small | kathbath | 104.2092 | 101.1847–107.3437 | <0.001 | yes |
| whisper-gujarati-small | kathbath | 7.0706 | 6.5295–7.6532 | <0.001 | yes |

Positive Δ means the model is worse than the reference on the same utterances.
