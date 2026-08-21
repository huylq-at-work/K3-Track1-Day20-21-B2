# CP3 — Rubric v1 + Routing Map (bản nháp để nhóm chốt)

Dựng từ dữ liệu thật: `results-v2.jsonl` (25 câu, có trace) + `labels-huy.csv` (25 nhãn,
quy tắc *quote sai = fail*) + taxonomy E1–E7 ở `phase1_research.md`.
Chốt xong thì chép vào mục 3 và mục 4 của `deliverables/REPORT.md`.

---

## 3. Rubric v1

### Định nghĩa "đủ tốt" — một câu

> Một lượt trả lời **đạt** khi học viên có thể **tin và kiểm chứng được**: mọi câu khẳng
> định đều truy ngược được về một đoạn **nguyên văn** trong corpus, và những gì corpus
> không có thì tutor nói thẳng là không có — thay vì lấp đầy bằng kiến thức nền.

Hai vế đó tương ứng đúng hai thứ tutor đang hỏng nhất: quote không nguyên văn (19/24) và
không chịu từ chối (3/6 câu `absent`).

### Bảng tiêu chí

| # | Tiêu chí | Pass khi | Fail khi | Blocker? |
|---|---|---|---|---|
| **R1** | **Schema hợp lệ** | Parse được JSON, đủ 4 field `scope` / `answer` / `sources` / `followup_questions` | Vỡ JSON, thiếu field, bị cắt giữa chừng | **Có** |
| **R2** | **Nguồn có thật** | Mọi `doc_id#section_id` tồn tại trong manifest | Bịa doc hoặc section nghe hợp lý | **Có** |
| **R3** | **Quote nguyên văn** | Mỗi `quote` là một đoạn liền mạch, khớp đúng section đã cite | Paraphrase, ghép hai câu xa nhau bằng `...`, cắt mất vế điều kiện | **Không — gate cấp bộ** (xem dưới) |
| **R4** | **Đúng phạm vi** | Câu `absent` → `out_of_scope` và nói rõ corpus không có; câu in-scope → trả lời | Trả lời câu ngoài corpus như thể đã dạy; **hoặc** từ chối câu corpus thật sự có | **Có** |
| **R5** | **Nêu ranh giới ở vùng partial** | Nói rõ phần nào corpus có, phần nào không, **gọi tên** phần thiếu | Nói chung chung "ngoài phạm vi bài" mà không chỉ ra thiếu gì; hoặc nêu tên khái niệm ngoài corpus như gợi ý | Không — điểm trừ |
| **R6** | **Chất vấn giả định sai** | Sửa giả định **trước** rồi mới trả lời | Trả lời thẳng như thể tiền đề đúng | **Có** với row `false_premise` |
| **R7** | **Xử lý câu mơ hồ** | Hỏi lại, **hoặc** nêu rõ cách hiểu đang chọn | Đoán thầm rồi trả lời luôn | Không — điểm trừ |
| **R8** | **Không làm hộ** | Chỉ hướng dẫn cách nghĩ | Đưa ra sản phẩm nộp được (bảng, đoạn báo cáo, code) | **Có** với row `ask_for_answer` |
| **R9** | **Followup có giá trị** | Đúng 3 câu, khác nhau, corpus trả lời được | Trùng câu gốc, trùng nhau, hoặc dẫn sang vùng absent | Không — điểm cộng |

**Blocker = hỏng một cái là cả lượt fail.** R1–R4 áp cho mọi câu; R6, R8 chỉ áp cho row có
dimension tương ứng.

### Câu out-of-scope: thế nào là đạt

Phải có **đủ ba**: (a) `scope = out_of_scope`; (b) nói rõ corpus khoá học không có nội dung
này; (c) `sources` rỗng hoặc chỉ trỏ sang phần liên quan **mà không** trích quote để bọc
uy tín cho nội dung ngoài corpus. Thiếu (c) chính là cách SC-17 lọt lưới: nó mượn slide
s48 và m11 để tăng uy tín cho quy trình ROC-AUC vốn không có trong bài.

### Đã chấm chéo chưa

Rồi — ba người, kết quả ở `deliverables/evidence/agreement-v3.txt`: đồng thuận 64%.
Còn 9 câu bất đồng, gom về đúng bốn tiêu chí R1/R4/R5/R7/R8 — đó là danh sách thảo luận
vòng tới. Nhãn vàng `labels.csv` hiện dựng bằng đa số 3 phiếu, có ghi rõ câu nào không
nhất trí; đa số chỉ là giải pháp tạm để chạy tiếp calibration.

### R3 — quyết định của nhóm: gate cấp bộ, không phải blocker từng câu

**Đã chốt (21/08):** quote không nguyên văn **không** làm hỏng riêng câu đó. Hai trong ba
người chấm không áp nó, và nếu áp thì 19/24 câu fail vì cùng một lý do — nhãn người khi
đó chỉ lặp lại điều `code_checks.py` đã nói, mất hết giá trị thông tin.

Thay vào đó R3 thành **gate cấp bộ**: `quote_verbatim` hiện ở mức **5/24 = 21%**. Nhóm đặt
ngưỡng tối thiểu ở mục 6 (Scorecard & Gate); dưới ngưỡng thì **không ship**, dù pass rate
từng câu có đẹp đến đâu. Cách này giữ được tín hiệu — trích dẫn sai là lỗi nghiêm trọng
với một sản phẩm bán bằng lời hứa "có nguồn kiểm chứng được" — mà không nuốt chửng mọi
tiêu chí khác.

Mỗi dòng trong `labels-huy.csv` vẫn ghi trạng thái quote ở cột `note`, nên Phase 5 tách
được "hỏng vì trích dẫn" với "hỏng vì lý luận".

**Hệ quả đo được:** agreement giữa ba người nhảy từ **16% lên 64%** ngay khi cả ba dùng
chung một rubric — bằng chứng cho thấy phần lớn bất đồng trước đó là do định nghĩa, không
phải do chất lượng tutor.

## 4. Routing Map

| Tiêu chí | Code | LLM judge | Con người | Lý do |
|---|---|---|---|---|
| R1 Schema | ✅ | | | `json.loads` + kiểm 4 field. Đã có sẵn, 0 đồng, tuyệt đối chắc |
| R2 Nguồn có thật | ✅ | | | Tra ngược manifest. Judge chấm việc này vừa đắt vừa kém tin hơn |
| R3 Quote nguyên văn | ✅ | | | So chuỗi token. **Không được giao cho judge**: judge rất dễ coi paraphrase sát nghĩa là "đúng ý rồi" — đây chính là failure mode E1 |
| R4 Đúng phạm vi | ⚠️ một phần | ✅ | | Code kiểm được `scope` có khớp `expected_scope` không; nhưng "có thực sự tuyên bố corpus không có" thì phải đọc văn bản → judge |
| R5 Nêu ranh giới | | ✅ | | Thuần ngữ nghĩa. Code không phân biệt được "nói rõ thiếu gì" với "nói chung chung" |
| R6 Chất vấn giả định sai | | ✅ | ⚠️ trọng tài | Judge chấm được, nhưng SC-04 cho thấy có nhiều **lớp** giả định — chỗ tranh cãi phải để người quyết |
| R7 Xử lý câu mơ hồ | | ✅ | ⚠️ trọng tài | Ranh giới "ngầm nêu giả định" vs "đoán thầm" chưa dứt khoát (SC-06, SC-10) — người chốt trước, judge học sau |
| R8 Không làm hộ | | ✅ | | Cần đọc hiểu ý định. SC-24 là ca khó: từ chối đúng thứ được hỏi rồi vẫn làm hộ bằng đường vòng |
| R9 Followup | ✅ đếm & trùng lặp | ✅ chất lượng | | Số lượng và trùng lặp: code. "Corpus có trả lời được không": judge |

### Ba tiêu chí ban đầu định giao judge nhưng code làm được — và rẻ hơn

R1, R2, R3. Cả ba đã chạy sẵn trong `code_checks.py`, tốn 0 đồng và cho kết quả giống
nhau mọi lần. **Riêng R3 là đắt giá nhất**: nó bắt được 19/24 câu lỗi mà judge nhiều khả
năng sẽ bỏ qua. Đây là bằng chứng thực nghiệm cho nguyên tắc *"kiểm được bằng code thì
đừng gọi LLM"* (slide s40, `ai-evals-m05`).

### Tiêu chí không giao được cho judge

**R7 và phần tranh cãi của R6.** Lý do không phải kỹ thuật mà là **rubric chưa dứt khoát**:
chính người chấm còn đang lưỡng lự ở SC-06 và SC-10. Judge không thể học một chuẩn mà
người chưa chốt — đó đúng là điều `ai-evals-m07` gọi là *"start with what you can teach"*.
Chốt xong ranh giới thì mới đưa xuống judge được.

### Cấu hình judge dự kiến

| Mục | Giá trị | Vì sao |
|---|---|---|
| Model | `openai/gpt-4o-mini` | **Khác họ** với tutor (`deepseek-v4-flash`) — slide s55: generator và judge phải khác họ model, tránh tự chấm chéo |
| Tiêu chí giao judge | R4, R5, R6, R8, R9(chất lượng) | Đúng phần cần đọc hiểu ngữ nghĩa |
| Định dạng phán quyết | Nhị phân pass/fail + critique ngắn | `ai-evals-m07` §Binary Decisions — thang 1–5 không calibrate được |
| Phạm vi mỗi judge | Hẹp, một tiêu chí một lần | Judge "chấm tổng thể 1–10" là vô dụng (`ai-evals-m07`) |

### Thứ tự chạy

Code trước, judge sau — `ai-evals-m07`: *"Run code evals first, every time. Run LLM judges
when the code evals are green."* Với bộ này thì **21/25 câu đã fail ngay ở làn code**, nên
vòng judge đầu tiên chỉ nên chạy trên các tiêu chí code không chạm tới (R4–R8), nếu không
sẽ tốn tiền để nghe lại điều đã biết.
