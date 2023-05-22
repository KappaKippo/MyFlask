from flask import redirect, Flask, url_for, render_template, request, flash
from werkzeug.utils import secure_filename
import json
import os


UPLOAD_FOLDER = 'C:\\Users\\bekas\\Downloads'
ALLOWED_EXTENSIONS = {'json', 'zip'}

app = Flask(__name__)
host = 'http://10.10.4.15:5000'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# link to home page redirecting to flask_page function
@app.route('/')
def home():
    return f'''<a href={host}{url_for("flask_page")}>Flask Page</a><p>\n</p>
               <a href={host}{url_for("projects")}>Projects</a><p>\n</p>
               <a href={host}{url_for("about")}>About</a><p>\n</p>
               <a href={host}{url_for("profile")}>User/ a name</a><p>\n</p>
               <a href={host}{url_for("upload_file")}>Upload File</a>'''


# home button
def home_button():
    return f'<a href={host}{url_for("home")}>Home</a>'


# imprints text
def text_func(text):
    text = f'<p>{text}</p>\n'
    return text


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# printing text
@app.route('/flask')
def flask_page():
    return f'{text_func("Flask!!!")}' \
           f'{home_button()}'


# typing /projects or /projects/ will work as expected
@app.route('/projects/')
def projects():
    return f'<p>The Project Page</p>\n' \
           f'{home_button()}'


# typing /about will work, typing /about/ will not
@app.route('/about')
def about():
    return f'<p>The about Page</p>\n' \
           f'{home_button()}'


# using variable and html file
@app.route('/user/')
@app.route('/user/<username>/')
def profile(username=None):
    # rendering templates
    return f"{render_template('hello.html', name=username)}" \
           f"{render_template('greeting.html')}<p>\n" \
           f"{home_button()}"


# using type converter
@app.route('/profile/<int:profile_id>/')
def id_profile(profile_id):
    return f'Profile id {profile_id}'


# receiving json data through http POST requests
@app.route('/data/', methods=['POST'])
def process_data():
    content_type = request.headers['Content-Type']
    if content_type == 'application/json':
        json_data = request.get_json()
        with open('data.json', 'w') as f:
            json.dump(json_data, f)
        return 'JSON data received'
    else:
        return 'Unsupported media type', 415


# receiving json files through http POST requests
@app.route('/file/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return f'{render_template("upload_file.html")}<p>\n</p>' \
           f'{home_button()}'


with app.test_request_context():
    print('Home Page:', url_for('home'))
    print('Profile Page:', url_for('profile'))
    print('Flask Page:', url_for('flask_page'))
    print('Projects Page:', url_for('projects'))
    print('About Page:', url_for('about'))
    print('JSON data endpoint:', url_for('process_data'))
