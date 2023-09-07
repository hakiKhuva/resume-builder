from flask import Blueprint, render_template, request, session, redirect, url_for, g, abort, make_response, flash
from ..userform import UserForm
from ..functions import resume_data_required, get_all_fonts_name, font_exists, get_font
from ..config import TEMPLATES, TEMPLATES_PATH


resume_builder = Blueprint("ResumeBuilder", __name__)


@resume_builder.route("/", methods=["GET", "POST"])
def create_resume():
    current_user_form = UserForm()
    if request.method == "POST":
        current_user_form.from_request()
        current_user_form.validate()
        session.permanent = True
        session["resume-data"] = current_user_form.resume_data
        if len(current_user_form.errors) > 0:
            return redirect(url_for(".create_resume"))
        return redirect(url_for(".select_template"))

    current_user_form.from_session("resume-data")
    current_user_form.validate()

    return render_template(
        "resume_builder/create_resume.html",
        title="Build New Resume",
        resume_formdata=current_user_form.resume_data,
        resume_formdata_errors=current_user_form.errors,
    )


@resume_builder.route("/select-template")
@resume_data_required
def select_template():
    return render_template(
        "resume_builder/select_template.html",
        title="Select template for Resume",
        all_fonts=get_all_fonts_name(),
        available_templates=TEMPLATES
    )


@resume_builder.route("/preview")
@resume_data_required
def preview_and_save():
    TEMPLATE_NAME = request.args.get("template-name","").upper()
    HEADING_FONT = request.args.get("heading-font","")
    PARAGRAPH_FONT = request.args.get("paragraph-font","")
    if TEMPLATE_NAME not in TEMPLATES or\
        font_exists(HEADING_FONT) is False or\
        font_exists(PARAGRAPH_FONT) is False:
        flash("Please select template and fonts to view preview!")
        return redirect(url_for(".select_template"))

    current_user_form = g.user_form

    if request.args.get("form") == "iframe":
        return render_template(
            TEMPLATES_PATH[TEMPLATE_NAME],
            formdata=current_user_form.resume_data,
            HEADING_FONT=get_font(HEADING_FONT),
            PARAGRAPH_FONT=get_font(PARAGRAPH_FONT),
            type=type
        )

    elif request.args.get("form") == "download":
        HTML_DATA = render_template(
            TEMPLATES_PATH[TEMPLATE_NAME],
            formdata=current_user_form.resume_data,
            HEADING_FONT=get_font(HEADING_FONT),
            PARAGRAPH_FONT=get_font(PARAGRAPH_FONT),
            type=type
        )
        response = make_response(HTML_DATA)
        response.headers.add("Content-Disposition", 'attachment', filename='resume.html')
        return response
        

    elif request.args.get("form") is not None:
        abort(400)

    return render_template(
        "resume_builder/preview.html",
        title="Resume preview",
    )