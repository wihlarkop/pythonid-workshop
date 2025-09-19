"""
Sentiment Analysis of Product Reviews
Uses TextBlob to analyze sentiment polarity and classify reviews as positive, negative, or neutral
Creates visualization of sentiment distribution
"""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud

warnings.filterwarnings('ignore')

# Global variables
OUTPUT_DIR = Path(__file__).parent.parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)


def load_reviews(csv_path):
    """Load reviews from CSV file"""
    try:
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"Reviews CSV file not found: {csv_path}")

        # Load CSV data
        reviews_df = pd.read_csv(csv_path)

        # Handle different dataset formats
        if 'content' in reviews_df.columns:
            # Gojek dataset format
            reviews_df = reviews_df.rename(columns={'content': 'review'})
            print(f"Loaded {len(reviews_df)} Gojek app reviews from {csv_path}")
        elif 'review' in reviews_df.columns:
            # Standard review format
            print(f"Loaded {len(reviews_df)} reviews from {csv_path}")
        else:
            raise ValueError("CSV must contain either 'review' or 'content' column")

        # Sample large datasets for workshop purposes
        if len(reviews_df) > 5000:
            reviews_df = reviews_df.sample(n=5000, random_state=42).reset_index(drop=True)
            print(f"Sampled 5000 reviews for analysis (original: {len(reviews_df)} reviews)")

        return reviews_df

    except Exception as e:
        print(f"Error loading reviews: {e}")
        raise


def analyze_sentiment(reviews_df):
    """Analyze sentiment polarity for each review using TextBlob"""
    if reviews_df is None or reviews_df.empty:
        raise ValueError("No reviews data provided")

    print("Analyzing sentiment with TextBlob...")

    # Initialize lists to store results
    polarities = []
    subjectivities = []
    sentiments = []

    # Analyze each review
    for review_text in reviews_df['review']:
        try:
            # Handle missing/null values
            if pd.isna(review_text) or review_text == '':
                polarities.append(0.0)
                subjectivities.append(0.0)
                sentiments.append('neutral')
                continue

            # Create TextBlob object and analyze sentiment
            blob = TextBlob(str(review_text))
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            # Classify sentiment based on polarity
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            # Store results
            polarities.append(polarity)
            subjectivities.append(subjectivity)
            sentiments.append(sentiment)

        except Exception as e:
            print(f"Error analyzing review: {e}")
            # Default values for problematic reviews
            polarities.append(0.0)
            subjectivities.append(0.0)
            sentiments.append('neutral')

    # Add sentiment data to dataframe
    reviews_df['polarity'] = polarities
    reviews_df['subjectivity'] = subjectivities
    reviews_df['sentiment'] = sentiments

    print("Sentiment analysis completed!")
    return reviews_df


def create_sentiment_visualizations(reviews_df):
    """Create sentiment distribution pie chart"""
    print("Creating sentiment distribution chart...")

    # Get sentiment counts
    sentiment_counts = reviews_df['sentiment'].value_counts()

    # Define colors matching your screenshot
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # Green for neutral, Red for positive, Gray for negative

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Create pie chart
    wedges, texts, autotexts = ax.pie(sentiment_counts.values,
                                      labels=sentiment_counts.index,
                                      autopct='%1.1f%%',
                                      colors=colors,
                                      startangle=90)

    # Set title
    ax.set_title('Sentiment Distribution', fontsize=16, fontweight='bold', pad=20)

    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)

    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')

    # Save visualization
    save_path = OUTPUT_DIR / 'sentiment_distribution.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Sentiment distribution chart saved: {save_path}")

    plt.show()
    plt.close()

    return save_path


def create_wordcloud_visualization(reviews_df):
    """Create word clouds for positive and negative reviews"""
    print("Creating word cloud visualizations...")

    # Separate reviews by sentiment
    positive_reviews = reviews_df[reviews_df['sentiment'] == 'positive']['review']
    negative_reviews = reviews_df[reviews_df['sentiment'] == 'negative']['review']

    # Create figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Word Clouds by Sentiment', fontsize=16, fontweight='bold')

    # Positive reviews word cloud
    if not positive_reviews.empty:
        positive_text = ' '.join(positive_reviews.astype(str))
        positive_wordcloud = WordCloud(width=800, height=400,
                                       background_color='white',
                                       colormap='Greens').generate(positive_text)

        axes[0].imshow(positive_wordcloud, interpolation='bilinear')
        axes[0].set_title('Positive Reviews Word Cloud', fontsize=14)
        axes[0].axis('off')
    else:
        axes[0].text(0.5, 0.5, 'No positive reviews found',
                     ha='center', va='center', transform=axes[0].transAxes)
        axes[0].set_title('Positive Reviews Word Cloud', fontsize=14)

    # Negative reviews word cloud
    if not negative_reviews.empty:
        negative_text = ' '.join(negative_reviews.astype(str))
        negative_wordcloud = WordCloud(width=800, height=400,
                                       background_color='white',
                                       colormap='Reds').generate(negative_text)

        axes[1].imshow(negative_wordcloud, interpolation='bilinear')
        axes[1].set_title('Negative Reviews Word Cloud', fontsize=14)
        axes[1].axis('off')
    else:
        axes[1].text(0.5, 0.5, 'No negative reviews found',
                     ha='center', va='center', transform=axes[1].transAxes)
        axes[1].set_title('Negative Reviews Word Cloud', fontsize=14)

    # Save word cloud visualization
    wordcloud_path = OUTPUT_DIR / 'sentiment_wordclouds.png'
    plt.savefig(wordcloud_path, dpi=300, bbox_inches='tight')
    print(f"Word cloud visualization saved: {wordcloud_path}")

    plt.show()
    plt.close()

    return wordcloud_path


def calculate_sentiment_statistics(reviews_df):
    """Calculate and display comprehensive sentiment statistics"""
    # Basic counts
    total_reviews = len(reviews_df)
    sentiment_counts = reviews_df['sentiment'].value_counts()

    positive_count = sentiment_counts.get('positive', 0)
    negative_count = sentiment_counts.get('negative', 0)
    neutral_count = sentiment_counts.get('neutral', 0)

    # Percentages
    positive_ratio = (positive_count / total_reviews) * 100
    negative_ratio = (negative_count / total_reviews) * 100
    neutral_ratio = (neutral_count / total_reviews) * 100

    # Polarity statistics
    mean_polarity = reviews_df['polarity'].mean()
    median_polarity = reviews_df['polarity'].median()
    std_polarity = reviews_df['polarity'].std()

    # Subjectivity statistics
    mean_subjectivity = reviews_df['subjectivity'].mean()
    median_subjectivity = reviews_df['subjectivity'].median()

    print(f"\nGOJEK APP REVIEW STATISTICS:")
    print(f"Total reviews analyzed: {total_reviews}")
    print(f"Positive reviews: {positive_count} ({positive_ratio:.1f}%)")
    print(f"Negative reviews: {negative_count} ({negative_ratio:.1f}%)")
    print(f"Neutral reviews: {neutral_count} ({neutral_ratio:.1f}%)")

    # App rating analysis if score column exists
    if 'score' in reviews_df.columns:
        rating_counts = reviews_df['score'].value_counts().sort_index()
        mean_rating = reviews_df['score'].mean()
        print(f"\nAPP STORE RATINGS:")
        print(f"Average rating: {mean_rating:.2f}/5.0")
        for rating in sorted(rating_counts.index):
            count = rating_counts[rating]
            percentage = (count / total_reviews) * 100
            print(f"{rating} stars: {count} reviews ({percentage:.1f}%)")

    print(f"\nSENTIMENT ANALYSIS METRICS:")
    print(f"Mean polarity: {mean_polarity:.3f}")
    print(f"Median polarity: {median_polarity:.3f}")
    print(f"Standard deviation: {std_polarity:.3f}")
    print(f"Mean subjectivity: {mean_subjectivity:.3f}")

    print(f"\nKEY INSIGHTS:")
    print(f"Most positive review (polarity: {reviews_df['polarity'].max():.3f})")
    print(f"Most negative review (polarity: {reviews_df['polarity'].min():.3f})")

    # Business insights for Gojek app
    if positive_ratio > 60:
        print(f"   Strong user satisfaction ({positive_ratio:.1f}% positive sentiment)")
        print("   Recommendation: Highlight positive features in app store description")
    elif negative_ratio > 40:
        print(f"   High user dissatisfaction detected ({negative_ratio:.1f}%)")
        print("   Recommendation: Address common complaints in next app update")
    else:
        print("   Mixed user feedback - room for improvement")
        print("   Recommendation: Focus on converting neutral users to positive")

    # Create statistics dictionary
    stats = {
        'total_reviews': total_reviews,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'positive_ratio': positive_ratio,
        'negative_ratio': negative_ratio,
        'neutral_ratio': neutral_ratio,
        'mean_polarity': mean_polarity,
        'median_polarity': median_polarity,
        'std_polarity': std_polarity,
        'mean_subjectivity': mean_subjectivity,
        'median_subjectivity': median_subjectivity
    }

    return stats


def save_results_to_csv(reviews_df, filename='sentiment_results.csv'):
    """Save analyzed results to CSV file"""
    output_path = OUTPUT_DIR / filename
    reviews_df.to_csv(output_path, index=False)
    print(f"Results saved to: {output_path}")
    return output_path


def run_complete_sentiment_analysis(csv_path=None):
    """Run complete sentiment analysis pipeline"""
    print("STARTING GOJEK APP SENTIMENT ANALYSIS")
    print("=" * 60)

    # Use provided path or default to Gojek dataset
    if not csv_path:
        csv_path = Path(__file__).parent.parent / 'data' / 'gojek.csv'

    # Step 1: Load reviews
    reviews_df = load_reviews(csv_path)

    # Step 2: Analyze sentiment
    reviews_df = analyze_sentiment(reviews_df)

    # Step 3: Calculate statistics
    stats = calculate_sentiment_statistics(reviews_df)

    # Step 4: Create visualization
    create_sentiment_visualizations(reviews_df)

    # Step 5: Save results
    save_results_to_csv(reviews_df)

    print(f"\nSENTIMENT ANALYSIS COMPLETED!")
    print("=" * 60)
    print(f"All outputs saved to: {OUTPUT_DIR}")
    print("Generated files:")
    print("  - sentiment_distribution.png")
    print("  - sentiment_results.csv")

    return reviews_df, stats


def main():
    """Main function to run sentiment analysis"""
    run_complete_sentiment_analysis()


if __name__ == "__main__":
    main()
