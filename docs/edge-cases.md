# Edge Cases: AI-Powered Restaurant Recommendation System

This document lists detailed edge cases for the restaurant recommendation project defined in `docs/problemstatement.md`.  
Each edge case includes the scenario, risk, and expected system behavior.

## 1) Data Ingestion and Preparation Edge Cases

| ID | Edge Case | Risk/Impact | Expected Handling |
|---|---|---|---|
| D-01 | Dataset URL is unavailable or times out | Pipeline fails before startup | Retry with backoff, then fail gracefully with a clear error and fallback to last successful snapshot if available |
| D-02 | Dataset schema changes (column renamed/removed) | Feature extraction breaks silently | Enforce schema validation; block deployment if required fields are missing |
| D-03 | Duplicate restaurants with slight name differences | Duplicate recommendations | Apply deduplication rules using normalized name + location + cuisine |
| D-04 | Missing ratings for many records | Poor ranking quality | Keep records but tag missing rating; avoid hard filtering unless user sets strict minimum |
| D-05 | Invalid rating values (negative or greater than max scale) | Incorrect sorting and filtering | Clamp or discard invalid records during preprocessing; log data quality issue |
| D-06 | Cost field in mixed formats (numeric, ranges, text) | Budget filter errors | Standardize into a comparable numeric range and retain raw value for display |
| D-07 | Location stored with inconsistent spelling (Bengaluru vs Bangalore) | False no-match results | Use canonical location mapping and alias normalization |
| D-08 | Cuisine field contains multiple cuisines in one string | Incorrect cuisine matching | Tokenize cuisine values and support multi-label matching |
| D-09 | Non-English or special characters in restaurant names | Parsing/display issues | Preserve Unicode safely and sanitize only for matching logic |
| D-10 | Extremely small filtered dataset after cleanup | No useful recommendations | Trigger relaxed retrieval strategy with transparent messaging |

## 2) User Input and Validation Edge Cases

| ID | Edge Case | Risk/Impact | Expected Handling |
|---|---|---|---|
| U-01 | User submits empty input | System cannot infer preferences | Ask follow-up questions and default to popular nearby options |
| U-02 | Unknown location not present in dataset | Zero candidates | Suggest nearest supported locations or city alternatives |
| U-03 | Budget input outside accepted values | Bad filter state | Map synonyms to known buckets or reject with guidance |
| U-04 | Minimum rating exceeds dataset scale (for example 6/5) | Zero results always | Validate range and request correction |
| U-05 | Conflicting preferences (very low budget + premium cuisine + high rating) | Empty candidate set | Explain conflict and suggest relaxing one constraint |
| U-06 | Ambiguous cuisine terms ("veg", "healthy", "desi") | Weak retrieval precision | Use synonym/intent mapping and ask disambiguation question when confidence is low |
| U-07 | Input includes typos ("Banglore", "Itallian") | Missed matches | Apply fuzzy matching and confirm interpreted value |
| U-08 | User requests unsupported attributes (parking, pet-friendly) | Hallucinated recommendations | Mark as unsupported metadata and avoid claiming certainty |
| U-09 | User provides malicious prompt-like text in preferences | Prompt injection risk | Sanitize/escape raw input and isolate instructions from user text in prompt |
| U-10 | Very long free-text preference paragraph | Token overflow and noisy retrieval | Summarize intent with rule-based extraction before LLM call |

## 3) Candidate Generation and Retrieval Edge Cases

| ID | Edge Case | Risk/Impact | Expected Handling |
|---|---|---|---|
| C-01 | Hard filters return zero matches | Empty recommendation response | Use staged fallback: relax optional constraints first, then suggest nearest alternatives |
| C-02 | Too many matches (thousands) | Slow LLM inference and high cost | Pre-rank using deterministic scoring and pass only top-N to LLM |
| C-03 | Candidate list lacks diversity (same cuisine/chain) | Poor user experience | Apply diversity constraints (cuisine, price band, locality variety) |
| C-04 | Candidates from wrong city due to alias collision | Irrelevant results | Enforce strict city match after normalization |
| C-05 | Freshly added records have null critical fields | Bad explanations | Exclude incomplete records from LLM context or fill defaults safely |
| C-06 | Ranking favors high rating only and ignores budget fit | Misaligned recommendations | Use weighted candidate scoring aligned to user priorities |
| C-07 | Candidate pool too small for requested top-K | Repeated/low-quality output | Return fewer results with explicit note rather than padding with poor matches |
| C-08 | Same restaurant appears under multiple branches | Duplicate top recommendations | Group by brand + branch and avoid near-duplicate ranking neighbors |

## 4) Prompting, LLM Ranking, and Explanation Edge Cases

| ID | Edge Case | Risk/Impact | Expected Handling |
|---|---|---|---|
| L-01 | LLM returns restaurants not present in candidate input | Hallucinated entities | Strict post-validation against candidate IDs; drop invalid items |
| L-02 | LLM ignores user constraints and over-prioritizes generic popularity | Recommendation mismatch | Include explicit hard constraints in prompt and validate post-output |
| L-03 | LLM explanation fabricates unavailable facts (for example "has rooftop seating") | Trust and compliance issue | Limit explanations to available attributes and mark uncertain claims as unknown |
| L-04 | LLM output format is malformed JSON/text | Parsing failure | Use schema-constrained output or robust parser with retry prompt |
| L-05 | Token limit exceeded due to large context | Truncated/failed response | Compress candidate context and cap input size deterministically |
| L-06 | LLM latency spikes | Bad user-perceived performance | Add timeout + fallback deterministic ranking response |
| L-07 | API key quota exceeded/rate-limited | Service outage | Queue/retry with backoff, then fallback to non-LLM ranking |
| L-08 | Prompt injection from candidate data fields | Instruction override | Treat all dataset/user text as data and isolate system instructions |
| L-09 | Non-deterministic ranking across identical requests | Inconsistent UX | Use stable seeds/low temperature and deterministic tie-breakers |
| L-10 | Offensive/biased language in generated explanation | Reputation risk | Add moderation layer and safe-regeneration policy |

## 5) API, Output, and Presentation Edge Cases

| ID | Edge Case | Risk/Impact | Expected Handling |
|---|---|---|---|
| O-01 | API returns partial payload (missing cost or cuisine) | UI render breaks | Enforce response schema and default placeholders |
| O-02 | Client requests more results than available | Inconsistent pagination | Return actual count with `has_more=false` |
| O-03 | Same response cached across different users accidentally | Personalization leak | Cache by normalized preference hash, not global key |
| O-04 | Currency/unit mismatch in cost display | User confusion | Standardize display format and indicate currency clearly |
| O-05 | Explanation text too long for UI card | Layout overflow | Truncate with "read more" while preserving full details in expandable view |
| O-06 | User language preference differs from output language | Reduced usability | Provide localization option or simple translation layer |
| O-07 | Sorting displayed differently than backend rank | Trust issues | Send explicit rank order field and render as-is |
| O-08 | UI fails when recommendation list is empty | Broken journey | Show graceful empty-state guidance and suggested filter changes |

## 6) Monitoring, Feedback, and Iteration Edge Cases

| ID | Edge Case | Risk/Impact | Expected Handling |
|---|---|---|---|
| M-01 | Logs capture raw personal user text | Privacy/compliance concern | Redact/anonymize sensitive fields before storage |
| M-02 | Feedback rate is very low | Hard to evaluate quality | Use implicit signals (click-through, dwell time) alongside explicit ratings |
| M-03 | Feedback is skewed by small user segment | Biased optimization | Segment metrics by geography, cuisine preference, and budget band |
| M-04 | A/B test variants leak between users | Invalid experiment conclusions | Ensure stable user bucketing and strict experiment isolation |
| M-05 | Metrics improve but user satisfaction declines | Metric mismatch | Track both proxy metrics and direct satisfaction indicators |
| M-06 | Drift in dataset quality over time | Degraded recommendation relevance | Schedule periodic data quality audits and retraining/tuning cycles |
| M-07 | Silent failure in logging pipeline | No operational visibility | Add health checks and alerting for telemetry gaps |
| M-08 | Model/prompt update causes regression | Production instability | Add regression test suite and canary rollout with rollback support |

## 7) Cross-Cutting Security and Reliability Edge Cases

| ID | Edge Case | Risk/Impact | Expected Handling |
|---|---|---|---|
| X-01 | Prompt injection through user or dataset text | Unsafe/unreliable output | Use strict prompt boundaries and output validation |
| X-02 | Denial-of-service via high-frequency requests | Cost and latency spikes | Apply rate limiting, throttling, and circuit breakers |
| X-03 | Third-party dependency outage (dataset host or LLM API) | Service disruption | Use retries, fallback paths, and cached snapshots |
| X-04 | Inconsistent behavior between environments | Hard-to-debug failures | Maintain environment parity and config validation checks |
| X-05 | Unhandled exception in any phase | Full request failure | Use centralized exception handling and user-safe error responses |

## Suggested Test Suite Mapping

- **Unit Tests:** Field normalization, budget parsing, rating validation, schema checks
- **Integration Tests:** End-to-end flow from preferences to ranked output
- **Prompt/LLM Tests:** Schema conformance, hallucination rejection, constraint adherence
- **Load Tests:** High concurrency and latency resilience for retrieval + LLM calls
- **Regression Tests:** Stable ranking behavior for fixed benchmark queries

## Minimum Failure-Safe Rules

1. Never return hallucinated restaurants not present in filtered candidates.
2. Never fail silently; return actionable fallback guidance to users.
3. Never trust raw user text inside prompts without sanitization.
4. Always provide deterministic fallback ranking when LLM is unavailable.
5. Always log errors with enough context to debug, without exposing sensitive data.
