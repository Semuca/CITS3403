"""Main route views"""

from flask import Blueprint, render_template, request, redirect

from app.helpers import redirect_wrapper, get_user_by_token, database_manager
from app.models.inventory import INVENTORY_CATEGORIES

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
    thread = database_manager.get_thread_by_id(thread_id)

    if thread is None:
        return redirect("/forum")

    thread.poster = database_manager.get_user_by_id(thread.user_id)
    comments = database_manager.get_comments_by_thread_id(thread_id)
    for i in comments:
        i.user = database_manager.get_user_by_id(i.user_id)
    return redirect_wrapper(render_template('thread.html', thread_id=thread_id, thread=thread, comments=comments))


@main_bp.route("/profile")
def profile_page():
    """The profile page"""
    user = get_user_by_token(request.cookies.get('token'))
    threads = []
    if user is not None:
        threads = database_manager.get_threads_by_user(user)
    return redirect_wrapper(render_template('profile.html', posts=threads, user=user))


@main_bp.route("/game")
def game_page():
    """The game page"""
    user = get_user_by_token(request.cookies.get('token'))

    if user is None: # needs to be done first since the game template uses user attributes
        return redirect("/login")

    # using [*enumerate(items)] so that we can use the iterator more than once
    return render_template('game.html', user=user, items=[*enumerate(INVENTORY_CATEGORIES)])
