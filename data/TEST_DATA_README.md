# Test Data for Portfolio Risk & Concentration Alert System

This directory contains comprehensive test data for the Wissen Technology Hackathon 2026 - Real-Time Portfolio Risk & Concentration Alert System.

## Overview

The test data is organized into multiple files to support different testing scenarios:
- **Portfolio holdings data** (JSON and CSV formats)
- **Risk limits and configurations**
- **Expected alert scenarios**
- **API request/response samples**

## Files

### 1. `test_portfolios.json`
Main portfolio data file containing 5 diverse portfolios with different risk profiles.

**Structure:**
```json
{
  "portfolios": [
    {
      "portfolio_id": "PORT-2026-0001",
      "fund_name": "Alpha Growth Opportunities Fund",
      "fund_type": "Multi-Asset - Long Only",
      "submitted_date": "2026-07-11T09:15:32Z",
      "nav_value": 50000000,
      "risk_limits": { ... },
      "holdings": [ ... ]
    }
  ]
}
```

**Portfolios Included:**

#### Portfolio 1: Alpha Growth Opportunities Fund (PORT-2026-0001)
- **Type:** Multi-Asset - Long Only
- **NAV:** $50M
- **Holdings:** 9 positions (equities, bonds, cash)
- **Key Features:**
  - Single-issuer breach: Reliance Industries (9.8% vs 8.0% limit)
  - Sector warning: Energy at 22.4% (approaching 25% limit)
  - High correlation cluster: TCS-INFY (0.88 correlation)
  - All India geography

**Expected Alerts:**
- HIGH: Single-issuer breach on Reliance
- MEDIUM: Energy sector approaching limit
- MEDIUM: Correlation flag on TCS-INFY

---

#### Portfolio 2: Global Equity Diversified Fund (PORT-2026-0002)
- **Type:** Equity - Global
- **NAV:** $75M
- **Holdings:** 9 positions across US, Europe, Asia
- **Key Features:**
  - Single-issuer breach: Apple (8.0% vs 7.0% limit)
  - Good geographic diversification
  - Technology sector concentrated
  - Moderate correlation in tech holdings

**Expected Alerts:**
- HIGH: Single-issuer breach on Apple
- LOW: Technology sector near limit but acceptable
- LOW: Tech correlation within acceptable range

---

#### Portfolio 3: Fixed Income Portfolio (PORT-2026-0003)
- **Type:** Bond - Conservative
- **NAV:** $120M
- **Holdings:** 7 bond positions + cash
- **Key Features:**
  - **CRITICAL:** Government of India 10Y bond (30.0% vs 12.0% limit) - SEVERE BREACH
  - Government sector concentration (50.0% vs 40.0% limit)
  - Conservative volatility profile
  - Excellent for testing edge cases and critical severity

**Expected Alerts:**
- CRITICAL: Government bond concentration (18 pts breach)
- HIGH: Single issuer breach on India sovereign
- LOW: Low portfolio volatility (positive)

---

#### Portfolio 4: Sector-Concentrated Tech Fund (PORT-2026-0004)
- **Type:** Equity - Sector Focused
- **NAV:** $30M
- **Holdings:** 9 positions, heavily tech-weighted
- **Key Features:**
  - Single-issuer breach: NVIDIA (12.0% vs 10.0% limit)
  - Sector concentration: Tech at 61.5% (exceeds 60% limit)
  - High volatility (AMD 52%, GAZPROM 68%)
  - High correlation cluster: AMD-TSM (0.85)

**Expected Alerts:**
- HIGH: NVIDIA single-issuer breach
- MEDIUM: Tech sector slightly over limit
- HIGH: Semiconductor correlation cluster
- MEDIUM: Elevated volatility warning

---

#### Portfolio 5: Emerging Markets Growth Fund (PORT-2026-0005)
- **Type:** Equity - Emerging Markets
- **NAV:** $60M
- **Holdings:** 10 positions across multiple emerging markets
- **Key Features:**
  - Single-issuer breach: Tencent (7.0% vs 6.0% limit)
  - China concentration: 18.5%
  - Geopolitical risk exposure
  - Moderate correlation cluster in China tech

**Expected Alerts:**
- HIGH: Tencent single-issuer breach
- MEDIUM: China sector concentration
- MEDIUM: Elevated volatility (Gazprom 68%)
- LOW: Moderate correlation in China holdings

---

### 2. `test_portfolios.csv`
CSV format of all portfolio holdings for easy import into databases or data pipelines.

**Columns:**
```
portfolio_id, fund_name, fund_type, submitted_date, nav_value, symbol, issuer, 
asset_class, sector, geography, position_value, percentage_nav, volatility_30day
```

**Usage:**
- Import into databases for batch processing
- Use for CSV file upload testing
- Data validation testing

---

### 3. `test_risk_limits.json`
Configuration file defining risk limits and alert severity thresholds.

**Structure:**

```json
{
  "risk_limits_by_fund_type": { ... },
  "sector_definitions": [ ... ],
  "geography_regions": [ ... ],
  "alert_severity_thresholds": { ... },
  "escalation_rules": { ... }
}
```

**Severity Levels:**

| Severity | Breach Magnitude | Confidence | Actions |
|----------|-----------------|-----------|---------|
| CRITICAL | > 2.0 pts | >= 85% | Immediate escalation to CFO/CRO |
| HIGH | 1.0-2.0 pts | >= 80% | Risk Desk escalation |
| MEDIUM | 0.5-1.0 pts | >= 70% | Monitoring & warnings |
| LOW | < 0.5 pts | >= 60% | Log & track |

**Escalation Actions:**

- **CRITICAL:** Jira blocker, Slack #portfolio-risk-critical, CFO/CRO email, Dashboard flag
- **HIGH:** Jira high priority, Slack #portfolio-risk-alerts, CRO notification
- **MEDIUM:** Jira medium, Slack #portfolio-monitoring, Dashboard update
- **LOW:** Logging only

---

### 4. `test_expected_alerts.json`
Expected alert outputs for each portfolio to validate Claude's analysis.

**Structure:**
```json
{
  "expected_alerts": [
    {
      "portfolio_id": "PORT-2026-0001",
      "expected_alerts": [
        {
          "alert_type": "SINGLE_ISSUER_BREACH",
          "severity": "HIGH",
          "confidence": 91,
          "rationale_keywords": [ ... ]
        }
      ]
    }
  ],
  "test_scenarios": [ ... ]
}
```

**Use Cases:**
- Validate Claude's alert generation
- Test alert severity classification
- Verify rationale generation quality
- Compare against expected confidence scores

---

### 5. `test_api_samples.json`
Sample API requests and responses for integration testing.

**Includes:**

**Request Samples:**
1. `POST /api/portfolio/analyze` - Single portfolio analysis
2. `POST /api/portfolio/batch-analyze` - Batch analysis
3. `POST /api/exposure/concentration` - Concentration metrics
4. `GET /api/alerts/list` - Alert retrieval
5. `POST /api/correlation/cluster-analysis` - Correlation analysis

**Response Samples:**
- Full response body examples
- Expected HTTP status codes
- Timestamp and token usage info
- Automated action execution records

**Edge Cases:**
- Positions at exact limit
- Empty portfolios
- Unaccounted value
- High cash positions
- Negative correlations
- Perfect correlations (1.0)
- Overlapping geographies

---

## Test Scenarios

### Scenario 1: Breach Detection
**Portfolio:** PORT-2026-0001  
**Expected:** HIGH alert on Reliance Industries  
**Test:** Verify Claude correctly identifies 9.8% > 8.0% breach

### Scenario 2: Multi-Breach Escalation
**Portfolio:** PORT-2026-0003  
**Expected:** CRITICAL alert on Government bonds  
**Test:** Verify system escalates multiple breaches to CRITICAL

### Scenario 3: Correlation Analysis
**Portfolio:** PORT-2026-0004  
**Expected:** HIGH alert on semiconductor correlation  
**Test:** Verify Claude identifies 0.85+ correlations

### Scenario 4: Volatility Warnings
**Portfolio:** PORT-2026-0005  
**Expected:** MEDIUM alert on volatility  
**Test:** Verify thresholds are applied correctly

### Scenario 5: Global Diversification
**Portfolio:** PORT-2026-0002  
**Expected:** LOW alerts despite breach  
**Test:** Verify diversification context factors into severity

---

## Usage Guide

### 1. Load Portfolio Data
```json
# Load from test_portfolios.json
POST /api/portfolio/batch-analyze
{
  "portfolios": ["PORT-2026-0001", "PORT-2026-0002", "PORT-2026-0003", ...]
}
```

### 2. Validate Against Expected Alerts
```
For each portfolio_id:
  - Load portfolio from test_portfolios.json
  - Load expected alerts from test_expected_alerts.json
  - Run analysis
  - Compare severity, confidence, and rationale
```

### 3. Test API Endpoints
```
Use request samples from test_api_samples.json
- Verify response structure
- Validate status codes
- Check timestamp format
- Monitor token usage
```

### 4. Edge Case Testing
```
Run edge_case_test_data scenarios
- Exact limit positions
- Empty portfolios
- Perfect/negative correlations
- Overlapping classifications
```

---

## Key Metrics for Validation

### Breach Detection Accuracy
- Single-issuer: 5 expected breaches (RIL, AAPL, NVDA, GOI, TENCENT)
- Sector: 4 expected breaches/warnings (Energy, Tech, Government, Energy)
- Geography: 1 expected breach (India in FI portfolio)

### Correlation Analysis
- TCS-INFY: 0.88 (HIGH cluster)
- MSFT-GOOGL: 0.78 (near threshold)
- AMD-TSM: 0.85 (HIGH cluster)
- Tencent-Alibaba: 0.68 (moderate cluster)

### Volatility Ranges
- Low: 0.0-0.20 (bonds, cash)
- Moderate: 0.20-0.40 (diversified equities)
- High: 0.40-0.60 (sector stocks, EM)
- Critical: > 0.60 (GAZPROM 0.68)

### Alert Distribution
- CRITICAL: 1 alert (Government bonds)
- HIGH: 5 alerts (RIL, AAPL, NVDA, TENCENT, correlation)
- MEDIUM: 8 alerts (sector, correlation, volatility)
- LOW: 6 alerts (normal conditions, diversification)

---

## Data Quality Notes

### Asset Classes
- **Equity:** Individual stocks
- **Bond:** Government and corporate bonds
- **Cash:** Cash equivalents and reserves

### Sectors
- Technology, Energy, Financials, Telecom, Consumer Staples, Automobiles, Infrastructure, E-commerce, Government

### Geographies
- Americas: USA, Brazil
- Europe: Germany, Switzerland, Netherlands, UK
- Asia-Pacific: India, China, Taiwan, Israel, South Korea
- Russia (emerging market risk factor)

### Volatility Data
- Real 30-day realized volatility
- Ranges from 0.0 (cash) to 0.68 (GAZPROM - geopolitical risk)
- Used to contextualize breach severity

### Correlation Data
- Rolling 30-day Pearson correlation
- Values between -1.0 and 1.0
- Threshold varies by fund type (0.75-0.85)

---

## Testing Best Practices

1. **Validate Systematically**
   - Test each portfolio independently
   - Cross-reference with expected_alerts.json
   - Verify confidence scores align

2. **Check Context**
   - Volatility context for single-issuer breaches
   - Historical patterns (previous Q1 breaches)
   - Geopolitical/market context

3. **Test Edge Cases**
   - Positions at exact limits
   - Overlapping classifications
   - Extreme values (perfect correlation, zero volatility)

4. **Monitor API Efficiency**
   - Track token usage per analysis
   - Verify batch processing efficiency
   - Check response times

5. **Validate Escalation**
   - Verify correct Slack channels
   - Check Jira ticket creation
   - Confirm email notifications

---

## Integration with Claude API

Each alert generation should use Claude with:
- **Model:** Claude Opus 4.8 (recommended for financial analysis)
- **Temperature:** 0.7 (balance precision and natural language)
- **Context:** Portfolio data + risk limits + historical patterns
- **Output:** Structured alert with rationale

**Sample Prompt Structure:**
```
You are a portfolio risk analyst. Analyze the following portfolio:
[Portfolio data]

Against these limits:
[Risk limits]

Generate alerts for:
1. Single-issuer concentrations
2. Sector concentrations
3. Geography concentrations
4. Correlation clusters
5. Volatility concerns

For each alert, provide:
- Severity (LOW/MEDIUM/HIGH/CRITICAL)
- Confidence score (0-100)
- Clear rationale with specific numbers
```

---

## Maintenance & Updates

- **Update Volatility:** Monthly with real market data
- **Update Correlations:** Weekly rolling 30-day calculations
- **Add Scenarios:** Include new breach patterns as discovered
- **Refresh Limits:** Update per fund policy changes

---

## Questions & Support

For issues with test data:
1. Check data format consistency
2. Verify date ranges (all timestamps are 2026-07-11)
3. Confirm NAV values match position sum
4. Validate percentage calculations
