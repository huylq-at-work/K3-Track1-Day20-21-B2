# Track 1 · Day 21 — AI Evaluation Capstone

> Đổi tên file này thành `README.md` khi đóng gói thư mục nộp
> `Track1_Day21_<MSSV>_<HoVaTen>/`.

## Thông tin

| | |
|---|---|
| Họ tên | _(điền)_ |
| MSSV | _(điền)_ |
| Lớp / Track | K3 · Track 1 · Day 20–21 |
| Nhóm | B2 — Huy · Quân · Cường |
| Repo | https://github.com/huylq-at-work/K3-Track1-Day20-21-B2 |
| Trace | LangSmith · project `ai-evaluation` — 100 trace (25 tutor + 75 judge) |

## Sản phẩm được đánh giá

**VLearn AI Tutor** — trợ giảng trả lời câu hỏi học viên, chỉ dựa trên corpus 18 tài liệu
của khoá học, output JSON `{scope, answer, sources, followup_questions}`.
Model tutor: `deepseek/deepseek-v4-flash` · Model judge: `openai/gpt-4o-mini` (khác họ).

## Verdict tóm tắt

**HOLD — không ship.** Ba gate hỏng trên bốn:

| Gate | Ngưỡng | Thực tế | |
|---|---|---|---|
| `quote_verbatim` | ≥ 90% | **46%** | ❌ |
| Pass rate `critical_regression` | ≥ 90% | **67%** | ❌ |
| Độ trễ p95 | ≤ 8s | **14.7s** | ❌ |
| `schema_valid` + `citation_exists` | ≥ 95% | 96% / 100% | ✅ |

Lý do cốt lõi: tutor **làm tốt việc thường ngày** (representative 100%) nhưng **hỏng đúng
chỗ đắt giá** (critical_regression 67%). Nguy hiểm nhất là kiểu lỗi "trông đúng": trích
nguồn thật, có quote, có cấu trúc, chỉ thiếu đúng câu "cái này không có trong khoá học" —
học viên không có cách nào phát hiện.

Đòn bẩy tiếp theo, rẻ → đắt: sửa system prompt phần quote → sửa phần từ chối → ép dedupe
sources → chỉ khi đó mới đụng model.

## Đóng góp của tôi

| Phase | Việc |
|---|---|
| P1 Coverage | Chốt 4 dimension (loại 5 ứng viên kèm lý do), loại tổ hợp 128 → 96, chọn 18 ô, chốt 25 rows |
| P0 Dọn nền | Phát hiện dataset neo vào corpus giả định sai; remap 55 anchor sang 18 doc thật, verify bằng code; viết lại 6 gold label |
| P2 Human baseline | Chấm độc lập 25 câu; chốt quy tắc quote sai có tính fail không |
| P3 Rubric + Routing | Dựng R1–R9, chốt R3 thành gate cấp bộ thay vì blocker; bảng routing code/judge/người |
| P4 Judge | Thêm 2 code check của nhóm; 3 vòng calibrate judge (TNR 17% → 67%) |
| P5–P6 | Đọc kết quả theo lát cắt, đặt ngưỡng gate, chốt verdict |

## Cấu trúc bài nộp

```
deliverables/
├── REPORT.md              # 7 mục theo phase
└── evidence/
    ├── dataset-v1.jsonl           # 25 rows, anchor đã verify
    ├── results-v1/v2.jsonl        # v1 chạy khi chưa bật trace, v2 là vòng chính thức
    ├── labels-huy/quan/cuong.csv  # 3 nhãn người độc lập
    ├── labels.csv                 # nhãn vàng sau thảo luận (19 pass / 6 fail)
    ├── agreement-v1/v2/v3.txt     # đồng thuận qua từng vòng (16% → 64%)
    ├── judge-prompt-v1…v4.md      # mỗi vòng calibrate một snapshot
    ├── verdicts-v1/v2/v3.jsonl    # output judge từng vòng
    ├── calibration-v1.md          # ảnh chụp vòng 1
    └── braintrust-link.md         # link project trace
ai-support-log.md
```

## Chạy lại

```bash
pip install -r requirements.txt
cp .env.example .env          # điền key + BRAINTRUST_API_KEY hoặc LANGSMITH_API_KEY
PYTHONIOENCODING=utf-8 py tests/test_eval_kit.py    # 44 test offline
PYTHONIOENCODING=utf-8 py eval/run_eval.py          # ~5 phút, ~$0.27
PYTHONIOENCODING=utf-8 py eval/code_checks.py
PYTHONIOENCODING=utf-8 py eval/judge.py
```
