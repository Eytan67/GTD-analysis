import pandas as pd
from flask import Blueprint, jsonify, request
from sqlalchemy import func

from app.database.load_data import session_maker
from app.models.event import Event


def find_deadliest_attack_style():
    with session_maker() as session:
        try:
            results = session.query(
                Event.attack_type,
                func.sum(func.coalesce(Event.n_kill, 0)).label('total_kills'),
                func.sum(func.coalesce(Event.n_wound, 0)).label('total_wounds')
            ).group_by(Event.attack_type).all()

            df = pd.DataFrame(results, columns=['Attack_Type', 'Total_Kills', 'Total_Wounds'])
            df['Calculated_Column'] = (df['Total_Kills'] * 2) + df['Total_Wounds']
            sorted_df = df.sort_values(by='Calculated_Column', ascending=False)
            return sorted_df
        except Exception as e:
            print(f"An error occurred: {e}")



analysis_bp = Blueprint('analysis', __name__)

# 1.
@analysis_bp.route('/deadliest', methods=['GET'])
def deadliest_attack_style():
    res = find_deadliest_attack_style()
    limit = request.args.get('limit', default=None)
    if limit:
        res = res.head(5)
    res_json = res.to_dict('records')

    return jsonify(res_json)