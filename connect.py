from beanie import init_beanie
from motor.motor_asyncio import  AsyncIOMotorClient
from typing import Optional
from pydantic_settings import BaseSettings

from model import Todo


#beanie, pydantic-settings 설치함

class Settings(BaseSettings):
    databaseu_url: Optional[str] = 'mongodb://yong:yong@localhost:27017'

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.databaseu_url)
        db = client.get_database('todo')
        await init_beanie(database=db, document_models=[Todo])

# await 있을때만 앞에 async가 앞에 붙어있으면 된다 동기-비동기 관련된거 찾아보기를