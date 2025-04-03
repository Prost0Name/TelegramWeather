from tortoise import Tortoise 

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://sqlite/user.db",
    },
    "apps": {
        "models_users": {
            "models": ["database.models"],
            "default_connection": "default",
        },
    },
}


async def setup():
    await Tortoise.init(config=TORTOISE_ORM, _create_db=True)
    await Tortoise.generate_schemas()