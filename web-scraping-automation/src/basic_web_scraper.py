"""
Basic Web Scraper - Extract and analyze data from websites
Demonstrates fundamental web scraping techniques with requests and BeautifulSoup
"""

import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import requests
import seaborn as sns
from bs4 import BeautifulSoup

# Global variables
OUTPUT_DIR = Path(__file__).parent.parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)


def scrape_quotes_toscrape() -> List[Dict]:
    """Scrape quotes from quotes.toscrape.com (a scraping practice site)"""
    print("Scraping quotes from quotes.toscrape.com...")

    base_url = "http://quotes.toscrape.com"
    page = 1
    quotes = []

    while True:
        print(f"  Scraping page {page}...")

        # Get the page
        url = f"{base_url}/page/{page}/"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  Error fetching page {page}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find quote containers
        quote_containers = soup.find_all('div', class_='quote')

        if not quote_containers:
            print(f"  No more quotes found on page {page}")
            break

        # Extract data from each quote
        for container in quote_containers:
            try:
                quote_text = container.find('span', class_='text').get_text()
                author = container.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in container.find_all('a', class_='tag')]

                quote_data = {
                    'quote': quote_text,
                    'author': author,
                    'tags': tags,
                    'page': page,
                    'scraped_at': datetime.now().isoformat()
                }

                quotes.append(quote_data)

            except AttributeError as e:
                print(f"  Error parsing quote: {e}")
                continue

        print(f"  Found {len(quote_containers)} quotes on page {page}")

        # Check for next page
        next_btn = soup.find('li', class_='next')
        if not next_btn:
            break

        page += 1
        time.sleep(1)  # Be respectful to the server

    print(f"Total quotes scraped: {len(quotes)}")
    return quotes


def save_to_csv(data: List[Dict], filename: str):
    """Save scraped data to CSV file"""
    if not data:
        print(f"No data to save for {filename}")
        return

    csv_path = OUTPUT_DIR / f"{filename}.csv"

    # Get all unique keys from all dictionaries
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    print(f"Data saved to: {csv_path}")
    return csv_path


def save_to_json(data: List[Dict], filename: str):
    """Save scraped data to JSON file"""
    if not data:
        print(f"No data to save for {filename}")
        return

    json_path = OUTPUT_DIR / f"{filename}.json"

    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)

    print(f"Data saved to: {json_path}")
    return json_path


def create_tags_visualization(quotes: List[Dict]):
    """Create visualizations for the top 10 tags analysis"""
    if not quotes:
        return

    print("\nCreating tags visualization...")

    # Calculate tags data
    tags_count = {}
    for quote in quotes:
        for tag in quote['tags']:
            tags_count[tag] = tags_count.get(tag, 0) + 1

    # Get top 10 tags
    top_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10]
    tag_names = [tag for tag, _ in top_tags]
    tag_counts = [count for _, count in top_tags]

    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")

    # Create figure for pie chart only
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.suptitle('Top 10 Tags Distribution from Quotes.toscrape.com', fontsize=16, fontweight='bold')

    # Pie Chart
    colors = sns.color_palette("husl", len(tag_names))
    wedges, texts, autotexts = ax.pie(tag_counts, labels=tag_names, autopct='%1.1f%%',
                                      colors=colors, startangle=90)

    # Enhance pie chart text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    # Adjust layout and save
    plt.tight_layout()

    # Save the visualization
    viz_path = OUTPUT_DIR / 'top_10_tags_analysis.png'
    plt.savefig(viz_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {viz_path}")

    # Show additional statistics
    total_tags_in_top10 = sum(tag_counts)
    total_quotes = len(quotes)
    coverage = (total_tags_in_top10 / total_quotes) * 100

    # Create a summary stats text box
    stats_text = f"""
    Total Quotes: {total_quotes}
    Top 10 Tags Coverage: {total_tags_in_top10}/{total_quotes} quotes ({coverage:.1f}%)
    Most Popular Tag: "{tag_names[0]}" ({tag_counts[0]} quotes)
    Least Popular in Top 10: "{tag_names[-1]}" ({tag_counts[-1]} quotes)
    """

    # Add stats as text
    fig.text(0.02, 0.02, stats_text, fontsize=10, bbox=dict(boxstyle="round", facecolor='lightgray', alpha=0.8))

    plt.show()
    plt.close()


def generate_summary_report(all_data: Dict[str, List[Dict]]):
    """Generate a comprehensive summary report"""
    print("\n" + "=" * 60)
    print("WEB SCRAPING AUTOMATION SUMMARY")
    print("=" * 60)

    total_items = sum(len(data) for data in all_data.values())
    print(f"Total items scraped: {total_items}")

    for data_type, data in all_data.items():
        print(f"  - {data_type}: {len(data)}")

    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("Files generated:")
    for file_path in OUTPUT_DIR.glob('*'):
        if file_path.is_file():
            print(f"  - {file_path.name}")


def run_complete_scraping():
    """Run the complete web scraping automation"""
    print("STARTING WEB SCRAPING AUTOMATION")
    print("=" * 60)

    all_scraped_data = {}

    # Scrape quotes only
    quotes = scrape_quotes_toscrape()
    if quotes:
        all_scraped_data['quotes'] = quotes
        save_to_csv(quotes, 'quotes_data')
        save_to_json(quotes, 'quotes_data')
        create_tags_visualization(quotes)

    # Generate summary
    generate_summary_report(all_scraped_data)


def main():
    """Main function to run web scraping automation"""
    run_complete_scraping()


if __name__ == "__main__":
    main()
