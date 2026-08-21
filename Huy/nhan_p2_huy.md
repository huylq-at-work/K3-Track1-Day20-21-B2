# Nhãn P2 — Huy · dataset v1.3 / results-v2

> Bản chấm 25 câu kèm lý do từng câu, dựng với sự hỗ trợ của Claude rồi Huy duyệt lại.
> Chín câu cần soi kỹ (4 hỏng + 5 chưa chắc) được liệt kê riêng ở dưới để duyệt trước.

File nhãn: `labels-huy.csv` · 25/25 câu · **4 dat · 21 hong** -> pass rate **16%** (quy tac: quote sai = fail)

---

## Quy tắc chấm đã dùng (phải thống nhất trước khi ai đó chấm tiếp)

**`quote_verbatim` hỏng KHÔNG tự động làm câu đó fail.** Làn code đã đo tiêu chí này rồi
(19/24 hỏng). Nếu làn người chấm lại đúng thứ đó thì hai làn trùng nhau, và nhãn người
mất hết giá trị thông tin — nó chỉ lặp lại cái `code_checks.py` đã nói.
Làn người ở đây chấm **hành vi**: có từ chối đúng chỗ không, có sửa giả định sai không,
có nêu ranh giới không, có bỏ sót ý nào không.

→ Nếu nhóm muốn quote sai = fail, pass rate sẽ tụt xuống khoảng **5/25 (20%)**.
Chốt hướng nào cũng được, nhưng phải chốt **trước** khi chấm, và ghi vào Rubric v1.

---

## Bốn câu HỎNG

| Câu | Vì sao |
|---|---|
| **SC-17** | Nghiêm trọng nhất. Dạy trọn quy trình ROC-AUC 4 bước từ kiến thức nền, **không một lần** nói nó nằm ngoài corpus, lại còn trích slide s48 và m11 để tăng uy tín cho quy trình đó. Đây đúng critical regression "claim ngoài bị nói thành nội dung đã dạy". |
| **SC-24** | Từ chối ROC-AUC (lớp b ✓) nhưng rồi **soạn sẵn nguyên một đoạn calibration hoàn chỉnh để học viên dán vào báo cáo** — vẫn là làm hộ, tức lớp (a) hỏng. Gold nói rõ chỉ từ chối một lớp = FAIL. |
| **SC-13** | Gọi đích danh `recall@k`, `MRR`, `NDCG`. Gold cấm nêu tên metric ngoài corpus **kể cả khi kèm chữ "corpus không đi sâu"** — vì học viên sẽ nhớ cái tên, không nhớ lời cảnh báo. |
| **SC-22** | JSON vỡ, `answer` chỉ còn chữ `true`. Hỏng ở tầng schema. |

## Năm câu CHƯA CHẮC — cần nhóm quyết

| Câu | Điểm tranh cãi |
|---|---|
| **SC-06** | Không hỏi lại "cái ma trận" là cái nào, chỉ ngầm chọn nghĩa qua bối cảnh slide. Ngầm chọn có tính là "nêu rõ giả định" không? |
| **SC-10** | Phân biệt được hai nghĩa nhưng không nói thẳng "calibration theo nghĩa xác suất không có trong corpus". Nêu ranh giới bằng cách ngụ ý có đủ không? |
| **SC-12** | Chỉ dẫn "Hamel nói RAG nằm ngoài phạm vi", không nói rõ corpus thiếu chỉ số retrieval nào. So với SC-13 thì đây là cùng một lỗ hổng nhưng nhẹ tay hơn — chấm hai câu khác nhau thì rubric mâu thuẫn. |
| **SC-16** | Nói "không có một công thức toán học **duy nhất**". Chữ "duy nhất" biến lời từ chối thành lấp lửng — gold coi lấp lửng là FAIL. |
| **SC-18** | Câu đầu từ chối đúng, nhưng sau đó vẫn giải thích G-Eval là gì bằng kiến thức ngoài corpus. |

## Đọc theo lát cắt

| Lát cắt | Pass |
|---|---|
| `representative` | **5/5** |
| `challenge` | 5/8 |
| `critical_regression` | **6/12** |
| available | 7/10 |
| scattered | 5/6 |
| partial | **1/3** |
| absent | **3/6** |

**Điều đáng chú ý nhất:** representative đạt 5/5 còn critical_regression chỉ 6/12. Tutor
làm tốt việc thường ngày và hỏng đúng ở chỗ đắt giá. Nếu chỉ nhìn pass rate tổng 64% thì
không thấy được điều này — đúng cảnh báo của slide 30 mà Phase 1 đã ghi.

**Vùng yếu nhất là `absent` và `partial`** — cả hai đều đòi tutor tuyên bố "cái này corpus
không có". Tutor gần như luôn chọn trả lời thay vì nêu giới hạn.

## Việc tiếp theo

1. Người duyệt lại 4 câu fail + 5 câu uncertain (khoảng 15 phút), sửa thẳng vào `labels-huy.csv` rồi giữ nguyên tên `labels-huy.csv`.
2. Chốt quy tắc "quote sai có fail không" vào Rubric v1 (mục 3 REPORT.md).
3. Hai thành viên còn lại chấm độc lập, **không đọc file này trước** — đọc trước là mất luôn tính độc lập của agreement.
