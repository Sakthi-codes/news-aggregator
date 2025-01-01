import feedparser
import logging

def fetch_news(category=None):
    """Fetches news articles from multiple RSS feeds, optionally filtered by category.

    Args:
        category (str, optional): The name of the category to filter articles by.
            Defaults to None (all categories).

    Returns:
        A list of dictionaries, where each dictionary represents a news article
        containing the following keys:
            - title: The title of the news article.
            - description: A summary of the news article.
            - link: The URL of the news article.
            - author (optional): The author of the news article (if available).
            - source: The URL of the RSS feed from which the article was fetched.
    """

    # Define categories and their corresponding RSS feed URLs
    categories = {
        "Business": [
            "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
            "https://cfo.economictimes.indiatimes.com/rss/corporate-finance",
            "https://cfo.economictimes.indiatimes.com/rss/strategy-operations"
        ],
        "Technology": [
            "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
            "https://cfo.economictimes.indiatimes.com/rss/cfo-tech",
            "https://www.techcrunch.com/feed/"
        ],
        "World News": [
            "https://rss.nytimes.com/services/xml/rss/nyt/International.xml",
            "https://www.bbc.co.uk/news/world/rss.xml"
        ]
    }

    # Handle invalid categories
    if category and category not in categories:
        raise ValueError(f"Invalid category: {category}")

    feed_items = []
    for category_name, feed_urls in categories.items():
        if category is None or category_name == category:  # Filter by category if provided
            for url in feed_urls:
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries:
                        item = {
                            "title": entry.title,
                            "description": entry.summary,
                            "link": entry.link,
                            "author": entry.author if hasattr(entry, 'author') else None,
                            "source": url
                        }
                        feed_items.append(item)
                except feedparser.ParseError as e:
                    logging.error(f"Error parsing feed from {url}: {e}")
                except Exception as e:
                    logging.exception(f"Error fetching from {url}: {e}")

    return feed_items

if __name__ == "__main__":
    # Fetch all categories (optional for debugging)
    all_articles = fetch_news()
    # for item in all_articles:
    #     print(item)

    # Fetch articles from a specific category (e.g., "Business")
    business_articles = fetch_news(category="Business")
    # for item in business_articles:
    #     print(item)
