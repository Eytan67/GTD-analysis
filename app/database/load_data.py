import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import POSTGRES_URL, POSTGRES_DB, AAA
from app.models import Base
import logging
import psycopg2
path = r'C:\Users\eytan zichel\PycharmProjects\spark\GTD-analysis\app\database\gdt-1000rows.csv'

df = pd.read_csv(path, encoding='ISO-8859-1')

relvant = df[['eventid', 'iyear', 'imonth', 'iday', 'region', 'country_txt',
              'city', 'latitude', 'longitude', 'attacktype1_txt', 'targtype1_txt',
              'gname', 'nkill', "nwound"]]

engine = create_engine(POSTGRES_URL)
session_maker = sessionmaker(bind=engine)



def is_database_exist(db_name: str) -> bool:
    """Check if database exists"""
    engine1 = create_engine(AAA)
    with engine1.connect() as connection:
        try:
            result = connection.execute(text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'"))
            if result.fetchone():
                return True
            else:
                return True
        except OperationalError as e:
            logging.info("Error connecting to PostgreSQL:", e)


def init_db():
    """Initialize the database by creating all tables"""
    if not is_database_exist(POSTGRES_DB):
        engine1 = create_engine(AAA)
        with engine1.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(text(f"CREATE DATABASE {POSTGRES_DB}"))
            logging.info(f"Database '{POSTGRES_DB}' created successfully.")
    try:
        is_database_exist(POSTGRES_DB)
        Base.metadata.create_all(engine)
        logging.info("Successfully created database tables")
        # Base.metadata.drop_all(bind=engine)
        # logging.info("Successfully drop database tables")
        # with session_maker() as session:
        #     if session.query(Incident).count() == 0:
        #         initial_incident = Incident(
        #             incident_id=uuid.uuid4(),
        #             created_by="system_init",
        #             created_at=datetime.now(),
        #             description="Initial incident for testing",
        #             message="System initialization"
        #         )
        #         session.add(initial_incident)
        #
        #         initial_participant = IncidentParticipant(
        #             incident_id=initial_incident.incident_id,
        #             person_id="init_person_001",
        #             status=False,
        #             details="Initial participant for testing"
        #         )
        #         session.add(initial_participant)
        #
        #         try:
        #             session.commit()
        #             logging.info("Successfully added initial data to tables")
        #         except IntegrityError as e:
        #             session.rollback()
        #             logging.warning(f"Initial data already exists: {e}")
        #     else:
        #         logging.info("Database already contains data, skipping initialization")

    except Exception as e:
        logging.error(f"Failed to initialize database: {e}", exc_info=True)
        raise

init_db()
# print(is_database_exist(POSTGRES_DB))
#
# for index, row in relvant.iterrows():
#     try:
#         obj = Event.from_df(row)
#         print(obj)
#     except ValueError as e:
#         print(f"Error processing row {index}: {e}")