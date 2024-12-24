from datetime import datetime
from pandas import DataFrame



def clean_data(data_frame:DataFrame)->DataFrame:
    data_frame = clean_year(data_frame)
    data_frame['imonth'] = clean_month(data_frame['imonth'])
    data_frame['day'] = clean_day(data_frame['day'])
    return data_frame

def clean_year(data_frame:DataFrame, start_year = 1900, end_year = datetime.now().year):
    data_frame = data_frame[(data_frame['iyear'] >= start_year) & (data_frame['iyear'] <= end_year)]
    return data_frame
def clean_month(month_column):
    month_column = month_column.where((month_column >= 1) & (month_column <= 12), None)
    return month_column
def clean_day(day_column):
    day_column = day_column.where((day_column >= 1) & (day_column <= 31), None)
    return day_column
def clean_region(region_column):
    return region_column
def clean_country(country_column):
    return country_column
def clean_latitude(lat_column):
    return lat_column
def clean_longitude(long_column):
    return long_column
def clean_attacktype(attacktype_column):
    return attacktype_column
def clean_targettype(targettype_column):
    return targettype_column
def clean_gname(gname_column):
    return gname_column
def clean_nperps(nperps_column):
    return nperps_column
def clean_nkill(nkill_column):
    return nkill_column
def clean_nwound(nwound_column):
    return nwound_column