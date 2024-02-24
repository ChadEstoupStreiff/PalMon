from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB:
    __instance = None
    __last_session = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if DB.__instance is None:
            DB.__instance = super(DB, cls).__new__(cls, *args, **kwargs)
            config = dotenv_values("/.env")

            DB.__instance.engine = create_engine(
                f'mysql+mysqldb://{config["SERV_EGGS_SQL_USER"]}:{config["SERV_EGGS_SQL_PASSWORD"]}@palmon_database_eggs:3306/{config["SERV_EGGS_SQL_DATABASE"]}'
            )
        return DB.__instance

    def get(self):
        if self.__last_session is not None:
            self.__last_session.commit()
            self.__last_session.close()
            self.__last_session.close_all()
        Session = sessionmaker(bind=self.engine)
        self.__last_session = Session()
        return self.__last_session
