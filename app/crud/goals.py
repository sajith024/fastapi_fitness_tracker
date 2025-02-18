from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select

from app.models.goals import Goal
from app.models.users import User
from app.schemas.goals import GoalCreate, GoalUpdate


async def get_all_goals(
    session: AsyncSession, user: User, page: int, limit: int
) -> list[Goal]:
    page_limit = limit * page
    offset = (page - 1) * limit
    query = (
        select(Goal)
        .where(Goal.user == user, Goal.is_deleted == False)
        .offset(offset)
        .limit(page_limit)
    )
    db_objs = await session.scalars(query)
    return list(db_objs.all())


async def total_goals(session: AsyncSession, user: User) -> int:
    query = select(func.count(Goal.id)).where(
        Goal.user == user, Goal.is_deleted == False
    )
    db_obj = await session.scalar(query)
    return db_obj or 0


async def get_goal_by_id(
    session: AsyncSession, user: User, goal_id: UUID
) -> Goal | None:
    query = select(Goal).where(
        Goal.id == goal_id, Goal.user == user, Goal.is_deleted == False
    )

    goal = await session.scalar(query)
    return goal


async def create_goal(
    session: AsyncSession, user: User, workout_data: GoalCreate
) -> Goal:
    goal = Goal(
        target_exercise=workout_data.target_exercise,
        target_duration=workout_data.target_duration,
        target_calories=workout_data.target_calories,
        deadline=workout_data.deadline,
        user=user,
    )

    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    return goal


async def update_goal(session: AsyncSession, goal: Goal, goal_data: GoalUpdate) -> Goal:
    goal_dump = goal_data.model_dump(exclude_unset=True)

    for var, value in goal_dump.items():
        setattr(goal, var, value)

    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    return goal


async def delete_goal(session: AsyncSession, goal: Goal) -> None:
    goal.is_deleted = True
    session.add(goal)
    await session.commit()
