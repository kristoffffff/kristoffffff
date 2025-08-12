from __future__ import annotations

from datetime import date
from flask import Flask, render_template, request, redirect, url_for

from .models import Project, Stakeholder
from . import cli

app = Flask(__name__)


@app.route("/")
def index():
    projects = cli.load_projects()
    return render_template("index.html", projects=projects)


@app.route("/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        start_date = date.fromisoformat(request.form["start_date"])
        end_date_str = request.form.get("end_date")
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        duration_str = request.form.get("duration_months")
        duration_months = int(duration_str) if duration_str else None
        goals = [g.strip() for g in request.form.get("goals", "").split(",") if g.strip()]
        sponsor_name = request.form.get("sponsor_name", "")
        sponsor_email = request.form.get("sponsor_email") or None
        manager_name = request.form.get("manager_name", "")
        manager_email = request.form.get("manager_email") or None
        stakeholders = [
            Stakeholder(role="Szponzor", display_name=sponsor_name, email=sponsor_email),
            Stakeholder(role="Projektvezető", display_name=manager_name, email=manager_email),
        ]
        budget_str = request.form.get("budget")
        budget = float(budget_str) if budget_str else None
        budget_approved = bool(request.form.get("budget_approved"))
        assumptions = [
            a.strip()
            for a in request.form.get("assumptions", "").splitlines()
            if a.strip()
        ]
        project = Project(
            start_date=start_date,
            end_date=end_date,
            duration_months=duration_months,
            goals=goals,
            stakeholders=stakeholders,
            budget=budget,
            budget_approved=budget_approved,
            assumptions=assumptions,
        )
        projects = cli.load_projects()
        projects.append(project)
        cli.save_projects(projects)
        return redirect(url_for("index"))
    return render_template("add_project.html")


if __name__ == "__main__":
    app.run(debug=True)
