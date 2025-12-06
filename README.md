# US Stock Screener & Scorer

## Overview

This program automatically fetches and scores all major US-listed stocks based on a comprehensive 7-point investment criteria system.

## Scoring System

### Total Score = Financial Score + Moat Score + Risk Deductions

**Minimum Passing Score: 7 points**

---

## 1. Financial Analysis (Max 9 Points)

| Criteria | Points | Requirements |
|----------|--------|--------------|
| **EPS Growth** | 1.0 | 10-year stable growth OR >5% recent growth |
| **Dividend** | 0.5-1.0 | 1.0: Consistent 5+ year dividend<br>0.5: Has dividend |
| **Share Count** | 1.0 | Stable or decreasing (buybacks) |
| **Book Value** | 1.0 | 10-year stable growth |
| **Free Cash Flow** | 1.0 | Consistently positive |
| **Net Margin** | 0.5-1.0 | 1.0: >10%<br>0.5: >5% and stable |
| **ROE** | 0.5-1.0 | 1.0: 15-40%<br>0.5: 10-15% |
| **Interest Coverage** | 0.5-1.0 | 1.0: >10x or no debt<br>0.5: >5x |
| **Debt/Equity** | 1.0 | <0.5 |

---

## 2. Competitive Moat (Max 7 Points)

| Criteria | Points | Indicators |
|----------|--------|------------|
| **Brand** | 1.0 | Large market cap + consumer-facing |
| **Patents/Licenses** | 1.0 | Healthcare or Technology sector |
| **Cost Advantage** | 1.0 | High margin (>15%) + large scale |
| **Switching Costs** | 1.0 | Software, Banking, Insurance, Utilities |
| **Network Effects** | 1.0 | Internet, Payment, Social Media platforms |
| **Niche Market** | 1.0 | Market leader in specialized segment |
| **Longevity** | 1.0 | Established company (dividend history or large cap) |

---

## 3. Risk Deductions (Max -3 Points)

| Risk | Deduction | Description |
|------|-----------|-------------|
| **Technology Risk** | -1 | Semiconductor, Software, Electronics sectors |
| **Government Risk** | -1 | Aerospace, Defense, Government contractors |
| **China Risk** | -1 | Chinese companies listed in US |

---

## Installation

```bash
# Install required packages
pip install yfinance pandas numpy openpyxl

# Or if using system Python
pip install yfinance pandas numpy openpyxl --break-system-packages
```

---

## Usage

### Basic Run

```bash
python stock_screener.py
```

This will:
1. Fetch data for ~200 major US stocks
2. Score each stock
3. Generate an Excel file with results
4. Print summary statistics

### Output

The program generates an Excel file with multiple sheets:

1. **Summary**: All stocks with scores
2. **Top Scorers (≥7)**: Only stocks passing the 7-point threshold
3. **Sector Sheets**: Stocks grouped by sector

### Output Columns

- `ticker`: Stock symbol
- `company_name`: Full company name
- `sector`: Business sector
- `industry`: Specific industry
- `current_price`: Current stock price
- `market_cap`: Market capitalization
- `financial_score`: Score from financial metrics (0-9)
- `moat_score`: Score from competitive advantages (0-7)
- `risk_deduction`: Risk penalties (0 to -3)
- `total_score`: Final score (Financial + Moat + Risk)
- `passing`: TRUE if score ≥ 7
- `dividend_yield`: Current dividend yield %

---

## Example Results

### Top Scoring Stocks (Score ≥7)

```
Rank  Ticker  Company                    Score  Price
1     AAPL    Apple Inc.                 12.0   $195.50
2     MSFT    Microsoft Corporation      11.5   $425.30
3     KO      The Coca-Cola Company      11.0   $62.15
4     JNJ     Johnson & Johnson          10.5   $158.20
5     V       Visa Inc.                  10.0   $285.40
```

### Budget-Friendly Options (Price <$20, Score ≥7)

```
Ticker  Company              Price    Score  Sector
F       Ford Motor Company   $13.01   7.0    Consumer Cyclical
T       AT&T Inc.            $25.27   8.0    Communication Services
```

---

## Customization

### Add More Stocks

Edit the `get_all_us_stocks()` function to include more tickers:

```python
major_tickers = [
    'AAPL', 'MSFT', 'GOOGL',  # Add more here
    'YOUR_STOCK_1', 'YOUR_STOCK_2',
]
```

### Adjust Scoring Criteria

Modify the scoring functions in the `StockScorer` class:

- `score_financial_metrics()` - Adjust financial requirements
- `score_competitive_moat()` - Modify moat criteria
- `calculate_risk_deductions()` - Change risk factors

### Change Minimum Passing Score

```python
scorer = StockScorer()
scorer.min_passing_score = 8  # Raise bar to 8 points
```

---

## Performance Tips

1. **Rate Limiting**: The script includes a 0.5s delay between requests to avoid overwhelming Yahoo Finance

2. **Batch Processing**: For very large stock lists, consider processing in batches:
   ```python
   stock_list = get_all_us_stocks()
   batch_size = 50
   for i in range(0, len(stock_list), batch_size):
       batch = stock_list[i:i+batch_size]
       # Process batch
   ```

3. **Caching**: Save results and only update periodically (weekly/monthly)

---

## Limitations

1. **Data Availability**: Some metrics may not be available for all stocks
2. **Historical Data**: 10-year trends are approximated using available data
3. **Qualitative Factors**: Brand strength and moat quality are estimated using proxies
4. **Real-time Accuracy**: Data is fetched from Yahoo Finance with slight delays

---

## For Your Specific Use Case

### Finding Sell Put Candidates

Use this screener to find stocks that meet your criteria:

1. **Run the screener**
2. **Filter results**:
   - Score ≥ 7 (good company)
   - Price suitable for your budget
   - Check dividend yield for income potential

3. **Then verify with OptionStrat**:
   - 25-35 days to expiration
   - Strike 10-20% out of money
   - IV Rank >50%
   - Success probability >80%

### Budget Considerations ($6,890)

**Conservative (25% max per position):**
- Maximum collateral: $1,722
- Look for stocks priced: <$17.22

**Moderate (30% max per position):**
- Maximum collateral: $2,067
- Look for stocks priced: <$20.67

**Examples from results:**
- F ($13): Collateral $900-1,300 ✓
- T ($25): Collateral $2,000-2,500 ✓

---

## Troubleshooting

### Error: "No module named 'yfinance'"
```bash
pip install yfinance
```

### Error: "Rate limit exceeded"
- Increase delay in main loop: `time.sleep(1.0)`
- Run during off-peak hours

### Error: "No data available"
- Stock may be delisted or have ticker change
- Check ticker symbol is correct

---

## Future Enhancements

1. **Real-time monitoring**: Schedule daily runs
2. **Alerts**: Email when new stocks meet criteria  
3. **Backtesting**: Historical score tracking
4. **Integration**: Connect with broker API for automatic trading
5. **Machine Learning**: Improve scoring predictions

---

## License

Free to use and modify for personal investment research.

## Disclaimer

This tool is for educational and research purposes only. Always do your own due diligence before making investment decisions. Past performance does not guarantee future results.
