from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from sqlalchemy.orm import Session

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views in session if not present
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views by 1 for every request
    session['page_views'] += 1

    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:
        with Session(db.engine) as db_session:
            article = db_session.get(Article, id)
            if article:
                return jsonify({
                    'author': article.author,
                    'title': article.title,
                    'content': article.content,
                    'preview': article.preview,
                    'minutes_to_read': article.minutes_to_read,
                    'date': article.date
                })

    # If the user has viewed more than 3 pages, return a 401 unauthorized response
    return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
