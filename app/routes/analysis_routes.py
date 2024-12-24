from flask import Blueprint, jsonify, request, render_template, render_template_string
import folium
from app.ripository.querys import *



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

# 2.
@analysis_bp.route('/victims_by_region', methods=['GET'])
def average_casualties_by_region():
    res = find_average_casualties_by_region()

    limit = request.args.get('limit', default=None)
    if limit:
        res = res.head(5)

    res_json = res.to_dict('records')

    return jsonify(res_json)

# 3.
@analysis_bp.route('/most_aggressive', methods=['GET'])
def most_aggressive_groups():
    res = find_most_aggressive_groups().head(5).to_dict('records')

    return jsonify(res)

# 6.
@analysis_bp.route('/change_percent_by_region', methods=['GET'])
def change_percent_by_region():
    res = find_change_percent_by_region()

    limit = request.args.get('limit', default=None)
    if limit:
        res = res.head(5)

    res_json = res.to_dict('records')
    return jsonify(res_json)

# 8.
@analysis_bp.route('/top_5_by_country_region', methods=['GET'])
def top_5_by_region():
    region = request.args.get('region', default=None)
    response = find_top_5_by_region(region)

    map = folium.Map(location=[31.7683, 35.2137], zoom_start=7)

    for loc in response:
        if loc["latitude"] and loc["longitude"]:
            popup_html = """
                <div style="font-family: Arial, sans-serif; color: #333;">
                    <h3 style="color: #0073e6; text-align: center;">Groups Information</h3>
                    <ul style="list-style-type: none; padding: 0;">
            """
            for group in loc["groups"]:
                popup_html += f"""
                    <li style="padding: 8px; border-bottom: 1px solid #ddd;">
                        <strong style="color: #333;">{group['group name']}</strong>: <span style="color: #0073e6;">{group['count']}</span> attacks
                    </li>
                """
            popup_html += """
                    </ul>
                </div>
            """
            folium.Marker([loc["latitude"], loc["longitude"]], popup=folium.Popup(popup_html, max_width=300)).add_to(map)

    map_html = map._repr_html_()

    return render_template_string('''
           <html>
               <body>
                   <h1>Top 5 by Region Map</h1>
                   {{ map_html|safe }}
               </body>
           </html>
       ''', map_html=map_html)
