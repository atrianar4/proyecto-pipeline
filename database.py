from pymongo import MongoClient
import certifi 

MONGO_URI = 'mongodb+srv://juan:jlozano123@cluster0.lhonrj1.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAfile=ca)
        db = client["Pipeline"]
    except ConnectionError:
        print('Error de conexion con la base de datos')
    return db     