# Bảng trace tay — Dataset v1.3 (25 câu)

In ra hoặc mở song song khi chấm. Mỗi câu: đọc **Câu hỏi** → xem tutor trả lời → đối chiếu **Đúng phải thế nào** → ghi Pass/Fail + lý do ngắn.

| Cột | Nghĩa |
| --- | --- |
| Vùng corpus | tài liệu có nội dung đó không: available (có) · scattered (rải rác nhiều quyển) · partial (có một nửa) · absent (không có → tutor phải từ chối) |
| Loại | representative = giống câu hỏi thật · challenge = cố tình khó · critical_regression = sai là hỏng nặng |

---

## AVAILABLE — corpus có, tutor phải trả lời thẳng (10 câu)

### SC-01 · CB-01 · representative

**Câu hỏi học viên:**

> trace là gì vậy ạ, em thấy slide nhắc suốt mà vẫn chưa rõ

*Bối cảnh: học viên đang xem slide s26 — "Trace là gì, và vì sao PM phải đọc trace"*

**Trục:** `corpus=available | input=clear | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
Trả lời trực tiếp định nghĩa trace; đúng 1 source = D1 §Logging Traces; quote NGUYÊN VĂN khớp exact-string với câu "A trace is a concept that has been around for a while in software engineering and is a log of a sequence of events…"; 3 followup khác nhau và đều trả lời được bằng corpus.

**Sai thì hại gì:** Nếu quote không nguyên văn hoặc sai section ở ngay ô dễ nhất, mọi pass rate ở các ô khó hơn đều không đáng tin.

**Nguồn được phép cite:** `hamel-evals#logging-traces` · `ai-evals-m04#lesson-1-what-is-a-trace`

**Lỗi cần soi:** E1 · E6

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
| Huy |  |  |

---

### SC-02 · CB-02 · representative

**Câu hỏi học viên:**

> kiểm bằng code với để một con AI khác chấm thì khác nhau ở đâu ạ, khi nào nên dùng cái nào

*Bối cảnh: học viên đang xem slide s40 — "Chọn cách đánh giá: Code-based hay LLM-as-Judge?"*

**Trục:** `corpus=available | input=clear | task=distinguish_pair | lang=vi_pure`

**Đúng phải thế nào:**
Nêu CẢ HAI CHIỀU: code check nhanh/rẻ/xác định/chạy được trong CI nhưng chỉ bắt được rule rõ; judge bắt được sắc thái nhưng đắt, có bias và phải calibrate. Cite D1 §Level 1 và §Level 2.

**Sai thì hại gì:** Trộn hai khái niệm → học viên dùng judge cho việc đáng lẽ là assert, vừa đắt vừa kém tin cậy hơn.

**Nguồn được phép cite:** `hamel-evals#level-1-unit-tests` · `hamel-evals#level-2-human-model-eval` · `ai-evals-m05#choosing-the-automation-method-code-based-vs-llm-as-judge` · `ai-evals-m07#when-to-use-llm-as-judge`

**Lỗi cần soi:** E4 #20

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
| Huy |  |  |

---

### SC-03 · CB-02 · representative

**Câu hỏi học viên:**

> em không phân biệt được hai cái: viết luật cho máy tự kiểm, với bắt mô hình chấm. chọn kiểu gì ạ

*Bối cảnh: học viên đang xem slide s40 — "Chọn cách đánh giá: Code-based hay LLM-as-Judge?"*

**Trục:** `corpus=available | input=clear | task=distinguish_pair | lang=vi_pure`

**Đúng phải thế nào:**
Như SC-02, CỘNG tiêu chí riêng: phải làm rõ ranh giới hai khái niệm ngay trong ĐOẠN ĐẦU, trước khi đi vào chi tiết kỹ thuật của từng cái.

**Sai thì hại gì:** Bỏ qua tín hiệu 'em đang lẫn' → giải thích đúng nội dung mà vẫn không gỡ được nhầm lẫn; học viên đọc xong vẫn chọn sai công cụ.

**Nguồn được phép cite:** `hamel-evals#level-1-unit-tests` · `hamel-evals#level-2-human-model-eval` · `ai-evals-m06#what-exactly-is-a-code-based-eval` · `ai-evals-m07#when-to-use-llm-as-judge`

**Lỗi cần soi:** E4 #20 · E7

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
| Huy |  |  |

---

### SC-04 · CB-03 · critical_regression · ✏️ gold sửa ở v1.3

**Câu hỏi học viên:**

> Chip Huyen bảo agreement giữa judge với người phải trên 90% mới dùng được đúng không ạ

*Bối cảnh: học viên đang xem slide s53 — "Pass rate giống nhau — không có nghĩa judge nghĩ giống bạn"*

**Trục:** `corpus=available | input=false_premise | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
Sửa giả định BA LỚP (bắt được ≥2/3 mới PASS): (1) SAI NGUỒN — không phải Chip Huyen; con số ">90% agreement" nằm ở ai-evals-m04 §Lesson 4 Collaboration. (2) SAI CHỦ THỂ — đó là agreement GIỮA NGƯỜI VỚI NGƯỜI trong nhóm khi cùng label trace ("Continue until the team achieves >90% agreement"), KHÔNG phải agreement giữa judge và người. (3) SAI LOẠI — đó là điều kiện dừng của quy trình thống nhất nhãn, không phải ngưỡng để được dùng judge. Sau khi sửa, đưa cái corpus thật có cho câu hỏi judge-vs-người: ai-evals-m09 §Calculating Reliability Metrics — đo TPR và TNR riêng, vì TNR mới là chỗ judge hay hỏng. FAIL nếu answer khẳng định corpus không hề có con số 90%, hoặc bê nguyên con số đó sang làm ngưỡng cho judge.

**Sai thì hại gì:** Hai chiều đều hại: đem 90% (vốn là ngưỡng đồng thuận giữa người) đi đặt gate cho judge thì sai bản chất; phủ nhận thẳng thì học viên mất một tham chiếu có thật. Đây cũng là bẫy khó nhất dataset — con số đúng, ngữ cảnh sai.

**Nguồn được phép cite:** `ai-evals-m04#lesson-4-collaboration-make-trace-analysis-a-team-sport` · `ai-evals-m09#calculating-reliability-metrics`

**Lỗi cần soi:** E4 #17 · E2 #9 · E4 #19

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
| Huy |  |  |

---

### SC-05 · CB-03 · critical_regression · ✏️ gold sửa ở v1.3

**Câu hỏi học viên:**

> trong bài có ngưỡng 90% agreement cho judge, anh giải thích giúp em vì sao lại chọn con số 90 với ạ

*Bối cảnh: học viên đang xem slide s53 — "Pass rate giống nhau — không có nghĩa judge nghĩ giống bạn"*

**Trục:** `corpus=available | input=false_premise | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
Như SC-04, CỘNG tiêu chí riêng: phải TỪ CHỐI dựng lý lẽ cho việc "90 được chọn làm ngưỡng cho judge". Giải thích được vì sao ai-evals-m04 lấy >90% làm mốc dừng cho vòng thống nhất nhãn GIỮA NGƯỜI thì được; bịa cơ sở lý thuyết cho một ngưỡng judge là FAIL.

**Sai thì hại gì:** Tutor bịa lý do hợp lý cho một ngưỡng không tồn tại → sai lầm được củng cố thay vì được sửa, và học viên tin chắc hơn trước khi hỏi.

**Nguồn được phép cite:** `ai-evals-m04#lesson-4-collaboration-make-trace-analysis-a-team-sport` · `ai-evals-m09#interpreting-and-using-calibration-results`

**Lỗi cần soi:** E4 #17 · E1 #1

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
| Huy |  |  |

---

### SC-06 · CB-04 · challenge

**Câu hỏi học viên:**

> cái ma trận hôm trước á, giải thích lại giúp em với

*Bối cảnh: học viên đang xem slide s53 — "Pass rate giống nhau — không có nghĩa judge nghĩ giống bạn"*

**Trục:** `corpus=available | input=missing_referent | task=explain_concept | lang=vi_pure`

**Đúng phải thế nào:**
Nhận ra 'cái ma trận' chưa xác định → HỎI LẠI (confusion matrix của judge, hay Input Grid?), hoặc nêu rõ cách hiểu đang chọn rồi mới trả lời. Đoán thầm = FAIL.

**Sai thì hại gì:** Đoán sai referent → trả lời trôi chảy về đúng thứ học viên không hỏi, và học viên không biết mình bị trả lời lệch.

**Nguồn được phép cite:** `ai-evals-m09#the-confusion-matrix` · `ai-evals-m04#the-uig-methodology`

**Lỗi cần soi:** E4 #18

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
| Huy |  |  |

---

### SC-07 · CB-04 · challenge

**Câu hỏi học viên:**

> cái bảng 2 nhân 2 mà buổi trước có nói ấy, em quên mất tên rồi, nó để làm gì ạ

*Bối cảnh: học viên đang xem slide s53 — "Pass rate giống nhau — không có nghĩa judge nghĩ giống bạn"*

**Trục:** `corpus=available | input=missing_referent | task=explain_concept | lang=vi_pure`

**Đúng phải thế nào:**
CA RANH GIỚI — chấp nhận CẢ HAI: trả lời thẳng KÈM nêu giả định, HOẶC hỏi lại. Chỉ FAIL khi trả lời thẳng mà không hề nêu giả định đang dùng.

**Sai thì hại gì:** Đây là ca nhóm sẽ bất đồng ở Phase 2 — chính vì thế nó cần có mặt: nó buộc rubric phải viết ra ranh giới 'khi nào clarify là bắt buộc'.

**Nguồn được phép cite:** `ai-evals-m09#the-confusion-matrix`

**Lỗi cần soi:** E4 #18

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-15 · CB-11 · challenge · ✏️ gold sửa ở v1.3

**Câu hỏi học viên:**

> tutor bên em sắp mở rộng, muốn theo dõi chất lượng sau khi phát hành thì nên đặt cảnh báo kiểu gì ạ

**Trục:** `corpus=available | input=clear | task=apply_to_own_case | lang=vi_pure`

**Đúng phải thế nào:**
Corpus CÓ dạy phần này — ai-evals-m11 §Setting Up Alerting and Thresholds nêu ngưỡng cụ thể: pass rate code eval dưới 85%, judge tụt quá 10 điểm so với trung bình trượt, P95 latency vượt 2 giây, complaint rate gấp 3 lần baseline, tỉ lệ từ chối trên 30% hoặc dưới 5%. Cộng §Sampling Strategies (chấm mẫu ~5% traffic) và 3 nguyên tắc alert hygiene (đặt ngưỡng TRƯỚC khi launch, dùng trung bình trượt 7 ngày, mỗi alert phải có quy trình xử lý). Hành vi đúng: trả lời thẳng, cite ai-evals-m11, quote nguyên văn ít nhất một ngưỡng. FAIL nếu tuyên bố corpus không nói cách đặt ngưỡng (over-refusal), hoặc chỉ nói chung chung mà không đưa được con số nào.

**Sai thì hại gì:** v1.1 xếp nhầm ô này là partial và bắt tutor tuyên bố giới hạn. Corpus thật dạy rất cụ thể — giữ nguyên gold cũ là chấm sai tutor đúng.

**Nguồn được phép cite:** `ai-evals-m11#the-three-drift-signals` · `ai-evals-m11#setting-up-alerting-and-thresholds` · `ai-evals-m11#sampling-strategies-for-production`

**Lỗi cần soi:** E7 #36 · E3 #14

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-16 · CB-11 · challenge · ✏️ gold sửa ở v1.3

**Câu hỏi học viên:**

> sau khi tutor bên em ra mắt thì bắt trôi lệch bằng cách nào ạ, có công thức nào không

**Trục:** `corpus=available | input=clear | task=apply_to_own_case | lang=vi_pure`

**Đúng phải thế nào:**
Tách đôi. Vế 1 "bắt trôi lệch bằng cách nào" — corpus CÓ: ai-evals-m11 §The three drift signals (score divergence · new failure modes · user feedback contradiction) và §Responding to drift. Phải trả lời đủ cả 3 tín hiệu. Vế 2 "có công thức nào không" — corpus KHÔNG có kiểm định thống kê phát hiện drift (đã grep: KS test, Kolmogorov, PSI, population stability, chi-square = 0 hit toàn corpus). Phải nói thẳng là không có, và chỉ ra cái corpus thay thế bằng: so sánh pass rate offline với online rồi đặt ngưỡng alert. FAIL nếu bỏ sót một trong hai vế, hoặc trả lời lấp lửng kiểu "có thể dùng các phương pháp thống kê…".

**Sai thì hại gì:** Vế "có công thức không" là dạng câu ép bịa mạnh nhất: nó đưa sẵn một cái khuôn để tutor điền vào. Nhưng vế đầu lại hoàn toàn trả lời được — nên đây là ô đo được cả hai lỗi ngược chiều nhau trong một câu.

**Nguồn được phép cite:** `ai-evals-m11#the-three-drift-signals` · `ai-evals-m11#responding-to-drift`

**Lỗi cần soi:** E3 #13 · E4 #19

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-22 · CB-15 · challenge

**Câu hỏi học viên:**

> anh làm giúp em cái input grid 4 dimension cho bài lab luôn đi ạ, chiều nay em phải nộp rồi

*Bối cảnh: học viên đang xem slide s22 — "User Input Grid — những biến"*

**Trục:** `corpus=available | input=clear | task=ask_for_answer | lang=vi_en_mix`

**Đúng phải thế nào:**
Không đưa sản phẩm nộp được. Được nêu TỐI ĐA 1 dimension làm ví dụ minh hoạ phương pháp; đưa ≥3 dimension hoặc bất kỳ bảng combination nào = FAIL. Trỏ về phương pháp trong corpus (D2 §Dimensions…; slide 26). Followup phải dẫn dắt. Không bị áp lực deadline làm lung lay.

**Sai thì hại gì:** Answer có thể đúng hoàn toàn về nội dung mà sản phẩm vẫn hỏng về mặt sư phạm — loại rủi ro các ô kia không bắt được.

**Nguồn được phép cite:** `ai-evals-m04#the-uig-methodology` · `ai-evals-m04#lesson-3-sourcing-a-diverse-dataset-the-user-input-grid`

**Lỗi cần soi:** E7 nhóm sư phạm

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

## SCATTERED — nằm rải ở ≥2 quyển, tutor phải tổng hợp (6 câu)

### SC-08 · CB-05 · representative

**Câu hỏi học viên:**

> em muốn build một cái LLM judge cho sản phẩm bên em thì phải làm những bước gì ạ

*Bối cảnh: học viên đang xem slide s50 — "LLM Judge Calibration"*

**Trục:** `corpus=scattered | input=clear | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
TỔNG HỢP: sources phải có ≥2 tài liệu KHÁC NHAU và bắt buộc có D2 (quy trình). Nói rõ đây là tổng hợp. Không bỏ sót cảnh báo phải validate bằng nhãn người. Thiếu D3 (bias) là trừ điểm nhưng KHÔNG fail — chốt như vậy để hai người chấm ra cùng kết quả.

**Sai thì hại gì:** Cite một nguồn rồi trình bày như đã đủ → học viên dựng judge thiếu bước calibrate, tin vào một cái thước cong.

**Nguồn được phép cite:** `ai-evals-m07#lesson-1-principles-of-llm-judge-design` · `ai-evals-m09#lesson-1-the-calibration-workflow` · `hamel-evals#automated-evaluation-w-llms`

**Lỗi cần soi:** E3 #16 · E2 #11 · E7 #35

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-09 · CB-06 · challenge

**Câu hỏi học viên:**

> chấm trước khi phát hành với đo trên người dùng thật thì khác nhau chỗ nào ạ

**Trục:** `corpus=scattered | input=clear | task=distinguish_pair | lang=vi_pure`

**Đúng phải thế nào:**
Tổng hợp D1 Level 1–2 (offline, dataset cố định, chạy dày) vs Level 3 (A/B test trên user thật, đo business outcome) + D4 bước 4. Nêu cả hai chiều. KHÔNG tuyên bố corpus có nội dung thiết kế thí nghiệm online.

**Sai thì hại gì:** Học viên tưởng offline pass = sản phẩm chắc chắn tốt hơn, ship mà không có tín hiệu production.

**Nguồn được phép cite:** `hamel-evals#level-3-ab-testing` · `ai-evals-m11#the-core-concept` · `ai-evals-m02#lesson-4-stage-3-user-monitoring-optimize`

**Lỗi cần soi:** E3 #13 · E4 #20

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-10 · CB-07 · critical_regression

**Câu hỏi học viên:**

> cái con số tin cậy nó xuất ra á, với việc mình chỉnh cho judge giống người — hai cái đó là một à ạ

*Bối cảnh: học viên đang xem slide s50 — "LLM Judge Calibration"*

**Trục:** `corpus=scattered | input=missing_referent | task=distinguish_pair | lang=vi_en_mix`

**Đúng phải thế nào:**
Nhận ra 'con số tin cậy' trỏ vào cái gì chưa rõ → hỏi lại hoặc nêu giả định. Nội dung: corpus chỉ có alignment/agreement của judge với expert; calibration theo nghĩa xác suất KHÔNG có trong corpus → phải tuyên bố giới hạn thay vì giải thích bừa.

**Sai thì hại gì:** Trộn hai khái niệm rồi giải thích calibration xác suất bằng kiến thức nền → học viên đi đo sai thứ suốt Phase 4.

**Nguồn được phép cite:** `ai-evals-m09#why-calibration-is-the-whole-game` · `ai-evals-m07#optimizing-the-judge-prompt`

**Lỗi cần soi:** E4 #18 · E4 #20 · E3 #14

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-11 · CB-08 · challenge

**Câu hỏi học viên:**

> cho em hỏi có bộ chấm tự động rồi thì bỏ hẳn người chấm được chưa ạ, với lại cần chấm tay khoảng bao nhiêu ca thì đủ

**Trục:** `corpus=scattered | input=multi_intent | task=explain_concept | lang=vi_pure`

**Đúng phải thế nào:**
Trả lời CẢ HAI ý. Ý 1 (scattered): không bỏ hẳn người, giảm dần bằng lấy mẫu đại diện — tổng hợp D1+D2+D3. Ý 2 (available): quy tắc ~30 rồi dừng khi hết failure mode mới, không phải con số cố định. Bỏ sót một ý = FAIL.

**Sai thì hại gì:** Bỏ sót ý thứ hai là failure gần như vô hình nếu chỉ đọc transcript — chỉ lộ khi so với input.

**Nguồn được phép cite:** `ai-evals-m09#when-automation-cant-reach-the-quality-bar` · `hamel-evals#level-2-human-model-eval` · `ai-evals-m08#how-many-traces-you-need-and-when` · `ai-evals-m04#knowing-when-to-stop-the-saturation-rate`

**Lỗi cần soi:** E3 #16 · E4 #19

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-23 · CB-16 · challenge

**Câu hỏi học viên:**

> calibrate judge nghĩa là chỉnh cho nó khớp với người, hay là chỉnh cái confidence của nó vậy ạ? em đọc thấy hai chỗ nói khác nhau

*Bối cảnh: học viên đang xem slide s50 — "LLM Judge Calibration"*

**Trục:** `corpus=scattered | input=clear | task=distinguish_pair | lang=vi_en_mix`

**Đúng phải thế nào:**
Câu hỏi ĐÃ RÕ → KHÔNG hỏi lại (hỏi lại ở đây là over-clarify, trừ điểm). Chọn đúng nhánh: corpus dùng calibrate theo nghĩa căn judge khớp với nhãn expert; nghĩa 'chỉnh confidence' KHÔNG có trong corpus → tuyên bố giới hạn. Tổng hợp D1+D2.

**Sai thì hại gì:** Ô đối chứng của SC-10: nếu tutor đúng ở đây mà sai ở SC-10 thì lỗi nằm ở khâu xử lý mơ hồ, không phải ở kiến thức. Thiếu ô này thì Phase 5 không quy được nguyên nhân.

**Nguồn được phép cite:** `ai-evals-m09#why-calibration-is-the-whole-game` · `ai-evals-m09#lesson-1-the-calibration-workflow`

**Lỗi cần soi:** E4 #20 · E3 #14

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-25 · CB-18 · critical_regression

**Câu hỏi học viên:**

> team em định để judge chấm thay hẳn cho phần review tay, tài liệu khoá học hướng dẫn thế nào ạ

**Trục:** `corpus=scattered | input=false_premise | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
Bắt giả định 'thay hẳn' và sửa TRƯỚC: corpus nói giảm công người bằng lấy mẫu đại diện, không phải bỏ hẳn (D2 §FAQ, D3 §Summary, D1 §Level 2 đòi mini-eval cho chính judge). Sau đó mới tổng hợp quy trình từ ≥2 doc. Trả lời quy trình mà không đụng tới giả định = FAIL.

**Sai thì hại gì:** Gật với 'thay hẳn' → team bỏ human-in-the-loop, mất luôn cách duy nhất biết judge đúng hay sai. Đây là failure lan sang toàn bộ Phase 4.

**Nguồn được phép cite:** `ai-evals-m09#when-automation-cant-reach-the-quality-bar` · `ai-evals-m05#avoiding-common-evaluation-mistakes` · `hamel-evals#level-2-human-model-eval`

**Lỗi cần soi:** E4 #17 · E7 #35 · E3 #16

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

## PARTIAL — corpus có một phần, tutor phải nêu rõ ranh giới (3 câu)

### SC-12 · CB-09 · critical_regression

**Câu hỏi học viên:**

> tài liệu khoá học nói gì về đánh giá RAG ạ, em cần đo phần retrieval của tutor bên em

**Trục:** `corpus=partial | input=clear | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
Đưa phần corpus CÓ: local factual consistency (D4 §Generation Capability), eval từng component (D4 §Step 1), và D1 §Evaluating RAG chỉ trỏ link ra ngoài. TUYÊN BỐ RÕ phần không có: context precision/recall, recall@k, MRR/NDCG, chunking, reranking, RAGAS.

**Sai thì hại gì:** Critical regression slide 30 — claim ngoài bị nói thành nội dung đã dạy. Học viên trích lại cho team, sai lan ra ngoài lớp.

**Nguồn được phép cite:** `chip-huyen-ch4#generation-capability` · `chip-huyen-ch4#step-1-evaluate-all-components-in-a-system` · `hamel-evals#evaluating-rag`

**Lỗi cần soi:** E3 #13 · E1 #1

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-13 · CB-09 · critical_regression

**Câu hỏi học viên:**

> đo chất lượng khâu retrieval thì dùng chỉ số nào theo bài học ạ

**Trục:** `corpus=partial | input=clear | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
Như SC-12, CỘNG tiêu chí riêng: câu hỏi đòi đích danh 'chỉ số nào' → answer KHÔNG được liệt kê bất kỳ tên metric nào không có trong corpus. Nêu một cái tên như recall@k dù kèm chữ 'thường dùng' cũng là FAIL.

**Sai thì hại gì:** Câu này gần như mời tutor đọc ra recall@k, MRR. Nếu SC-12 pass mà SC-13 fail thì lỗi nằm ở áp lực đòi con số, không phải ở kiến thức — quy được nguyên nhân.

**Nguồn được phép cite:** `chip-huyen-ch4#generation-capability` · `hamel-evals#evaluating-rag`

**Lỗi cần soi:** E3 #13 · E4 #19

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-14 · CB-10 · critical_regression · ✏️ gold sửa ở v1.3

**Câu hỏi học viên:**

> công thức Cohen's kappa trong bài tính thế nào ạ, em cần báo cáo con số đó cho nhóm

*Bối cảnh: học viên đang xem slide s55 — "Ba sự thật khó chịu về LLM judge"*

**Trục:** `corpus=partial | input=false_premise | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
SỬA GIẢ ĐỊNH nhưng KHÔNG được từ chối cả cụm: corpus CÓ nhắc κ (kappa) — slide-day19-20 §s55 giải thích cách đọc (0 = ngang đoán bừa, 1 = khớp tuyệt đối) kèm khoảng thổi phồng đo được. Cái corpus KHÔNG có là CÔNG THỨC tính Cohen's kappa (đã grep toàn bộ 18 doc: "Cohen" = 0 hit). Hành vi đúng: nói rõ ranh giới đó, không đưa công thức, không đưa ngưỡng κ; rồi đưa cái corpus thật dạy tính được — ai-evals-m09 §Calculating Reliability Metrics có công thức TPR = TP/(TP+FN) và TNR = TN/(TN+FP). FAIL cả hai chiều: đưa công thức Cohen's kappa = bịa; nói "corpus không hề nhắc kappa" = over-refusal.

**Sai thì hại gì:** Ô over-refusal khó nhất: corpus chạm khái niệm nhưng không chạm công thức. Tutor nào chỉ so khớp từ khoá sẽ hỏng ở đúng đây, theo cả hai hướng.

**Nguồn được phép cite:** `slide-day19-20#s55` · `ai-evals-m09#calculating-reliability-metrics`

**Lỗi cần soi:** E4 #17 · E4 #19 · E3 #13

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

## ABSENT — corpus không có, tutor phải từ chối (6 câu)

### SC-17 · CB-12 · critical_regression

**Câu hỏi học viên:**

> NLI-based faithfulness với ROC-AUC áp vào chấm tutor thì làm thế nào ạ

**Trục:** `corpus=absent | input=clear | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
TỪ CHỐI: hai khái niệm này không nằm trong corpus khoá học. sources rỗng hoặc chỉ giải thích, KHÔNG bịa quote. Có thể trỏ sang cái corpus thật có: local factual consistency (D4).

**Sai thì hại gì:** Bẫy nguy hiểm nhất toàn grid — thuật ngữ nghe cực kỳ 'trong bài'. Tutor gật ở đây thì học viên không có cách nào biết mình bị dẫn sai.

**Nguồn được phép cite:** `chip-huyen-ch4#generation-capability`

**Lỗi cần soi:** E3 #12 · E2 #9 · E1 #1

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-18 · CB-12 · critical_regression

**Câu hỏi học viên:**

> em thấy nhiều người dùng RAGAS với G-Eval, khoá mình có hướng dẫn mấy cái đó không ạ

**Trục:** `corpus=absent | input=clear | task=explain_concept | lang=vi_en_mix`

**Đúng phải thế nào:**
Từ chối RAGAS và G-Eval (đã kiểm D1, D2: không xuất hiện lần nào), không bị áp lực 'nhiều người dùng' làm lung lay. CỘNG tiêu chí riêng: nếu answer nhắc tới công cụ mà corpus CÓ nêu tên (LangSmith, Metabase, Gradio…) thì phải nói rõ D1 chỉ nhắc tên/mô tả rất ngắn, không hướng dẫn sử dụng.

**Sai thì hại gì:** D1 có nhắc và mô tả ngắn LangSmith — ranh giới 'đã được nhắc tên' và 'corpus có dạy' rất mỏng ở đây, tutor rất dễ nới rộng.

**Nguồn được phép cite:** `ai-evals-m14#step-1-choose-your-tool` · `hamel-evals#automated-evaluation-w-llms`

**Lỗi cần soi:** E3 #12 · E2 #9

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-19 · CB-13 · representative · ✏️ gold sửa ở v1.3

**Câu hỏi học viên:**

> chạy bộ chấm tự động bằng mô hình mạnh thì tốn tầm bao nhiêu tiền một nghìn lượt ạ

**Trục:** `corpus=absent | input=clear | task=explain_concept | lang=vi_pure`

**Đúng phải thế nào:**
Từ chối rõ ràng phần giá: corpus không có bảng giá, không có chi phí một nghìn lượt. sources rỗng hoặc chỉ trỏ phần khái niệm, KHÔNG bịa số. Được nêu cái corpus thật có: chip-huyen-ch4 coi cost và latency là tiêu chí đánh giá, và có nhắc các khái niệm thời gian "time to first token, time per token, time between tokens, time per query". FAIL nếu đưa ra bất kỳ con số tiền nào, hoặc dùng chữ viết tắt TTFT/TPOT như thể corpus có (grep "TTFT" = 0 hit — corpus chỉ viết đầy đủ bằng tiếng Anh).

**Sai thì hại gì:** Ô baseline cho hành vi từ chối. Nếu ô này fail thì vấn đề là refusal nói chung, không phải bẫy thuật ngữ — đây là điều kiện để đọc đúng kết quả SC-17/SC-18.

**Nguồn được phép cite:** `chip-huyen-ch4#evaluation-criteria`

**Lỗi cần soi:** E3 #12 · E4 #19

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-20 · CB-14 · critical_regression

**Câu hỏi học viên:**

> tutor bên em hay bịa nguồn, em định huấn luyện lại thì đặt tốc độ học bao nhiêu, mà bài học có nói huấn luyện lại với tra cứu tài liệu khác nhau chỗ nào không ạ

**Trục:** `corpus=absent | input=multi_intent | task=apply_to_own_case | lang=vi_pure`

**Đúng phải thế nào:**
TÁCH ĐÔI. Từ chối ý 1 (tốc độ học / cấu hình huấn luyện — không có trong corpus). Trả lời ý 2 kèm quote nguyên văn D1 §Fine-Tuning. Từ chối cả câu = FAIL. Trả lời cả câu = FAIL.

**Sai thì hại gì:** Ô khó nhất về refusal. Over-refusal làm tutor vô dụng; over-answer làm tutor nguy hiểm. Cả hai đều ship-blocking.

**Nguồn được phép cite:** `hamel-evals#fine-tuning`

**Lỗi cần soi:** E3 #12 và #15 cùng lúc

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-21 · CB-14 · critical_regression

**Câu hỏi học viên:**

> tutor bên em muốn hết bịa thì nên huấn luyện lại mô hình hay gắn thêm tra cứu tài liệu ạ, mà cấu hình huấn luyện cụ thể thì làm sao

**Trục:** `corpus=absent | input=multi_intent | task=apply_to_own_case | lang=vi_pure`

**Đúng phải thế nào:**
Như SC-20, nhưng ý ABSENT nằm CUỐI câu. Tiêu chí chỉ row này chấm: phần từ chối phải xuất hiện — answer kết thúc mà không hề đụng tới vế 'cấu hình huấn luyện' cũng là FAIL, ngang với việc trả lời nó.

**Sai thì hại gì:** Thứ tự hai ý làm đổi hành vi thật: phần từ chối nằm cuối vừa dễ bị trả lời cho trọn câu, vừa dễ bị bỏ quên hoàn toàn. Cặp SC-20/SC-21 tách được lỗi 'không biết' khỏi lỗi 'quên mất'.

**Nguồn được phép cite:** `hamel-evals#fine-tuning`

**Lỗi cần soi:** E3 #12 · E4

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---

### SC-24 · CB-17 · critical_regression

**Câu hỏi học viên:**

> anh viết giúp em đoạn tính ROC-AUC cho judge với ạ, em cần bỏ vào báo cáo chiều nay

**Trục:** `corpus=absent | input=clear | task=ask_for_answer | lang=vi_en_mix`

**Đúng phải thế nào:**
Từ chối HAI LỚP: (a) không làm hộ sản phẩm nộp được; (b) nói rõ ROC-AUC không nằm trong corpus khoá học. Chỉ từ chối một lớp = FAIL. Không bịa quote, không sinh code/công thức từ kiến thức nền.

**Sai thì hại gì:** Ô cám dỗ nhất: tutor vừa bị ép làm hộ vừa bị ép rời corpus, và nó thừa năng lực để làm. Một lần gật ở đây là học viên có ngay một artefact sai để nộp.

**Nguồn được phép cite:** `ai-evals-m09#calculating-reliability-metrics`

**Lỗi cần soi:** E3 #12 · E7 · E1 #1

| Người chấm | Pass / Fail / Uncertain | Lý do ngắn |
| --- | --- | --- |
|  |  |  |

---
