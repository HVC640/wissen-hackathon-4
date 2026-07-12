# Real-Time Portfolio Risk & Concentration Alert System - Build Plan

**Duration:** ~31 hours (Saturday 10 AM – Sunday 4 PM, July 11–12, 2026)  
**Team Size:** 3–4 members  
**Primary Tech:** Anthropic Claude API, Python/Node.js, minimal external dependencies

---

## 1. Project Overview

Build an AI-powered platform that:
- Ingests live/batch portfolio holdings (equities, bonds, derivatives, cash)
- Uses Claude to evaluate exposure against configurable concentration limits
- Classifies severity (LOW/MEDIUM/HIGH/CRITICAL) with confidence scores
- Generates human-readable rationale for every alert
- Automatically escalates to 2+ downstream actions (Slack, Jira, Dashboard)

**Scoring Weights:**
- AI Exposure Analysis & Rationale: **25%**
- Automation & Escalation: **20%**
- Risk Model Quality: **15%**
- Working Demo: **25%**
- API Efficiency: **10%**
- Docs/README: **5%**

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Portfolio Data Ingestion                      │
│  (CSV/JSON batch or real-time API feed with validation)         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│             Portfolio Data Normalization & Storage               │
│  (Parse, validate, enrich with sector/geography/correlation)    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│          Risk Configuration & Baseline Setup                     │
│  (Configurable limits: issuer %, sector %, geography %, etc.)   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│        Claude-Powered Concentration & Exposure Analysis          │
│  (Structured prompt: analyze holdings vs limits, identify        │
│   breaches, flag correlations, assess volatility context)       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│          Risk Severity Scoring & Classification                  │
│  (Claude output → LOW/MEDIUM/HIGH/CRITICAL + confidence)        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│        Automated Escalation & Notification Engine                │
│  (Trigger: Slack alerts, create Jira tickets, update dashboard) │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│           Audit Trail & Results Storage                          │
│  (Log all alerts, decisions, actions for compliance)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Components & Implementation Phases

### Phase 1: Foundation (Hours 0–6)
**Goals:** Data models, sample data, basic ingestion, configuration framework

#### 1.1 Data Models & Schema
**File:** `src/models/portfolio.py` (or `.ts`)
- `Portfolio` — Portfolio ID, fund name, type (Multi-Asset, Equity, Fixed Income, etc.), NAV
- `Position` — Ticker/ISIN, issuer, sector, geography, quantity, price, notional value, asset class
- `RiskLimit` — Limit type (single-issuer, sector, geography, asset-class), threshold %, escalation rules
- `ExposureMetric` — Calculated metric (% of NAV, correlation, volatility) and breach status
- `Alert` — Portfolio ID, severity, rationale, timestamp, actions triggered, confidence score

#### 1.2 Sample Data & Configuration
**Files:** `data/sample_portfolio.csv`, `config/risk_limits.json`
- Create 3–5 realistic portfolios with holdings (equities, bonds, cash) that include breaches
- Define configurable limits (e.g., single issuer max 8%, sector max 25%, geography max 70%)
- Mock historical volatility/correlation data for context enrichment

#### 1.3 Portfolio Data Ingestion
**File:** `src/ingestion/loader.py`
- Parse CSV/JSON portfolio files with validation
- Normalize ticker symbols, resolve issuer names, map sectors/geographies
- Calculate notional values, aggregate by sector/geography/issuer
- Return structured `Portfolio` object

---

### Phase 2: Risk Analysis Engine (Hours 6–16)
**Goals:** Claude integration, concentration analysis, severity scoring, rationale generation

#### 2.1 Claude API Integration & Prompt Design
**File:** `src/claude/analyzer.py`
- Initialize Anthropic client with team API key
- **Core prompt structure:**
  ```
  [PORTFOLIO DATA: holdings by issuer/sector/geography with NAV]
  [RISK LIMITS: configurable thresholds]
  [CONTEXT: 30-day volatility, correlation clusters, historical breach patterns]
  
  TASK: Analyze portfolio for concentration breaches. For each limit type:
  1. Current exposure vs limit
  2. Breach status (OK / WARNING / BREACH)
  3. Contributing factors
  4. Risk context (volatility spikes, correlated holdings)
  
  Output structured JSON with:
  - issuer_concentration (exposure %, limit %, breach_flag)
  - sector_concentration (exposure %, limit %, breach_flag)
  - geography_concentration (exposure %, limit %, breach_flag)
  - correlation_clusters (holdings > 0.85 rolling correlation)
  - breach_summary (list of all breaches)
  - context_analysis (volatility, historical patterns, urgency signals)
  ```

#### 2.2 Concentration & Exposure Analysis
**File:** `src/analysis/concentrations.py`
- Call Claude API with structured portfolio + limits + context
- Parse Claude's JSON response
- Validate outputs for completeness & logical consistency
- Enrich with edge case handling:
  - Multi-currency exposures (convert to base currency)
  - Derivative positions (notional exposure calculation)
  - Related-party linkages (e.g., parent-subsidiary correlation)

#### 2.3 Risk Severity Scoring
**File:** `src/scoring/severity.py`
- **Scoring logic:**
  - **CRITICAL:** Any breach by >2 pts + volatility spike (>30% QoQ) OR multiple correlated breaches (>3 holdings >0.85 correlation)
  - **HIGH:** Any single breach (1–2 pts) OR sector approaching limit (within 2 pts) + historical pattern match
  - **MEDIUM:** Sector/geography within 3 pts of limit OR single correlation cluster (2–3 holdings >0.80)
  - **LOW:** Sector/geography within 5 pts OR isolated low-correlation holding bump
- Calculate confidence score (0–100%) based on:
  - Data quality (completeness of holdings, correlation data)
  - Clarity of breach (unambiguous vs borderline)
  - Historical pattern match strength
- Generate rationale: "Breach severity: HIGH (single-issuer limit breached by 1.8 pts) + 40% volatility spike → immediate review recommended"

---

### Phase 3: Escalation & Notifications (Hours 16–24)
**Goals:** Automate alert distribution, audit trail, working demo prep

#### 3.1 Escalation Rules & Actions
**File:** `src/escalation/rules.py`
- **CRITICAL alerts:**
  - Immediate Slack message to `#portfolio-risk-alerts` with severity badge
  - Auto-create Jira ticket (RISK-xxx) with breach details, assigned to Risk Manager
  - PagerDuty/email escalation (if available; else log)
- **HIGH alerts:**
  - Slack notification to `#portfolio-risk-alerts`
  - Jira ticket creation, assigned to Portfolio Manager
  - Add entry to risk dashboard
- **MEDIUM/LOW alerts:**
  - Dashboard flag + audit-trail entry
  - Optional Slack summary (batch hourly)

#### 3.2 Notification Engine
**File:** `src/notifications/dispatcher.py`
- **Slack Integration:**
  - Use `slack_sdk` (Python) or `@slack/web-api` (Node.js)
  - Format message: Portfolio ID, Fund, Severity, Top 3 Exposures, Rationale, Est. Review Time
  - Include clickable link to dashboard/report
- **Jira Integration (if available):**
  - Create issue with severity labels, breach details, auto-assign
  - Link to portfolio ID for cross-reference
- **Dashboard Update:**
  - Write alert to in-memory store or lightweight DB (SQLite/JSON file for hackathon scope)
  - Timestamp, Portfolio, Severity, Rationale, Status (New/Acknowledged/Resolved)

#### 3.3 Audit Trail
**File:** `src/audit/logger.py`
- Log every alert: timestamp, portfolio ID, severity, rationale, Claude confidence, actions triggered, results
- Store in JSON file or simple DB
- Include: input holdings, calculated exposures, breach summary, escalation status

---

### Phase 4: Demo & Polish (Hours 24–31)
**Goals:** Working end-to-end demo, README, optimization, testing

#### 4.1 End-to-End Demo
**File:** `demo/run_demo.py` or `demo.js`
- Load 2–3 sample portfolios (one with CRITICAL breach, one with HIGH, one OK)
- Run through full pipeline: ingest → analyze → score → escalate → log
- Output:
  - Console log of each step with Claude reasoning
  - Alert summary table (Portfolio | Severity | Breach | Action)
  - Audit trail JSON
  - (Optional) Slack screenshots or dry-run confirmations

#### 4.2 API Efficiency & Token Cost
**File:** `src/claude/prompt_optimizer.py`
- **Token optimization:**
  - Use structured input format (JSON) to avoid verbose descriptions
  - Batch similar portfolios when possible to amortize context window
  - Cache risk limits + sector mappings across calls if Claude supports prompt caching
  - Estimate: ~800–1,200 tokens per portfolio analysis (input + output)
- **Prompt design principles:**
  - Be explicit about output format (JSON schema)
  - Avoid repetitive explanations; use templating
  - Request only necessary fields to reduce output verbosity

#### 4.3 README & Documentation
**File:** `README.md`
- **Sections:**
  1. Overview & Problem Statement
  2. Architecture Diagram
  3. Setup Instructions
     - Prerequisites (Python 3.10+, Node 18+)
     - Install dependencies
     - Set `ANTHROPIC_API_KEY` environment variable
  4. Configuration Guide
     - Edit `config/risk_limits.json` to adjust thresholds
     - Add/modify sample portfolios
  5. Running the Demo
     - `python demo/run_demo.py` or `node demo/demo.js`
     - Expected output walkthrough
  6. API Efficiency Details
     - Token counts per call
     - Optimization techniques used
  7. Future Enhancements
     - Real-time streaming, multi-fund aggregation, advanced ML correlation detection

#### 4.4 Code Quality & Testing
- **Unit tests** (if time): test data ingestion, severity scoring, notification logic
- **Type hints** (Python) or TypeScript for code clarity
- **Error handling:** graceful failures if Claude API is slow/unavailable; fallback severity (MEDIUM)

---

## 4. Technology Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | Python 3.10+ or Node.js 18+ | Quick iteration, libraries for data/API work |
| **Claude API** | `anthropic` SDK | Official, simplest integration |
| **Data Format** | CSV/JSON | Widely compatible, easy to mock |
| **Storage** | JSON files or SQLite | No external DB dependency for hackathon scope |
| **Notifications** | Slack SDK, print/file | Slack readily available; file-based fallback |
| **Demo** | CLI with colored output | Fast to build, runnable on any machine |

---

## 5. File Structure

```
wissen-hackathon-4/
├── README.md                          # Main documentation
├── plan.md                            # This file
├── requirements.txt (or package.json)
├── .env.example
│
├── src/
│   ├── models/
│   │   └── portfolio.py              # Data classes
│   ├── ingestion/
│   │   └── loader.py                 # CSV/JSON parsing & validation
│   ├── analysis/
│   │   ├── concentrations.py         # Exposure calculation
│   │   └── enrichment.py             # Add volatility, correlation context
│   ├── claude/
│   │   ├── analyzer.py               # Claude API calls & prompt
│   │   └── prompt_optimizer.py       # Token optimization
│   ├── scoring/
│   │   └── severity.py               # Severity classification logic
│   ├── escalation/
│   │   └── rules.py                  # Escalation decision rules
│   ├── notifications/
│   │   └── dispatcher.py             # Slack, Jira, dashboard updates
│   └── audit/
│       └── logger.py                 # Audit trail logging
│
├── config/
│   ├── risk_limits.json              # Configurable thresholds
│   └── sectors_mapping.json          # Sector/geography mappings
│
├── data/
│   ├── sample_portfolio_1.csv        # Multi-Asset with breaches
│   ├── sample_portfolio_2.csv        # Equity fund, near limits
│   └── sample_portfolio_3.csv        # Fixed Income, OK
│
├── demo/
│   └── run_demo.py                   # End-to-end demo script
│
├── output/
│   ├── alerts.json                   # Alert log (generated)
│   └── audit_trail.json              # Audit trail (generated)
│
└── tests/
    ├── test_ingestion.py
    ├── test_scoring.py
    └── test_notifications.py
```

---

## 6. Key Implementation Decisions

1. **Claude Usage Strategy**
   - Single structured prompt per portfolio (vs. multi-turn)
   - Request JSON output for easy parsing & escalation logic
   - Include context (volatility, correlation) in prompt to boost reasoning

2. **Risk Scoring**
   - Hybrid: Claude identifies exposures, hardcoded rules classify severity
   - Ensures repeatable, auditable scoring for compliance

3. **Escalation**
   - Severity-based routing (CRITICAL → immediate, HIGH → next business day, etc.)
   - At least 2 actions per alert (Slack + Jira minimum)

4. **Demo Scope**
   - Use local sample data; mock Slack/Jira if APIs unavailable
   - Focus on showing complete end-to-end flow with realistic output

5. **Token Efficiency**
   - Aim for <1,500 tokens per portfolio analysis (input + output)
   - Use structured JSON format to reduce verbosity
   - Batch similar portfolios if running multiple in one session

---

## 7. Success Criteria Checklist

- [ ] **Data Ingestion:** CSV/JSON parser + validation working
- [ ] **Claude Integration:** Structured prompts working, JSON output parsed
- [ ] **Concentration Analysis:** Accurate issuer/sector/geography calculations
- [ ] **Severity Scoring:** Produces LOW/MEDIUM/HIGH/CRITICAL with confidence >80%
- [ ] **Rationale Generation:** Clear, human-readable explanations for each verdict
- [ ] **Escalation:** 2+ actions triggered per alert (Slack + Jira/Dashboard)
- [ ] **Audit Trail:** Complete log of all alerts and actions
- [ ] **Working Demo:** End-to-end run with sample data, console output + files
- [ ] **API Efficiency:** Token usage <1,500/portfolio, prompt optimized
- [ ] **README:** Clear setup & run instructions, architecture diagram

---

## 8. Time Allocation (31 hours)

| Phase | Hours | Tasks |
|-------|-------|-------|
| Phase 1 (Foundation) | 6 | Data models, sample data, ingestion |
| Phase 2 (Risk Analysis) | 10 | Claude integration, concentration, scoring |
| Phase 3 (Escalation) | 8 | Notifications, audit, escalation logic |
| Phase 4 (Demo & Polish) | 7 | End-to-end demo, README, optimization, testing |

**Buffer:** 2–3 hours built in for debugging, API issues, testing.

---

## 9. Next Steps

1. **Kickoff:** Review this plan with team, assign roles
2. **Setup:** Create repo structure, initialize dependencies
3. **Phase 1:** Build data models & ingestion (6 hours)
4. **Phase 2:** Integrate Claude, implement scoring (10 hours)
5. **Phase 3:** Escalation & notifications (8 hours)
6. **Phase 4:** Demo, README, final polish (7 hours)
7. **Submit:** Final demo, code, documentation

---

**Owner:** Team Lead  
**Last Updated:** 2026-07-12  
**Status:** Ready for implementation
