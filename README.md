# US Stock Screener & Scorer

This program automatically fetches and scores all major US-listed stocks based on a comprehensive 7-point investment criteria system.

## Features

- Reads ticker symbols from CSV file
- Scores stocks on 16-point scale based on:
  - Financial metrics (max 9 points)
  - Competitive moat (max 7 points)
  - Risk deductions (max -3 points)
- Generates multiple CSV output files:
  - All stock scores
  - Top scorers (≥7 points)
  - Budget-friendly options (<$20)
  - Sector-specific results

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

Create a `data` folder in the same directory as the script:

```bash
mkdir data
```

Place your `nasdaqtraded.csv` file in the `data` folder. The CSV must have a column named `ticker` (case-insensitive).

**Example CSV structure:**
```csv
ticker
AAPL
MSFT
GOOGL
AMZN
```

### 3. Run the Screener

```bash
python stock_screener.py
```

## Output Files

Results are saved in the `output` folder with timestamp:

- `stock_scores_YYYYMMDD_HHMMSS.csv` - All analyzed stocks
- `stock_scores_top_scorers_YYYYMMDD_HHMMSS.csv` - Stocks with score ≥7
- `stock_scores_budget_friendly_YYYYMMDD_HHMMSS.csv` - High-scoring stocks <$20
- `stock_scores_sector_*.csv` - Results by sector

## Scoring System

### Financial Analysis (Max 9 Points)

1. **EPS Growth** (1 pt) - >5% annual growth
2. **Dividend Stability** (0.5-1 pt) - Consistent dividend payments
3. **Share Count** (1 pt) - Stable or decreasing shares
4. **Book Value** (1 pt) - Positive book value growth
5. **Free Cash Flow** (1 pt) - Positive FCF
6. **Net Margin** (0.5-1 pt) - >10% margin
7. **ROE** (0.5-1 pt) - 15-40% return on equity
8. **Interest Coverage** (0.5-1 pt) - >10x coverage
9. **Debt/Equity** (1 pt) - <0.5 ratio

### Competitive Moat (Max 7 Points)

1. **Brand** (1 pt) - Large consumer brand
2. **Patents/Licenses** (1 pt) - Healthcare/Tech sectors
3. **Cost Advantage** (1 pt) - High margins with scale
4. **Switching Costs** (1 pt) - Software/Banking/Insurance
5. **Network Effects** (1 pt) - Platforms/Payments
6. **Niche Market** (1 pt) - Mid-cap dominance
7. **Longevity** (1 pt) - Established companies

### Risk Deductions (Max -3 Points)

1. **Technology Risk** (-1 pt) - Fast-changing sectors
2. **Government Risk** (-1 pt) - Dependent on government
3. **China Risk** (-1 pt) - Chinese companies

## Trading Criteria

**Recommended for Options Trading:**
- Company Score: ≥7 points
- Budget-friendly: Price <$20 (for $6,890 budget)
- High dividend yield preferred

## Notes

- Script includes 0.5 second delay between API calls to respect rate limits
- Runtime depends on number of stocks (typically 0.5s per stock)
- Yahoo Finance API may occasionally fail for specific tickers
- Results are sorted by total score (highest first)

## Troubleshooting

**Error: File not found**
- Ensure `data/nasdaqtraded.csv` exists
- Check CSV has `ticker` column header

**Error: No module named 'yfinance'**
- Run `pip install -r requirements.txt`

**Slow performance**
- Normal - script deliberately includes delays
- For 1000 stocks, expect ~8-10 minutes runtime

## Example Output

```
================================================================================
TOP 20 STOCKS (Highest Scores)
================================================================================

Rank  Ticker  Company                                 Score   Price       
--------------------------------------------------------------------------------
1     AAPL    Apple Inc.                              8.5     $175.23     
2     MSFT    Microsoft Corporation                   8.5     $378.91     
3     ORCL    Oracle Corporation                      8.5     $119.45     
...
```

## License

Free to use for personal investment research.

## Disclaimer

This tool is for educational and research purposes only. Always do your own due diligence before making investment decisions. Past performance does not guarantee future results.
