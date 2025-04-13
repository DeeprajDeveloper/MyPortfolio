import os
from flask import Blueprint, request, render_template, abort
import config
from app.api import functionality as api_func
from app.constants import Information as Const, QueryString as Query
from utils import db_util as db

bp_gui = Blueprint('bp_gui', __name__, url_prefix='/gui', template_folder='templates', static_folder=os.path.join(os.path.dirname(__file__), 'static'), static_url_path='/bp_gui/static')


@bp_gui.route('/test', methods=['GET'])
def test():
    return render_template('test.html')


@bp_gui.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@bp_gui.route('/', methods=['GET'])
@bp_gui.route('/home', methods=['GET'])
def home():
    project_details: list = []
    my_information_list = api_func.get_my_info()
    experience_info = my_information_list['myInformation']['myIndustryExperiences']
    about_me_info = my_information_list['myInformation']['aboutMe']
    expertise_info = my_information_list['myInformation']['myExpertise']
    projects_to_display = my_information_list['myInformation']['topDisplayProjectIdentifiers'].split(',')
    for project_id in projects_to_display:
        project_details.append(api_func.get_project_summary(filter_parameters=project_id)[0])
    return render_template('index.html', author=Const.AUTHOR, version=Const.VERSION, experience=experience_info, about_me=about_me_info, my_projects=project_details, my_expertise=expertise_info)


@bp_gui.route('/explore', methods=['GET'])
def explore_projects():
    project_details = api_func.get_project_summary(filter_parameters='')
    return render_template('explore_projects.html', author=Const.AUTHOR, version=Const.VERSION, my_projects=project_details)


@bp_gui.route('/project-details', methods=['GET'])
def project_details():
    project_id = request.args.get('projectIdentifier')
    if api_func.project_exists(project_id=project_id):
        extended_project_data = api_func.get_project_details(project_id=project_id)
    else:
        abort(404)
    return render_template('project_details.html', author=Const.AUTHOR, version=Const.VERSION, project_data=extended_project_data)


@bp_gui.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', author=Const.AUTHOR, version=Const.VERSION)


@bp_gui.errorhandler(404)
def display_error_page_404(error):
    error_short_description = "Project Not Found"
    error_message = "The project details you are trying to look for were not found."
    return render_template('error.html', author=Const.AUTHOR, version=Const.VERSION, error_cd=404, error_short_desc=error_short_description, error_message=error_message), 404


@bp_gui.errorhandler(400)
def display_error_page_400(error):
    error_short_description = "Bad Request"
    error_message = "The project details you are trying to look for were not found."
    return render_template('error.html', author=Const.AUTHOR, version=Const.VERSION, error_cd=400, error_short_desc=error_short_description, error_message=error_message), 400
