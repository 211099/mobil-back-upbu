from app import app

from utils.db import db
from waitress import serve

import os


with app.app_context():
    db.init_app(app)
    db.create_all()
    print('creado')

if __name__ == "__main__":
    # app.run(debug=True)
     serve(app, host='0.0.0.0', port=os.getenv("PORT", default=5000))
 
