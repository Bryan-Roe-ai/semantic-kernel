#!/usr/bin/env python3
"""
AI module for main

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import List
from pydantic import BaseModel

from fastapi import FastAPI
from evaluate import load
from comet import download_model, load_from_checkpoint

app = FastAPI()


class SummarizationEvaluationRequest(BaseModel):
    sources: List[str]
    summaries: List[str]


class TranslationEvaluationRequest(BaseModel):
    sources: List[str]
    translations: List[str]


@app.post("/bert-score/")
def bert_score(request: SummarizationEvaluationRequest):
    bertscore = load("bertscore")
    return bertscore.compute(
        predictions=request.summaries, references=request.sources, lang="en"
    )


@app.post("/meteor-score/")
def meteor_score(request: SummarizationEvaluationRequest):
    meteor = load("meteor")
    return meteor.compute(predictions=request.summaries, references=request.sources)


@app.post("/bleu-score/")
def bleu_score(request: SummarizationEvaluationRequest):
    bleu = load("bleu")
    return bleu.compute(predictions=request.summaries, references=request.sources)


@app.post("/comet-score/")
def comet_score(request: TranslationEvaluationRequest):
    model_path = download_model("Unbabel/wmt22-cometkiwi-da")
    model = load_from_checkpoint(model_path)
    data = [
        {"src": src, "mt": mt} for src, mt in zip(request.sources, request.translations)
    ]
    return model.predict(data, accelerator="cpu")
