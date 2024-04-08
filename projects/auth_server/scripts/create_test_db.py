from src.database import Database
from src.settings import AuthSettings
import asyncio
import os
import sys

"""주의
entity는 아래에 기술해서 BASE가 알수 있게 끔 preloading을 해주어야 한다.
Base에 상속되어 있는 Entity들을 create_database 시에 테이블을 생성하는 데
import 가 안되어 있으면, 존재를 몰라서, 테이블을 생성하지 않는다.
"""
from src.users.repository import UserRepository



if __name__ == '__main__':
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print("test db를 생성합니다.")
        db = Database(AuthSettings(
            db_type=f"sqlite+aiosqlite:///{file_path}",
            private_key=""
        ))
        asyncio.run(db.create_database())