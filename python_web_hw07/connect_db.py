import configparser

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker


config = configparser.ConfigParser()
config.read("config.ini")

driver_sync = config.get('DB', 'driver_sync')
driver_async = config.get('DB', 'driver_async')
user = config.get('DB', 'user')
password = config.get('DB', 'password')
host = config.get('DB', 'host')
port = config.get('DB', 'port')
dbname = config.get('DB', 'dbname')

url = f"{driver_sync}://{user}:{password}@{host}:{port}/{dbname}"

engine: AsyncEngine = create_async_engine(f"{driver_sync}+{driver_async}://{user}:{password}@{host}:{port}/{dbname}", echo=False)
AsyncDBSession = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
