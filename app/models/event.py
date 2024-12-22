import uuid

from sqlalchemy import Column, Integer, String, Float
from app.models import Base

class Event(Base):
    __tablename__ = 'event'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    region = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    n_kill = Column(Float, nullable=False)
    n_wound = Column(Float, nullable=False)
    g_name = Column(String, nullable=True)
    attack_type = Column(String, nullable=True)
    target_type = Column(String, nullable=True)

    @classmethod
    def from_df(cls, row):
        try:
            return cls(
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

