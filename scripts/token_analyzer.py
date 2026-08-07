#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
token_analyzer.py - Reproducible token-cost analyzer for yy-spec-review (builtin-v1)
===================================================================================

WHY THIS EXISTS
---------------
yy-spec-review's slimming design claims a ">=40% framework token reduction".
review-002 (CR-004, P0) found the measurement algorithm was *undefined*, so the
>=40% claim could not be objectively reproduced. This script fixes that by
pinning a deterministic, zero-dependency algorithm. Same algorithm + same
manifest + same normalization applied to baseline and candidate => the reduction
ratio is exactly reproducible on any machine running Python >= 3.9.

TOKENIZATION ALGORITHM (builtin-v1) -- MUST BE REPRODUCED EXACTLY
-----------------------------------------------------------------
1. Normalize (applied identically to every file):
     - read file as UTF-8
     - convert all line endings to LF ("\n")
     - strip trailing whitespace from each line
     - ensure the file ends with exactly one "\n"
2. Scan characters and count tokens:
     - CJK ideographs / kana / hangul / fullwidth forms / CJK punctuation
         -> 1 token per character
     - maximal run of ASCII alphanumerics [A-Za-z0-9]+
         -> ceil(len/4) tokens   (English ~4 chars/token proxy)
     - maximal run of ASCII whitespace [ \t\r\n]+
         -> 1 token per run
     - any other single character (ASCII punctuation, symbols, emoji,
         Latin-extended, etc.) -> 1 token per character
3. file_tokens = the sum above.
   set_tokens  = sum of file_tokens over files sorted by path (lexicographic),
                 eliminating any ordering nondeterminism.

The absolute numbers are a *proxy* for real LLM token cost, but because the SAME
algorithm is applied to both baseline and candidate, the REDUCTION RATIO is an
exact, reproducible invariant. That is what makes ">=40%" objectively checkable.

USAGE
-----
  python token_analyzer.py --baseline            measure current framework (baseline)
  python token_analyzer.py --compare            baseline vs candidate gate (>=40%)
  python token_analyzer.py --manifest PATH       manifest (default: prompt_scope.json)
  python token_analyzer.py --algorithm-info      print algorithm id/version/rules
  python token_analyzer.py --scope {baseline,candidate}

EXIT CODES: 0 = PASS (reduction >= threshold); 1 = FAIL or error.
Machine-readable JSON is printed to stdout.
"""

import argparse
import json
import math
import os
import re
import sys

ALGORITHM_ID = "builtin-v1"
ALGORITHM_VERSION = "1.0.0"


def is_cjk(cp):
    """Return True if the codepoint is a CJK/kana/hangul/fullwidth character
    (counted as 1 token per character under builtin-v1)."""
    if 0x3000 <= cp <= 0x303F:
        return True  # CJK symbols and punctuation
    if 0x3040 <= cp <= 0x309F:
        return True  # Hiragana
    if 0x30A0 <= cp <= 0x30FF:
        return True  # Katakana
    if 0x3400 <= cp <= 0x4DBF:
        return True  # CJK Extension A
    if 0x4E00 <= cp <= 0x9FFF:
        return True  # CJK Unified Ideographs
    if 0xA000 <= cp <= 0xA4CF:
        return True  # Yi
    if 0xAC00 <= cp <= 0xD7AF:
        return True  # Hangul Syllables
    if 0xF900 <= cp <= 0xFAFF:
        return True  # CJK Compatibility Ideographs
    if 0xFF00 <= cp <= 0xFFEF:
        return True  # Fullwidth / Halfwidth forms
    if 0x20000 <= cp <= 0x2A6DF:
        return True  # CJK Extension B
    if 0x2A700 <= cp <= 0x2B73F:
        return True  # CJK Extension C
    if 0x2B740 <= cp <= 0x2B81F:
        return True  # CJK Extension D
    if 0x2B820 <= cp <= 0x2CEAF:
        return True  # CJK Extension E
    if 0x2CEB0 <= cp <= 0x2EBEF:
        return True  # CJK Extension F
    if 0x30000 <= cp <= 0x3134F:
        return True  # CJK Extension G
    return False


def normalize(text):
    """builtin-v1 normalization step 1."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    return "\n".join(lines) + "\n"


def count_tokens(text):
    """builtin-v1 token counting (steps 1-2)."""
    text = normalize(text)
    n = len(text)
    tokens = 0
    i = 0
    while i < n:
        ch = text[i]
        cp = ord(ch)
        if is_cjk(cp):
            tokens += 1
            i += 1
        elif ch.isascii():
            if ch.isalnum():
                j = i
                while j < n and text[j].isascii() and text[j].isalnum():
                    j += 1
                run = j - i
                tokens += (run + 3) // 4  # ceil(run / 4)
                i = j
            elif ch.isspace():
                j = i
                while j < n and text[j].isspace():
                    j += 1
                tokens += 1  # 1 token per whitespace run
                i = j
            else:
                tokens += 1  # ASCII punctuation / symbol
                i += 1
        else:
            tokens += 1  # emoji, Latin-extended, etc.
            i += 1
    return tokens


def load_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def skill_root_of(manifest_path):
    """Manifest lives in <skill>/scripts/; skill root is its parent dir."""
    return os.path.dirname(os.path.dirname(os.path.abspath(manifest_path)))


def measure_group(manifest, group_key, root):
    group = manifest[group_key]
    files = sorted(group["files"])  # lexicographic -> deterministic order
    per_file = []
    total = 0
    missing = []
    for rel in files:
        full = os.path.join(root, rel)
        if not os.path.isfile(full):
            missing.append(rel)
            continue
        with open(full, "r", encoding="utf-8") as f:
            t = count_tokens(f.read())
        per_file.append({"path": rel, "tokens": t})
        total += t
    return per_file, total, missing


def extract_heading_sections(text):
    """Return the set of section numbers (e.g. '1', '3.1') found in markdown
    headings of the form '# 1. Title' or '### 3.1 Confidence'."""
    nums = set()
    for line in text.split("\n"):
        m = re.match(r"^#{1,6}\s+(\d+(?:\.\d+)?)", line)
        if m:
            nums.add(m.group(1))
    return nums


def check_reference_integrity(manifest, root):
    """Verify every 'references/common.md §X.Y' reference in the candidate
    framework files resolves to a real heading in references/common.md.

    Returns (unresolved_list, checked_count). Each unresolved entry is
    {"file": <rel>, "ref": <section-number>}. When common.md itself is
    missing it is reported via candidate_missing and nothing is checked here.
    """
    candidate = manifest.get("candidate", {})
    cfiles = candidate.get("files", [])
    common_rel = "references/common.md"
    common_path = os.path.join(root, common_rel)
    unresolved = []
    checked = 0
    if not os.path.isfile(common_path):
        return unresolved, checked
    with open(common_path, "r", encoding="utf-8") as f:
        common_text = f.read()
    headings = extract_heading_sections(common_text)
    for rel in cfiles:
        if rel == common_rel:
            continue
        full = os.path.join(root, rel)
        if not os.path.isfile(full):
            continue
        with open(full, "r", encoding="utf-8") as f:
            text = f.read()
        for line in text.split("\n"):
            # Only treat a '§X' as a common.md reference when it is anchored to a
            # 'common.md' mention (e.g. "`references/common.md` §3.1"). Bare '§X'
            # on the same line that points at the file's own section is ignored.
            for m in re.finditer(r"common\.md`?\s*§\s*(\d+(?:\.\d+)?)", line):
                ref = m.group(1)
                checked += 1
                if ref not in headings:
                    unresolved.append({"file": rel, "ref": ref})
    return unresolved, checked


def print_algorithm_info():
    info = {
        "algorithm": {"id": ALGORITHM_ID, "version": ALGORITHM_VERSION},
        "rules": [
            "normalize: UTF-8 -> LF -> strip trailing whitespace per line -> exactly one trailing newline",
            "CJK/kana/hangul/fullwidth/CJK-punctuation: 1 token per character",
            "ASCII [A-Za-z0-9]+ run: ceil(len/4) tokens",
            "ASCII whitespace [ \\t\\r\\n]+ run: 1 token per run",
            "any other single character: 1 token per character",
            "set_tokens = sum over files sorted by path (lexicographic)",
        ],
        "dependencies": "Python >= 3.9 standard library only (zero external deps)",
        "determinism": "identical output on any machine for identical files",
    }
    print(json.dumps(info, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Reproducible token analyzer (builtin-v1)")
    ap.add_argument("--baseline", action="store_true", help="measure baseline scope")
    ap.add_argument("--compare", action="store_true", help="baseline vs candidate gate")
    ap.add_argument("--scope", choices=["baseline", "candidate"], help="single-scope report")
    ap.add_argument("--manifest", default=None, help="manifest path (default: prompt_scope.json next to this script)")
    ap.add_argument("--algorithm-info", action="store_true", help="print algorithm id/version/rules")
    args = ap.parse_args()

    if args.algorithm_info:
        print_algorithm_info()
        return 0

    here = os.path.abspath(__file__)
    manifest_path = args.manifest or os.path.join(os.path.dirname(here), "prompt_scope.json")
    if not os.path.isfile(manifest_path):
        print(json.dumps({"error": "manifest not found: %s" % manifest_path}, ensure_ascii=False))
        return 1

    manifest = load_manifest(manifest_path)
    root = skill_root_of(manifest_path)

    if args.baseline or args.scope == "baseline":
        per_file, total, missing = measure_group(manifest, "baseline", root)
        out = {
            "algorithm": {"id": ALGORITHM_ID, "version": ALGORITHM_VERSION},
            "scope": "baseline",
            "root": root,
            "files": per_file,
            "total_tokens": total,
            "missing_files": missing,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if not missing else 1

    if args.scope == "candidate":
        per_file, total, missing = measure_group(manifest, "candidate", root)
        out = {
            "algorithm": {"id": ALGORITHM_ID, "version": ALGORITHM_VERSION},
            "scope": "candidate",
            "root": root,
            "files": per_file,
            "total_tokens": total,
            "missing_files": missing,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if not missing else 1

    if args.compare:
        b_per, b_total, b_missing = measure_group(manifest, "baseline", root)
        c_per, c_total, c_missing = measure_group(manifest, "candidate", root)
        th = manifest.get("threshold", {})
        enforced = bool(th.get("enforced", True))
        min_red = th.get("min_reduction_pct", 40.0)
        reduction = ((b_total - c_total) / b_total * 100.0) if b_total else 0.0
        unresolved, ref_checked = check_reference_integrity(manifest, root)
        ref_ok = (len(unresolved) == 0)
        reduction_ok = True
        if enforced and min_red is not None:
            reduction_ok = reduction >= float(min_red)
        passed = (not b_missing) and (not c_missing) and ref_ok and reduction_ok
        out = {
            "algorithm": {"id": ALGORITHM_ID, "version": ALGORITHM_VERSION},
            "baseline_tokens": b_total,
            "candidate_tokens": c_total,
            "reduction_pct": round(reduction, 4),
            "reduction_enforced": enforced,
            "threshold_pct": (float(min_red) if (enforced and min_red is not None) else None),
            "reference_integrity": {
                "checked": ref_checked,
                "unresolved": unresolved,
                "ok": bool(ref_ok),
            },
            "pass": bool(passed),
            "baseline_missing": b_missing,
            "candidate_missing": c_missing,
            "baseline_files": b_per,
            "candidate_files": c_per,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if passed else 1

    # default: algorithm info
    print_algorithm_info()
    return 0


if __name__ == "__main__":
    sys.exit(main())
