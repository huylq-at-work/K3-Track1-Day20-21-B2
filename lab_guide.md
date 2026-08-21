# Hướng Dẫn Thực Hành: AI Evaluation Lab
**Khóa học:** AI Thực Chiến · **Track 1 - Day 20 & 21**

---

> [!IMPORTANT]
> **Mục tiêu tổng quát:**
> Nhóm 3 người vận hành trọn vẹn một **Evaluation Workflow** chuyên nghiệp cho tính năng **AI Tutor** trên nền tảng VLearn: từ thiết kế coverage, chấm tay tạo baseline, siết rubric & phân làn kiểm thử, calibrate LLM judge cho đến việc chốt threshold và ra quyết định **Ship / Ship with conditions / Hold** dựa trên bằng chứng định lượng (evidence-based).

| Thông tin | Chi tiết |
| :--- | :--- |
| **Cấp độ** | Trung cấp |
| **Thời lượng dự kiến** | **300 phút** (Day 20: 60 phút cuối · Day 21: 240 phút) |
| **Hình thức** | Làm việc theo nhóm 3 người |
| **Môi trường & Công cụ** | • Hệ điều hành: macOS / Linux / Windows<br>• Repo eval-kit: `git clone https://github.com/VinUni-AI20k/K3-Track1-Day20-21-AI-Evaluation.git`<br>• Python 3 + API key LLM (OpenAI / DeepSeek / Gemini / Anthropic / OpenRouter)<br>• Tracing: Braintrust (hoặc LangSmith) để ghi trace bắt buộc<br>• AI Assistant cá nhân (ChatGPT / Claude / Gemini...) để hỗ trợ paraphrase |
| **Kiến thức tiên quyết** | • Đã hoàn thành Day 20 (lecture & micro-activities về trace, coverage, routing)<br>• Đọc hiểu cơ bản định dạng JSON / JSONL |

---

## 1. Bối Cảnh & Bài Toán Thực Tế

### Đề bài
Nhóm bạn đóng vai trò là **PM Team** của nền tảng học trực tuyến **VLearn**, phụ trách tính năng **AI Tutor** (trợ giảng AI giải đáp thắc mắc về chủ đề AI Evaluation dựa trên corpus tài liệu chuẩn của khóa học).

Mỗi câu trả lời của AI Tutor trả về định dạng JSON gồm:
- `answer`: Nội dung câu trả lời.
- `sources`: Nguồn trích dẫn (`doc` + `section` + `quote` nguyên văn).
- `followup_questions`: 3 câu hỏi gợi mở, dẫn dắt học viên đào sâu.

> [!NOTE]
> **Câu hỏi trọng tâm của bài Lab:**
> *Làm sao biết AI Tutor đã đủ tốt để triển khai thực tế? Tiêu chí nào có thể giao cho máy chấm (Code check / LLM Judge), và tiêu chí nào bắt buộc cần con người (Expert / Human review)?*
>
> *(Bài lab tập trung vào quy trình đánh giá, không yêu cầu code lại model hay tối ưu prompt của AI Tutor).*

---

## 2. Thuật Ngữ Cốt Lõi (Glossary)

| Thuật ngữ | Ý nghĩa thực tế |
| :--- | :--- |
| **Trace** | Bản ghi đầy đủ một lượt tương tác của Tutor: *Câu hỏi đầu vào → Câu trả lời → Nguồn trích dẫn → Câu hỏi follow-up*. |
| **Coverage** | Độ phủ tình huống của bộ test — đảm bảo quét qua đầy đủ các dạng câu hỏi, biến thể và trường hợp rủi ro. |
| **Rubric** | Bảng tiêu chí chấm điểm chuẩn hóa — định nghĩa rõ ràng để nhiều người cùng chấm cho ra một kết quả nhất quán. |
| **LLM Judge** | Một mô hình AI được phân công chấm điểm tự động thay người dựa trên prompt hướng dẫn (Judge Prompt). |
| **Calibration** | Quá trình hiệu chuẩn Judge: So sánh kết quả của Judge với nhãn người (Gold standard), phân tích sai lệch, tinh chỉnh prompt lặp lại cho đến khi đạt độ tương đồng mong muốn. |
| **Grounded** | Câu trả lời bám sát tài liệu nguồn trong corpus, không tự suy diễn hoặc bịa đặt (hallucination). |
| **Slice** | Một tập con trong dữ liệu đánh giá (ví dụ: nhóm câu hỏi mơ hồ, nhóm câu hỏi out-of-scope) — giúp phát hiện lỗi cục bộ mà số trung bình tổng thể che giấu. |
| **Threshold** | Ngưỡng chất lượng tối thiểu cần đạt để ra quyết định (ví dụ: *Groundedness ≥ 90%, Citation tồn tại = 100%*). |

---

## 3. Bản Đồ Quy Trình & Phân Bổ Công Việc

```
DAY 20 (60 phút)                    DAY 21 (240 phút)
┌───────────────────────┐           ┌───────────────────────┐     ┌───────────────────────┐
│ Phase 1: Coverage     │           │ Phase 2: Baseline     │     │ Phase 3: Formalize    │
│ Input Grid → Dataset  │ ────────> │ Chấm tay → Nhãn vàng  │ ──> │ Rubric v1 + Routing   │
└───────────────────────┘           └───────────────────────┘     └───────────────────────┘
                                                │
                                                ▼
┌───────────────────────┐           ┌───────────────────────┐     ┌───────────────────────┐
│ Phase 6: Verdict      │           │ Phase 5: Result & Gate│     │ Phase 4: Calibrate    │
│ Báo cáo PM: Ship/Hold │ <──────── │ Scorecard theo Slice  │ <── │ Code checks + Judge   │
└───────────────────────┘           └───────────────────────┘     └───────────────────────┘
```

### Bản đồ thực hiện theo Workspace

| Phase | Nhiệm vụ chính | Môi trường / File làm việc |
| :--- | :--- | :--- |
| **P1. Thiết kế Coverage** | Lập User Input Grid, bồi ràng buộc, sinh biến thể | Giấy / Bảng tính + AI chat cá nhân |
| **P2. Human Baseline** | Chạy tutor, chấm tay độc lập, đo đồng thuận | Repo: `eval/run_eval.py` → `eval/report.py` → `report.html` → `eval/agreement.py` |
| **P3. Formalize & Route** | Siết rubric từ bất đồng, phân làn đánh giá | Thảo luận nhóm → `deliverables/REPORT.md` (mục 3, 4) |
| **P4. Scale & Calibrate** | Viết code checks, soạn prompt judge, hiệu chuẩn | Repo: `eval/code_checks.py`, `eval/judge_prompt.md` → `eval/judge.py` |
| **P5. Phân tích & Đặt ngưỡng** | Đặt ngưỡng trước, chạy full eval, soi slice | Repo: `results.jsonl`, `report.html`, `deliverables/REPORT.md` (mục 6) |
| **P6. Ra quyết định (Verdict)** | Tổng hợp báo cáo 1 trang PM, bảo vệ Ship/Hold | `deliverables/REPORT.md` (mục 7) + `deliverables/evidence/` |

---

## 4. Nguyên Tắc & Quy Định Thực Hiện

### 7 Luật Bất Biến Của Bài Lab
1. **Con người khóa coverage trước, AI sinh biến thể sau:** Dimensions và combinations do nhóm tự chọn; AI chỉ paraphrase ngôn ngữ tự nhiên.
2. **Human labels là baseline:** LLM judge chưa calibrate **không được** dùng làm ground truth cho bất kỳ kết luận nào.
3. **Mỗi test row phải mang một risk/behavior khác biệt:** Paraphrase trùng lặp không tạo thêm coverage.
4. **Khóa threshold trước khi xem số liệu:** Đổi threshold sau khi thấy kết quả là thỏa hiệp, không phải tiêu chuẩn chất lượng.
5. **Không dùng pass rate trung bình để che regression ở critical slice:** Mọi kết luận phải kèm báo cáo phân tích theo slice.
6. **Mỗi vòng calibrate judge chỉ sửa một biến:** Đổi ít nhất có thể trong prompt và ghi rõ lý do để biết thay đổi nào tạo ra tác động.
7. **Không đổi dataset/rubric giữa chừng mà không versioning:** Mọi thay đổi phải ghi nhận phiên bản (`v1`, `v2`...) và lý do trong báo cáo.

### Quy Tắc Sử Dụng AI & Phối Hợp Nhóm
- **Được phép dùng AI:** Paraphrase câu hỏi test, brainstorm assertions cho code checks, soạn nháp judge prompt, tóm tắt pattern lệch.
- **Tuyệt đối không dùng AI:** Tự chọn dimensions/combinations thay nhóm; gắn nhãn thay con người ở Phase 2; tự bịa số liệu, trace hoặc verdict.
- **Trách nhiệm cá nhân:** Tất cả thành viên phải nắm rõ toàn bộ quy trình; giảng viên/coach có thể hỏi vấn đáp ngẫu nhiên bất kỳ thành viên nào về một label, dimension, routing choice hoặc threshold.

---

## 5. Hướng Dẫn Chi Tiết Từng Phase

---

### Phase 1: Thiết Kế Coverage (60 phút — Cuối Day 20)
*Môi trường thực hiện: Ngoài repo (Giấy / Sheet + AI chat cá nhân).*

#### 1. Chọn 3–5 Dimensions then chốt (10 phút)
Xác định các trục biến thiên khiến expected behavior của AI Tutor phải thay đổi hoàn toàn:

| Dimension gợi ý | Giá trị (Values) mẫu | Lý do làm thay đổi behavior |
| :--- | :--- | :--- |
| **Loại câu hỏi** | Trong bài / Ngoài bài / Xin đáp án / Mơ hồ | Trả lời trực tiếp → Từ chối → Hướng dẫn phương pháp → Hỏi làm rõ |
| **Độ phủ corpus** | Có sẵn trực tiếp / Rải rác nhiều tài liệu / Chỉ có một phần / Không có | Trả lời ngay → Tổng hợp nhiều nguồn → Nêu rõ giới hạn → Từ chối |
| **Độ rõ của câu hỏi** | Rõ ràng / Thiếu ngữ cảnh / Nhiều ý phức tạp | Trả lời đầy đủ → Yêu cầu clarify → Tách ý trả lời từng phần |

#### 2. Định nghĩa Values cụ thể (10 phút)
Tránh các giá trị chung chung (như *"câu hỏi khó"*). Thay bằng các tình huống cụ thể:
- *Ví dụ:* "Khái niệm calibration nằm rải rác ở cả blog lẫn slide" (yêu cầu tổng hợp) hoặc "Giá model DeepSeek không có trong corpus" (yêu cầu từ chối).

#### 3. Tổ hợp Grid & Lọc bỏ trường hợp phi lý (10 phút)
- Loại các kết hợp vô nghĩa (ví dụ: *Xin đáp án* × *Ngoài bài*).
- Chọn **12–15 combinations** đáng giá nhất dựa trên 3 tiêu chí: *Tần suất cao*, *Dễ gây lỗi*, *Hậu quả sai sót lớn (high-risk)*.

#### 4. Bồi ràng buộc đời thực (10 phút)
Tăng độ chân thực cho từng combination bằng các yếu tố:
- Thiếu ngữ cảnh (*"Cái phần hôm trước ấy..."*).
- Dùng từ mơ hồ (*"Cái ma trận đó là gì?"*).
- Giả định sai có sẵn trong câu hỏi.
- Văn phong cộc lốc, viết tắt hoặc hối thúc.

#### 5. Dùng AI Paraphrase & Con người thẩm định (15 phút)
Sử dụng Prompt sau cho AI Assistant:

```text
Bạn là học viên thật đang nhắn cho AI tutor của một khóa học online.
Tôi đang thiết kế test inputs. Nhiệm vụ: viết mỗi combination sau thành 2 câu hỏi tự nhiên.

Yêu cầu:
- Không tự thêm combination mới, không đổi intent hay độ thiếu thông tin đã cho.
- Viết như user thật: có câu ngắn cụt, câu dài vòng vo, câu thiếu context, câu hơi cộc.
- Không giải thích cách tutor nên trả lời.
- Output dạng bảng: combination_id | user_input | style | notes

Combinations:
[Dán danh sách combinations của nhóm vào đây]
```

Lọc từng câu AI sinh ra theo 3 quyết định: **Keep** (Giữ) / **Rewrite** (Viết lại) / **Reject** (Bỏ).

#### 6. Chốt Dataset v1 (5 phút)
- Hoàn thiện tập dữ liệu **20–30 rows**.
- Mỗi row gồm: `scenario_id`, `input`, và `metadata` (`dimension_values`, `expected_behavior`, `risk_if_fail`, `set_type`, `slide`).
- **Yêu cầu bắt buộc:** Phải có ít nhất **≥2 câu out-of-scope**, **≥2 câu mơ hồ**, **≥2 câu high-risk**.

> [!TIP]
> **GATE 1 — Coverage Có Chủ Đích:**
> Nhóm đạt Gate 1 khi: Mọi dimension giải thích được lý do làm đổi behavior; mỗi row có mục đích kiểm thử rõ ràng; dataset không dồn vào happy path; 100% câu do AI sinh đã qua thẩm định của con người.

---

### Phase 2: Chấm Tay Baseline & Đo Đồng Thuận (50 phút)
*Môi trường thực hiện: Trong repo (`eval/run_eval.py`, `eval/report.py`, `eval/agreement.py`).*

| Phút | Nhiệm vụ |
| :--- | :--- |
| **0–10** | Ghi dataset vào `dataset.jsonl`, bật tracing, chạy `eval/run_eval.py`, lưu backup `results-v1.jsonl`. |
| **10–30** | 3 thành viên chấm độc lập 15–20 outputs qua `report.html` (không xem nhãn của nhau). |
| **30–35** | Mỗi người xuất file `labels-<tên>.csv`. |
| **35–50** | Chạy `eval/agreement.py` đo độ lệch, thảo luận các case bất đồng, chốt nhãn vàng. |

#### 1. Chạy Dataset trên AI Tutor
1. Cấu hình file `.env` (đặt API key LLM và `BRAINTRUST_API_KEY`).
2. Ghi Dataset v1 vào file `dataset.jsonl` ở root repo theo chuẩn:
   ```json
   {"scenario_id": "G01", "input": "Cái phần đó áp dụng cho bài mình thế nào ạ?", "metadata": {"dimension_values": "trong bài / có sẵn / mơ hồ", "expected_behavior": "Hỏi lại để xác định rõ phần nào trước khi trả lời", "set_type": "challenge", "slide": {"id": "s27", "title": "User Input Grid", "keyword": "context richness"}}}
   ```
3. Thực thi đánh giá:
   ```bash
   python3 eval/run_eval.py
   ```
4. Sao lưu ngay kết quả: Copy `results.jsonl` → `deliverables/evidence/results-v1.jsonl`.
5. *(Tùy chọn)* Thử nghiệm tương tác nhanh: `python3 -i tutor/tutor.py` rồi gõ `ask_tutor("câu hỏi")`.

#### 2. Chấm độc lập qua 3 góc nhìn (Lenses)
Mỗi thành viên chạy `python3 eval/report.py` và mở `report.html` trên máy mình để chấm:
- **Góc nhìn PM:** Có đáp ứng đúng cam kết sản phẩm và intent của học viên không?
- **Góc nhìn Kỹ thuật:** Đúng định dạng JSON schema, citation tồn tại không?
- **Góc nhìn Chuyên môn:** Nội dung giải thích có chính xác theo corpus không?

*Quy tắc chấm:* Đánh giá tổng quan (`pass`/`fail`/`uncertain`). Bất kỳ tiêu chí con nào fail thì toàn bộ row bị coi là `fail`. Ghi rõ lý do vào ô note (ví dụ: `fail: citation sai section`). Xuất file `labels-<tên>.csv`.

#### 3. Đo Disagreement & Thống Nhất Nhãn Vàng
Chạy lệnh đo độ đồng thuận giữa 3 thành viên:
```bash
python3 eval/agreement.py labels-an.csv labels-binh.csv labels-chi.csv
```
- Phân tích các tiêu chí gây tranh cãi nhiều nhất.
- Thảo luận từng case bất đồng để chốt **Nhãn vàng (Gold Standard)** lưu vào `deliverables/evidence/labels.csv`.
- Ghi lại chỉ số **Human–Human Agreement tổng** (đo trước khi thảo luận) để làm trần đối chiếu cho LLM judge ở Phase 4.

> [!TIP]
> **GATE 2 — Baseline Thật:**
> Nhóm đạt Gate 2 khi: Đã có nhãn vàng cho 15–20 outputs; có chỉ số Human–Human Agreement định lượng từ vòng chấm độc lập; có danh sách các case bất đồng kèm phân tích nguyên nhân.

---

### Phase 3: Chuẩn Hóa Rubric & Phân Làn Đánh Giá (35 phút)
*Môi trường thực hiện: Thảo luận nhóm → Cập nhật `deliverables/REPORT.md` (mục 3, 4).*

#### 1. Siết Rubric từ các Case Bất Đồng (15 phút)
Chuẩn hóa từng tiêu chí gây tranh cãi theo cấu trúc:
- **Tên tiêu chí** + **Định nghĩa 1 câu ngắn gọn**.
- **Tiêu chuẩn Yes/No quan sát được** (không đánh giá cảm tính).
- **Ví dụ thực tế:** 1 mẫu Pass rõ ràng, 1 mẫu Fail rõ ràng, 1 mẫu Borderline (lấy trực tiếp từ các case bất đồng ở Phase 2).

#### 2. Xây dựng Routing Map (20 phút)
Phân loại nguyên nhân lỗi:
- **Spec Gap:** Prompt của tutor chưa mô tả rõ hành vi mong muốn → Cần sửa prompt của tutor (ghi backlog), chưa cần tạo eval.
- **Generalization Gap:** Prompt đã rõ nhưng model xử lý không ổn định → Ứng viên bắt buộc phải đưa vào eval tự động.

Phân bổ từng tiêu chí vào đúng làn đánh giá:

| Làn đánh giá | Điều kiện áp dụng | Ví dụ tiêu biểu |
| :--- | :--- | :--- |
| **Code Check** | Kiểm tra bằng luật logic / regex / determinism (rẻ, nhanh, chính xác 100%). | JSON valid schema, `doc_id` tồn tại trong manifest, `quote` nằm đúng trong section trích dẫn. |
| **LLM Judge** | Cần hiểu ngữ nghĩa ngôn ngữ tự nhiên. | Answer có được tài liệu hỗ trợ (Groundedness), câu hỏi follow-up có tính dẫn dắt sư phạm. |
| **LLM Assist** | Máy tổng hợp bằng chứng/nghi vấn, con người ra quyết định cuối. | Phát hiện câu trả lời có khả năng bị hallucination ở các chủ đề nhạy cảm. |
| **Expert (Người)** | Rủi ro cao (High-stakes) hoặc con người chưa đạt đồng thuận cao (>20% bất đồng). | Đánh giá độ sâu sư phạm chuyên sâu, ranh giới đạo đức/an toàn. |

> [!TIP]
> **GATE 3 — Rubric & Routing Bảo Vệ Được:**
> Nhóm đạt Gate 3 khi: Rubric v1 đủ rõ ràng để người ngoài nhóm đọc và chấm chính xác; mọi lựa chọn phân làn đều có lý do thuyết phục; có ít nhất một tiêu chí được giao cho Code Check.

---

### Phase 4: Tự Động Hóa & Hiệu Chuẩn LLM Judge (90 phút)
*Môi trường thực hiện: `eval/code_checks.py`, `eval/judge_prompt.md`, `eval/judge.py`.*

| Phút | Nhiệm vụ |
| :--- | :--- |
| **0–30** | Chạy 3 code checks có sẵn + Viết thêm 1–2 rule kiểm tra mới của nhóm. |
| **30–55** | Soạn `eval/judge_prompt.md` cho 2 tiêu chí, chạy thử nghiệm Judge v1. |
| **55–85** | Vòng lặp hiệu chuẩn (Calibration Loop): Phân tích Confusion Matrix → Tinh chỉnh Prompt → Chạy lại. |
| **85–90** | Đưa ra kết luận (Verdict) về độ tin cậy cho từng Evaluator. |

#### 1. Triển khai Code Checks (30 phút)
1. Chạy 3 kiểm tra mặc định:
   ```bash
   python3 eval/code_checks.py
   ```
   *(Bao gồm: `schema_valid` — JSON đúng cấu trúc; `citation_exists` — ID tài liệu có thật; `quote_verbatim` — Trích dẫn nguyên văn).*
2. Thêm 1–2 rule mới trong `eval/code_checks.py` (ví dụ: kiểm tra số lượng câu follow-up, độ dài tối thiểu của câu trả lời...).
3. So sánh kết quả code check với nhãn tay: Nếu code fail mà người pass, sửa lại logic code, không sửa nhãn người.

#### 2. Xây dựng Judge v1 (25 phút)
Soạn thảo `eval/judge_prompt.md` cho 2 tiêu chí ngữ nghĩa (ví dụ: *Groundedness* và *Follow-up quality*).
Cấu trúc chuẩn của một Judge Prompt:
- **Role:** Vai trò của judge.
- **Single Evaluation Question:** Đúng 1 câu hỏi trọng tâm cần đánh giá.
- **Observable Criteria:** Các tiêu chí quan sát cụ thể (Pass/Fail).
- **2–3 Near-Miss Examples:** Các ví dụ suýt đúng nhưng sai (hoặc ngược lại) để dạy judge ranh giới mong manh.
- **JSON Schema:** Định dạng đầu ra bắt buộc (`verdict`, `score`, `rationale`).

Thực thi judge:
```bash
python3 eval/judge.py
```

#### 3. Vòng Lặp Hiệu Chuẩn (Calibration Loop — 35 phút)
1. Chạy `python3 eval/judge.py` để xem **Confusion Matrix** đối chiếu Judge vs Nhãn vàng con người.
2. Lưu bằng chứng từng vòng:
   - `verdicts.jsonl` → `deliverables/evidence/verdicts-v1.jsonl`
   - `eval/judge_prompt.md` → `deliverables/evidence/judge-prompt-v1.md`
3. Phân tích ma trận sai lệch:
   - **Tỉ lệ nhận diện Output Tốt (Specificity):** Nếu thấp → Judge quá khắt khe/chặn nhầm (tốn công review).
   - **Tỉ lệ bắt lỗi Output Xấu (Sensitivity/Recall):** Nếu thấp → Judge quá dễ dãi/bỏ sót lỗi (cực kỳ nguy hiểm).
4. **Cách khắc phục:** Thêm 2–3 ví dụ *Near-miss* vào prompt để siết chặt tiêu chuẩn bắt lỗi.
5. Tinh chỉnh prompt sang `v2` (chỉ sửa 1 biến tại một thời điểm) và chạy lại.
6. **Xác định điểm trần:** Nếu sau 2 vòng tinh chỉnh mà độ chính xác không tăng và tiệm cận mức Human Agreement ở Phase 2 → Chấp nhận điểm trần hoặc chuyển sang làn *LLM Assist / Expert*.

#### 4. Đánh giá độ tin cậy từng Evaluator (5 phút)
Chốt vai trò cho từng tiêu chí dựa trên số liệu:
- **Tự động hóa hoàn toàn (LLM Judge):** Bắt lỗi tốt, tương đồng cao với người (kèm kiểm toán ngẫu nhiên 5–10%).
- **Bán tự động (LLM Assist):** Judge gom lỗi nghi vấn, người duyệt lại.
- **Thủ công (Expert):** Judge không đạt yêu cầu calibration.

> [!TIP]
> **GATE 4 — Calibration Có Bằng Chứng Định Lượng:**
> Nhóm đạt Gate 4 khi: Mỗi judge trải qua tối thiểu 2 vòng chạy có Confusion Matrix và phân tích pattern sai lệch rõ ràng; quyết định chọn evaluator có số liệu chứng minh.

---

### Phase 5: Phân Tích Kết Quả & Thiết Lập Ngưỡng (45 phút)
*Môi trường thực hiện: `results.jsonl`, `report.html`, `deliverables/REPORT.md` (mục 6).*

| Phút | Nhiệm vụ |
| :--- | :--- |
| **0–10** | Chốt cứng các ngưỡng chất lượng (Thresholds) ra giấy — TRƯỚC KHI chạy candidate. |
| **10–20** | Chạy full evaluation: Toàn bộ Code Checks + LLM Judges đã calibrate. |
| **20–35** | Mở `report.html`, phân tích kết quả chi tiết theo từng Slice. |
| **35–45** | Lập Scorecard tổng hợp, đọc tay tối thiểu 3 trace fail nghiêm trọng nhất. |

#### 1. Khóa Ngưỡng (Thresholds) Trước Khi Xem Số
Cam kết trước các ngưỡng chất lượng chấp nhận được:
- *Ngưỡng Critical (Không thỏa hiệp):* Schema Valid = 100%, Citation Exists = 100%, Out-of-scope Handling = 100%.
- *Ngưỡng chất lượng nội dung:* Groundedness ≥ 90%, Follow-up Quality ≥ 80%.
- *Quy định rõ:* Tiêu chí nào được phép trade-off, tiêu chí nào là blocker tuyệt đối.

#### 2. Chạy Đánh Giá Toàn Diện & Đọc Theo Slice
1. Chạy full pipeline:
   ```bash
   python3 eval/code_checks.py
   python3 eval/judge.py
   ```
2. Mở `report.html` để kiểm tra:
   - Tỉ lệ Pass tổng thể vs Tỉ lệ Pass trên từng Slice (theo từng dimension value).
   - Xác định các cụm câu hỏi có tỉ lệ rớt cao (ví dụ: nhóm câu hỏi mơ hồ, câu hỏi rải rác nhiều tài liệu).
   - Phát hiện các bất thường kỹ thuật (Pass rate = 0% thường do lỗi evaluator, không phải lỗi model).

#### 3. Lập Scorecard & Đọc Sâu Trace Thất Bại
- Lập bảng Scorecard tổng hợp điểm số theo từng tiêu chí × từng slice.
- Liệt kê các trường hợp **Regression** (những câu ở phiên bản trước pass nhưng phiên bản này fail).
- **Bắt buộc đọc tay 3 trace fail nặng nhất** để tìm nguyên nhân gốc rễ (do Retrieval, do Prompt của Tutor hay do Giới hạn của Corpus).

> [!TIP]
> **GATE 5 — Ngưỡng Trước, Số Liệu Sau:**
> Nhóm đạt Gate 5 khi: Thresholds được xác lập trước khi có kết quả candidate; có phân tích kết quả chi tiết theo slice; các ca regression và failure đều được đọc tay phân tích nguyên nhân.

---

### Phase 6: Ra Quyết Định & Bảo Vệ Sản Phẩm (20 phút)
*Môi trường thực hiện: Hoàn thiện mục 7 của `deliverables/REPORT.md`.*

#### 1. Lựa Chọn Phán Quyết (Product Verdict — 10 phút)
Nhóm chọn 1 trong 3 phán quyết:
- **SHIP:** Mọi tiêu chuẩn critical đều đạt, không có regression ở các slice quan trọng.
- **SHIP WITH CONDITIONS:** Đạt ngưỡng cơ bản nhưng đi kèm điều kiện vận hành (ví dụ: *Áp dụng LLM Judge kết hợp kiểm toán người 10% hàng tuần; thêm guardrail chặn câu hỏi out-of-scope*).
- **HOLD:** Chưa đạt ngưỡng; chỉ rõ nguyên nhân và đòn bẩy kỹ thuật cần tối ưu tiếp theo (*Prompt → Retrieval/Corpus → Fine-tuning/Model switch*).

#### 2. Hoàn Thiện Báo Cáo Executive 1 Trang (10 phút)
Báo cáo nằm tại **Mục 7 của `deliverables/REPORT.md`**, bao gồm đầy đủ 5 nội dung chuẩn PM:
1. **Dataset đã đánh giá:** Tổng số traces, độ phủ các dimensions, điểm mù (blind spots) còn tồn đọng.
2. **Quá trình đồng thuận của con người:** Tỉ lệ Human–Human Agreement vòng độc lập, nguyên nhân bất đồng lớn nhất và giải pháp chuẩn hóa rubric.
3. **Hiệu năng LLM Judge:** Model sử dụng, kết quả sau các vòng calibrate (tỉ lệ bắt lỗi xấu / nhận diện output tốt), các tiêu chí judge không thể đảm nhận.
4. **Bảng phân làn (Routing Table) & Ngưỡng chất lượng:** Ngưỡng pass cho từng tiêu chí, phân công cho Code / Judge / Assist / Expert kèm số liệu chứng minh.
5. **Verdict & Kế hoạch hành động:** Phán quyết cuối cùng + Phương án giám sát tuần đầu (nếu Ship) hoặc Kế hoạch khắc phục lỗi (nếu Hold).

---

## 6. Hướng Dẫn Nộp Bài & Cấu Trúc Repository

### Quy Định Đặt Tên Repo
Mỗi học viên nộp một repository cá nhân theo định dạng:
```text
Track1_Day21_MHV_HoVaTen
```
*(Các thành viên trong cùng nhóm dùng chung bộ dữ liệu thực hành nhưng nộp repo riêng, ghi rõ phần đóng góp cá nhân và AI Support Log của bản thân).*

### Cấu Trúc Thư Mục Nộp Bài Chuẩn

```text
Track1_Day21_MHV_HoVaTen/
├── README.md                          # Thông tin cá nhân, đóng góp, tóm tắt kết quả bài lab
├── ai-support-log.md                  # Nhật ký ghi nhận việc sử dụng AI của cá nhân
├── deliverables/
│   ├── REPORT.md                      # Báo cáo đánh giá 7 mục chi tiết (ngôn ngữ PM)
│   └── evidence/                      # Dữ liệu thô minh chứng cho từng bước
│       ├── dataset-v1.jsonl           # Bộ test inputs chuẩn của nhóm
│       ├── results-v1.jsonl           # Kết quả chạy tutor thực tế
│       ├── labels.csv                 # Nhãn vàng con người sau khi thống nhất
│       ├── labels-an.csv              # Nhãn chấm độc lập của thành viên 1
│       ├── labels-binh.csv            # Nhãn chấm độc lập của thành viên 2
│       ├── labels-chi.csv             # Nhãn chấm độc lập của thành viên 3
│       ├── judge-prompt-v1.md         # Prompt judge phiên bản 1
│       ├── judge-prompt-v2.md         # Prompt judge phiên bản 2 (sau calibrate)
│       ├── verdicts-v1.jsonl          # Kết quả chấm của judge vòng 1
│       ├── verdicts-v2.jsonl          # Kết quả chấm của judge vòng 2
│       └── braintrust-link.md         # Link truy cập project Tracing (Braintrust/LangSmith)
```

> [!IMPORTANT]
> **Nguyên tắc "3 thành phần bắt buộc" cho mỗi bước:**
> Mọi kết luận trong `REPORT.md` phải luôn đi kèm **Input** (dữ liệu đưa vào) và **Output thô** (file log/jsonl trong `evidence/`). Thiếu dữ liệu thô đối chiếu thì bước đó coi như không hợp lệ.

---

## 7. Bảng Tổng Hợp 6 Gate Đánh Giá

| Gate | Tiêu chuẩn ĐẠT | Dấu hiệu KHÔNG ĐẠT |
| :--- | :--- | :--- |
| **Gate 1: Coverage** | Dimensions thay đổi behavior rõ rệt; mỗi row có lý do tồn tại; có đủ câu OOS, mơ hồ và high-risk. | Dataset nhiều nhưng trùng lặp; dồn vào happy path; giao toàn quyền cho AI tự sinh. |
| **Gate 2: Baseline** | Chấm độc lập trước khi thảo luận; có chỉ số Agreement định lượng từ vòng độc lập. | Không chấm độc lập; ghi "thấy ổn" mà không có ghi chú lỗi; đồng thuận giả tạo. |
| **Gate 3: Rubric & Routing** | Rubric rõ ràng, khách quan; phân làn có lý do bảo vệ được; tận dụng Code check. | Giao toàn bộ cho LLM Judge vì tiện; rubric mơ hồ mang tính cảm tính. |
| **Gate 4: Calibration** | Tối thiểu 2 vòng hiệu chuẩn/tiêu chí; có Confusion Matrix đối chiếu; nhận biết điểm trần. | Chỉ đưa ra 1 con số agreement duy nhất; sửa prompt nhiều biến cùng lúc; không có near-miss examples. |
| **Gate 5: Thresholds & Slices** | Khóa threshold trước khi chạy số; phân tích kết quả theo slice; đọc tay các ca failure/regression. | Thấy số liệu rồi mới hạ threshold; chỉ báo cáo điểm trung bình tổng thể. |
| **Gate 6: Verdict** | Phán quyết Ship/Hold có evidence định lượng chống lưng; có điều kiện vận hành rõ ràng. | Ra quyết định cảm tính; thiếu kế hoạch monitoring hoặc thiếu đòn bẩy khắc phục. |

---

## 8. Checklist Kiểm Tra Trước Khi Nộp Bài

- [ ] Tên Repository đúng định dạng: `Track1_Day21_MHV_HoVaTen`.
- [ ] File `deliverables/REPORT.md` hoàn thiện đầy đủ **7 mục** có liên kết logic chặt chẽ.
- [ ] Thư mục `deliverables/evidence/` chứa đầy đủ toàn bộ file dữ liệu thô (`dataset-v1.jsonl`, `results-v1.jsonl`, `labels.csv`, `verdicts-*.jsonl`, `judge-prompt-*.md`, link Braintrust).
- [ ] Dataset v1 có tối thiểu 2 câu Out-of-scope, 2 câu Mơ hồ, 2 câu High-risk.
- [ ] Có số liệu đo lường **Human–Human Agreement** từ vòng chấm độc lập.
- [ ] Calibration report có đầy đủ **Confusion Matrix** và lịch sử thay đổi Judge Prompt qua các vòng.
- [ ] Thresholds được cam kết trước khi chạy tập candidate cuối cùng; kết quả có phân tích theo Slice.
- [ ] File `ai-support-log.md` được điền đầy đủ, trung thực bởi chính người nộp bài.