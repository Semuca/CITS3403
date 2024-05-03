def get_posts_from_user(user_id: str):
    from app import db, ThreadModel
    return db.session.scalars(
        db.select(ThreadModel)
        .where(ThreadModel.user_id == user_id)
        .order_by(ThreadModel.created_at.asc())
    ).all()

def get_user_by_id(user_id):
    from app import db, UserModel
    user = db.session.scalars(
        db.select(UserModel)
        .where(UserModel.id == user_id)
    ).first()
    return user
