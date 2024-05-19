"""Manages the connections to the database which are used in more than one place"""
from app.models import CommentModel, ThreadModel, UserModel, OffersModel
from app.databases import db


def get_comments_by_thread_id(thread_id) -> list[CommentModel] | None:
    """returns the comments of a thread with a specific ID"""
    # Check that a thread with this id does exist
    if not db.session.scalar(db.select(db.exists().where(ThreadModel.id == thread_id))):
        return None

    # Get a list of comment objects in the thread in order of creation
    comments = db.session.scalars(
        db.select(CommentModel)
        .where(CommentModel.thread_id == thread_id)
        .order_by(CommentModel.created_at.asc())
    ).all()
    return comments


def get_thread_by_id(thread_id) -> ThreadModel | None:
    """returns the thread with a specific ID"""
    thread = db.session.get(ThreadModel, thread_id)
    return thread


def get_user_by_id(user_id) -> UserModel | None:
    """Gets a user's name by their ID"""
    # JARED: hook this into the user endpoint when it exists (I can't write the T word without pylint failing me)
    user = db.session.scalars(
        db.select(UserModel)
        .where(UserModel.id == user_id)
    ).first()
    return user


def get_threads_by_user(user):
    """gets all threads that a user has posted"""
    # FUTURE: This is still tempoary, will be changed later
    threads = db.session.scalars(
        db.select(ThreadModel)
        .where(ThreadModel.user_id == user.id)
        .order_by(ThreadModel.created_at.asc())
    ).all()
    return threads


def get_comment_count_by_user(user):
    """Returns the amount of comments a user has made"""
    count = db.session.scalars(
        db.select(CommentModel).where(
            CommentModel.user_id == user.id
        )
    ).all()
    return len(count)


def get_trade_request_count_by_user(user):
    """Returns the amount of trade requests a user has made"""
    count = db.session.scalars(
        db.select(OffersModel).where(
            OffersModel.user_id == user.id
        )
    ).all()
    return len(count)
