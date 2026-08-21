# AI Support Log — Cường

Ghi nhận mức độ hỗ trợ của AI trong quá trình thực hiện bài lab AI Evaluation.

---

## 1. Bảng ghi nhận hỗ trợ

| # | Bước | AI hỗ trợ những gì (mức tối thiểu) | Tôi tự làm & kiểm chứng thế nào |
|---|---|---|---|
| 1 | **Debug kết quả chạy Tutor** | Hỗ trợ viết lệnh lọc nhanh các dòng bị lỗi cú pháp JSON trong `results-v1.jsonl` và `results-v2.jsonl`. | Tự đọc trực tiếp trường `raw_content` của SC-15, SC-20, SC-22 để xác định nguyên nhân model in text trước chuỗi JSON `{`. |
| 2 | **Cải tiến hàm Code Check** | Gợi ý cú pháp Regex (`re.split`) để tách chuỗi theo dấu ba chấm `...` và tính toán độ phủ token. | Tự mở file slide gốc `day19-20-deck.md` ở `s26` và `s33`, phát hiện bố cục 2 cột gây lỗi so khớp từ; tự chạy `eval/code_checks.py` để kiểm chứng 24/24 câu đạt PASS. |
| 3 | **Format bảng biểu báo cáo** | Hỗ trợ định dạng bảng Markdown cho ma trận nhầm lẫn (Confusion Matrix) và bảng so sánh đồng thuận. | Tự phân tích số liệu thực tế, đọc từng ca bất đồng giữa các thành viên để hiểu bản chất lens đánh giá. |

---

## 2. Các quyết định độc lập & phần bác bỏ đề xuất của AI

* **Phần AI gợi ý mà tôi bác bỏ:**
  - AI từng đề xuất tự sinh dữ liệu giả lập (mock labels) để test nhanh lệnh agreement. Tôi đã **bác bỏ hoàn toàn (Denied)** và yêu cầu pull dữ liệu chấm thật của các thành viên trong nhóm về để đo lường khách quan.
* **Phần tôi hoàn toàn tự làm:**
  - Tự đọc và chấm điểm độc lập toàn bộ 25 kịch bản theo góc nhìn PM/Nội dung trong `labels-cuong.csv`.
  - Tham gia thảo luận cùng nhóm để thống nhất không dùng $R_3$ làm blocker từng câu, giúp nâng độ đồng thuận của nhóm từ 16% lên 64%.
  - Thống nhất phán quyết cuối cùng: **HOLD — không ship**.
