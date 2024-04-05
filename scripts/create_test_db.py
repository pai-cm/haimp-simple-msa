from src.database import Database
from src.settings import AuthSettings
import asyncio


"""주의

entity는 아래에 기술해서 BASE가 알수 있게 끔 preloading을 해주어야 한다.
Base에 상속되어 있는 Entity들을 create_database 시에 테이블을 생성하는 데
import 가 안되어 있으면, 존재를 몰라서, 테이블을 생성하지 않는다.
"""
from src.users import models


if __name__ == '__main__':
    db = Database(AuthSettings(
        db_host="sqlite+aiosqlite:///./test.db",
        private_key=""
    ))
    asyncio.run(db.create_database())