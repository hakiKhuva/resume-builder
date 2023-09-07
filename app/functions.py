from flask import session, redirect, url_for, g
from functools import wraps
from .userform import UserForm
from .config import AVAILABLE_FONTS


def resume_data_required(f):
    @wraps(f)
    def caller(*args,**kwargs):
        if 'resume-data' not in session:
            return redirect(url_for("ResumeBuilder.create_resume"))
        uf = UserForm()
        uf.from_session('resume-data')
        uf.validate()
        if len(uf.errors) > 0:
            return redirect(url_for("ResumeBuilder.create_resume"))
        g.user_form = uf
        return f(*args, **kwargs)
    return caller


def get_all_fonts_name():
    return [x['name'] for x in AVAILABLE_FONTS]


def font_exists(fontname:str):
    fontname = fontname.lower()
    for item in AVAILABLE_FONTS:
        if item["name"].lower() == fontname:
            return True
    return False


def get_font(fontname:str):
    fontname = fontname.lower()
    for item in AVAILABLE_FONTS:
        if item["name"].lower() == fontname:
            return item
