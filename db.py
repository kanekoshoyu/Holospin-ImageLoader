from pymongo import MongoClient
from enum import Enum
import io


class DataBaseType(Enum):
    Order = 1,


def get_collection(db_type: DataBaseType):
    # db_address = 'localhost'
    # db_address = '127.0.0.1'
    # db_address = '192.168.50.100'
    db_address = 'ttcshenzhen.asuscomm.com'
    # db_port = 27027 # Sho's ITX
    db_port = 27017  # TTC SZ NUC

    try:
        conn = MongoClient(db_address, db_port)
        print("Connected to MongoDB")
    except:
        print("Could not connect to MongoDB")

    # database
    db = conn.database
    # Pattern Matching only in Python 3.10
    if db_type == DataBaseType.Order:
        return db.holo_spinner_order_sandbox_1

    return False


def list_collection(db_type: DataBaseType):
    cursor = get_collection(db_type).find()
    for record in cursor:
        print(record, "\r\n")


def make_pcba_entry(pix_array):
    r = {
        "pix_array": pix_array
    }
    return r
