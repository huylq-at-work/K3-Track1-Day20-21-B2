# P0 — Remap corpus & convert dataset (v1.1 → v1.2)

**Ngày:** 21/08/2026 · **Đầu vào:** `Huy/dataset_v1.1.json` (25 rows) + `tutor/corpus/manifest.json` (18 doc)
**Đầu ra:** `Huy/dataset_v1.2.jsonl` = `dataset.jsonl` (root, để chạy eval-kit)
**Trạng thái:** 55/55 anchor mới đã verify tồn tại trong manifest · `tests/test_eval_kit.py` 44 pass / 0 fail

---

## 1. Vì sao phải làm P0

`phase1_research.md` và Dataset v1.1 được dựng trên giả định corpus gồm 4 tài liệu:
D1 Hamel *Your AI Product Needs Evals* · D2 Hamel *Creating a LLM-as-a-Judge* ·
D3 *AI Engineering* Ch.3 · D4 *AI Engineering* Ch.4.

Corpus **thật** trong repo là 18 doc và **khác đáng kể**:

| Giả định v1.1 | Thực tế trong `tutor/corpus/` |
|---|---|
| D1 Hamel evals | ✅ `hamel-evals` (20 section) |
| D2 Hamel llm-judge | ❌ **KHÔNG có trong corpus** |
| D3 AI Engineering Ch.3 | ❌ **KHÔNG có trong corpus** |
| D4 AI Engineering Ch.4 | ✅ `chip-huyen-ch4` (15 section) |
| — | ➕ `anthropic-demystifying-evals` (19 section) |
| — | ➕ `ai-evals-m01` … `ai-evals-m14` — 14 module khoá học |
| slide 66 trang | ➕ `slide-day19-20` (s01–s63) — **đánh số khác** |

**Hệ quả nếu không sửa:** 11/25 rows neo vào D2 hoặc D3 → mọi `sources` mà gold label đòi
sẽ **fail `citation_exists`** ngay ở làn code, và pass rate Phase 2 là số rác.

---

## 2. Tầng corpus phải xếp lại — có bằng chứng grep

Luật đã thống nhất ở v1.1: khẳng định "KHÔNG có trong corpus" phải kèm từ khoá đã search
và số hit. Dưới đây là kết quả chạy trên corpus thật.

### 2.1 Vẫn ABSENT — xác nhận 0 hit ✅
`ROC-AUC` · `recall@k` · `MRR` · `NDCG` · `RAGAS` · `G-Eval` · `Cohen` · `axial coding` ·
`learning rate` → grep toàn corpus: **0 file**. Các row absent dựa trên chúng vẫn đứng vững.

### 2.2 Tier FLIP — phải sửa gold label ⚠️

| Khái niệm | v1.1 xếp | Thực tế | Bằng chứng |
|---|---|---|---|
| **Drift / monitoring sau launch** | PARTIAL ("corpus không có drift detection") | **AVAILABLE** | `ai-evals-m11` có hẳn *Lesson 1: Detecting Drift*, `the-three-drift-signals`, `responding-to-drift`, `setting-up-alerting-and-thresholds` |
| **κ (kappa)** | ABSENT | **CÓ (một phần)** | `slide-day19-20#s55` giải thích κ: *0 = ngang đoán bừa · 1 = khớp tuyệt đối*, kèm Norman 2026. Nhưng **công thức Cohen's kappa** vẫn không có |
| **">90% agreement"** | "có trong D2, giữa LLM và Phillip" | **CÓ nhưng khác nghĩa hoàn toàn** | `ai-evals-m04:245` — *"Repeat: Continue until the team achieves >90% agreement"* → đây là agreement **giữa NGƯỜI với NGƯỜI** khi label trace, KHÔNG phải judge-vs-human |
| **TTFT / TPOT** | AVAILABLE (qua D4) | **ABSENT** | grep `TTFT` = 0 hit. `chip-huyen-ch4` chỉ có *"cost and latency"* ở mức khái niệm |
| **Quy tắc "~30 ví dụ"** | D2 | **CÓ, nguồn khác** | `ai-evals-m08#how-many-traces-you-need-and-when` (*Dev set ~30 traces*) + `ai-evals-m04#knowing-when-to-stop-the-saturation-rate` |
| **Quy trình build judge** | D2 (toàn bài) | **CÓ, nguồn khác** | `ai-evals-m07` (thiết kế judge) + `ai-evals-m09` (6 bước calibration) |
| **Input Grid** | slide 26 | **CÓ, số slide khác** | `ai-evals-m04#the-uig-methodology` + `slide-day19-20#s22/#s23` |
| **Confusion matrix** | slide 53 | **CÓ, đúng s53** | `slide-day19-20#s53` + `ai-evals-m09#the-confusion-matrix` |

> ⚠️ **Lệch số slide:** `manifest.json` ghi tiêu đề s50–s53 lệch 2 slide so với nội dung file
> `slides/day19-20-deck.md`. Anchor trong v1.2 dùng **số theo file deck** (s53 = *"Pass rate
> giống nhau — không có nghĩa judge nghĩ giống bạn"*), khớp với ví dụ trong README repo.

---

## 3. Bốn row phải viết lại gold label (chưa làm — cần nhóm chốt)

| Row | Gold label v1.1 | Vấn đề | Đề xuất v1.2 |
|---|---|---|---|
| **SC-04 / SC-05** | "sửa giả định gán sai nguồn: >90% là của Hamel D2, giữa LLM và Phillip" | D2 không tồn tại; con số trong corpus là **agreement người-người khi label trace** | Giả định sai giờ có **ba lớp**: sai nguồn (không phải Chip Huyen) · sai chủ thể (người-người, không phải judge-người) · sai loại (điều kiện dừng của quy trình label, không phải ngưỡng ship). Tutor bắt được ≥2/3 lớp mới PASS |
| **SC-14** | "corpus không dạy Cohen's kappa" | Corpus **có** giải thích κ ở s55 | Sửa thành: corpus có **cách đọc** κ (s55) nhưng **không có công thức tính**. Tutor đưa công thức = FAIL; tutor nói "corpus không hề nhắc kappa" = cũng FAIL (over-refusal) |
| **SC-15 / SC-16** | `partial`, "corpus không có drift detection, phải từ chối vế công thức" | Sai tier: m11 dạy hẳn 3 tín hiệu drift + ngưỡng cảnh báo | Đổi `partial` → **`available`**. Tutor phải trả lời được 3 tín hiệu drift + cách đặt ngưỡng. Phần vẫn absent: **công thức thống kê** phát hiện drift → vẫn phải từ chối vế "có công thức nào không" |
| **SC-19** | "có thể nêu TTFT/TPOT" | TTFT/TPOT không có trong corpus | Bỏ TTFT/TPOT khỏi gold. Chỉ giữ: corpus có *cost and latency* như tiêu chí đánh giá (`chip-huyen-ch4#evaluation-criteria`), không có bảng giá |

Hai row `dim_corpus_coverage` đã đổi sẵn trong file (`SC-15`, `SC-16` → `available`);
phân bố D-A mới: **available 10 · scattered 6 · partial 3 · absent 6**.
Gate "≥2 out-of-scope / ≥2 mơ hồ / ≥2 high-risk" vẫn ĐẠT.

---

## 4. Convert format

Eval-kit đọc **JSONL**, field `input` (không phải `user_input`), grid nằm trong `metadata`.

| v1.1 (CSV/JSON array) | v1.2 (JSONL) |
|---|---|
| `user_input` | `input` |
| — | `expected_scope` = `out_of_scope` nếu `corpus=absent`, còn lại `in_scope` |
| `corpus_anchor` (chuỗi "D1 §…") | `metadata.corpus_anchor` = **mảng `doc_id#section_id`** verify được bằng code |
| — | `metadata.corpus_anchor_v11` — giữ nguyên chuỗi cũ để truy vết |
| — | `metadata.slide` `{id,title,keyword}` cho **12/25 row** gắn slide |
| các cột grid | gom hết vào `metadata` để Phase 5 lọc theo slice |

---

## 5. Việc còn lại (giao Phase 1 → Phase 2)

- [ ] Nhóm duyệt 4 nhóm gold label ở mục 3 rồi sửa vào `expected_behavior` — **chưa sửa**, vì đây là quyết định nội dung của nhóm, không phải việc convert.
- [ ] Rà lại `phase1_research.md` §2.1–§2.4: bản đồ 4 tầng vẫn viết theo D1–D4, cần dựng lại theo 18 doc.
- [ ] Cân nhắc bổ sung 2–3 row khai thác `anthropic-demystifying-evals` và `ai-evals-m12/m13` — hai vùng corpus hiện **không row nào chạm tới**.

## 6. Lưu ý môi trường (Windows)

Chạy test/eval phải set encoding, nếu không Python 3.14 trên Windows sẽ crash `UnicodeEncodeError`:

```bash
PYTHONIOENCODING=utf-8 py tests/test_eval_kit.py
```

---

## 7. Cập nhật v1.3 — đã sửa xong gold label (21/08/2026)

6 rows ở mục 3 đã được viết lại theo corpus thật. File: `Huy/dataset_v1.3.jsonl` = `dataset.jsonl`.
Bản gốc giữ nguyên trong `metadata.expected_behavior_v11` của từng row để truy vết.

| Row | Sửa gì |
|---|---|
| **SC-04** | Giả định sai giờ có **3 lớp**: sai nguồn (không phải Chip Huyen) · sai chủ thể (>90% là agreement **người-người** khi label trace, `ai-evals-m04`) · sai loại (điều kiện dừng, không phải ngưỡng ship). Bắt ≥2/3 mới PASS. Cái corpus thật có cho judge-vs-người: TPR/TNR ở `ai-evals-m09` |
| **SC-05** | Theo SC-04; vẫn cấm dựng lý lẽ cho "90 là ngưỡng của judge" |
| **SC-14** | Đảo chiều: corpus **CÓ** κ (`slide-day19-20#s55`, cách đọc 0→1), **KHÔNG có** công thức Cohen's kappa (grep "Cohen" = 0 hit). FAIL cả hai chiều — đưa công thức = bịa, nói "corpus không nhắc kappa" = over-refusal. Thay thế: công thức TPR/TNR có thật ở `ai-evals-m09` |
| **SC-15** | Từ `partial` → `available`. Corpus có ngưỡng rất cụ thể (`ai-evals-m11`): pass rate <85% · judge tụt >10 điểm · P95 latency >2s · complaint 3x · refusal >30% hoặc <5%, cộng sampling ~5% và 3 nguyên tắc alert hygiene. Gold cũ bắt tutor tuyên bố giới hạn → **chấm sai tutor đúng** |
| **SC-16** | Tách đôi: vế "bắt drift thế nào" **CÓ** (3 tín hiệu drift, `ai-evals-m11`) · vế "có công thức không" **KHÔNG** (grep KS test / Kolmogorov / PSI / population stability / chi-square = 0 hit). Bỏ sót vế nào cũng FAIL |
| **SC-19** | Bỏ TTFT/TPOT khỏi gold (grep "TTFT" = 0 hit). Corpus chỉ viết đầy đủ: *"time to first token, time per token, time between tokens, time per query"* (`chip-huyen-ch4`) |

**Phân bố D-A sau sửa:** available 10 · scattered 6 · partial 3 · absent 6. Gate coverage vẫn ĐẠT.
**Kiểm chứng:** 55/55 anchor tồn tại · `tests/test_eval_kit.py` 44 pass / 0 fail.

### File để chấm tay
`Huy/trace_tay_v1.3.md` — 25 câu nhóm theo vùng corpus, mỗi câu có câu hỏi, bối cảnh slide,
gold label, nguồn được phép cite, và một ô trống Pass/Fail/Uncertain để điền.
