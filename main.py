from controller.app_controller import AppController
from db.database import init_db

if __name__ == '__main__':
    init_db()

    init_db()
    app = AppController()
    app.run()