from flask import (
    Blueprint,
    current_app,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

import datetime
from lifetracker.db import get_db
from lifetracker.goals import fetch_goals

bp = Blueprint("progress", __name__)


def get_recent_progress(goal_id, history_num, check_author=True):
    """
        Get recent progress on a goal by goal based on returning
        latest recorded progress per day.

        :param goal_id: id of goal
        :param history_num: number of past progress dates and values to return
        :return: the past progress with goal id and author

        Note: currently there is no check against author or goal.
    """
    progress_recent = (
        get_db()
        .execute(
            "SELECT progress.id AS progress_id, \
            progress, goal_id, date(progress.created) AS date"
            " FROM progress"
            " WHERE goal_id = ?"
            " GROUP BY date"
            " HAVING MAX(progress.id)"
            " ORDER BY progress.id DESC"
            " LIMIT ?",
            (goal_id, history_num),
        )
        .fetchall()
    )
    return progress_recent


def organise_history():  # including direction of output etc
    num_past_progress = 5
    progress_table = []
    recent_dates = set()
    inter_table = []  # list of dictionaries TODO: improve name
    goals = fetch_goals()
    current_app.logger.debug("Retrieving progress")
    for goal in goals:
        progress_data = get_recent_progress(goal[0], num_past_progress)
        goal_dict = {"Description": goal[1]}
        # Collate progress per date with goal title
        for row in progress_data:
            current_app.logger.debug(
                "goal %s, date %s: value %s", goal[0], row[3], row[1]
            )
            row_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
            recent_dates.add(row_date)
            goal_dict.update({row_date: row[1]})
        inter_table.append(goal_dict)
    sorted_dates = sorted(recent_dates)[-num_past_progress:]
    header = ["Description"]
    header.extend(sorted_dates)
    # format data for display in table
    current_app.logger.debug("header: %s", header)
    for goal in inter_table:
        row = list()
        row.clear()
        row.append(goal["Description"])
        for date in sorted_dates:
            if date in goal_dict:
                row.append(goal[date])
            else:
                row.append("")
        progress_table.append(row)
    return header, progress_table


@bp.route("/progress", methods=("GET",))
def index():
    """
        Display progress for the last five days.
    """
    # create a row based table based on the goal description and each date's
    # progress value for each goal
    # this includes a row for the headers: Goal, Date1, Date2 etc
    header, progress_table = organise_history()
    return render_template(
        "progress/index.html", header=header, progress_history=progress_table
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
