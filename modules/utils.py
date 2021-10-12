from datetime import datetime


def snowflake_to_datetime(snowflake: int) -> datetime:
    return datetime.fromtimestamp(((snowflake >> 22) + 1420070400000) / 1000)