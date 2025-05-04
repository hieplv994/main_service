from src.auth.service import verify_password, get_password_hash
import logging
from uuid import UUID
from . import model
from src.entities.user import User

def get_user_by_id(db, user_id: UUID) -> model.UserResponse | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"User with id {user_id} not found")
        raise Exception("User not found")
    return user

def change_password(db, user_id: UUID, password_change_request: model.PasswordChangeRequest) -> bool:
    try:
        user = get_user_by_id(db, user_id)
        if not verify_password(password_change_request.old_password, user.hashed_password):
            logging.warning(f"Failed to change password for user {user_id}: old password is incorrect")
            raise Exception("Old password is incorrect")
        if password_change_request.new_password != password_change_request.confirm_password:
            logging.warning(f"Failed to change password for user {user_id}: new password and confirm password do not match")
            raise Exception("New password and confirm password do not match")
        user.hashed_password = get_password_hash(password_change_request.new_password)
        db.commit()
        logging.info(f"Password changed for user {user_id}")
        return True
    except Exception as e:
        logging.error(f"Failed to change password for user {user_id}: {str(e)}")
        return False