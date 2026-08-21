# Link trace

**Backend:** LangSmith · **Project:** `ai-evaluation`
**Link:** https://smith.langchain.com/ → project `ai-evaluation`

## Các vòng đã log

| Vòng | Dataset | Số trace | Ghi chú |
|---|---|---|---|
| results-v1 | dataset v1.2 (gold cũ) | 0 | Chạy khi tracing còn tắt — giữ lại để đối chiếu, KHÔNG dùng làm bằng chứng trace |
| **results-v2** | **dataset v1.3** | **25** | Vòng chính thức: `tutor-run`, mỗi trace có input, output, tool_calls, tokens, cost |

Judge sẽ log tiếp vào cùng project khi chạy `eval/judge.py`.

> Lưu ý khi điền `.env`: đặt key **một mình trên một dòng**. Nếu viết
> `LANGSMITH_API_KEY=lsv2_... # ghi chú` thì phần ghi chú bị tính là một phần của key
> và LangSmith trả lỗi `latin-1 ... ordinal not in range(256)`.
