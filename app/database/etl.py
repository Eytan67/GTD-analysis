from app.database.data_cleaning import clean_data
from app.database.extract_data import relevant_data
from app.database.init_db import init_db, load_data_in_chunks



def etl():
    data = relevant_data
    data = clean_data(data)
    init_db()
    load_data_in_chunks(data, 200)