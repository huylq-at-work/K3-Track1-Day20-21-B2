# AI Support Log — Huy

Ghi lại tôi dùng AI ở đâu, AI sai ở đâu, và tôi quyết lại gì.

---

## Bảng theo bước

| # | Bước | Dùng AI làm gì | Tôi làm gì | Kết quả |
|---|---|---|---|---|
| 1 | P1 · Chuẩn bị | Đọc slide Day 20–21, dựng bản đồ corpus 4 tầng, taxonomy 37 failure mode, menu **9 dimension ứng viên** | Chốt lấy 4, bỏ 5, ghi lý do từng cái | Grid 4 dimension ở mục 1 |
| 2 | P1 · Bước 3 | — | Tự loại tổ hợp phi lý (128 → 96), tự chọn 18 ô | Phễu tổ hợp ở mục 1 |
| 3 | P1 · Bước 5 | Paraphrase mỗi combination thành 2 câu tự nhiên | Keep / Rewrite / Reject từng câu | 25 rows dataset |
| 4 | P0 · Dọn nền | Grep 18 doc corpus thật, remap 55 anchor, verify tồn tại bằng code | Duyệt bảng remap, chốt 6 gold label viết lại | dataset v1.3 |
| 5 | P2 · Chấm tay | Dựng bản chấm nháp 25 câu kèm lý do từng câu | Duyệt lại, đổi 3 câu, chốt quy tắc R3 | `labels-huy.csv` |
| 6 | P3 · Rubric | Soạn nháp R1–R9 + routing map từ taxonomy | Chốt R3 thành gate cấp bộ thay vì blocker | REPORT mục 3–4 |
| 7 | P4 · Code checks | Viết 2 hàm `check_*` mới | Chọn tiêu chí nào đáng thêm | `followup_quality`, `sources_distinct` |
| 8 | P4 · Judge | Viết judge prompt v2 → v3 | Chốt mỗi vòng chỉ sửa một thứ | 2 vòng calibration |
| 9 | P5–P6 | Tính slice, dựng scorecard | Đặt ngưỡng gate, chốt verdict HOLD | REPORT mục 5–7 |

---

## Ba chỗ AI sai, và tôi sửa thế nào

### 1. AI khẳng định chắc chắn về nội dung corpus mà không kiểm

Ở bản nghiên cứu Phase 1, AI xếp con số ">90% agreement" vào nhóm "không có trong corpus,
thuộc Field Guide của Hamel". Tôi kiểm trực tiếp trên hamel.dev thì con số **có thật**.

Gold label của SC-04/SC-05 dựng trên khẳng định sai đó bắt tutor **phủ nhận** một con số
có thật — tức tutor càng chính xác càng bị chấm fail.

**Tôi chốt thành luật:** mọi khẳng định *"corpus không có X"* phải kèm từ khoá đã search
và số hit. Áp luật này ở P0 thì lòi ra tiếp 6 gold label sai chiều nữa.

### 2. AI dựng cả dataset trên corpus giả định, không đọc corpus thật

Toàn bộ Phase 1 giả định corpus là 4 tài liệu (2 bài Hamel + AI Engineering Ch.3, Ch.4).
Corpus thật trong repo là **18 tài liệu khác**: không có bài llm-judge của Hamel, không có
Ch.3; đổi lại có 14 module khoá học và bài của Anthropic.

11/25 rows neo vào nguồn không tồn tại → sẽ fail `citation_exists` ngay ở làn code, và pass
rate thu được là số rác.

**Tôi bắt dừng lại làm P0 trước khi chạy bất cứ vòng eval nào**, remap 55 anchor và verify
bằng code (55/55 tồn tại). Nếu chạy trước rồi mới phát hiện thì mất cả tiền lẫn một vòng.

### 3. AI đề xuất tự nộp nhãn do nó sinh làm "nhãn người"

Khi tôi nhờ chấm hộ 25 câu, AI cảnh báo trước rằng nhãn AI dùng làm nhãn người sẽ thổi
phồng agreement ở Phase 4 vì judge cũng là LLM. Cảnh báo đúng.

**Tôi quyết:** dùng bản chấm đó làm **nháp**, tự duyệt lại từng câu rồi mới chốt. Tôi đổi
3 câu so với bản nháp (SC-06, SC-10, SC-18 — cho nhất quán với SC-07 và SC-23 vốn đã pass
vì cùng hành vi). Con số agreement báo cáo là của người, không phải của AI.

---

## Chỗ tôi giữ quyền quyết, không giao cho AI

- **Chọn dimension nào lên grid, bỏ cái nào** — AI chỉ đưa menu 9 ứng viên.
- **Loại tổ hợp phi lý và chọn 18 ô** — kèm lý do từng ô bị loại.
- **R3 là blocker hay gate cấp bộ.** Đây là quyết định đắt nhất cả bài: đặt R3 làm blocker
  thì pass rate 16%, không thì 64%. Tôi chọn gate cấp bộ vì nếu để blocker thì 19/24 câu
  fail vì cùng một lý do, và nhãn người chỉ lặp lại điều `code_checks.py` đã nói — làn
  người mất hết giá trị.
- **Ngưỡng gate và verdict HOLD** — mọi ngưỡng ở mục 6 là quyết định sản phẩm, không phải
  quyết định kỹ thuật.

---

## Ba thứ mang về

1. **Kiểm được bằng code thì đừng gọi LLM.** Làn code bắt 13/24 lỗi trích dẫn với $0;
   judge tốn tiền mà sót đúng những lỗi đó.
2. **Agreement thô là con số biết nói dối.** Judge đạt 76% agreement trong khi TNR = 17% —
   nó cho qua 5/6 lỗi thật. Phải đọc TPR và TNR riêng.
3. **Bất đồng giữa người chấm thường là lỗi rubric, không phải lỗi người.** Thống nhất một
   định nghĩa đẩy agreement từ 16% lên 64% mà không ai phải đổi ý về câu nào.
