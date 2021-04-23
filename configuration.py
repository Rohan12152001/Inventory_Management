import os

class DB:
    host = 'localhost'
    database = 'Inv_management'
    user = 'root'
    password = str(os.environ.get('IplDbPass'))
    secretKey = str(os.environ.get('flaskKey'))



