import os

from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    send_from_directory,
    url_for,
)
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
# from werkzeug.security import check_password_hash

basic_auth = HTTPBasicAuth()

bp = Blueprint("api", __name__)


@basic_auth.verify_password
def verify_basic_auth(username, password):
    if username in current_app.config['USERS'] and current_app.config['USERS'][username] == password:
        uploads = f"{current_app.config['UPLOAD_FOLDER']}/{username}"
        os.makedirs(uploads, exist_ok=True)
        return username
    return None


@basic_auth.error_handler
def basic_auth_error(status):
    return {"error": "Basic Auth failed"}, status


@bp.route('/api/files', methods=['GET'])
@basic_auth.login_required
def api_files():
    files = []
    uploads = f"{current_app.config['UPLOAD_FOLDER']}/{basic_auth.current_user()}"
    for filename in os.listdir(uploads):
        path = os.path.join(uploads, filename)
        if os.path.isfile(path):
            files.append({
                "name": filename,
                "size": os.path.getsize(path),
                "url": url_for('api.download', filename=filename, _external=True)
            })
    return jsonify({"files": files})


@bp.route('/api/upload', methods=['POST'])
@basic_auth.login_required
def api_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        uploads = f"{current_app.config['UPLOAD_FOLDER']}/{basic_auth.current_user()}"
        filename = secure_filename(file.filename)
        file.save(os.path.join(uploads, filename))
        return jsonify({
            "status": "success",
            "filename": filename,
            "url": url_for('api.api_download', filename=filename, _external=True)
        }), 201


@bp.route('/api/download/<filename>', methods=['GET'])
@basic_auth.login_required
def api_download(filename):
    return send_from_directory(
        f"{current_app.config['UPLOAD_FOLDER']}/{basic_auth.current_user()}",
        filename,
        as_attachment=True
    )


@bp.route('/api/delete/<filename>', methods=['DELETE'])
@basic_auth.login_required
def api_delete(filename):
    uploads = f"{current_app.config['UPLOAD_FOLDER']}/{basic_auth.current_user()}"
    file_path = os.path.join(uploads, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    os.remove(file_path)
    return jsonify({"status": "success", "message": f"{filename} deleted"})
