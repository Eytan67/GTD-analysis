from flask import Flask, render_template_string
from app.routes.analysis_routes import analysis_bp

app = Flask(__name__)

app.register_blueprint(analysis_bp, url_prefix='/api')
@app.route('/')
def index():
    routes = [
        '/api/deadliest',
        '/api/most_aggressive',
        '/api/victims_by_region',
        '/api/change_percent_by_region',
        '/api/top_5_by_country_region'
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
    app.run(host='0.0.0.0', port=5000,
            debug=True)