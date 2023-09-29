import configparser

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker


config = configparser.ConfigParser()
config.read("config.ini")

username = config.get('DB', 'user')
password = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

URL = f'postgresql+asyncpg://{username}:{password}@{domain}:5432/{db_name}'

engine: AsyncEngine = create_async_engine(URL, echo=False)
AsyncDBSession = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
