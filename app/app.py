import hashlib, os, sqlite3, subprocess
import requests
from flask import Flask, request, session, send_from_directory

app = Flask(__name__)
# F2 fix: read secret from environment variable
app.secret_key = os.environ.get("MEDICARE_SECRET_KEY", "default-lab-key") 
DB = "medicare.db"

def db():
    return sqlite3.connect(DB)

def require_role(*roles):
    def deco(fn):
        def wrapper(*a, **k):
            if session.get("role") not in roles:
                return "Forbidden", 403
            return fn(*a, **k)
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pw = request.form["password"]
    # F3 fix: MD5 replaced with werkzeug check_password_hash
    from werkzeug.security import check_password_hash
    sql = "SELECT id, role, pw FROM staff WHERE name = ?" # F1 fix: parameterized
    row = db().execute(sql, (user,)).fetchone()
    if row and check_password_hash(row[2], pw):
        session["role"] = row[1]
        session["uid"] = row[0]
        return "OK"
    return "Invalid"

@app.route("/patient")
@require_role("doctor", "nurse", "lab", "billing", "admin") # F7/F8 fix: Role matrix
def patient():
    pid = request.args.get("id")
    # F7 fix: IDOR ownership check (if a patient is logged in, they can only see their own record)
    if session.get("role") == "patient" and str(session.get("uid")) != pid:
        return "Forbidden", 403
    # F1 fix: parameterized query
    row = db().execute("SELECT name, diagnosis FROM patients WHERE id = ?", (pid,)).fetchone()
    return str(row)

@app.route("/prescription", methods=["POST"])
@require_role("doctor", "nurse") # F7/F8 fix
def prescription():
    db().execute("UPDATE rx SET dose = ? WHERE id = ?", (request.form["dose"], request.form["id"]))
    return "Updated"

@app.route("/labreport")
@require_role("doctor", "nurse", "lab", "admin") # F7/F8 fix
def labreport():
    # F4 fix (path traversal): Use send_from_directory and confine the path
    name = os.path.basename(request.args.get("file", ""))
    return send_from_directory("reports", name)

@app.route("/billing/export")
@require_role("billing", "admin") # F7/F8 fix
def export():
    # F4 fix (command injection): allow-list + list args, no shell=True
    ALLOWED = {"A", "B", "C"}
    ward = request.args.get("ward", "")
    if ward not in ALLOWED:
        return "Bad ward", 400
    return subprocess.check_output(["python", "export.py", ward])

@app.route("/pharmacy/stock")
@require_role("pharmacist", "admin")
def stock():
    return "stock list"

if __name__ == "__main__":
    # F5 & F6 fix: 127.0.0.1 and debug=False
    app.run(host="127.0.0.1", debug=False)