from flask import Flask, render_template, url_for, redirect, request, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from os import path, environ

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

uri = environ.get('MONGODB_URI', 'mongodb://localhost:27017/MyAnime')
client = MongoClient(uri)
db = client.get_default_database()

watched_shows = db.watched_shows
current_shows = db.current_shows
future_shows = db.future_shows
users = db.users

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/login', methods=['POST'])
def check_user():
    if session.get('email'):
        return redirect(url_for('user_shows'))

    email = users.find_one({'email': request.form.get('email')})
    password = users.find_one({'password': request.form.get('password')})
    if not email or not password:
        flash('Please enter correct email and/or password', 'danger')
        return redirect(url_for('login'))

    session['email'] = email.get('email', 'danger')
    return redirect(url_for('user_shows'))

@app.route('/signup')
def sign_up():
    return render_template('sign_up.html')

@app.route('/newUser', methods=['POST'])
def user_new():
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if users.find_one({'email': email}):
        flash('That email is already in use. Please use another', 'info')
        return redirect(url_for('sign_up'))
    elif users.find_one({'username': username}):
        flash('That username is already in use. Please use another', 'info')
        return redirect(url_for('sign_up'))

    user = {
        'name': name,
        'email': email,
        'username': username,
        'password': password
    }
    users.insert_one(user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/myshows')
def user_shows():
    return render_template('my_shows.html', watched_shows=watched_shows.find(), current_shows=current_shows.find(), future_shows=future_shows.find(), user=users.find_one({'email': session.get('email')}))

@app.route('/watchedshows/new')
def new_watched_show():
    return render_template('new_watched_show.html')

@app.route('/watchedshows', methods=['GET', 'POST'])
def submit_watched_show():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for(new_watched_show))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for(new_watched_show))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    
    watched_show = {
            'image': file.filename,
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
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for(new_watched_show))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for(new_watched_show))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    current_show = {
            'image': file.filename,
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
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for(new_watched_show))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for(new_watched_show))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    future_show = {
            'image': file.filename,
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