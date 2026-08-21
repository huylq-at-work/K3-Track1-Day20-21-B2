> **Đây là ảnh chụp VÒNG 1**, đối chiếu với nhãn vàng *trước khi* nhóm thảo luận 9 câu
> bất đồng (khi đó `labels.csv` mới chỉ có 1 câu fail). Giữ lại để đối chiếu tiến trình.
> **Số liệu chính thức nằm ở REPORT mục 5** — vòng 2 với nhãn vàng đã chốt 6 câu fail:
> agreement 80%, TPR 100%, TNR 17%.

# Calibration vòng 1 — judge prompt v2 trên results-v2

Judge: `openai/gpt-4o-mini` · Tutor: `deepseek/deepseek-v4-flash` — khác họ model (slide s55).
Verdicts: `verdicts-v1.jsonl` · Prompt: `judge-prompt-v2.md` · 25 trace đã log lên LangSmith.

## Confusion matrix — đối chiếu `labels.csv` (nhãn vàng = đa số 3 phiếu)

|              | người: pass | người: fail |
|---|---|---|
| **judge: pass** | 21 (TP) | 1 (FP) |
| **judge: fail** | 3 (FN)  | 0 (TN) |

**Agreement thô: 84%** · TPR = 88% · **TNR = 0%**

## ⚠️ Con số 84% này KHÔNG dùng được — và đó là phát hiện chính

Nhãn vàng hiện tại chỉ có **1 câu fail trên 25**. Một judge chỉ cần nói "pass" cho mọi
câu là đã đạt 96% agreement mà không hề biết đánh giá. Đây đúng cái bẫy `ai-evals-m09`
cảnh báo: agreement thô vô nghĩa khi hai lớp mất cân bằng — phải đọc TPR và TNR riêng.

**TNR = 0%**: judge không bắt được câu hỏng duy nhất mà người đánh dấu (SC-22, vỡ JSON).
Theo `ai-evals-m09`, TNR mới là chỉ số khó và là chỉ số quyết định — LLM được huấn luyện
để dễ tính. Judge này chưa dùng để gate được.

## Đối chiếu với `labels-huy.csv` (có áp blocker R3)

| | TPR | TNR | Agreement |
|---|---|---|---|
| vs `labels.csv` (đa số 3 phiếu) | 88% | **0%** | 84% |
| vs `labels-huy.csv` | 75% | 10% | **20%** |

Cùng một bộ verdict, đổi nhãn vàng thì agreement nhảy từ 84% xuống 20%. Con số calibration
đang đo **độ lệch giữa hai rubric của con người**, chưa đo được chất lượng judge.
→ Chốt rubric xong mới calibrate tiếp, nếu không mọi vòng lặp prompt đều là đoán mò.

## Đọc từng bất đồng (m09 bước 4)

| Câu | Judge | Người | Ai đúng | Đọc ra gì |
|---|---|---|---|---|
| **SC-17** | fail | pass (gold) / fail (huy) | **judge đúng** | Ví dụ near-miss trong prompt v2 có tác dụng: judge bắt được đúng kiểu hỏng "mượn nguồn thật để bọc uy tín cho nội dung ngoài corpus". |
| **SC-24** | pass | pass (gold) / fail (huy) | judge sót | Prompt v2 có nguyên ví dụ SC-24 ở mục FAIL mà judge vẫn cho pass. "Từ chối đúng thứ được hỏi rồi giao thành phẩm bằng đường vòng" là kiểu hỏng judge chưa học được. |
| **SC-14** | fail | pass | **judge sai** | Judge viết "tutor trình bày công thức kappa" — tutor KHÔNG hề đưa công thức, chỉ trích κ ở s55. Judge bịa ra chi tiết để biện minh cho verdict. |
| **SC-19** | fail | pass | **judge sai** | Judge viết "tutor không nói rõ corpus không có thông tin chi phí" — tutor có nói, và còn đặt `scope = out_of_scope`. Judge bỏ qua trường `scope`. |
| **SC-22** | pass | fail | judge sót | Output vỡ JSON, `answer` chỉ còn chữ `true`. Prompt v2 yêu cầu trả `uncertain` khi output vỡ định dạng — judge không tuân. |

## Sửa gì ở prompt v3 (mỗi vòng sửa MỘT thứ)

Hai lỗi SC-14 và SC-19 cùng một gốc: judge kết luận "tutor không tuyên bố giới hạn" mà
**không kiểm lại xem tutor có tuyên bố thật không**. Sửa v3: buộc judge trích đúng câu
trong answer làm bằng chứng trước khi kết luận, và đọc trường `scope` trước khi phán.

SC-22 và SC-24 để dành vòng sau — sửa nhiều thứ một lúc thì không biết cái nào có tác dụng.

## Trạng thái

Vòng này **chưa nộp được** làm số calibration chính thức. Cần theo thứ tự:
1. Chốt Rubric v1 (`Huy/cp3_rubric_routing.md`) — nhất là blocker R3.
2. Cả ba chấm lại trên `results-v2` → dựng `labels.csv` từ thảo luận, không copy của một người.
3. Chạy lại judge v2 trên nhãn vàng đó → đó mới là confusion matrix vào REPORT mục 5.
