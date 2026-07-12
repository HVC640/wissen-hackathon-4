# Quick Reference: Test Data Summary

## 📊 Portfolio Overview

| Portfolio ID | Fund Name | Type | NAV | Breaches | Key Test Case |
|---|---|---|---|---|---|
| PORT-2026-0001 | Alpha Growth Opportunities | Multi-Asset | $50M | RIL (9.8%) | High alerts, sector warnings |
| PORT-2026-0002 | Global Equity Diversified | Equity-Global | $75M | AAPL (8.0%) | Global diversification, moderate risk |
| PORT-2026-0003 | Fixed Income Portfolio | Bond-Conservative | $120M | GOI 10Y (30%) | CRITICAL breach testing |
| PORT-2026-0004 | Tech Sector Fund | Equity-Focused | $30M | NVDA (12%), Tech (61.5%) | Correlation clusters, volatility |
| PORT-2026-0005 | Emerging Markets Fund | Equity-EM | $60M | TENCENT (7.0%) | Geopolitical risk, high volatility |

## 🎯 Expected Alert Counts

- **CRITICAL:** 1 (GOI bonds concentration)
- **HIGH:** 5 (RIL, AAPL, NVDA, TENCENT, Semiconductors correlation)
- **MEDIUM:** 8 (sector warnings, correlations, volatility)
- **LOW:** 6 (normal conditions, diversification notes)

## 📈 Breach Examples by Type

### Single-Issuer Breaches
```
RIL:     9.8% vs 8.0% limit → 1.8 pt breach → HIGH
AAPL:    8.0% vs 7.0% limit → 1.0 pt breach → HIGH
NVDA:   12.0% vs 10.0% limit → 2.0 pt breach → HIGH
GOI 10Y: 30.0% vs 12.0% limit → 18.0 pt breach → CRITICAL
TENCENT: 7.0% vs 6.0% limit → 1.0 pt breach → HIGH
```

### Sector Breaches
```
Energy:      22.4% vs 25.0% → Warning (2.6 pts away)
Tech (Fund 4): 61.5% vs 60.0% → Marginal (1.5 pts over)
Government:  50.0% vs 40.0% → Breach (10 pts over)
```

### Correlation Flags
```
TCS-INFY:      0.88 vs 0.85 threshold → HIGH CLUSTER
MSFT-GOOGL:    0.78 vs 0.80 threshold → NEAR THRESHOLD
AMD-TSM:       0.85 vs 0.75 threshold → HIGH CLUSTER
Tencent-Alibaba: 0.68 vs 0.80 threshold → MODERATE
```

## 🚨 Severity Classification Guide

```
BREACH MAGNITUDE          SEVERITY
> 2.0 percentage points   CRITICAL
1.0 - 2.0 pts             HIGH
0.5 - 1.0 pts             MEDIUM
< 0.5 pts / Warning       LOW
```

## 📋 Files at a Glance

| File | Purpose | Format | Records |
|---|---|---|---|
| test_portfolios.json | Full portfolio data | JSON | 5 portfolios, 45 holdings |
| test_portfolios.csv | Holdings for import | CSV | 45 rows |
| test_risk_limits.json | Config & limits | JSON | 5 fund types, severity rules |
| test_expected_alerts.json | Validation data | JSON | 18 expected alerts |
| test_api_samples.json | API samples | JSON | 5 requests, 3 responses, 8 edge cases |
| TEST_DATA_README.md | Full documentation | Markdown | Comprehensive guide |

## 🔍 Key Test Scenarios

### Scenario 1: Basic Breach Detection
- **Portfolio:** PORT-2026-0001 (RIL)
- **Test:** Verify single-issuer breach at 1.8 pts
- **Expected:** HIGH alert with 91% confidence

### Scenario 2: Critical Multi-Breach
- **Portfolio:** PORT-2026-0003 (GOI bonds)
- **Test:** Verify CRITICAL severity on 18 pt breach
- **Expected:** Escalate to CFO/CRO, Jira blocker

### Scenario 3: Correlation Cluster
- **Portfolio:** PORT-2026-0004 (Semiconductors)
- **Test:** Detect 0.85 correlation breach
- **Expected:** HIGH alert on AMD-TSM cluster

### Scenario 4: Approaching Limits
- **Portfolio:** PORT-2026-0001 (Energy sector)
- **Test:** Flag 22.4% at 25% limit
- **Expected:** MEDIUM alert, no rebalancing yet

### Scenario 5: Geopolitical Risk
- **Portfolio:** PORT-2026-0005 (Tencent)
- **Test:** Single breach + elevated volatility + geopolitical factors
- **Expected:** HIGH alert with context

## 💡 Important Data Points

**Volatility Ranges:**
- Conservative: 0.0-0.25 (bonds, cash, large-cap)
- Moderate: 0.25-0.40 (diversified equity)
- High: 0.40-0.60 (sector stocks, EM equities)
- Critical: >0.60 (GAZPROM 0.68 - geopolitical)

**Confidence Scores (Expected):**
- CRITICAL alerts: 85-99%
- HIGH alerts: 80-92%
- MEDIUM alerts: 70-90%
- LOW alerts: 60-75%

**Fund Types & Limits:**
```
Multi-Asset:         Single 8%, Sector 25%, Geo 70%
Global Equity:       Single 7%, Sector 20%, Geo 40%
Bond-Conservative:   Single 12%, Sector 40%, Geo 60%
Equity-Focused:      Single 10%, Sector 60%, Geo 50%
Equity-EM:           Single 6%, Sector 22%, Geo 35%
```

## 🔗 Data Relationships

```
test_portfolios.json
    ├─ Holdings → test_risk_limits.json (fund type → limits)
    ├─ Analysis output → test_expected_alerts.json (compare results)
    └─ API call → test_api_samples.json (request structure)

test_portfolios.csv
    └─ Normalized view of test_portfolios.json for bulk import
```

## 🛠️ Quick Integration Steps

1. **Load portfolios:**
   ```bash
   curl -X POST /api/portfolio/batch-analyze \
     -d @test_api_samples.json
   ```

2. **Validate alerts:**
   ```python
   actual = system.analyze(portfolio)
   expected = load_json('test_expected_alerts.json')
   assert matches(actual, expected)
   ```

3. **Check severity:**
   ```python
   assert actual['severity'] == expected['severity']
   assert actual['confidence'] >= expected['confidence'] - 5
   ```

4. **Test escalation:**
   ```python
   assert action['slack_channel'] in ['#portfolio-risk-critical', '#portfolio-risk-alerts']
   assert jira_ticket.priority == expected_priority
   ```

## 📊 Distribution Summary

**By Geography:**
- India: 8 holdings
- USA: 13 holdings  
- Europe: 4 holdings
- Emerging Markets: 14 holdings
- Global: 6 holdings

**By Asset Class:**
- Equities: 35 positions
- Bonds: 9 positions
- Cash: 5 positions

**By Sector:**
- Technology: 12 positions
- Government: 4 positions
- Energy: 5 positions
- Financials: 4 positions
- Other: 15 positions

## ⚡ Performance Baseline

Expected metrics from test runs:
- **Analysis time:** ~3-5 seconds per portfolio
- **Token usage:** 1,200-1,500 tokens per analysis
- **Confidence score:** 80-95% (average 87%)
- **Alert latency:** <100ms after Claude response

## 🎓 Learning Points

These portfolios were designed to test:
1. ✅ Breach detection at various magnitude levels
2. ✅ Severity classification logic
3. ✅ Correlation cluster identification
4. ✅ Multi-asset diversification handling
5. ✅ Geopolitical/volatility context
6. ✅ Escalation rule triggers
7. ✅ Rationale generation quality
8. ✅ API efficiency & token management

---

**Generated:** 2026-07-11  
**Format Version:** 1.0  
**Total Test Cases:** 18 explicit + 8 edge cases
