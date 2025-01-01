from flask import Flask, render_template, jsonify, url_for
from hello import fetch_news  # Assuming fetch_news is in hello.py

# Define categories and their corresponding RSS feeds (place this at the beginning of your app.py)
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

app = Flask(__name__, template_folder='templates', static_folder='templates')

@app.route('/news/<category>')  # Dynamic route for categories
def news_by_category(category):
    try:
        if category not in categories:
            raise ValueError(f"Invalid category: {category}")

        articles = fetch_news(category)  # Call fetch_news with category
        return jsonify(articles)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400  # Handle invalid category

@app.route('/')
def index():
    # Pass category options to the template (optional)
    category_options = list(categories.keys())
    return render_template('index.html', category_options=category_options)

if __name__ == '__main__':
    app.run(debug=True)
