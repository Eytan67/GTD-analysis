import pandas as pd
from sqlalchemy import func
from app.database.init_db import session_maker
from app.models.event import Event
from app.yotils.region_coordinates_map import regions_coordinates_map



def find_deadliest_attack_style():
    with session_maker() as session:
        try:
            results = session.query(
                Event.attack_type,
                func.sum(func.coalesce(Event.n_kill, 0)).label('total_kills'),
                func.sum(func.coalesce(Event.n_wound, 0)).label('total_wounds')
            ).group_by(Event.attack_type).all()

            df = pd.DataFrame(results, columns=['Attack_Type', 'Total_Kills', 'Total_Wounds'])
            df['score'] = (df['Total_Kills'] * 2) + df['Total_Wounds']
            sorted_df = df.sort_values(by='score', ascending=False)
            return sorted_df
        except Exception as e:
            print(f"An error occurred: {e}")

def find_average_casualties_by_region():
    with session_maker() as session:
        try:
            results = session.query(
                Event.region,
                (func.sum(func.coalesce(Event.n_kill, 0)) * 2 + func.sum(func.coalesce(Event.n_wound, 0))).label('score'),
                func.count()
            ).group_by(Event.region).all()
            df = pd.DataFrame(results, columns=['region', 'score', 'count'])
            df['score_per_count'] = df['score'] / df['count']

            return df[['region', 'score_per_count']]
        except Exception as e:
            print(f"An error occurred: {e}")

def find_most_aggressive_groups():
    with session_maker() as session:
        try:
            results = session.query(
                Event.g_name,
                func.sum(func.coalesce(Event.n_kill, 0)).label('total_kills'),
                func.sum(func.coalesce(Event.n_wound, 0)).label('total_wounds')
            ).group_by(Event.g_name).all()

            df = pd.DataFrame(results, columns=['g_name', 'total_kills', 'total_wounds'])
            df['score'] = df['total_kills'] + df['total_wounds']
            sorted_df = df.sort_values(by='score', ascending=False)
            return sorted_df
        except Exception as e:
            print(f"An error occurred: {e}")

def find_change_percent_by_region():
    with session_maker() as session:
        try:
            results = session.query(
                Event.region,
                Event.year,
                func.count(Event.id).label('count')
            ).group_by(Event.region, Event.year).all()
            df = pd.DataFrame(results, columns=['region', 'year', 'count'])
            df = df.sort_values(by=['region', 'year'])
            df['change'] = df.groupby('region')['count'].pct_change() * 100
            avg_change = df.groupby('region')['change'].mean().reset_index()
            return avg_change
        except Exception as e:
            print(f"An error occurred: {e}")

def find_top_5_by_region(region=None):
    with session_maker() as session:
        try:
            results = session.query(
                Event.region,
                Event.g_name,
                func.count(Event.id).label('count')
            ).group_by(Event.region, Event.g_name).order_by(Event.region, func.count(Event.id).desc()).all()
            df = pd.DataFrame(results, columns=['region', 'group name', 'count'])
            df = df[df['group name'] != 'Unknown']
            df = df[df['group name'] != 'Other']
            df = df.groupby('region').apply(lambda x: x.nlargest(5, 'count')).reset_index(drop=True)
            result = []

            for region, group_df in df.groupby('region'):
                groups = group_df[['group name', 'count']].to_dict(orient='records')
                latitude = regions_coordinates_map[int(region)][0]
                longitude = regions_coordinates_map[int(region)][1]
                region_json = {
                    'region': region,
                    'latitude': latitude,
                    'longitude': longitude,
                    'groups': groups
                }

                result.append(region_json)

            print(result)

            # if region:
            #     result = result[result['region'] == region]
            return result
        except Exception as e:
            print(f"An error occurred: {e}")