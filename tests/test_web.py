from project_registry import web, cli
import json


def test_index_page(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "PROJECTS_FILE", tmp_path / "projects.json")
    client = web.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


def test_add_project(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "PROJECTS_FILE", tmp_path / "projects.json")
    client = web.app.test_client()
    data = {
        "start_date": "2024-01-01",
        "duration_months": "6",
        "goals": "Teszt",
        "sponsor_name": "Szponzor",
        "manager_name": "PM",
    }
    resp = client.post("/add", data=data, follow_redirects=True)
    assert resp.status_code == 200
    stored = json.loads((tmp_path / "projects.json").read_text(encoding="utf-8"))
    assert stored[0]["duration_months"] == 6
