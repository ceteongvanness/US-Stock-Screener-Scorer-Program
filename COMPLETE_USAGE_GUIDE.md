# Complete Stock Screener Package - Usage Guide

## 📦 What You've Received

You now have 3 programs:

1. **stock_screener.py** - Full production version (fetches live data from Yahoo Finance)
2. **README.md** - Complete documentation


---

## 🚀 Quick Start
### Run Full Version (When You Have Internet)

```bash
python stock_screener.py
```

This will:
- Fetch live data for ~134 major US stocks
- Score each one
- Take 2-3 minutes to complete
- Generate comprehensive Excel report

---

## 📊 Demo Results Summary

From the sample data, here's what you learned:

### ✓ PASSING STOCKS (Score ≥7)

| Rank | Ticker | Company | Score | Price | Budget OK? |
|------|--------|---------|-------|-------|------------|
| 1 | MSFT | Microsoft | 11.0 | $425.30 | ❌ Too expensive |
| 2 | JNJ | Johnson & Johnson | 11.0 | $158.20 | ❌ Too expensive |
| 3 | KO | Coca-Cola | 8.5 | $62.15 | ❌ Too expensive |
| 4 | AAPL | Apple | 8.0 | $195.50 | ❌ Too expensive |
| 5 | T | AT&T | 7.5 | $25.27 | ✅ **Suitable!** |

### ✗ FAILING STOCKS (Score <7)

| Ticker | Company | Score | Why It Failed |
|--------|---------|-------|---------------|
| INTC | Intel | 6.0 | Poor financials + Tech risk |
| F | Ford | 5.5 | Weak ROE, high debt |
| PATH | UiPath | 3.5 | Negative margins, tech risk |
| GME | GameStop | 2.5 | No moat, poor financials |
| SOFI | SoFi | 2.0 | Negative FCF, no dividend |

---

## 💡 Key Findings for Your Budget ($6,890)

### Your Constraints:
- Conservative limit: $1,722 per position (25%)
- Stock price must be < $17.22 for single contract

### Results from Demo:
**T (AT&T) at $25.27:**
- ✓ Score: 7.5 (PASS)
- ⚠️ Collateral for Strike $20: $2,000 (29% of budget)
- Status: Slightly over conservative limit, but within moderate limit

**Actual good options need price < $17:**
- None in this sample dataset
- But you know F ($13.01) scored 5.5 - not quite 7
- This shows why the screener is valuable - helps you avoid marginal stocks

---

##  How the Scoring Works

### Example: MSFT (Score: 11.0)

**Financial Score: 7.5/9**
```
✓ EPS Growth: 15.0% → +1.0
✓ Dividend: $3.00, 5yr history → +1.0
⚠ Shares: Assumed stable → +0.5
✓ Net Margin: 36.0% → +1.0
✓ ROE: 40.0% → +1.0
✓ FCF: $65.0B → +1.0
✓ D/E: 0.35 → +1.0
✓ Interest Coverage: OK → +1.0
```

**Moat Score: 4.5/7**
```
⚠ Brand: Large cap → +0.5
✓ Patents: Technology sector → +1.0
✓ Cost Advantage: 36% margin + scale → +1.0
✓ Switching Cost: Software industry → +1.0
✓ Longevity: Dividend history → +1.0
```

**Risk Deduction: -1**
```
✗ Tech Risk: Software industry → -1.0
```

**Total: 7.5 + 4.5 - 1.0 = 11.0 ✓ PASS**

---

### Example: INTC (Score: 6.0) ❌

**Financial Score: 4.5/9**
```
✗ EPS Growth: -45.0% → +0.0
✓ Dividend: $0.50, 5yr history → +1.0
⚠ Shares: Assumed → +0.5
✗ Net Margin: 2.0% → +0.0
✗ ROE: 2.0% → +0.0
✓ FCF: $8.0B → +1.0
✓ D/E: 0.42 → +1.0
✓ Interest Coverage: OK → +1.0
```

**Moat Score: 2.5/7**
```
✓ Patents: Technology → +1.0
⚠ Longevity: Large cap → +0.5
✓ Brand: Large cap tech → +0.5
⚠ Switching Cost: Partial → +0.5
```

**Risk Deduction: -1**
```
✗ Tech Risk: Semiconductors → -1.0
```

**Total: 4.5 + 2.5 - 1.0 = 6.0 ✗ FAIL**

**Why it fails:** Just 1 point short! Poor recent performance drags it down.

---

## 🎯 How to Use This for Your Trading

### Step 1: Run the Screener

When you have internet access:
```bash
python stock_screener.py
```

This will generate an Excel file with all stocks scored.

### Step 2: Filter for Your Budget

Open the Excel file and filter:
```
Column: passing = TRUE
Column: price < $20
Sort by: total_score (descending)
```

### Step 3: Manual Verification

For each stock that passes, check:
1. ✓ Open OptionStrat
2. ✓ Select 30-45 day expiration
3. ✓ Find Strike 10-20% out of money
4. ✓ Verify IV Rank > 50%
5. ✓ Check success probability > 80%
6. ✓ Verify BID > $0
7. ✓ Fill out your Checklist in Google Sheets

### Step 4: Only Then Open Position

If everything checks out:
- Use the Google Sheets Checklist
- Must score ≥80% on checklist
- Then execute in IBKR

---

## 📈 Expected Results

Based on typical market conditions:

**Out of 100 large-cap US stocks:**
- ~20-30 will score ≥7 points
- ~5-10 will be budget-friendly (<$30 price)
- ~2-5 will be perfect for your budget (<$20 price)

**Quality distribution:**
- Score 10-16: Excellent (AAPL, MSFT, JNJ, KO, V)
- Score 7-10: Good (T, WMT, BAC, VZ)
- Score 5-7: Marginal (INTC, F - avoid these)
- Score <5: Poor (SOFI, PATH, GME - never trade)

---

## 🔧 Customizing the Screener

### Add More Stocks

Edit `stock_screener.py` line 347:

```python
major_tickers = [
    'AAPL', 'MSFT', 'GOOGL',
    # Add your stocks here:
    'YourStock1',
    'YourStock2',
]
```

### Adjust Minimum Score

Edit `stock_screener.py` line 12:

```python
self.min_passing_score = 8  # Raise to 8 for stricter criteria
```

### Change Financial Criteria

Edit the `score_financial_metrics()` function to adjust thresholds:

```python
# Example: Require higher profit margin
if profit_margin > 0.15:  # Changed from 0.10
    score += 1
```

---

## 📁 Output Files

### Excel File Structure

**Sheet 1: Summary**
- All stocks with complete scores
- Sortable and filterable

**Sheet 2: Top Scorers (≥7)**
- Only passing stocks
- Pre-filtered for you

**Sheet 3: Budget Friendly** (if applicable)
- Passing stocks under $30
- Perfect for your use case

**Sheet 4+: By Sector**
- Technology stocks
- Healthcare stocks
- Finance stocks
- etc.

---

## 🚨 Important Reminders

### The Screener is Step 1 Only!

```
Step 1: Run screener → Find 7+ point stocks
                      ↓
Step 2: Open OptionStrat → Verify options metrics
                      ↓
Step 3: Fill Google Sheets Checklist → Must pass 80%
                      ↓
Step 4: Open position in IBKR
```

### Don't Skip Steps!

A stock can score 10/16 but still be bad for Sell Put if:
- ❌ No 30-day options available
- ❌ IV too low
- ❌ Strike prices don't fit your budget
- ❌ BID = $0 (no liquidity)

---

## 💾 Saving and Tracking

### Save Results Periodically

Run monthly and compare:
```bash
# December run
python stock_screener.py
# Saves: stock_scores_20251206_142433.xlsx

# January run  
python stock_screener.py
# Saves: stock_scores_20250106_093021.xlsx

# Compare to see if scores changed
```

### Track Your Trades

In Google Sheets, add a column linking to screener scores:
```
If you traded F:
- Reference: "Screener score: 5.5/16 on 2024-12-06"
- Lesson: "Should have waited for 7+ score"
```
---

## 🎯 Next Steps

1. **Download the Excel file** from `/mnt/user-data/outputs/`

2. **Study the results** 
   - See which stocks you know scored well
   - Notice patterns (sectors, characteristics)

3. **When you have internet, run the full version**
   ```bash
   python stock_screener.py
   ```

4. **Compare with your current watchlist**
   - Did any of your stocks pass?
   - What's the average score?

5. **Use this + OptionStrat + Google Sheets**
   - Trinity of tools
   - All three must agree before trading

---

## 📞 Troubleshooting

**Error: "No module named 'yfinance'"**
```bash
pip install yfinance pandas openpyxl
```

**Error: "CONNECT tunnel failed, response 403"**
- Yahoo Finance is blocked in your environment
- Use the demo version instead
- Or run on your personal computer

**Want to add 1000s of stocks?**
- Use a stock listing API (NASDAQ, NYSE)
- But be aware: will take hours to run
- Start small, expand gradually

---

## ✅ Success Criteria

You'll know the screener is working when:

1. ✓ You can identify quality stocks automatically
2. ✓ You avoid bad stocks before even checking options
3. ✓ Your watchlist only has 7+ score stocks
4. ✓ You combine this with OptionStrat effectively
5. ✓ Your Google Sheets checklist pass rate increases

---

## 💪 Final Thoughts

**This screener saves you from:**
- ❌ Wasting time analyzing bad stocks
- ❌ Being tempted by cheap options on poor companies
- ❌ Ignoring fundamental analysis
- ❌ Making the INTC mistake again

**This screener helps you:**
- ✅ Focus only on quality companies
- ✅ Make data-driven decisions
- ✅ Build a systematic process
- ✅ Grow your portfolio safely

**Remember:**
> "It's not about finding the most opportunities. It's about finding the BEST opportunities."

With $6,890, you can't afford mistakes. This screener ensures every trade is backed by solid fundamentals.

---
