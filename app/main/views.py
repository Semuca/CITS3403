"""Main route views"""

from flask import Blueprint, render_template

from app.helpers import redirect_wrapper

main_bp = Blueprint('main_bp', __name__)


@main_bp.route("/")
def hello_world():
    """A test 'hello world' function"""

    return "<p>Hello, World!</p>"


@main_bp.route("/login")
def login_page():
    """The login page"""

    return render_template('login.html')


@main_bp.route("/register")
def signup_page():
    """The sign up page"""

    return render_template('register.html')


@main_bp.route("/forum/create")
def create_thread_page():
    """The trade forum page"""

    return redirect_wrapper(render_template('forum.html'))


@main_bp.route("/forum")
def forum_page():
    """The trade forum page"""

    return redirect_wrapper(render_template('view_all_threads.html'))


@main_bp.route("/thread/<int:thread_id>")
def thread_page(thread_id):
    """The single thread page"""

    return redirect_wrapper(render_template('thread.html', thread_id=thread_id))
