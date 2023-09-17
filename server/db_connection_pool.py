import config
from pymysqlpool import ConnectionPool


class DbConnectionPool:
    _instance = None

    def __init__(self):
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = ConnectionPool(
                size=2,
                pre_create_num=2,
                host=config.customhost,
                port=3306,
                user=config.customuser,
                password=config.custompass,
                db=config.customdb,
            )

        return cls._instance
