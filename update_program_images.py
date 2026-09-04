from app import app
from extensions import db
from models import Program


with app.app_context():

    stem = Program.query.filter_by(
        title="STEM & Future-Tech Workshops"
    ).first()

    if stem:
        stem.image = "stem_future.png"


    school = Program.query.filter_by(
        title="School Digitalisation"
    ).first()

    if school:
        school.image = "school_digitalisation.png"


    db.session.commit()

    print("Program images updated successfully.")