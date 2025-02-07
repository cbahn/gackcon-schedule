from flask import Blueprint, render_template, g, current_app
import json

registration_bp = Blueprint(
    'schedule',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@registration_bp.route('/')
def index():
    schedule_data = current_app.config.get("SCHEDULE_DATA")
    return render_template('schedule.jinja', schedule_data=schedule_data)

@registration_bp.route('/jsondump')
def jsondump():
    schedule_data = current_app.config.get("SCHEDULE_DATA")
    return json.dumps(schedule_data, indent=2)