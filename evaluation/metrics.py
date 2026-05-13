"""Metric helpers for AgentCloseoutBench."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Confusion:
    tp: int = 0
    fp: int = 0
    fn: int = 0
    tn: int = 0

    @property
    def n(self) -> int:
        return self.tp + self.fp + self.fn + self.tn


def safe_div(num: float, den: float) -> float | None:
    if den == 0:
        return None
    return num / den


def precision(c: Confusion) -> float | None:
    return safe_div(c.tp, c.tp + c.fp)


def recall(c: Confusion) -> float | None:
    return safe_div(c.tp, c.tp + c.fn)


def f1(c: Confusion) -> float | None:
    if c.tp == 0 and (c.fp > 0 or c.fn > 0):
        return 0.0
    p = precision(c)
    r = recall(c)
    if p is None or r is None:
        return None
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def fbeta(c: Confusion, beta: float) -> float | None:
    if c.tp == 0 and (c.fp > 0 or c.fn > 0):
        return 0.0
    p = precision(c)
    r = recall(c)
    if p is None or r is None:
        return None
    if p + r == 0:
        return 0.0
    beta2 = beta * beta
    return (1 + beta2) * p * r / ((beta2 * p) + r)


def f0_5(c: Confusion) -> float | None:
    return fbeta(c, 0.5)


def fpr(c: Confusion) -> float | None:
    return safe_div(c.fp, c.fp + c.tn)


def specificity(c: Confusion) -> float | None:
    return safe_div(c.tn, c.fp + c.tn)


def accuracy(c: Confusion) -> float | None:
    return safe_div(c.tp + c.tn, c.n)


def mcc(c: Confusion) -> float | None:
    den = (c.tp + c.fp) * (c.tp + c.fn) * (c.tn + c.fp) * (c.tn + c.fn)
    if den == 0:
        return None
    return ((c.tp * c.tn) - (c.fp * c.fn)) / math.sqrt(den)


def wilson_interval(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float | None, float | None]:
    if n == 0:
        return (None, None)
    phat = successes / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    half = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * pct
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - rank) + ordered[hi] * (rank - lo)


def bootstrap_f1_interval(pairs: list[tuple[int, int]], *, samples: int = 1000, seed: int = 42) -> tuple[float | None, float | None]:
    if not pairs:
        return (None, None)
    rng = random.Random(seed)
    vals: list[float] = []
    n = len(pairs)
    for _ in range(samples):
        tp = fp = fn = tn = 0
        for _ in range(n):
            truth, pred = pairs[rng.randrange(n)]
            if truth == 1 and pred == 1:
                tp += 1
            elif truth == 0 and pred == 1:
                fp += 1
            elif truth == 1 and pred == 0:
                fn += 1
            else:
                tn += 1
        score = f1(Confusion(tp, fp, fn, tn))
        if score is not None:
            vals.append(score)
    return (percentile(vals, 0.025), percentile(vals, 0.975))


def prevalence_adjusted_ppv(c: Confusion, prevalence: float) -> float | None:
    sens = recall(c)
    false_positive_rate = fpr(c)
    if sens is None or false_positive_rate is None:
        return None
    numerator = sens * prevalence
    denominator = numerator + false_positive_rate * (1 - prevalence)
    return safe_div(numerator, denominator)


def metric_dict(c: Confusion, pairs: list[tuple[int, int]] | None = None) -> dict:
    rec_den = c.tp + c.fn
    prec_den = c.tp + c.fp
    fpr_den = c.fp + c.tn
    return {
        "n": c.n,
        "TP": c.tp,
        "FP": c.fp,
        "FN": c.fn,
        "TN": c.tn,
        "precision": precision(c),
        "precision_wilson_95": wilson_interval(c.tp, prec_den),
        "recall": recall(c),
        "recall_wilson_95": wilson_interval(c.tp, rec_den),
        "F0.5": f0_5(c),
        "F1": f1(c),
        "F1_bootstrap_95": bootstrap_f1_interval(pairs or []) if pairs is not None else (None, None),
        "FPR": fpr(c),
        "FPR_wilson_95": wilson_interval(c.fp, fpr_den),
        "specificity": specificity(c),
        "false_positives_per_1000_benign": (fpr(c) * 1000) if fpr(c) is not None else None,
        "accuracy": accuracy(c),
        "MCC": mcc(c),
        "prevalence_adjusted_PPV": {
            "0.005": prevalence_adjusted_ppv(c, 0.005),
            "0.01": prevalence_adjusted_ppv(c, 0.01),
            "0.05": prevalence_adjusted_ppv(c, 0.05),
            "0.10": prevalence_adjusted_ppv(c, 0.10),
        },
    }
