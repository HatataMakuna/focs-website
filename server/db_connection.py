import config
from pymysql import Connection

class DbConnection:
    _instance = None

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Connection(
                host=config.customhost,
                port=3306,
                user=config.customuser,
                password=config.custompass,
                db=config.customdb,
            )

        return cls._instance
