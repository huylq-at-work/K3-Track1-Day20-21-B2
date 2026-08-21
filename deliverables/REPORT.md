# REPORT — Eval loop A→Z: VLearn AI Tutor

Report A→Z của eval loop — mỗi mục ứng một phase của bài lab. Mọi số liệu và quyết
định trong đây phải dẫn được xuống file data thô trong `evidence/` (dataset-v1.jsonl,
results-vN.jsonl, labels.csv, judge-prompt-vN.md, verdicts-vN.jsonl, braintrust-link.md).


---

## 1. Input Grid

> Lưới input = trục "ai hỏi" × "hỏi kiểu gì". LLM giúp sinh input, con người kiểm soát
> coverage. Trả lời các câu hỏi sau rồi vẽ lưới của bạn.

- AI Tutor của bạn phục vụ những **nhóm người dùng** nào? (học viên mới, học viên đang
  làm bài, học viên ôn lại, PM khác team...?)
- Mỗi nhóm có những **ý định (intent)** hỏi nào? (hỏi khái niệm, xin ví dụ, hỏi ngoài
  lề, xin đáp án, hỏi mơ hồ...?)
- Ô nào trong lưới là **rủi ro cao** nhất (trả lời sai thì hại người học)? Ô nào **tần
  suất cao** nhất?

### Lưới của bạn

| Nhóm user \ Intent | ... | ... | ... |
|---|---|---|---|
| ... | | | |

---

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

- `dataset.jsonl` của bạn có **bao nhiêu câu**? Mỗi câu thuộc ô nào trong lưới input?
- Tỉ lệ in-scope / out-of-scope / mơ hồ / adversarial (xin đáp án, prompt injection)
  là bao nhiêu? Vì sao chọn tỉ lệ đó?
- Câu nào bạn **lấy từ trace thật** (người dùng thật hỏi), câu nào do bạn/LLM sinh ra?
- Ai đã **review** dataset? Phát hiện gì khi review (câu trùng ý, câu quá dễ, thiếu ô
  rủi ro cao)?
- Nếu chỉ được giữ 10 câu, bạn giữ 10 câu nào? Vì sao?

### Danh sách scenario (bảng tóm tắt)

| scenario_id | ô trong lưới | expected | nguồn câu hỏi |
|---|---|---|---|
| | | | |

---

## 3. Rubric v1

> Rubric = định nghĩa "đủ tốt" mà cả team chấm giống nhau. Thu hẹp scope trước khi
> viết tiêu chí.

**Chốt ngày 21/08 sau vòng chấm chéo 3 người.** Bản đầy đủ kèm lập luận: `Huy/cp3_rubric_routing.md`.

### "Đủ tốt" là gì — một câu

> Một lượt trả lời **đạt** khi học viên **tin và kiểm chứng được**: mọi khẳng định truy
> ngược được về một đoạn nguyên văn trong corpus, và cái gì corpus không có thì tutor nói
> thẳng là không có — thay vì lấp đầy bằng kiến thức nền của model.

Hai vế đó nhắm đúng hai chỗ tutor đang hỏng nhất: quote không nguyên văn (19/24) và không
chịu từ chối (chỉ 1/6 câu `absent` được từ chối đúng).

### Rubric của bạn

| Tiêu chí | Pass khi | Fail khi | Blocker? |
|---|---|---|---|
| **R1 Schema hợp lệ** | Parse được JSON, đủ 4 field `scope`/`answer`/`sources`/`followup_questions` | Vỡ JSON, thiếu field, bị cắt giữa chừng | **Có** |
| **R2 Nguồn có thật** | Mọi `doc_id#section_id` tồn tại trong manifest | Bịa doc hoặc section nghe hợp lý | **Có** |
| **R2b Không cite trùng** | Mỗi section chỉ xuất hiện một lần trong `sources` | Cite lặp một section để `sources` trông dày hơn thực tế | Không |
| **R3 Quote nguyên văn** | Mỗi `quote` là đoạn liền mạch, khớp section đã cite | Paraphrase, ghép hai câu xa nhau, cắt mất vế điều kiện | **Không — gate cấp bộ** |
| **R4 Trung thực về phạm vi** | Câu ngoài corpus → nói thẳng corpus không có, trước khi nói gì khác | Trình bày kiến thức nền như nội dung khoá học; hoặc từ chối oan câu corpus có | **Có** |
| **R5 Nêu ranh giới vùng partial** | Chỉ rõ phần nào có, phần nào không, **gọi tên** phần thiếu | Nói chung chung "ngoài phạm vi bài"; hoặc nêu tên khái niệm ngoài corpus như gợi ý | Không |
| **R6 Chất vấn giả định sai** | Sửa giả định **trước** rồi mới trả lời | Trả lời thẳng như thể tiền đề đúng | **Có** với row `false_premise` |
| **R7 Xử lý câu mơ hồ** | Hỏi lại, **hoặc** nêu rõ cách hiểu đang chọn | Đoán thầm rồi trả lời luôn | Không |
| **R8 Không làm hộ** | Chỉ hướng dẫn cách nghĩ | Giao thành phẩm nộp được (bảng, đoạn báo cáo, code) | **Có** với row `ask_for_answer` |
| **R9 Followup có giá trị** | Đúng 3 câu, khác nhau, corpus trả lời được | Trùng câu gốc, trùng nhau, hoặc dẫn sang vùng absent | Không |

**Blocker = hỏng một cái là cả lượt fail.** R1, R2, R4 áp cho mọi câu; R6 và R8 chỉ áp cho
row có dimension tương ứng.

### Câu out-of-scope: đạt khi có ĐỦ BA

(a) `scope = out_of_scope`; (b) nói rõ corpus không có nội dung này; (c) **không** trích quote
từ nguồn thật để bọc uy tín cho nội dung ngoài corpus. Thiếu (c) chính là cách SC-17 lọt
lưới — nó mượn slide s48 và module m11 để tăng uy tín cho quy trình ROC-AUC vốn không có
trong bài.

### R3 vì sao không phải blocker từng câu

Ban đầu đặt R3 làm blocker thì 19/24 câu fail vì **cùng một lý do**, và nhãn người chỉ lặp
lại điều `code_checks.py` đã nói — làn người mất hết giá trị thông tin. Nhóm chuyển R3
thành **gate cấp bộ**: `quote_verbatim` hiện **5/24 = 21%**, đặt ngưỡng tối thiểu ở mục 6,
dưới ngưỡng thì không ship dù pass rate từng câu đẹp đến đâu. Trạng thái quote của từng
dòng vẫn ghi ở cột `note` trong `labels-*.csv` để mục 5 tách được "hỏng vì trích dẫn" với
"hỏng vì lý luận".

### Chấm chéo: đã làm, và nó đổi rubric

Ba người chấm độc lập trên `results-v2.jsonl`. Kết quả ở `evidence/agreement-v3.txt`:

| | Vòng 1 (hai rubric khác nhau) | Vòng 3 (một rubric chung) |
|---|---|---|
| Cả ba nhất trí | 16% | **64%** |
| huy vs quan | 24% | 64% |
| huy vs cuong | 20% | 68% |
| quan vs cuong | 88% | 96% |

Agreement nhảy 4 lần **chỉ vì thống nhất định nghĩa**, không ai đổi ý về chất lượng tutor.
Đây là bằng chứng trực tiếp cho việc rubric mơ hồ chứ không phải người chấm cẩu thả.

**9 câu còn bất đồng** (đều một chiều: huy fail / hai bạn pass) gom về đúng bốn tiêu chí —
đây là danh sách thảo luận vòng tới, không phải danh sách "ai chấm sai":

| Tiêu chí | Câu |
|---|---|
| R4 | SC-16, SC-17, SC-18 |
| R5 | SC-10, SC-12, SC-13 |
| R7 | SC-06 |
| R8 | SC-24 |
| R1 | SC-22 |

`labels.csv` hiện dựng bằng **đa số 3 phiếu**, cột note ghi rõ câu nào không nhất trí. Đa số
chỉ là giải pháp tạm để chạy tiếp calibration — theo `ai-evals-m04` thì 9 câu trên phải
được thảo luận rồi chốt, không phải bỏ phiếu.

---

## 4. Routing Map

> Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay expert. Không phải
> tiêu chí nào cũng cần LLM.

### Bảng routing

| Tiêu chí | Code | LLM judge | Con người | Lý do |
|---|---|---|---|---|
| R1 Schema | ✅ | | | `json.loads` + kiểm 4 field. 0 đồng, tuyệt đối chắc |
| R2 Nguồn có thật | ✅ | | | Tra ngược manifest. Judge làm việc này vừa đắt vừa kém tin hơn |
| R2b Không cite trùng | ✅ | | | So sánh danh sách. Rule nhóm tự thêm |
| R3 Quote nguyên văn | ✅ | | | So chuỗi token. **Không giao judge**: judge rất dễ coi paraphrase sát nghĩa là "đúng ý rồi" — đúng failure mode E1 |
| R4 Trung thực về phạm vi | ⚠️ một phần | ✅ | | Code kiểm được `scope` khớp `expected_scope`; "có thực sự tuyên bố corpus không có" phải đọc văn bản |
| R5 Nêu ranh giới | | ✅ | | Thuần ngữ nghĩa. Code không phân biệt "nói rõ thiếu gì" với "nói chung chung" |
| R6 Chất vấn giả định sai | | ✅ | ⚠️ trọng tài | SC-04 cho thấy giả định có nhiều **lớp** — chỗ tranh cãi để người quyết |
| R7 Xử lý câu mơ hồ | | ✅ | ⚠️ trọng tài | Ranh giới "ngầm nêu giả định" vs "đoán thầm" chưa dứt khoát (SC-06, SC-10) |
| R8 Không làm hộ | | ✅ | | Cần đọc hiểu ý định. SC-24 là ca khó: từ chối đúng thứ được hỏi rồi vẫn làm hộ bằng đường vòng |
| R9 Followup | ✅ đếm & trùng lặp | ✅ chất lượng | | Số lượng/trùng lặp: code. "Corpus trả lời được không": judge |

### Định giao judge nhưng code làm được — và rẻ hơn

**R1, R2, R2b, R3.** Cả bốn chạy trong `eval/code_checks.py`, tốn 0 đồng, kết quả giống nhau
mọi lần. Riêng **R3 đắt giá nhất**: bắt được 19/24 câu lỗi mà judge nhiều khả năng bỏ qua.
Bằng chứng thực nghiệm cho nguyên tắc *"kiểm được bằng code thì đừng gọi LLM"*
(slide s40, `ai-evals-m05`).

Hai rule nhóm tự thêm: `followup_quality` (R9 — đúng 3 câu, không trùng, không lặp câu gốc)
và `sources_distinct` (R2b). Kết quả trên results-v2: followup **24/24 đạt**,
sources_distinct **8/24 hỏng** — một failure mode trước đó không ai đo.

### Không giao được cho judge

**R7 và phần tranh cãi của R6.** Lý do không phải kỹ thuật mà là **rubric chưa dứt khoát**:
chính người chấm còn lưỡng lự ở SC-06 và SC-10. Judge không học được chuẩn mà người chưa
chốt — đúng điều `ai-evals-m07` gọi là *"start with what you can teach"*.

### Cấu hình judge

| Mục | Giá trị | Vì sao |
|---|---|---|
| Model | `openai/gpt-4o-mini` | **Khác họ** với tutor `deepseek-v4-flash` — slide s55: generator và judge phải khác họ model |
| Tiêu chí giao judge | R4, R5, R6, R8, R9 (chất lượng) | Đúng phần cần đọc hiểu ngữ nghĩa |
| Phán quyết | Nhị phân pass/fail + critique ngắn | `ai-evals-m07` §Binary Decisions — thang 1–5 không calibrate được |
| Phạm vi mỗi judge | Hẹp, một tiêu chí một lần | Judge "chấm tổng thể 1–10" là vô dụng |

**judge_prompt v2** thu hẹp từ "groundedness" gộp bốn thứ xuống **một câu hỏi duy nhất**:
*tutor có trung thực về ranh giới corpus không?* Kèm 4 ví dụ sát ranh giới lấy từ chính
dataset của nhóm (`evidence/judge-prompt-v2.md`).

### Thứ tự chạy

Code trước, judge sau — `ai-evals-m07`: *"Run code evals first, every time."*

---

## 5. Calibration Report

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người. Đây là minh chứng
> cho việc đó.

- Bạn đã **gán nhãn tay** bao nhiêu row? (labels.csv, export từ report.html)
- Chạy `python3 eval/judge.py`: **agreement** giữa judge và nhãn người là bao nhiêu %? Dán
  confusion matrix vào đây.
- Judge **sai ở đâu**? (chặt quá / lỏng quá / lệch ở nhóm câu nào — in-scope hay
  out-of-scope?)
- Bạn đã sửa `eval/judge_prompt.md` thế nào sau vòng calibrate đầu? Agreement sau sửa?
- Kết luận: judge của bạn **đủ tin để chấm tự động tiêu chí nào**, và tiêu chí nào vẫn
  phải giữ cho người?

### Confusion matrix (dán output judge.py)

```
(dán ở đây)
```

---

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

- Kết quả chạy `eval/run_eval.py` + `eval/judge.py` trên dataset v1: **pass rate** theo từng tiêu
  chí là bao nhiêu? (kèm link/chỉ đường tới results.jsonl, verdicts.jsonl, report.html)
- Chi phí 1 vòng eval là bao nhiêu ($, token)? Latency trung bình 1 câu?
- **Gate**: ngưỡng nào thì ship? Ví dụ: groundedness pass ≥ 90%, không có fail nào ở
  nhóm blocker... — định nghĩa ngưỡng của bạn và giải thích vì sao.
- Kết quả hiện tại: **SHIP hay CHƯA SHIP**? Căn cứ vào gate ở trên.
- Nếu chưa ship: 3 lỗi lớn nhất cần fix ở tutor (prompt, retrieval, corpus)?

### Scorecard

| Tiêu chí | Pass | Fail | Uncertain | Pass rate |
|---|---|---|---|---|
| | | | | |

### Quyết định gate

**SHIP / CHƯA SHIP** — vì: ...

---

## 7. Verdict + Report cuối

> Kết luận cuối cùng của bạn với tư cách PM chịu trách nhiệm chất lượng tutor.
> Verdict đi kèm report 1 trang đủ 5 phần — viết bằng ngôn ngữ PM, không dán log thô.

### Report

#### 1. Dataset đã đánh giá

(tập nào, bao nhiêu traces, coverage chính là gì, blind spot nào còn lại)

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập (nhãn tổng): ___% — kèm thống kê từ note: tiêu chí nào gây bất đồng nhiều nhất
- Mâu thuẫn lớn nhất: (case/tiêu chí nào, hai phía nghĩ gì)
- Nhóm xử lý bằng cách nào: (siết định nghĩa / đổi thang / bỏ tiêu chí...)

#### 3. LLM judge

- Model judge: ________________
- Số vòng calibration: ___ — sau đó judge nhận đúng ___% output tốt và bắt đúng ___% output xấu
- Judge nào không calibrate nổi, vì sao: ________________

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| vd: groundedness | ≥90% | LLM judge + audit 10%/tuần | bắt đúng 91% output xấu sau 2 vòng near-miss |
|  |  |  |  |
|  |  |  |  |

#### 5. Verdict + bước tiếp theo

**Ship / Ship with conditions / Hold** — vì: ________________

- Nếu Ship: monitoring tuần đầu xem gì, sample bao nhiêu %, alert ở ngưỡng nào?
- Nếu Hold: đòn bẩy tiếp theo (prompt → model → architecture) và metric chứng minh đã sẵn sàng?

### Câu hỏi tự soi

- Tin cậy nhất ở đâu, đáng lo nhất ở đâu? (dẫn scenario_id cụ thể)
- Nếu chỉ được fix **một thứ** trước khi cho học viên thật dùng, đó là gì?
- Eval loop này sẽ chạy lại **khi nào** (mỗi lần đổi prompt? mỗi tuần? khi corpus đổi?) và ai nhìn kết quả?
- Điều gì trong bài này bạn sẽ **mang về áp dụng** vào sản phẩm thật của mình?
