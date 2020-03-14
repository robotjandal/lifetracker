from flask import (
    Blueprint,
    render_template,
    g,
    redirect,
    url_for,
)

from lifetracker.auth import login_required

bp = Blueprint("home", __name__)


@bp.route("/")
@login_required
def index():
    """ Homepage is displayed."""
    return redirect(url_for("goals.goals"))

