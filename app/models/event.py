from uuid import UUID

from sqlalchemy import Column, Integer, String, Float
from app.models import Base

class Event(Base):
    __tablename__ = 'event'
    id = Column(String, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    region = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    n_kill = Column(Integer, nullable=False)
    n_wound = Column(Integer, nullable=False)
    g_name = Column(String, nullable=True)
    attack_type = Column(String, nullable=True)
    target_type = Column(String, nullable=True)

    @classmethod
    def from_df(cls, row):
        try:
            return cls(
                id=row.get('eventid', UUID),
                year=int(row['iyear']),
                month=row.get('imonth', None),
                day=row.get('iday', None),
                region=row['region'],
                country=row['country_txt'],
                city=row.get('city', None),
                latitude=row.get('latitude', None),
                longitude=row.get('longitude', None),
                n_kill=row.get('nkill', 0),
                n_wound=row.get('nwound', 0),
                g_name=row.get('gname', None),
                attack_type=row.get('attacktype1_txt', None),
                target_type=row.get('targtype1_txt', None)
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e.args[0]}")
        except ValueError as e:
            raise ValueError(f"Error parsing field: {e}")

    def __repr__(self):
        return f"<Event {self.id} >, country {self.country}, city {self.city}"

import pandas as pd

path = r'C:\Users\eytan zichel\PycharmProjects\spark\GTD-analysis\app\database\gdt-1000rows.csv'

df = pd.read_csv(path, encoding='ISO-8859-1')
relvant = df[['eventid', 'iyear', 'imonth', 'iday', 'region', 'country_txt',
              'city', 'latitude', 'longitude', 'attacktype1_txt', 'targtype1_txt',
              'gname', 'nkill', "nwound"]]
for index, row in relvant.iterrows():
    try:
        obj = Event.from_df(row)
        print(obj)
    except ValueError as e:
        print(f"Error processing row {index}: {e}")