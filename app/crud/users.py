from uuid import UUID
from sqlalchemy.sql import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


async def authenticate(session: AsyncSession, email: str, password: str) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None

    if not verify_password(password, db_user.password):
        return None

    return db_user


async def get_all_user(session: AsyncSession) -> list[User]:
    query = select(User).where(User.is_deleted == False, User.is_active == True)
    users = await session.scalars(query)
    return list(users.all())


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    db_obj = await session.scalar(query)
    return db_obj


async def create_user(
    session: AsyncSession, user_create: UserCreate, is_staff=False
) -> User:
    db_obj = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        password=get_password_hash(user_create.password),
    )
    if is_staff:
        db_obj.is_staff = is_staff

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_user(
    session: AsyncSession, db_user: User, user_in: UserUpdate
) -> User:
    user_data = user_in.model_dump(exclude_unset=True)

    for var, value in user_data.items():
        setattr(db_user, var, value)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user(session: AsyncSession, user_id: UUID) -> User | None:
    db_users = await session.scalar(select(User).where(User.id == user_id))
    return db_users


async def total_users(session: AsyncSession) -> int:
    stmt = select(func.count(User.id)).where(User.is_deleted == False)
    return await session.scalar(stmt) or 0
