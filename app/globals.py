from flask import g
def init_app(app):
    with app.app_context():
        app.config['loginUserArray'] = {}