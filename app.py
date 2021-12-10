from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.MyAnime

users = db.users
watched_shows = db.watched_shows
current_shows = db.current_shows
future_shows = db.future_shows

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)