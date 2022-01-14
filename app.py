from flask import Flask, render_template, url_for, redirect, request, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import urllib.request
import os

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

client = MongoClient()
db = client.MyAnime

watched_shows = db.watched_shows
current_shows = db.current_shows
future_shows = db.future_shows
users = db.users

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def sign_up():
    return render_template('sign_up.html')

@app.route('/myshows')
def user_shows():
    return render_template('my_shows.html', watched_shows=watched_shows.find(), current_shows=current_shows.find(), future_shows=future_shows.find())

@app.route('/watchedshows/new')
def new_watched_show():
    return render_template('new_watched_show.html')

@app.route('/watchedshows', methods=['POST'])
def submit_watched_show():
    watched_show = {
            'image': request.form.get('image'),
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'rating': request.form.get('rating')
        }
    watched_shows.insert_one(watched_show)
    flash(f'{watched_show["title"]} was successfully added to watched shows!')
    return redirect(url_for('user_shows'))

@app.route('/watchedshow/<watchedshow_id>/delete', methods=['POST'])
def delete_watched_show(watchedshow_id):
    watched_shows.delete_one({'_id': ObjectId(watchedshow_id)})
    return redirect(url_for('user_shows'))

@app.route('/currentshows/new')
def new_current_show():
    return render_template('new_current_show.html')

@app.route('/currentshows', methods=['POST'])
def submit_current_show():
    current_show = {
            'image': request.form.get('image'),
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'rating': request.form.get('rating')
        }
    current_shows.insert_one(current_show)
    flash(f'{current_show["title"]} was successfully added to current shows!')
    return redirect(url_for('user_shows'))

@app.route('/currentshow/<currentshow_id>/delete', methods=['POST'])
def delete_currentshow(currentshow_id):
    current_shows.delete_one({'_id': ObjectId(currentshow_id)})
    return redirect(url_for('user_shows'))

@app.route('/futureshows/new')
def new_future_show():
    return render_template('new_future_show.html')

@app.route('/futureshows', methods=['POST'])
def submit_future_show():
    future_show = {
            'image': request.form.get('image'),
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'rating': request.form.get('rating')
        }
    future_shows.insert_one(future_show)
    flash(f'{future_show["title"]} was successfully added to future shows!')
    return redirect(url_for('user_shows'))

@app.route('/futureshow/<futureshow_id>/delete', methods=['POST'])
def delete_show(futureshow_id):
    future_shows.delete_one({'_id': ObjectId(futureshow_id)})
    return redirect(url_for('user_shows'))



if __name__=='__main__':
    app.run(debug=True)