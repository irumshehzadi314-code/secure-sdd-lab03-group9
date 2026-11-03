import hashlib, os, sqlite3, subprocess
import requests
from flask import Flask, request, session, send_file

app = Flask(__name__)
app.secret_key = "medicare-admin-123"
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
    h = hashlib.md5(pw.encode()).hexdigest()
    sql = "SELECT id, role FROM staff WHERE name = '%s' AND pw = '%s'" % (user, h)
    row = db().execute(sql).fetchone()
    if row:
        session["role"] = row[1]
        return "OK"
    return "Invalid"

@app.route("/patient")
def patient():
    pid = request.args.get("id")
    row = db().execute("SELECT name, diagnosis FROM patients WHERE id = %s" % (pid,)).fetchone()
    return str(row)

@app.route("/prescription", methods=["POST"])
def prescription():
    db().execute("UPDATE rx SET dose = ? WHERE id = ?", (request.form["dose"], request.form["id"]))
    return "Updated"

@app.route("/labreport")
def labreport():
    return send_file("reports/" + request.args.get("file"))

@app.route("/billing/export")
def export():
    return subprocess.check_output("python export.py " + request.args.get("ward"), shell=True)

@app.route("/pharmacy/stock")
@require_role("pharmacist", "admin")
def stock():
    return "stock list"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)