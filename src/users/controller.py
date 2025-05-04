from src.db.core import DbSession
from . import model, service
from src.auth.service import CurrentUser
from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=model.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    return service.get_user_by_id(db, current_user.get_uuid())


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(current_user: CurrentUser, db: DbSession, password_change_request: model.PasswordChangeRequest):
    service.change_password(db, current_user.get_uuid(), password_change_request)