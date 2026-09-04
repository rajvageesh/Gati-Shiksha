from extensions import db
from datetime import datetime


# =========================================
# PROGRAM MODEL
# =========================================

class Program(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    duration = db.Column(
        db.String(100)
    )

    image = db.Column(
        db.String(300)
    )




# =========================================
# GATISHAALA MODEL
# =========================================

class GatiShaala(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    feature = db.Column(
        db.String(200)
    )

    image = db.Column(
        db.String(300)
    )


# =========================================
# METRIC MODEL
# =========================================

class Metric(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    value = db.Column(
        db.String(50),
        nullable=False
    )

    label = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.String(300)
    )

# =========================================
# LEADER MODEL
# =========================================

class Leader(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    role = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(300)
    )
# =========================================
# ADVISORY MENTOR MODEL
# =========================================

class Mentor(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    role = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(300)
    )

# =========================================
# INQUIRY MODEL
# =========================================

# =========================================
# INQUIRY MODEL
# =========================================

class Inquiry(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(200),
        nullable=False
    )

    mobile = db.Column(
        db.String(20)
    )

    organisation = db.Column(
        db.String(200)
    )

    role = db.Column(
        db.String(150),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    # =====================================
    # PROGRAM INTEREST
    # =====================================

    program = db.Column(
        db.String(200)
    )

    status = db.Column(
        db.String(50),
        default="New",
        nullable=False
    )

    # =====================================
    # DATE
    # =====================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
