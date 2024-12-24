import pandas as pd


path = r'/app/data/csv1-1000.csv'

df = pd.read_csv(path, encoding='ISO-8859-1')
relevant_columns = ['eventid', 'iyear', 'imonth', 'iday', 'region', 'country_txt',
              'city', 'latitude', 'longitude', 'attacktype1_txt', 'targtype1_txt',
              'gname', 'nkill', "nwound"]

relevant_data = df[relevant_columns]


