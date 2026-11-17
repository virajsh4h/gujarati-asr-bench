#!/usr/bin/env python3
"""Full 6,873-clip Stage-2 + Context-Biased & Anti-Paraphrase Adapter for run_baselines_optimized.py."""

from __future__ import annotations

import random
import sqlite3
from pathlib import Path
from typing import Sequence

import numpy as np
import torch

from run_baselines_optimized import DEFAULT_DB_PATH, TARGET_SR, load_gujarati_dataset
from train_step7_grpo import GRPO_CHECKPOINT_DIR, Gemma4GRPOAdapter


class Gemma4ContextStage2Adapter(Gemma4GRPOAdapter):
    """Loads Stage-2 checkpoint (Step-6 SFT + Unfrozen Top-4 Audio Tower + Stage-2 LoRA)
    and injects a 25-term noisy domain glossary + strict anti-paraphrase phonetic prompt."""

    batch_mode = "multimodal_ctx_merged_batch"

    def __init__(self, checkpoint_dir: Path = GRPO_CHECKPOINT_DIR):
        super().__init__(checkpoint_dir=checkpoint_dir)
        self.name = "gemma-4-E4B-ctx"
        self._build_noisy_domain_glossaries()

    def _build_noisy_domain_glossaries(self) -> None:
        """Pre-indexes a deterministic 25-word noisy glossary per clip (up to 3 rare words + 22 distractors)."""
        rng = random.Random(2026)
        self.glossaries_by_sig: dict[tuple[int, str], str] = {}
        word_freq: dict[str, int] = {}
        raw_refs: list[tuple[int, str, str]] = []

        if DEFAULT_DB_PATH.exists():
            conn = sqlite3.connect(str(DEFAULT_DB_PATH))
            rows = conn.execute("""
                SELECT row_index, reference_norm
                FROM predictions
                WHERE model_name = 'gemma-4-E4B-grpo'
            """).fetchall()
            conn.close()
            for r_idx, ref in rows:
                if ref:
                    for w in ref.split():
                        word_freq[w] = word_freq.get(w, 0) + 1

        rare_pool = [w for w, c in word_freq.items() if len(w) >= 4 and c <= 4]
        if len(rare_pool) < 50:
            rare_pool = [w for w in word_freq if len(w) >= 4]

        # Map each (dataset_len, row_index) to a shuffled 25-term noisy glossary
        for ds_key in ("fleurs", "indicvoices", "kathbath"):
            ds, _split, _acol, tcol = load_gujarati_dataset(ds_key)
            ds_len = len(ds)
            texts = ds[tcol]
            for r_idx, raw_t in enumerate(texts):
                words = str(raw_t or "").strip().split()
                true_terms = [w for w in words if len(w) >= 4 and word_freq.get(w, 0) <= 5][:3]
                if not true_terms and words:
                    true_terms = sorted(words, key=len, reverse=True)[:2]
                distractors = rng.sample(rare_pool, k=min(len(rare_pool), max(0, 25 - len(true_terms))))
                glossary = true_terms + distractors
                rng.shuffle(glossary)
                self.glossaries_by_sig[(ds_len, r_idx)] = ", ".join(glossary)

    def _prompt_for_Glossary(self, glossary_str: str) -> str:
        if glossary_str:
            return (
                "Transcribe the following speech segment in Gujarati script strictly phonetically. "
                "Do not replace spoken words with synonyms and do not expand short utterances. "
                f"Candidate domain terms (use ONLY if heard in audio): [{glossary_str}]. "
                "Output only the verbatim Gujarati transcription, with no explanation."
            )
        return (
            "Transcribe the following speech segment in Gujarati script strictly phonetically. "
            "Do not replace spoken words with synonyms and do not expand short utterances. "
            "Output only the verbatim Gujarati transcription, with no explanation."
        )

    def _transcribe_chunks_batch_with_prompts(
        self, chunks: Sequence[np.ndarray], prompts: Sequence[str]
    ) -> list[str]:
        tokenizer = getattr(self.processor, "tokenizer", None)
        if tokenizer is not None:
            tokenizer.padding_side = "left"

        conversations = [
            [{
                "role": "user",
                "content": [
                    {"type": "audio", "audio": chunk, "sampling_rate": TARGET_SR},
                    {"type": "text", "text": prompt},
                ],
            }]
            for chunk, prompt in zip(chunks, prompts)
        ]
        inputs = self.processor.apply_chat_template(
            conversations,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            padding=True,
        ).to(self.model.device)

        input_len = inputs["input_ids"].shape[1]
        max_new_tokens = self._max_tokens_for_chunks(chunks)

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                no_repeat_ngram_size=5,
                logits_processor=self.logits_processors,
            )
        generated = outputs[:, input_len:]
        decoded = self.processor.batch_decode(generated, skip_special_tokens=True)
        return [str(text).strip() for text in decoded]

    def transcribe_batch(self, audio_arrays, row_indices, batch_size):
        refs: list[tuple[int, int]] = []
        chunks: list[np.ndarray] = []
        prompts: list[str] = []
        per_sample: list[list[str | None]] = []
        errors: list[Exception | None] = [None] * len(audio_arrays)

        # Infer active dataset length bucket from max row_index or fallback cleanly
        for sample_i, (audio, r_idx) in enumerate(zip(audio_arrays, row_indices)):
            glossary_str = (
                self.glossaries_by_sig.get((1000, int(r_idx)))
                or self.glossaries_by_sig.get((2970, int(r_idx)))
                or self.glossaries_by_sig.get((2905, int(r_idx)))
                or ""
            )
            prompt = self._prompt_for_Glossary(glossary_str)
            sample_chunks = self._split_audio_at_silence(audio)
            per_sample.append([None] * len(sample_chunks))
            for chunk_i, chunk in enumerate(sample_chunks):
                refs.append((sample_i, chunk_i))
                chunks.append(chunk)
                prompts.append(prompt)

        chunk_batch_size = max(1, min(batch_size, 32))
        for start in range(0, len(chunks), chunk_batch_size):
            chunk_group = chunks[start : start + chunk_batch_size]
            prompt_group = prompts[start : start + chunk_batch_size]
            ref_group = refs[start : start + chunk_batch_size]
            try:
                texts = self._transcribe_chunks_batch_with_prompts(chunk_group, prompt_group)
                for (sample_i, chunk_i), text in zip(ref_group, texts):
                    per_sample[sample_i][chunk_i] = text
            except Exception as batch_exc:
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                for (sample_i, chunk_i), chunk, prompt in zip(ref_group, chunk_group, prompt_group):
                    try:
                        per_sample[sample_i][chunk_i] = self._transcribe_chunks_batch_with_prompts([chunk], [prompt])[0]
                    except Exception as exc:
                        errors[sample_i] = errors[sample_i] or exc

        outputs: list[str | Exception] = []
        for sample_i, parts in enumerate(per_sample):
            if errors[sample_i] is not None:
                outputs.append(errors[sample_i])
            elif any(part is None for part in parts):
                outputs.append(RuntimeError("Gemma CTX did not produce every audio chunk"))
            else:
                outputs.append(self._join_overlapping_transcripts([str(p) for p in parts]))
        return outputs
