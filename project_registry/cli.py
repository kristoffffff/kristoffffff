from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List

from .models import (
    DEFAULT_GOALS,
    DEFAULT_IMPACT_AREAS,
    DEFAULT_ROLE_LABELS,
    DEFAULT_ROLES,
    Link,
    Project,
    Risk,
    Stakeholder,
)

PROJECTS_FILE = Path("projects.json")


def prompt_date(label: str) -> datetime:
    while True:
        value = input(f"{label} (YYYY-MM-DD): ")
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Érvénytelen dátum formátum.")


def prompt_goals() -> List[str]:
    goals = []
    print("Elérhető célok:")
    for idx, goal in enumerate(DEFAULT_GOALS, 1):
        print(f"{idx}. {goal}")
    print("Válassza ki a célokat vesszővel elválasztva vagy adjon meg újakat.")
    selection = input("Célok: ")
    if selection.strip():
        for part in selection.split(","):
            part = part.strip()
            if part.isdigit() and 1 <= int(part) <= len(DEFAULT_GOALS):
                goals.append(DEFAULT_GOALS[int(part) - 1])
            elif part:
                goals.append(part)
    return goals


def prompt_stakeholders() -> List[Stakeholder]:
    stakeholders: List[Stakeholder] = []
    mandatory = ["Szponzor", "Projektvezető"]
    for role in mandatory:
        stakeholders.append(prompt_stakeholder(role))

    print("További szerepkörök, választhat a listából vagy adjon meg újat.")
    while True:
        for idx, role in enumerate(DEFAULT_ROLES, 1):
            print(f"{idx}. {role}")
        role_input = input("Szerepkör (üres a befejezéshez): ")
        if not role_input:
            break
        if role_input.isdigit() and 1 <= int(role_input) <= len(DEFAULT_ROLES):
            role = DEFAULT_ROLES[int(role_input) - 1]
        else:
            role = role_input
        stakeholders.append(prompt_stakeholder(role))
    return stakeholders


def prompt_stakeholder(role: str) -> Stakeholder:
    display_name = input(f"{role} neve: ") or "N/A"
    email = input("Email (opcionális): ") or None
    print("Címkék:")
    for idx, label in enumerate(DEFAULT_ROLE_LABELS, 1):
        print(f"{idx}. {label}")
    labels_input = input("Válasszon címkéket vesszővel elválasztva vagy adjon meg újakat: ")
    labels: List[str] = []
    if labels_input.strip():
        for part in labels_input.split(","):
            part = part.strip()
            if part.isdigit() and 1 <= int(part) <= len(DEFAULT_ROLE_LABELS):
                labels.append(DEFAULT_ROLE_LABELS[int(part) - 1])
            elif part:
                labels.append(part)
    dedication = input("Dedikáció (FTE): ")
    dedication_fte = float(dedication) if dedication else None
    return Stakeholder(role=role, display_name=display_name, email=email, labels=labels, dedication_fte=dedication_fte)


def prompt_risks() -> List[Risk]:
    risks: List[Risk] = []
    print("Adjon meg kockázatokat (enter a befejezéshez).")
    while True:
        description = input("Kockázat leírása: ")
        if not description:
            break
        probability = int(input("Valószínűség (1-4): "))
        print("Hatásterületek:")
        for idx, area in enumerate(DEFAULT_IMPACT_AREAS, 1):
            print(f"{idx}. {area}")
        area_input = input("Válasszon hatásterületet vagy adjon meg újat: ")
        if area_input.isdigit() and 1 <= int(area_input) <= len(DEFAULT_IMPACT_AREAS):
            impact_area = DEFAULT_IMPACT_AREAS[int(area_input) - 1]
        else:
            impact_area = area_input
        severity = int(input("Hatás súlyossága (1-4): "))
        risks.append(
            Risk(
                description=description,
                probability=probability,
                impact_area=impact_area,
                severity=severity,
            )
        )
    return risks


def prompt_assumptions() -> List[str]:
    assumptions: List[str] = []
    print("Adjon meg feltételezéseket (enter a befejezéshez).")
    while True:
        assumption = input("Feltételezés: ")
        if not assumption:
            break
        assumptions.append(assumption)
    return assumptions


def prompt_links() -> List[Link]:
    links: List[Link] = []
    print("Adjon meg linkeket (enter a befejezéshez).")
    while True:
        description = input("Leírás: ")
        if not description:
            break
        url = input("URL: ")
        links.append(Link(description=description, url=url))
    return links


def add_project() -> Project:
    start_date = prompt_date("Tervezett kezdés")
    end = input("Tervezett zárás (YYYY-MM-DD) vagy hagyja üresen: ")
    end_date = datetime.strptime(end, "%Y-%m-%d").date() if end else None
    duration = None
    if not end_date:
        duration_input = input("Időtartam hónapokban: ")
        duration = int(duration_input) if duration_input else None
    goals = prompt_goals()
    stakeholders = prompt_stakeholders()
    budget_input = input("Projekt büdzséje: ")
    budget = float(budget_input) if budget_input else None
    approved_input = input("Büdzsé jóváhagyva? (igen/nem): ").lower()
    budget_approved = approved_input.startswith("i")
    risks = prompt_risks()
    assumptions = prompt_assumptions()
    links = prompt_links()
    project = Project(
        start_date=start_date.date(),
        end_date=end_date,
        duration_months=duration,
        goals=goals,
        stakeholders=stakeholders,
        budget=budget,
        budget_approved=budget_approved,
        risks=risks,
        assumptions=assumptions,
        links=links,
    )
    projects = load_projects()
    projects.append(project)
    save_projects(projects)
    print("Projekt elmentve.")
    return project


def load_projects() -> List[Project]:
    if not PROJECTS_FILE.exists():
        return []
    data = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    projects: List[Project] = []
    for item in data:
        project = Project(
            start_date=datetime.strptime(item["start_date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(item["end_date"], "%Y-%m-%d").date()
            if item.get("end_date")
            else None,
            duration_months=item.get("duration_months"),
            goals=item.get("goals", []),
            stakeholders=[Stakeholder(**s) for s in item.get("stakeholders", [])],
            budget=item.get("budget"),
            budget_approved=item.get("budget_approved", False),
            risks=[Risk(**r) for r in item.get("risks", [])],
            assumptions=item.get("assumptions", []),
            links=[Link(**l) for l in item.get("links", [])],
        )
        projects.append(project)
    return projects


def save_projects(projects: List[Project]) -> None:
    data = []
    for p in projects:
        data.append(
            {
                "start_date": p.start_date.isoformat(),
                "end_date": p.end_date.isoformat() if p.end_date else None,
                "duration_months": p.duration_months,
                "goals": p.goals,
                "stakeholders": [s.__dict__ for s in p.stakeholders],
                "budget": p.budget,
                "budget_approved": p.budget_approved,
                "risks": [r.__dict__ for r in p.risks],
                "assumptions": p.assumptions,
                "links": [l.__dict__ for l in p.links],
            }
        )
    PROJECTS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    add_project()
