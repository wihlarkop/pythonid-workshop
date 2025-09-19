# Web Scraping Automation

A clean, function-based web scraping automation that demonstrates fundamental web scraping techniques using Python.

## Features

- **Function-based architecture** - Simple, easy-to-understand functions
- **Multiple data sources** - Scrapes quotes and books from practice sites
- **Data export** - Saves data in CSV and JSON formats
- **Data analysis** - Provides statistical insights
- **Visualizations** - Creates charts and graphs
- **Error handling** - Robust error handling for network issues

## What it does

1. **Scrapes Quotes** - Extracts quotes, authors, and tags from quotes.toscrape.com
2. **Scrapes Books** - Extracts book titles, prices, ratings from books.toscrape.com
3. **Analyzes Data** - Provides statistics and insights
4. **Creates Visualizations** - Generates charts for data analysis
5. **Exports Results** - Saves data in multiple formats

## Sample Output

- **100 quotes** from 50 different authors with 137 unique tags
- **100 books** with price range £10-£58 and rating distribution
- **Comprehensive analysis** with top authors, tags, and pricing insights
- **Visual charts** showing data distributions and patterns

## Files Generated

- `quotes_data.csv` / `quotes_data.json` - Scraped quotes data
- `books_data.csv` / `books_data.json` - Scraped books data
- `quotes_analysis.png` - Author and tag visualizations
- `books_analysis.png` - Price and rating distributions

## Usage

```bash
uv run python web-scraping-automation/src/basic_web_scraper.py
```

This replaces the previous messy automation-case with a clean, focused web scraping automation project.