from app import app
from extensions import db
from models import Program, GatiShaala, Metric, Leader, Mentor, Inquiry


# =========================================
# PROGRAM DATA
# =========================================

programs = [

    {
        "title": "STEM & Future-Tech Workshops",

        "description": (
            "Hands-on learning experiences in "
            "aeromodelling, drone technology, robotics, "
            "space technology and emerging technologies."
        ),

        "category": "STEM & Future Technology",

        "duration": "Workshop-based",

        "image": "stem_future.png"
    },

    {
        "title": "NEP 2020 Teacher Empowerment",

        "description": (
            "Practical teacher training focused on "
            "hands-on learning, educational kits and "
            "digital pedagogy aligned with NEP 2020."
        ),

        "category": "Teacher Empowerment",

        "duration": "Training Program",

        "image": "nep20.png"
    },

    {
        "title": "School Digitalization",

        "description": (
            "Technology solutions for schools including "
            "custom web platforms, administration portals "
            "and automated communication systems."
        ),

        "category": "School Technology",

        "duration": "Custom Program",

        "image": "school_digitalisation.png"
    }

]


# =========================================
# GATISHAALA DATA
# =========================================

gati_shaala = [

    {
        "title": "GatiShaala",

        "description": (
            "A holistic learning platform designed to help "
            "track student learning, progress, mastery and "
            "confidence through a structured digital experience."
        ),

        "feature": "Student Learning & Progress Tracking",

        "image": None
    }
]    
    # =========================================
# IMPACT METRICS
# =========================================

metrics = [

    {
        "value": "83,500+",
        "label": "Students Impacted",
        "description": "Students reached through Gati Shiksha initiatives."
    },

    {
        "value": "350+",
        "label": "Schools Served",
        "description": "Schools engaged through programs and workshops."
    },

    {
        "value": "50+",
        "label": "STEM & Aeromodelling Workshops",
        "description": "Hands-on STEM and aeromodelling workshops conducted."
    },

    {
        "value": "52%",
        "label": "Girl Participation",
        "description": "Participation of girls across the reported programs."
    }
]

    # =========================================
# LEADERSHIP DATA
# =========================================

leaders = [

    {
        "name": "Swetank Tripathi",

        "role": "Founder & CEO",

        "description": (
            "Founder and CEO of Gati Shiksha, working "
            "towards building future-ready learning "
            "through STEM, technology and innovation."
        ),

        "image": 'swetank-sir.png'
    },

  
]
    # =========================================
# ADVISORY MENTORS
# =========================================

mentors = [

    {
        "name": "Academic Advisors",
        "role": "Academic & Higher Education",
        "description": (
            "Academic guidance supporting the development "
            "of meaningful, future-focused learning initiatives."
        ),
        "image": None
    },

    {
        "name": "Education Experts",
        "role": "Education & Pedagogy",
        "description": (
            "Experienced educators contributing insights into "
            "student learning, teacher empowerment and pedagogy."
        ),
        "image": None
    },

    {
        "name": "Science & Technology Advisors",
        "role": "Science, Technology & Innovation",
        "description": (
            "Advisory expertise supporting STEM, technology "
            "and innovation-oriented learning initiatives."
        ),
        "image": None
    }

]


# =========================================
# SEED DATABASE
# =========================================

with app.app_context():

    # Create tables
    db.create_all()


    # -------------------------------------
    # PROGRAMS
    # -------------------------------------

    Program.query.delete()

    for program_data in programs:

        program = Program(
            title=program_data["title"],
            description=program_data["description"],
            category=program_data["category"],
            duration=program_data["duration"],
            image=program_data["image"]
        )

        db.session.add(program)


    # -------------------------------------
    # GATISHAALA
    # -------------------------------------

    GatiShaala.query.delete()

    for gati_data in gati_shaala:

        gati = GatiShaala(
            title=gati_data["title"],
            description=gati_data["description"],
            feature=gati_data["feature"],
            image=gati_data["image"]
        )

        db.session.add(gati)
        # -------------------------------------
    # IMPACT METRICS
    # -------------------------------------

    Metric.query.delete()

    for metric_data in metrics:

        metric = Metric(
            value=metric_data["value"],
            label=metric_data["label"],
            description=metric_data["description"]
        )

        db.session.add(metric)    
    # -------------------------------------
# LEADERSHIP
# -------------------------------------

    Leader.query.delete()

    for leader_data in leaders:

        leader = Leader(
            role=leader_data["role"],
            name=leader_data["name"],
            description=leader_data["description"],
            image=leader_data["image"]
        )

        db.session.add(leader) 
        # =====================================
    # ADVISORY MENTORS
    # =====================================

    Mentor.query.delete()

    for mentor_data in mentors:

        mentor = Mentor(
            name=mentor_data["name"],
            role=mentor_data["role"],
            description=mentor_data["description"],
            image=mentor_data["image"]
        )

        db.session.add(mentor)       
    # -------------------------------------
    # SAVE DATABASE
    # -------------------------------------

    db.session.commit()


    print("Program, GatiShaala, impact metrics, leadership and mentor data added successfully!")