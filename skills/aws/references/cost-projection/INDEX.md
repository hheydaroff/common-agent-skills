> **Domain: cost-projection** — local skill `aws-cost-projection` (not from the AWS pack).
> Paths in this file are relative to the `aws` skill root.

# AWS Cost Projection & Analysis

## When to Use
- Contract renegotiation with AWS resellers requiring spend forecasts
- Budget planning for next fiscal year based on historical usage
- Multi-account cost consolidation (dev/stage/prod per application)
- Growth rate estimation for token-based or usage-based AWS services
- Comparing scenarios (conservative/base/aggressive) for commitment levels

## Architecture

```
project/
├── collect_<service>_costs.py   # Per-account collector (interactive)
├── consolidate_analysis.py      # Merges all accounts → report
├── data/                        # Raw per-account JSON outputs
└── output/                      # Final reports (MD + JSON)
```

## Steps

### 1. Create the Collector Script
- Uses `boto3` with credentials from environment (no hardcoded keys)
- Interactive prompts for account alias + region
- Collects from multiple AWS APIs:
  - **Cost Explorer** (us-east-1) — monthly costs by usage type
  - **CloudWatch** — service-specific metrics (tokens, invocations, etc.)
  - **Service APIs** — inventory of resources (agents, KBs, etc.)
- Saves structured JSON to `./data/<alias>_usage.json`

### 2. Create the Consolidation Script
- Loads all JSON files from `./data/`
- Aggregates: monthly trends, per-account breakdown, per-model costs
- Calculates growth rates:
  - MoM (month-over-month)
  - QoQ (quarter-over-quarter)
  - Recent 3-month trend (most relevant for projection)
- Projects 4 scenarios (see Projection Methodology below)
- Outputs markdown report + JSON data

### 3. User Workflow
```bash
# Per account (repeat for each):
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
export AWS_DEFAULT_REGION=eu-central-1
uv run --with boto3 python3 collect_<service>_costs.py

# After all accounts collected:
uv run --with boto3,tabulate python3 consolidate_analysis.py
```

## Key Design Decisions

1. **No stored credentials** — user exports per-account in terminal
2. **uv run --with** — no venv setup needed, deps are transient
3. **12-month lookback** — enough data for trend without ancient noise
4. **Growth floor rates** — prevents projections from going to zero if recent months are flat
5. **Outlier filtering** — >500% MoM excluded from averages (ramp-up months)
6. **Daily CloudWatch resolution** — aggregated to monthly in consolidation for flexibility

## Gotchas & Lessons

- Cost Explorer API is **only available in us-east-1** regardless of resource region
- CloudWatch Bedrock metrics require the **exact model ID** including version suffix
- Cross-region inference model IDs have prefixes: `us.anthropic.`, `eu.anthropic.`
- New accounts may not have Cost Explorer data enabled (takes 24h)
- Provisioned throughput shows in Cost Explorer as separate line items
- Token metrics in CloudWatch may be missing if invocation logging isn't enabled
- `tabulate` package is optional — script includes fallback formatter

### CRITICAL: Anthropic Claude Billing is NOT Under "Amazon Bedrock"

**Anthropic Claude models on Bedrock are billed as separate AWS Marketplace services.**
Filtering Cost Explorer by `SERVICE = "Amazon Bedrock"` only returns AWS-native models
(Titan, Nova, etc.). Claude costs appear under separate service names:

- `"Claude (Amazon Bedrock Edition)"`
- `"Claude 3 Haiku (Amazon Bedrock Edition)"`
- `"Claude 3.5 Sonnet (Amazon Bedrock Edition)"`
- `"Claude 3.5 Sonnet v2 (Amazon Bedrock Edition)"`
- `"Claude Sonnet 4 (Amazon Bedrock Edition)"`
- `"Claude Opus 4 (Amazon Bedrock Edition)"`
- etc.

**Fix:** First query Cost Explorer grouped by SERVICE (no filter) to discover all services,
then query each Claude/AI service individually. Always include a discovery step.

This also means:
- AWS Cost Anomaly Detection does NOT monitor Marketplace charges by default
- Claude costs won't appear in Bedrock-filtered billing dashboards
- Need to query both `"Amazon Bedrock"` AND each `"Claude X (Amazon Bedrock Edition)"` service

## Projection Methodology (Lessons Learned)

Naive compound growth from MoM averages is **misleading** for AWS AI costs because:
- Ramp-up months inflate averages (99%+ MoM during initial deployment)
- One-time data processing spikes create false peaks
- Model migrations are cost-neutral but look like growth
- Recent decline after a spike looks like negative growth

**Use component-based projection instead of single-rate compound growth:**

### Why Single-Rate Fails
- Ramp-up months inflate averages (99%+ MoM during initial deployment)
- One-time spikes (data processing, RAG ingestion) create false peaks
- Cost optimizations (caching) look like decline but are permanent reductions
- Model migrations are cost-neutral but look like growth
- Recent decline after a spike looks like negative growth

### Component-Based Projection (Recommended)

Model each product/workload **separately** with its own growth rate:

```
| Component          | Baseline | Growth Rate | Driver                     |
|--------------------|----------|-------------|----------------------------|
| Stable product     | $X/mo    | 2-5%/mo     | Organic (more users/data)  |
| Growing product    | $Y/mo    | 15-25%/mo   | User adoption curve        |
| Dev tools / R&D    | $Z/mo    | 5-15%/mo    | Team size                  |
| New services       | $0       | Step + 15%  | Launch date + adoption     |
```

This captures reality: stable products don't compound, growth products do.

### Scenario Framework

| Scenario | Method | When It's Right |
|----------|--------|----------------|
| **Conservative** | Each component at low growth | No new use cases planned |
| **Base Case** | Per-component realistic growth | Normal business development |
| **Aggressive** | High growth + multiple new services | Org-wide AI push |

### Key Analysis Patterns
- **Group accounts by application** (not individual accounts) to see business-level trends
- **Identify permanent cost changes** (caching, model switches) vs temporary spikes
- **Dev/experiment accounts are leading indicators** — what's there today ships to prod in 3-6mo
- **User-facing products dominate long-term** — even starting small, 20%/mo compound overtakes everything
- **40:1 input/output token ratio** → RAG workloads (large context, short answers)
- Track model migration events (cost-neutral transitions that confuse trend analysis)

### Contract Negotiation Formula
Given trailing 12-month spend X and base-case projection Y:
- Commit at Y (e.g., $260K for $82K trailing when growth is strong)
- Tier discounts at Y, 1.3×Y, 2×Y
- Quarterly true-up option (adjust after Q1 actuals)
- **Always confirm commitment covers ALL marketplace services** (Claude billed separately!)
- Negotiate pay-as-you-go above commitment at discounted rate (not list price)

## Adapting for Other Services

Replace the service-specific parts:
- Model IDs → resource identifiers for the target service
- CloudWatch namespace (`AWS/Bedrock`) → service namespace
- Pricing table → current pricing for the target service
- Service inventory calls → relevant list/describe APIs

## Report Sections
1. Account Overview (IDs, regions, total spend)
2. Monthly Cost Trend (with per-account breakdown)
3. Usage Type Breakdown (from Cost Explorer categories)
4. Model/Resource-Level Usage (from CloudWatch metrics)
5. Service Inventory (agents, KBs, guardrails, etc.)
6. Growth Rate Analysis (MoM, QoQ, recent trend)
7. Cost Projections (3 scenarios × monthly detail)
8. Contract Negotiation Recommendations (commitment levels, optimization levers)
