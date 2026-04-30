from flask import Flask, render_template, request, redirect, session
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "team_project_key"

# 👥 10 TEAM MEMBERS
users = [
    "Amit", "Rahul", "Neha", "Priya", "Rohan",
    "Simran", "Arjun", "Kavya", "Vijay", "Sonali"
]

tasks = []

# ---------------- HOME ROUTE (🔥 MISSING THA YE) ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        session["user"] = username
        return redirect("/dashboard")

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return redirect("/login")

    return render_template("signup.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    total = len(tasks)
    pending = len([t for t in tasks if t["status"] == "Pending"])
    progress = len([t for t in tasks if t["status"] == "In Progress"])
    done = len([t for t in tasks if t["status"] == "Done"])
    overdue = len([t for t in tasks if t["due"] < date.today() and t["status"] != "Done"])

    return render_template("dashboard.html",
                           user=session["user"],
                           tasks=tasks,
                           users=users,
                           total=total,
                           pending=pending,
                           progress=progress,
                           done=done,
                           overdue=overdue)


# ---------------- ADD TASK ----------------
@app.route("/add", methods=["POST"])
def add():
    task = {
        "title": request.form.get("title"),
        "assigned_to": request.form.get("assigned_to"),
        "status": request.form.get("status"),
        "due": datetime.strptime(request.form.get("due"), "%Y-%m-%d").date()
    }

    tasks.append(task)
    return redirect("/dashboard")


# ---------------- UPDATE STATUS ----------------
@app.route("/update/<int:id>/<status>")
def update(id, status):
    if 0 <= id < len(tasks):
        tasks[id]["status"] = status
    return redirect("/dashboard")


# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):
    if 0 <= id < len(tasks):
        tasks.pop(id)
    return redirect("/dashboard")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)