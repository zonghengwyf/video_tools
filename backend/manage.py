import os
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run("0.0.0.0" ,port=80)