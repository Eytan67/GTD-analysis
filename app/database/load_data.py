import logging

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text, func
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from app.config import POSTGRES_URL, POSTGRES_DB
from app.models import Base
from app.models.event import Event


def create_engine_for_postgres(url, dbname=None):
    if dbname is None:
        engine_url = url
    else:
        engine_url = f'{url}/{dbname}'
    print(engine_url)
    engine = create_engine(engine_url)
    return engine

def is_database_exist(engine, db_name: str) -> bool:
    """Check if database exists"""
    with engine.connect() as connection:
        try:
            result = connection.execute(text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'"))
            if result.fetchone():
                return True
            else:
                return False
        except OperationalError as e:
            logging.info("Error connecting to PostgreSQL:", e)

engine = None
session_maker = None

def init_db():
    """Initialize the database by creating all tables"""
    global engine, session_maker
    engine= create_engine_for_postgres(POSTGRES_URL)
    if not is_database_exist(engine, POSTGRES_DB):
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(text(f"CREATE DATABASE {POSTGRES_DB}"))
            logging.info(f"Database '{POSTGRES_DB}' created successfully.")
    engine = create_engine_for_postgres(POSTGRES_URL, POSTGRES_DB)
    session_maker = sessionmaker(bind=engine)
    try:
        Base.metadata.drop_all(bind=engine)
        logging.info("Successfully drop database tables")
        Base.metadata.create_all(engine)
        logging.info("Successfully created database tables")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}", exc_info=True)
        raise

def load_data_in_chunks(data_frame: DataFrame, chunk_size: int = 1000):
    try:
        for start_row in range(0, len(data_frame), chunk_size):
            chunk = data_frame.iloc[start_row:start_row + chunk_size]

            with session_maker() as session:
                try:
                    chunk_records = [Event.from_df(row[1]) for row in chunk.iterrows()]
                    session.add_all(chunk_records)
                    session.commit()
                    print(f"Loaded rows {start_row} to {start_row + chunk_size}")
                except Exception as e:
                    session.rollback()
                    print(f"Error loading chunk {start_row} to {start_row + chunk_size}: {e}")
                    raise e
        print("Data loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load data into database: {e}", exc_info=True)


