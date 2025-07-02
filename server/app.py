import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ff3237a80255173097fe0f996d41d49b')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///server/data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from server.controllers.students_activities import students_activities_bp
    from server.controllers.students_fees import students_fees_bp
    from server.controllers.add_student import add_student_bp
    app.register_blueprint(students_activities_bp)
    app.register_blueprint(students_fees_bp)
    app.register_blueprint(add_student_bp)

    return app

# Create the app instance for Gunicorn
app = create_app()