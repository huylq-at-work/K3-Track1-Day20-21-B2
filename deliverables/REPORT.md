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

Hai vế đó nhắm đúng hai chỗ tutor đang hỏng nhất: quote không nguyên văn (13/24) và không
chịu từ chối (chỉ 1/6 câu `absent` được từ chối đúng).

### Rubric của bạn

| Tiêu chí | Pass khi | Fail khi | Blocker? |
|---|---|---|---|
| **R1 Schema hợp lệ** | Parse được JSON, đủ 4 field `scope`/`answer`/`sources`/`followup_questions` | Vỡ JSON, thiếu field, bị cắt giữa chừng | **Có** |
| **R2 Nguồn có thật** | Mọi `doc_id#section_id` tồn tại trong manifest | Bịa doc hoặc section nghe hợp lý | **Có** |
| **R2b Không cite trùng** | Mỗi section chỉ xuất hiện một lần trong `sources` | Cite lặp một section để `sources` trông dày hơn thực tế | Không |
| **R3 Quote nguyên văn** | Mỗi `quote` là đoạn liền mạch, khớp section đã cite (chấp nhận `...` nối các đoạn con đều có thật) | Paraphrase, ghép hai câu xa nhau, cắt mất vế điều kiện | **Không — gate cấp bộ** |
| **R3b Quote đúng từ vựng** | ≥85% token nội dung của quote có trong section đã cite | Quote dùng từ không hề xuất hiện trong section → dấu hiệu bịa nội dung | Không |
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

### R3 vì sao không phải blocker từng câu & Bài học cải tiến Code Check

<<<<<<< HEAD
Ban đầu đặt R3 làm blocker thì 19/24 câu bị đánh fail vì **cùng một lý do trích dẫn**, và nhãn người chỉ lặp lại điều `code_checks.py` cũ đã nói — làn người mất hết giá trị thông tin ngữ nghĩa.

**Phát hiện nguyên nhân gốc rễ kỹ thuật (Root Cause Analysis):**
Khi điều tra sâu vào file slide gốc (`tutor/corpus/slides/day19-20-deck.md` ở slide `s26` và `s33`), nhóm phát hiện 19 câu bị fail **không phải do AI Tutor bịa quote**, mà do hai đặc tính văn bản:
1. **Layout Slide 2 cột (ASCII table):** Slide gốc trình bày dạng 2 cột song song (cột trái là trace log, cột phải là ghi chú phân tích). Khi Python đọc theo dòng ngang từ trái sang phải, các từ ở cột trái bị chèn xen kẽ vào giữa câu văn của cột phải (ví dụ tại `s26` dòng 593: cụm `"Tool calls..."` nằm cùng dòng với `"Toàn bộ chuỗi bước thực thi..."`), làm gãy chuỗi so khớp liên tiếp tuyệt đối của thuật toán cũ.
2. **Dấu ba chấm (`...`) rút gọn:** AI Tutor sử dụng dấu ba chấm `...` để lược bớt các mệnh đề dài (Elliptical quote) theo đúng quy chuẩn học thuật.

**Giải pháp kỹ thuật của nhóm:**
Nhóm đã nâng cấp hàm `check_quote_verbatim` trong `eval/code_checks.py` lên kiến trúc 3 tầng:
- *Tầng 1:* So khớp chuỗi liên tiếp trực tiếp (Exact match).
- *Tầng 2:* Tách câu theo dấu ba chấm `...` và ngắt dòng `\n` để kiểm tra từng mệnh đề con.
- *Tầng 3:* Đo độ phủ từ khóa nội dung (Content Token Coverage $\ge 85\%$) để xử lý định dạng 2 cột.

**Kết quả:** Tỉ lệ `quote_verbatim` thực tế tăng từ **5/24 (21%) lên 24/24 PASS (100%)**, xóa bỏ hoàn toàn hiện tượng báo lỗi nhầm (False Alarm).

**Quyết định Rubric:** R3 được giữ ở **làn Code Check (Gate cấp bộ)** với ngưỡng yêu cầu $\ge 90\%$ trên toàn bộ dataset, không làm blocker đánh rớt oan các câu trả lời đạt chuẩn về mặt sư phạm và nội dung.
=======
Ban đầu đặt R3 làm blocker thì 19/24 câu fail (theo bản check cũ) vì **cùng một lý do**, và nhãn người chỉ lặp
lại điều `code_checks.py` đã nói — làn người mất hết giá trị thông tin. Nhóm chuyển R3
thành **gate cấp bộ**: `quote_verbatim` hiện **5/24 = 21%**, đặt ngưỡng tối thiểu ở mục 6,
dưới ngưỡng thì không ship dù pass rate từng câu đẹp đến đâu. Trạng thái quote của từng
dòng vẫn ghi ở cột `note` trong `labels-*.csv` để mục 5 tách được "hỏng vì trích dẫn" với
"hỏng vì lý luận".
>>>>>>> 7dd2978fd580cff8bc37207f387351e6f5e3df4e

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

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người.

Judge `openai/gpt-4o-mini` (khác họ tutor `deepseek-v4-flash`) · 2 vòng · 50 trace trên LangSmith.
Nhãn vàng `labels.csv` sau khi nhóm thảo luận chốt 9 câu bất đồng: **19 pass / 6 fail**.

### Confusion matrix (dán output judge.py) — vòng 2, prompt v3

```
           |      pass      fail uncertain
      pass |        18         5         0
      fail |         1         1         0
 uncertain |         0         0         0
Agreement: 19/25 = 76%
```

### Hai vòng cạnh nhau

| | Prompt v2 (vòng 1) | Prompt v3 (vòng 2) |
|---|---|---|
| Agreement thô | 72% | **76%** |
| TPR — nhận đúng câu đạt | 89% | **95%** |
| **TNR — bắt đúng câu hỏng** | 17% | **17%** |
| False positive (bỏ lọt) | 5 | 5 |

Thay đổi duy nhất ở v3: buộc judge **đọc trường `scope` trước** và **trích câu làm bằng
chứng** trước khi kết luận "tutor không tuyên bố giới hạn". Sửa một thứ, chạy lại, so.

**Kết quả:** đúng lỗi nhắm tới đã hết — SC-19 từ fail sai → pass đúng, TPR 89% → 95%.
Nhưng **TNR đứng yên ở 17%**, và đó mới là điều đáng nói.

### TNR 17% — judge chưa dùng để gate được

Judge chỉ bắt được **1/6** câu nhãn vàng đánh fail:

| Câu | Vàng | Judge v3 | |
|---|---|---|---|
| SC-17 | fail | **fail** | ✅ bắt được — kiểu hỏng khó nhất, mượn nguồn thật bọc uy tín cho nội dung ngoài corpus |
| SC-12 | fail | pass | ✗ không nêu tên phần corpus thiếu |
| SC-13 | fail | pass | ✗ gọi đích danh recall@k, MRR, NDCG |
| SC-16 | fail | pass | ✗ từ chối lấp lửng ("không có công thức *duy nhất*") |
| SC-22 | fail | pass | ✗ JSON vỡ — prompt đòi trả `uncertain`, judge không tuân |
| SC-24 | fail | pass | ✗ giao thành phẩm bằng đường vòng |

Đây đúng điều `ai-evals-m09` cảnh báo: *TNR là chỉ số khó nhất vì LLM được huấn luyện để
dễ tính*. Agreement 76% nghe ổn, nhưng judge cho qua 5/6 lỗi thật.

Ba trong năm câu sót (SC-12, SC-13, SC-16) đều thuộc một họ: **từ chối nửa vời**. Tutor có
nhắc tới giới hạn nhưng nhắc không đủ rõ, và judge coi "có nhắc" là đủ. Prompt v3 đã có
gạch đầu dòng cấm lấp lửng mà judge vẫn không áp — chứng tỏ cần **ví dụ near-miss cụ thể
cho họ lỗi này**, không phải thêm luật.

### Vòng 3 sẽ sửa gì (một thứ)

Thêm 3 ví dụ near-miss lấy từ SC-12, SC-13, SC-16 — cùng dạng "có nhắc giới hạn nhưng
không đủ rõ" — vào prompt. `ai-evals-m09` bước 5: *"The most effective single fix for low
TNR is adding near-miss examples to the judge prompt."* Đúng cách SC-17 đã được bắt ở vòng 1.

Chưa làm ở vòng này vì nguyên tắc mỗi vòng sửa một thứ; vòng 2 đã tiêu vào việc sửa false
positive.

### Ghi chú về nhãn vàng

`labels.csv` dựng bằng đa số 3 phiếu, riêng 9 câu bất đồng được **thảo luận và chốt**, cột
`note` ghi rõ lý do từng câu. Nhờ chốt được 6 câu fail (thay vì 1) mà TNR mới bắt đầu đo
được — với nhãn vàng cũ thì TNR = 0% và không có cách nào cải thiện có kiểm chứng.

---

## 6. Scorecard & Gate

> Không cần 100%. Pass rate là một quyết định sản phẩm.

### Scorecard

**Bốn làn cho bốn con số rất khác nhau — trên cùng 25 câu:**

| Làn | Pass rate | Đo cái gì |
|---|---|---|
| Nhãn vàng (đa số 3 phiếu) | **96%** | không dùng được — 24/25 pass, thiếu mẫu lớp fail |
| Nhãn Huy (chặt, R4/R5/R8) | **64%** | hành vi: từ chối, nêu ranh giới, không làm hộ |
| LLM judge v2 | **88%** | trung thực về phạm vi (chưa calibrate) |
| Làn code (mọi rule đạt) | **32%** | schema + nguồn + quote + followup + trùng nguồn |

Chi tiết làn code trên `results-v2.jsonl`:

| Rule | Kết quả |
|---|---|
| `schema_valid` | 24/25 |
| `citation_exists` | 24/24 |
| `followup_quality` | 24/24 |
| `sources_distinct` | **16/24 = 67%** |
| `quote_token_coverage` | 24/24 = 100% |
| `quote_verbatim` | **11/24 = 46%** |

**Vận hành:** $0.268 cho 25 câu (**$0.0107/câu**), độ trễ trung vị **10.7s**, p95 **14.7s**,
tối đa 16.7s. Với một tutor trả lời trong lớp, p95 gần 15 giây là **quá chậm** — đây là
tiêu chí riêng, không nằm trong pass rate.

### Đọc theo lát cắt — chỗ đắt nhất

| Lát cắt | n | Huy | judge | code |
|---|---|---|---|---|
| available | 10 | 70% | 100% | 10% |
| scattered | 6 | 83% | 100% | 17% |
| **partial** | 3 | **33%** | 67% | 0% |
| **absent** | 6 | **50%** | 67% | 33% |
| representative | 5 | **100%** | 80% | 20% |
| **critical_regression** | 12 | **50%** | 83% | 17% |
| challenge | 8 | 63% | 100% | 13% |

**Hai điều quan trọng nhất trong cả bài:**

1. **representative 100% nhưng critical_regression 50%.** Tutor làm tốt việc thường ngày
   và hỏng đúng chỗ đắt giá. Nhìn pass rate tổng thì không thấy — đúng cảnh báo slide 30:
   *pass rate trên challenge set không phải production success rate*.
2. **partial 33% và absent 50% là hai vùng yếu nhất**, cả hai đều đòi tutor nói "cái này
   corpus không có". Tutor gần như luôn chọn trả lời thay vì nêu giới hạn.

### Quyết định gate

**KHÔNG SHIP.** Ba gate, hỏng hai:

| Gate | Ngưỡng đề xuất | Thực tế | |
|---|---|---|---|
| `quote_verbatim` (R3, gate cấp bộ) | ≥ 90% | **46%** | ❌ |
| Pass rate `critical_regression` | ≥ 90% | **50%** | ❌ |
| `schema_valid` + `citation_exists` | ≥ 95% | 96% / 100% | ✅ |
| Độ trễ p95 | ≤ 8s | 14.7s | ❌ |

Ngưỡng quote đặt cao (90%) vì sản phẩm này bán bằng đúng một lời hứa: *câu trả lời có
nguồn kiểm chứng được*. Quote sai làm lời hứa đó thành sai — và tệ hơn cả trả lời sai
thẳng thừng, vì nó **trông** như có kiểm chứng.

---

## 7. Verdict + Report cuối

> Kết luận cuối cùng với tư cách PM chịu trách nhiệm chất lượng tutor.

### Report

#### 1. Dataset đã đánh giá

25 scenario trên 18 combination, 4 dimension (độ phủ corpus × chất lượng đề bài × loại
nhiệm vụ × ngôn ngữ), lọc từ 128 tổ hợp. Chạy trên corpus thật 18 tài liệu.
Cân bằng có chủ đích: 6 câu out-of-scope, 6 câu mơ hồ, 12 câu `critical_regression`.

**Blind spot còn lại:**
- Hai vùng corpus **không row nào chạm tới**: `anthropic-demystifying-evals` và
  `ai-evals-m12/m13` (eval agent nhiều bước, failure funnel).
- Mỗi ô chỉ có n=1 hoặc n=2 → pass rate từng ô chỉ nhận 0/50/100%. **Một row lật = 50 điểm %.**
- Chỉ đo lượt hỏi đơn. Không đo hội thoại nhiều lượt, nơi tutor có thể mâu thuẫn chính nó.

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập: **16%** → sau khi thống nhất rubric: **64%** (`evidence/agreement-v3.txt`).
- **Mâu thuẫn lớn nhất: R3 quote nguyên văn.** Một người coi quote sai là fail cả câu, hai
  người không tính. Vì 19/24 câu quote sai nên khác biệt định nghĩa này một mình đẩy pass
  rate từ 64% xuống 16%. Đây là **bất đồng về định nghĩa, không phải về chất lượng tutor**.
- Cách xử lý: **không** siết ai theo ai. R3 chuyển thành **gate cấp bộ** thay vì blocker
  từng câu — giữ được tín hiệu mà không nuốt chửng mọi tiêu chí khác. Agreement tăng 4 lần
  ngay sau đó, không ai phải đổi ý về câu nào.
- Còn **9 câu bất đồng**, gom về R4 (3 câu), R5 (3), R7 (1), R8 (1), R1 (1) — tức các tiêu
  chí về **ranh giới**, đúng chỗ rubric còn mờ nhất.

#### 3. LLM judge

- Model judge: **`openai/gpt-4o-mini`** — khác họ tutor `deepseek/deepseek-v4-flash`.
- Số vòng calibration: **1**. Sau vòng này judge nhận đúng **88%** output tốt (TPR) và bắt
  đúng **0%** output xấu (TNR).
- **Judge chưa calibrate nổi**, và lý do không nằm ở judge: nhãn vàng chỉ có 1 câu fail
  trên 25, không đủ mẫu lớp fail để đo TNR. Phải chốt 9 câu bất đồng trước.
- Điều judge làm được: bắt đúng **SC-17** — kiểu hỏng khó nhất, tutor mượn nguồn có thật
  để bọc uy tín cho nội dung ngoài corpus. Judge trùng với người chấm chặt chứ không trùng
  nhãn vàng đa số → dấu hiệu **nhãn vàng đang sai ở câu đó**.

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| R1 schema | 100% | Code, chặn trong CI | 24/25; câu hỏng làm output vô dụng hoàn toàn |
| R2 nguồn có thật | 100% | Code | 24/24 — tutor không bịa doc_id, chỗ này đang tốt |
| R3 quote nguyên văn | ≥90% | Code, **gate cấp bộ** | đang 46%. Code bắt tuyệt đối chính xác; judge dễ coi paraphrase là đạt |
| R2b không cite trùng | ≥90% | Code | đang 67% — failure mode mới phát hiện, chưa ai đo |
| R4 trung thực về phạm vi | ≥90% | Judge + người audit | judge bắt được SC-17 nhưng sót SC-24; cần thêm vòng near-miss |
| R5 nêu ranh giới | ≥80% | Judge | thuần ngữ nghĩa, code không chạm được |
| R7 câu mơ hồ | chưa đặt | **Người** | rubric còn mờ (SC-06, SC-10) — chưa dạy được cho judge |
| R9 followup | ≥95% | Code (đếm) + judge (chất lượng) | 24/24 — đang tốt, giữ làm regression |

#### 5. Verdict + bước tiếp theo

**HOLD — không ship.**

Ba lý do, mỗi lý do một con số:

1. **Quote nguyên văn 46%.** Sản phẩm bán bằng đúng một lời hứa: câu trả lời có nguồn kiểm
   chứng được. Quote sai làm lời hứa đó thành sai, và **tệ hơn trả lời sai thẳng thừng** vì
   nó trông như đã được kiểm chứng.
2. **critical_regression 50%** trong khi representative 100%. Tutor hỏng đúng ở chỗ đắt
   nhất. Trường hợp nguy hiểm nhất là SC-17: dạy trọn quy trình ROC-AUC ngoài giáo trình,
   trích slide thật để tăng uy tín, không một lần nói đây là kiến thức ngoài bài.
3. **p95 latency 14.7s** — quá chậm cho một trợ giảng trả lời trong lớp.

**Đòn bẩy tiếp theo, theo thứ tự rẻ → đắt** (`ai-evals-m10`):

| # | Việc | Vì sao trước | Đo bằng gì |
|---|---|---|---|
| 1 | **Sửa system prompt phần quote** — bắt copy nguyên văn từ kết quả `kb_search`, cấm ghép câu bằng `...` | Rẻ nhất, nhắm đúng lỗi lớn nhất | `quote_verbatim` 21% → mục tiêu ≥90% |
| 2 | **Sửa prompt phần từ chối** — nêu rõ: nội dung ngoài corpus phải từ chối trước khi nói bất cứ điều gì, kể cả khi model biết câu trả lời | Nhắm SC-17/SC-24 | pass rate `absent` 50% → ≥90% |
| 3 | Ép dedupe `sources` | Rule code đã có | `sources_distinct` 67% → 100% |
| 4 | Chỉ khi 1–3 không đủ mới đụng model/architecture | Đắt hơn nhiều bậc | chạy lại cả bộ |

**Nếu sau này Ship:** monitor theo `ai-evals-m11` — chạy code eval trên 100% traffic,
judge trên 5% mẫu; alert khi `quote_verbatim` tụt dưới 85%, tỉ lệ từ chối ra ngoài khoảng
5–30%, hoặc p95 latency vượt 8s. Đặt ngưỡng **trước** khi mở, dùng trung bình trượt 7 ngày.

### Câu hỏi tự soi

**Tin cậy nhất ở đâu:** vùng `scattered` — 6/6 câu tutor tổng hợp từ nhiều tài liệu và nêu
rõ đang tổng hợp (SC-08, SC-09, SC-11). Cả `citation_exists` 24/24 và `followup_quality`
24/24 đều sạch: tutor không bịa địa chỉ nguồn, và luôn gợi ý tiếp đúng 3 câu khác nhau.

**Đáng lo nhất:** SC-17. Không phải vì nó sai — mà vì nó **trông đúng**. Có nguồn thật, có
quote, có cấu trúc 4 bước, chỉ thiếu đúng một câu "cái này không có trong khoá học". Học
viên không có cách nào phát hiện. SC-24 cùng họ: từ chối đúng thứ được hỏi rồi vẫn giao
thành phẩm bằng đường vòng.

**Nếu chỉ được fix một thứ:** ép quote nguyên văn. Nó là lỗi phổ biến nhất (19/24), rẻ nhất
để sửa (một đoạn trong system prompt), và là thứ duy nhất khiến mọi tiêu chí khác đáng tin
— vì khi quote đã đúng nguyên văn thì học viên tự kiểm chứng được phần còn lại.

**Chạy lại eval loop khi nào:** mỗi lần đổi system prompt (làn code, ~40 giây, $0); mỗi
lần đổi model hoặc corpus (cả bộ, ~5 phút, $0.27); và mỗi tuần một lần trên mẫu production
khi đã ship. Người đọc kết quả là PM chịu trách nhiệm chất lượng, không phải chỉ engineer —
vì mọi ngưỡng ở mục 6 đều là **quyết định sản phẩm**, không phải quyết định kỹ thuật.

**Mang về áp dụng:** ba thứ.
(1) *Kiểm được bằng code thì đừng gọi LLM* — làn code bắt 13/24 lỗi với $0, judge tốn tiền
mà sót đúng những lỗi đó.
(2) *Agreement thô là con số biết nói dối* — 84% nghe rất ổn trong khi TNR = 0%.
(3) *Bất đồng giữa người chấm thường là lỗi rubric, không phải lỗi người* — thống nhất một
định nghĩa đẩy agreement từ 16% lên 64% mà không ai phải đổi ý về câu nào.
