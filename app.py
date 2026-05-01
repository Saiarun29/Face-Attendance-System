from flask import Flask, render_template, request, redirect, session, flash
from register import register_user
from train_model import train_model
from attendance import start_recognition

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy teacher credentials
TEACHER_USERNAME = "admin"
TEACHER_PASSWORD = "1234"

@app.before_request
def clear_session_on_restart():
    if not hasattr(app, 'session_cleared'):
        session.clear()
        app.session_cleared = True

# 🔐 LOGIN PAGE
@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect('/home')
    return render_template("index.html")


# 🔐 LOGIN
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == TEACHER_USERNAME and password == TEACHER_PASSWORD:
        session['logged_in'] = True
        flash("✅ Login successful")
        return redirect('/home')
    else:
        flash("❌ Invalid credentials")
        return redirect('/')


# 🔐 LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# 🏠 CONTROL PANEL
@app.route('/home')
def main_home():
    if not session.get('logged_in'):
        return redirect('/')
    return render_template("home.html")


# 📸 REGISTER FACE
@app.route('/register', methods=['POST'])
def register():
    if not session.get('logged_in'):
        return redirect('/')

    name = request.form['name']
    register_user(name)

    flash("✅ Face registered successfully!")
    return redirect('/home')


# 🧠 TRAIN MODEL
@app.route('/train')
def train():
    if not session.get('logged_in'):
        return redirect('/')

    train_model()
    flash("🧠 Model trained successfully!")
    return redirect('/home')


# 🎥 START ATTENDANCE
@app.route('/start')
def start():
    if not session.get('logged_in'):
        return redirect('/')

    start_recognition()
    flash("🎥 Attendance completed!")
    return redirect('/home')


# 📊 DASHBOARD
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')

    from db import get_connection
    conn = get_connection()
    cursor = conn.cursor()

    today = "CURDATE()"

    # ✅ Present
    cursor.execute("""
        SELECT s.name, s.roll_no
        FROM students s
        JOIN users u ON s.name = u.name
        JOIN attendance a ON u.id = a.user_id
        WHERE DATE(a.time) = CURDATE()
    """)
    present = cursor.fetchall()

    # 🟡 Registered but Absent
    cursor.execute("""
        SELECT name, roll_no
        FROM students
        WHERE registered = TRUE
        AND name NOT IN (
            SELECT u.name
            FROM users u
            JOIN attendance a ON u.id = a.user_id
            WHERE DATE(a.time) = CURDATE()
        )
    """)
    absent = cursor.fetchall()

    # 🔴 Not Registered
    cursor.execute("""
        SELECT name, roll_no
        FROM students
        WHERE registered = FALSE
    """)
    not_registered = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        present=present,
        absent=absent,
        not_registered=not_registered
    )


# 🚀 RUN APP
if __name__ == '__main__':
    app.run(debug=True)