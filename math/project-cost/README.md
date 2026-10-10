# FFT research project: cost estimate

Updated 2026-10-10. Currency: USD. Scope: the FFT research project, its six-worker research workflow, and separate related ChatGPT conversations.

## Bottom line

- **Recorded cash spend: unknown.** No invoice, credit ledger, or token-usage export was supplied.
- **Using the requested assumption of $30 per 30 active minutes per Astra worker:** six workers active for 30 minutes are valued at **$180**. Eight active hours per worker would be **$2,880**, before separately valued chats.
- **Hypothetical model-only budget:** the explicitly assumed base workload below, excluding coordinator/orchestration work and tools, costs **$2,438.40 at Standard** or **$4,876.80 at Fast**. The low/high Standard scenarios span **$143.40–$14,102.40**. These are scenario outputs, not a measured spending range or confidence interval.

These three accounting views are alternatives. Do not add them together.

## What can be claimed as a lower bound?

The $60/active-worker-hour rate is the user's valuation assumption, not a verified OpenAI hourly tariff. For a verified minimum of `H` active worker-hours, the corresponding conditional lower bound is `60 × H` dollars. If all six workers each completed at least one active half-hour, that conditional bound is $180.

A wall-clock half-hour alone does not establish six active half-hours or any minimum token volume. Waiting, idle time, tools, and inference have different costs. Without paid-usage evidence, **no strictly positive lower bound on incremental cash spend has been established**. This does not mean the work had zero computational value or that the subscription was free.

The reviewed worker effort is `xhigh`. `xhigh` and `max` are reasoning-effort settings, not fixed dollar-per-minute tariffs; this document does not claim that `max`, `ultra`, or a fixed reasoning multiplier was billed. Concurrency and effort settings do not themselves measure consumption. The research's approximately October 8–10 window is not evidence of continuous execution. Archive size, repeated ZIP copies, and file counts are not token meters. A bounded FFT search found 15 related conversations and 492 distinct message IDs; this is scope evidence, not complete-account coverage or token usage. Two checked research records span about 48 hours 56 minutes from October 8 to October 10, which likewise does not measure active worker-hours.

## 1. Time-based valuation requested by the user

| Scenario | Active hours per worker | Six-worker active hours | At assumed $60/worker-hour |
|---|---:|---:|---:|
| One half-hour block | 0.5 | 3 | $180 |
| One-hour illustration | 1 | 6 | $360 |
| Eight-hour illustration | 8 | 48 | $2,880 |
| Twenty-four-hour illustration | 24 | 144 | $8,640 |

Durations are assumptions, not reconstructed activity. Count actual active intervals for each worker; overlapping workers count separately, but idle elapsed time does not. Separate ChatGPT chats need their own agreed valuation or measured usage; their count alone supplies neither.

## 2. Hypothetical API replacement cost

OpenAI publishes a rate for `gpt-6-astra`, so this calculation uses that exact model rather than substituting another model. At Standard speed, the USD rates per million tokens are $10 ordinary input, $1 cached input, $12.50 cache-write input, and $50 output. Requests above 272,000 input tokens use twice the input/cache rates and 1.5 times the output rate for the whole request. Fast doubles the applicable Standard rates. [Official model pricing](https://developers.openai.com/api/docs/models/gpt-6-astra), checked 2026-10-10.

For short-context Standard requests:

```text
ordinary_input = total_input - cached_read_input - cache_write_input
cost = (10 × ordinary_input + 1 × cached_read_input
        + 12.5 × cache_write_input + 50 × billed_output) / 1,000,000
```

Cache-write input is a separate input category, not an additional charge on the same ordinary-input tokens. Actual cache reuse must be measured. [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

Use the billed output total once: it includes reasoning tokens, including reasoning not visible in the final answer. Do not add `reasoning_tokens` again. [Reasoning-token accounting](https://developers.openai.com/api/docs/guides/reasoning)

### Explicit workload assumptions

A “request group” here is an assumed collection of multiple model requests, with no assigned time. Its aggregate tokens can exceed one request's context or output limit. These API scenarios are independent of the time-based valuation; they imply no tokens-per-second rate. Every constituent request is assumed to remain at or below 272,000 input tokens. Input is assumed to be 20% ordinary, 60% cached reads, and 20% cache writes in every scenario.

| Assumption | Low | Base | High |
|---|---:|---:|---:|
| Workers | 6 | 6 | 6 |
| Assumed request groups per worker | 2 | 16 | 48 |
| Aggregate input tokens per worker-request-group | 500,000 | 1,500,000 | 3,000,000 |
| Output tokens per worker-request-group, including reasoning | 100,000 | 300,000 | 600,000 |
| Separate conversations modeled | 15 | 15 | 15 |
| Aggregate input tokens per separate conversation | 200,000 | 1,000,000 | 4,000,000 |
| Aggregate output tokens per separate conversation, including reasoning | 50,000 | 250,000 | 1,000,000 |

The separate-chat rows price an assumed equivalent workload on Astra; they do not establish which models those chats actually used. Fifteen search-matched conversations anchor the scenario scope. Per-conversation token totals are assumed across all its requests; the search's 464 matching assistant messages and 28 matching user messages are not API-call counts. Additional conversations, if any, are outside this scenario. All prompts, repeated context, and tool-result text are included in assumed aggregate input. These token volumes are budgeting assumptions, not measured throughput.

### Result by work category within the project

| API-equivalent category | Low | Base | High |
|---|---:|---:|---:|
| Six-worker research | $90.60 | $2,174.40 | $13,046.40 |
| Separate related ChatGPT work | $52.80 | $264.00 | $1,056.00 |
| **Standard model-only subtotal** | **$143.40** | **$2,438.40** | **$14,102.40** |
| **Fast model-only subtotal, same tokens** | **$286.80** | **$4,876.80** | **$28,204.80** |

The assumed volume, caching, context lengths, and speed tier drive these results. There is no claim that the base scenario is statistically most likely. Further research branches should receive measured project tags rather than invented allocation percentages.

Tools and infrastructure are additional where applicable. For example, API web search is $0.01/call plus search-content tokens at model rates; container, file-search/storage, and third-party charges must be taken from their usage records. No parent/coordinator/orchestration model usage, tool, hosting, storage, tax, or currency-conversion amount is included above. The result is a worker-and-chat model-only subtotal, not a full-project cost. Native product tools are not automatically billed like API tools. [Official API tool pricing](https://developers.openai.com/api/docs/pricing)

## 3. Subscription allocation and actual cash

ChatGPT/Codex plan usage, purchased credits, and API-key billing are distinct. The official page currently lists Pro plans at $100, $200, and $500/month; the user's actual plan and payments have not been verified. Codex credit billing has no separate cache-write charge, unlike the API calculation above. [ChatGPT/Codex pricing](https://learn.chatgpt.com/docs/pricing)

For a subscription already purchased, included work can have zero additional per-message cash charge while consuming plan allowance. Purchased credits or API usage can add charges. A project allocation is an accounting choice: `actual subscription payment × project share`. A deliberately simple three-day allocation in a 31-day billing period is `S × 3/31`; it is not proof of active time or a new purchase. Use the actual invoice period and avoid allocating the same subscription twice across projects.

## Replace assumptions with measurements

1. Confirm the billing route and actual subscription/credit/API payments for the relevant period.
2. Obtain per-request model, speed tier, input tokens, cached-read tokens, cache-write tokens where applicable, and total billed output tokens. Include parent and worker requests, retries, and compaction without double counting aggregate reports.
3. Tag each request to its project and identify the separate ChatGPT work. Record tools/infrastructure independently.
4. For the requested time valuation, record each worker's actual active intervals. For cash accounting, reconcile usage to the invoice or credit ledger.

Reproducible arithmetic and assumptions are in [calculations.json](calculations.json); checked official source facts are in [sources.json](sources.json).
