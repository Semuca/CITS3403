"""Main route views"""

from flask import Blueprint, render_template

from app.helpers import redirect_wrapper
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
    # TODO (Jared): Find a way to get this information without breaking the space time continuim
    from app import db, ThreadModel
    thread = db.session.get(ThreadModel, thread_id)
    comments = [i.comment_text for i in db.session.scalars(
        db.select(CommentModel)
        .where(CommentModel.thread_id == thread_id)
        .order_by(CommentModel.created_at.asc())
    ).all()]
    thread.comments = comments
    return redirect_wrapper(render_template('thread.html', thread_id=thread_id, thread=thread))
