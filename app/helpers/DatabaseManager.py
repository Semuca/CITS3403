from app.models import CommentModel, ThreadModel, UserModel
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
    #TODO (JARED): hook this into the user endpoint when it exists
    user = db.session.scalars(
        db.select(UserModel)
        .where(UserModel.id == user_id)
    ).first()
    return user
