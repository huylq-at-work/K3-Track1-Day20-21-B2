# Phase 1 — Tài liệu nền & Menu dimensions
**VLearn AI Tutor · Coverage Design · Day 20 (60')**
Trạng thái: *nghiên cứu xong — chờ nhóm CHỐT dimensions*

---

## 0. Tóm tắt 30 giây

Tôi đã đọc slide Day 20–21 (66 trang) và dựng bản đồ corpus thật của khoá học (2 bài Hamel + AI Engineering Ch.3, Ch.4). Ba thứ dùng được ngay:

1. **Bản đồ corpus 4 tầng** — 30+ khái niệm được xếp vào AVAILABLE / SCATTERED / PARTIAL / ABSENT. Đây là thứ biến "độ phủ corpus" từ một chữ trong bảng thành một trục test có bằng chứng.
2. **Taxonomy 37 failure mode** của tutor, gom thành 7 nhóm — nguyên liệu cho trace codes ở Phase 3 và rubric ở Phase 4.
3. **Menu 9 dimension ứng viên**, mỗi cái đã chạy sẵn phép thử "đổi value → hành vi đúng có đổi không" (slide 26). Nhóm chỉ cần gạch bỏ, không cần nghĩ từ đầu.

**Việc nhóm phải tự làm (không giao được):** chốt lấy dimension nào, bỏ cái nào, và vì sao. Mục 4 là chỗ để làm việc đó.

---

## 1. Slide nói gì về Phase 1 — bốn câu phải thuộc để bảo vệ trước coach

| Slide | Câu chốt | Hệ quả cho bài của nhóm |
|---|---|---|
| **26** | "Đổi giá trị → hành vi đúng có đổi không? Không đổi → chỉ là paraphrase." | Đây là *phép thử duy nhất* để một thuộc tính được lên grid. Slide lấy ví dụ **"cách diễn đạt (lịch sự / cộc lốc / câu hỏi)" là KHÔNG phải dimension** — 3 giá trị, vẫn 1 hành vi. Nếu nhóm đưa "tone" hay "độ dài câu" lên trục, coach sẽ bắt bằng đúng slide này. |
| **25** | "50 rows LLM sinh ≈ 3 case thật · 20 rows thật = 20 case thật" (Si & Yang 2024: xin 4.000 ý → còn ~200 ý không trùng) | Bảo vệ được vì sao dataset chỉ 20–30 rows mà vẫn đủ. Số rows không phải KPI. |
| **27** | "Ô ≠ dòng dataset. Coverage = chọn ô có chủ đích — biết rõ vì sao chọn ô này, bỏ ô kia." | Mỗi ô bị loại cũng phải có lý do ghi lại. Phần "loại vì phi lý" là deliverable, không phải rác. |
| **30** | 3 loại scenario: **Representative** (giống production) · **Challenge** (cố ý over-sample) · **Critical regression** | Đây chính là cột `set_type`. Slide còn cảnh báo: *"Pass rate trên challenge set không phải production success rate"* — câu này sẽ cần lại ở Phase 5. |

Slide 30 còn liệt kê sẵn 4 **critical regression candidate** cho đúng loại sản phẩm này:
> Claim ngoài bị nói thành nội dung đã dạy · Citation không support claim · Agent reasoning từ false premise · View source dẫn tới source không liên quan

→ Bốn cái này nên có mặt trong dataset dưới dạng row high-risk. Chúng là gợi ý từ chính giảng viên.

**Một lệch cần biết:** slide 29 nói phễu `64 tổ hợp → 15–20 scenario → 40–50 test input`. Đề lab Phase 1 chỉ yêu cầu `12–15 combinations → 20–30 rows`. **Theo đề lab** — nhưng nếu coach hỏi "sao ít hơn slide", trả lời: đề bài Phase 1 chốt ở 20–30 rows để Phase 2 chấm tay kịp trong 50 phút; slide mô tả quy mô đầy đủ của một eval suite thật.

---

## 2. Bản đồ corpus — thứ làm cho "độ phủ" trở thành trục test được

Corpus = **D1** Hamel, *Your AI Product Needs Evals* · **D2** Hamel, *Creating a LLM-as-a-Judge That Drives Business Results* · **D3** *AI Engineering* Ch.3 Evaluation Methodology · **D4** *AI Engineering* Ch.4 Evaluate AI Systems · + slide khoá học.

### 2.1 AVAILABLE — nằm gọn trong MỘT section, tutor trả lời trực tiếp + quote được

3 cấp eval Level 1/2/3 (D1) · assertion/unit test cho LLM (D1) · định nghĩa **trace** — có câu nguyên văn (D1) · "remove all friction" (D1) · fine-tune vs RAG (D1) · Principal Domain Expert (D2) · Features/Scenarios/Personas (D2) · binary pass/fail + critique (D2) · quy tắc **"~30 ví dụ, dừng khi hết failure mode mới"** (D2) · Critique Shadowing 7 bước (D2) · guardrail ≠ judge (D2) · perplexity & cross-entropy (D3) · functional correctness (D3) · BLEU/ROUGE = lexical similarity "khá thô" (D3) · 4 bias của judge: self / verbosity / position / inconsistency (D3) · reward model vs preference model (D3) · **local vs global factual consistency** — có định nghĩa nguyên văn (D4) · TTFT/TPOT (D4) · model selection 4 bước (D4) · data contamination (D4) · "guideline phải định nghĩa cả should-do **và** shouldn't-do" (D4) · component-level eval (D4).

### 2.2 SCATTERED — phải tổng hợp từ ≥2 tài liệu (đây là mỏ vàng của dataset)

| Khái niệm | Ở đâu và đâu | Vì sao khó |
|---|---|---|
| **LLM-as-a-judge toàn cảnh** | D1 §Automated Eval + D2 (cả bài) + D3 §AI as a Judge | D1 cho vị trí trong hệ thống, D2 cho quy trình, D3 cho danh mục bias — thiếu nguồn nào cũng lệch |
| **Đánh giá chính judge (meta-eval)** | D1 §Automated Eval + D2 §FAQ + D4 §Step 3 | Cả 3 đều cảnh báo agreement thô, nhưng mỗi nơi một góc |
| **Human eval còn cần không** | D1 Level 2 + D2 Step 3/6/FAQ + D3 Summary | Câu trả lời đúng nằm ở giao của 3 nguồn |
| **Synthetic data cho eval** | D1 §Step 2 + D1 §Data Synthesis + D2 §Generating Synthetic Data | Cả hai chỉ sinh **input**, không sinh đáp án chuẩn |
| **Error analysis** | D2 §Step 6 + D1 §Step 2/§Debugging | |

### 2.3 PARTIAL — corpus chạm một phần, tutor phải tuyên bố giới hạn

| Chủ đề | Corpus CÓ | Corpus THIẾU |
|---|---|---|
| **Đánh giá RAG** | local factual consistency, eval từng component | context precision/recall, recall@k, MRR/NDCG, chunking, reranking, RAGAS |
| **Online eval / monitoring** | A/B test là Level 3; monitor sau khi chọn model | thiết kế thí nghiệm online, drift detection, canary/shadow, sampling rate |
| **Thống kê cho eval** | cảnh báo imbalance → dùng precision/recall | công thức TPR/TNR, Cohen's kappa, khoảng tin cậy, tính cỡ mẫu |
| **Eval agent nhiều bước** | eval intermediate output, per-turn | tool-call accuracy, đo theo quỹ đạo, đánh giá planning |
| **Cost/latency** | định nghĩa TTFT/TPOT, coi là criteria | giá thật của model nào, caching/batching/quantization |

### 2.4 ABSENT — tutor phải TỪ CHỐI

Giá API & gói dịch vụ · điểm MMLU/SWE-bench của model cụ thể · "model nào đang top LMArena" · kiến trúc Transformer/attention · LoRA/hyperparameter fine-tune · RLHF/DPO · EU AI Act, GDPR, ISO 42001 · tin model mới ra tuần này · so sánh LangSmith vs Braintrust.

**Nhóm 6 — bẫy nguy hiểm nhất:** kỹ thuật eval nghe *rất giống* corpus nhưng nằm ở tài liệu NGOÀI corpus:
- ROC-AUC / PR-AUC, NLI-based faithfulness, chrF/BLEURT/COMET → chỉ có ở **Eugene Yan**, không có trong D1–D4
- axial coding / open coding, capability funnel, criteria drift (phân tích đầy đủ) → chỉ có ở **Field Guide** của Hamel
- ⚠️ **SỬA v1.1 — khẳng định cũ ở đây SAI.** Trước đó tôi ghi con số ">90% agreement" thuộc Field Guide, ngoài corpus. Đã kiểm trực tiếp `hamel.dev/blog/posts/llm-judge/` (= **D2, trong corpus**): câu nguyên văn là *"It took us only three iterations to achieve > 90% agreement between the LLM and Phillip."* Con số này **CÓ trong corpus**. Giả định sai thật sự trong câu hỏi của học viên là hai thứ khác: gán cho **Chip Huyen** (thực ra là Hamel/D2), và biến một **kết quả case study** thành **ngưỡng bắt buộc để ship**.

→ Đây là nguồn sinh câu hỏi ABSENT tốt nhất: học viên đọc thêm blog khác, hỏi bằng thuật ngữ nghe rất "trong bài", tutor rất dễ gật.

### 2.5 22 cặp khái niệm dễ nhầm (rút gọn 8 cặp đắt nhất)

| Cặp | Nhầm lẫn thường gặp |
|---|---|
| Offline eval ↔ Online eval / A/B test | Tưởng offline pass = sản phẩm chắc chắn tốt hơn |
| Vibe check ↔ systematic eval | Tưởng "nhìn dữ liệu bằng tay" = vibe check (D1/D2 **bắt buộc** nhìn tay, nhưng có cấu trúc) |
| LLM judge ↔ human eval | Tưởng judge **thay** người; thực ra judge chỉ *khuếch đại* phán quyết của người |
| Code check ↔ LLM judge | Dùng judge cho thứ đáng lẽ là `assert` (JSON hợp lệ, độ dài) |
| **Alignment của judge ↔ calibration nghĩa xác suất** | Nghe "calibrated scale 1–5" trong D2 rồi tưởng là calibration xác suất |
| Agreement thô ↔ precision/recall | "Judge khớp người 95%" bị hiểu là judge tốt (95% dataset là pass thì judge nói "pass" luôn cũng được 95%) |
| **Local ↔ global factual consistency** | Chấm RAG bằng global → thưởng nhầm khi model bịa từ kiến thức nền |
| Hallucination ↔ retrieval failure | Gộp mọi câu sai thành hallucination → đi sửa prompt trong khi lỗi ở retriever |

### 2.6 Câu hỏi bẫy chứa giả định sai (rút 10/25)

1. "Dùng BLEU chấm tutor này thế nào?" → giả định output open-ended có reference chuẩn
2. "Cần bao nhiêu **nghìn** test case?" → giả định có con số cố định, càng nhiều càng tốt
3. "Judge GPT-4 rồi thì khỏi cần người chấm đúng không?" → giả định judge tự nó đáng tin
4. "Judge em agreement 95% với người, xong chứ?" → giả định agreement thô là đủ
5. "Perplexity bao nhiêu thì tutor được coi là tốt?" → giả định perplexity đo chất lượng sản phẩm
6. "Chip Huyen nói agreement phải trên 90% đúng không?" → **gán sai nguồn + sai loại**: con số >90% CÓ trong D2 (Hamel), nhưng là kết quả một case study sau 3 vòng lặp chứ không phải ngưỡng. *(Sửa ở v1.1 — bản đầu ghi sai rằng corpus không có con số này.)*
7. "Hamel khuyên dùng axial coding trong error analysis, giải thích giúp?" → **gán sai nguồn** — thuật ngữ này ở Field Guide, D1/D2 chỉ nói "classify traces by hand". *(Chưa xác minh lại ở v1.1 — nằm trong danh sách cần kiểm.)*
8. "Fine-tune tutor để nó hết bịa, learning rate bao nhiêu?" → 2 giả định sai chồng nhau
9. "Chạy A/B test trước rồi mới viết unit test cho nhanh?" → đảo ngược thứ tự chi phí Level 1→3
10. "Đổi judge từ GPT-4 sang model rẻ hơn, điểm cũ vẫn so sánh được chứ?" → D3 nói rõ điểm giữa các judge **không** so sánh chéo được

---

## 3. Taxonomy failure mode của tutor (37 mode / 7 nhóm)

Schema output: `{answer, sources: [{doc, section, quote}], followup_questions[3]}`

| Nhóm | Failure mode tiêu biểu | Ai chấm được (dự kiến Phase 3) |
|---|---|---|
| **E1 · QUOTE** | quote bịa hoàn toàn · **paraphrase bị coi là nguyên văn** · ghép 2 câu xa nhau thành 1 · quote có thật nhưng không hỗ trợ claim · cắt mất vế điều kiện làm đảo ý | exact-string match = **code**; "có support claim không" = **judge** |
| **E2 · CITATION** | đúng doc sai section · nhầm D1↔D2, Ch.3↔Ch.4 · bịa heading nghe hợp lý · **gán ý của Field Guide/Eugene Yan cho D1/D2** · sources rỗng khi answer khẳng định mạnh | doc/section có tồn tại = **code**; gán đúng nguồn = **judge** |
| **E3 · PHẠM VI** | trả lời câu ABSENT không từ chối · trả lời PARTIAL như thể đầy đủ · **trộn kiến thức nền vào answer đã grounded** (khó phát hiện nhất) · over-refusal câu thật ra có trong corpus · từ chối câu SCATTERED vì không thấy ở một chỗ | **judge** |
| **E4 · GIẢ ĐỊNH** | không chất vấn giả định sai · trả lời tự tin khi câu mơ hồ · **bịa con số/ngưỡng** ("cần ≥90% agreement") · trộn 2 khái niệm gần nhau · nói corpus đồng thuận trong khi 3 nguồn có sắc thái khác nhau | **judge** (một phần con số bịa = code) |
| **E5 · FOLLOWUP** | trùng câu hỏi gốc · 3 câu trùng nhau · dẫn sang chủ đề ABSENT · corpus không trả lời được · không phải câu hỏi · sai số lượng ≠ 3 | đếm & trùng lặp = **code**; chất lượng = **judge** |
| **E6 · SCHEMA** | JSON không parse (rất dễ vỡ vì `quote` chứa dấu `"`) · markdown fence bao quanh · sai tên field · thiếu `section` · thừa field · **lỗi encoding smart-quote làm exact match trượt dù nội dung đúng** | **code** 100% |
| **E7 · SƯ PHẠM** | đúng nhưng bỏ cảnh báo quan trọng · không phân biệt "corpus nói" vs "thực tiễn phổ biến" · **hỏi tiếng Việt trả lời tiếng Anh** (lưu ý: `quote` thì PHẢI giữ nguyên tiếng Anh) | **judge** / một phần **human** |

Chưa cần dùng ở Phase 1 — nhưng biết trước 7 nhóm này giúp chọn combination có mục đích: mỗi combination nên nhắm vào ít nhất một nhóm.

---

## 4. MENU DIMENSIONS — phần nhóm phải chốt

Mỗi ứng viên đã chạy sẵn phép thử slide 26. Cột cuối là **đề xuất của tôi**, không phải quyết định.

### ✅ D-A · Độ phủ corpus — *đề xuất: LẤY, làm trục xương sống*

| Value | Hành vi đúng đổi thế nào | Nguồn |
|---|---|---|
| `available` | Trả lời trực tiếp, cite 1 nguồn, quote nguyên văn | §2.1 |
| `scattered` | **Tổng hợp ≥2 doc**, cite từng nguồn, nói rõ đây là tổng hợp | §2.2 |
| `partial` | Trả lời phần có + **tuyên bố rõ phần corpus không có** | §2.3 |
| `absent` | **Từ chối**, không bịa quote, gợi ý nơi khác | §2.4 |

4 value → 4 hành vi khác hẳn nhau. Đây là dimension mạnh nhất và đã có bằng chứng cụ thể ở §2. Slide 28 cũng dùng chính nó làm ví dụ cho AI Tutor.

### ✅ D-B · Chất lượng đề bài — *đề xuất: LẤY*

| Value | Hành vi đúng |
|---|---|
| `rõ & đủ` | Trả lời ngay |
| `thiếu chỉ trỏ` ("cái bài hôm trước", "cái ma trận đó") | **Hỏi lại** để xác định, hoặc nêu rõ giả định đang dùng |
| `nhiều ý trong 1 câu` | **Tách và trả lời cả hai**, không bỏ sót ý thứ hai |
| `chứa giả định sai` | **Sửa giả định TRƯỚC**, rồi mới trả lời phần còn lại |

4 value → 4 hành vi. Slide 26 dùng đúng trục này ("độ đủ thông tin") làm ví dụ dimension **hợp lệ**. Giá trị `giả định sai` là nơi bắt failure mode E4 và trùng với critical regression "Agent reasoning từ false premise" (slide 30).

> **Điểm tranh luận đáng để nhóm cãi nhau:** nên tách `giả định sai` thành dimension riêng (Tính đúng của tiền đề: đúng/sai) hay để làm 1 value của D-B? Tách ra thì grid nở gấp đôi; gộp lại thì D-B trộn 2 loại khiếm khuyết khác nhau (thiếu thông tin vs sai thông tin). **Tôi nghiêng về gộp** ở quy mô 12–15 combination — nhưng ghi lại lý do vào biên bản, coach hay hỏi đúng chỗ này.

### ✅ D-C · Loại nhiệm vụ — *đề xuất: LẤY*

| Value | Hành vi đúng |
|---|---|
| `giải thích khái niệm` | Định nghĩa + quote nguyên văn |
| `phân biệt cặp dễ nhầm` | Nêu **cả hai chiều** khác biệt, không trộn (§2.5) |
| `áp dụng vào tình huống của học viên` | Suy luận có điều kiện, **nêu rõ giả định**, không khẳng định như fact trong corpus |
| `nhờ làm hộ / xin đáp án` | **Không đưa đáp án**, hướng dẫn cách nghĩ |

### ⚠️ D-D · Ngôn ngữ & thuật ngữ — *đề xuất: LẤY nếu còn chỗ, chọn 2 value*

`tiếng Việt thuần` (thuật ngữ dịch: "chấm chéo", "bộ chấm") ↔ `Việt trộn thuật ngữ Anh` ("cái grounding á").
Hành vi đổi: answer phải theo ngôn ngữ người hỏi, **nhưng `quote` bắt buộc giữ nguyên tiếng Anh** — mâu thuẫn này là một failure mode thật (E7 #37). Value "tiếng Việt thuần" còn tạo áp lực retrieval: corpus tiếng Anh, câu hỏi không có từ khoá trùng.

### ⚠️ D-E · Persona / giai đoạn học — *đề xuất: CÂN NHẮC*

`học viên mới` / `giữa khoá` / `ôn thi`. Slide 28 liệt kê Persona là dimension phổ biến. Nhưng phải trả lời được: hành vi **đúng** đổi hay chỉ *độ dài / độ sâu* đổi? Nếu rubric Phase 3 không có tiêu chí "độ sâu phù hợp người hỏi" thì đây là trục **không chấm được** → thành paraphrase trá hình. Lấy thì phải cam kết viết tiêu chí đó.

### ❌ D-F · Cách diễn đạt / tone (lịch sự · cộc lốc · dạng câu hỏi) — *LOẠI*
Slide 26 dùng chính cái này làm ví dụ **không phải dimension**: 3 giá trị → vẫn 1 hành vi.

### ❌ D-G · Độ dài câu hỏi (ngắn / dài vòng vo) — *LOẠI*
Cùng lý do. Đây là **constraint bồi ở Bước 4**, không phải trục grid.

### ❌ D-H · Failure cost / mức rủi ro — *LOẠI khỏi trục, dùng làm TAG*
Đây là **tiêu chí chọn ô** (slide 27) và là cột `risk_if_fail` + `set_type` trong dataset, không phải thuộc tính của input. Đưa lên trục sẽ trộn "input là gì" với "ta quan tâm gì".

### ❌ D-I · Có cần research ngoài không — *LOẠI vì trùng D-A*
Đã nằm trong `absent` của D-A. Hai trục trùng nhau không tạo thêm coverage (luật lab #3).

---

## 5. Phễu tổ hợp nếu chốt theo đề xuất

```
D-A (4) × D-B (4) × D-C (4) × D-D (2) = 128 tổ hợp
     ↓ loại phi lý
  ~40 tổ hợp còn nghĩa
     ↓ chọn có chủ đích (thường gặp · dễ sai · failure cost cao · có ambiguity · team chưa chắc boundary)
  12–15 combinations   ← Bước 3
     ↓ bồi ràng buộc đời thực + LLM paraphrase ×2 → human Keep/Rewrite/Reject
  20–30 rows Dataset v1   ← bắt buộc ≥2 out-of-scope · ≥2 mơ hồ · ≥2 high-risk
```

**Ví dụ tổ hợp phi lý cần loại (ghi lại làm bằng chứng):**
- `absent` × `xin đáp án` — không có bài tập nào ngoài corpus để mà xin đáp án
- `absent` × `phân biệt cặp dễ nhầm` — không phân biệt được hai thứ corpus không có
- `available` × `giả định sai` **không** phi lý — ngược lại đây là ô đắt nhất: câu hỏi về thứ corpus CÓ nhưng tiền đề sai (vd "Chip Huyen nói agreement phải >90% đúng không?")

---

## 6. Ba câu hỏi nhóm phải trả lời trước khi sang Bước 3

1. **Lấy 3 hay 4 dimension?** 3 (A+B+C) → grid gọn, dễ bảo vệ, nhưng bỏ mất trục ngôn ngữ vốn rất thật với học viên Việt. 4 → phủ tốt hơn, nhưng 12–15 ô sẽ thưa trên 128 tổ hợp, phải giải thích được vì sao ô này chứ không phải ô kia.
2. **`giả định sai` — value của D-B hay dimension riêng?** (xem hộp tranh luận ở D-B)
3. **Có lấy Persona không?** Chỉ lấy nếu nhóm cam kết viết được tiêu chí rubric chấm được nó ở Phase 3.

---

## 7. AI Support Log — Phase 1 (ghi tiếp khi làm)

| # | Bước | Dùng AI làm gì | Con người làm gì | Kết quả |
|---|---|---|---|---|
| 1 | Chuẩn bị | Claude đọc slide Day 20–21, dựng bản đồ corpus 4 tầng + taxonomy 37 failure mode + menu 9 dimension ứng viên | Nhóm đọc, chốt lấy/bỏ từng dimension | *(đang chờ)* |
| 2 | Bước 1–2 | — | Nhóm tự chốt dimensions & values | |
| 3 | Bước 3 | — | Nhóm tự loại tổ hợp phi lý & chọn 12–15 ô | |
| 4 | Bước 5 | AI paraphrase combination → 2 câu tự nhiên | Nhóm quyết Keep / Rewrite / Reject từng câu | |

> Lưu ý tuân thủ luật lab: mục 4 là **menu để nhóm chọn**, không phải grid đã chốt. Việc AI không được làm — tự chọn dimensions/combinations — vẫn thuộc về nhóm.

---

> **Nhật ký sửa** · v1.1 (21/08/2026): sửa khẳng định về con số ">90% agreement" ở §2.4 và §2.6 sau khi kiểm trực tiếp trên hamel.dev. Bài học rút ra và đã áp vào Dataset v1.1: mọi khẳng định *"KHÔNG có trong corpus"* phải kèm bằng chứng đã tìm (từ khoá đã search, kết quả 0 hit), không được suy đoán từ trí nhớ. Danh sách còn phải kiểm trên D3/D4 và slide: `kappa` · `ROC-AUC` · `NLI` · `axial coding` · `recall@k` · `MRR` · `drift`.

*Nguồn: slide `day2021.pdf` (AI IN ACTION Day 20–21 Track 1, Mai Anh Nguyen) · [hamel.dev/blog/posts/evals](https://hamel.dev/blog/posts/evals/) · [hamel.dev/blog/posts/llm-judge](https://hamel.dev/blog/posts/llm-judge/) · [AI Engineering Ch.3](https://www.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html) · [Ch.4](https://www.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html) · ngoài corpus (dùng để sinh câu ABSENT): [Field Guide](https://hamel.dev/blog/posts/field-guide/) · [Eugene Yan](https://eugeneyan.com/writing/evals/)*
