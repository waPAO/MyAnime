from flask import Flask, render_template, url_for, redirect, request, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import urllib.request
import os

client = MongoClient()
db = client.MyAnime

watched_shows = db.watched_shows
current_shows = db.current_shows
future_shows = db.future_shows

app = Flask(__name__)

IMG_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = '/static/uploads/'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def check_img(img_file):
    return '.' in img_file and img_file.rsplit('.', 1)[1].lower() in IMG_EXTENSIONS

@app.route('/')
def index():
    return render_template('home.html')

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
    return redirect(url_for('user_shows'))

@app.route('/futureshow/<futureshow_id>/delete', methods=['POST'])
def delete_charity(futureshow_id):
    future_shows.delete_one({'_id': ObjectId(futureshow_id)})
    return redirect(url_for('user_shows'))



if __name__=='__main__':
    app.run(debug=True)