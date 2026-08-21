"""Code checks — kiểm tra results.jsonl bằng rule thuần Python (không tốn API).

Đây là làn "Code check" của bài lab: những tiêu chí viết được thành rule thì kiểm
bằng code — nhanh, rẻ, khách quan, chạy lại bao nhiêu lần cũng được.

Chạy:  python3 eval/code_checks.py            # in bảng pass/fail từng check từng row
Mở rộng: thêm hàm check_* mới của riêng nhóm (xem 3 hàm mẫu dưới).
"""
import json
import os
import re
import sys
from pathlib import Path

# tutor.py nằm ở tutor/ (khu vực sản phẩm) — thêm vào sys.path để import được
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tutor"))

import tutor  # dùng lại load_corpus

EXPECTED_FIELDS = {"scope", "answer", "sources", "followup_questions"}


def check_schema(rec):
    """Output parse được và đủ 4 field đúng contract."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return False, "JSON không parse được (xem raw_content)"
    missing = EXPECTED_FIELDS - set(out)
    if missing:
        return False, "thiếu field: " + ", ".join(sorted(missing))
    return True, None


def check_citation_exists(rec, valid_ids):
    """Mọi doc_id/section_id trong sources phải tồn tại thật trong corpus."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    for s in out.get("sources") or []:
        key = (s.get("doc_id"), s.get("section_id"))
        if key not in valid_ids:
            return False, f'nguồn không tồn tại: {key[0]}#{key[1]}'
    return True, None


def _token_subsequence(needle, haystack):
    """True nếu chuỗi token của needle xuất hiện liên tiếp trong haystack."""
    if not needle:
        return True
    n = len(needle)
    return any(haystack[i:i + n] == needle for i in range(len(haystack) - n + 1))


def check_quote_verbatim(rec, section_tokens):
    """Quote phải nằm trong section đã cite:
    1. Thử so khớp chuỗi token liên tiếp trực tiếp.
    2. Tách theo dấu ba chấm (...) để so khớp từng đoạn con.
    3. Hỗ trợ layout đa cột (slide 2 cột) qua độ phủ token nội dung >= 85%.
    """
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    for s in out.get("sources") or []:
        tokens = section_tokens.get((s.get("doc_id"), s.get("section_id")), [])
        quote_raw = s.get("quote") or ""
        quote_tokens = tutor.tokens(quote_raw)
        
        if not quote_tokens:
            continue
            
        # 1. So khớp chuỗi liên tiếp trực tiếp
        if _token_subsequence(quote_tokens, tokens):
            continue
            
        # 2. Tách theo dấu ba chấm (...)
        sub_clauses = [c.strip() for c in re.split(r"\.{2,}|…|\n", quote_raw) if c.strip()]
        if len(sub_clauses) > 1:
            all_ok = True
            for sub in sub_clauses:
                sub_t = tutor.tokens(sub)
                if len(sub_t) >= 3 and not _token_subsequence(sub_t, tokens):
                    all_ok = False
                    break
            if all_ok:
                continue

        # 3. Kiểm tra độ phủ token từ khoá (xử lý layout slide 2 cột)
        sec_set = set(tokens)
        content_tokens = [t for t in quote_tokens if t not in tutor.STOPWORDS] or quote_tokens
        matched = sum(1 for t in content_tokens if t in sec_set)
        coverage = matched / len(content_tokens)
        
        if coverage >= 0.85:
            continue
            
        return False, f'quote không khớp section {s.get("section_id")}: "{(quote_raw)[:35]}..." (độ phủ {int(coverage*100)}%)'
        
    return True, None


CHECKS = [  # thêm check của nhóm vào đây
    ("schema_valid", check_schema),
    ("citation_exists", check_citation_exists),
    ("quote_verbatim", check_quote_verbatim),
]


def main(path="results.jsonl"):
    if not os.path.exists(path):
        raise SystemExit("Không thấy %s — chạy python3 eval/run_eval.py trước." % path)
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]

    sections = tutor.load_corpus()
    valid_ids = {(s["doc_id"], s["section_id"]) for s in sections}
    section_tokens = {(s["doc_id"], s["section_id"]): tutor.tokens(s["text"]) for s in sections}

    totals = {name: [0, 0] for name, _ in CHECKS}  # [pass, fail] (skip không đếm)
    for rec in rows:
        sid = rec.get("scenario_id", "?")
        line = [sid]
        for name, fn in CHECKS:
            if fn is check_schema:
                ok, reason = fn(rec)
            elif fn is check_citation_exists:
                ok, reason = fn(rec, valid_ids)
            else:
                ok, reason = fn(rec, section_tokens)
            if ok is None:
                line.append(f"{name}: skip")
                continue
            totals[name][0 if ok else 1] += 1
            line.append(f"{name}: {'pass' if ok else 'FAIL — ' + str(reason)}")
        print(" | ".join(line))

    print("\nTổng kết:")
    for name, (p, f) in totals.items():
        print(f"  {name}: {p} pass / {f} fail")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results.jsonl")
