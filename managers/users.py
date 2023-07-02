from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from helpers import check_email, get_password_hash, signJWT, verify_password
from models import User

from . import BaseManager


class UserManager(BaseManager):
    def get_user_by_username(self, user: User, session: Session) -> User:
        user = session.query(User).filter_by(username=user.username).scalar()
        return user

    def create(self, user, session: Session) -> User:
        exist_user = self.get_user_by_username(user, session)
        if exist_user:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"User with username = {user.username} already exists!"
                },
            )
        verify_email = check_email(user.username)
        if not verify_email:
            raise HTTPException(status_code=400, detail={"error": f"Invalid email"})
        # hash password
        user.password = get_password_hash(user.password)
        new_user: User = super().create(user, session)
        return new_user

    def check_user(self, user, session: Session):
        current_user = self.get_user_by_username(user, session)
        if hasattr(current_user, "password"):
            current_password = verify_password(
                getattr(user, "password"), current_user.password
            )
        else:
            current_password = False

        if not (current_user and current_password):
            raise HTTPException(
                status_code=403, detail={"error": f"Invalid user credentials"}
            )
        else:
            return signJWT(current_user.id)


user_manager = UserManager(User)
