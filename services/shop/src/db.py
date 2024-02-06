from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB:
    __instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if DB.__instance is None:
            DB.__instance = super(DB, cls).__new__(cls, *args, **kwargs)
            config = dotenv_values("/.env")

            DB.__instance.engine = create_engine(
                f'mysql+mysqldb://{config["SERV_SHOP_SQL_USER"]}:{config["SERV_SHOP_SQL_PASSWORD"]}@palmon_database_shop:3306/{config["SERV_SHOP_SQL_DATABASE"]}'
            )
        return DB.__instance

    def get(self):
        Session = sessionmaker(bind=self.engine)
        return Session()
