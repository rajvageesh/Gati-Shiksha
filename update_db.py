from app import app, db
from sqlalchemy import text


with app.app_context():

    result = db.session.execute(
        text("PRAGMA table_info(inquiry)")
    )

    columns = [
        row[1]
        for row in result.fetchall()
    ]


    if "status" not in columns:

        db.session.execute(
            text(
                "ALTER TABLE inquiry "
                "ADD COLUMN status VARCHAR(50) "
                "DEFAULT 'New'"
            )
        )

        print("Added status column.")

    else:

        print("Status column already exists.")


    db.session.commit()

    print("Database updated successfully!")