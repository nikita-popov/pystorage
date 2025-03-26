import os


class Config(object):
    SECRET_KEY = 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    USERS = {
        'admin': 'admin',
        'user': 'qwerty'
    }
