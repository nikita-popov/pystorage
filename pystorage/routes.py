import os

from datetime import datetime
from flask import (
    Blueprint,
    current_app,
    flash,
    render_template,
    redirect,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename


bp = Blueprint("main", __name__)


def login_required(f):
    """Authorization decorator"""
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in current_app.config['USERS'] and current_app.config['USERS'][username] == password:
            session['username'] = username
            path = f"{current_app.config['UPLOAD_FOLDER']}/{username}"
            os.makedirs(path, exist_ok=True)
            return redirect(url_for('index'))
        return render_template('login.html', error='Wrong credentials')

    # GET
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.login'))


@bp.route('/')
@login_required
def index():
    upload = f"{current_app.config['UPLOAD_FOLDER']}/{session['username']}"
    files = []
    for filename in os.listdir(upload):
        path = os.path.join(upload, filename)
        if os.path.isfile(path):
            files.append({
                'name': filename,
                'size': os.path.getsize(path),
                'upload_date': datetime.fromtimestamp(os.path.getctime(path)),
            })
    return render_template('index.html', files=files)


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return render_template('upload.html', error='Empty file')

    if file:
        filename = secure_filename(file.filename)
        upload = f"{current_app.config['UPLOAD_FOLDER']}/{session['username']}"
        file.save(os.path.join(upload, filename))
        return redirect(url_for('index'))


@bp.route('/download/<filename>')
@login_required
def download(filename):
    return send_from_directory(
        f"{current_app.config['UPLOAD_FOLDER']}/{session['username']}",
        filename,
        as_attachment=True
    )


@bp.route('/delete/<filename>', methods=['POST'])
@login_required
def delete(filename):
    uploads = f"{current_app.config['UPLOAD_FOLDER']}/{session['username']}"
    file_path = os.path.join(uploads, filename)

    if not os.path.exists(file_path):
        flash('File not found', 'error')
    else:
        try:
            os.remove(file_path)
            flash('File successfully deleted', 'success')
        except Exception as e:
            flash(f'Error deleting file: {str(e)}', 'error')

    return redirect(url_for('main.index'))
