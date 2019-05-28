from app import app
import views
import logger_handlers
import user_manage
from mongoengine import connect

if __name__ == "__main__":
    # create all tables in sqlite db
    db.create_all()
    # connect to mongo db
    connect(
        app.config['MONGO_DBNAME'],
        alias='default',
        host=app.config['MONGO_HOST'],
        port=app.config['MONGO_PORT']
    )
    app.run(host="0.0.0.0", port=5000, debug=True)
