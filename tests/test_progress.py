import datetime
from lifetracker.db import get_db


# Testing disply of progress (history)
def test_static_history(client, auth):
    auth.login()
    response = client.get("/progress")
    assert b"Progress History" in response.data
    assert b"2018-01-02" in response.data
    assert b"First test goal" in response.data
    # test a single record is exists
    assert b"<td>5</td>" in response.data
    # test the record update takes the latest value
    assert b"<td>4</td>" in response.data
    # ensuring oldest date doesn't exist
    assert b"2018-01-01" not in response.data


def test_create(client, auth, app):
    auth.login()
    # using UTC dates as that is what the database stores
    today = datetime.datetime.utcnow().date()
    assert client.get("/progress/create").status_code == 200
    client.post("/progress/create", data={"id": [1, 2], "progress": [1, 5]})
    with app.app_context():
        db = get_db()
        # adding two records the second of which has progress value 5 tested
        # later
        row_count = db.execute("SELECT COUNT(id) FROM progress ").fetchone()[0]
        latest = db.execute(
            "SELECT goal_id, progress, date(created) as date, id \
                FROM progress ORDER BY progress.id DESC LIMIT 1"
        ).fetchone()
    assert row_count == 15
    # most recent progress result
    assert latest[1] == 5
    date = datetime.datetime.strptime(str(latest[2]), "%Y-%m-%d").date()
    assert date == today
