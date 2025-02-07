from flask import Flask, render_template,g
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import json

def read_json_file(filename):
    """Reads a JSON file and returns its contents as a dictionary."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' is not a valid JSON file.")
        return None
    
def remove_backslashes(data):
    """Recursively removes all '\' characters from strings in dictionaries and lists."""
    if isinstance(data, dict):
        return {key: remove_backslashes(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [remove_backslashes(item) for item in data]
    elif isinstance(data, str):
        return data.replace("\\", "")
    else:
        return data

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(None)

    # This tells flask recognize X-Forwarded-Proto headers
    # So it knows what url to use for redirects
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    rawdata = read_json_file("schedule.json")
    app.config['SCHEDULE_DATA'] = remove_backslashes(rawdata)


    with app.app_context():

        from .schedule import routes as registration_routes
        app.register_blueprint(registration_routes.registration_bp)

        @app.errorhandler(404)
        def page_not_found(e):
            return "<h1>404</h1><p>The resource could not be found.</p>", 404
            # return render_template('404.jinja2'), 404

        return app