from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


async def get_by_email(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    db_obj = await session.scalar(query)
    return db_obj
