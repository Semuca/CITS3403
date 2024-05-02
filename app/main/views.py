"""Main route views"""
from random import Random

from flask import Blueprint, render_template

from app.helpers import redirect_wrapper
from app.helpers.DatabaseManager import get_comments_by_thread_id, get_thread_by_id
from app.models import CommentModel

main_bp = Blueprint('main_bp', __name__)


@main_bp.route("/")
def home_page():
    """The home page"""

    return render_template('home.html')


@main_bp.route("/login")
def login_page():
    """The login page"""

    return render_template('login.html')


@main_bp.route("/register")
def signup_page():
    """The sign up page"""

    return render_template('register.html')


@main_bp.route("/forum")
def forum_page():
    """The trade forum page"""

    return redirect_wrapper(render_template('forum.html'))


@main_bp.route("/thread/<int:thread_id>")
def thread_page(thread_id):
    """The single thread page"""
    thread = get_thread_by_id(thread_id)
    comments = get_comments_by_thread_id(thread_id)
    # TODO (JARED): Fix this so it truly chooses your username
    rand = Random()
    for i in comments:
        i.username = rand.choice(["aeoniaa", "sellsol", "Semuca", "Jh1236", "fakename863", "b4d_at_c0d1ng"])
    comments = comments
    return redirect_wrapper(render_template('thread.html', thread_id=thread_id, thread=thread, comments=comments))
