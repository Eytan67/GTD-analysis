from flask import Flask, render_template_string
from app.database.etl import etl
from app.routes.analysis_routes import analysis_bp

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///version10.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# players = grid_data(start_season, end_season)
#
# db.init_app(app)
# with app.app_context():
#     db.create_all()
#     db.session.add_all(players)
#     db.session.commit()


app.register_blueprint(analysis_bp, url_prefix='/api')
@app.route('/')
def index():
    routes = [
        '/api/deadliest',
        '/api/most_aggressive',
        '/api/victims_by_region',
        '/api/change_percent_by_region'
    ]
    return render_template_string('''
        <html>
            <body>
                <h1>Welcome to the API</h1>
                <ul>
                    {% for route in routes %}
                        <li><a href="{{ route }}">{{ route }}</a></li>
                    {% endfor %}
                </ul>
            </body>
        </html>
    ''', routes=routes
    )
if __name__ == '__main__':
    etl()
    app.run(host='0.0.0.0', port=5000,
            debug=True)