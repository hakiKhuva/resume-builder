from flask import Flask

def create_app(config:dict):
    app = Flask(__name__)
    app.config.update(config)

    from .views.resume_builder import resume_builder
    app.register_blueprint(resume_builder)

    return app