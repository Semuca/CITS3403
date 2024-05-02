from app.models import CommentModel


def get_comments_by_thread_id(thread_id):
    from app import db
    comments = db.session.scalars(
        db.select(CommentModel)
        .where(CommentModel.thread_id == thread_id)
        .order_by(CommentModel.created_at.asc())
    ).all()
    return comments


def get_thread_by_id(thread_id):
    from app import db, ThreadModel
    thread = db.session.get(ThreadModel, thread_id)
    return thread
