# Link trace

**Backend:** LangSmith · **Project:** `ai-evaluation`
**Link:** https://smith.langchain.com/ → project `ai-evaluation`

## Các vòng đã log

| Vòng | Dataset | Số trace | Ghi chú |
|---|---|---|---|
| results-v1 | dataset v1.2 (gold cũ) | 0 | Chạy khi tracing còn tắt — giữ lại để đối chiếu, KHÔNG dùng làm bằng chứng trace |
| **results-v2** | **dataset v1.3** | **25** | Vòng chính thức: `tutor-run`, mỗi trace có input, output, tool_calls, tokens, cost |

| judge vòng 1 | prompt v2 | **25** | `judge-run`, verdicts-v1.jsonl |
| judge vòng 2 | prompt v3 | **25** | `judge-run`, verdicts-v2.jsonl |

Tổng: **75 trace** trong project `ai-evaluation` (25 tutor + 50 judge).

> Lưu ý khi điền `.env`: đặt key **một mình trên một dòng**. Nếu viết
> `LANGSMITH_API_KEY=lsv2_... # ghi chú` thì phần ghi chú bị tính là một phần của key
> và LangSmith trả lỗi `latin-1 ... ordinal not in range(256)`.
