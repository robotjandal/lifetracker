import pytest
from lifetracker.db import get_db


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    print(response.data)
    assert b"test title" in response.data
    assert b"by test on 2018-01-01" in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize("path", ("/2/update", "/2/delete"))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", })

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM goals ").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", })

    with app.app_context():
        db = get_db()
        goal = db.execute("SELECT * FROM goals WHERE id = 1").fetchone()
        assert goal["title"] == "updated"


@pytest.mark.parametrize("path", ("/create", "/1/update"))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", })
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "http://localhost/"

    with app.app_context():
        db = get_db()
        goal = db.execute("SELECT * FROM goals WHERE id = 1").fetchone()
    assert goal is None
