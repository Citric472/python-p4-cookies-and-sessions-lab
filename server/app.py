#!/usr/bin/env python3
from flask import Flask, jsonify, session, request
from flask_migrate import Migrate
from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize the database
db.init_app(app)

@app.route('/clear')
def clear_session():
    """Route to clear session data."""
    session['page_views'] = 0
    return jsonify({'message': 'Successfully cleared session data.'}), 200

@app.route('/articles')
def index_articles():
    """Route to list all articles."""
    articles = Article.query.all()  # Query all articles from the database
    articles_list = [article.to_dict() for article in articles]  # Convert articles to JSON-like dictionaries
    
    # Return the list of articles as a JSON response
    return jsonify(articles_list)

@app.route('/articles/<int:id>')
def show_article(id):
    """Route to display an article by its ID."""
    # Initialize page views in session if not already set
    session['page_views'] = session.get('page_views', 0)
    
    # Increment page views
    session['page_views'] += 1
    
    # Check if the user has reached the paywall limit of 3 views
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    
    # Fetch the article from the database using the provided ID
    session_instance = db.session
    article = session_instance.get(Article, id)
    
    if article:
        # Convert the article to a dictionary and return as JSON
        return jsonify(article.to_dict())  # Assuming `to_dict` returns a JSON-like dictionary
    
    # If article is not found, return a 404 error response
    return jsonify({'message': 'Article not found'}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5555, debug=True)

