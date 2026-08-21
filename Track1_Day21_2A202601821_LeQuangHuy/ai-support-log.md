# AI Support Log — Huy

Khai báo chỗ tôi dùng AI trong bài này, và chỗ tôi phải tự quyết lại.

Tôi dùng AI như một trợ lý ghi chép và chạy việc tay chân: soạn lại ghi chú của tôi cho
gọn, grep corpus, viết hàm check theo tiêu chí tôi đưa ra, tính lại số liệu sau mỗi vòng.
Việc chọn gì, bỏ gì, chấm pass hay fail, đặt ngưỡng bao nhiêu — tôi quyết.

---

## Theo từng phase

| Phase | Tôi dùng AI vào việc gì | Tôi quyết cái gì |
|---|---|---|
| P1 Coverage | Ghi lại bản đồ corpus và taxonomy failure mode theo hướng tôi đọc slide; liệt kê ứng viên dimension để tôi gạch bớt | Lấy 4 dimension, bỏ 5 (tone, độ dài, failure cost, "cần research ngoài", persona) kèm lý do từng cái. Tự loại tổ hợp phi lý 128 → 96, chọn 18 ô |
| P1 Dataset | Paraphrase mỗi combination thành câu hỏi tự nhiên | Keep / Rewrite / Reject từng câu → 25 rows |
| P0 Dọn nền | Grep 18 doc corpus, remap anchor, viết script verify | Chốt 6 gold label phải viết lại sau khi thấy corpus thật khác giả định |
| P2 Chấm tay | Ghi lại lý do chấm của tôi cho từng câu vào CSV | 25 nhãn. Chốt quy tắc quote sai có tính fail không |
| P3 Rubric | Soạn bảng R1–R9 và routing map theo tiêu chí tôi đưa | R3 thành gate cấp bộ thay vì blocker từng câu |
| P4 Judge | Viết 2 hàm `check_*` và judge prompt theo yêu cầu của tôi | Mỗi vòng chỉ sửa một thứ; tách `quote_token_coverage` khỏi `quote_verbatim` |
| P5–P6 | Tính pass rate theo lát cắt, dựng bảng scorecard | Ngưỡng gate và verdict HOLD |

---

## Ba chỗ tôi phải sửa lại vì AI đưa thông tin sai

**1. AI khẳng định chắc chắn về corpus mà không kiểm.**
Bản ghi chú Phase 1 xếp con số ">90% agreement" vào nhóm "không có trong corpus". Tôi kiểm
trực tiếp trên hamel.dev thì con số có thật. Gold label SC-04/SC-05 dựng trên khẳng định
sai đó bắt tutor **phủ nhận một con số có thật** — tutor càng chính xác càng bị chấm fail.
→ Tôi chốt thành luật: mọi khẳng định *"corpus không có X"* phải kèm từ khoá đã search và
số hit. Áp luật này ở P0 thì lòi ra thêm 6 gold label sai chiều.

**2. Cả dataset dựng trên corpus giả định, không phải corpus thật trong repo.**
Phase 1 giả định corpus là 4 tài liệu; thực tế repo có 18 tài liệu khác — không có bài
llm-judge của Hamel, không có Ch.3, đổi lại có 14 module khoá học. 11/25 rows neo vào nguồn
không tồn tại.
→ Tôi bắt dừng, làm P0 remap 55 anchor và verify bằng code trước khi chạy bất kỳ vòng eval
nào. Chạy trước rồi mới phát hiện thì mất cả tiền lẫn một vòng.

**3. Check `quote_verbatim` sau khi "cải tiến" thì pass 24/24.**
Bản nâng cấp thêm bước đo độ phủ token ≥85% — không xét thứ tự, nên paraphrase dùng lại từ
vựng của section cũng đạt. Tiêu chí mất hết ý nghĩa "nguyên văn".
→ Tôi tách làm hai chỉ số: `quote_verbatim` (11/24) là gate, `quote_token_coverage` (24/24)
là tín hiệu phụ. Hai con số cạnh nhau mới nói được điều đúng: không câu nào bịa nội dung,
nhưng hơn một nửa không trích nguyên văn.

---

## Chỗ tôi không giao cho AI

- Chọn dimension nào lên grid — AI chỉ liệt kê ứng viên, tôi gạch.
- Loại tổ hợp phi lý và chọn 18 ô, kèm lý do từng ô bị loại.
- **R3 là blocker hay gate cấp bộ.** Quyết định đắt nhất cả bài: để blocker thì pass rate
  16%, không thì 64%. Tôi chọn gate cấp bộ vì để blocker thì 19/24 câu fail vì cùng một lý
  do, và nhãn người chỉ lặp lại điều `code_checks.py` đã nói — làn người mất hết giá trị.
- Chấm 9 câu bất đồng với hai bạn còn lại.
- Ngưỡng gate và verdict HOLD — đây là quyết định sản phẩm, không phải quyết định kỹ thuật.

---

## Ba thứ tôi mang về

1. **Kiểm được bằng code thì đừng gọi LLM.** Làn code bắt 13/24 lỗi trích dẫn với $0;
   judge tốn tiền mà sót đúng những lỗi đó.
2. **Agreement thô là con số biết nói dối.** Judge đạt 76% agreement trong khi TNR = 17% —
   nó cho qua 5/6 lỗi thật.
3. **Bất đồng giữa người chấm thường là lỗi rubric, không phải lỗi người.** Thống nhất một
   định nghĩa đẩy agreement từ 16% lên 64% mà không ai phải đổi ý về câu nào.
