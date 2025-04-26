import os
from datetime import datetime
from flask import Blueprint, request, render_template, abort, flash, redirect, url_for
from werkzeug.exceptions import HTTPException
from app.api import functionality as api_func
from app.gui import functionality as gui_func
from app.constants import Information as Const

bp_gui = Blueprint('bp_gui', __name__, url_prefix='/gui', template_folder='templates', static_folder=os.path.join(os.path.dirname(__file__), 'static'), static_url_path='/bp_gui/static')
chat_log = []  # Temporary in-memory storage


@bp_gui.route('/playground', methods=['GET'])
def test():
    return render_template('test.html')


@bp_gui.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@bp_gui.route('/', methods=['GET'])
@bp_gui.route('/home', methods=['GET'])
def home():
    project_details: list = []
    current_datetime = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    my_information_list = api_func.get_my_info()
    experience_info = my_information_list['myInformation']['myIndustryExperiences']
    about_me_info = my_information_list['myInformation']['aboutMe']
    expertise_info = my_information_list['myInformation']['myExpertise']
    projects_to_display = my_information_list['myInformation']['topDisplayProjectIdentifiers'].split(',')
    for project_id in projects_to_display:
        project_details.append(api_func.get_project_summary(filter_parameters=project_id)[0])
    return render_template('index.html', author=Const.AUTHOR, version=Const.VERSION, experience=experience_info, about_me=about_me_info, my_projects=project_details, my_expertise=expertise_info, current_date_time=current_datetime)


@bp_gui.route('/explore', methods=['GET'])
def explore_projects():
    project_details = api_func.get_project_summary(filter_parameters='')
    return render_template('explore_projects.html', author=Const.AUTHOR, version=Const.VERSION, my_projects=project_details)


@bp_gui.route('/project-details', methods=['GET'])
def project_details():
    try:
        project_id = request.args.get('projectIdentifier')
        random_project_ids = gui_func.choose_random_project(int(project_id))
        if api_func.project_exists(project_id=project_id):
            extended_project_data = api_func.get_project_details(project_id=project_id)
            random_project_details = api_func.get_project_summary(random_project_ids)
            return render_template('project_details.html', author=Const.AUTHOR, version=Const.VERSION, project_data=extended_project_data, random_projects=random_project_details)
        else:
            abort(404)
    except Exception as error:
        abort(404, description=str(error))


@bp_gui.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        message_name = request.form['username']
        message_email = request.form['email']
        message_subject = request.form['subject']
        message_body = request.form['message']
        message_json = {
            "name": message_name,
            "emailAddress": message_email,
            "messageSubject": message_subject,
            "messageBody": message_body
        }
        response_json = api_func.add_message(json_input=message_json)
        flash('Your message has been sent successfully!')
        redirect(url_for('bp_gui.contact'))
    return render_template('contact.html', author=Const.AUTHOR, version=Const.VERSION, show_message=False)


@bp_gui.route('/maintenance', methods=['GET'])
def maintenance():
    return render_template('maintenance.html', author=Const.AUTHOR, version=Const.VERSION, show_message=True)


@bp_gui.route('/chat', methods=['GET', 'POST'])
def chat():
    current_datetime = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    if request.method == 'POST':
        form_data = request.get_json()
        response_data = api_func.process_chat(form_data, chat_log=[])
    return render_template('chat.html', author=Const.AUTHOR, version=Const.VERSION, current_date_time=current_datetime)


@bp_gui.errorhandler(HTTPException)
def display_error_page_404(error):
    error_short_description = "Something went wrong"
    error_message = error.description
    return render_template('error.html', author=Const.AUTHOR, version=Const.VERSION, error_short_desc=error_short_description, error_message=error_message), 404


