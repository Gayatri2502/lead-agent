"""Training pipeline: TF-IDF + Logistic Regression intent classifier.

The trained bundle is persisted per-user under models/<uid>/ and its metadata
(metrics, intents, version) is pushed to Firestore by the AI Training page.
"""
from __future__ import annotations

import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ..config import MODELS_DIR
from .datasets import build_dataset, dataset_stats


def _user_model_dir(uid: str) -> str:
    path = os.path.join(MODELS_DIR, uid)
    os.makedirs(path, exist_ok=True)
    return path


def model_path(uid: str) -> str:
    return os.path.join(_user_model_dir(uid), "intent_model.joblib")


def _build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True, ngram_range=(1, 2), min_df=1,
            sublinear_tf=True, strip_accents="unicode")),
        ("clf", LogisticRegression(max_iter=1000, C=8.0, solver="lbfgs")),
    ])


def train_receptionist(cfg: Dict[str, Any], uid: str) -> Dict[str, Any]:
    """Train (or retrain) the intent model from the current agent config."""
    started = time.time()
    samples = build_dataset(cfg)
    texts = [t for t, _ in samples]
    labels = [i for _, i in samples]

    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.25, random_state=42, stratify=labels)

    pipeline = _build_pipeline()
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    intents = sorted(set(labels))
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    matrix = confusion_matrix(y_test, predictions, labels=intents).tolist()
    accuracy = round(accuracy_score(y_test, predictions) * 100, 2)
    macro_f1 = round(f1_score(y_test, predictions, average="macro", zero_division=0) * 100, 2)

    bundle = {"pipeline": pipeline, "intents": intents,
              "faqs": cfg.get("faqs", []), "config_hash": hex(hash(str(cfg)))[:10]}
    joblib.dump(bundle, model_path(uid))

    per_intent = {
        intent: {
            "precision": round(report.get(intent, {}).get("precision", 0) * 100, 1),
            "recall": round(report.get(intent, {}).get("recall", 0) * 100, 1),
            "f1": round(report.get(intent, {}).get("f1-score", 0) * 100, 1),
            "support": int(report.get(intent, {}).get("support", 0)),
        }
        for intent in intents
    }

    version = datetime.now().strftime("v%Y%m%d-%H%M%S")
    return {
        "version": version,
        "trained_at": datetime.now().isoformat(timespec="seconds"),
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "samples": len(samples),
        "train_samples": len(x_train),
        "test_samples": len(x_test),
        "intents": intents,
        "per_intent": per_intent,
        "confusion_matrix": matrix,
        "dataset_breakdown": dataset_stats(samples),
        "duration_sec": round(time.time() - started, 1),
        "algorithm": "TF-IDF(1-2gram) + LogisticRegression",
    }


def load_model(uid: str):
    path = model_path(uid)
    if not os.path.exists(path):
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None


def predict_intent(bundle, text: str) -> Tuple[str, float]:
    """Return (intent, confidence 0-1)."""
    if not bundle:
        return "unknown", 0.0
    pipeline = bundle["pipeline"]
    proba = pipeline.predict_proba([text])[0]
    idx = int(np.argmax(proba))
    return pipeline.classes_[idx], float(proba[idx])


def match_faq(bundle, question: str, faqs: List[Dict[str, str]],
              threshold: float = 0.30) -> Tuple[Optional[str], float]:
    """Cosine-similarity FAQ retrieval using the trained TF-IDF vectorizer."""
    if not bundle or not faqs:
        return None, 0.0
    vectorizer: TfidfVectorizer = bundle["pipeline"].named_steps["tfidf"]
    questions = [f.get("q", "") for f in faqs]
    if not any(questions):
        return None, 0.0
    q_vec = vectorizer.transform([question])
    faq_vecs = vectorizer.transform(questions)
    scores = (q_vec @ faq_vecs.T).toarray()[0]
    idx = int(np.argmax(scores)) if len(scores) else -1
    best = float(scores[idx]) if idx >= 0 else 0.0
    if best >= threshold:
        return faqs[idx].get("a", ""), round(best, 3)
    return None, round(best, 3)
