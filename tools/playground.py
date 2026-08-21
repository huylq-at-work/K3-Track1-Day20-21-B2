#!/usr/bin/env python3
"""Playground: hỏi tutor thật và xem trace ngay trên trình duyệt.

    py tools/playground.py            # rồi mở http://127.0.0.1:8777

Mỗi câu hỏi chạy đúng vòng tool-calling của eval/run_eval.py, nên cái bạn thấy
ở đây là cái sẽ xuất hiện trong results.jsonl. Trace vẫn log lên
Braintrust/LangSmith nếu .env có key — dùng để thử tracing trước khi chạy cả bộ.
"""
import json
import os
import sys
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tutor"))
sys.path.insert(0, os.path.join(ROOT, "eval"))

import tutor                      # noqa: E402
import code_checks                # noqa: E402
from run_eval import estimate_cost_usd  # noqa: E402
import tracing                    # noqa: E402

PORT = int(os.environ.get("PLAYGROUND_PORT", "8777"))
HTML = os.path.join(ROOT, "tools", "playground.html")

_sections = None
_tracer = None


def corpus():
    """Nạp corpus một lần rồi dùng lại — nạp lại mỗi request thì chậm."""
    global _sections
    if _sections is None:
        secs = tutor.load_corpus()
        _sections = {
            "list": secs,
            "valid": {(s["doc_id"], s["section_id"]) for s in secs},
            "tokens": {(s["doc_id"], s["section_id"]): tutor.tokens(s["text"]) for s in secs},
            "text": {(s["doc_id"], s["section_id"]): s["text"] for s in secs},
        }
    return _sections


def tracer():
    global _tracer
    if _tracer is None:
        _tracer = tracing.init_tracer()
    return _tracer


def run_checks(rec):
    """Chạy đúng CHECKS của eval/code_checks.py lên một câu trả lời."""
    c = corpus()
    out = []
    for name, fn in code_checks.CHECKS:
        try:
            if fn is code_checks.check_schema:
                ok, reason = fn(rec)
            elif fn is code_checks.check_citation_exists:
                ok, reason = fn(rec, c["valid"])
            else:
                ok, reason = fn(rec, c["tokens"])
        except Exception as e:                      # check của nhóm có thể lỗi
            ok, reason = None, "check lỗi: %s" % e
        out.append({"name": name,
                    "status": "skip" if ok is None else ("pass" if ok else "fail"),
                    "reason": reason})
    return out


def dataset_rows(path):
    if not os.path.exists(path):
        return []
    rows = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        md = r.get("metadata") or {}
        rows.append({
            "scenario_id": r.get("scenario_id") or r.get("id"),
            "input": r.get("input", ""),
            "slide": md.get("slide"),
            "tier": md.get("dim_corpus_coverage", ""),
            "set_type": md.get("set_type", ""),
            "expected_behavior": md.get("expected_behavior", ""),
            "anchors": md.get("corpus_anchor") or [],
        })
    return rows


def ask(question, slide=None):
    t0 = time.time()
    output, meta = tutor.call_tutor(question, slide=slide)
    cost = estimate_cost_usd(tutor.MODEL, meta["usage"])
    rec = {"scenario_id": "playground", "input": question, "output": output}

    try:                                            # trace: để thử tracing thật
        tracer().log_run(
            name="tutor-playground",
            inputs={"question": question, "slide": slide, "model": tutor.MODEL},
            outputs=output,
            metadata={"steps": meta.get("steps"), "source": "playground"},
            metrics={**{k: v for k, v in meta["usage"].items() if isinstance(v, (int, float))},
                     "latency_s": meta["latency_s"],
                     **({"cost_usd": cost} if cost else {})},
        )
        tracer().flush()
        traced = "noop" not in type(tracer()).__name__.lower()
    except Exception:
        traced = False

    c = corpus()
    for tc in meta["tool_calls"]:                   # kèm sẵn text để xem tại chỗ
        tc["hit_texts"] = [c["text"].get(tuple(h.split("#", 1)), "")[:1200] for h in tc["hits"]]

    return {
        "output": output,
        "raw_content": meta["raw_content"],
        "tool_calls": meta["tool_calls"],
        "retrieved": meta["retrieved"],
        "steps": meta["steps"],
        "finish_reason": meta["finish_reason"],
        "usage": meta["usage"],
        "latency_s": meta["latency_s"],
        "wall_s": round(time.time() - t0, 2),
        "cost_usd": cost,
        "model": tutor.MODEL,
        "checks": run_checks(rec),
        "traced": traced,
        "trace_backend": type(tracer()).__name__,
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):              # bớt ồn, chỉ in lỗi
        pass

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            return self._send(200, open(HTML, "rb").read(), "text/html; charset=utf-8")
        if u.path == "/api/boot":
            return self._send(200, json.dumps({
                "model": tutor.MODEL,
                "trace_backend": type(tracer()).__name__,
                "rows": dataset_rows(os.path.join(ROOT, "dataset.jsonl")),
                "checks": [n for n, _ in code_checks.CHECKS],
            }, ensure_ascii=False))
        if u.path == "/api/section":
            q = parse_qs(u.query)
            key = (q.get("doc", [""])[0], q.get("sec", [""])[0])
            text = corpus()["text"].get(key)
            if text is None:
                return self._send(404, json.dumps({"error": "không có section này"}))
            return self._send(200, json.dumps({"doc_id": key[0], "section_id": key[1],
                                               "text": text}, ensure_ascii=False))
        self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if urlparse(self.path).path != "/api/ask":
            return self._send(404, json.dumps({"error": "not found"}))
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            res = ask(body.get("question", ""), body.get("slide"))
            self._send(200, json.dumps(res, ensure_ascii=False))
        except Exception as e:
            traceback.print_exc()
            self._send(500, json.dumps({"error": str(e)}, ensure_ascii=False))


if __name__ == "__main__":
    if not tutor.get_api_key():
        raise SystemExit("Chưa có API key cho %s — điền .env rồi chạy lại." % tutor.MODEL)
    print("Tutor : %s" % tutor.MODEL)
    print("Trace : %s" % type(tracer()).__name__)
    print("Mở    : http://127.0.0.1:%d   (Ctrl+C để dừng)" % PORT)
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
