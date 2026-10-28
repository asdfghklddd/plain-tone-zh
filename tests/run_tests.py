#!/usr/bin/env python3
"""回归测试 / Regression tests: before/* 必须 FAIL，after/* 和 false_positive*.md 必须 PASS 且 0 hard。"""
import glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from tone_check import check

def run():
    fails = []
    cases = [(f, "FAIL") for f in sorted(glob.glob(os.path.join(ROOT, "tests/before/*.*")))]
    cases += [(f, "PASS") for f in sorted(glob.glob(os.path.join(ROOT, "tests/after/*.*")))]
    cases += [(f, "PASS") for f in sorted(glob.glob(os.path.join(ROOT, "tests/false_positive*.*")))]
    for f, want in cases:
        r = check(open(f, encoding="utf-8").read())
        ok = r["verdict"] == want and (want == "FAIL" or r["hard"] == 0)
        print(f"{'ok  ' if ok else 'BAD '} {os.path.relpath(f, ROOT)}: {r['verdict']} hard={r['hard']} soft={r['soft']} (want {want})")
        if not ok: fails.append(f)
    print(f"\n{len(cases) - len(fails)}/{len(cases)} passed")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(run())
