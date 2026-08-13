from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import time

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DB_PATH = os.path.join(os.path.dirname(__file__), "ratemyteacher.db")

REVIEW_COOLDOWN_SECONDS = 45


# ============================================================
# SCHOOL DATA
# ============================================================

SCHOOL_DATA = [
    ("Acreage Pines Elementary", "2141", "Elementary"),
    ("Addison Mizner School", "1451", "Other"),
    ("Alexander W. Dreyfoos Jr. School of the Arts", "0395", "High School"),
    ("Allamanda Elementary", "0101", "Elementary"),
    ("Atlantic Community High", "0862", "High School"),
    ("Bak Middle School of the Arts", "2511", "Middle School"),
    ("Banyan Creek Elementary", "1891", "Elementary"),
    ("Barton Elementary", "0741", "Elementary"),
    ("Beacon Cove Intermediate", "2541", "Other"),
    ("Bear Lakes Middle", "1981", "Middle School"),
    ("Belle Glade Elementary", "2401", "Elementary"),
    ("Belvedere Elementary", "0531", "Elementary"),
    ("Benoist Farms Elementary", "2751", "Elementary"),
    ("Berkshire Elementary", "0601", "Elementary"),
    ("Binks Forest Elementary", "2561", "Elementary"),
    ("Blue Lake Elementary School", "2171", "Elementary"),
    ("Boca Raton Community High School", "0961", "High School"),
    ("Boca Raton Community Middle", "1491", "Middle School"),
    ("Boca Raton Elementary", "0951", "Elementary"),
    ("Boynton Beach Community High", "2361", "High School"),
    ("Calusa Elementary", "1911", "Elementary"),
    ("Carver Community Middle", "2041", "Middle School"),
    ("Cholee Lake Elementary", "2761", "Elementary"),
    ("Christa McAuliffe Middle", "1821", "Middle School"),
    ("Citrus Cove Elementary", "2071", "Elementary"),
    ("Clifford O. Taylor/Kirklane Elementary", "1531", "Elementary"),
    ("Congress Middle", "1581", "Middle School"),
    ("Conniston Community Middle", "0541", "Middle School"),
    ("Coral Reef Elementary", "2581", "Elementary"),
    ("Coral Sunset Elementary", "1811", "Elementary"),
    ("Crestwood Middle", "1691", "Middle School"),
    ("Crosspointe Elementary School", "2731", "Elementary"),
    ("Crystal Lakes Elementary", "2121", "Elementary"),
    ("Cypress Trails Elementary", "1941", "Elementary"),
    ("Del Prado Elementary", "1741", "Elementary"),
    ("Diamond View Elementary", "3261", "Elementary"),
    ("Discovery Key Elementary", "2721", "Elementary"),
    ("Don Estridge High Tech Middle", "2711", "Middle School"),
    ("Dr. Joaquín García High School", "1561", "High School"),
    ("Dr. Mary McLeod Bethune Elementary", "2491", "Elementary"),
    ("Dwight D. Eisenhower Elementary", "1541", "Elementary"),
    ("Eagles Landing Middle", "2461", "Middle School"),
    ("Egret Lake Elementary", "2101", "Elementary"),
    ("Elbridge Gale Elementary", "3361", "Elementary"),
    ("Emerald Cove Middle", "3371", "Middle School"),
    ("Equestrian Trails Elementary", "3341", "Elementary"),
    ("Everglades Elementary", "0061", "Elementary"),
    ("Forest Hill Community High", "0581", "High School"),
    ("Forest Hill Elementary", "0621", "Elementary"),
    ("Forest Park Elementary", "0831", "Elementary"),
    ("Freedom Shores Elementary", "2671", "Elementary"),
    ("Frontier Elementary", "2551", "Elementary"),
    ("Galaxy E3 Elementary", "0821", "Elementary"),
    ("Glade View Elementary", "1251", "Elementary"),
    ("Glades Central Community High", "2301", "High School"),
    ("Golden Grove Elementary", "2421", "Elementary"),
    ("Gove Elementary", "1241", "Elementary"),
    ("Grassy Waters Elementary", "3351", "Elementary"),
    ("Greenacres Elementary", "0631", "Elementary"),
    ("Grove Park Elementary", "1411", "Elementary"),
    ("H. L. Johnson Elementary", "1761", "Elementary"),
    ("Hagen Road Elementary", "1421", "Elementary"),
    ("Hammock Pointe Elementary", "2081", "Elementary"),
    ("Heritage Elementary", "2571", "Elementary"),
    ("Hidden Oaks K-8 School", "0011", "K-8"),
    ("Highland Elementary", "0671", "Elementary"),
    ("Hope-Centennial Elementary", "0012", "Elementary"),
    ("Howell L. Watkins Middle", "0121", "Middle School"),
    ("Independence Middle", "2621", "Middle School"),
    ("Indian Pines Elementary", "1861", "Elementary"),
    ("J. C. Mitchell Elementary", "0931", "Elementary"),
    ("Jeaga Middle", "2701", "Middle School"),
    ("Jerry Thomas Elementary", "1651", "Elementary"),
    ("John F. Kennedy Middle", "0201", "Middle School"),
    ("John I. Leonard High", "1361", "High School"),
    ("Jupiter Community High", "0081", "High School"),
    ("Jupiter Elementary", "0071", "Elementary"),
    ("Jupiter Farms Elementary", "2091", "Elementary"),
    ("Jupiter Middle", "1731", "Middle School"),
    ("K. E. Cunningham/Canal Point Elementary", "1831", "Elementary"),
    ("L. C. Swain Middle", "0021", "Middle School"),
    ("Lake Park Elementary", "0141", "Elementary"),
    ("Lake Shore Middle", "1232", "Middle School"),
    ("Lake Worth Community High", "0691", "High School"),
    ("Lake Worth Middle", "2131", "Middle School"),
    ("Lantana Community Middle", "0761", "Middle School"),
    ("Lantana Elementary", "0751", "Elementary"),
    ("Liberty Park Elementary", "1871", "Elementary"),
    ("Lighthouse Elementary", "1931", "Elementary"),
    ("Limestone Creek Elementary", "2031", "Elementary"),
    ("Lincoln Elementary", "0211", "Elementary"),
    ("Loggers' Run Community Middle", "1751", "Middle School"),
    ("Loxahatchee Groves Elementary", "1901", "Elementary"),
    ("Manatee Elementary", "2241", "Elementary"),
    ("Marsh Pointe Elementary", "0661", "Elementary"),
    ("Meadow Park Elementary", "0591", "Elementary"),
    ("Melaleuca Elementary", "1441", "Elementary"),
    ("Morikami Park Elementary", "1951", "Elementary"),
    ("New Horizons Elementary", "2051", "Elementary"),
    ("North Grade K-8", "0681", "K-8"),
    ("Northboro Elementary", "0291", "Elementary"),
    ("Northmore Elementary", "0271", "Elementary"),
    ("Okeeheelee Middle", "2151", "Middle School"),
    ("Olympic Heights Community High", "2181", "High School"),
    ("Omni Middle", "1991", "Middle School"),
    ("Orchard View Elementary", "2351", "Elementary"),
    ("Osceola Creek Middle", "2821", "Middle School"),
    ("Pahokee Elementary", "1101", "Elementary"),
    ("Pahokee Middle-Senior High", "1771", "High School"),
    ("Palm Beach Central High", "2631", "High School"),
    ("Palm Beach Gardens Community High", "1371", "High School"),
    ("Palm Beach Gardens Elementary", "0111", "Elementary"),
    ("Palm Beach Lakes Community High", "1851", "High School"),
    ("Palm Beach Public", "0421", "Other"),
    ("Palm Beach Virtual School", "7001", "Other"),
    ("Palm Springs Community Middle", "0611", "Middle School"),
    ("Palm Springs Elementary", "0651", "Elementary"),
    ("Palmetto Elementary", "0561", "Elementary"),
    ("Panther Run Elementary", "2161", "Elementary"),
    ("Park Vista Community High", "2001", "High School"),
    ("Pierce Hammock Elementary", "2861", "Elementary"),
    ("Pine Grove Elementary", "0911", "Elementary"),
    ("Pine Jog Elementary", "0051", "Elementary"),
    ("Pioneer Park Elementary", "2371", "Elementary"),
    ("Pleasant City Elementary", "2591", "Elementary"),
    ("Plumosa School of the Arts", "0871", "Other"),
    ("Poinciana Elementary", "0791", "Elementary"),
    ("Polo Park Middle", "2611", "Middle School"),
    ("Rolling Green Elementary", "0781", "Elementary"),
    ("Roosevelt Community Middle", "0311", "Middle School"),
    ("Roosevelt Elementary", "0341", "Elementary"),
    ("Rosenwald Elementary", "1321", "Elementary"),
    ("Royal Palm Beach Community High", "2331", "High School"),
    ("Royal Palm Beach Elementary", "2741", "Elementary"),
    ("S. D. Spady Elementary", "0881", "Elementary"),
    ("Saddle View Elementary", "0235", "Elementary"),
    ("Sandpiper Shores Elementary", "1961", "Elementary"),
    ("Santaluces Community High", "1611", "High School"),
    ("Seminole Ridge Community High", "3861", "High School"),
    ("Seminole Trails Elementary", "1711", "Elementary"),
    ("South Grade Elementary", "2431", "Elementary"),
    ("South Tech Academy", "1571", "High School"),
    ("Spanish River Community High", "1681", "High School"),
    ("Starlight Cove Elementary", "0771", "Elementary"),
    ("Suncoast High", "0151", "High School"),
    ("Sunrise Park Elementary", "2691", "Elementary"),
    ("Sunset Palms Elementary", "0281", "Elementary"),
    ("The Conservatory School @ North Palm Beach", "0131", "Other"),
    ("The South Olive School", "0572", "Other"),
    ("Timber Trace Elementary", "2011", "Elementary"),
    ("Tradewinds Middle", "2781", "Middle School"),
    ("U. B. Kinsey/Palmview Elementary", "0361", "Elementary"),
    ("Verde K-8", "1661", "K-8"),
    ("Village Academy on the Art & Sara Jo Kobacker Campus", "2811", "Other"),
    ("Washington Elementary", "0191", "Elementary"),
    ("Waters Edge Elementary", "0031", "Elementary"),
    ("Watson B. Duncan Middle", "1971", "Middle School"),
    ("Wellington Community High", "2191", "High School"),
    ("Wellington Elementary", "1671", "Elementary"),
    ("Wellington Landings Middle", "1701", "Middle School"),
    ("West Boca Raton Community High", "3251", "High School"),
    ("West Boynton Middle School", "1721", "Middle School"),
    ("West Gate Elementary", "0481", "Elementary"),
    ("West Riviera Elementary", "1401", "Elementary"),
    ("Western Pines Middle", "2451", "Middle School"),
    ("Westward Elementary", "0351", "Elementary"),
    ("Whispering Pines Elementary", "1781", "Elementary"),
    ("William T. Dwyer High", "2201", "High School"),
    ("Woodlands Middle", "1921", "Middle School"),
    ("Wynnebrook Elementary", "1391", "Elementary"),
]


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS schools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            school_number TEXT UNIQUE,
            school_type TEXT NOT NULL DEFAULT 'Other',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            school_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            overall_rating INTEGER NOT NULL,
            difficulty INTEGER NOT NULL,
            workload INTEGER NOT NULL,
            clarity INTEGER NOT NULL,
            test_difficulty INTEGER NOT NULL,
            participation INTEGER NOT NULL,
            comment TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        );
    """)

    # Add school_id if your old database doesn't have it yet
    columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(teachers)").fetchall()
    }

    if "school_id" not in columns:
        conn.execute(
            "ALTER TABLE teachers ADD COLUMN school_id INTEGER"
        )

    # Add all schools
    for name, number, school_type in SCHOOL_DATA:
        conn.execute("""
            INSERT OR IGNORE INTO schools
            (name, school_number, school_type)
            VALUES (?, ?, ?)
        """, (name, number, school_type))

    conn.commit()
    conn.close()


# ============================================================
# RATING HELPERS
# ============================================================

def rating_to_letter(avg):
    if avg is None:
        return "NA"

    if avg >= 4.5:
        return "A"
    elif avg >= 3.5:
        return "B"
    elif avg >= 2.5:
        return "C"
    elif avg >= 1.5:
        return "D"
    else:
        return "F"


def get_teacher_stats(conn, teacher_id):

    row = conn.execute("""
        SELECT
            COUNT(*) AS review_count,
            AVG(overall_rating) AS avg_overall,
            AVG(difficulty) AS avg_difficulty,
            AVG(workload) AS avg_workload,
            AVG(clarity) AS avg_clarity,
            AVG(test_difficulty) AS avg_test_difficulty,
            AVG(participation) AS avg_participation
        FROM reviews
        WHERE teacher_id = ?
    """, (teacher_id,)).fetchone()

    if row["review_count"] == 0:
        return {
            "review_count": 0,
            "letter_grade": "NA"
        }

    return {
        "review_count": row["review_count"],
        "avg_overall": round(row["avg_overall"], 1),
        "avg_difficulty": round(row["avg_difficulty"], 1),
        "avg_workload": round(row["avg_workload"], 1),
        "avg_clarity": round(row["avg_clarity"], 1),
        "avg_test_difficulty": round(row["avg_test_difficulty"], 1),
        "avg_participation": round(row["avg_participation"], 1),
        "letter_grade": rating_to_letter(row["avg_overall"])
    }


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    query = request.args.get("q", "").strip()
    school_type = request.args.get("type", "").strip()

    conn = get_db()

    sql = """
        SELECT *
        FROM schools
        WHERE 1=1
    """

    params = []

    if query:
        sql += " AND name LIKE ?"
        params.append(f"%{query}%")

    if school_type:
        sql += " AND school_type = ?"
        params.append(school_type)

    sql += " ORDER BY name"

    schools = conn.execute(sql, params).fetchall()

    conn.close()

    return render_template(
        "index.html",
        schools=schools,
        query=query,
        school_type=school_type
    )


# ============================================================
# SCHOOL PAGE
# ============================================================

@app.route("/school/<int:school_id>")
def school_detail(school_id):

    query = request.args.get("q", "").strip()

    conn = get_db()

    school = conn.execute("""
        SELECT *
        FROM schools
        WHERE id = ?
    """, (school_id,)).fetchone()

    if school is None:
        conn.close()
        return "School not found", 404

    sql = """
        SELECT *
        FROM teachers
        WHERE school_id = ?
    """

    params = [school_id]

    if query:
        sql += """
            AND (
                name LIKE ?
                OR subject LIKE ?
            )
        """

        params.extend([
            f"%{query}%",
            f"%{query}%"
        ])

    sql += " ORDER BY name"

    teachers = conn.execute(sql, params).fetchall()

    teacher_list = []

    for teacher in teachers:

        teacher_dict = dict(teacher)

        teacher_dict.update(
            get_teacher_stats(
                conn,
                teacher["id"]
            )
        )

        teacher_list.append(teacher_dict)

    conn.close()

    return render_template(
        "school.html",
        school=school,
        teachers=teacher_list,
        query=query
    )


# ============================================================
# TEACHER PAGE
# ============================================================

@app.route("/teacher/<int:teacher_id>")
def teacher_detail(teacher_id):

    conn = get_db()

    teacher = conn.execute("""
        SELECT
            teachers.*,
            schools.name AS school_name,
            schools.id AS school_id
        FROM teachers
        LEFT JOIN schools
            ON schools.id = teachers.school_id
        WHERE teachers.id = ?
    """, (teacher_id,)).fetchone()

    if teacher is None:
        conn.close()
        return "Teacher not found", 404

    stats = get_teacher_stats(
        conn,
        teacher_id
    )

    reviews = conn.execute("""
        SELECT *
        FROM reviews
        WHERE teacher_id = ?
        ORDER BY created_at DESC
    """, (teacher_id,)).fetchall()

    conn.close()

    return render_template(
        "teacher.html",
        teacher=teacher,
        stats=stats,
        reviews=reviews
    )


# ============================================================
# ADD TEACHER
# ============================================================

@app.route("/add-teacher", methods=["GET", "POST"])
def add_teacher():

    conn = get_db()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        subject = request.form.get("subject", "").strip()
        school_id = request.form.get("school_id", "").strip()

        if not name or not subject or not school_id:

            conn.close()

            flash(
                "Please enter the teacher name, subject, and school."
            )

            return redirect(
                url_for("add_teacher")
            )

        try:
            school_id = int(school_id)

        except ValueError:

            conn.close()

            flash("Please choose a valid school.")

            return redirect(
                url_for("add_teacher")
            )

        school = conn.execute("""
            SELECT id
            FROM schools
            WHERE id = ?
        """, (school_id,)).fetchone()

        if school is None:

            conn.close()

            flash("School not found.")

            return redirect(
                url_for("add_teacher")
            )

        existing = conn.execute("""
            SELECT id
            FROM teachers
            WHERE name = ?
            AND subject = ?
            AND school_id = ?
        """, (
            name,
            subject,
            school_id
        )).fetchone()

        if existing:

            conn.close()

            flash(
                "That teacher is already listed at this school."
            )

            return redirect(
                url_for(
                    "teacher_detail",
                    teacher_id=existing["id"]
                )
            )

        cursor = conn.execute("""
            INSERT INTO teachers
            (name, subject, school_id)
            VALUES (?, ?, ?)
        """, (
            name,
            subject,
            school_id
        ))

        conn.commit()

        teacher_id = cursor.lastrowid

        conn.close()

        return redirect(
            url_for(
                "teacher_detail",
                teacher_id=teacher_id
            )
        )

    schools = conn.execute("""
        SELECT *
        FROM schools
        ORDER BY name
    """).fetchall()

    conn.close()

    return render_template(
        "add_teacher.html",
        schools=schools
    )


# ============================================================
# ADD REVIEW
# ============================================================

@app.route(
    "/teacher/<int:teacher_id>/review",
    methods=["GET", "POST"]
)
def add_review(teacher_id):

    conn = get_db()

    teacher = conn.execute("""
        SELECT
            teachers.*,
            schools.name AS school_name,
            schools.id AS school_id
        FROM teachers
        LEFT JOIN schools
            ON schools.id = teachers.school_id
        WHERE teachers.id = ?
    """, (teacher_id,)).fetchone()

    if teacher is None:

        conn.close()

        return "Teacher not found", 404

    if request.method == "POST":

        # Spam protection
        if request.form.get("website", "").strip():

            conn.close()

            return redirect(
                url_for(
                    "teacher_detail",
                    teacher_id=teacher_id
                )
            )

        # Cooldown
        last_review = session.get(
            "last_review_at",
            0
        )

        elapsed = time.time() - last_review

        if elapsed < REVIEW_COOLDOWN_SECONDS:

            wait = int(
                REVIEW_COOLDOWN_SECONDS - elapsed
            )

            conn.close()

            flash(
                f"Please wait {wait} more seconds before submitting another review."
            )

            return redirect(
                url_for(
                    "add_review",
                    teacher_id=teacher_id
                )
            )

        try:

            overall = int(
                request.form["overall_rating"]
            )

            difficulty = int(
                request.form["difficulty"]
            )

            workload = int(
                request.form["workload"]
            )

            clarity = int(
                request.form["clarity"]
            )

            test_difficulty = int(
                request.form["test_difficulty"]
            )

            participation = int(
                request.form["participation"]
            )

        except (KeyError, ValueError):

            conn.close()

            flash(
                "Please complete every rating."
            )

            return redirect(
                url_for(
                    "add_review",
                    teacher_id=teacher_id
                )
            )

        ratings = [
            overall,
            difficulty,
            workload,
            clarity,
            test_difficulty,
            participation
        ]

        if any(
            rating < 1 or rating > 5
            for rating in ratings
        ):

            conn.close()

            flash(
                "Ratings must be between 1 and 5."
            )

            return redirect(
                url_for(
                    "add_review",
                    teacher_id=teacher_id
                )
            )

        comment = request.form.get(
            "comment",
            ""
        ).strip()

        conn.execute("""
            INSERT INTO reviews (
                teacher_id,
                overall_rating,
                difficulty,
                workload,
                clarity,
                test_difficulty,
                participation,
                comment
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            teacher_id,
            overall,
            difficulty,
            workload,
            clarity,
            test_difficulty,
            participation,
            comment
        ))

        conn.commit()

        conn.close()

        session["last_review_at"] = time.time()

        return redirect(
            url_for(
                "teacher_detail",
                teacher_id=teacher_id
            )
        )

    conn.close()

    return render_template(
        "add_review.html",
        teacher=teacher
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    init_db()

    app.run(
        debug=True
    )