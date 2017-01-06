from config import config
from webapi import app

app.config.from_object(config)
# app.config.from_envvar('WEBAPI_SETTINGS')
config.init_app(app)

if __name__ == "__main__":
    app.run()
