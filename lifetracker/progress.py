from flask import (
    Blueprint,
    current_app,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_table import create_table, Table, Col

from lifetracker.db import get_db
from lifetracker.goals import fetch_goals

bp = Blueprint("progress", __name__)


class ProgressTable(Table):
    name = Col('Goal')
    description = Col('Description')


def get_recent_progress_by_goal(goal_id, dates, offset=0, check_author=True):
    """
        Get recent progress for a goal over a set number of dates.

        : param limit: number of dates to return
        : param offset: page to display (paginiation)
        : return: a table with columns as dates and goals as rows
    """
    sql_query = (
        "SELECT p.id AS progress_id, progress, goal_id, date(p.created) AS "
        + " date, g.title"
        + " FROM progress p JOIN user u ON p.author_id = u.id"
        + " JOIN goals g ON p.goal_id = g.id"
        + " WHERE u.id = ? AND p.goal_id = ? AND date IN (%s)"
        % ",".join("?" * len(dates))
    )
    arguments = (g.user["id"], goal_id) + tuple(dates)
    progress = get_db().execute(sql_query, arguments).fetchall()
    if progress is None:
        return None
    else:
        return progress


def fetch_progress_dates(limit, offset=0, check_author=True):
    """
        Get the recent dates during which progress has been written.

        :param limit: number of results to return
        :param offset: which page of results to display
        :return: the past progress dates as a list

    """
    progress_dates = (
        get_db()
        .execute(
            "SELECT DISTINCT DATE(created) as date, author_id"
            " FROM progress p JOIN user u ON p.author_id = u.id"
            " WHERE u.id = ?"
            " ORDER BY date DESC"
            " LIMIT ?",
            (g.user["id"], limit),
        )
        .fetchall()
    )
    return [row["date"] for row in progress_dates]


def progress_table():
    """
    Assemble progress table fetching goals, then progress results by id.
    The assembled table is then returned.
    """
    output = []
    limit = 5
    goals = fetch_goals()
    progress_dates = fetch_progress_dates(limit)
    TableCls = create_table("Progress").add_column("Goal", Col("Goal"))
    # create table columns
    for row in progress_dates:
        TableCls.add_column(row, Col(row))

    for row in goals:
        goal_progress = get_recent_progress_by_goal(row["id"], progress_dates, 5)
        if goal_progress is not None:
            # collate progress into a dictionary
            output_dictionary = {"Goal": goal_progress[0]["title"]}
            for row in goal_progress:
                output_dictionary[row["date"]] = row["progress"]
            # add remaining keys not found
            for row in progress_dates:
                if row not in output_dictionary.keys():
                    output_dictionary[row] = None
            # append to output list
            output.append(output_dictionary)
    # build table
    table = TableCls(output, no_items="-")
    return table


@bp.route("/progress", methods=("GET",))
def index():
    """
        Display progress for the last five days.
    """
    # create a row based table based on the goal description and each date's
    # progress value for each goal
    # this includes a row for the headers: Goal, Date1, Date2 etc
    table = progress_table()
    return render_template(
        "progress/index.html", table=table
    )


@bp.route("/progress/create", methods=("GET", "POST"))
def create():
    """
        Progress can be added to any/all goal(s) displayed.
    """
    goals = fetch_goals()
    if request.method == "POST":
        data_id = request.form.getlist("id")
        data_progress = request.form.getlist("progress")
        data = {int(k): int(v) for k, v in zip(data_id, data_progress)}
        db = get_db()
        for goal, progress in data.items():
            db.execute(
                "INSERT INTO progress (author_id, goal_id, progress) "
                " VALUES (?, ?, ?)",
                (g.user["id"], goal, progress),
            )
        db.commit()
        return redirect(url_for("progress.index"))

    return render_template("progress/create.html", goals=goals)
