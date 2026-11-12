from html import escape
import random
import pandas as pd
from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    text = text.casefold()
    pattern = pattern.casefold()

    if pattern == "":
        return True

    lps = build_lps(pattern)
    i = 0
    j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                return True

        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

    return False

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="exam_seating_db"
    )

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "MySQL Database Connected Successfully!"
    except Exception as e:
        return f"Database connection failed: {e}"
    

from flask import request


@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    message = ""
    message_color = "#16a34a"

    if request.method == "POST":
        roll_no = request.form["roll_no"].strip()
        student_name = request.form["student_name"].strip()
        class_group = request.form["class_group"].strip()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO students (roll_no, student_name, class_group) VALUES (%s, %s, %s)",
                (roll_no, student_name, class_group)
            )

            conn.commit()
            message = "Student added successfully!"

            cursor.close()
            conn.close()

        except Exception as e:
            message = "Could not add student. Check if the Roll Number already exists."
            message_color = "#dc2626"

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Student | ExamSeat Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { box-sizing: border-box; }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                color: #1e293b;
            }

            .header {
                background: #1a2b59;
                color: white;
                padding: 22px 35px;
                font-size: 24px;
                font-weight: bold;
            }

            .container {
                max-width: 650px;
                margin: 45px auto;
                padding: 0 20px;
            }

            .card {
                background: white;
                padding: 32px;
                border-radius: 16px;
                box-shadow: 0 5px 20px #0000000d;
                border-top: 5px solid #2563eb;
            }

            h2 {
                margin-top: 0;
                font-size: 28px;
            }

            .subtitle {
                color: #64748b;
                margin-bottom: 28px;
                line-height: 1.5;
            }

            label {
                display: block;
                margin: 18px 0 8px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 12px;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                font-size: 15px;
            }

            input:focus {
                outline: 2px solid #93c5fd;
                border-color: #2563eb;
            }

            button {
                width: 100%;
                margin-top: 25px;
                padding: 13px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover { background: #1d4ed8; }

            .message {
                background: #f0fdf4;
                color: """ + message_color + """;
                padding: 12px;
                margin-bottom: 18px;
                border-radius: 8px;
            }

            .back {
                display: inline-block;
                margin-top: 22px;
                color: #2563eb;
                text-decoration: none;
            }

            @media (max-width: 600px) {
                .header { padding: 20px; }
                .container { margin-top: 25px; }
                .card { padding: 22px; }
            }
        </style>
    </head>
    <body>
        <div class="header">🎓 ExamSeat Pro</div>

        <div class="container">
            <div class="card">
                <h2>👨‍🎓 Add New Student</h2>
                <p class="subtitle">
                    Enter the student's details to register them
                    in the examination seating system.
                </p>

                """ + (
                    '<div class="message">' + message + '</div>'
                    if message else ''
                ) + """

                <form method="POST">
                    <label>Roll Number</label>
                    <input name="roll_no" placeholder="e.g. 26MCA001"
                           required>

                    <label>Student Name</label>
                    <input name="student_name"
                           placeholder="Enter full name" required>

                    <label>Class / Group</label>
                    <input name="class_group"
                           placeholder="e.g. MCA-A" required>

                    <button type="submit">Add Student</button>
                </form>

                <a class="back" href="/">← Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """



@app.route("/add-room", methods=["GET", "POST"])
def add_room():
    message = ""

    if request.method == "POST":
        room_name = request.form["room_name"]
        rows = int(request.form["rows_count"])
        cols = int(request.form["cols_count"])

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO rooms (room_name, rows_count, cols_count) VALUES (%s, %s, %s)",
            (room_name, rows, cols)
        )

        conn.commit()
        cursor.close()
        conn.close()

        message = "Exam room added successfully!"

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Exam Room</title>
        <style>
            body {
                font-family: Arial;
                background: #f1f5f9;
                margin: 0;
                color: #1e293b;
            }
            header {
                background: #1a2b59;
                color: white;
                padding: 22px 35px;
                font-size: 24px;
            }
            .card {
                background: white;
                max-width: 550px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 14px;
                box-shadow: 0 4px 15px #00000012;
            }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0 18px;
                box-sizing: border-box;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
            }
            button {
                background: #2563eb;
                color: white;
                border: 0;
                padding: 13px;
                width: 100%;
                border-radius: 7px;
                cursor: pointer;
            }
            button:hover { background: #1d4ed8; }
            .message { color: green; }
            a { color: #2563eb; text-decoration: none; }
            



        </style>
    </head>
    <body>
        <header>ExamSeat Pro</header>
        <div class="card">
            <h2>Add Exam Room</h2>
            <p class="message">""" + message + """</p>
            <form method="POST">
                Room Name
                <input name="room_name" placeholder="e.g. Room 101" required>

                Number of Rows
                <input type="number" id="rows" name="rows_count"
                       min="1" required oninput="calculateSeats()">

                Number of Columns
                <input type="number" id="cols" name="cols_count"
                       min="1" required oninput="calculateSeats()">

                <h3>Total Seats: <span id="total">0</span></h3>

                <button type="submit">Add Room</button>
            </form>
            <p><a href="/">← Back to Dashboard</a></p>
        </div>

        <script>
            function calculateSeats() {
                let rows = Number(document.getElementById("rows").value);
                let cols = Number(document.getElementById("cols").value);
                document.getElementById("total").innerText = rows * cols;
            }
        </script>
    </body>
    </html>
    """

   

@app.route("/generate")
def generate_seating():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all students
    cursor.execute(
        "SELECT roll_no, student_name, class_group FROM students"
    )
    students = list(cursor.fetchall())

    # Get all exam rooms
    cursor.execute(
        "SELECT room_id, room_name, rows_count, cols_count FROM rooms"
    )
    rooms = cursor.fetchall()

    if not students:
        cursor.close()
        conn.close()
        return "Please add students first!"

    # Create a list of all available seats
    seats = []
    for room_id, room_name, rows, cols in rooms:
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                seats.append((room_id, room_name, r, c))

    if len(seats) < len(students):
        cursor.close()
        conn.close()
        return "Not enough seats! Please add more rooms."

   
    # Backtracking algorithm for conflict-free seating
    def solve_seating(remaining, current, occupied):
        if not remaining:
            return current.copy()

        # Try the most frequent group first
        group_counts = {}
        for student in remaining:
            group_counts[student[2]] = (
                group_counts.get(student[2], 0) + 1
            )

        student = max(
            remaining,
            key=lambda s: group_counts[s[2]]
        )

        next_remaining = remaining.copy()
        next_remaining.remove(student)

        for room_id, room_name, row, col in seats:
            seat_key = (room_id, row, col)

            # Never assign an occupied seat twice
            if seat_key in occupied:
                continue

            conflict = False

            for ar_id, other_student, ar, ac, other_room in current:
                if ar_id != room_id:
                    continue

                adjacent = (
                    (ar == row and abs(ac - col) == 1)
                    or
                    (ac == col and abs(ar - row) == 1)
                )

                if adjacent and other_student[2] == student[2]:
                    conflict = True
                    break

            if conflict:
                continue

            current.append(
                (room_id, student, row, col, room_name)
            )
            occupied.add(seat_key)

            result = solve_seating(
                next_remaining, current, occupied
            )

            if result is not None:
                return result

            current.pop()
            occupied.remove(seat_key)

        return None

    assignments = solve_seating(students.copy(), [], set())

    if assignments is None:
        cursor.close()
        conn.close()
        return (
            "No conflict-free seating arrangement found. "
            "Please check the room layout and student groups."
        )

    # Save the new seating arrangement
    cursor.execute("DELETE FROM seating_assignments")

    for room_id, student, row, col, room_name in assignments:
        cursor.execute(
            """INSERT INTO seating_assignments
            (roll_no, room_id, row_no, col_no)
            VALUES (%s, %s, %s, %s)""",
            (student[0], room_id, row, col)
        )

    conn.commit()
    cursor.close()
    conn.close()

    # Display the result

    result = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated Seating</title>
        <style>
            body {
                font-family: Arial;
                background: #f1f5f9;
                margin: 0;
                color: #1e293b;
            }
            header {
                background: #1a2b59;
                color: white;
                padding: 22px 35px;
                font-size: 24px;
            }
            .container {
            margin: 30px auto;
            padding: 25px;
            background: white;
            border-radius: 14px;
            overflow-x: auto;
            max-width: 1400px;
}

.container h3 {
    margin-top: 30px;
    margin-bottom: 15px;
}
            }
            table {
                border-collapse: collapse;
                margin: 15px 0;
                width: 100%;
            }
            th {
                background: #2563eb;
                color: white;
            }
            th, td {
                padding: 12px;
                border: 1px solid #cbd5e1;
                text-align: center;
            }
            td {
                background: #eff6ff;
            }
            a {
                color: #2563eb;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
    <header>ExamSeat Pro</header>
    <div class="container">
    <h2>Generated Exam Seating Arrangement</h2>
    <table>
    <tr>
        <th>Roll Number</th>
        <th>Student Name</th>
        <th>Class</th>
        <th>Room</th>
        <th>Row</th>
        <th>Seat</th>
    </tr>
    """
    for room_id, student, row, col, room_name in assignments:
        result += f"""
        <tr>
        <td>{student[0]}</td>
        <td>{student[1]}</td>
        <td>{student[2]}</td>
        <td>{room_name}</td>
        <td>{row}</td>
        <td>{col}</td>
        </tr>
        """

   
    result += "</table>"

   
    result += "<h2>Visual Seating Layout</h2>"

    room_layouts = {}

    for room_id, student, row, col, room_name in assignments:
        if room_id not in room_layouts:
            room_layouts[room_id] = {}

        room_layouts[room_id][(row, col)] = student

    for room_id, room_name, rows, cols in rooms:
        result += f"<h3>{room_name}</h3>"

        result += """
        <div style="width:100%; overflow-x:auto;">
        <table style="
            border-collapse:collapse;
            table-layout:fixed;
            margin:15px 0 30px;
        ">
        """

        for r in range(1, rows + 1):
            result += "<tr>"

            for c in range(1, cols + 1):
                student = room_layouts.get(
                    room_id, {}
                ).get((r, c))

                if student:
                    label = (
                        f"<strong>{student[0]}</strong>"
                        f"<br>{student[1]}"
                    )
                    bg = "#dbeafe"
                    color = "#1e3a8a"
                else:
                    label = "Empty"
                    bg = "#f8fafc"
                    color = "#94a3b8"

                result += f"""
                <td style="
                    border:1px solid #cbd5e1;
                    padding:12px 8px;
                    min-width:100px;
                    height:65px;
                    text-align:center;
                    vertical-align:middle;
                    background:{bg};
                    color:{color};
                    overflow-wrap:anywhere;
                ">{label}</td>
                """

            result += "</tr>"

        # Close the table AFTER all rows
        result += """
        </table>
        </div>
        """

    result += """
        <p><a href="/">← Back to Dashboard</a></p>
        </div>
        </body>
        </html>
    """

    return result



@app.route("/room-report")
def room_report():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.room_name,
               r.rows_count * r.cols_count AS total_seats,
               COUNT(sa.roll_no) AS occupied_seats
        FROM rooms r
        LEFT JOIN seating_assignments sa ON r.room_id = sa.room_id
        GROUP BY r.room_id, r.room_name,
                 r.rows_count, r.cols_count
        ORDER BY r.room_id
    """)

    rooms_data = cursor.fetchall()
    cursor.close()
    conn.close()

    result = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Room Reports</title>
        <style>
            body {
                font-family: Arial;
                background: #f1f5f9;
                margin: 0;
                color: #1e293b;
            }
            header {
                background: #1a2b59;
                color: white;
                padding: 22px 35px;
                font-size: 24px;
            }
            .container {
                margin: 35px;
                padding: 25px;
                background: white;
                border-radius: 14px;
                overflow-x: auto;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th {
                background: #2563eb;
                color: white;
            }
            th, td {
                padding: 14px;
                border: 1px solid #e2e8f0;
                text-align: center;
            }
            tr:nth-child(even) { background: #f8fafc; }
            a { color: #2563eb; text-decoration: none; }
        </style>
    </head>
    <body>
        <header>ExamSeat Pro</header>
        <div class="container">
            <h2>Exam Room Capacity Report</h2>
            <table>
                <tr>
                    <th>Room Name</th>
                    <th>Total Seats</th>
                    <th>Occupied Seats</th>
                    <th>Empty Seats</th>
                </tr>
    """

    for room_name, total, occupied in rooms_data:
        empty = total - occupied
        result += f"""
            <tr>
                <td>{room_name}</td>
                <td>{total}</td>
                <td>{occupied}</td>
                <td>{empty}</td>
            </tr>
        """

    result += """
            </table>
            <p><a href="/">← Back to Dashboard</a></p>
        </div>
    </body>
    </html>
    """

    return result

    

    
@app.route("/edit-student/<roll_no>", methods=["GET", "POST"])
def edit_student(roll_no):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["student_name"]
        class_group = request.form["class_group"]

        cursor.execute(
            "UPDATE students SET student_name=%s, class_group=%s WHERE roll_no=%s",
            (name, class_group, roll_no)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return """
        <h2>Student Updated Successfully!</h2>
        <a href="/students-list">Back to Student List</a>
        """

    cursor.execute(
        "SELECT student_name, class_group FROM students WHERE roll_no=%s",
        (roll_no,)
    )
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student is None:
        return "Student not found!"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Student</title>
        <style>
            body {{
                font-family: Arial;
                background: #f1f5f9;
                margin: 0;
                color: #1e293b;
            }}
            header {{
                background: #1a2b59;
                color: white;
                padding: 22px 35px;
                font-size: 24px;
            }}
            .card {{
                background: white;
                max-width: 500px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 14px;
                box-shadow: 0 4px 15px #00000012;
            }}
            input {{
                width: 100%;
                padding: 12px;
                margin: 10px 0 18px;
                box-sizing: border-box;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
            }}
            button {{
                background: #2563eb;
                color: white;
                border: 0;
                padding: 13px;
                width: 100%;
                border-radius: 7px;
                cursor: pointer;
            }}
            button:hover {{ background: #1d4ed8; }}
            a {{ color: #2563eb; text-decoration: none; }}
        </style>
    </head>
    <body>
        <header>ExamSeat Pro</header>
        <div class="card">
            <h2>Edit Student</h2>
            <form method="POST">
                Student Name
                <input name="student_name" value="{student[0]}" required>
                Class / Group
                <input name="class_group" value="{student[1]}" required>
                <button type="submit">Save Changes</button>
            </form>
            <p><a href="/students-list">Back to Student List</a></p>
        </div>
    </body>
    </html>
    """


@app.route("/delete-student/<roll_no>", methods=["POST"])
def delete_student(roll_no):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM seating_assignments WHERE roll_no=%s",
        (roll_no,)
    )

    cursor.execute(
        "DELETE FROM students WHERE roll_no=%s",
        (roll_no,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return """
    
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Deleted</title>
        <style>
            body {
                font-family: Arial;
                background: #f1f5f9;
                text-align: center;
                padding: 60px 20px;
            }
            .card {
                background: white;
                padding: 30px;
                max-width: 450px;
                margin: auto;
                border-radius: 14px;
            }
            a {
                color: #2563eb;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Student Deleted Successfully!</h2>
            <a href="/students-list">Back to Student List</a>
        </div>
    </body>
    </html>
    """



@app.route("/students-list")
def students_list():
    search_term = request.args.get("search", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT roll_no, student_name, class_group "
        "FROM students ORDER BY roll_no"
    )
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    # Search using the KMP algorithm
    if search_term:
        students = [
            student for student in students
            if any(
                kmp_search(str(value), search_term)
                for value in student
                if value is not None
            )
        ]

    result = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student List | ExamSeat Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                margin: 0;
                color: #1e293b;
            }
            header {
                background: #1a2b59;
                color: white;
                padding: 22px 35px;
                font-size: 24px;
            }
            .container {
                margin: 35px auto;
                max-width: 1200px;
                background: white;
                padding: 25px;
                border-radius: 14px;
                overflow-x: auto;
            }
            input {
                padding: 12px;
                width: 100%;
                max-width: 400px;
                box-sizing: border-box;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
            }
            button {
                background: #2563eb;
                color: white;
                border: none;
                padding: 12px 18px;
                border-radius: 7px;
                cursor: pointer;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th {
                background: #2563eb;
                color: white;
            }
            th, td {
                padding: 13px;
                border: 1px solid #e2e8f0;
                text-align: left;
            }
            tr:nth-child(even) {
                background: #f8fafc;
            }
            a {
                color: #2563eb;
                text-decoration: none;
            }
            .delete-form {
                display: inline;
            }
            .delete-btn {
                background: transparent;
                color: #2563eb;
                border: none;
                padding: 0;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <header>ExamSeat Pro</header>

        <div class="container">
            <h2>All Registered Students</h2>

            <form method="GET" action="/students-list">
                <input type="text" name="search"
                       placeholder="Search roll number, name or class"
                       value="
    """ + escape(search_term, quote=True) + """">
                <button type="submit">Search</button>
                <a href="/students-list">Show All</a>
            </form>

            <p>Matching Students: """ + str(len(students)) + """</p>

            <table>
                <tr>
                    <th>Roll Number</th>
                    <th>Student Name</th>
                    <th>Class / Group</th>
                    <th>Edit</th>
                    <th>Delete</th>
                </tr>
    """

    if not students:
        result += """
            <tr>
                <td colspan="5">No matching students found.</td>
            </tr>
        """

    for roll_no, name, class_group in students:
        safe_roll = escape(str(roll_no), quote=True)
        safe_name = escape(str(name), quote=True)
        safe_class = escape(str(class_group), quote=True)

        result += f"""
            <tr>
                <td>{safe_roll}</td>
                <td>{safe_name}</td>
                <td>{safe_class}</td>
                <td>
                    <a href="/edit-student/{safe_roll}">Edit</a>
                </td>
                <td>
                    <form class="delete-form" method="POST"
                          action="/delete-student/{safe_roll}"
                          onsubmit="return confirm('Delete this student?')">
                        <button class="delete-btn" type="submit">
                            Delete
                        </button>
                    </form>
                </td>
            </tr>
        """

    result += """
            </table>
            <p><a href="/">← Back to Dashboard</a></p>
        </div>
    </body>
    </html>
    """

    return result


    
@app.route("/")
def home():
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ExamSeat Pro Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                color: #1e293b;
            }

            .sidebar {
                width: 240px;
                height: 100vh;
                background: #172554;
                color: white;
                position: fixed;
                padding: 25px 18px;
            }

            .brand {
                font-size: 23px;
                font-weight: bold;
                margin-bottom: 40px;
            }

            .sidebar a {
                display: block;
                color: #dbeafe;
                text-decoration: none;
                padding: 14px;
                margin: 8px 0;
                border-radius: 8px;
            }

            .sidebar a:hover {
                background: #2563eb;
                color: white;
            }

            .main {
                margin-left: 240px;
                padding: 30px;
            }

            .topbar {
                background: white;
                padding: 22px;
                border-radius: 14px;
                margin-bottom: 25px;
                box-shadow: 0 3px 12px #00000008;
            }

            .topbar h1 {
                margin: 0 0 8px;
                font-size: 27px;
            }

            .topbar p {
                margin: 0;
                color: #64748b;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 20px;
            }

            .card {
                background: white;
                padding: 25px;
                border-radius: 14px;
                box-shadow: 0 3px 12px #00000008;
                border-top: 5px solid #2563eb;
                transition: transform 0.2s;
            }

            .card:hover {
                transform: translateY(-4px);
            }

            .card h2 {
                font-size: 20px;
                margin-top: 0;
            }

            .card p {
                color: #64748b;
                line-height: 1.5;
            }

            .blue { border-color: #2563eb; }
            .green { border-color: #16a34a; }
            .purple { border-color: #9333ea; }
            .orange { border-color: #ea580c; }

            .btn {
                display: inline-block;
                background: #2563eb;
                color: white;
                text-decoration: none;
                padding: 11px 16px;
                border-radius: 7px;
                margin-top: 8px;
                font-size: 14px;
            }

            .green .btn { background: #16a34a; }
            .purple .btn { background: #9333ea; }
            .orange .btn { background: #ea580c; }

            .section-title {
                margin: 28px 0 18px;
            }

            .footer {
                margin-top: 30px;
                color: #64748b;
                font-size: 13px;
                text-align: center;
            }

            @media (max-width: 700px) {
                .sidebar {
                    position: static;
                    width: 100%;
                    height: auto;
                }

                .brand {
                    margin-bottom: 15px;
                }

                .main {
                    margin-left: 0;
                    padding: 18px;
                }

                .cards {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>

    <body>

        <div class="sidebar">
            <div class="brand">🎓 ExamSeat Pro</div>

            <a href="/">🏠 Dashboard</a>
            <a href="/add-student">👨‍🎓 Add Student</a>
            <a href="/bulk-upload">📁 Bulk Upload Students</a>
            <a href="/students-list">📋 Student List</a>
            <a href="/add-room">🏫 Add Exam Room</a>
            <a href="/generate">🪑 Generate Seating</a>
            <a href="/room-report">📊 Room Reports</a>
            <a href="/test-db">🔗 Test Database</a>
        </div>

        <div class="main">

            <div class="topbar">
                <h1>Exam Seating Dashboard</h1>
                <p>Smart Exam Seating Arrangement Management System</p>
            </div>

            <h2 class="section-title">Manage Your Examination</h2>

            <div class="cards">

                <div class="card blue">
                    <h2>👨‍🎓 Student Management</h2>
                    <p>Register students and view their details.</p>
                    <a class="btn" href="/add-student">Add Student</a>
                    <a class="btn" href="/students-list">View Students</a>
                </div>

                <div class="card green">
                    <h2>🏫 Room Management</h2>
                    <p>Add examination rooms and define their seating capacity.</p>
                    <a class="btn" href="/add-room">Manage Rooms</a>
                </div>

                <div class="card purple">
                    <h2>🪑 Seating Arrangement</h2>
                    <p>
                Generate seating using a Backtracking algorithm
                to prevent adjacent students from the same class.
                    </p>
                    <a class="btn" href="/generate">Generate Seating</a>
                </div>

                <div class="card orange">
                    <h2>📊 Room Capacity Report</h2>
                    <p>Check occupied seats, available seats and room capacity.</p>
                    <a class="btn" href="/room-report">View Reports</a>
                </div>

            </div>

            <div class="footer">
                ExamSeat Pro | Python • Flask • MySQL • DAA
            </div>

        </div>

    </body>
    </html>
    """


    return """
    <html>
    <head>
        <title>Exam Seating Optimizer</title>
    </head>
    <body style="font-family: Arial; text-align: center;">
        <h1>Exam Seating Arrangement Optimizer</h1>
        <p>Manage students, exam rooms, and seating arrangements.</p>

        <h2>Project Dashboard</h2>

        <p><a href="/add-student">Add Student</a></p>
        <p><a href="/add-room">Add Exam Room</a></p>
        <p><a href="/generate">Generate Seating Arrangement</a></p>
        <p><a href="/room-report">Room Capacity Report</a></p>
        <p><a href="/students-list">View All Students</a></p>
        <p><a href="/test-db">Test Database Connection</a></p>
    </body>
    </html>
    """

    

@app.route('/bulk-upload', methods=['GET', 'POST'])
def bulk_upload():

    if request.method == 'POST':

        file = request.files.get('file')

        if not file or file.filename == '':
            return "Please select an Excel file."

        if not file.filename.lower().endswith('.xlsx'):
            return "Please upload an .xlsx Excel file."

        try:
            # Read Excel file
            df = pd.read_excel(file, dtype=str)
            df.columns = df.columns.str.strip().str.lower()

            # Required columns
            required = ['roll_no', 'student_name', 'class_group']

            if not all(col in df.columns for col in required):
                return "Excel must contain: roll_no, student_name, class_group"

            # Select required columns and clean data
            df = df[required].fillna('')
            for col in required:
                df[col] = df[col].str.strip()

            # Remove completely empty rows
            df = df[df[required].ne('').any(axis=1)]

            # Check missing values
            if (df[required] == '').any().any():
                return "Some student records have missing values. Please correct Excel."

            # Remove duplicate roll numbers in Excel
            df = df.drop_duplicates(subset=['roll_no'])

            # Prepare records
            records = list(df.itertuples(index=False, name=None))

            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                INSERT IGNORE INTO students
                (roll_no, student_name, class_group)
                VALUES (%s, %s, %s)
            """

            cursor.executemany(query, records)

            imported = cursor.rowcount
            skipped = len(records) - imported

            conn.commit()
            cursor.close()
            conn.close()

            return f"""
                <h2>Excel Upload Successful!</h2>
                <p>Students Imported: {imported}</p>
                <p>Duplicate Records Skipped: {skipped}</p>
                <a href="/bulk-upload">Upload Another File</a>
            """

        except Exception as e:
            return f"Upload Error: {str(e)}"

    return """
        <h2>Bulk Upload Students</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".xlsx" required>
            <br><br>
            <button type="submit">Import Students</button>
        </form>
        <br>
        <a href="/">Back to Dashboard</a>
    """

if __name__ == "__main__":
    app.run(debug=True)