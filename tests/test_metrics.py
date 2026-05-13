from evaluation.metrics import Confusion, f0_5, f1, metric_dict, wilson_interval


def test_basic_metrics():
    c = Confusion(tp=8, fp=2, fn=1, tn=9)
    d = metric_dict(c, [(1, 1)] * 8 + [(0, 1)] * 2 + [(1, 0)] + [(0, 0)] * 9)
    assert d["precision"] == 0.8
    assert round(d["recall"], 3) == 0.889
    assert round(f1(c), 3) == 0.842
    assert round(f0_5(c), 3) == 0.816
    assert round(d["F0.5"], 3) == 0.816
    assert d["FPR"] == 2 / 11
    assert d["false_positives_per_1000_benign"] == (2 / 11) * 1000
    assert "0.01" in d["prevalence_adjusted_PPV"]


def test_f1_zero_when_precision_and_recall_zero():
    assert f1(Confusion(tp=0, fp=3, fn=4, tn=9)) == 0.0
    assert f1(Confusion(tp=0, fp=0, fn=4, tn=9)) == 0.0


def test_wilson_bounds():
    lo, hi = wilson_interval(50, 100)
    assert 0.40 < lo < 0.41
    assert 0.59 < hi < 0.60
