# FFT and mathematical research

Research materials, experiments, certificates, and audits for the FFT/math project are indexed in [math/README.md](./math/README.md).


## Reviewed research updates

Earlier snapshots remain preserved. Each dated folder records its own proof scope, corrections and source provenance; independent checks do not establish historical novelty.

- [12:00 reviewed updates](./math/updates/2026-10-10-1200/)
- [12:20 finalized algebraic results](./math/updates/2026-10-10-1220/)
- [12:40 reviewed algorithms and bounds](./math/updates/2026-10-10-1240/)
- [13:00 representation and interface results](./math/updates/2026-10-10-1300/)
- [13:10 proof coverage and bounded N7 checkpoint](./math/updates/2026-10-10-1310/)

## Project cost estimate

Updated **2026-10-10**. All amounts are **USD**.

**Useful working numbers:** under the user's $60 per active Astra-worker-hour assumption, one half-hour with six active workers is **$180**. For exactly the hypothetical token workload below, the base model-only budget is **about $2,400 at Standard API rates or $4,900 at Fast rates**, excluding coordinator/orchestration work and tools. These are assumption-based valuations, not recorded charges. **Actual cash spend remains unknown.**

### Time valuation and the requested lower bound

| Assumed active time per worker | Six-worker time | Value at $60/worker-hour |
|---|---:|---:|
| 30 minutes | 3 worker-hours | $180 |
| 1 hour | 6 worker-hours | $360 |
| 8 hours | 48 worker-hours | $2,880 |
| 24 hours | 144 worker-hours | $8,640 |

The $60/hour rate comes from the user's valuation of $30 per active half-hour. It is not a verified OpenAI hourly tariff. If at least `H` active worker-hours are verified, `60 × H` is a conditional valuation lower bound. Wall-clock duration alone does not prove activity, six-way concurrency, token usage, or incremental cash spend.

The reviewed worker effort is `xhigh`. `xhigh` and `max` are reasoning-effort settings, not fixed dollar-per-minute prices. No strictly positive incremental-cash lower bound is established without a paid-usage record.

### Hypothetical API budget scenarios

These hypothetical worker-and-chat workloads use published `gpt-6-astra` prices. They do not claim that these ChatGPT/product sessions were API-billed.

| Assumption or result | Low | Base | High |
|---|---:|---:|---:|
| Total assumed worker input / output tokens, across all six workers | 6M / 1.2M | 144M / 28.8M | 864M / 172.8M |
| Separate conversations modeled | 15 | 15 | 15 |
| Aggregate input / output tokens per separate conversation | 0.2M / 0.05M | 1M / 0.25M | 4M / 1M |
| Six-worker research, Standard | $90.60 | $2,174.40 | $13,046.40 |
| Separate-chat equivalent, Standard | $52.80 | $264.00 | $1,056.00 |
| **Standard model-only subtotal** | **$143.40** | **$2,438.40** | **$14,102.40** |
| **Fast model-only subtotal** | **$286.80** | **$4,876.80** | **$28,204.80** |

Every token quantity is an assumption. The API scenarios have no assigned duration and are independent of the time valuation above. They are not estimates of likely historical usage or model throughput. A request group/conversation can contain multiple requests. Each request is assumed to stay at or below 272,000 input tokens. Input is modeled as 20% ordinary, 60% cached reads, and 20% cache writes; output includes all billed reasoning tokens. The low/high values are scenario outputs, not a confidence interval or measured spending range.

Standard prices per million tokens are $10 ordinary input, $1 cached input, $12.50 cache-write input, and $50 output. Fast doubles these rates. Longer-context requests have higher rates. [Official Astra pricing](https://developers.openai.com/api/docs/models/gpt-6-astra), checked 2026-10-10.

A bounded search found 15 related conversations and 492 distinct matching message IDs. These establish some project scope, not complete coverage or billed request counts. The roughly October 8–10 research window and archive sizes do not establish continuous activity or token usage. No cost is assigned to other projects.

### Cash and subscription accounting

Subscription allocation, time valuation, and API replacement cost are different accounting views. **Do not add them together.** Included subscription activity can have no additional per-message cash charge; purchased credits and API-key charges need separate records. Allocate the actual subscription invoice by an agreed project share. The user's plan, payments, and token totals have not been verified.

Codex credit billing has no separate cache-write charge; the cache-write term above applies only to the API scenario. [Official ChatGPT/Codex pricing](https://learn.chatgpt.com/docs/pricing).

Parent/coordinator/orchestration model usage, tools, infrastructure, storage, taxes, and any unobserved conversations are excluded. These model-only subtotals are not a complete project cost. To replace the assumptions, collect per-project model/tier and token-usage records, paid-credit/API charges, actual worker activity, and tool costs, then reconcile to invoices.

[Detailed assumptions and formulas](./math/project-cost/README.md) · [Calculation JSON](./math/project-cost/calculations.json) · [Checked sources](./math/project-cost/sources.json)
