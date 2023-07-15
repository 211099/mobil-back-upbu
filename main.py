from app import app

from utils.db import db

with app.app_context():
    db.init_app(app)
    db.create_all()
    print('creado')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
 
