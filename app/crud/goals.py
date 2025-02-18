from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func, select

from app.models.goals import Goal
from app.models.users import User


async def get_goal_by_id(
    session: AsyncSession, user: User, goal_id: UUID
) -> Goal | None:
    query = select(Goal).where(
        Goal.id == goal_id, Goal.user == user, Goal.is_deleted == False
    )

    goal = await session.scalar(query)
    return goal
