import pandas as pd

from app.database.data_cleaning import clean_data
from app.database.extract_data import relevant_data
from app.database.load_data import init_db, load_data_in_chunks

#extract
data = relevant_data

#transform

data = clean_data(data)

#load
init_db()
load_data_in_chunks(data, 200)

def etl():
    data = relevant_data
    data = clean_data(data)
    init_db()
    load_data_in_chunks(data, 200)