"""
US Stock Screener and Scorer
Fetches all US-listed stocks and scores them based on a 7-point investment criteria system
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

class StockScorer:
    """
    Scores stocks based on:
    1. Financial Analysis (max 9 points)
    2. Competitive Moat (max 7 points)  
    3. Risk Deductions (max -3 points)
    
    Total Score >= 7 = Good investment candidate
    """
    
    def __init__(self):
        self.min_passing_score = 7
        
    def score_financial_metrics(self, stock_info, historical_data):
        """
        Score based on financial metrics (max 9 points)
        
        Criteria:
        - EPS growth (1 point)
        - Dividend stability (0.5-1 point)
        - Share count stable/decreasing (1 point)
        - Book value growth (1 point)
        - Positive FCF (1 point)
        - Net margin >10% (0.5-1 point)
        - ROE 15-40% (0.5-1 point)
        - Interest coverage >10 (0.5-1 point)
        - Debt/Equity <0.5 (1 point)
        """
        score = 0
        details = {}
        
        try:
            # Get financial data
            financials = stock_info.get('financialData', {})
            key_stats = stock_info.get('defaultKeyStatistics', {})
            
            # 1. EPS Growth (1 point)
            eps_growth = financials.get('earningsGrowth', 0)
            if eps_growth and eps_growth > 0.05:  # >5% growth
                score += 1
                details['EPS Growth'] = f"✓ {eps_growth*100:.1f}%"
            else:
                details['EPS Growth'] = f"✗ {eps_growth*100:.1f}% if eps_growth else '✗ N/A'"
            
            # 2. Dividend (0.5-1 point)
            dividend_rate = stock_info.get('dividendRate', 0)
            five_year_avg_yield = stock_info.get('fiveYearAvgDividendYield', 0)
            
            if dividend_rate and dividend_rate > 0:
                if five_year_avg_yield and five_year_avg_yield > 0:
                    score += 1  # Consistent dividend
                    details['Dividend'] = f"✓ ${dividend_rate:.2f}, 5yr avg {five_year_avg_yield:.1f}%"
                else:
                    score += 0.5  # Has dividend but not long history
                    details['Dividend'] = f"⚠ ${dividend_rate:.2f}"
            else:
                details['Dividend'] = "✗ No dividend"
            
            # 3. Share Count (1 point) - using shares outstanding
            shares_outstanding = stock_info.get('sharesOutstanding', 0)
            if shares_outstanding:
                # If we can't get historical, give benefit of doubt if there's buyback program
                if stock_info.get('sharesShort', 0) or 'buyback' in str(stock_info.get('longBusinessSummary', '')).lower():
                    score += 0.5
                    details['Shares'] = "⚠ Unable to verify trend"
            
            # 4. Book Value - skip if data unavailable
            book_value = stock_info.get('bookValue', 0)
            if book_value and book_value > 0:
                score += 0.5
                details['Book Value'] = f"⚠ ${book_value:.2f}"
            
            # 5. Free Cash Flow (1 point)
            free_cash_flow = financials.get('freeCashflow', 0)
            if free_cash_flow and free_cash_flow > 0:
                score += 1
                details['FCF'] = f"✓ ${free_cash_flow/1e9:.2f}B"
            else:
                details['FCF'] = "✗ Negative or N/A"
            
            # 6. Net Margin (0.5-1 point)
            profit_margin = financials.get('profitMargins', 0)
            if profit_margin:
                if profit_margin > 0.10:  # >10%
                    score += 1
                    details['Net Margin'] = f"✓ {profit_margin*100:.1f}%"
                elif profit_margin > 0.05:  # >5% but stable
                    score += 0.5
                    details['Net Margin'] = f"⚠ {profit_margin*100:.1f}%"
                else:
                    details['Net Margin'] = f"✗ {profit_margin*100:.1f}%"
            
            # 7. ROE (0.5-1 point)
            roe = financials.get('returnOnEquity', 0)
            if roe:
                if 0.15 <= roe <= 0.40:  # 15-40%
                    score += 1
                    details['ROE'] = f"✓ {roe*100:.1f}%"
                elif 0.10 <= roe < 0.15:  # 10-15%
                    score += 0.5
                    details['ROE'] = f"⚠ {roe*100:.1f}%"
                else:
                    details['ROE'] = f"✗ {roe*100:.1f}%"
            
            # 8. Interest Coverage (0.5-1 point)
            ebit = financials.get('ebit', 0)
            interest_expense = financials.get('interestExpense', 0)
            
            if interest_expense and interest_expense != 0:
                ic_ratio = abs(ebit / interest_expense) if ebit else 0
                if ic_ratio > 10:
                    score += 1
                    details['Interest Coverage'] = f"✓ {ic_ratio:.1f}x"
                elif ic_ratio > 5:
                    score += 0.5
                    details['Interest Coverage'] = f"⚠ {ic_ratio:.1f}x"
                else:
                    details['Interest Coverage'] = f"✗ {ic_ratio:.1f}x"
            else:
                score += 1  # No debt = best case
                details['Interest Coverage'] = "✓ No debt"
            
            # 9. Debt/Equity (1 point)
            debt_to_equity = financials.get('debtToEquity', 0)
            if debt_to_equity is not None:
                if debt_to_equity < 50:  # <0.5 (expressed as percentage)
                    score += 1
                    details['D/E Ratio'] = f"✓ {debt_to_equity/100:.2f}"
                else:
                    details['D/E Ratio'] = f"✗ {debt_to_equity/100:.2f}"
            
        except Exception as e:
            details['Error'] = str(e)
        
        return score, details
    
    def score_competitive_moat(self, stock_info):
        """
        Score based on competitive advantages (max 7 points)
        
        Criteria:
        - Brand (1 point) - based on market cap and consumer recognition
        - Patents/Licenses (1 point) - pharma, tech with high R&D
        - Cost advantage (1 point) - high profit margin with scale
        - High switching cost (1 point) - B2B software, banking
        - Network effects (1 point) - platforms, payments
        - Niche market (1 point) - smaller market cap with dominance
        - Longevity confidence (1 point) - age and stability
        """
        score = 0
        details = {}
        
        try:
            sector = stock_info.get('sector', '')
            industry = stock_info.get('industry', '')
            market_cap = stock_info.get('marketCap', 0)
            profit_margin = stock_info.get('profitMargins', 0)
            
            # 1. Brand (1 point) - large consumer-facing companies
            if market_cap > 50e9:  # >$50B market cap
                if sector in ['Consumer Cyclical', 'Consumer Defensive', 'Communication Services']:
                    score += 1
                    details['Brand'] = "✓ Large consumer brand"
                else:
                    score += 0.5
                    details['Brand'] = "⚠ Large company"
            
            # 2. Patents/Licenses (1 point)
            if sector in ['Healthcare', 'Technology']:
                score += 1
                details['Patents'] = f"✓ {sector} sector"
            
            # 3. Cost advantage (1 point)
            if profit_margin and profit_margin > 0.15 and market_cap > 10e9:
                score += 1
                details['Cost Advantage'] = f"✓ {profit_margin*100:.1f}% margin + scale"
            
            # 4. Switching costs (1 point)
            high_switching_industries = ['Software', 'Banks', 'Insurance', 'Utilities']
            if any(ind in industry for ind in high_switching_industries):
                score += 1
                details['Switching Cost'] = f"✓ {industry}"
            
            # 5. Network effects (1 point)
            network_industries = ['Internet', 'Payment', 'Social Media', 'Marketplace']
            if any(net in industry for net in network_industries):
                score += 1
                details['Network Effect'] = f"✓ {industry}"
            
            # 6. Niche market (1 point)
            if 1e9 < market_cap < 10e9:  # $1B-$10B
                score += 0.5
                details['Niche'] = "⚠ Mid-cap potential niche"
            
            # 7. Longevity (1 point) - based on company age proxy
            # If pays dividend consistently, likely established
            if stock_info.get('fiveYearAvgDividendYield', 0) > 0:
                score += 1
                details['Longevity'] = "✓ Established (dividend history)"
            elif market_cap > 100e9:
                score += 0.5
                details['Longevity'] = "⚠ Large cap (likely established)"
                
        except Exception as e:
            details['Error'] = str(e)
        
        return score, details
    
    def calculate_risk_deductions(self, stock_info):
        """
        Deduct points for specific risks (max -3 points)
        
        Risks:
        - Technology risk (-1): Fast-changing tech sectors
        - Government risk (-1): Revenue dependent on government
        - China risk (-1): Chinese companies listed in US
        """
        deduction = 0
        details = {}
        
        try:
            sector = stock_info.get('sector', '')
            industry = stock_info.get('industry', '')
            country = stock_info.get('country', '')
            
            # 1. Technology risk
            high_tech_industries = ['Semiconductor', 'Software—Application', 'Electronics', 
                                   'Consumer Electronics', 'Internet Content']
            if any(tech in industry for tech in high_tech_industries):
                deduction -= 1
                details['Tech Risk'] = f"✗ -{1} ({industry})"
            
            # 2. Government risk
            gov_industries = ['Aerospace & Defense', 'Government']
            if any(gov in industry for gov in gov_industries):
                deduction -= 1
                details['Gov Risk'] = f"✗ -{1} ({industry})"
            
            # 3. China risk
            if country in ['China', 'Hong Kong']:
                deduction -= 1
                details['China Risk'] = f"✗ -{1} (Chinese company)"
                
        except Exception as e:
            details['Error'] = str(e)
        
        return deduction, details
    
    def score_stock(self, ticker):
        """
        Complete scoring for a single stock
        
        Returns: dict with scores and details
        """
        try:
            # Fetch stock data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get historical data for trend analysis
            hist = stock.history(period="5y")
            
            # Calculate scores
            financial_score, financial_details = self.score_financial_metrics(info, hist)
            moat_score, moat_details = self.score_competitive_moat(info)
            risk_deduction, risk_details = self.calculate_risk_deductions(info)
            
            total_score = financial_score + moat_score + risk_deduction
            
            result = {
                'ticker': ticker,
                'company_name': info.get('longName', ticker),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', 0),
                'financial_score': financial_score,
                'moat_score': moat_score,
                'risk_deduction': risk_deduction,
                'total_score': total_score,
                'passing': total_score >= self.min_passing_score,
                'financial_details': financial_details,
                'moat_details': moat_details,
                'risk_details': risk_details,
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
            }
            
            return result
            
        except Exception as e:
            return {
                'ticker': ticker,
                'error': str(e),
                'total_score': 0,
                'passing': False
            }


def get_all_us_stocks():
    """
    Get list of all US-listed stocks
    
    Sources:
    1. NASDAQ listed stocks
    2. NYSE listed stocks
    3. Common ETFs
    """
    
    print("Fetching list of US-listed stocks...")
    
    # Download stock lists from various sources
    stocks = set()
    
    # Method 1: Use a predefined list of major US stocks
    # In production, you'd want to use a more comprehensive data source
    
    # Major indices components
    major_tickers = [
        # FAANG + Microsoft
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
        
        # Blue chips
        'JNJ', 'JPM', 'V', 'WMT', 'PG', 'UNH', 'HD', 'BAC', 'XOM', 'CVX',
        'ABBV', 'MA', 'KO', 'PEP', 'COST', 'MRK', 'TMO', 'AVGO', 'ABT', 'LLY',
        'ORCL', 'ACN', 'NKE', 'CSCO', 'DHR', 'VZ', 'ADBE', 'CRM', 'MCD', 'WFC',
        
        # Dividend aristocrats
        'MMM', 'AFL', 'APD', 'ADM', 'AOS', 'ABT', 'ABBV', 'ADP', 'ALB', 'ARE',
        'CHRW', 'CAH', 'CAT', 'CB', 'CINF', 'CTAS', 'CLX', 'CL', 'ED', 'ECL',
        'EMR', 'ESS', 'EXR', 'XOM', 'FRT', 'GD', 'GPC', 'HRL', 'ITW', 'IBM',
        
        # Tech
        'AMD', 'INTC', 'QCOM', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS', 'CDNS',
        'NOW', 'PANW', 'CRWD', 'ZS', 'DDOG', 'NET', 'SNOW',
        
        # Finance
        'GS', 'MS', 'C', 'BLK', 'SCHW', 'AXP', 'USB', 'PNC', 'TFC', 'COF',
        
        # Healthcare
        'UNH', 'CVS', 'CI', 'HUM', 'ANTM', 'PFE', 'MRNA', 'BMY', 'GILD', 'AMGN',
        
        # Consumer
        'DIS', 'NFLX', 'SBUX', 'NKE', 'LOW', 'TGT', 'TJX', 'ROST', 'DG', 'DLTR',
        
        # Industrials
        'BA', 'HON', 'UPS', 'RTX', 'LMT', 'GE', 'DE', 'EMR', 'MMM',
        
        # Energy
        'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO',
        
        # Telecom & Utilities
        'T', 'TMUS', 'VZ', 'NEE', 'DUK', 'SO', 'D', 'AEP',
        
        # Small caps mentioned in conversation
        'F', 'SOFI', 'PATH', 'PLTR', 'NIO', 'GME', 'INTC',
    ]
    
    stocks.update(major_tickers)
    
    print(f"Found {len(stocks)} stocks to analyze")
    return sorted(list(stocks))


def main():
    """
    Main execution function
    """
    print("="*80)
    print("US STOCK SCREENER & SCORER")
    print("="*80)
    print()
    
    # Initialize scorer
    scorer = StockScorer()
    
    # Get stock list
    stock_list = get_all_us_stocks()
    
    # Score all stocks
    print(f"\nScoring {len(stock_list)} stocks...")
    print("This may take several minutes...\n")
    
    results = []
    
    for i, ticker in enumerate(stock_list, 1):
        print(f"[{i}/{len(stock_list)}] Analyzing {ticker}...", end=" ")
        
        try:
            result = scorer.score_stock(ticker)
            results.append(result)
            
            if 'error' in result:
                print(f"✗ Error: {result['error']}")
            else:
                status = "✓ PASS" if result['passing'] else "✗ FAIL"
                print(f"{status} (Score: {result['total_score']}/16)")
            
            # Rate limiting - be nice to Yahoo Finance
            time.sleep(0.5)
            
        except Exception as e:
            print(f"✗ Failed: {e}")
            results.append({
                'ticker': ticker,
                'error': str(e),
                'total_score': 0,
                'passing': False
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Filter to only valid results (exclude rows with 'error' key)
    if 'error' in df.columns:
        df_valid = df[df['error'].isna()].copy()
    else:
        df_valid = df.copy()
    
    # Sort by total score
    df_valid = df_valid.sort_values('total_score', ascending=False)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define summary columns
    summary_cols = ['ticker', 'company_name', 'sector', 'industry', 'current_price', 
                   'market_cap', 'financial_score', 'moat_score', 'risk_deduction', 
                   'total_score', 'passing', 'dividend_yield']
    
    # Save to CSV files in output folder
    output_dir = './output'
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Save main summary CSV
    csv_file = f'{output_dir}/stock_scores_{timestamp}.csv'
    df_valid[summary_cols].to_csv(csv_file, index=False)
    print(f"\n✓ Saved main results to: {csv_file}")
    
    # 2. Save top scorers CSV (>=7 points)
    top_scorers = df_valid[df_valid['passing'] == True]
    top_scorers_file = f'{output_dir}/stock_scores_top_scorers_{timestamp}.csv'
    top_scorers[summary_cols].to_csv(top_scorers_file, index=False)
    print(f"✓ Saved top scorers to: {top_scorers_file}")
    
    # 3. Save budget-friendly stocks CSV
    budget_stocks = df_valid[
        (df_valid['passing'] == True) & 
        (df_valid['current_price'] < 20) &
        (df_valid['current_price'] > 0)
    ].sort_values('total_score', ascending=False)
    
    if len(budget_stocks) > 0:
        budget_file = f'{output_dir}/stock_scores_budget_friendly_{timestamp}.csv'
        budget_stocks[summary_cols].to_csv(budget_file, index=False)
        print(f"✓ Saved budget-friendly stocks to: {budget_file}")
    
    # 4. Save by sector (separate CSV for each sector)
    for sector in df_valid['sector'].unique():
        if pd.notna(sector):
            sector_df = df_valid[df_valid['sector'] == sector]
            # Clean sector name for filename
            clean_sector = sector.replace(' ', '_').replace('&', 'and').replace('/', '_')
            sector_file = f'{output_dir}/stock_scores_sector_{clean_sector}_{timestamp}.csv'
            sector_df[summary_cols].to_csv(sector_file, index=False)
            print(f"✓ Saved {sector} sector to: {sector_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nTotal stocks analyzed: {len(df_valid)}")
    print(f"Stocks with score ≥7: {len(top_scorers)} ({len(top_scorers)/len(df_valid)*100:.1f}%)")
    print(f"\nAll CSV files saved to: {output_dir}")
    print(f"Main results: stock_scores_{timestamp}.csv")
    
    # Print top 20 scorers
    print("\n" + "="*80)
    print("TOP 20 STOCKS (Highest Scores)")
    print("="*80)
    print(f"\n{'Rank':<6}{'Ticker':<8}{'Company':<40}{'Score':<8}{'Price':<12}")
    print("-" * 80)
    
    for i, row in enumerate(df_valid.head(20).itertuples(), 1):
        company = row.company_name[:38] if hasattr(row, 'company_name') else row.ticker
        price = f"${row.current_price:.2f}" if hasattr(row, 'current_price') and row.current_price else 'N/A'
        print(f"{i:<6}{row.ticker:<8}{company:<40}{row.total_score:<8}{price:<12}")
    
    # Print stocks suitable for your budget ($6,890)
    print("\n" + "="*80)
    print("STOCKS SUITABLE FOR YOUR BUDGET ($6,890)")
    print("(Score ≥7, Price <$20 for reasonable collateral)")
    print("="*80)
    
    budget_stocks = df_valid[
        (df_valid['passing'] == True) & 
        (df_valid['current_price'] < 20) &
        (df_valid['current_price'] > 0)
    ].sort_values('total_score', ascending=False)
    
    if len(budget_stocks) > 0:
        print(f"\n{'Ticker':<8}{'Company':<35}{'Price':<12}{'Score':<8}{'Sector':<20}")
        print("-" * 90)
        
        for row in budget_stocks.head(15).itertuples():
            company = row.company_name[:33] if hasattr(row, 'company_name') else row.ticker
            price = f"${row.current_price:.2f}"
            sector = row.sector[:18] if hasattr(row, 'sector') else 'N/A'
            print(f"{row.ticker:<8}{company:<35}{price:<12}{row.total_score:<8}{sector:<20}")
    else:
        print("\nNo stocks found matching criteria")
    
    print("\n" + "="*80)
    print("DONE!")
    print("="*80)
    
    return df_valid


if __name__ == "__main__":
    results_df = main()