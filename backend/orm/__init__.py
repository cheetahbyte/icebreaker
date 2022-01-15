from tortoise import Tortoise


async def init() -> None:
    """initialize the database"""
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={
            "models": ["orm.models"],
        },
    )
    await Tortoise.generate_schemas()