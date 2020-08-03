from config import DevelopmentConfig
from tortoise.contrib.quart import register_tortoise
from tortoise import Tortoise
from quart import Quart
app = Quart(__name__)

app.config.from_object(DevelopmentConfig)

register_tortoise(
    app, db_url=DevelopmentConfig.DATABASE_URI, modules={"models": ["app.models"]}, generate_schemas=True
)
from app.views import deep, neutral

app.register_blueprint(deep)
app.register_blueprint(neutral)

if __name__ == '__main__':
    app.run()



