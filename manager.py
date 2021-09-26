import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)



from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
import ihome


app = ihome.create_app("develop")
manager = Manager(app)

Migrate(app,ihome.db)
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()
