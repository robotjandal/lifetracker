from flask import (
    Blueprint,
    render_template,
)
from lifetracker.db import get_db

bp = Blueprint("goals", __name__)


@bp.route("/")
def index():
    """ Current goals are displayed."""
    db = get_db()
    goals = db.execute(
        "SELECT p.id, title, created, author_id, username"
        " FROM goals p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("goals/index.html", goals=goals)
