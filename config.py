# WebAPI Configuration File

class Config:
    SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://iqms:zeigler17@iqora'

    @staticmethod
    def init_app(app):
        pass

config = Config
