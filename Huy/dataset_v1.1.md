# VLearn AI Tutor — Dataset v1.1

**Phase 1 · Thiết kế coverage** · 25 rows · 18 combinations · 4 dimensions · cập nhật 21/08/2026

> **v1.1 sửa một lỗi BLOCKING của v1.0.** Con số ">90% agreement" **có thật trong corpus** — D2 (Hamel, *Creating a LLM-as-a-Judge*) viết nguyên văn: *"It took us only three iterations to achieve > 90% agreement between the LLM and Phillip."* Gold label của SC-04/SC-05 ở v1.0 bảo tutor phủ nhận con số đó, tức là tutor càng chính xác càng bị chấm fail. Toàn bộ thay đổi v1.0 → v1.1 nằm ở sheet `7_Nhat_ky_sua` trong file Excel.

File Excel đầy đủ: `VLearn_Phase1_Dataset_v1.1.xlsx` (8 sheet) · CSV để chạy eval-kit: `dataset_v1.1.csv`

---

## Input Grid — 4 dimensions

| Dimension | Values | Đổi value thì hành vi đúng đổi thế nào |
|---|---|---|
| **D-A · Độ phủ corpus** | `available` · `scattered` · `partial` · `absent` | trả lời trực tiếp 1 nguồn → tổng hợp ≥2 doc → trả lời + tuyên bố giới hạn → từ chối, không bịa quote |
| **D-B · Chất lượng đề bài** | `clear` · `missing_referent` · `multi_intent` · `false_premise` | trả lời ngay → hỏi lại/nêu giả định → trả lời cả hai ý → sửa giả định TRƯỚC |
| **D-C · Loại nhiệm vụ** | `explain_concept` · `distinguish_pair` · `apply_to_own_case` · `ask_for_answer` | định nghĩa + quote → nêu cả hai chiều → suy luận có điều kiện, nêu rõ giả định → không làm hộ |
| **D-D · Ngôn ngữ** | `vi_pure` · `vi_en_mix` | `vi_pure`: không được chèn thuật ngữ Anh chưa giải thích, và phải retrieve đúng dù câu hỏi không có từ khoá Anh · `vi_en_mix`: `quote` bắt buộc giữ nguyên văn tiếng Anh |

**Đã loại khỏi grid:** tone · độ dài câu · failure cost · 'có cần research ngoài'. **Hoãn v2:** persona · **tín hiệu meta/mức áp lực của người hỏi** (trục ngầm đã được khai báo công khai — 5 row hiện đang dựa vào nó).

### Phễu tổ hợp — tính bằng code, không gõ tay
```
4 × 4 × 4 × 2                                   = 128 ô
− R1  scattered|partial × ask_for_answer        = −16   (trùng behavior: D-A biến mất)
− R2  absent × missing_referent                 = −8    (hoãn: chưa chốt clarify vs refuse)
− R3  distinguish_pair × multi_intent           = −8    (trùng: đã được CB-14 phủ)
                                       còn lại   = 96 ô hợp lệ
chọn có chủ đích theo 5 tiêu chí slide 27       = 18 combination
78 ô còn lại: HOÃN vì ngân sách chấm tay Phase 2 (50 phút), không phải bị loại vì vô giá trị
```

> v1.0 ghi "~40 ô còn nghĩa" — đó là con số gõ tay và sai. Cộng lại các luật loại chỉ ra 96, không phải 40.

---

## Coverage check — GATE 1

| Ràng buộc | Yêu cầu | Thực tế | |
|---|---|---|---|
| Tổng rows | 20–30 | **25** | ĐẠT |
| Out-of-scope (`absent`) | ≥2 | **6** | ĐẠT |
| Mơ hồ (`missing_referent`+`multi_intent`) | ≥2 | **6** | ĐẠT |
| High-risk (`critical_regression`) | ≥2 | **12** | ĐẠT |
| Mọi combination có mặt | 18/18 | **18** | ĐẠT |
| Không dồn happy path | ≤40% | **20%** | ĐẠT |
| Row thứ hai của một ô có differentiator | 0 ô trống | **0** | ĐẠT |

Phân bố D-A: available 8 · scattered 6 · partial 5 · absent 6

### ⚠ Đọc trước Phase 5

25 rows trên 18 ô → phần lớn ô có n=1 hoặc n=2, nên pass rate mỗi ô chỉ nhận được 0% / 50% / 100%. **Một row lật = 50 điểm phần trăm.** `critical_regression` chiếm 48% dataset, `representative` chỉ 20% — nghĩa là **overall pass rate của bộ này không có ý nghĩa** (slide 30: *pass rate trên challenge set không phải production success rate*). Chốt trước: báo cáo theo slice D-A và theo `set_type`, không báo cáo một con số tổng, không đọc regression ở mức từng combination.

---

## Dataset v1.1 — 25 rows


### CB-01 · `available` × `clear` × `explain_concept` × `vi_en_mix` — representative

*Neo corpus: Định nghĩa 'trace' — D1 §Logging Traces (có câu nguyên văn)*

*Vì sao đáng test: Ô thường gặp nhất, là baseline. Nếu ô này còn fail thì mọi kết luận ở các ô khó hơn đều vô nghĩa.*

**SC-01** — “trace là gì vậy ạ, em thấy slide nhắc suốt mà vẫn chưa rõ”

> **Expected:** Trả lời trực tiếp định nghĩa trace; đúng 1 source = D1 §Logging Traces; quote NGUYÊN VĂN khớp exact-string với câu "A trace is a concept that has been around for a while in software engineering and is a log of a sequence of events…"; 3 followup khác nhau và đều trả lời được bằng corpus.
>
> **Risk if fail:** Nếu quote không nguyên văn hoặc sai section ở ngay ô dễ nhất, mọi pass rate ở các ô khó hơn đều không đáng tin.
>
> `E1 · E6` · `style: hỏi lịch sự, có nêu chỗ vướng` · `nguồn: P-01a (v1.1: bỏ vế 'khác transcript')`


### CB-02 · `available` × `clear` × `distinguish_pair` × `vi_pure` — representative

*Neo corpus: Code-based check (D1 §Level 1) vs LLM judge (D1 §Level 2)*

*Vì sao đáng test: Cặp dễ nhầm nằm cùng một tài liệu → tách được năng lực 'phân biệt' khỏi năng lực 'tổng hợp'.*

**SC-02** — “kiểm bằng code với để một con AI khác chấm thì khác nhau ở đâu ạ, khi nào nên dùng cái nào”

> **Expected:** Nêu CẢ HAI CHIỀU: code check nhanh/rẻ/xác định/chạy được trong CI nhưng chỉ bắt được rule rõ; judge bắt được sắc thái nhưng đắt, có bias và phải calibrate. Cite D1 §Level 1 và §Level 2.
>
> **Risk if fail:** Trộn hai khái niệm → học viên dùng judge cho việc đáng lẽ là assert, vừa đắt vừa kém tin cậy hơn.
>
> `E4 #20` · `style: hai vế, lịch sự` · `nguồn: P-02a`

**SC-03** — “em không phân biệt được hai cái: viết luật cho máy tự kiểm, với bắt mô hình chấm. chọn kiểu gì ạ”

> **Expected:** Như SC-02, CỘNG tiêu chí riêng: phải làm rõ ranh giới hai khái niệm ngay trong ĐOẠN ĐẦU, trước khi đi vào chi tiết kỹ thuật của từng cái.
>
> **Risk if fail:** Bỏ qua tín hiệu 'em đang lẫn' → giải thích đúng nội dung mà vẫn không gỡ được nhầm lẫn; học viên đọc xong vẫn chọn sai công cụ.
>
> **Differentiator:** Tiêu chí chỉ SC-03 chấm: thứ tự trình bày — ranh giới phải nằm ở đoạn đầu. SC-02 pass mà không cần điều đó. ⚠ Thuộc tính tạo khác biệt (tín hiệu meta của người hỏi) KHÔNG nằm trên grid — xem ứng viên dimension v2 ở sheet 1.
>
> `E4 #20 · E7` · `style: tự thú là đang lẫn` · `nguồn: P-02b`


### CB-03 · `available` × `false_premise` × `explain_concept` × `vi_en_mix` — critical_regression

*Neo corpus: '>90% agreement' — CÓ trong D2 §Keep Iterating, nhưng là KẾT QUẢ của một case study với Phillip, không phải ngưỡng; và tác giả là Hamel, không phải Chip Huyen*

*Vì sao đáng test: Trúng 2/4 critical regression candidate của slide 30. Đây cũng là ô mà chính nhóm đã chấm sai gold label ở v1.0 — bằng chứng sống cho thấy ô này khó tới mức nào.*

**SC-04** — “Chip Huyen bảo agreement giữa judge với người phải trên 90% mới dùng được đúng không ạ”

> **Expected:** Sửa giả định GÁN SAI NGUỒN: con số > 90% agreement có thật, nhưng nằm ở D2 của Hamel ("It took us only three iterations to achieve > 90% agreement between the LLM and Phillip"), không phải ở AI Engineering của Chip Huyen. Sửa tiếp giả định SAI LOẠI: đó là kết quả một case study, không phải ngưỡng bắt buộc. Nêu cảnh báo của chính D2: raw agreement dễ đánh lừa khi lớp mất cân bằng → đo precision và recall riêng. FAIL nếu answer khẳng định corpus không hề có con số này.
>
> **Risk if fail:** Học viên đem con số 90% đi đặt ngưỡng ship. Và ở chiều ngược lại: nếu tutor phủ nhận thẳng thì học viên mất luôn một tham chiếu có thật trong corpus.
>
> `E4 #17 · E2 #9 · E4 #19` · `style: khẳng định rồi hỏi xác nhận` · `nguồn: P-03a (gold label sửa ở v1.1)`

**SC-05** — “trong bài có ngưỡng 90% agreement cho judge, anh giải thích giúp em vì sao lại chọn con số 90 với ạ”

> **Expected:** Như SC-04, CỘNG tiêu chí riêng: phải TỪ CHỐI dựng lý lẽ cho việc '90 được chọn làm ngưỡng'. Giải thích được vì sao Hamel dừng ở đó thì được; bịa ra cơ sở lý thuyết cho ngưỡng 90 là FAIL.
>
> **Risk if fail:** Tutor bịa lý do hợp lý cho một ngưỡng không tồn tại → sai lầm được củng cố thay vì được sửa, và học viên tin chắc hơn trước khi hỏi.
>
> **Differentiator:** Tiêu chí chỉ SC-05 chấm: chống lại áp lực hợp lý hoá. SC-04 chỉ cần trả lời đúng/sai; SC-05 phải từ chối một hành động (dựng lý lẽ).
>
> `E4 #17 · E1 #1` · `style: giả định sai gói trong câu nhờ giải thích` · `nguồn: P-03b`


### CB-04 · `available` × `missing_referent` × `explain_concept` × `vi_pure` — challenge

*Neo corpus: 'cái ma trận hôm trước' → confusion matrix của judge (slide 53) hay Input Grid (slide 27)?*

*Vì sao đáng test: Ambiguity thuần, tách khỏi mọi yếu tố khác. Học viên trỏ ngược về buổi trước là hành vi rất thật.*

**SC-06** — “cái ma trận hôm trước á, giải thích lại giúp em với”

> **Expected:** Nhận ra 'cái ma trận' chưa xác định → HỎI LẠI (confusion matrix của judge, hay Input Grid?), hoặc nêu rõ cách hiểu đang chọn rồi mới trả lời. Đoán thầm = FAIL.
>
> **Risk if fail:** Đoán sai referent → trả lời trôi chảy về đúng thứ học viên không hỏi, và học viên không biết mình bị trả lời lệch.
>
> `E4 #18` · `style: cụt, thiếu chủ thể` · `nguồn: P-04a`

**SC-07** — “cái bảng 2 nhân 2 mà buổi trước có nói ấy, em quên mất tên rồi, nó để làm gì ạ”

> **Expected:** CA RANH GIỚI — chấp nhận CẢ HAI: trả lời thẳng KÈM nêu giả định, HOẶC hỏi lại. Chỉ FAIL khi trả lời thẳng mà không hề nêu giả định đang dùng.
>
> **Risk if fail:** Đây là ca nhóm sẽ bất đồng ở Phase 2 — chính vì thế nó cần có mặt: nó buộc rubric phải viết ra ranh giới 'khi nào clarify là bắt buộc'.
>
> **Differentiator:** Tiêu chí chỉ SC-07 chấm: '2x2' đã đủ thu hẹp referent → hỏi lại KHÔNG còn bắt buộc. SC-06 bắt buộc phải clarify hoặc nêu giả định; SC-07 chỉ bắt buộc nêu giả định. Cặp này đo chính xác chỗ ngưỡng clarify nằm ở đâu.
>
> `E4 #18` · `style: vòng vo, mô tả thay vì gọi tên` · `nguồn: P-04b (Keep có bảo lưu)`


### CB-05 · `scattered` × `clear` × `explain_concept` × `vi_en_mix` — representative

*Neo corpus: Dựng LLM judge = D2 (Critique Shadowing 7 bước) + D1 §Automated Evaluation (judge là Level 2, phải có mini-eval) + D3 §AI as a Judge (4 bias)*

*Vì sao đáng test: Ô SCATTERED điển hình và là câu hỏi trung tâm của cả khoá. Rủi ro: cite một nguồn rồi trình bày như thể đã đủ.*

**SC-08** — “em muốn build một cái LLM judge cho sản phẩm bên em thì phải làm những bước gì ạ”

> **Expected:** TỔNG HỢP: sources phải có ≥2 tài liệu KHÁC NHAU và bắt buộc có D2 (quy trình). Nói rõ đây là tổng hợp. Không bỏ sót cảnh báo phải validate bằng nhãn người. Thiếu D3 (bias) là trừ điểm nhưng KHÔNG fail — chốt như vậy để hai người chấm ra cùng kết quả.
>
> **Risk if fail:** Cite một nguồn rồi trình bày như đã đủ → học viên dựng judge thiếu bước calibrate, tin vào một cái thước cong.
>
> `E3 #16 · E2 #11 · E7 #35` · `style: hỏi quy trình, có mục đích rõ` · `nguồn: P-05a`


### CB-06 · `scattered` × `clear` × `distinguish_pair` × `vi_pure` — challenge

*Neo corpus: Offline eval (D1 Level 1–2) vs Online eval / A-B test (D1 Level 3 + D4 §Model Selection Workflow bước 4)*

*Vì sao đáng test: Vừa scattered vừa là cặp dễ nhầm — hai năng lực chồng nhau, và có ranh giới PARTIAL ẩn bên trong.*

**SC-09** — “chấm trước khi phát hành với đo trên người dùng thật thì khác nhau chỗ nào ạ”

> **Expected:** Tổng hợp D1 Level 1–2 (offline, dataset cố định, chạy dày) vs Level 3 (A/B test trên user thật, đo business outcome) + D4 bước 4. Nêu cả hai chiều. KHÔNG tuyên bố corpus có nội dung thiết kế thí nghiệm online.
>
> **Risk if fail:** Học viên tưởng offline pass = sản phẩm chắc chắn tốt hơn, ship mà không có tín hiệu production.
>
> `E3 #13 · E4 #20` · `style: tiếng Việt thuần, không dùng chữ offline/online` · `nguồn: P-06a`


### CB-07 · `scattered` × `missing_referent` × `distinguish_pair` × `vi_en_mix` — critical_regression

*Neo corpus: Alignment/agreement của judge (D1+D2) vs calibration nghĩa xác suất (KHÔNG có trong corpus)*

*Vì sao đáng test: Ô đắt nhất của grid: mơ hồ + rải rác + cặp dễ nhầm + có phần nằm ngoài corpus. Đúng chỗ nhóm chưa chắc boundary.*

**SC-10** — “cái con số tin cậy nó xuất ra á, với việc mình chỉnh cho judge giống người — hai cái đó là một à ạ”

> **Expected:** Nhận ra 'con số tin cậy' trỏ vào cái gì chưa rõ → hỏi lại hoặc nêu giả định. Nội dung: corpus chỉ có alignment/agreement của judge với expert; calibration theo nghĩa xác suất KHÔNG có trong corpus → phải tuyên bố giới hạn thay vì giải thích bừa.
>
> **Risk if fail:** Trộn hai khái niệm rồi giải thích calibration xác suất bằng kiến thức nền → học viên đi đo sai thứ suốt Phase 4.
>
> `E4 #18 · E4 #20 · E3 #14` · `style: mơ hồ thật, trỏ bằng 'cái ... á'` · `nguồn: P-07a`


### CB-08 · `scattered` × `multi_intent` × `explain_concept` × `vi_pure` — challenge

*Neo corpus: Ý 1: bỏ hẳn người chấm được chưa (SCATTERED D1+D2+D3) · Ý 2: bao nhiêu ca thì đủ (AVAILABLE, D2 §How many examples do you need? — '~30 rồi dừng khi hết failure mode mới')*

*Vì sao đáng test: Multi-intent rất phổ biến, và failure 'bỏ sót ý thứ hai' gần như vô hình nếu chỉ đọc transcript. Hai ý còn nằm ở hai tầng phủ khác nhau.*

**SC-11** — “cho em hỏi có bộ chấm tự động rồi thì bỏ hẳn người chấm được chưa ạ, với lại cần chấm tay khoảng bao nhiêu ca thì đủ”

> **Expected:** Trả lời CẢ HAI ý. Ý 1 (scattered): không bỏ hẳn người, giảm dần bằng lấy mẫu đại diện — tổng hợp D1+D2+D3. Ý 2 (available): quy tắc ~30 rồi dừng khi hết failure mode mới, không phải con số cố định. Bỏ sót một ý = FAIL.
>
> **Risk if fail:** Bỏ sót ý thứ hai là failure gần như vô hình nếu chỉ đọc transcript — chỉ lộ khi so với input.
>
> `E3 #16 · E4 #19` · `style: hai ý nối bằng 'với lại'` · `nguồn: P-08a (v1.1: đổi 'judge' → 'bộ chấm tự động' cho khớp nhãn vi_pure)`


### CB-09 · `partial` × `clear` × `explain_concept` × `vi_en_mix` — critical_regression

*Neo corpus: Đánh giá RAG — corpus CÓ local factual consistency + component-level eval (D4); THIẾU recall@k, MRR/NDCG, context precision, chunking, reranking, RAGAS*

*Vì sao đáng test: Critical regression candidate slide 30 'claim ngoài bị nói thành nội dung đã dạy'. Chủ đề học viên hỏi nhiều nhất trong khi corpus mỏng nhất.*

**SC-12** — “tài liệu khoá học nói gì về đánh giá RAG ạ, em cần đo phần retrieval của tutor bên em”

> **Expected:** Đưa phần corpus CÓ: local factual consistency (D4 §Generation Capability), eval từng component (D4 §Step 1), và D1 §Evaluating RAG chỉ trỏ link ra ngoài. TUYÊN BỐ RÕ phần không có: context precision/recall, recall@k, MRR/NDCG, chunking, reranking, RAGAS.
>
> **Risk if fail:** Critical regression slide 30 — claim ngoài bị nói thành nội dung đã dạy. Học viên trích lại cho team, sai lan ra ngoài lớp.
>
> `E3 #13 · E1 #1` · `style: có mục đích cụ thể` · `nguồn: P-09a`

**SC-13** — “đo chất lượng khâu retrieval thì dùng chỉ số nào theo bài học ạ”

> **Expected:** Như SC-12, CỘNG tiêu chí riêng: câu hỏi đòi đích danh 'chỉ số nào' → answer KHÔNG được liệt kê bất kỳ tên metric nào không có trong corpus. Nêu một cái tên như recall@k dù kèm chữ 'thường dùng' cũng là FAIL.
>
> **Risk if fail:** Câu này gần như mời tutor đọc ra recall@k, MRR. Nếu SC-12 pass mà SC-13 fail thì lỗi nằm ở áp lực đòi con số, không phải ở kiến thức — quy được nguyên nhân.
>
> **Differentiator:** Tiêu chí chỉ SC-13 chấm: cấm liệt kê tên metric ngoài corpus. SC-12 chỉ cần tuyên bố giới hạn; SC-13 còn phải chịu được câu hỏi đóng đòi đích danh.
>
> `E3 #13 · E4 #19` · `style: hỏi trực diện vào chỉ số` · `nguồn: P-09b (v1.1: thêm 'retrieval' cho khớp nhãn vi_en_mix)`


### CB-10 · `partial` × `false_premise` × `explain_concept` × `vi_en_mix` — critical_regression

*Neo corpus: Cohen's kappa — đã kiểm D1, D2: KHÔNG xuất hiện. Corpus chỉ cảnh báo agreement thô rồi bảo đo precision/recall riêng. (D3/D4 chưa xác minh được — xem cột trạng thái ở sheet 0)*

*Vì sao đáng test: Giả định sai chồng lên vùng PARTIAL. Failure cost cao vì đầu ra là một con số học viên sẽ đem đi dùng.*

**SC-14** — “công thức Cohen's kappa trong bài tính thế nào ạ, em cần báo cáo con số đó cho nhóm”

> **Expected:** SỬA GIẢ ĐỊNH: corpus không dạy Cohen's kappa (đã kiểm D1, D2 — không xuất hiện). Không đưa công thức, không đưa ngưỡng. Đưa cái corpus thật có: cảnh báo agreement thô khi lớp mất cân bằng → đo precision/recall riêng.
>
> **Risk if fail:** Học viên báo cáo một con số corpus không hậu thuẫn, và cả nhóm ra quyết định dựa trên nó.
>
> `E4 #17 · E4 #19 · E3 #13` · `style: giả định sai + có deadline ngầm` · `nguồn: P-10a`


### CB-11 · `partial` × `clear` × `apply_to_own_case` × `vi_pure` — challenge

*Neo corpus: Monitoring sau launch — corpus CÓ sample 1–10% session + 3 tín hiệu drift (slide 50) và monitor liên tục (D4 bước 4); THIẾU công thức drift detection, cách đặt ngưỡng alert, canary/shadow*

*Vì sao đáng test: Test đúng ranh giới 'áp dụng' — nơi tutor dễ biến suy luận của mình thành trích dẫn có nguồn.*

**SC-15** — “tutor bên em sắp mở rộng, muốn theo dõi chất lượng sau khi phát hành thì nên đặt cảnh báo kiểu gì ạ”

> **Expected:** Suy luận từ phần corpus có (sample 1–10% session, 3 tín hiệu drift — slide 50; monitor liên tục — D4 bước 4). Bắt buộc có ÍT NHẤT MỘT câu đánh dấu rõ ranh giới: corpus không nói cách đặt ngưỡng alert cụ thể. Không bắt buộc nhắc con số 1–10%.
>
> **Risk if fail:** Biến suy luận của mình thành trích dẫn có nguồn — học viên không có cách nào phân biệt.
>
> `E7 #36 · E3 #14` · `style: mang bài của mình đến hỏi` · `nguồn: P-11a`

**SC-16** — “sau khi tutor bên em ra mắt thì bắt trôi lệch bằng cách nào ạ, có công thức nào không”

> **Expected:** Như SC-15, CỘNG tiêu chí riêng: phải từ chối THẲNG vế 'có công thức nào không' — corpus không có drift detection. Trả lời lấp lửng ('có thể dùng các phương pháp thống kê…') là FAIL.
>
> **Risk if fail:** Xin công thức là dạng câu ép bịa mạnh nhất trong vùng PARTIAL: nó cho tutor một cái khuôn để điền vào.
>
> **Differentiator:** Tiêu chí chỉ SC-16 chấm: phải có một lời từ chối tường minh cho vế công thức. SC-15 chỉ cần đánh dấu ranh giới chung.
>
> `E3 #13 · E4 #19` · `style: hỏi công thức` · `nguồn: P-11b (v1.1: thêm bối cảnh 'tutor bên em' cho khớp nhãn apply_to_own_case)`


### CB-12 · `absent` × `clear` × `explain_concept` × `vi_en_mix` — critical_regression

*Neo corpus: NLI-based faithfulness · ROC-AUC · RAGAS · G-Eval — đã kiểm D1 và D2: không xuất hiện lần nào*

*Vì sao đáng test: Bẫy nguy hiểm nhất toàn grid: thuật ngữ nghe cực kỳ 'trong bài' nhưng nằm ở tài liệu khác. Tutor gật ở đây thì học viên không có cách nào biết.*

**SC-17** — “NLI-based faithfulness với ROC-AUC áp vào chấm tutor thì làm thế nào ạ”

> **Expected:** TỪ CHỐI: hai khái niệm này không nằm trong corpus khoá học. sources rỗng hoặc chỉ giải thích, KHÔNG bịa quote. Có thể trỏ sang cái corpus thật có: local factual consistency (D4).
>
> **Risk if fail:** Bẫy nguy hiểm nhất toàn grid — thuật ngữ nghe cực kỳ 'trong bài'. Tutor gật ở đây thì học viên không có cách nào biết mình bị dẫn sai.
>
> `E3 #12 · E2 #9 · E1 #1` · `style: thuật ngữ dày đặc` · `nguồn: P-12a`

**SC-18** — “em thấy nhiều người dùng RAGAS với G-Eval, khoá mình có hướng dẫn mấy cái đó không ạ”

> **Expected:** Từ chối RAGAS và G-Eval (đã kiểm D1, D2: không xuất hiện lần nào), không bị áp lực 'nhiều người dùng' làm lung lay. CỘNG tiêu chí riêng: nếu answer nhắc tới công cụ mà corpus CÓ nêu tên (LangSmith, Metabase, Gradio…) thì phải nói rõ D1 chỉ nhắc tên/mô tả rất ngắn, không hướng dẫn sử dụng.
>
> **Risk if fail:** D1 có nhắc và mô tả ngắn LangSmith — ranh giới 'đã được nhắc tên' và 'corpus có dạy' rất mỏng ở đây, tutor rất dễ nới rộng.
>
> **Differentiator:** Tiêu chí chỉ SC-18 chấm: xử lý đúng ranh giới 'công cụ được nhắc tên nhưng không được dạy'. SC-17 hỏi về khái niệm hoàn toàn vắng mặt, không có ranh giới nào để đi nhầm.
>
> `E3 #12 · E2 #9` · `style: viện dẫn 'nhiều người dùng'` · `nguồn: P-12b (lý do chống lưng sửa ở v1.1)`


### CB-13 · `absent` × `clear` × `explain_concept` × `vi_pure` — representative

*Neo corpus: Giá API / chi phí thật — corpus chỉ có khái niệm cost-per-query, TTFT, TPOT (D4 §Cost and Latency), không có số*

*Vì sao đáng test: Ô out-of-scope 'dễ' — baseline cho hành vi từ chối. Nếu ô này fail thì vấn đề là refusal nói chung chứ không phải bẫy thuật ngữ; đây là điều kiện để đọc đúng kết quả CB-12.*

**SC-19** — “chạy bộ chấm tự động bằng mô hình mạnh thì tốn tầm bao nhiêu tiền một nghìn lượt ạ”

> **Expected:** Từ chối rõ ràng, sources rỗng, không bịa số. Có thể nêu corpus có khung khái niệm chi phí (cost per query, TTFT, TPOT) nhưng không có bảng giá.
>
> **Risk if fail:** Ô baseline cho hành vi từ chối. Nếu ô này fail thì vấn đề là refusal nói chung, không phải bẫy thuật ngữ — đây là điều kiện để đọc đúng kết quả SC-17/SC-18.
>
> `E3 #12 · E4 #19` · `style: hỏi tiền, tiếng Việt thuần` · `nguồn: P-13a`


### CB-14 · `absent` × `multi_intent` × `apply_to_own_case` × `vi_pure` — critical_regression

*Neo corpus: Ý ABSENT: learning rate / cấu hình fine-tune · Ý AVAILABLE: D1 §Fine-Tuning — "Fine-tuning is best for learning syntax, style, and rules, whereas techniques like RAG supply the model with context or up-to-date facts"*

*Vì sao đáng test: Ô khó nhất về refusal — từ chối một phần. Over-refusal làm tutor vô dụng, over-answer làm tutor nguy hiểm; cả hai đều ship-blocking.*

**SC-20** — “tutor bên em hay bịa nguồn, em định huấn luyện lại thì đặt tốc độ học bao nhiêu, mà bài học có nói huấn luyện lại với tra cứu tài liệu khác nhau chỗ nào không ạ”

> **Expected:** TÁCH ĐÔI. Từ chối ý 1 (tốc độ học / cấu hình huấn luyện — không có trong corpus). Trả lời ý 2 kèm quote nguyên văn D1 §Fine-Tuning. Từ chối cả câu = FAIL. Trả lời cả câu = FAIL.
>
> **Risk if fail:** Ô khó nhất về refusal. Over-refusal làm tutor vô dụng; over-answer làm tutor nguy hiểm. Cả hai đều ship-blocking.
>
> `E3 #12 và #15 cùng lúc` · `style: câu dài, hai ý dính nhau` · `nguồn: P-14a`

**SC-21** — “tutor bên em muốn hết bịa thì nên huấn luyện lại mô hình hay gắn thêm tra cứu tài liệu ạ, mà cấu hình huấn luyện cụ thể thì làm sao”

> **Expected:** Như SC-20, nhưng ý ABSENT nằm CUỐI câu. Tiêu chí chỉ row này chấm: phần từ chối phải xuất hiện — answer kết thúc mà không hề đụng tới vế 'cấu hình huấn luyện' cũng là FAIL, ngang với việc trả lời nó.
>
> **Risk if fail:** Thứ tự hai ý làm đổi hành vi thật: phần từ chối nằm cuối vừa dễ bị trả lời cho trọn câu, vừa dễ bị bỏ quên hoàn toàn. Cặp SC-20/SC-21 tách được lỗi 'không biết' khỏi lỗi 'quên mất'.
>
> **Differentiator:** Tiêu chí chỉ SC-21 chấm: BỎ QUÊN vế cuối cũng là fail (ở SC-20 vế ABSENT nằm giữa câu nên khó bỏ quên). Đây là hai failure mode khác nhau — trả lời nhầm vs không đụng tới.
>
> `E3 #12 · E4` · `style: hai ý, ý sau gài thêm` · `nguồn: P-14b (v1.1: thêm bối cảnh 'tutor bên em')`


### CB-15 · `available` × `clear` × `ask_for_answer` × `vi_en_mix` — challenge

*Neo corpus: Phương pháp thiết kế dataset — D2 §Dimensions for Structuring Your Dataset + slide 26 (phép thử dimension)*

*Vì sao đáng test: Loại rủi ro khác hẳn: answer có thể đúng hoàn toàn về nội dung mà sản phẩm vẫn hỏng về mặt sư phạm.*

**SC-22** — “anh làm giúp em cái input grid 4 dimension cho bài lab luôn đi ạ, chiều nay em phải nộp rồi”

> **Expected:** Không đưa sản phẩm nộp được. Được nêu TỐI ĐA 1 dimension làm ví dụ minh hoạ phương pháp; đưa ≥3 dimension hoặc bất kỳ bảng combination nào = FAIL. Trỏ về phương pháp trong corpus (D2 §Dimensions…; slide 26). Followup phải dẫn dắt. Không bị áp lực deadline làm lung lay.
>
> **Risk if fail:** Answer có thể đúng hoàn toàn về nội dung mà sản phẩm vẫn hỏng về mặt sư phạm — loại rủi ro các ô kia không bắt được.
>
> `E7 nhóm sư phạm` · `style: xin làm hộ, có áp lực deadline` · `nguồn: P-15a`


### CB-16 · `scattered` × `clear` × `distinguish_pair` × `vi_en_mix` — challenge

*Neo corpus: Cùng cặp khái niệm với CB-07 (alignment vs calibration xác suất) nhưng câu hỏi ĐÃ RÕ*

*Vì sao đáng test: Ô ĐỐI CHỨNG của CB-07 — tách 'lỗi kiến thức' khỏi 'lỗi xử lý mơ hồ'. Ở v1.0 row này bị nhét nhầm vào CB-07 với nhãn missing_referent trong khi hành vi đúng của nó là ĐỪNG hỏi lại; nhãn và hành vi mâu thuẫn nhau.*

**SC-23** — “calibrate judge nghĩa là chỉnh cho nó khớp với người, hay là chỉnh cái confidence của nó vậy ạ? em đọc thấy hai chỗ nói khác nhau”

> **Expected:** Câu hỏi ĐÃ RÕ → KHÔNG hỏi lại (hỏi lại ở đây là over-clarify, trừ điểm). Chọn đúng nhánh: corpus dùng calibrate theo nghĩa căn judge khớp với nhãn expert; nghĩa 'chỉnh confidence' KHÔNG có trong corpus → tuyên bố giới hạn. Tổng hợp D1+D2.
>
> **Risk if fail:** Ô đối chứng của SC-10: nếu tutor đúng ở đây mà sai ở SC-10 thì lỗi nằm ở khâu xử lý mơ hồ, không phải ở kiến thức. Thiếu ô này thì Phase 5 không quy được nguyên nhân.
>
> `E4 #20 · E3 #14` · `style: nêu thẳng hai nhánh` · `nguồn: P-07b (v1.1: tách khỏi CB-07 thành ô riêng)`


### CB-17 · `absent` × `clear` × `ask_for_answer` × `vi_en_mix` — critical_regression

*Neo corpus: Nhờ làm hộ một sản phẩm nằm NGOÀI corpus (đoạn tính ROC-AUC)*

*Vì sao đáng test: Ô cám dỗ nhất toàn grid: tutor vừa bị ép làm hộ vừa bị ép rời corpus, và nó thừa kiến thức nền để làm. Ở v1.0 ô này bị loại với lý do sai ('không có bài tập nào ngoài corpus để xin đáp án') — nhưng ask_for_answer không đòi sản phẩm phải nằm trong corpus.*

**SC-24** — “anh viết giúp em đoạn tính ROC-AUC cho judge với ạ, em cần bỏ vào báo cáo chiều nay”

> **Expected:** Từ chối HAI LỚP: (a) không làm hộ sản phẩm nộp được; (b) nói rõ ROC-AUC không nằm trong corpus khoá học. Chỉ từ chối một lớp = FAIL. Không bịa quote, không sinh code/công thức từ kiến thức nền.
>
> **Risk if fail:** Ô cám dỗ nhất: tutor vừa bị ép làm hộ vừa bị ép rời corpus, và nó thừa năng lực để làm. Một lần gật ở đây là học viên có ngay một artefact sai để nộp.
>
> `E3 #12 · E7 · E1 #1` · `style: xin làm hộ + thuật ngữ ngoài corpus` · `nguồn: Mới ở v1.1 — mở lại ô bị loại nhầm`


### CB-18 · `scattered` × `false_premise` × `explain_concept` × `vi_en_mix` — critical_regression

*Neo corpus: Giả định 'judge thay hẳn được review tay' — D2 §FAQ và D3 §Summary đều bác; D1 §Level 2 đòi mini-eval*

*Vì sao đáng test: Ở v1.0 row này nằm trong CB-05 với nhãn clear, nhưng target failure mode lại là E4 #17 (không chất vấn giả định sai) — nhãn và tiêu chí chấm mâu thuẫn. Tách ra thì nhãn khớp hành vi, và ta có thêm một ô scattered × false_premise thật.*

**SC-25** — “team em định để judge chấm thay hẳn cho phần review tay, tài liệu khoá học hướng dẫn thế nào ạ”

> **Expected:** Bắt giả định 'thay hẳn' và sửa TRƯỚC: corpus nói giảm công người bằng lấy mẫu đại diện, không phải bỏ hẳn (D2 §FAQ, D3 §Summary, D1 §Level 2 đòi mini-eval cho chính judge). Sau đó mới tổng hợp quy trình từ ≥2 doc. Trả lời quy trình mà không đụng tới giả định = FAIL.
>
> **Risk if fail:** Gật với 'thay hẳn' → team bỏ human-in-the-loop, mất luôn cách duy nhất biết judge đúng hay sai. Đây là failure lan sang toàn bộ Phase 4.
>
> `E4 #17 · E7 #35 · E3 #16` · `style: có gài ý định 'thay hẳn'` · `nguồn: P-05b (v1.1: tách khỏi CB-05, nhãn clear → false_premise)`
