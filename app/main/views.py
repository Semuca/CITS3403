"""Main route views"""

from flask import Blueprint, render_template, request

from app.helpers import redirect_wrapper, get_user_by_auth_header, database_manager

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
    thread.poster = database_manager.get_user_by_id(thread.user_id)
    comments = database_manager.get_comments_by_thread_id(thread_id)
    for i in comments:
        i.user = database_manager.get_user_by_id(i.user_id)
    return redirect_wrapper(render_template('thread.html', thread_id=thread_id, thread=thread, comments=comments))

#TODO: pls figure out the updated way to route to the profile page
@main_bp.route("/profile")
def profile_page():
    """The profile page"""
    print(request.headers)
    user = get_user_by_auth_header()

    # This is here temporarily to resolve merge conflict, will be done with changes to the user model later
    threads = []
    if user is not None:
        from app import db
        from app.models import ThreadModel
        threads = db.session.scalars(
            db.select(ThreadModel)
            .where(ThreadModel.user_id == user.id)
            .order_by(ThreadModel.created_at.asc())
        ).all()
    return redirect_wrapper(render_template('profile.html', posts=threads, user=user))
