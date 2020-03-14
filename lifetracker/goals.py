from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort

from lifetracker.auth import login_required
from lifetracker.db import get_db

bp = Blueprint("goals", __name__)


def get_goal(id, check_author=True):
    """
        Get a goal by id and author.

        :param id: id of goal to get
        :param check_author: require the current user to be the author
        :return: the goal with author information
        :raise 404: if a goal with the given id doesn't exist
        :raise 403: if the current user isn't the author
    """
    goal = (
        get_db()
        .execute(
            "SELECT g.id AS goal_id, title, created, author_id, username"
            " FROM goals g JOIN user u ON g.author_id = u.id"
            " WHERE g.id = ?",
            (id,),
        )
        .fetchone()
    )

    if goal is None:
        abort(404, "Gost {0} doesn't exist.".format(id))

    if check_author and goal["author_id"] != g.user["id"]:
        abort(403)

    return goal


def fetch_goals(check_author=True):
    """
        Retrieve all goals for a user.
    """
    db = get_db()
    goals = db.execute(
        "SELECT g.id, title, created, author_id, username"
        " FROM goals g JOIN user u ON g.author_id = u.id"
        " WHERE u.id = ?"
        " ORDER BY created DESC",
        (g.user["id"],),
    ).fetchall()

    return goals


@bp.route("/goals")
def goals():
    """ Current goals are displayed."""
    # db = get_db()
    goals = fetch_goals()
    return render_template("goals/index.html", goals=goals)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """
        Create a new goal for the current user.
    """
    if request.method == "POST":
        title = request.form["title"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO goals (title, author_id)" " VALUES (?, ?)",
                (title, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("goals.goals"))

    return render_template("goals/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a goal if the current user is the author."""
    goal = get_goal(id)
    if request.method == "POST":
        title = request.form["title"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("UPDATE goals SET title = ? WHERE id = ?", (title, id))
            db.commit()
            return redirect(url_for("goals.goals"))

    return render_template("goals/update.html", goal=goal)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a goal.
    Ensures that the goal exists and that the logged in user is the
    author of the goal.
    """
    get_goal(id)
    db = get_db()
    db.execute("DELETE FROM goals WHERE id = ?", (id,))
    db.commit()

    return redirect(url_for("goals.goals"))
